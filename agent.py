import os
import imaplib
import email
from email.header import decode_header
from google import genai
from google.genai import types

# =====================================================================
# 1. INITIALIZATION & CREDENTIALS
# =====================================================================
# This is your exact valid key from image_7982b9.jpg
API_KEY = "my key"
client = genai.Client(api_key=API_KEY)

# =====================================================================
# 2. LOCAL TOOL FUNCTIONS
# =====================================================================
def read_latest_emails() -> str:
    """
    Simulates reading the latest unread emails for testing the agent workflow.
    """
    print("📨 [MOCK TOOL] Simulating email fetching...")
    return """
FROM: hr@techcorp.com
SUBJECT: Technical Interview Scheduled
CONTENT: Dear Mehria, we are pleased to invite you for an interview. 
The event is confirmed for June 18, 2026 at 14:00 PM. Please be online.
---
"""

def create_calendar_file(event_title: str, date_yyyymmdd: str, time_hhmmss: str, description: str) -> str:
    """
    Creates a standard universal .ics calendar event file in the project folder.
    """
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//AI Event Agent//EN
BEGIN:VEVENT
SUMMARY:{event_title}
DTSTART:{date_yyyymmdd}T{time_hhmmss}
DESCRIPTION:{description}
END:VEVENT
END:VCALENDAR"""
    
    filename = "appointment.ics"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(ics_content.strip())
        
    print(f"📅 [SUCCESS] Calendar file written locally to: {filename}")
    return f"Success: Created calendar file {filename}."

# Dictionary mapping for the local execution loop
available_tools = {
    "read_latest_emails": read_latest_emails,
    "create_calendar_file": create_calendar_file
}

# =====================================================================
# 3. AGENT PIPELINE RUNNER
# =====================================================================
user_prompt = (
    "First, use the read_latest_emails tool to check for unread messages. "
    "Carefully review the text. You will find an interview event inside it. "
    "Extract its details and run the create_calendar_file tool immediately to save it."
)

print("🚀 Launching Unified Autonomous Agent Pipeline...")

# Step A: Ask Gemini what tool it wants to execute
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=user_prompt,
    config=types.GenerateContentConfig(
        tools=[read_latest_emails, create_calendar_file], 
    )
)

# Step B: Handle the execution path if a tool function call is made
if response.function_calls:
    for call in response.function_calls:
        tool_name = call.name
        tool_args = call.args
        
        print(f"🤖 Gemini requested tool execution: {tool_name}")
        
        if tool_name in available_tools:
            # Execute the function locally on your computer
            tool_output = available_tools[tool_name](**tool_args)
            
            # Send the data back to Gemini so it knows the tool succeeded
            final_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"The tool {tool_name} was run and returned: '{tool_output}'. Provide your final status response.",
            )
            print("\n--- Pipeline Completed ---")
            print(final_response.text)
else:
    print("\n--- Pipeline Completed ---")
    print(response.text)
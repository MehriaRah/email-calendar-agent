
# 📅 Email-to-Calendar Autonomous Agent

An AI-driven automation pipeline that parses inbox messages and converts interview or event details into standard `.ics` calendar files using the **Google GenAI SDK (`google-genai`)** and **Gemini 2.5 Flash**.

The agent inspects emails, identifies dates and event details using natural language reasoning, and automatically triggers local execution functions via native model tool calling.

---

## 🌟 Key Features

* **Native Model Tool Calling:** Employs `google.genai.types.GenerateContentConfig` to register custom Python functions directly with `gemini-2.5-flash`.
* **Automated Data Extraction:** Converts raw email contents (subjects, senders, dates, times) into structured parameters for event creation.
* **ICS Calendar Generation:** Dynamically builds RFC 5545-compliant iCalendar files (`.ics`) for local integration with calendar software (Apple Calendar, Google Calendar, Outlook).
* **Multi-Step Execution Loop:** Demonstrates a closed-loop agent workflow from data retrieval to automated local filesystem operations.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.10+
* **AI Model:** Gemini 2.5 Flash (`gemini-2.5-flash`)
* **SDK:** Official Google GenAI SDK (`google-genai`)
* **Protocols & Standards:** iCalendar (RFC 5545), Python `imaplib`/`email` standard modules

---

## 🚀 Getting Started

### Prerequisites

1. Python 3.10 or higher installed.
2. A Google Cloud Gemini API key.

### Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/email-calendar-agent.git](https://github.com/your-username/email-calendar-agent.git)
   cd email-calendar-agent

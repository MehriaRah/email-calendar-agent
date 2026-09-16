import imaplib
import email
from email.header import decode_header

def read_latest_emails() -> str:
    """
    Connects to the Gmail inbox and reads the text of the newest unread emails.
    
    Returns:
        str: A concatenated string containing email senders, subjects, and contents.
    """
    my_email = "mehria.rah@gmail.com"
    app_password = "uicp qmbm qhmh xfmh" 
    
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(my_email, app_password)
        mail.select("INBOX") 
        
        # Search for unread messages safely
        status, messages = mail.search(None, '(UNREAD)')
        mail_ids = messages[0].split()
        
        if not mail_ids:
            mail.logout()
            return "No new unread emails found."
            
        latest_ids = mail_ids[-5:]
        email_summaries = []
        
        for e_id in reversed(latest_ids):
            status, data = mail.fetch(e_id, '(RFC822)')
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Extract Subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")
                    
                    sender = msg.get("From")
                    
                    # Extract Body (Supporting both Plain Text and HTML formats)
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            if content_type in ["text/plain", "text/html"]:
                                payload = part.get_payload(decode=True)
                                if payload:
                                    body = payload.decode(errors="ignore")[:1000]
                                    break
                    else:
                        payload = msg.get_payload(decode=True)
                        if payload:
                            body = payload.decode(errors="ignore")[:1000]
                        
                    email_summaries.append(f"FROM: {sender}\nSUBJECT: {subject}\nCONTENT: {body}\n---")
                    
        mail.logout()
        return "\n".join(email_summaries)
        
    except Exception as e:
        return f"Error reading emails safely: {e}"
"""
Script to simulate or send email invitation for Banki Kuu SACCO 58th AGM.
Target Recipient: sam.gathigi@gmail.com
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

RECIPIENT = "sam.gathigi@gmail.com"
SUBJECT = "[CONFIDENTIAL] Official AGM Invitation & Encrypted Digital Pass — Samuel Gathigi (Member #342801)"

HTML_FILE = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e\Banki_Kuu_SACCO_AGM_Invitation_Email.html"

def read_html():
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        return f.read()

def main():
    html_content = read_html()
    print("=== EMAIL DISPATCH SIMULATION ===")
    print(f"To: {RECIPIENT}")
    print(f"Subject: {SUBJECT}")
    print(f"Link 1 (Confirm Pass): https://cbk-stride.streamlit.app/BKS?confirm=TKT-BK-342801&name=Samuel+Gathigi")
    print(f"Link 2 (Direct Vote Booth): https://cbk-stride.streamlit.app/BKS?vote_tkt=TKT-BK-342801")
    print("=" * 40)
    
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    
    if smtp_user and smtp_pass:
        print(f"Attempting live SMTP dispatch to {RECIPIENT} via {smtp_host}:{smtp_port}...")
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = SUBJECT
            msg["From"] = f"Banki Kuu SACCO Secretariat <{smtp_user}>"
            msg["To"] = RECIPIENT
            
            part = MIMEText(html_content, "html")
            msg.attach(part)
            
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, RECIPIENT, msg.as_string())
            server.quit()
            print("SUCCESS: EMAIL DISPATCH COMPLETED!")
        except Exception as e:
            print(f"SMTP Dispatch Error: {e}")
    else:
        print("NOTE: Live SMTP credentials not set; simulation ready.")

if __name__ == "__main__":
    main()

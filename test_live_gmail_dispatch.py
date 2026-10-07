"""
Live Email Dispatcher & Integration Test Script for Banki Kuu SACCO.
Supports sending via Gmail SMTP or custom SACCO Exchange / SMTP servers.
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Target recipient for test simulation
RECIPIENT = os.environ.get("TEST_RECIPIENT", "sam.gathigi@gmail.com")
SUBJECT = "[CONFIDENTIAL] Official AGM Invitation & Encrypted Digital Pass — Samuel Gathigi (Member #342801)"

HTML_FILE = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e\Banki_Kuu_SACCO_AGM_Invitation_Email.html"

def read_html():
    if os.path.exists(HTML_FILE):
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return """<!DOCTYPE html><html><body><h2>Banki Kuu SACCO 58th AGM Pass</h2><a href="https://cbk-stride.streamlit.app/BKS?confirm=TKT-BK-342801">Confirm Pass</a></body></html>"""

def dispatch():
    html_content = read_html()
    
    smtp_user = os.environ.get("SMTP_USER", "")
    smtp_pass = os.environ.get("SMTP_PASS", "")
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    sender_display = os.environ.get("SENDER_DISPLAY", f"Banki Kuu SACCO Secretariat <{smtp_user}>")

    print("==================================================")
    print("🏦 BANKI KUU SACCO EMAIL DISPATCH SIMULATOR")
    print("==================================================")
    print(f"Target Recipient : {RECIPIENT}")
    print(f"SMTP Host        : {smtp_host}:{smtp_port}")
    print(f"Sender Display   : {sender_display}")
    print("--------------------------------------------------")

    if not smtp_user or not smtp_pass:
        print("💡 SMTP Credentials Not Detected in Environment.")
        print("\nTo send a live test email from your Gmail to yourself:")
        print("1. Set environment variables in PowerShell:")
        print("   $env:SMTP_USER='your-gmail@gmail.com'")
        print("   $env:SMTP_PASS='your-gmail-app-password'")
        print("   $env:TEST_RECIPIENT='sam.gathigi@gmail.com'")
        print("2. Re-run this script!")
        print("\nTo share with SACCO IT Admin for their mail server:")
        print("   $env:SMTP_HOST='smtp.office365.com'")
        print("   $env:SMTP_USER='secretariat@bankikuusacco.co.ke'")
        print("   $env:SMTP_PASS='SACCO_ADMIN_PASS'")
        return

    print(f"Sending live email to {RECIPIENT}...")
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = SUBJECT
        msg["From"] = sender_display
        msg["To"] = RECIPIENT

        part = MIMEText(html_content, "html")
        msg.attach(part)

        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, RECIPIENT, msg.as_string())
        server.quit()
        print("✅ SUCCESS: Live email dispatched! Check your inbox.")
    except Exception as e:
        print(f"❌ SMTP Dispatch Error: {e}")

if __name__ == "__main__":
    dispatch()

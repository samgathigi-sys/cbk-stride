"""
Batch Email Invitation Dispatcher for Banki Kuu Staff SACCO 58th AGM.
Registers 10 delegate tickets in SQLite database and dispatches personalized emails.
"""

import os
import sys
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import utils
from utils import AttendanceBackend

backend = AttendanceBackend()

# Ensure Banki Kuu SACCO event exists
EVENT_ID = "EVT-BANKI-KUU-SACCO"
backend.ensure_banki_kuu_sacco_event()

# 10 Representative Delegates for Banki Kuu SACCO
DELEGATES = [
    {"name": "Samuel Gathigi", "member_id": "SACCO-342801", "ticket_id": "TKT-BK-342801", "email": "sam.gathigi@gmail.com", "dept": "IT & Digital Services"},
    {"name": "Dr. Beatrice Kiptoo", "member_id": "SACCO-342802", "ticket_id": "TKT-BK-342802", "email": "sam.gathigi+beatrice@gmail.com", "dept": "Internal Audit"},
    {"name": "Capt. Geoffrey Kemboi", "member_id": "SACCO-342803", "ticket_id": "TKT-BK-342803", "email": "sam.gathigi+geoffrey@gmail.com", "dept": "Banking Operations"},
    {"name": "Joyce Cheruiyot", "member_id": "SACCO-342804", "ticket_id": "TKT-BK-342804", "email": "sam.gathigi+joyce@gmail.com", "dept": "Finance & Accounts"},
    {"name": "Stanley Gicho", "member_id": "SACCO-342805", "ticket_id": "TKT-BK-342805", "email": "sam.gathigi+stanley@gmail.com", "dept": "Human Resources"},
    {"name": "Mary Wambui", "member_id": "SACCO-342806", "ticket_id": "TKT-BK-342806", "email": "sam.gathigi+mary@gmail.com", "dept": "Legal & Secretariat"},
    {"name": "David Kiiru", "member_id": "SACCO-342807", "ticket_id": "TKT-BK-342807", "email": "sam.gathigi+david@gmail.com", "dept": "Monetary Policy"},
    {"name": "Linda Otieno", "member_id": "SACCO-342808", "ticket_id": "TKT-BK-342808", "email": "sam.gathigi+linda@gmail.com", "dept": "Financial Markets"},
    {"name": "Eric Mwangi", "member_id": "SACCO-342809", "ticket_id": "TKT-BK-342809", "email": "sam.gathigi+eric@gmail.com", "dept": "Currency Logistics"},
    {"name": "Grace Mutisya", "member_id": "SACCO-342810", "ticket_id": "TKT-BK-342810", "email": "sam.gathigi+grace@gmail.com", "dept": "Governor's Office"}
]

print("🔄 Synchronizing 10 Delegate Tickets in SQLite Database...")
for d in DELEGATES:
    backend.register_event_ticket(
        event_id=EVENT_ID,
        attendee_name=d["name"],
        email=d["email"],
        phone="+254722000000",
        organization=f"Banki Kuu SACCO ({d['dept']} — Ref:{d['member_id']})",
        ticket_tier="VIP Shareholder Delegate",
        amount_paid=0.0,
        mpesa_trans_id=d["member_id"]
    )
print("✓ Database Synchronization Complete!\n")

HTML_FILE = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e\Banki_Kuu_SACCO_AGM_Invitation_Email.html"

def get_html_template():
    if os.path.exists(HTML_FILE):
        with open(HTML_FILE, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return """<!DOCTYPE html><html><body><h2>Banki Kuu SACCO 58th AGM Pass</h2><p>Dear {{NAME}}</p><a href="https://cbk-stride.streamlit.app/BKS?confirm={{TICKET_ID}}">Confirm Pass</a></body></html>"""

def run_batch_dispatch():
    smtp_user = os.environ.get("SMTP_USER", "sam.gathigi@gmail.com")
    smtp_pass = os.environ.get("SMTP_PASS", "kdjk tscr kxgb pjwh")
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))

    # Override recipient if provided, else use delegate's email
    force_recipient = os.environ.get("FORCE_RECIPIENT", "")

    print("==================================================")
    print("🚀 BATCH EMAIL DISPATCH ENGINE — 10 SACCO DELEGATES")
    print("==================================================")
    print(f"SMTP Server: {smtp_host}:{smtp_port}")
    print(f"Authenticated Sender: {smtp_user}")
    print("--------------------------------------------------")

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        print("✓ Connected & Authenticated with SMTP Server!\n")

        for i, d in enumerate(DELEGATES, 1):
            recipient = force_recipient if force_recipient else d["email"]
            subject = f"[CONFIDENTIAL] 58th AGM Invitation — {d['name']} ({d['member_id']})"
            
            # Populate HTML template
            name_url = d["name"].replace(" ", "+")
            raw_tmpl = get_html_template()
            html_body = raw_tmpl.replace("{{NAME}}", d["name"]) \
                                .replace("{{DEPT}}", d["dept"]) \
                                .replace("{{MEMBER_ID}}", d["member_id"]) \
                                .replace("{{TICKET_ID}}", d["ticket_id"]) \
                                .replace("{{NAME_URL}}", name_url)

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"Banki Kuu SACCO Secretariat <{smtp_user}>"
            msg["To"] = recipient

            msg.attach(MIMEText(html_body, "html"))
            server.sendmail(smtp_user, recipient, msg.as_string())
            
            print(f"[{i}/10] Dispatched to: {d['name']} ({recipient}) — Ticket: {d['ticket_id']}")
            time.sleep(1) # 1-sec throttling between emails

        server.quit()
        print("\n🎉 BATCH DISPATCH COMPLETED SUCCESSFULLY!")
        print("Check your inbox — 10 personalized delegate invitations have arrived!")

    except Exception as e:
        print(f"\n❌ Batch Dispatch Error: {e}")

if __name__ == "__main__":
    run_batch_dispatch()

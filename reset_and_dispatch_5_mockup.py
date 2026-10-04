"""
End-to-End Reset & 5-Delegate Mockup Invitation Dispatcher
Resets the database state for Banki Kuu SACCO 58th AGM and dispatches 5 personalized invitation emails.
"""

import os
import sys
import sqlite3
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import utils

DB_PATH = os.path.join(os.path.dirname(__file__), "cbk_dswaap.db")
EVENT_ID = "EVT-BANKI-KUU-SACCO"

DELEGATES = [
    {
        "name": "Samuel Gathigi",
        "member_id": "SACCO-342801",
        "ticket_id": "TKT-BK-342801",
        "email": "sam.gathigi@gmail.com",
        "dept": "IT & Digital Services",
        "phone": "0722849000",
        "tier": "VIP Shareholder Delegate"
    },
    {
        "name": "Dr. Beatrice Kiptoo",
        "member_id": "SACCO-342802",
        "ticket_id": "TKT-BK-342802",
        "email": "sam.gathigi+beatrice@gmail.com",
        "dept": "Internal Audit",
        "phone": "0733456789",
        "tier": "VIP Shareholder Delegate"
    },
    {
        "name": "Capt. Geoffrey Kemboi",
        "member_id": "SACCO-342803",
        "ticket_id": "TKT-BK-342803",
        "email": "sam.gathigi+geoffrey@gmail.com",
        "dept": "Banking Operations",
        "phone": "0722112233",
        "tier": "VIP Shareholder Delegate"
    },
    {
        "name": "Joyce Cheruiyot",
        "member_id": "SACCO-342804",
        "ticket_id": "TKT-BK-342804",
        "email": "sam.gathigi+joyce@gmail.com",
        "dept": "Finance & Accounts",
        "phone": "0725556677",
        "tier": "VIP Shareholder Delegate"
    },
    {
        "name": "Stanley Gicho",
        "member_id": "SACCO-342805",
        "ticket_id": "TKT-BK-342805",
        "email": "sam.gathigi+stanley@gmail.com",
        "dept": "Human Resources",
        "phone": "0720987654",
        "tier": "VIP Shareholder Delegate"
    }
]

def reset_database():
    print("==================================================")
    print("🧹 STEP 1: RESETTING ENTIRE SACCO AGM SETUP")
    print("==================================================")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 1. Clear existing SACCO tickets, ballots, and feedback
    cur.execute("DELETE FROM event_tickets_registry WHERE event_id = ?", (EVENT_ID,))
    cur.execute("DELETE FROM event_ballots_registry WHERE event_id = ?", (EVENT_ID,))
    cur.execute("DELETE FROM event_feedback_registry WHERE event_id = ?", (EVENT_ID,))
    print(f"✓ Cleared previous ticket, ballot, and feedback records for {EVENT_ID}")
    
    # 2. Re-seed clean 5 mockup delegates
    now_str = utils.get_eat_now().strftime("%Y-%m-%d %H:%M:%S")
    for d in DELEGATES:
        org_str = f"Banki Kuu SACCO ({d['dept']} — Ref:{d['member_id']})"
        cur.execute("""
            INSERT INTO event_tickets_registry (
                ticket_id, event_id, attendee_name, email, phone, organization,
                ticket_tier, amount_paid, mpesa_trans_id, gate_status, checkin_time, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 5000.0, ?, 'REGISTERED', '', ?)
        """, (
            d["ticket_id"], EVENT_ID, d["name"], d["email"], d["phone"], org_str,
            d["tier"], d["member_id"], now_str
        ))
        print(f"  + Seeded Delegate: {d['name']} ({d['ticket_id']} — {d['dept']})")

    conn.commit()
    conn.close()
    print("✓ Pristine 5-Delegate Roster Initialized!\n")

def get_html_template():
    html_file = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e\Banki_Kuu_SACCO_AGM_Invitation_Email.html"
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise FileNotFoundError(f"HTML Template not found at {html_file}")

def dispatch_emails():
    print("==================================================")
    print("🚀 STEP 2: DISPATCHING 5 PERSONALIZED AGM PASS EMAILS")
    print("==================================================")
    
    smtp_user = os.environ.get("SMTP_USER", "sam.gathigi@gmail.com")
    smtp_pass = os.environ.get("SMTP_PASS", "kdjk tscr kxgb pjwh")
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))

    print(f"SMTP Server: {smtp_host}:{smtp_port}")
    print(f"Authenticated Sender: {smtp_user}")
    print("--------------------------------------------------")

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        print("✓ Connected & Authenticated with Gmail SMTP Server!\n")

        raw_tmpl = get_html_template()

        for i, d in enumerate(DELEGATES, 1):
            recipient = d["email"]
            subject = f"[OFFICIAL NOTICE] 58th AGM Pass & Voter Credentials — {d['name']} ({d['member_id']})"
            name_url = d["name"].replace(" ", "+")
            
            html_body = raw_tmpl.replace("{{NAME}}", d["name"]) \
                                .replace("{{DEPT}}", d["dept"]) \
                                .replace("{{MEMBER_ID}}", d["member_id"]) \
                                .replace("{{TICKET_ID}}", d["ticket_id"]) \
                                .replace("{{NAME_URL}}", name_url)

            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"Banki Kuu SACCO Secretariat <{smtp_user}>"
            msg["To"] = recipient
            msg.attach(MIMEText(html_body, "html", "utf-8"))

            server.sendmail(smtp_user, [recipient], msg.as_string())
            print(f"  [{i}/5] ✉️  Dispatched email to {d['name']} -> {recipient} ({d['ticket_id']})")
            time.sleep(1)

        server.quit()
        print("\n==================================================")
        print("🎉 END-TO-END MOCKUP DISPATCH COMPLETE!")
        print("==================================================")
    except Exception as e:
        print(f"❌ SMTP Dispatch Error: {e}")

if __name__ == "__main__":
    reset_database()
    dispatch_emails()

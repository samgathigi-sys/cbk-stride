"""
Gmail Inbox Delivery Direct Diagnostic Script (Smart Accreditation-Aware)
Queries SQLite for real-time ticket gate status (ADMITTED vs REGISTERED) and dispatches dynamic status notification to sam.gathigi@gmail.com.
"""

import smtplib
import sqlite3
import os
import sys
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), "cbk_dswaap.db")
HTML_FILE = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e\Banki_Kuu_SACCO_AGM_Invitation_Email.html"

def send_smart_inbox_email():
    smtp_user = os.environ.get("SMTP_USER", "sam.gathigi@gmail.com")
    smtp_pass = os.environ.get("SMTP_PASS", "kdjk tscr kxgb pjwh")
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))

    recipient = "sam.gathigi@gmail.com"
    ticket_id = "TKT-BK-342801"
    name = "Samuel Gathigi"
    member_id = "SACCO-342801"
    dept = "IT & Digital Services"

    # Query SQLite for real-time gate status
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT gate_status, checkin_time FROM event_tickets_registry WHERE ticket_id = ?", (ticket_id,))
    row = cur.fetchone()
    conn.close()

    gate_status = row[0] if row else "REGISTERED"
    checkin_time = row[1] if row and len(row) > 1 else ""

    if gate_status == "ADMITTED":
        subject = f"🟢 ACCREDITED CONFIRMATION: Samuel Gathigi — You Are Checked In! ({ticket_id})"
        status_badge = '<span class="badge" style="background:#10B981; color:#FFFFFF;">🟢 ACCREDITED & ADMITTED AT GATE</span>'
        notice_banner = f"""
        <div style="background: #ECFDF5; border: 1.5px solid #10B981; border-radius: 10px; padding: 14px 18px; margin-bottom: 18px; color: #065F46;">
            <div style="font-weight: 800; font-size: 15px; color: #047857;">✅ YOU ARE ALREADY REGISTERED & ACCREDITED AT GATE!</div>
            <div style="font-size: 13px; margin-top: 4px;">
                Checked in on <strong>{checkin_time} EAT</strong>. Your seat in the main auditorium is reserved and your e-voting ballot is ready below.
            </div>
        </div>
        """
        gate_label = '<span style="color: #34D399; font-weight: 800;">🟢 ADMITTED AT GATE</span>'
    else:
        subject = f"🎟️ OFFICIAL NOTICE OF ASSEMBLY — Samuel Gathigi ({ticket_id})"
        status_badge = '<span class="badge">🏦 OFFICIAL NOTICE OF ASSEMBLY</span>'
        notice_banner = ""
        gate_label = '<span style="color: #F5C542; font-weight: 800;">🟡 PENDING GATE SCAN</span>'

    with open(HTML_FILE, "r", encoding="utf-8") as f:
        raw_html = f.read()

    html_body = raw_html.replace("{{NAME}}", name) \
                        .replace("{{DEPT}}", dept) \
                        .replace("{{MEMBER_ID}}", member_id) \
                        .replace("{{TICKET_ID}}", ticket_id) \
                        .replace("{{NAME_URL}}", urllib.parse.quote(name)) \
                        .replace("{{STATUS_BADGE}}", status_badge) \
                        .replace("{{REGISTRATION_NOTICE_BANNER}}", notice_banner) \
                        .replace("{{GATE_STATUS_LABEL}}", gate_label)

    print("==================================================")
    print("📧 GMAIL SMART ACCREDITATION-AWARE EMAIL DISPATCH")
    print("==================================================")
    print(f"Target Delegate: {name} ({ticket_id})")
    print(f"Real-Time Gate Status: {gate_status} ({checkin_time})")
    print(f"Generated Subject: {subject}")
    print("--------------------------------------------------")

    try:
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        print("✓ Connected & Authenticated with Gmail SMTP!")

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Banki Kuu SACCO Secretariat <{smtp_user}>"
        msg["To"] = recipient
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        res = server.sendmail(smtp_user, [recipient], msg.as_string())
        server.quit()

        print(f"✓ Smart Status Email Sent Successfully to {recipient}!")
        print(f"  SMTP Response: {res}")
        print("==================================================")
    except Exception as e:
        print(f"❌ SMTP Failed: {e}")

if __name__ == "__main__":
    send_smart_inbox_email()

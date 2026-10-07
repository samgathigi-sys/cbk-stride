"""
Banki Kuu SACCO 58th AGM — Semi-AGM Simulation & Dispatch Engine
1. Generates 100 realistic SACCO delegates across CBK divisions.
2. Ingests all 100 delegates into live Supabase PostgreSQL (and SQLite).
3. Dispatches 10 official HTML accreditation passes via Gmail SMTP to sam.gathigi@gmail.com.
4. Pre-casts 25 sample ballots to simulate live AGM quorum and voting tallies.
"""

import sys
import os
import time
import random
import smtplib
import urllib.parse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import utils
backend = utils.AttendanceBackend()

HTML_TEMPLATE_PATH = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e\Banki_Kuu_SACCO_AGM_Invitation_Email.html"
EVENT_ID = "EVT-BANKI-KUU-SACCO"

# Ensure event & ballot config exist in Supabase
backend.ensure_banki_kuu_sacco_event()

default_ballot = {
    "res1_title": "Ordinary Resolution 1: Approval of Audited Financial Statements for FY2025 and Declaration of a 14% First & Final Dividend",
    "res1_options": ["FOR (Approve Accounts & 14% Dividend)", "AGAINST (Reject Accounts)", "ABSTAIN"],
    "res2_title": "Item 2: Election of Supervisory Board Member (Nairobi East & Central Region)",
    "res2_candidates": [
        "Sarah Wanjiru CPA(K) (Independent, Audit & Finance)",
        "Eng. David Ndung'u (Incumbent, Risk & Governance)",
        "Dr. Peter Otieno (Institutional Nominee)"
    ],
    "res3_title": "Ordinary Resolution 2: Appointment of External Statutory Auditors for FY2026",
    "res3_auditors": ["Re-appoint KPMG Kenya", "Appoint PKF Kenya", "Appoint Deloitte East Africa", "ABSTAIN"]
}
backend.save_ballot_config(EVENT_ID, default_ballot, locked=1)

# 10 Executive & Delegate VIPs (Will receive the 10 real emails)
vip_delegates = [
    {"name": "Samuel Gathigi", "member_id": "SACCO-342801", "dept": "IT & Cybersecurity Division", "ticket_id": "TKT-BK-342801", "tier": "Executive Committee Delegate", "shares": 1850, "status": "ADMITTED", "checkin": "2026-10-04 08:15:22"},
    {"name": "Dr. Beatrice Kiptoo", "member_id": "SACCO-342802", "dept": "Internal Audit & Risk Oversight", "ticket_id": "TKT-BK-342802", "tier": "Principal Voting Shareholder", "shares": 1420, "status": "ADMITTED", "checkin": "2026-10-04 08:22:10"},
    {"name": "Capt. Geoffrey Kemboi", "member_id": "SACCO-342803", "dept": "Banking Operations & Settlement", "ticket_id": "TKT-BK-342803", "tier": "Principal Voting Shareholder", "shares": 980, "status": "REGISTERED", "checkin": ""},
    {"name": "Joyce Cheruiyot", "member_id": "SACCO-342804", "dept": "Finance & Accounts Division", "ticket_id": "TKT-BK-342804", "tier": "Principal Voting Shareholder", "shares": 1150, "status": "REGISTERED", "checkin": ""},
    {"name": "Stanley Gicho", "member_id": "SACCO-342805", "dept": "Human Resources & Training", "ticket_id": "TKT-BK-342805", "tier": "Principal Voting Shareholder", "shares": 820, "status": "REGISTERED", "checkin": ""},
    {"name": "Catherine Muthoni", "member_id": "SACCO-342806", "dept": "Currency Operations (CBD Nairobi)", "ticket_id": "TKT-BK-342806", "tier": "Principal Voting Shareholder", "shares": 750, "status": "REGISTERED", "checkin": ""},
    {"name": "David Ndung'u", "member_id": "SACCO-342807", "dept": "Bank Supervision Department", "ticket_id": "TKT-BK-342807", "tier": "Board Nominee & Delegate", "shares": 2100, "status": "REGISTERED", "checkin": ""},
    {"name": "Sarah Wanjiru CPA(K)", "member_id": "SACCO-342808", "dept": "Deposit Protection Fund", "ticket_id": "TKT-BK-342808", "tier": "Supervisory Board Candidate", "shares": 1600, "status": "REGISTERED", "checkin": ""},
    {"name": "Kenneth Mutai", "member_id": "SACCO-342809", "dept": "Financial Markets & Reserves", "ticket_id": "TKT-BK-342809", "tier": "Principal Voting Shareholder", "shares": 940, "status": "REGISTERED", "checkin": ""},
    {"name": "Mary Atieno", "member_id": "SACCO-342810", "dept": "Governor's Executive Secretariat", "ticket_id": "TKT-BK-342810", "tier": "Principal Voting Shareholder", "shares": 1300, "status": "REGISTERED", "checkin": ""}
]

# Generate 90 additional general SACCO members
first_names = ["Patrick", "Grace", "James", "Francis", "Mercy", "John", "Peter", "Lucy", "Joseph", "Jane", "Charles", "Eunice", "Dennis", "Rose", "Stephen", "Caroline", "Martin", "Agnes", "Brian", "Faith"]
last_names = ["Kariuki", "Ochieng", "Mwangi", "Kamau", "Kiprono", "Omondi", "Oduor", "Njoroge", "Chebet", "Wambui", "Kibet", "Otieno", "Nyambura", "Githinji", "Rotich", "Wekesa", "Kiplagat", "Maina", "Simiyu", "Kosgei"]
departments = [
    "Bank Supervision", "Currency Operations", "Financial Markets", "Internal Audit",
    "Governor's Office & Secretariat", "IT & Cybersecurity", "Risk & Compliance",
    "Human Resources", "Payments & Settlement Systems", "Deposit Protection"
]

all_100_delegates = list(vip_delegates)
for i in range(11, 101):
    fn = random.choice(first_names)
    ln = random.choice(last_names)
    name = f"{fn} {ln}"
    mem_id = f"SACCO-3428{i:02d}"
    tkt_id = f"TKT-BK-3428{i:02d}"
    dept = random.choice(departments)
    status = "ADMITTED" if i <= 25 else "REGISTERED"
    checkin = "2026-10-04 08:35:10" if status == "ADMITTED" else ""
    shares = random.randint(300, 1500)
    
    all_100_delegates.append({
        "name": name,
        "member_id": mem_id,
        "dept": dept,
        "ticket_id": tkt_id,
        "tier": "Principal Voting Shareholder",
        "shares": shares,
        "status": status,
        "checkin": checkin
    })

print(f"✓ Generated {len(all_100_delegates)} Banki Kuu SACCO delegates.")

# Ingest all 100 delegates into Supabase & SQLite
now_str = utils.get_eat_now().strftime("%Y-%m-%d %H:%M:%S")

pg_records = []
sqlite_records = []

for d in all_100_delegates:
    email = "sam.gathigi@gmail.com" if d["ticket_id"] in [v["ticket_id"] for v in vip_delegates] else f"{d['name'].lower().replace(' ', '.')}@centralbank.go.ke"
    phone = f"0722{random.randint(100000, 999999)}"
    org = f"Banki Kuu Staff SACCO ({d['dept']} — Ref:{d['member_id']})"
    amt = 5000.0
    tx_id = f"BK{d['member_id'].replace('SACCO-', '')}"
    
    rec_tuple = (
        d["ticket_id"], EVENT_ID, d["name"], email, phone, org,
        d["tier"], amt, tx_id, d["status"], d["checkin"], now_str
    )
    pg_records.append(rec_tuple)
    sqlite_records.append(rec_tuple)

# 1. Supabase Postgres Ingest
pg_conn = backend._get_pg_conn()
if pg_conn:
    cur = pg_conn.cursor()
    cur.executemany("""
        INSERT INTO event_tickets_registry (
            ticket_id, event_id, attendee_name, email, phone, organization,
            ticket_tier, amount_paid, mpesa_trans_id, gate_status, checkin_time, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ticket_id) DO UPDATE SET
            attendee_name = EXCLUDED.attendee_name,
            gate_status = EXCLUDED.gate_status,
            checkin_time = EXCLUDED.checkin_time;
    """, pg_records)
    pg_conn.commit()
    pg_conn.close()
    print("✓ Successfully ingested 100 delegates into Supabase Postgres!")

# 2. SQLite Ingest (Mirror)
import sqlite3
conn = sqlite3.connect(backend.db_path)
c = conn.cursor()
c.executemany("""
    INSERT OR REPLACE INTO event_tickets_registry (
        ticket_id, event_id, attendee_name, email, phone, organization,
        ticket_tier, amount_paid, mpesa_trans_id, gate_status, checkin_time, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", sqlite_records)
conn.commit()
conn.close()
print("✓ Successfully mirrored 100 delegates into SQLite!")

# Pre-cast 25 sample ballots to simulate live AGM voting results
res1_choices = [
    "FOR (Approve Accounts & 14% Dividend)",
    "FOR (Approve Accounts & 14% Dividend)",
    "FOR (Approve Accounts & 14% Dividend)",
    "AGAINST (Reject Accounts)",
    "ABSTAIN"
]
res2_choices = [
    "Sarah Wanjiru CPA(K) (Independent, Audit & Finance)",
    "Eng. David Ndung'u (Incumbent, Risk & Governance)",
    "Dr. Peter Otieno (Institutional Nominee)"
]
res3_choices = ["Re-appoint KPMG Kenya", "Re-appoint KPMG Kenya", "Appoint Deloitte East Africa", "ABSTAIN"]

ballots_cast_count = 0
for idx in range(25):
    d = all_100_delegates[idx]
    r1 = random.choice(res1_choices)
    r2 = random.choice(res2_choices)
    r3 = random.choice(res3_choices)
    weight = d["shares"]
    
    ok, msg, _ = backend.cast_event_ballot(
        EVENT_ID, d["ticket_id"], d["name"],
        f"Banki Kuu SACCO — {d['dept']}", weight,
        r1, r2, r3
    )
    if ok:
        ballots_cast_count += 1

print(f"✓ Cast {ballots_cast_count} live cryptographic ballots into Supabase!")

# Pre-submit 8 sample attendee feedback entries
sample_feedbacks = [
    (all_100_delegates[0], 5, "Seamless check-in and instantaneous QR accreditation! The electronic voting is totally transparent and fast. Hongera!"),
    (all_100_delegates[1], 5, "Very impressive governance platform. Real-time dividend pass confirmation and clear ballot structure."),
    (all_100_delegates[2], 4, "Smooth entry at the gate. Acoustics in the auditorium are clear. Glad we have 14% dividend."),
    (all_100_delegates[3], 5, "Mazingira safi sana na mchakato wa uchaguzi uko wazi. Vizuri sana Banki Kuu SACCO!"),
    (all_100_delegates[4], 4, "Voting on phone was super easy. Refreshments and breakfast served promptly."),
    (all_100_delegates[5], 3, "Registration was fast but queues at the tea station were slightly crowded in the morning."),
    (all_100_delegates[6], 5, "Top notch technological execution. The cryptographic ballot hashes ensure complete integrity."),
    (all_100_delegates[7], 5, "Kura imepita bila shida yoyote. Transparency on the board elections is commendable.")
]

for d, stars, txt in sample_feedbacks:
    backend.submit_event_feedback(EVENT_ID, d["ticket_id"], d["name"], stars, txt)

print(f"✓ Submitted {len(sample_feedbacks)} bilingual NLP feedback records into Supabase!")

# ==============================================================================
# DISPATCH 10 REAL ACCREDITATION EMAILS VIA GMAIL SMTP
# ==============================================================================
print("\n==================================================")
print("📧 DISPATCHING 10 ACCREDITATION PASSES VIA GMAIL SMTP")
print("==================================================")

smtp_user = "sam.gathigi@gmail.com"
smtp_pass = "kdjk tscr kxgb pjwh"
smtp_host = "smtp.gmail.com"
smtp_port = 587

try:
    server = smtplib.SMTP(smtp_host, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_pass)
    print("✓ Successfully authenticated with Gmail SMTP server!")
    
    with open(HTML_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        raw_html_template = f.read()

    emails_sent = 0
    for idx, d in enumerate(vip_delegates, 1):
        if d["status"] == "ADMITTED":
            subject = f"🟢 ACCREDITED CONFIRMATION: {d['name']} — You Are Checked In! ({d['ticket_id']})"
            status_badge = '<span class="badge" style="background:#10B981; color:#FFFFFF;">🟢 ACCREDITED & ADMITTED AT GATE</span>'
            notice_banner = f"""
            <div style="background: #ECFDF5; border: 1.5px solid #10B981; border-radius: 10px; padding: 14px 18px; margin-bottom: 18px; color: #065F46;">
                <div style="font-weight: 800; font-size: 15px; color: #047857;">✅ YOU ARE ALREADY ACCREDITED & ADMITTED AT GATE!</div>
                <div style="font-size: 13px; margin-top: 4px;">
                    Checked in on <strong>{d['checkin']} EAT</strong>. Your seat in the main auditorium is reserved and your e-voting ballot is ready below.
                </div>
            </div>
            """
            gate_label = '<span style="color: #34D399; font-weight: 800;">🟢 ADMITTED AT GATE</span>'
        else:
            subject = f"🎟️ OFFICIAL NOTICE OF ASSEMBLY: {d['name']} — 58th AGM Digital Pass ({d['ticket_id']})"
            status_badge = '<span class="badge">🏦 OFFICIAL NOTICE OF ASSEMBLY</span>'
            notice_banner = ""
            gate_label = '<span style="color: #F5C542; font-weight: 800;">🟡 PENDING GATE SCAN</span>'

        html_body = raw_html_template.replace("{{NAME}}", d["name"]) \
                                    .replace("{{DEPT}}", d["dept"]) \
                                    .replace("{{MEMBER_ID}}", d["member_id"]) \
                                    .replace("{{TICKET_ID}}", d["ticket_id"]) \
                                    .replace("{{NAME_URL}}", urllib.parse.quote(d["name"])) \
                                    .replace("{{STATUS_BADGE}}", status_badge) \
                                    .replace("{{REGISTRATION_NOTICE_BANNER}}", notice_banner) \
                                    .replace("{{GATE_STATUS_LABEL}}", gate_label)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"Banki Kuu SACCO Secretariat <{smtp_user}>"
        msg["To"] = smtp_user
        msg.attach(MIMEText(html_body, "html", "utf-8"))

        server.sendmail(smtp_user, [smtp_user], msg.as_string())
        emails_sent += 1
        print(f"  [{idx}/10] Sent: {d['name']} ({d['ticket_id']} — {d['tier']})")
        time.sleep(0.5)

    server.quit()
    print(f"\n🎉 ALL {emails_sent} OFFICIAL ACCREDITATION EMAILS DELIVERED TO {smtp_user}!")
except Exception as e:
    print(f"❌ SMTP Dispatch Error: {e}")

print("==================================================")
print("🏁 SEMI-AGM SIMULATION SETUP COMPLETE!")
print("==================================================")

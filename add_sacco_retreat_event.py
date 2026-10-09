"""
Add Tier-1 SACCO Annual Delegates Leadership & Strategy Retreat 2026 to events_registry and event_tickets_registry.
"""
import sqlite3
import datetime

conn = sqlite3.connect('cbk_dswaap.db')
cur = conn.cursor()

now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

event_id = "EVT-SACCO-RETREAT-2026"
title = "👔 Tier-1 SACCO Annual Delegates & Leadership Strategy Retreat 2026"
organizer = "Apex National SACCO Society Ltd (SASRA Regulated)"
category = "👔 Annual General Meetings (AGM) & Shareholder Assemblies"
event_date = "2026-11-12 to 2026-11-15"
event_time = "08:00 AM EAT"
venue = "PrideInn Paradise Beach Resort & Convention Centre, Mombasa"
description = (
    "Annual Statutory Delegates & Leadership Strategy Retreat for 1,200 Accredited SACCO Delegates, "
    "Supervisory Board, and Executive Leadership. Features multi-gate QR accreditation, catering quota lock, "
    "sitting allowance attendance audit ledger, and statutory digital secret balloting."
)
gate_mode = "QR_CAMERA_SCAN"
is_paid = 1
standard_price = 3500.0
vip_price = 8500.0
mpesa_paybill = "522123"
status = "ACTIVE"

# Insert or replace event
cur.execute("""
    INSERT OR REPLACE INTO events_registry (
        event_id, title, organizer_name, category, event_date, event_time,
        venue, description, gate_mode, is_paid, standard_price, vip_price,
        mpesa_paybill, created_at, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    event_id, title, organizer, category, event_date, event_time,
    venue, description, gate_mode, is_paid, standard_price, vip_price,
    mpesa_paybill, now_str, status
))

# Seed accredited delegates for this SACCO retreat
sample_sacco_tickets = [
    ("TKT-SACCO-3428", event_id, "Samuel Gathigi Njuguna", "sam.gathigi@gmail.com", "0722849000", "Central Bank of Kenya (Executive Supervisory Delegate)", "🗳️ Principal Shareholder / 10,000 Votes", 8500.0, "SACCO342890", "ADMITTED", f"{now_str}", now_str),
    ("TKT-SACCO-1011", event_id, "Catherine Ochieng", "catherine.o@harambeesacco.com", "0725556677", "Harambee Sacco Block (Nairobi Central Branch)", "📜 Duly Appointed Proxy Holder", 3500.0, "SACCO101122", "ADMITTED", f"{now_str}", now_str),
    ("TKT-SACCO-2022", event_id, "Eng. David Ndung'u", "david.ndungu@stimasacco.com", "0721889900", "Stima Sacco Supervisory Committee", "🗳️ Principal Shareholder / Voting Member", 8500.0, "SACCO202233", "ADMITTED", f"{now_str}", now_str),
    ("TKT-SACCO-3033", event_id, "Sarah Wanjiru CPA(K)", "swanjiru@mwalimusacco.co.ke", "0733123456", "Mwalimu National Sacco Audit Committee", "🗳️ Principal Shareholder / Voting Member", 8500.0, "SACCO303344", "ADMITTED", f"{now_str}", now_str),
    ("TKT-SACCO-4044", event_id, "Dr. Beatrice Kiptoo", "beatrice.k@afyasacco.com", "0720456789", "Afya Sacco Executive Board", "👔 Executive Board Director / Committee Member", 8500.0, "SACCO404455", "ADMITTED", f"{now_str}", now_str),
    ("TKT-SACCO-5055", event_id, "Wallace Mbugua", "wallace@policesacco.com", "0722123456", "Kenya Police Sacco National Delegates", "🗳️ Principal Shareholder / Voting Member", 3500.0, "SACCO505566", "ADMITTED", f"{now_str}", now_str)
]

for t in sample_sacco_tickets:
    cur.execute("""
        INSERT OR REPLACE INTO event_tickets_registry (
            ticket_id, event_id, attendee_name, email, phone, organization,
            ticket_tier, amount_paid, mpesa_trans_id, gate_status, checkin_time, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, t)

conn.commit()
conn.close()
print(f"Successfully added {event_id} and {len(sample_sacco_tickets)} accredited delegates.")

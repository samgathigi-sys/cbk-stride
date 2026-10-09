"""
clean_banki_kuu_sacco_delegates.py
Surgically cleans EVT-BANKI-KUU-SACCO tickets and ballots.
Preserves the entire sports team (staff_registry and attendance_logs) untouched.
Inserts ONLY the 11 legitimate SACCO leadership delegates.
Synchronizes both local SQLite and Supabase PostgreSQL.
"""

import sys
import sqlite3
import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import utils
backend = utils.AttendanceBackend()

EVENT_ID = "EVT-BANKI-KUU-SACCO"
now_str = utils.get_eat_now().strftime("%Y-%m-%d %H:%M:%S")

# 11 Legitimate Delegates
CLEAN_DELEGATES = [
    {
        "ticket_id": "TKT-BK-342801",
        "name": "Samuel Gathigi",
        "email": "sam.gathigi@gmail.com",
        "phone": "0722849000",
        "organization": "Banki Kuu SACCO (IT & Digital Services — Ref:SACCO-342801)",
        "tier": "🗳️ Executive Committee Delegate (10,000 Votes)",
        "amount": 5000.0,
        "ref": "BK-342801",
        "status": "ADMITTED",
        "checkin": f"{now_str}"
    },
    {
        "ticket_id": "TKT-BK-3366",
        "name": "Andrew Ogola",
        "email": "aogola@centralbank.go.ke",
        "phone": "0726103890",
        "organization": "Banki Kuu SACCO (IT & Digital Services — Ref:SACCO-3366 / Chess Captain)",
        "tier": "🗳️ Principal Voting Shareholder",
        "amount": 5000.0,
        "ref": "BK-3366",
        "status": "ADMITTED",
        "checkin": f"{now_str}"
    },
    {
        "ticket_id": "TKT-BK-342802",
        "name": "Dr. Beatrice Kiptoo",
        "email": "sam.gathigi+beatrice@gmail.com",
        "phone": "0733456789",
        "organization": "Banki Kuu SACCO (Internal Audit — Ref:SACCO-342802)",
        "tier": "🗳️ Principal Voting Shareholder",
        "amount": 5000.0,
        "ref": "BK-342802",
        "status": "ADMITTED",
        "checkin": f"{now_str}"
    },
    {
        "ticket_id": "TKT-BK-342803",
        "name": "Capt. Geoffrey Kemboi",
        "email": "sam.gathigi+geoffrey@gmail.com",
        "phone": "0722112233",
        "organization": "Banki Kuu SACCO (Banking Operations — Ref:SACCO-342803)",
        "tier": "🗳️ Principal Voting Shareholder",
        "amount": 5000.0,
        "ref": "BK-342803",
        "status": "REGISTERED",
        "checkin": ""
    },
    {
        "ticket_id": "TKT-BK-342804",
        "name": "Joyce Cheruiyot",
        "email": "sam.gathigi+joyce@gmail.com",
        "phone": "0725556677",
        "organization": "Banki Kuu SACCO (Finance & Accounts — Ref:SACCO-342804)",
        "tier": "🗳️ Principal Voting Shareholder",
        "amount": 5000.0,
        "ref": "BK-342804",
        "status": "REGISTERED",
        "checkin": ""
    },
    {
        "ticket_id": "TKT-BK-342805",
        "name": "Stanley Gicho",
        "email": "sam.gathigi+stanley@gmail.com",
        "phone": "0720987654",
        "organization": "Banki Kuu SACCO (Human Resources — Ref:SACCO-342805)",
        "tier": "🗳️ Principal Voting Shareholder",
        "amount": 5000.0,
        "ref": "BK-342805",
        "status": "REGISTERED",
        "checkin": ""
    },
    {
        "ticket_id": "TKT-BK-342806",
        "name": "Mary Wambui",
        "email": "sam.gathigi+mary@gmail.com",
        "phone": "0721334455",
        "organization": "Banki Kuu SACCO (Legal & Secretariat — Ref:SACCO-342806)",
        "tier": "🗳️ Principal Voting Shareholder",
        "amount": 5000.0,
        "ref": "BK-342806",
        "status": "REGISTERED",
        "checkin": ""
    },
    {
        "ticket_id": "TKT-BK-342807",
        "name": "David Kiiru",
        "email": "sam.gathigi+david@gmail.com",
        "phone": "0722445566",
        "organization": "Banki Kuu SACCO (Monetary Policy — Ref:SACCO-342807)",
        "tier": "🗳️ Principal Voting Shareholder",
        "amount": 5000.0,
        "ref": "BK-342807",
        "status": "REGISTERED",
        "checkin": ""
    },
    {
        "ticket_id": "TKT-BK-342808",
        "name": "Linda Otieno",
        "email": "sam.gathigi+linda@gmail.com",
        "phone": "0733556677",
        "organization": "Banki Kuu SACCO (Financial Markets — Ref:SACCO-342808)",
        "tier": "🗳️ Principal Voting Shareholder",
        "amount": 5000.0,
        "ref": "BK-342808",
        "status": "REGISTERED",
        "checkin": ""
    },
    {
        "ticket_id": "TKT-BK-342809",
        "name": "Eric Mwangi",
        "email": "sam.gathigi+eric@gmail.com",
        "phone": "0720667788",
        "organization": "Banki Kuu SACCO (Currency Logistics — Ref:SACCO-342809)",
        "tier": "🗳️ Principal Voting Shareholder",
        "amount": 5000.0,
        "ref": "BK-342809",
        "status": "REGISTERED",
        "checkin": ""
    },
    {
        "ticket_id": "TKT-BK-342810",
        "name": "Grace Mutisya",
        "email": "sam.gathigi+grace@gmail.com",
        "phone": "0723778899",
        "organization": "Banki Kuu SACCO (Governor's Office — Ref:SACCO-342810)",
        "tier": "🗳️ Principal Voting Shareholder",
        "amount": 5000.0,
        "ref": "BK-342810",
        "status": "REGISTERED",
        "checkin": ""
    }
]

# 1. SQLite Cleanup & Re-seeding (SURGICALLY for EVT-BANKI-KUU-SACCO ONLY)
conn = sqlite3.connect('cbk_dswaap.db')
cur = conn.cursor()

# Verify sports team count BEFORE cleanup
cur.execute("SELECT COUNT(*) FROM staff_registry")
sports_before = cur.fetchone()[0]

# Purge mock/synthetic tickets and ballots for EVT-BANKI-KUU-SACCO ONLY
cur.execute("DELETE FROM event_tickets_registry WHERE event_id = ?", (EVENT_ID,))
cur.execute("DELETE FROM event_ballots_registry WHERE event_id = ?", (EVENT_ID,))

# Insert only the 11 clean delegates
for d in CLEAN_DELEGATES:
    cur.execute("""
        INSERT INTO event_tickets_registry (
            ticket_id, event_id, attendee_name, email, phone,
            organization, ticket_tier, amount_paid, mpesa_trans_id,
            gate_status, checkin_time, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        d["ticket_id"], EVENT_ID, d["name"], d["email"], d["phone"],
        d["organization"], d["tier"], d["amount"], d["ref"],
        d["status"], d["checkin"], now_str
    ))

conn.commit()

# Verify sports team count AFTER cleanup
cur.execute("SELECT COUNT(*) FROM staff_registry")
sports_after = cur.fetchone()[0]
conn.close()

print(f"[OK] SQLite: Purged mock records for {EVENT_ID}.")
print(f"[OK] SQLite: Seeded exactly {len(CLEAN_DELEGATES)} legitimate SACCO delegates.")
print(f"[VERIFIED] Sports team records untouched: {sports_before} -> {sports_after} staff members.")

# 2. Supabase Postgres Cleanup & Re-seeding (If active)
pg = backend._get_pg_conn()
if pg:
    try:
        pcur = pg.cursor()
        pcur.execute("DELETE FROM event_tickets_registry WHERE event_id = %s;", (EVENT_ID,))
        pcur.execute("DELETE FROM event_ballots_registry WHERE event_id = %s;", (EVENT_ID,))
        for d in CLEAN_DELEGATES:
            pcur.execute("""
                INSERT INTO event_tickets_registry (
                    ticket_id, event_id, attendee_name, email, phone,
                    organization, ticket_tier, amount_paid, mpesa_trans_id,
                    gate_status, checkin_time, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                d["ticket_id"], EVENT_ID, d["name"], d["email"], d["phone"],
                d["organization"], d["tier"], d["amount"], d["ref"],
                d["status"], d["checkin"], now_str
            ))
        pg.commit()
        pg.close()
        print(f"[OK] Supabase PostgreSQL: Synced {len(CLEAN_DELEGATES)} clean delegates.")
    except Exception as e:
        print(f"[WARN] Supabase update notice: {e}")
else:
    print("[INFO] Supabase not connected locally; SQLite updated.")

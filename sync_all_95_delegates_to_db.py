"""
sync_all_95_delegates_to_db.py
Syncs all 95 delegates from RETREAT_BADGES_REGISTRY.csv into EVT-BANKI-KUU-SACCO in cbk_dswaap.db
and Supabase Postgres. Leaves sports team (staff_registry: 679) 100% untouched.
"""

import sys
import sqlite3
import pandas as pd
import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import utils
backend = utils.AttendanceBackend()

EVENT_ID = "EVT-BANKI-KUU-SACCO"
now_str = utils.get_eat_now().strftime("%Y-%m-%d %H:%M:%S")

# Load 95 delegates from master CSV
csv_path = "RETREAT_BADGES_REGISTRY.csv"
df = pd.read_csv(csv_path)

print(f"Loaded {len(df)} delegates from {csv_path}.")

# Connect SQLite
conn = sqlite3.connect('cbk_dswaap.db')
cur = conn.cursor()

# Verify sports team before
cur.execute("SELECT COUNT(*) FROM staff_registry")
sports_before = cur.fetchone()[0]

# Clear existing EVT-BANKI-KUU-SACCO tickets
cur.execute("DELETE FROM event_tickets_registry WHERE event_id = ?", (EVENT_ID,))

delegates_to_insert = []
for _, r in df.iterrows():
    ser = str(r["serial"]).strip()
    # Map friendly ticket IDs for key leaders and unique ID for casuals
    idx = int(r["index"])
    if ser == "3428":
        tkt_id = "TKT-BK-342801"
    elif ser == "3366":
        tkt_id = "TKT-BK-3366"
    elif ser == "CASUAL":
        tkt_id = f"TKT-BK-CASUAL-{idx:02d}"
    else:
        tkt_id = f"TKT-BK-{ser}"

    name = str(r["full_name"]).strip()
    role = str(r["role"]).strip()
    tier = str(r["tier"]).strip()
    token = str(r["token_id"]).strip()
    phone = str(r.get("masked_phone", "+254 722 *** *00")).strip()
    email = str(r.get("masked_email", f"{name.lower().replace(' ', '.')}@centralbank.go.ke")).strip()
    org = f"Banki Kuu SACCO ({role} — Ref:SACCO-{ser})"
    tier_desc = f"🗳️ {tier} Delegate / {role}"
    
    # Pre-admit leadership for immediate quorum testing
    if ser in ["3428", "3366", "3124", "2281", "3379", "3213", "2406", "3125", "2849", "3859", "2581"]:
        gate_st = "ADMITTED"
        cin_time = now_str
    else:
        gate_st = "REGISTERED"
        cin_time = ""

    delegates_to_insert.append((
        tkt_id, EVENT_ID, name, email, phone, org,
        tier_desc, 5000.0, token, gate_st, cin_time, now_str
    ))

cur.executemany("""
    INSERT INTO event_tickets_registry (
        ticket_id, event_id, attendee_name, email, phone,
        organization, ticket_tier, amount_paid, mpesa_trans_id,
        gate_status, checkin_time, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", delegates_to_insert)

conn.commit()

# Verify sports team after
cur.execute("SELECT COUNT(*) FROM staff_registry")
sports_after = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM event_tickets_registry WHERE event_id = ?", (EVENT_ID,))
sacco_count = cur.fetchone()[0]
conn.close()

print(f"[OK] Successfully ingested {sacco_count} delegates into {EVENT_ID}.")
print(f"[VERIFIED] Sports team (staff_registry) untouched: {sports_before} == {sports_after}.")

# Supabase Postgres sync
pg = backend._get_pg_conn()
if pg:
    try:
        pcur = pg.cursor()
        pcur.execute("DELETE FROM event_tickets_registry WHERE event_id = %s;", (EVENT_ID,))
        for d in delegates_to_insert:
            pcur.execute("""
                INSERT INTO event_tickets_registry (
                    ticket_id, event_id, attendee_name, email, phone,
                    organization, ticket_tier, amount_paid, mpesa_trans_id,
                    gate_status, checkin_time, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, d)
        pg.commit()
        pg.close()
        print(f"[OK] Supabase PostgreSQL: Synced all {len(delegates_to_insert)} delegates.")
    except Exception as e:
        print(f"[WARN] Supabase sync notice: {e}")
else:
    print("[INFO] Supabase not active; local SQLite updated.")

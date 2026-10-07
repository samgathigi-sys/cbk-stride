"""
Provision Complete Access for Andrew Ogola (Chess Captain & SACCO Delegate)
1. Registers Andrew Ogola in event_tickets_registry (Supabase Postgres & SQLite).
2. Grants him Secretariat / Officer RBAC in security_access_control with Passkey 3366.
3. Grants him Chess Captaincy in captain_credentials with Passkey 3366.
"""

import sys
import sqlite3
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

import utils
backend = utils.AttendanceBackend()

now_str = utils.get_eat_now().strftime('%Y-%m-%d %H:%M:%S')
pass_hash = backend._hash_passkey('3366')

# 1. SQLite: security_access_control
conn = sqlite3.connect('cbk_dswaap.db')
cur = conn.cursor()
cur.execute('''
    INSERT INTO security_access_control (
        staff_id, full_name, department, role,
        can_export_roster, can_export_finances, can_manage_roles,
        passkey_hash, granted_by, created_at
    ) VALUES (?, ?, ?, ?, 1, 1, 0, ?, 'SYSTEM_ADMIN', ?)
    ON CONFLICT(staff_id) DO UPDATE SET
        full_name=excluded.full_name,
        department=excluded.department,
        role=excluded.role,
        passkey_hash=excluded.passkey_hash
''', ('CBK-3366', 'Andrew Ogola', 'IT & Digital Services', 'Chess Captain & SACCO Delegate', pass_hash, now_str))

# 2. SQLite: captain_credentials
cur.execute('DELETE FROM captain_credentials WHERE staff_id = ? AND discipline = ?', ('CBK-3366', 'Chess'))
cur.execute('''
    INSERT INTO captain_credentials (
        staff_id, full_name, gmail_or_email, discipline,
        passkey_hash, temp_pin, created_at, expires_at, is_active
    ) VALUES (?, ?, ?, ?, ?, ?, ?, '2027-12-31 23:59:59', 1)
''', ('CBK-3366', 'Andrew Ogola', 'aogola@centralbank.go.ke', 'Chess', pass_hash, '3366', now_str))

# 3. SQLite: event_tickets_registry
cur.execute('DELETE FROM event_tickets_registry WHERE ticket_id = ? OR (event_id = ? AND attendee_name = ?)', ('TKT-BK-3366', 'EVT-BANKI-KUU-SACCO', 'Andrew Ogola'))
cur.execute('''
    INSERT INTO event_tickets_registry (
        ticket_id, event_id, attendee_name, email, phone,
        organization, ticket_tier, amount_paid, mpesa_trans_id,
        gate_status, checkin_time, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, 0.0, ?, 'REGISTERED', '', ?)
''', (
    'TKT-BK-3366',
    'EVT-BANKI-KUU-SACCO',
    'Andrew Ogola',
    'aogola@centralbank.go.ke',
    '0726103890',
    'Banki Kuu Staff SACCO (IT & Digital Services — Ref:SACCO-3366 / Chess Captain)',
    'Principal Voting Shareholder',
    'BK3366',
    now_str
))
conn.commit()
conn.close()
print('[OK] SQLite updated for Andrew Ogola.')

# 4. Postgres (Supabase)
pg = backend._get_pg_conn()
if pg:
    pcur = pg.cursor()
    pcur.execute('''
        CREATE TABLE IF NOT EXISTS security_access_control (
            staff_id TEXT PRIMARY KEY,
            full_name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL,
            can_export_roster INTEGER DEFAULT 1,
            can_export_finances INTEGER DEFAULT 0,
            can_manage_roles INTEGER DEFAULT 0,
            passkey_hash TEXT NOT NULL,
            granted_by TEXT DEFAULT 'SYSTEM_INIT',
            created_at TEXT NOT NULL,
            last_login TEXT
        );
    ''')
    pcur.execute('''
        INSERT INTO security_access_control (
            staff_id, full_name, department, role,
            can_export_roster, can_export_finances, can_manage_roles,
            passkey_hash, granted_by, created_at
        ) VALUES (%s, %s, %s, %s, 1, 1, 0, %s, 'SYSTEM_ADMIN', %s)
        ON CONFLICT(staff_id) DO UPDATE SET
            full_name=EXCLUDED.full_name,
            department=EXCLUDED.department,
            role=EXCLUDED.role,
            passkey_hash=EXCLUDED.passkey_hash;
    ''', ('CBK-3366', 'Andrew Ogola', 'IT & Digital Services', 'Chess Captain & SACCO Delegate', pass_hash, now_str))

    pcur.execute('DELETE FROM event_tickets_registry WHERE ticket_id = %s OR (event_id = %s AND attendee_name = %s);', ('TKT-BK-3366', 'EVT-BANKI-KUU-SACCO', 'Andrew Ogola'))
    pcur.execute('''
        INSERT INTO event_tickets_registry (
            ticket_id, event_id, attendee_name, email, phone,
            organization, ticket_tier, amount_paid, mpesa_trans_id,
            gate_status, checkin_time, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, 0.0, %s, 'REGISTERED', '', %s);
    ''', (
        'TKT-BK-3366',
        'EVT-BANKI-KUU-SACCO',
        'Andrew Ogola',
        'aogola@centralbank.go.ke',
        '0726103890',
        'Banki Kuu Staff SACCO (IT & Digital Services — Ref:SACCO-3366 / Chess Captain)',
        'Principal Voting Shareholder',
        'BK3366',
        now_str
    ))
    pg.commit()
    pg.close()
    print('[OK] Supabase Postgres updated for Andrew Ogola.')
else:
    print('[WARN] Supabase Postgres connection not active.')

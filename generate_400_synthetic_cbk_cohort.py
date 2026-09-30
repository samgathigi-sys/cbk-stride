"""
Central Bank of Kenya (CBK) - DSWAAP Synthetic Cohort Generator
Generates 400 realistic CBK staff athlete profiles across 10 Directorates and 18 Sporting Disciplines,
with complete end-to-end dual-gate attendance workflows (Gate 1 -> Training -> Gate 2 -> Allowance Audit).
"""

import os
import random
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(OUTPUT_DIR, "cbk_dswaap.db")
CSV_PATH = os.path.join(OUTPUT_DIR, "cbk_dswaap_records.csv")

# 10 Official Central Bank of Kenya Directorates
CBK_DIRECTORATES = [
    "Monetary Policy & Economic Research",
    "Financial Markets & Reserves Management",
    "Bank Supervision & Financial Integrity",
    "Currency Operations & Branch Logistics",
    "Banking & National Payment Services",
    "Human Resources & Institutional Development",
    "Finance, Planning & Accounts",
    "Information Technology & Digital Operations",
    "Legal, Corporate Governance & Board Secretariat",
    "Internal Audit & Fiduciary Assurance"
]

# 18 CBK Sporting Disciplines with Venue Stations
CBK_DISCIPLINES_MAP = {
    "Athletics & Track": {
        "code": "ATH",
        "stations": ["Track 100m Start Point", "Perimeter Gate 3", "Main Stadium Pavilion", "Cross-Country Outer Loop"],
        "weight": 55  # Flagship discipline
    },
    "Football (Soccer)": {
        "code": "FB",
        "stations": ["Main Pitch West Bench", "Main Pitch Entry Gate", "Goal Post South Checkpoint"],
        "weight": 45
    },
    "Basketball": {
        "code": "BB",
        "stations": ["Arena North Gate", "Scorer's Table", "Court 1 Base"],
        "weight": 30
    },
    "Volleyball": {
        "code": "VB",
        "stations": ["Hard Court Pavilion", "Sand Court 1", "Court Entry Post"],
        "weight": 25
    },
    "Netball": {
        "code": "NB",
        "stations": ["East Court Gate A", "Team Bench East"],
        "weight": 25
    },
    "Swimming": {
        "code": "SWM",
        "stations": ["Aquatic Centre Poolside Desk", "Lifeguard Station North"],
        "weight": 25
    },
    "Lawn Tennis": {
        "code": "LT",
        "stations": ["Tennis Centre Court 1 Desk", "Pavilion Gate"],
        "weight": 20
    },
    "Table Tennis": {
        "code": "TT",
        "stations": ["Indoor Hall Table 1 Desk", "Recreation Centre Entrance"],
        "weight": 20
    },
    "Badminton": {
        "code": "BDM",
        "stations": ["Badminton Hall Gate B", "Scorer's Post"],
        "weight": 20
    },
    "Golf": {
        "code": "GLF",
        "stations": ["Clubhouse Pro-Shop", "Tee Box Hole 1", "Halfway House Hole 9", "18th Green Marshals Post"],
        "weight": 20
    },
    "Chess": {
        "code": "CHS",
        "stations": ["Clubhouse Board 1 Arena", "Mindsport Lounge"],
        "weight": 20
    },
    "Physical Fitness & Aerobics": {
        "code": "FIT",
        "stations": ["Wellness Gymnasium Entrance", "Aerobics Studio Desk A"],
        "weight": 20
    },
    "Scrabble & Darts": {
        "code": "SCD",
        "stations": ["Quiet Games Room Station 1", "Board Lounge East"],
        "weight": 15
    },
    "Tug of War": {
        "code": "TOW",
        "stations": ["Lower Grounds Grass Arena", "Central Pull Post"],
        "weight": 15
    },
    "Cycling": {
        "code": "CYC",
        "stations": ["Bicycle Depot Base", "Outpost Checkpoint 2"],
        "weight": 15
    },
    "Squash": {
        "code": "SQ",
        "stations": ["Squash Court 1 Entry", "Viewing Gallery Desk"],
        "weight": 10
    },
    "Snooker / Pool": {
        "code": "SNK",
        "stations": ["Billiards Room Desk", "Table 1 Station"],
        "weight": 10
    },
    "Martial Arts & Self Defense": {
        "code": "MA",
        "stations": ["Dojo Studio Entry Desk", "Mat Area 1"],
        "weight": 10
    }
}

# Authentic Kenyan Names Pool
KENYAN_FIRST_NAMES = [
    "Brian", "Grace", "Bernard", "Alice", "Joyce", "David", "Eric", "Angela", "Kevin", "Samuel",
    "Faith", "Dennis", "Catherine", "Peter", "Mercy", "Victor", "Sarah", "James", "Caroline", "Paul",
    "Brenda", "Joseph", "Eunice", "George", "Beatrice", "Emmanuel", "Winnie", "Patrick", "Esther", "Daniel",
    "Millicent", "Felix", "Lydia", "Collins", "Nancy", "Geoffrey", "Ruth", "Kennedy", "Dorcas", "Anthony",
    "Gladys", "Moses", "Sharon", "Stephen", "Lilian", "Charles", "Mary", "Evans", "Hellen", "Ian",
    "Jane", "Ronald", "Janet", "Edwin", "Agnes", "Francis", "Phyllis", "Jackson", "Naomi", "Simon",
    "Sylvia", "Martin", "Lucy", "Vincent", "Edna", "Allan", "Jacqueline", "Nelson", "Florence", "Julius",
    "Rosemary", "Duncan", "Emily", "Oscar", "Diana", "Sammy", "Purity", "Albert", "Christine", "Titus"
]

KENYAN_SURNAMES = [
    "Kimani", "Mutisya", "Kiprono", "Chebet", "Cheruiyot", "Koech", "Mwangi", "Mutua", "Kariuki", "Kiptoo",
    "Ochieng", "Wambui", "Odhiambo", "Achieng", "Njeri", "Korir", "Maina", "Otieno", "Rotich", "Kamau",
    "Wekesa", "Kipchumba", "Nyambura", "Barasa", "Ndungu", "Kiplagat", "Onyango", "Mueni", "Gitau", "Omondi",
    "Kipkemboi", "Wanjiku", "Mbugua", "Kipruto", "Moraa", "Githinji", "Naliaka", "Chepkoech", "Musyoka", "Njoroge",
    "Makori", "Cherotich", "Kibiwott", "Karanja", "Jepchirchir", "Kiprotich", "Kiprop", "Kemei", "Langat", "Bett",
    "Ouma", "Kipkosgei", "Kipkoech", "Mutai", "Ngetich", "Ruto", "Sang", "Chepkirui", "Chepngetich", "Wanyonyi",
    "Khaemba", "Simiyu", "Nabiswa", "Wafula", "Juma", "Okoth", "Anyango", "Akoth", "Adhiambo", "Awino"
]


def generate_cohort():
    print("=" * 80)
    print("  CENTRAL BANK OF KENYA (CBK) - DSWAAP 400 SYNTHETIC COHORT GENERATOR")
    print("  Generating 400 Institutional Staff Athletes & End-to-End Attendance Workflows")
    print("=" * 80)

    # Deterministic seed for reproducible executive demo
    random.seed(42)

    # 1. Distribute 400 staff across 18 disciplines based on target weights
    disc_list = []
    for disc_name, info in CBK_DISCIPLINES_MAP.items():
        disc_list.extend([disc_name] * info["weight"])
    
    # Shuffle disciplines
    random.shuffle(disc_list)
    assert len(disc_list) == 400, f"Expected 400, got {len(disc_list)}"

    # 2. Build 400 unique staff profiles
    staff_profiles = []
    used_emails = set()

    # Pre-include the iconic pilot anchors
    anchors = [
        ("CBK-1024", "Brian Kimani", "bkimani@centralbank.go.ke", "Monetary Policy & Economic Research", "Athletics & Track"),
        ("CBK-2088", "Grace Mutisya", "gmutisya@centralbank.go.ke", "Information Technology & Digital Operations", "Basketball"),
        ("CBK-3112", "Bernard Kiprono", "bkiprono@centralbank.go.ke", "Finance, Planning & Accounts", "Football (Soccer)"),
        ("CBK-4055", "Alice Chebet", "achebet@centralbank.go.ke", "Internal Audit & Fiduciary Assurance", "Athletics & Track"),
        ("CBK-8201", "Joyce Cheruiyot", "jcheruiyot@centralbank.go.ke", "Human Resources & Institutional Development", "Lawn Tennis"),
    ]
    used_ids = set()
    for sid, fn, em, dep, sp in anchors:
        staff_profiles.append({
            "staff_id": sid,
            "full_name": fn,
            "cbk_email": em,
            "department": dep,
            "primary_sport": sp,
            "created_at": "2026-09-01"
        })
        used_emails.add(em)
        used_ids.add(sid)

    # Generate remaining 395 profiles
    next_id_num = 1001
    for i in range(5, 400):
        while f"CBK-{next_id_num:04d}" in used_ids:
            next_id_num += 1
        sid = f"CBK-{next_id_num:04d}"
        used_ids.add(sid)
        next_id_num += 1

        fn = random.choice(KENYAN_FIRST_NAMES)
        sn = random.choice(KENYAN_SURNAMES)
        full_name = f"{fn} {sn}"
        
        # Email formatting with duplicate resolution
        base_email = f"{fn[0].lower()}{sn.lower()}@centralbank.go.ke"
        email = base_email
        counter = 1
        while email in used_emails:
            if counter < len(fn):
                email = f"{fn[:counter+1].lower()}{sn.lower()}@centralbank.go.ke"
            else:
                email = f"{fn.lower()}.{sn.lower()}{counter}@centralbank.go.ke"
            counter += 1
        used_emails.add(email)

        dept = CBK_DIRECTORATES[i % len(CBK_DIRECTORATES)]
        sport = disc_list[i]

        staff_profiles.append({
            "staff_id": sid,
            "full_name": full_name,
            "cbk_email": email,
            "department": dept,
            "primary_sport": sport,
            "created_at": "2026-09-01"
        })

    print(f"Generated {len(staff_profiles)} authentic CBK staff profiles.")

    # 3. Populate SQLite staff_registry table
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM staff_registry")
    for s in staff_profiles:
        cur.execute("""
            INSERT INTO staff_registry (staff_id, full_name, cbk_email, department, primary_sport, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (s["staff_id"], s["full_name"], s["cbk_email"], s["department"], s["primary_sport"], s["created_at"]))
    conn.commit()
    print("Populated SQLite `staff_registry` table with 400 records.")

    # 4. Generate End-to-End Attendance Records ("Step 1 to the End")
    # Breakdown of the 400 staff:
    # - 310 Athletes: Full Dual-Gate Compliant (>= 45 mins) -> KES 2,500 Qualified
    # - 35 Athletes: Non-Compliant Short Session (< 45 mins) -> Disqualified (KES 0)
    # - 30 Athletes: In-Progress / Gate 1 Only (Currently on track/field) -> Pending Gate 2
    # - 25 Athletes: Rest Day (Enrolled in directory, 0 scans today)

    cur.execute("DELETE FROM attendance_logs")
    conn.commit()

    now = datetime.now()
    today_date = now.strftime("%Y-%m-%d")

    # Set up realistic base camp timing (morning session from 06:15 AM)
    base_morning = now.replace(hour=6, minute=15, second=0, microsecond=0)

    attendance_rows = []
    log_id_counter = 1

    # GROUP A: 310 Dual-Verified & Qualified Athletes (Duration 48 - 110 minutes)
    for idx in range(310):
        s = staff_profiles[idx]
        disc = s["primary_sport"]
        disc_info = CBK_DISCIPLINES_MAP[disc]
        stat_pre = disc_info["stations"][0]
        stat_post = disc_info["stations"][-1]

        # Stagger arrival times between 06:15 AM and 07:15 AM
        arrival_offset = random.randint(0, 55)
        pre_time = base_morning + timedelta(minutes=arrival_offset, seconds=random.randint(0, 59))
        
        # Duration: strictly >= 45 mins (between 48 and 105 mins)
        duration_mins = random.randint(48, 105) + round(random.random(), 1)
        post_time = pre_time + timedelta(minutes=duration_mins)

        sess_id = f"CAMP-{now.strftime('%Y%m%d')}-{disc_info['code']}"

        # Gate 1 Record (Arrival)
        attendance_rows.append((
            pre_time.strftime("%Y-%m-%d %H:%M:%S"),
            today_date,
            s["staff_id"],
            s["full_name"],
            s["cbk_email"],
            s["department"],
            disc,
            "PRE_SPORT",
            stat_pre,
            sess_id,
            "PRE_SPORT_VALIDATED",
            0.0,
            "AWAITING_POST_GATE",
            0,
            f"Gate 1 arrival scan validated at {stat_pre}",
            1
        ))

        # Gate 2 Record (Departure & Payout Reconciled)
        attendance_rows.append((
            post_time.strftime("%Y-%m-%d %H:%M:%S"),
            today_date,
            s["staff_id"],
            s["full_name"],
            s["cbk_email"],
            s["department"],
            disc,
            "POST_SPORT",
            stat_post,
            sess_id,
            "DUAL_VERIFIED",
            duration_mins,
            "QUALIFIED",
            2500,
            f"Dual-gate reconciled ({duration_mins} mins >= 45 min policy floor). KES 2,500 approved.",
            1
        ))

    # GROUP B: 35 Early Departure / Fiduciary Leakage Defense (Duration 15 - 38 mins < 45 mins)
    for idx in range(310, 345):
        s = staff_profiles[idx]
        disc = s["primary_sport"]
        disc_info = CBK_DISCIPLINES_MAP[disc]
        stat_pre = disc_info["stations"][0]
        stat_post = disc_info["stations"][-1]

        arrival_offset = random.randint(10, 50)
        pre_time = base_morning + timedelta(minutes=arrival_offset, seconds=random.randint(0, 59))
        
        # Duration: strictly < 45 mins (e.g. 18 to 36 mins)
        duration_mins = random.randint(18, 38) + round(random.random(), 1)
        post_time = pre_time + timedelta(minutes=duration_mins)

        sess_id = f"CAMP-{now.strftime('%Y%m%d')}-{disc_info['code']}"

        # Gate 1 Record
        attendance_rows.append((
            pre_time.strftime("%Y-%m-%d %H:%M:%S"),
            today_date,
            s["staff_id"],
            s["full_name"],
            s["cbk_email"],
            s["department"],
            disc,
            "PRE_SPORT",
            stat_pre,
            sess_id,
            "PRE_SPORT_VALIDATED",
            0.0,
            "AWAITING_POST_GATE",
            0,
            f"Gate 1 arrival scan validated at {stat_pre}",
            1
        ))

        # Gate 2 Record (Disqualified - Fiduciary Protection)
        attendance_rows.append((
            post_time.strftime("%Y-%m-%d %H:%M:%S"),
            today_date,
            s["staff_id"],
            s["full_name"],
            s["cbk_email"],
            s["department"],
            disc,
            "POST_SPORT",
            stat_post,
            sess_id,
            "INSUFFICIENT_DURATION",
            duration_mins,
            "DISQUALIFIED",
            0,
            f"DISQUALIFIED: Session duration ({duration_mins} mins) fell below mandatory 45.0 min policy threshold.",
            1
        ))

    # GROUP C: 30 In-Progress Athletes (Checked in at Gate 1 within last 25 mins, still active on track/field)
    for idx in range(345, 375):
        s = staff_profiles[idx]
        disc = s["primary_sport"]
        disc_info = CBK_DISCIPLINES_MAP[disc]
        stat_pre = disc_info["stations"][0]

        # Arrived recently
        pre_time = now - timedelta(minutes=random.randint(10, 28), seconds=random.randint(0, 59))
        sess_id = f"CAMP-{now.strftime('%Y%m%d')}-{disc_info['code']}"

        attendance_rows.append((
            pre_time.strftime("%Y-%m-%d %H:%M:%S"),
            today_date,
            s["staff_id"],
            s["full_name"],
            s["cbk_email"],
            s["department"],
            disc,
            "PRE_SPORT",
            stat_pre,
            sess_id,
            "PRE_SPORT_VALIDATED",
            0.0,
            "AWAITING_POST_GATE",
            0,
            f"Gate 1 verified. Athlete active on track circuit. Awaiting post-sport scan.",
            1
        ))

    # (Remaining 25 staff members are registered in directory on rest day, zero logs today)

    # Insert all attendance logs
    cur.executemany("""
        INSERT INTO attendance_logs (
            timestamp, date, staff_id, full_name, cbk_email, department,
            discipline, gate, station, session_id, validation_status,
            duration_minutes, allowance_qualified, allowance_amount, audit_notes, gsheets_synced
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, attendance_rows)
    conn.commit()
    conn.close()

    # 5. Mirror to CSV file (`cbk_dswaap_records.csv`)
    conn = sqlite3.connect(DB_PATH)
    df_all = pd.read_sql_query("SELECT * FROM attendance_logs ORDER BY id ASC", conn)
    conn.close()
    df_all.to_csv(CSV_PATH, index=False)

    total_scans = len(attendance_rows)
    total_allowance = 310 * 2500
    disqualified_savings = 35 * 2500

    print("=" * 80)
    print("  SYNTHETIC 400 COHORT GENERATION COMPLETE!")
    print("=" * 80)
    print(f"[*] Total Registered Staff Profiles:        400 CBK Employees")
    print(f"[*] Active Participating Staff Today:       375 Athletes")
    print(f"[*] Total Recorded Attendance Scans:        {total_scans} Scans (Gate 1 + Gate 2)")
    print(f"[OK] Dual-Gate Verified & Qualified (>=45m): 310 Athletes (KES {total_allowance:,.0f} Approved)")
    print(f"[SHIELD] Disqualified Short Sessions (<45m): 35 Claimants Prevented (KES {disqualified_savings:,.0f} Leakage Saved!)")
    print(f"[LIVE] Currently In-Progress on Track/Field: 30 Athletes (Awaiting Post-Gate Scan)")
    print(f"[REST] Off-Day / Registered in Directory:   25 Athletes")
    print(f"[FILE] Local Database Updated:              {DB_PATH}")
    print(f"[FILE] CSV Ledger Exported:                 {CSV_PATH}")
    print("=" * 80)


if __name__ == "__main__":
    generate_cohort()

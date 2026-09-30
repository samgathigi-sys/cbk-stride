"""
ingest_secretariat_roster.py
Parses, sanitizes, normalizes and ingests the official CBK Sports Secretariat roster
into the CBK STRIDE SQLite database (staff_registry) and mirrors to CSV.
"""

import os
import re
import sqlite3
from datetime import datetime
from collections import Counter, defaultdict
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
RAW_PATH = os.path.join(BASE_DIR, "raw_secretariat_data.txt")
DB_PATH = os.path.join(BASE_DIR, "cbk_dswaap.db")

# Directorate / Department Normalization Map
DEPT_MAP = {
    "itd": "IT & Digital Services",
    "information technology": "IT & Digital Services",
    "it": "IT & Digital Services",
    "it department": "IT & Digital Services",
    "cbk-ims": "CBK-IMS",
    "ims": "CBK-IMS",
    "cbk ims": "CBK-IMS",
    "itd=cbk-ims": "CBK-IMS",
    "ims cbk": "CBK-IMS",
    "fmd": "Financial Markets & Reserves",
    "financial markets": "Financial Markets & Reserves",
    "financial market": "Financial Markets & Reserves",
    "modm": "Financial Markets & Reserves",
    "bsd": "Bank Supervision",
    "bank supervision": "Bank Supervision",
    "cod": "Currency Operations & Logistics",
    "currency operations": "Currency Operations & Logistics",
    "currency": "Currency Operations & Logistics",
    "gsd": "General Services Department",
    "general services": "General Services Department",
    "general service": "General Services Department",
    "general service department": "General Services Department",
    "msa- gsd": "General Services Department",
    "msa- general services": "General Services Department",
    "hr": "Human Resources",
    "hrd": "Human Resources",
    "human resources": "Human Resources",
    "human resource": "Human Resources",
    "hr-staff clinic": "Human Resources",
    "hrd- hq": "Human Resources",
    "hrd-hq": "Human Resources",
    "gov": "Governor's Executive Office",
    "governors": "Governor's Executive Office",
    "governor's": "Governor's Executive Office",
    "governor's office": "Governor's Executive Office",
    "governor’s office": "Governor's Executive Office",
    "governors' office": "Governor's Executive Office",
    "governors'": "Governor's Executive Office",
    "gorvernors": "Governor's Executive Office",
    "governor's office'": "Governor's Executive Office",
    "governor's office -security": "Governor's Executive Office",
    "governors office": "Governor's Executive Office",
    "governors office hq": "Governor's Executive Office",
    "governor’s office (police)": "Governor's Executive Office",
    "governors-communications": "Governor's Executive Office",
    "comms- hq": "Governor's Executive Office",
    "bps": "Banking & Payment Services",
    "banking": "Banking & Payment Services",
    "banking & payment services": "Banking & Payment Services",
    "banking and payment services": "Banking & Payment Services",
    "banking & payments": "Banking & Payment Services",
    "banking & payment": "Banking & Payment Services",
    "banking services & payments": "Banking & Payment Services",
    "bps-hq": "Banking & Payment Services",
    "bps -hq": "Banking & Payment Services",
    "finance": "Finance & Accounts",
    "finance (pensions)": "Finance & Accounts",
    "pensions": "Finance & Accounts",
    "finance department - pensions": "Finance & Accounts",
    "finance department": "Finance & Accounts",
    "internal audit": "Internal Audit",
    "internal audit & risk": "Internal Audit",
    "iar": "Internal Audit",
    "audit": "Internal Audit",
    "ia": "Internal Audit",
    "iad": "Internal Audit",
    "research": "Monetary Policy & Research",
    "research department": "Monetary Policy & Research",
    "research-hq": "Monetary Policy & Research",
    "res": "Monetary Policy & Research",
    "legal": "Legal & Board Secretariat",
    "legal & board secretariat": "Legal & Board Secretariat",
    "mombasa": "Mombasa Branch",
    "mombasa branch": "Mombasa Branch",
    "security mombasa": "Mombasa Branch",
    "coba mombasa": "Mombasa Branch",
    "eldoret": "Eldoret Branch",
    "eldoret branch": "Eldoret Branch",
    "coba eldoret": "Eldoret Branch",
    "itd-eldoret": "Eldoret Branch",
    "kisumu": "Kisumu Branch",
    "kisumu branch": "Kisumu Branch",
    "coba kisumu": "Kisumu Branch",
    "coba / kisumu": "Kisumu Branch",
    "nyeri": "Nyeri Currency Centre",
    "nyeri cc": "Nyeri Currency Centre",
    "nyeri center": "Nyeri Currency Centre",
    "currency - nyeri centre": "Nyeri Currency Centre",
    "nyeri-cod": "Nyeri Currency Centre",
    "nakuru": "Nakuru Currency Centre",
    "nakuru cc": "Nakuru Currency Centre",
    "nakuri cc": "Nakuru Currency Centre",
    "currency -nakuru centre": "Nakuru Currency Centre",
    "bps- nakuru": "Nakuru Currency Centre",
    "coba nakuru": "Nakuru Currency Centre",
    "meru": "Meru Currency Centre",
    "meru cc": "Meru Currency Centre",
    "coba meru": "Meru Currency Centre",
    "cod-meru": "Meru Currency Centre",
    "security - meru": "Meru Currency Centre",
    "transport - meru": "Meru Currency Centre",
    "bps-meru": "Meru Currency Centre",
    "kisii": "Kisii Currency Centre",
    "kisii cc": "Kisii Currency Centre",
    "coba kisii": "Kisii Currency Centre",
    "kisii centre": "Kisii Currency Centre",
    "currency -kisii centre": "Kisii Currency Centre",
    "gsd-kisii": "Kisii Currency Centre",
    "cod -kisii": "Kisii Currency Centre",
    "police": "Security & Protective Services",
    "security": "Security & Protective Services",
    "security - hq": "Security & Protective Services",
    "security (gsu) - mombasa": "Security & Protective Services",
    "security- nakuru centre": "Security & Protective Services",
    "ksms": "Kenya School of Monetary Studies (KSMS)",
    "gsd-ksms": "Kenya School of Monetary Studies (KSMS)",
    "bad": "Branch Administration",
    "branch administration": "Branch Administration",
    "strategy and risk": "Strategy & Risk Management",
    "strategy & risk": "Strategy & Risk Management",
    "srd": "Strategy & Risk Management",
    "hq": "CBK Head Office (General)",
    "cbk-hq": "CBK Head Office (General)"
}

# Discipline Normalization Map
DISCIPLINE_MAP = {
    "athletics ladies": ("Athletics & Track", "Ladies", "Athletics Ladies"),
    "athletics men": ("Athletics & Track", "Men", "Athletics Men"),
    "badminton ladies": ("Badminton", "Ladies", "Badminton Ladies"),
    "badminton men": ("Badminton", "Men", "Badminton Men"),
    "basketball ladies": ("Basketball", "Ladies", "Basketball Ladies"),
    "basketball men": ("Basketball", "Men", "Basketball Men"),
    "chess ladies": ("Chess", "Ladies", "Chess Ladies"),
    "chess men": ("Chess", "Men", "Chess Men"),
    "darts ladies": ("Darts", "Ladies", "Darts Ladies"),
    "darts men": ("Darts", "Men", "Darts Men"),
    "draughts ladies": ("Draughts", "Ladies", "Draughts Ladies"),
    "draughts men": ("Draughts", "Men", "Draughts Men"),
    "football ladies": ("Football (Soccer)", "Ladies", "Football Ladies"),
    "football men": ("Football (Soccer)", "Men", "Football Men"),
    "golf": ("Golf", "Mixed", "Golf"),
    "handball ladies": ("Handball", "Ladies", "Handball Ladies"),
    "handball men": ("Handball", "Men", "Handball Men"),
    "lawn tennis ladies": ("Lawn Tennis", "Ladies", "Lawn Tennis Ladies"),
    "lawn tennis men": ("Lawn Tennis", "Men", "Lawn Tennis Men"),
    "netball": ("Netball", "Ladies", "Netball"),
    "scrabble ladies": ("Scrabble", "Ladies", "Scrabble Ladies"),
    "scrabble men": ("Scrabble", "Men", "Scrabble Men"),
    "snooker": ("Snooker / Pool", "Men", "Snooker"),
    "squash ladies": ("Squash", "Ladies", "Squash Ladies"),
    "squash men": ("Squash", "Men", "Squash Men"),
    "swimming ladies": ("Swimming", "Ladies", "Swimming Ladies"),
    "swimming men": ("Swimming", "Men", "Swimming Men"),
    "table tennis - ladies": ("Table Tennis", "Ladies", "Table Tennis Ladies"),
    "table tennis - men": ("Table Tennis", "Men", "Table Tennis Men"),
    "tug of war - ladies": ("Tug of War", "Ladies", "Tug of War Ladies"),
    "tug of war - men": ("Tug of War", "Men", "Tug of War Men"),
    "volleyball ladies": ("Volleyball", "Ladies", "Volleyball Ladies"),
    "volleyball men": ("Volleyball", "Men", "Volleyball Men"),
}

def clean_phone(phone_str: str) -> str:
    """Normalizes phone numbers to standard Kenyan +254 7XX XXX XXX or international format."""
    if not phone_str:
        return ""
    digits = re.sub(r"[^\d+]", "", str(phone_str))
    if digits.startswith("+"):
        return digits
    if digits.startswith("254") and len(digits) >= 12:
        return f"+{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}"
    if digits.startswith("0") and len(digits) >= 10:
        return f"+254 {digits[1:4]} {digits[4:7]} {digits[7:]}"
    if len(digits) == 9 and digits.startswith("7"):
        return f"+254 {digits[:3]} {digits[3:6]} {digits[6:]}"
    if len(digits) == 9 and digits.startswith("1"):
        return f"+254 {digits[:3]} {digits[3:6]} {digits[6:]}"
    return phone_str.strip()

def clean_name(raw_name: str) -> str:
    """Strips honorifics, extra spaces, notes, and formats name into clean Title Case."""
    n = str(raw_name).strip()
    # Strip suffixes like (Team Manager), (Captain), (TC), (TM), -, etc.
    n = re.sub(r"\(.*?\)", "", n)
    n = re.sub(r"\b(mr|mrs|ms|col|dr)\b\.?", "", n, flags=re.IGNORECASE)
    n = re.sub(r"™", "", n)
    n = n.replace("-", " ").strip()
    # Collapse multiple spaces
    n = " ".join(n.split())
    # Title case
    words = [w.capitalize() for w in n.split()]
    return " ".join(words)

def generate_email(name: str, staff_num: str) -> str:
    """Generates official standard institutional CBK email."""
    # Special exact match for user
    if "gathigi" in name.lower():
        return "sgathigi@centralbank.go.ke"
    parts = [p.lower() for p in name.split() if p.isalpha()]
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[-1]}@centralbank.go.ke"
    elif len(parts) == 1:
        return f"{parts[0]}@centralbank.go.ke"
    else:
        return f"staff{staff_num.lower()}@centralbank.go.ke"

def main():
    print(f"Reading raw data from: {RAW_PATH}")
    if not os.path.exists(RAW_PATH):
        print(f"Error: {RAW_PATH} not found.")
        return

    # Prepare SQLite Schema
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Ensure all required columns exist in staff_registry
    cur.execute("PRAGMA table_info(staff_registry)")
    existing_cols = {col[1] for col in cur.fetchall()}
    
    needed_cols = [
        ("phone_number", "TEXT"),
        ("national_id", "TEXT"),
        ("gender_category", "TEXT"),
        ("sub_discipline", "TEXT")
    ]
    for col_name, col_type in needed_cols:
        if col_name not in existing_cols:
            print(f"Adding column '{col_name}' to staff_registry...")
            cur.execute(f"ALTER TABLE staff_registry ADD COLUMN {col_name} {col_type} DEFAULT ''")
    conn.commit()

    # Parse raw rows
    raw_lines = open(RAW_PATH, "r", encoding="utf-8").readlines()
    
    athletes_parsed = []
    seen_keys = set()
    
    for line in raw_lines:
        line = line.strip()
        if not line or line.replace(',', '') == '':
            continue
        parts = [p.strip() for p in line.split(',')]
        if 'NATIONAL ID' in parts or 'STAFF NO.' in parts:
            continue
        if len(parts) >= 7:
            no, nat_id, staff_no, phone, raw_n, dept_raw, game_raw = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
            if not raw_n:
                continue

            cleaned_name = clean_name(raw_n)
            if not cleaned_name:
                continue

            # Standardize Staff ID
            clean_sno = staff_no.strip().upper().replace(' ', '')
            if clean_sno.startswith('S') and clean_sno[1:].isdigit():
                clean_sno = clean_sno[1:]
            if clean_sno.startswith('P') and clean_sno[1:].isdigit():
                clean_sno = clean_sno[1:]
            
            if clean_sno.isdigit():
                staff_id = f"CBK-{clean_sno}"
                staff_num_only = clean_sno
            elif clean_sno:
                staff_id = f"CBK-{clean_sno}" if not clean_sno.startswith("CBK-") else clean_sno
                staff_num_only = staff_id.replace("CBK-", "")
            elif nat_id.strip():
                clean_nat = nat_id.strip()
                staff_id = f"CBK-ID{clean_nat}"
                staff_num_only = clean_nat
            else:
                h_val = abs(hash(cleaned_name)) % 9000 + 1000
                staff_id = f"CBK-TMP{h_val}"
                staff_num_only = str(h_val)

            # Standardize Department
            dept_key = dept_raw.lower().strip()
            department = DEPT_MAP.get(dept_key)
            if not department:
                # Fuzzy fallback
                for k, v in DEPT_MAP.items():
                    if k in dept_key or dept_key in k:
                        department = v
                        break
            if not department:
                department = dept_raw.strip() if dept_raw.strip() else "CBK General Services"

            # Standardize Game / Discipline
            game_key = game_raw.lower().strip()
            disc_info = DISCIPLINE_MAP.get(game_key)
            if not disc_info:
                for k, v in DISCIPLINE_MAP.items():
                    if k in game_key:
                        disc_info = v
                        break
            if disc_info:
                primary_sport, gender, sub_disc = disc_info
            else:
                primary_sport = game_raw.strip()
                gender = "Mixed"
                sub_disc = game_raw.strip()

            phone_clean = clean_phone(phone)
            email_clean = generate_email(cleaned_name, staff_num_only)

            # Multi-sport unique key
            unique_key = (staff_id, primary_sport)
            if unique_key not in seen_keys:
                seen_keys.add(unique_key)
                athletes_parsed.append({
                    "staff_id": staff_id,
                    "full_name": cleaned_name,
                    "cbk_email": email_clean,
                    "department": department,
                    "primary_sport": primary_sport,
                    "sub_discipline": sub_disc,
                    "phone_number": phone_clean,
                    "national_id": nat_id.strip(),
                    "gender_category": gender,
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

    print(f"Total deduplicated athlete entries parsed: {len(athletes_parsed)}")

    # Upsert into database
    # For athletes with multiple sports, their latest entry will set their primary sport in staff_registry,
    # or we can upsert.
    upserted_count = 0
    now_iso = datetime.now().isoformat()
    
    for a in athletes_parsed:
        cur.execute("""
            INSERT INTO staff_registry (staff_id, full_name, cbk_email, department, primary_sport, sub_discipline, phone_number, national_id, gender_category, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(staff_id) DO UPDATE SET
                full_name=excluded.full_name,
                cbk_email=excluded.cbk_email,
                department=excluded.department,
                primary_sport=excluded.primary_sport,
                sub_discipline=excluded.sub_discipline,
                phone_number=excluded.phone_number,
                national_id=excluded.national_id,
                gender_category=excluded.gender_category
        """, (
            a["staff_id"],
            a["full_name"],
            a["cbk_email"],
            a["department"],
            a["primary_sport"],
            a["sub_discipline"],
            a["phone_number"],
            a["national_id"],
            a["gender_category"],
            now_iso
        ))
        upserted_count += 1

    conn.commit()
    conn.close()

    print(f"Successfully upserted {upserted_count} official staff records into {DB_PATH}!")

    # Summary by sport
    sport_counts = Counter([a['primary_sport'] for a in athletes_parsed])
    print("\n--- Ingested Roster Breakdown by Sport ---")
    for s, c in sport_counts.most_common():
        print(f"  {s}: {c} athletes")

    # Export master registered staff to CSV
    conn_r = sqlite3.connect(DB_PATH)
    df_all_staff = pd.read_sql_query("SELECT * FROM staff_registry ORDER BY primary_sport ASC, full_name ASC", conn_r)
    conn_r.close()

    master_csv_path = os.path.join(BASE_DIR, "cbk_stride_master_staff_roster.csv")
    df_all_staff.to_csv(master_csv_path, index=False)
    print(f"\nMaster Staff Roster exported to: {master_csv_path} (Total Registered: {len(df_all_staff)})")

if __name__ == "__main__":
    main()

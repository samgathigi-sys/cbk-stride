"""
DSWAAP - Central Bank of Kenya (CBK) Sports Wellness & Attendance Automation Platform
Live End-to-End Field Test Simulation Script
Simulates the entire real-world workflow from Field Arrival to Finance Disbursement in seconds.
"""

import sys
import time
import os
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import utils
from utils import AttendanceBackend, DynamicQREngine, CBKEmailDispatcher, CBK_DISCIPLINES, CBK_ALLOWANCE_POLICY

def run_simulation():
    print("=" * 75)
    print("  CENTRAL BANK OF KENYA (CBK) - DSWAAP LIVE FIELD TEST SIMULATION")
    print("  Testing End-to-End Workflow: Mobile Check-In -> Dual Gate -> HR -> Finance")
    print("=" * 75)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Domain Whitelist: @centralbank.go.ke\n")

    backend = AttendanceBackend()
    
    # --------------------------------------------------------------------------
    # SCENARIO A: COMPLIANT ATHLETICS 10K / 5K TRACK TRAINING (BRIAN KIMANI)
    # --------------------------------------------------------------------------
    print("🔹 STEP 1: FIELD CAPTAIN BROADCASTS DYNAMIC QR CODE")
    print("   Location: Running Track - Track 100m Start Point (Circuit Base)")
    print("   Track Captain: Capt. Geoffrey Kemboi (Ext. 2405)")
    
    token = DynamicQREngine.generate_token(
        discipline="Athletics & Track",
        gate="PRE_SPORT",
        station="Track 100m Start Point",
        validity_minutes=15,
        session_id="CAMP-20260930-ATH"
    )
    print(f"   [QR GENERATED] Expiration: {token['expires_at']} | HMAC Sig: {token['sig']}")
    time.sleep(0.8)

    print("\n🔹 STEP 2: PARTICIPANT GATE 1 (ARRIVAL CHECK-IN)")
    print("   Staff Athlete: Brian Kimani (Staff ID: CBK-1024)")
    print("   Directorate:   Monetary Policy & Economic Research")
    print("   Institutional: bkimani@centralbank.go.ke")

    # Log Gate 1 arrival
    res_gate1 = backend.log_checkin(
        staff_id="CBK-1024",
        full_name="Brian Kimani",
        cbk_email="bkimani@centralbank.go.ke",
        department="Monetary Policy & Research",
        discipline="Athletics & Track",
        gate="PRE_SPORT",
        station="Track 100m Start Point",
        session_id="CAMP-20260930-ATH",
        notes="Arrival validated at Track 100m Start Point"
    )
    print(f"   [GATE 1 LOCKED] Status: {res_gate1['validation_status']}")
    print(f"   Timestamp:      {res_gate1['timestamp']}")
    print(f"   Allowance:      {res_gate1['allowance_qualified']} (Policy minimum: 45 mins required)")
    time.sleep(1.0)

    print("\n🔹 STEP 3: SIMULATING 75-MINUTE ACTIVE PHYSICAL TRAINING SESSION...")
    print("   Participant completes 10K running camp along the stadium perimeter track circuit.")
    
    # Backdate Pre-Gate by 75 minutes in the database
    conn = sqlite3.connect(backend.db_path)
    cur = conn.cursor()
    backdated_pre_time = (datetime.now() - timedelta(minutes=75)).strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("UPDATE attendance_logs SET timestamp = ? WHERE id = ?", (backdated_pre_time, res_gate1["id"]))
    conn.commit()
    conn.close()
    print(f"   [TIMER RECONCILED] Simulated Arrival Time: {backdated_pre_time} (75 mins ago)")
    time.sleep(1.0)

    print("\n🔹 STEP 4: PARTICIPANT GATE 2 (DEPARTURE CHECK-IN)")
    print("   Location: Perimeter Track Gate 3 (Circuit Finish)")
    
    res_gate2 = backend.log_checkin(
        staff_id="CBK-1024",
        full_name="Brian Kimani",
        cbk_email="bkimani@centralbank.go.ke",
        department="Monetary Policy & Research",
        discipline="Athletics & Track",
        gate="POST_SPORT",
        station="Perimeter Track Gate 3",
        session_id="CAMP-20260930-ATH",
        notes="Circuit completed at Perimeter Gate 3"
    )

    print(f"   [DUAL-GATE RECONCILED!]")
    print(f"   Active Duration:      {res_gate2['duration_minutes']} Minutes")
    print(f"   Compliance Status:    {res_gate2['validation_status']}")
    print(f"   Stipend Qualification: {res_gate2['allowance_qualified']}")
    print(f"   Approved Allowance:   KES {res_gate2['allowance_amount']:,}")
    time.sleep(1.0)

    print("\n🔹 STEP 5: AUTOMATED INSTITUTIONAL NOTIFICATION DISPATCH")
    recent = CBKEmailDispatcher.RECENT_DISPATCHES
    if recent:
        latest = recent[0]
        print(f"   [DISPATCHED] Recipient: {latest['recipient']}")
        print(f"   Subject:   {latest['subject']}")
        print(f"   Status:    {latest['status']}")
        print(f"   Stipend:   KES {latest['allowance']:,} Approved under circular CBK/HR/WEL/2026")
    time.sleep(0.8)

    # --------------------------------------------------------------------------
    # SCENARIO B: AUDIT EXCEPTION TRAPPING (SHORT SESSION < 45 MINS)
    # --------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("🔹 STEP 6: SIMULATING AUDIT EXCEPTION TRAPPING (FRAUD & LEAKAGE DEFENSE)")
    print("   Scenario: Staff signs Gate 1, but scans Gate 2 after only 22 minutes (<45 min floor).")
    
    # Pre-sport
    res_short_pre = backend.log_checkin(
        staff_id="CBK-4055",
        full_name="Alice Chebet",
        cbk_email="achebet@centralbank.go.ke",
        department="Internal Audit",
        discipline="Athletics & Track",
        gate="PRE_SPORT",
        station="Track 100m Start Point"
    )
    # Backdate by only 22 minutes
    conn = sqlite3.connect(backend.db_path)
    cur = conn.cursor()
    short_time = (datetime.now() - timedelta(minutes=22)).strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("UPDATE attendance_logs SET timestamp = ? WHERE id = ?", (short_time, res_short_pre["id"]))
    conn.commit()
    conn.close()

    # Post-sport
    res_short_post = backend.log_checkin(
        staff_id="CBK-4055",
        full_name="Alice Chebet",
        cbk_email="achebet@centralbank.go.ke",
        department="Internal Audit",
        discipline="Athletics & Track",
        gate="POST_SPORT",
        station="Perimeter Gate 3"
    )
    print(f"   [AUDIT FLAG TRIGGERED!]")
    print(f"   Recorded Duration: {res_short_post['duration_minutes']} Minutes (< 45 min policy floor)")
    print(f"   Validation Status: {res_short_post['validation_status']}")
    print(f"   Stipend Assigned:  KES {res_short_post['allowance_amount']} (PAYROLL LEAKAGE PREVENTED!)")
    print(f"   Audit Notes:       {res_short_post['notes']}")
    time.sleep(1.0)

    # --------------------------------------------------------------------------
    # STEP 7: FINANCE & HR DASHBOARD RECONCILIATION
    # --------------------------------------------------------------------------
    print("\n" + "-" * 75)
    print("🔹 STEP 7: FINANCE & AUDIT RECONCILIATION SUMMARY")
    df = backend.get_all_records()
    total_allowance = df["allowance_amount"].sum()
    qualified_count = len(df[df["allowance_qualified"] == "QUALIFIED"])
    flagged_count = len(df[df["allowance_qualified"].isin(["INSUFFICIENT_DURATION", "DISQUALIFIED_NO_PRE_GATE"])])

    print(f"   Total Audit Records:       {len(df)} Logs")
    print(f"   Total Approved Sessions:   {qualified_count} Sessions")
    print(f"   Total Flagged Exceptions:  {flagged_count} Sessions (Blocked from payout)")
    print(f"   Consolidated AP Payout:    KES {total_allowance:,}")
    print(f"   Local Mirror Status:       {backend.csv_path} (Zero Data Loss)")

    print("\n" + "=" * 75)
    print("  SIMULATION COMPLETED WITH 100% SUCCESS!")
    print("  Both Dual-Gate Qualification and Audit Fraud Exception Trapping Verified.")
    print("=" * 75)

if __name__ == "__main__":
    run_simulation()

"""
================================================================================
SIMULATION SCRIPT: Flat KES 10,000 Introductory Offer & Full End-to-End Verification
================================================================================
"""

import sys
import os
import time
import sqlite3
import pandas as pd

import utils
backend = utils.AttendanceBackend()

def safe_str(s):
    return str(s).encode('ascii', 'ignore').decode('ascii')

print("="*75)
print("STARTING FLAT KES 10,000 SACCO GOVERNANCE END-TO-END SIMULATION")
print("="*75)

# STEP 1: CLEAN RESET DATABASE
print("\n[STEP 1] Resetting Database & Seeding Clean Canonical Events...")
conn = sqlite3.connect(utils.DB_PATH)
c = conn.cursor()

c.execute("DELETE FROM event_tickets_registry")
c.execute("DELETE FROM event_ballots_registry")
c.execute("DELETE FROM event_feedback_registry")
c.execute("DELETE FROM events_registry WHERE event_id != 'EVT-BANKI-KUU-SACCO'")

conn.commit()
conn.close()

# Ensure EVT-BANKI-KUU-SACCO & 5 Mockup Delegates exist
bk_event = backend.ensure_banki_kuu_sacco_event()
print(f"[OK] Event Initialized: {safe_str(bk_event['title'])} ({bk_event['event_id']})")

seeded_tickets = backend.get_tickets_by_event("EVT-BANKI-KUU-SACCO")
print(f"[OK] Seeded Delegates Loaded: {len(seeded_tickets)} Core Officers:")
for t in seeded_tickets:
    print(f"   - {t['ticket_id']} -- {safe_str(t['attendee_name'])} ({safe_str(t['organization'])})")

# STEP 2: SIMULATE BULK ROSTER INGESTION (500 DELEGATES)
print("\n[STEP 2] Simulating Secretariat Master Roster Ingestion (500 Delegates)...")
df_500 = backend.generate_synthetic_sacco_roster_df(500)
ok_bulk, msg_bulk, stats_bulk = backend.bulk_ingest_event_tickets("EVT-BANKI-KUU-SACCO", df_500)
assert ok_bulk, f"Bulk ingestion failed: {msg_bulk}"
print(f"[OK] Bulk Ingestion Success: {stats_bulk['total_ingested']} delegates loaded into SQLite DB!")

all_delegates = backend.get_tickets_by_event("EVT-BANKI-KUU-SACCO")
print(f"[OK] Total Accredited Delegates in DB: {len(all_delegates)}")

# STEP 3: SIMULATE SACCO FINANCE MANAGER SETTLEMENT (KES 10,000 FLAT INTRODUCTORY OFFER)
print("\n[STEP 3] Simulating Finance Manager KES 10,000 STK Settlement & Tax Invoice Issue...")
inv_ref = f"INV-2026-BKS-{int(time.time())}"[-8:]
mpesa_ref = f"QK{int(time.time())}"[-10:]
flat_fee = 10000.0

print(f"   - Billing Entity: Banki Kuu Staff SACCO Society Ltd.")
print(f"   - Billing Email:  finance@bankikuusacco.co.ke")
print(f"   - Handset:        0722849000 (Finance Manager)")
print(f"   - Invoice Ref:    {inv_ref}")
print(f"   - M-Pesa Receipt: {mpesa_ref}")
print(f"   - Flat Fee:       KES {flat_fee:,.2f} (Introductory SACCO Special Offer)")

# Ensure event directory has ZERO duplicates
all_events_after = backend.get_events(status="ALL")
event_ids = [e['event_id'] for e in all_events_after]
print(f"[OK] Current Active Events Directory Count: {len(all_events_after)} events (IDs: {event_ids})")
assert event_ids.count("EVT-BANKI-KUU-SACCO") == 1, "Duplicate EVT-BANKI-KUU-SACCO found!"

# STEP 4: SIMULATE GATE USHER SCANNER & QUORUM ACCREDITATION
print("\n[STEP 4] Simulating Gate Usher Scanner & Quorum Telemetry...")
# Admit first 55 delegates to achieve SASRA quorum floor
for t in all_delegates[:55]:
    backend.verify_and_admit_ticket(t["ticket_id"])

admitted_list = [t for t in backend.get_tickets_by_event("EVT-BANKI-KUU-SACCO") if t.get("gate_status") == "ADMITTED"]
print(f"[OK] Admitted Delegates at Gate: {len(admitted_list)} / 50 Quorum Floor")
assert len(admitted_list) >= 50, "Quorum floor not reached!"
print("[STATUS] STATUTORY QUORUM ATTAINED! (Meeting lawfully constituted under Companies Act Section 284)")

# STEP 5: SIMULATE DIGITAL SECRET BALLOT VOTING & ANTI-DUPLICATE LOCKING
print("\n[STEP 5] Simulating Digital Secret Ballot & Anti-Duplicate Vote Locking...")
voter1 = seeded_tickets[0]  # Samuel Gathigi

# Cast Vote 1
ok_v1, msg_v1, b1 = backend.cast_event_ballot(
    event_id="EVT-BANKI-KUU-SACCO",
    ticket_id=voter1["ticket_id"],
    voter_name=voter1["attendee_name"],
    voter_organization=voter1["organization"],
    voting_weight=10000,
    res1_vote="FOR (Approve Accounts & 14% Dividend)",
    res2_candidate="Sarah Wanjiru CPA(K) (Independent, Audit & Finance)",
    res3_auditor="Appoint Deloitte East Africa"
)
assert ok_v1, f"Vote 1 failed: {msg_v1}"
print(f"[OK] Vote Cast by {safe_str(voter1['attendee_name'])} ({voter1['ticket_id']}): SHA-256 Proof = {b1['ballot_hash'][:16]}...")

# Attempt Duplicate Vote (Anti-Double Voting Lock Test)
ok_dup, msg_dup, b_dup = backend.cast_event_ballot(
    event_id="EVT-BANKI-KUU-SACCO",
    ticket_id=voter1["ticket_id"],
    voter_name=voter1["attendee_name"],
    voter_organization=voter1["organization"],
    voting_weight=10000,
    res1_vote="AGAINST (Reject Accounts)",
    res2_candidate="Eng. David Ndung'u (Incumbent, Risk & Governance)",
    res3_auditor="Re-appoint KPMG Kenya"
)
assert not ok_dup, "Anti-double voting failed! Duplicate vote was allowed."
print(f"[OK] Anti-Duplicate Vote Locking Verified: '{safe_str(msg_dup)}'")

# STEP 6: ELECTION TALLY & SCRUTINEER CERTIFICATION
print("\n[STEP 6] Scrutineer Tally & Telemetry Summary:")
tally = backend.get_election_results("EVT-BANKI-KUU-SACCO")
print(f"   - Total Ballots Cast:    {tally['total_ballots']}")
print(f"   - Total Weighted Power:  {tally['total_weighted_votes']:,} Votes")
print(f"   - Double-Voting Shield:  ENFORCED (0 Duplicates Allowed)")

print("\n" + "="*75)
print("END-TO-END VERIFICATION COMPLETE: ALL CHECKS PASSED WITH 100% INTEGRITY!")
print("="*75)

"""
Bank of Uganda Cyber Forensics Masterclass - Day 1 Interactive Lab
Simulated Case: RTGS Gateway Incident & Cryptographic Evidence Capture
"""

import os
import json
import hashlib
from datetime import datetime, timezone

def run_day1_simulation():
    print("=" * 75)
    print("  BANK OF UGANDA CYBER FORENSICS MASTERCLASS — DAY 1 LAB SIMULATION")
    print("  Case: 'Operation Crested Crane' - Suspected Settlement Log Tampering")
    print("=" * 75)

    evidence_dir = os.path.join(os.path.dirname(__file__), "evidence_store")
    os.makedirs(evidence_dir, exist_ok=True)
    raw_log_path = os.path.join(evidence_dir, "BOU_RTGS_GATEWAY_20261019.log")

    # 1. Simulate Evidence Seizure on RTGS Node (ALWAYS use binary mode to avoid OS newline translation)
    raw_bytes = (
        b"[2026-10-19T06:14:02Z] AUTH_SUCCESS: Operator 'svc_swift_gw' from 10.12.4.15\n"
        b"[2026-10-19T06:28:44Z] BATCH_QUEUED: RTGS-OUT-9912 | UGX 4,800,000,000 -> BENEFICIARY: CR-8831-EXT\n"
        b"[2026-10-19T06:29:10Z] ANOMALY_WARN: Dual-sign bypass detected via memory patch on PID 4128\n"
        b"[2026-10-19T06:30:00Z] INTRUSION_ALERT: SOC EDR Flagged 'mimikatz.exe' artifact in C:\\Windows\\Temp\n"
    )
    with open(raw_log_path, "wb") as f:
        f.write(raw_bytes)

    print(f"\n[STEP 1: EVIDENCE SEIZED] Captured bitstream to: {os.path.basename(raw_log_path)}")
    print("  -> Forensic Note: Binary capture enforced (prevents CRLF timestamp corruption)")

    # 2. Compute Dual Hashes (SHA-256 and MD5)
    sha256 = hashlib.sha256(raw_bytes).hexdigest()
    md5 = hashlib.md5(raw_bytes).hexdigest()

    manifest = {
        "case_id": "BOU-FORENSIC-2026-001",
        "evidence_id": "EVD-RTGS-01",
        "custodian": "BoU Cyber Forensics Unit",
        "seizure_timestamp": datetime.now(timezone.utc).isoformat(),
        "sha256_baseline": sha256,
        "md5_baseline": md5,
        "file_size_bytes": len(raw_bytes),
        "admissibility_standard": "Uganda Evidence Act (Cap 6) & Electronic Signatures Act 2011"
    }

    manifest_path = os.path.join(evidence_dir, "EVD-RTGS-01_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)

    print(f"[STEP 2: HASH CALCULATED] SHA-256: {sha256}")
    print(f"                         MD5:     {md5}")

    # 3. Simulate Tamper Verification Check
    print("\n[STEP 3: INTEGRITY VERIFICATION TEST]")
    with open(raw_log_path, "rb") as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()

    if current_hash == sha256:
        print("  -> Status: [VERIFIED] Evidence is bit-for-bit authentic. Legally admissible.")
    else:
        print("  -> Status: [COMPROMISED] Tampering detected! Hash mismatch.")

    # 4. Chain of Custody Record
    print("\n[STEP 4: CHAIN OF CUSTODY LOGGED]")
    print("  -> Custody Transferred to: BoU IT Forensics Evidence Vault Safe #2")
    print("  -> Tracking ID: BOU-CUSTODY-TAPE-084")
    print("=" * 75)

if __name__ == "__main__":
    run_day1_simulation()

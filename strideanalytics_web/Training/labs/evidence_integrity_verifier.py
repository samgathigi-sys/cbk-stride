"""
Bank of Uganda Cyber Forensics Masterclass - Lab 1
Evidence Integrity & Chain of Custody Verification Suite
Compliant with ISO/IEC 27037 and Uganda Electronic Signatures Act, 2011
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

class EvidenceIntegrityVerifier:
    def __init__(self, investigator_name="BoU Forensic Examiner", case_id="BOU-CYBER-2026-001"):
        self.investigator_name = investigator_name
        self.case_id = case_id

    def calculate_hashes(self, file_path: str, chunk_size=65536) -> dict:
        """Calculate SHA-256 and MD5 hashes simultaneously for digital evidence."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Evidence file not found: {file_path}")

        sha256 = hashlib.sha256()
        md5 = hashlib.md5()
        file_size = os.path.getsize(file_path)

        with open(file_path, "rb") as f:
            while chunk := f.read(chunk_size):
                sha256.update(chunk)
                md5.update(chunk)

        manifest = {
            "case_id": self.case_id,
            "investigator": self.investigator_name,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "evidence_target": os.path.abspath(file_path),
            "file_size_bytes": file_size,
            "sha256": sha256.hexdigest(),
            "md5": md5.hexdigest(),
            "forensic_status": "AUTHENTICATED_SECURE"
        }
        return manifest

    def verify_evidence(self, file_path: str, expected_sha256: str) -> bool:
        """Verify whether an evidence file maintains byte-for-byte integrity."""
        current_manifest = self.calculate_hashes(file_path)
        is_valid = current_manifest["sha256"].lower() == expected_sha256.lower()
        return is_valid

def demo_evidence_verification():
    print("=" * 70)
    print("  BANK OF UGANDA CYBER FORENSICS LAB 1: EVIDENCE INTEGRITY SUITE")
    print("=" * 70)
    
    # Create sample evidence file for testing
    sample_file = "sample_rtgs_transaction_log.evd"
    with open(sample_file, "w", encoding="utf-8") as f:
        f.write("[2026-10-19 14:15:02] RTGS-OUT: ACCT:9901-BOU-SETTLE AMOUNT:UGX 1,500,000,000 STATUS:AUTHENTICATED\n")
        f.write("[2026-10-19 14:22:15] ALERT: UNUSUAL TRANSFER FLAGGED BY SOC GATEWAY 10.12.4.99\n")
    
    verifier = EvidenceIntegrityVerifier(investigator_name="Cyber Forensics Specialist", case_id="BOU-INC-2026-99")
    manifest = verifier.calculate_hashes(sample_file)

    print("\n[+] Evidence Manifest Generated:")
    print(json.dumps(manifest, indent=4))

    print("\n[+] Testing Integrity Verification:")
    verified = verifier.verify_evidence(sample_file, manifest["sha256"])
    print(f"    Hash Match: {verified} | Evidence Integrity Intact: {verified}")

    # Clean up test artifact
    if os.path.exists(sample_file):
        os.remove(sample_file)

if __name__ == "__main__":
    demo_evidence_verification()

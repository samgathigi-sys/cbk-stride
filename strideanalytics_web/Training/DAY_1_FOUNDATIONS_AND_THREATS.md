# Day 1: Foundations of Central Bank Digital Forensics & Threat Landscape

## 📌 Executive Agenda
- **09:00 - 10:30**: Introduction to Digital Forensics & Sovereign Financial Infrastructure
- **10:45 - 12:30**: Digital Evidence Taxonomy & The Role of the Digital Forensic Investigator
- **13:30 - 15:00**: Threat Modeling: Banking Vectors (RTGS, SWIFT, Core Banking, Mobile Money Integrations)
- **15:15 - 16:30**: **Lab 1**: Evidence Integrity, Cryptographic Hashing, and Live Incident Verification

---

## 1. Principles of Forensic Soundness (ISO/IEC 27037)
When handling systems at Bank of Uganda:
1. **Never work on original evidence**: Always acquire bit-stream disk or memory clones before examination.
2. **Order of Volatility (RFC 3227)**:
   - Registers, cache
   - Routing table, ARP cache, process table, kernel memory
   - System memory (RAM)
   - Temporary file systems / swap space
   - Disk storage (HDD, NVMe, SAN arrays)
   - Remote logging & network topology
   - Physical media / backup tapes
3. **Cryptographic Validation**:
   - Compute dual hashes (SHA-256 and MD5) immediately upon acquisition.
   - Maintain identical verification hashes across every copy and post-analysis step.

---

## 2. Threat Modeling for Central Bank Systems
Bank of Uganda protects the monetary infrastructure of the nation. Attack vectors of note:
- **SWIFT / Payment Gateway Compromise**: Tampering with financial messaging interfaces (e.g., Carbanak, Lazarus group techniques).
- **Core Banking & RTGS Manipulations**: Unauthorized direct credit adjustments, synthetic accounts, transaction replay.
- **Ransomware & Double Extortion**: Hostage of hypervisors and storage area networks (SAN) combined with exfiltration of confidential reserve data.
- **Malicious Insiders & Privileged Credential Abuse**: Circumvention of dual-control authorization and audit log tampering.

---

## 3. Hands-On Lab 1: Evidence Integrity & Verification Suite
See `labs/evidence_integrity_verifier.py` to generate cryptographic baseline manifests and tamper-evident logs for seized digital assets.

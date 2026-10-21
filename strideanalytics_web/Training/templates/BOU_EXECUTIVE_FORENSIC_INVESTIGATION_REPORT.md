# BANK OF UGANDA
## FORENSIC INVESTIGATION REPORT & INCIDENT DOSSIER
**CONFIDENTIAL // LAW ENFORCEMENT & EXECUTIVE COMMITTEE RESTRICTED**

---

### 1. Document Control & Metadata
- **Report Reference:** BOU-FOR-REP-2026-`[ID]`
- **Date of Report:** `YYYY-MM-DD`
- **Lead Investigator:** `[Name, Qualifications, Title]`
- **Peer Reviewer / Quality Assurance:** `[Name, Title]`
- **Target Systems:** `[Payment Gateway / Core Banking / Domain Controllers]`
- **Governing Legislation:** Uganda Computer Misuse Act (2011/2022), Electronic Signatures Act (2011)

---

### 2. Executive Summary
*(Non-technical summary for the Governor, Deputy Governor, and Executive Committee)*
- **Incident Overview:**
- **Financial & Operational Impact:**
- **Attribution & Adversary Assessment:**
- **Current Status of Containment:**

---

### 3. Scope of Investigation & Evidentiary Chain of Custody
- **Mandate:** `[Authority under which the investigation was conducted]`
- **Evidence Acquired:**
  | Item ID | Source Device | Media Type | Acquisition Date | SHA-256 Hash |
  | :--- | :--- | :--- | :--- | :--- |
  | `EVD-01` | Host `BOU-SRV-04` | RAM Image | `2026-10-19 10:14 EAT` | `e3b0c442...` |
  | `EVD-02` | Core Switch Tap | PCAP Trace | `2026-10-19 11:30 EAT` | `8c5a2b10...` |

---

### 4. Technical Analysis & Forensic Findings
#### 4.1 Initial Access & Attack Vector
*(Phishing email analysis, perimeter firewall logs, exploited vulnerabilities)*

#### 4.2 Lateral Movement & Privilege Escalation
*(Active Directory event logs, credential dumping artifacts, PsExec/WMI activity)*

#### 4.3 Malicious Payloads & Command & Control (C2)
*(Reverse shell IPs, domain fronting, persistence mechanisms in Registry/Scheduled Tasks)*

#### 4.4 Impact on Financial Transactions & Data
*(Reconstructed wire orders, database audit logs, data exfiltration volume)*

---

### 5. Timeline of Events (Chronological Reconstruction)
| Timestamp (EAT) | Source System | Actor / Process | Activity Description | Evidence Reference |
| :--- | :--- | :--- | :--- | :--- |
| `2026-10-18 23:14:02` | Ingress Firewall | External IP `198.51.100.24` | Exploitation probe against VPN portal | Firewall Log L-812 |
| `2026-10-18 23:42:19` | `BOU-DC-01` | `NT AUTHORITY\SYSTEM` | Unauthorized token impersonation | Security EVTX ID 4624 |

---

### 6. Legal & Regulatory Defensibility (Uganda Jurisdiction)
- **Breaches of Uganda Law Identified:**
  - Section 12 (Unauthorized Access) – *Computer Misuse Act*
  - Section 15 (Unauthorized Modification) – *Computer Misuse Act*
  - Section 20 (Electronic Fraud) – *Computer Misuse Act*
- **Evidentiary Integrity Certification:** All evidence was imaged with hardware write-blocking and bit-stream verification complying with the Uganda Evidence Act.

---

### 7. Recommendations & Remediation Plan
1. **Immediate Tactical Actions (0 - 48 Hours):**
2. **Systemic Architectural Hardening (1 - 30 Days):**
3. **Governance & Audit Enhancements (Quarterly):**

---

### 8. Signatures & Investigator Certification
I certify that the findings and opinions expressed in this report are based on objective technical analysis performed in accordance with internationally accepted digital forensics practices.

**Lead Forensic Examiner:** ___________________________  Date: ___________  
**Head of Information Security (BoU):** ___________________________  Date: ___________

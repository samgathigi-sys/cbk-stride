# CENTRAL BANK OF KENYA (CBK)
## Sports Wellness & Attendance Automation Platform (DSWAAP)
### Comprehensive Project Proposal & System Architecture Specification
**Document Reference:** CBK/SEC/WEL/2026/04  
**Date:** September 30, 2026  
**Target Directorate:** Sports & Wellness Secretariat, Human Resources, Finance & Accounts, Internal Audit  
**Classification:** Confidential - Internal Banking Operations  

---

## 1. Executive Summary
The **Central Bank of Kenya Sports Wellness & Attendance Automation Platform (DSWAAP)** is an enterprise-grade, mobile-first digital attendance and allowance compliance ecosystem. Engineered to modernise the Central Bank's sports and staff physical wellness operations, DSWAAP addresses systemic operational bottlenecks across all **18 institutional sporting disciplines** (including complex distributed sports such as Golf).

By replacing vulnerable manual paper signing sheets with a **Dual-Gate Dynamic QR Verification Architecture**, real-time **Google Sheets API synchronization**, and automated **institutional email dispatching**, DSWAAP enforces ironclad audit compliance, automates sports allowance stipend ledgers, and equips CBK leadership with real-time operational and HR wellness analytics.

---

## 2. Problem Statement & Legacy Vulnerabilities
Historically, CBK sports camps, daily training sessions, and inter-bank championship preparations relied on manual clipboards and sign-in sheets. This legacy approach introduced severe governance and operational deficiencies:

1. **Ghost Attendance & Proxy Signatures:** Staff could sign attendance registers for absent colleagues or sign once and depart immediately without participating in training.
2. **Delayed Stipend Reconciliations:** Processing monthly sports allowances required manually deciphering hundreds of physical sheets, leading to reconciliation backlogs exceeding 3-4 weeks.
3. **Audit Exposure & Inadequate Timestamps:** Internal Audit had no verifiable timestamp records to confirm whether an employee completed the mandatory 45-minute minimum session duration.
4. **Dispersed Venue Logistics:** Specialized sports like **Golf**, played across an 18-hole course, or off-site running loops lacked fixed turnstile access, making attendance verification practically impossible.
5. **Lack of Executive Visibility:** Human Resources and Senior Management lacked data-driven metrics on departmental wellness engagement, gender parity, or sport popularity.

---

## 3. Core Architecture & Strategic Innovations

```
                       +-----------------------------------------------+
                       |           CBK DSWAAP WEB APPLICATION          |
                       |       (Streamlit Mobile-First Responsive)     |
                       +-----------------------+-----------------------+
                                               |
             +---------------------------------+---------------------------------+
             |                                 |                                 |
             v                                 v                                 v
+------------------------+        +------------------------+        +------------------------+
| 📱 MOBILE CHECK-IN     |        | 🏷️ CAPTAIN QR BROADCAST|        | 🏛️ EXECUTIVE CONSOLES  |
| - Gate 1: Pre-Sport    |        | - Dynamic HMAC Refresh |        | - Secretariat Live Ops |
| - Gate 2: Post-Sport   |        | - 18 Disciplines       |        | - HR Wellness Command  |
| - Auto Staff ID Lookup |        | - Multi-Station (Golf) |        | - Finance Audit Ledger |
+-----------+------------+        +-----------+------------+        +-----------+------------+
            |                                 |                                 |
            +---------------------------------+---------------------------------+
                                               |
                                               v
                       +-----------------------------------------------+
                       |              HYBRID STORAGE ENGINE            |
                       | - High-Speed SQLite Local Database (ACID)     |
                       | - Instant CSV Mirroring (Offline Resilient)   |
                       | - Real-Time Google Sheets API (gspread v6)    |
                       +-----------------------+-----------------------+
                                               |
                                               v
                       +-----------------------------------------------+
                       |      INSTITUTIONAL EMAIL DISPATCHER (SMTP)    |
                       | - Branded HTML Dual-Verification Certificates |
                       | - Automated Delivery to @centralbank.go.ke Inboxes |
                       +-----------------------------------------------+
```

### 3.1 Dual-Gate Dynamic QR Verification
DSWAAP introduces a rigorous two-step verification gate:
- **Gate 1 (Pre-Sport Arrival Check-In):** Scanned at the start of training. Captures staff credentials, timestamp, sport discipline, and entry station. Status transitions to `PRE_SPORT_VALIDATED`, and allowance status is marked `AWAITING_POST_GATE`.
- **Gate 2 (Post-Sport Departure Check-In):** Scanned upon completing the workout. The system algorithmically matches the employee's ID and discipline against the morning/evening session arrival, calculates the exact active duration in minutes, and validates compliance against the 45-minute policy floor.
- **Dynamic Time-Bounded QR Codes:** Captains and course marshals display dynamic QR codes featuring cryptographic HMAC signatures that rotate every 15-30 minutes, preventing participants from photographing or circulating static codes over messaging apps.

### 3.2 18 Sporting Disciplines & Multi-Station Topology
DSWAAP natively configures all 18 Central Bank disciplines with dedicated stations and captains:
1. **Football (Soccer):** Main Pitch Entry Gate, Team Bench West.
2. **Basketball:** Arena North Gate, Scorer's Table.
3. **Volleyball:** Hard Court Pavilion, Sand Court 1.
4. **Netball:** East Court Gate A.
5. **Athletics & Track:** Track 100m Start Point, Perimeter Gate 3.
6. **Golf (Specialized Multi-Station):**
   - *Station 1:* Clubhouse Pro-Shop Check-In
   - *Station 2:* Tee Box Hole 1 (Front Nine Start)
   - *Station 3:* Halfway House (Hole 9 Green)
   - *Station 4:* Tee Box Hole 10 (Back Nine Start)
   - *Station 5:* 18th Green Marshals Post (Round Completion)
   - *Station 6:* Practice Driving Range
7. **Lawn Tennis:** Court 1 Umpire Desk, Courts 3-4 Gate.
8. **Table Tennis:** Recreation Hall Zone A Reception.
9. **Badminton:** Multi-Purpose Indoor Hall Bay 2.
10. **Swimming:** Poolside Lifeguard Tower, Locker Room Turnstile.
11. **Squash:** Squash Complex Glass Courts 1 & 2.
12. **Darts:** Staff Club Lounge Scorers Station.
13. **Pool / Snooker:** Billiards Desk 1.
14. **Chess:** Quiet Strategy Room 3.
15. **Scrabble:** Quiet Strategy Room 4 Desk.
16. **Tug of War:** Lower Grounds Central Post.
17. **Cycling:** Bicycle Depot Base, Outpost Checkpoint 2.
18. **Physical Fitness & Aerobics:** Gym Main Entrance, Studio Desk A.

---

## 4. Google Sheets Backend & Hybrid Offline Resilience
DSWAAP leverages Google Sheets as a low-friction, institutional data repository:
- **`gspread` v6 Engine:** Connects via service account JSON credentials to push every check-in row to `CBK_DSWAAP_Attendance_Ledger` in real-time.
- **Zero-Data-Loss Local Resilience:** When operating on remote golf fairways or outdoor tracks where internet drops, DSWAAP immediately falls back to its local SQLite database and CSV mirror. Transactions are marked `LOCAL_PERSISTED` and synchronized to Google Sheets upon connectivity restoration.
- **Audit Columns Captured:**
  `Timestamp`, `Date`, `Staff ID`, `Full Name`, `CBK Email`, `Department`, `Discipline`, `Gate`, `Station`, `Session ID`, `Validation Status`, `Duration (Mins)`, `Allowance Qualified`, `Allowance (KES)`, `Audit Notes`.

---

## 5. Institutional Notifications & Financial Compliance
- **Branded Email Receipts:** Every successful dual verification automatically triggers an HTML email with CBK green/gold insignia, timestamp audit table, and verified stipend calculation.
- **Financial Allowance Rules:**
  - *Standard Session Rate:* KES 2,500 for fully compliant dual-gate sessions (duration ≥ 45 minutes).
  - *Short Session Exception:* Sessions < 45 minutes are flagged as `DUAL_VERIFIED_SHORT_SESSION` with KES 0 stipend and logged in the audit ledger.
  - *Single Gate Penalty:* Unpaired check-ins (e.g. participant forgot to scan out) receive `DISQUALIFIED_NO_PRE_GATE` or `AWAITING_POST_GATE`.
  - *One-Click Batch AP Approval:* Accounts Payable can approve the ledger with a single click and export directly to `.xlsx` or `.csv`.

---

## 6. Executive & Operational Dashboards
1. **Secretariat Operational View:** Real-time counters of live athletes on field, discipline status cards (Active, Concluded, Standby), and incoming live activity ticker.
2. **HR Analytics Command Center:** Departmental participation progress bars tracking engagement across all 10 CBK directorates against target quotas, sport popularity bar charts, and category donut charts.
3. **Finance & Audit Compliance Portal:** Detailed timestamp matrix showing Gate 1 Time, Gate 2 Time, Delta Duration, and allowance qualification with batch approval triggers.

---

## 7. Implementation Roadmap & Rollout Strategy
- **Phase 1 (Weeks 1-2): Pilot Deployment** - Pilot in Football, Athletics, and Golf with 50 staff members.
- **Phase 2 (Weeks 3-4): Full 18-Discipline Rollout** - Onboard all discipline captains and integrate with CBK institutional Google Workspace.
- **Phase 3 (Weeks 5-6): Finance & ERP Integration** - Connect automated disbursement ledgers to CBK Oracle/SAP Financials.

**Conclusion:** DSWAAP delivers unprecedented integrity, operational transparency, and administrative savings to the Central Bank of Kenya's sports wellness initiatives.

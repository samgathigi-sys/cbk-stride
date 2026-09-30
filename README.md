# Central Bank of Kenya (CBK)
## Sports Wellness & Attendance Automation Platform (DSWAAP)

Production-ready, mobile-first web application and executive PowerPoint/Markdown presentation generator for the Central Bank of Kenya (CBK) Sports & Wellness Secretariat.

---

## 🌟 Core Architecture & Key Capabilities

1. **Dual-Gate Dynamic QR Verification Workflow:**
   - **Gate 1: Pre-Sport Arrival Check-In:** Staff athlete scans the dynamic QR code generated at their discipline station. Captures arrival timestamp, locks in sport discipline, and establishes session identity.
   - **Gate 2: Post-Sport Departure Check-In:** Staff athlete scans the closing QR code upon workout completion.
   - **Automated Duration & Allowance Reconciler:** DSWAAP reconciles both gates, computes active training minutes, and evaluates compliance against the CBK mandatory policy floor (≥ 45 minutes). Compliant sessions automatically qualify for the standard KES 2,500 daily sports stipend.
   - **Dynamic Cryptographic HMAC Signatures:** Station QR codes refresh automatically on a 15–30 minute interval to prevent static screenshot sharing or proxy attendance.

2. **18 Institutional Sporting Disciplines & Multi-Station Topology:**
   - Pre-configured with all 18 CBK sports: Football, Basketball, Volleyball, Netball, Athletics & Track, Golf, Lawn Tennis, Table Tennis, Badminton, Swimming, Squash, Darts, Pool/Snooker, Chess, Scrabble, Tug of War, Cycling, and Physical Fitness & Aerobics.
   - **Specialized Golf Multi-Station Support:** Distributed course marshal stations across the 18-hole course:
     - Station 1: Clubhouse Pro-Shop Check-In
     - Station 2: Tee Box Hole 1 (Front Nine Start)
     - Station 3: Halfway House (Hole 9 Green Transition)
     - Station 4: Tee Box Hole 10 (Back Nine Start)
     - Station 5: 18th Green Marshals Post (Round Completion)
     - Station 6: Practice Driving Range

3. **Hybrid Real-Time Google Sheets Backend & Offline Resilience:**
   - **Real-Time Google Sheets API (`gspread` v6):** Synchronizes every check-in row to `CBK_DSWAAP_Attendance_Ledger` in real time.
   - **Zero-Data-Loss Offline Fallback:** If internet is disrupted on remote golf fairways or outdoor tracks, DSWAAP immediately falls back to high-speed local SQLite persistence and an instant CSV ledger mirror (`cbk_dswaap_records.csv`).
   - **Logged Audit Fields:** Timestamp, Date, Staff ID, Full Name, CBK Institutional Email (`@centralbank.go.ke`), Department, Discipline, Gate (Pre/Post), Station, Session ID, Validation Status, Duration (Mins), Allowance Qualified, Allowance (KES), and Audit Notes.

4. **Executive & Operational Command Consoles:**
   - **Secretariat Operational View:** Real-time athlete counters, live 18-discipline operational matrix, and chronological activity stream.
   - **HR Analytics Command Center:** Departmental participation progress bars tracking engagement across all 10 CBK Directorates against target quotas, sport popularity bar charts, and wellness leaderboards.
   - **Finance & Audit Compliance Portal:** Dual-gate timestamp audit matrix with duration math, exception flagging for short/unpaired sessions, one-click "Batch Approve for Accounts Payable", and one-click export to signed Excel (`.xlsx`) workbooks and CSV files.

5. **Automated Institutional Email Notifications:**
   - Automated delivery of branded HTML Dual-Verification Receipts directly to institutional inboxes (`@centralbank.go.ke`) with official CBK Green & Gold styling, digital seal, duration breakdown, and stipend approval details.

---

## 🚀 Quickstart & Execution Guide

### 1. Prerequisites & Installation
Ensure Python 3.10+ is installed on your system. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 2. Launching the DSWAAP Web Application
To start the mobile-first Streamlit application:

```bash
streamlit run app.py
```

The web application will open in your browser (typically at `http://localhost:8501`).

### 3. Compiling the Executive Proposal & PowerPoint Presentation
To re-generate the 12-slide 16:9 executive PowerPoint deck and comprehensive Markdown proposal:

```bash
python generate_presentation.py
```
This produces:
- `DSWAAP_Executive_Presentation.pptx`: 16:9 widescreen presentation deck styled in CBK corporate colors with slide layouts, comparison tables, and metric cards.
- `DSWAAP_Executive_Proposal.md`: Boardroom-ready executive proposal and technical specification document.

---

## 📁 Repository Structure

```
cbk-dswaap/
│
├── app.py                         # Main Streamlit web application (Mobile-first UI & 6 interactive tabs)
├── utils.py                       # Core utilities (QR engine, Google Sheets logger, SMTP dispatcher, audit math)
├── generate_presentation.py       # Executive PowerPoint deck & Markdown proposal generator
├── requirements.txt               # Project dependencies (streamlit, qrcode, gspread, pandas, pillow, etc.)
├── README.md                      # Comprehensive project documentation
├── DSWAAP_Executive_Presentation.pptx # Compiled 12-slide 16:9 executive presentation
├── DSWAAP_Executive_Proposal.md   # Compiled technical proposal document
├── cbk_dswaap.db                  # Local SQLite database (ACID audit persistence)
└── cbk_dswaap_records.csv         # Real-time mirrored CSV audit ledger
```

---

## 🏛️ Security & Institutional Compliance
- **HMAC Signatures:** Dynamic QR codes are cryptographically signed using HMAC-SHA256 to prevent tampering or manual manipulation.
- **Domain Verification:** Restricted to verified `@centralbank.go.ke` institutional identities.
- **Audit Trails:** Immutable logging of pre and post timestamps to ensure fiduciary compliance with Central Bank Sports Welfare Policy circular `CBK/HR/WEL/2026`.

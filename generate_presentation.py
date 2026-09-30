"""
DSWAAP - Central Bank of Kenya (CBK) Sports Wellness & Attendance Automation Platform
Presentation & Proposal Generator: Produces DSWAAP_Executive_Proposal.md and DSWAAP_Executive_Presentation.pptx
"""

import os
import io
import sys
from datetime import datetime

import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(OUTPUT_DIR, "DSWAAP_Executive_Proposal.md")
PPTX_PATH = os.path.join(OUTPUT_DIR, "DSWAAP_Executive_Presentation.pptx")

# CBK Corporate Color Palette
COLOR_CBK_GREEN = RGBColor(0, 102, 51)      # #006633 Deep Kenya Green
COLOR_CBK_DARK_GREEN = RGBColor(10, 77, 46) # #0A4D2E Forest Green
COLOR_CBK_GOLD = RGBColor(212, 175, 55)     # #D4AF37 Royal Bank Gold
COLOR_CBK_DARK = RGBColor(26, 26, 26)       # #1A1A1A Slate Dark
COLOR_CBK_LIGHT = RGBColor(248, 249, 250)   # #F8F9FA Clean Background
COLOR_CBK_WHITE = RGBColor(255, 255, 255)
COLOR_CBK_GREY = RGBColor(100, 116, 139)    # #64748B Slate Grey
COLOR_CBK_LIGHT_GREEN = RGBColor(235, 247, 238)
COLOR_CBK_ACCENT_BLUE = RGBColor(29, 78, 216)


# ==============================================================================
# 1. MARKDOWN EXECUTIVE PROPOSAL GENERATOR
# ==============================================================================
def generate_markdown_proposal():
    content = f"""# CENTRAL BANK OF KENYA (CBK)
## Sports Wellness & Attendance Automation Platform (DSWAAP)
### Comprehensive Project Proposal & System Architecture Specification
**Document Reference:** CBK/SEC/WEL/2026/04  
**Date:** {datetime.now().strftime('%B %d, %Y')}  
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
"""
    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Markdown proposal generated at: {MD_PATH}")


# ==============================================================================
# 2. POWERPOINT EXECUTIVE PRESENTATION GENERATOR
# ==============================================================================
def create_slide_header(slide, title_text, category_text="CENTRAL BANK OF KENYA | DSWAAP"):
    """Adds a standard CBK executive header banner to a slide."""
    # Top banner bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_CBK_GREEN
    top_bar.line.fill.background()

    # Gold accent line
    gold_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.08))
    gold_line.fill.solid()
    gold_line.fill.fore_color.rgb = COLOR_CBK_GOLD
    gold_line.line.fill.background()

    # Category / Super-title
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(11.5), Inches(0.3))
    tf = tx_box.text_frame
    tf.word_wrap = True
    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CBK_GOLD

    # Main Title
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_CBK_WHITE


def add_card(slide, left, top, width, height, bg_color=COLOR_CBK_WHITE, border_color=COLOR_CBK_GOLD):
    """Draws a styled card container."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        card.line.fill.background()
    return card


def generate_presentation_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --------------------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE (CBK DEEP GREEN LUXURY COVER)
    # --------------------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_CBK_DARK_GREEN
    bg1.line.fill.background()

    # Gold accent line on top & bottom
    g1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    g1.fill.solid()
    g1.fill.fore_color.rgb = COLOR_CBK_GOLD
    g1.line.fill.background()

    g2 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.35), Inches(13.333), Inches(0.15))
    g2.fill.solid()
    g2.fill.fore_color.rgb = COLOR_CBK_GOLD
    g2.line.fill.background()

    # Central Badge & Title
    tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p = tf1.paragraphs[0]
    p.text = "CENTRAL BANK OF KENYA | BANKI KUU YA KENYA"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "DSWAAP PROJECT"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_WHITE
    p.space_after = Pt(10)

    p = tf1.add_paragraph()
    p.text = "Sports Wellness & Attendance Automation Platform"
    p.font.size = Pt(24)
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(20)

    p = tf1.add_paragraph()
    p.text = "Executive Architecture, Dual-Gate QR Verification & Financial Compliance Proposal\n" \
             "Serving 18 Institutional Sporting Disciplines across CBK Sports Complex & Country Club"
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(220, 235, 225)

    # --------------------------------------------------------------------------
    # SLIDE 2: STRATEGIC MANDATE & EXECUTIVE SUMMARY
    # --------------------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    create_slide_header(s2, "Strategic Mandate: Modernizing CBK Sports Wellness", "Executive Overview")

    col_w = Inches(3.6)
    col_h = Inches(5.4)
    top_pos = Inches(1.5)

    # Card 1: The Mandate
    add_card(s2, Inches(0.8), top_pos, col_w, col_h, COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s2.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.2), col_w - Inches(0.4), col_h - Inches(0.4))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🏛️ INSTITUTIONAL MANDATE"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(12)

    bullets1 = [
        "Fosters physical wellness, mental resilience, and inter-departmental synergy across 10 CBK Directorates.",
        "Prepares Bank athletes for Inter-Bank Games and national corporate wellness championships.",
        "Mandates robust governance, zero-trust verification, and institutional fiduciary accountability.",
        "Requires modern mobile-first tooling eliminating paper friction for 500+ active staff athletes."
    ]
    for b in bullets1:
        p = tf.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_CBK_DARK
        p.space_after = Pt(8)

    # Card 2: Core Solution
    add_card(s2, Inches(4.8), top_pos, col_w, col_h, COLOR_CBK_WHITE, COLOR_CBK_GOLD)
    tx = s2.shapes.add_textbox(Inches(5.0), top_pos + Inches(0.2), col_w - Inches(0.4), col_h - Inches(0.4))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚡ THE DSWAAP SOLUTION"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(12)

    bullets2 = [
        "Dual-Gate QR Verification: Pre-Sport Arrival & Post-Sport Departure scanning.",
        "Dynamic HMAC QR rotation every 15-30 mins preventing static pass sharing.",
        "Specialized field deployment across 18 disciplines including 6-station Golf topologies.",
        "Seamless hybrid backend: Real-time Google Sheets API with offline local persistence."
    ]
    for b in bullets2:
        p = tf.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_CBK_DARK
        p.space_after = Pt(8)

    # Card 3: Value Delivered
    add_card(s2, Inches(8.8), top_pos, col_w, col_h, COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s2.shapes.add_textbox(Inches(9.0), top_pos + Inches(0.2), col_w - Inches(0.4), col_h - Inches(0.4))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📈 MEASURABLE OUTCOMES"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(12)

    bullets3 = [
        "100% Elimination of Paper Sign-In Sheets and manual handwriting deciphering.",
        "Instant Allowance Calculation: Automated KES stipend disbursement ledgers.",
        "Sub-Second Audit Verification: Automated timestamps and duration math.",
        "Real-Time Executive Visibility: Secretariat, HR, and Internal Audit live consoles."
    ]
    for b in bullets3:
        p = tf.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_CBK_DARK
        p.space_after = Pt(8)

    # --------------------------------------------------------------------------
    # SLIDE 3: PROBLEM VS SOLUTION COMPARISON
    # --------------------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    create_slide_header(s3, "Transforming Sports Attendance Governance", "Comparative Analysis")

    rows = [
        ("Verification Method", "Physical paper sheets passed around fields", "Dynamic cryptographic QR scanning at arrival & exit"),
        ("Proxy Signing Risk", "Severe: Colleagues sign on behalf of absentees", "Zero: Unique dynamic codes + staff auto-identification"),
        ("Active Duration Proof", "None: No departure timestamps recorded", "Precise: Algorithmically verified 45+ minute session math"),
        ("Stipend Reconciliations", "Slow: 3-4 week lag compiling allowances", "Instantaneous: Pre-calculated KES disbursement ledger"),
        ("Golf & Field Venues", "Impossible: Course spread over 18 holes", "Seamless: Multi-station terminals across tees, greens, & clubhouse"),
        ("Audit Compliance Trail", "Weak: Fragmented files and missing dates", "Irrefutable: Immutable timestamps mirrored in Google Sheets")
    ]

    # Draw Table
    t_left = Inches(0.8)
    t_top = Inches(1.5)
    t_width = Inches(11.733)
    t_height = Inches(5.4)

    table_shape = s3.shapes.add_table(len(rows) + 1, 3, t_left, t_top, t_width, t_height)
    tbl = table_shape.table
    tbl.columns[0].width = Inches(2.8)
    tbl.columns[1].width = Inches(4.4)
    tbl.columns[2].width = Inches(4.533)

    # Headers
    headers = ["Evaluation Metric", "Legacy Manual Practice (Deficient)", "DSWAAP Automation (Target State)"]
    for i, h in enumerate(headers):
        cell = tbl.cell(0, i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_CBK_DARK_GREEN
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = COLOR_CBK_WHITE

    # Rows
    for r_idx, (col0, col1, col2) in enumerate(rows, start=1):
        c0 = tbl.cell(r_idx, 0)
        c0.text = col0
        c0.text_frame.paragraphs[0].font.bold = True
        c0.text_frame.paragraphs[0].font.size = Pt(11)
        c0.text_frame.paragraphs[0].font.color.rgb = COLOR_CBK_DARK

        c1 = tbl.cell(r_idx, 1)
        c1.text = col1
        c1.text_frame.paragraphs[0].font.size = Pt(11)
        c1.text_frame.paragraphs[0].font.color.rgb = RGBColor(180, 40, 40)

        c2 = tbl.cell(r_idx, 2)
        c2.text = col2
        c2.text_frame.paragraphs[0].font.size = Pt(11)
        c2.text_frame.paragraphs[0].font.color.rgb = COLOR_CBK_GREEN

    # --------------------------------------------------------------------------
    # SLIDE 4: DUAL-GATE DYNAMIC QR VERIFICATION WORKFLOW
    # --------------------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    create_slide_header(s4, "Dual-Gate QR Verification Workflow", "Zero-Trust Architecture")

    # Flowchart Blocks
    box_w = Inches(3.6)
    box_h = Inches(4.5)

    # Step 1: Pre-Sport Arrival
    add_card(s4, Inches(0.8), Inches(1.6), box_w, box_h, COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s4.shapes.add_textbox(Inches(1.0), Inches(1.8), box_w - Inches(0.4), box_h - Inches(0.4))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "GATE 1: PRE-SPORT\n(ARRIVAL CHECK-IN)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "1. Participant arrives at sports complex/venue.\n" \
             "2. Captain/Marshal displays active Station Dynamic QR.\n" \
             "3. Participant scans via smartphone or self-checks in.\n" \
             "4. Status set to: PRE_SPORT_VALIDATED.\n" \
             "5. System locks in Arrival Timestamp.\n" \
             "6. Allowance status: AWAITING_POST_GATE."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CBK_DARK
    p.space_after = Pt(8)

    # Step 2: Active Training Session
    add_card(s4, Inches(4.8), Inches(1.6), box_w, box_h, COLOR_CBK_LIGHT, COLOR_CBK_GOLD)
    tx = s4.shapes.add_textbox(Inches(5.0), Inches(1.8), box_w - Inches(0.4), box_h - Inches(0.4))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SESSION EXECUTION\n(ACTIVE TRAINING)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Athlete participates in chosen discipline.\n" \
             "• Training schedules supported:\n" \
             "   - Daily Morning Camps (06:00 - 08:30)\n" \
             "   - Evening Sessions (16:30 - 19:30)\n" \
             "   - Weekend Tournaments & Championships\n" \
             "• Policy Requirement: Minimum 45 minutes active duration required for allowance."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CBK_DARK

    # Step 3: Post-Sport Departure
    add_card(s4, Inches(8.8), Inches(1.6), box_w, box_h, COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s4.shapes.add_textbox(Inches(9.0), Inches(1.8), box_w - Inches(0.4), box_h - Inches(0.4))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "GATE 2: POST-SPORT\n(DUAL RECONCILIATION)"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "1. Participant scans Post-Sport QR upon workout finish.\n" \
             "2. Engine matches Gate 1 & Gate 2 timestamps.\n" \
             "3. Calculates session duration (e.g., 75 mins).\n" \
             "4. Status: DUAL_VERIFIED_QUALIFIED.\n" \
             "5. KES 2,500 stipend auto-allocated.\n" \
             "6. Institutional HTML email receipt dispatched."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CBK_DARK

    # --------------------------------------------------------------------------
    # SLIDE 5: 18 SPORTING DISCIPLINES & GOLF MULTI-STATION
    # --------------------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    create_slide_header(s5, "18 Sporting Disciplines & Multi-Station Topology", "Operational Breadth")

    # Left: 18 Disciplines Breakdown
    add_card(s5, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.5), COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s5.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.4), Inches(5.1))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🏅 COMPLETE 18 SPORTING DISCIPLINES"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(10)

    disciplines_list = [
        "1. Football (Soccer) - Main Pitch & Bench Posts",
        "2. Basketball - Indoor Arena North & Scorer's Table",
        "3. Volleyball - Hard Court Pavilion & Sand Courts",
        "4. Netball - East Court Gate A",
        "5. Athletics & Track - 100m Start & Perimeter Gate",
        "6. Golf - Multi-Station 18-Hole Course Topology",
        "7. Lawn Tennis - Courts 1-4 Umpires Desk",
        "8. Table Tennis - Recreation Hall Zone A Reception",
        "9. Badminton - Indoor Multi-Purpose Hall Bay 2",
        "10. Swimming - Olympic Pool & Aquatics Centre",
        "11. Squash - Complex Glass Courts 1 & 2",
        "12. Darts - Staff Club Lounge Scorers Station",
        "13. Pool / Snooker - Billiards Desk 1",
        "14. Chess - Quiet Strategy Room 3",
        "15. Scrabble - Quiet Strategy Room 4",
        "16. Tug of War - Lower Grounds Arena",
        "17. Cycling - Perimeter Track Depot & Checkpoints",
        "18. Physical Fitness & Gym - Aerobics Studio"
    ]
    p = tf.add_paragraph()
    p.text = "\n".join(disciplines_list)
    p.font.size = Pt(9.5)
    p.font.color.rgb = COLOR_CBK_DARK
    p.line_spacing = 1.15

    # Right: Specialized Golf Multi-Station
    add_card(s5, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.5), COLOR_CBK_WHITE, COLOR_CBK_GOLD)
    tx = s5.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(5.1))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⛳ SPECIALIZED GOLF MULTI-STATION SYSTEM"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(10)

    golf_desc = [
        "Challenge: Golf takes place over 18 holes across 6,000+ yards, making traditional single-gate turnstiles impossible.",
        "DSWAAP Solution: Distributed station QR nodes assigned to Course Captains and Marshals:",
        "• Station 1: Clubhouse Pro-Shop (Pre-Round Arrival)",
        "• Station 2: Tee Box Hole 1 (Front Nine Start Verification)",
        "• Station 3: Halfway House (Hole 9 Green Transition Check)",
        "• Station 4: Tee Box Hole 10 (Back Nine Entry)",
        "• Station 5: 18th Green Marshals Post (Round Completion)",
        "• Station 6: Practice Driving Range (Short Clinic Verification)",
        "Impact: Full audit visibility over 3-4 hour rounds with zero course congestion."
    ]
    for g in golf_desc:
        p = tf.add_paragraph()
        p.text = g
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_CBK_DARK
        p.space_after = Pt(5)

    # --------------------------------------------------------------------------
    # SLIDE 6: REAL-TIME GOOGLE SHEETS & RESILIENT BACKEND
    # --------------------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    create_slide_header(s6, "Real-Time Google Sheets Backend & Offline Resilience", "Data Infrastructure")

    add_card(s6, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s6.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.1), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "📊 ZERO-LATENCY GOOGLE SHEETS SYNCHRONIZATION WITH FIELD RESILIENCE"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(14)

    sheets_points = [
        ("Institutional Data Sovereignty", "Logs directly into the official Central Bank of Kenya Google Workspace spreadsheet ('CBK_DSWAAP_Attendance_Ledger') via gspread v6 and OAuth2 service accounts."),
        ("Instant Real-Time Stream", "Every scan at Gate 1 or Gate 2 triggers an immediate append row event containing 15 comprehensive audit fields."),
        ("Offline Field Resilience (Zero Data Loss)", "If internet connectivity fluctuates at remote golf holes or track perimeters, DSWAAP immediately falls back to high-speed local SQLite persistence and CSV ledger mirroring. Queued rows sync automatically once reconnected."),
        ("Comprehensive Audit Schema", "Columns: Timestamp | Date | Staff ID | Full Name | CBK Email | Department | Discipline | Gate | Station | Session ID | Validation Status | Duration (Mins) | Allowance Qualified | Allowance (KES) | Audit Notes.")
    ]

    for title, desc in sheets_points:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_CBK_DARK

        p2 = tf.add_paragraph()
        p2.text = f"  {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = RGBColor(70, 80, 90)
        p2.space_after = Pt(8)

    # --------------------------------------------------------------------------
    # SLIDE 7: SECRETARIAT OPERATIONAL DASHBOARD
    # --------------------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    create_slide_header(s7, "Secretariat Operational Command Center", "Live Operations UI")

    # 4 Mock KPI Cards
    kpis_data = [
        ("Today's Total Scans", "148 Scans", "Across All 18 Disciplines", COLOR_CBK_GREEN),
        ("Active on Field", "42 Athletes", "Gate 1 Pre-Sport Active", COLOR_CBK_ACCENT_BLUE),
        ("Dual-Verified", "96 Completed", "Both Gates Validated", COLOR_CBK_DARK_GREEN),
        ("Policy Compliance", "97.9%", "Sessions >= 45 Minutes", COLOR_CBK_GOLD)
    ]

    card_w = Inches(2.7)
    card_h = Inches(1.3)
    for idx, (title, val, sub, col) in enumerate(kpis_data):
        c_left = Inches(0.8) + (idx * Inches(2.95))
        add_card(s7, c_left, Inches(1.5), card_w, card_h, COLOR_CBK_WHITE, col)
        tx = s7.shapes.add_textbox(c_left + Inches(0.1), Inches(1.6), card_w - Inches(0.2), card_h - Inches(0.2))
        tf = tx.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title.upper()
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_CBK_GREY

        p = tf.add_paragraph()
        p.text = val
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = col

        p = tf.add_paragraph()
        p.text = sub
        p.font.size = Pt(8.5)
        p.font.color.rgb = COLOR_CBK_DARK

    # Bottom Content: Discipline Status & Live Stream Mockup
    add_card(s7, Inches(0.8), Inches(3.1), Inches(11.733), Inches(3.8), COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s7.shapes.add_textbox(Inches(1.0), Inches(3.2), Inches(11.3), Inches(3.5))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "⚡ REAL-TIME DISCIPLINE STATUS & ACTIVITY STREAM CAPABILITIES"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Live Turnout Matrix: Instant health cards for every discipline showing active participant counts, completed dual gates, and assigned Captain contact extensions.\n" \
             "• Real-Time Activity Ticker: Chronological stream capturing incoming arrival and departure scans with sub-second timestamps.\n" \
             "• Dynamic Filtering: Secretariat can isolate specific sports, gates, or departments during inter-bank championships.\n" \
             "• Field Captain Directory: Direct extension links to all 18 discipline captains for rapid on-site logistics coordination."
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_CBK_DARK
    p.line_spacing = 1.3

    # --------------------------------------------------------------------------
    # SLIDE 8: HR WELLNESS ANALYTICS COMMAND CENTER
    # --------------------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    create_slide_header(s8, "HR Analytics & Wellness Engagement Command", "Executive Human Resources")

    add_card(s8, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s8.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.4), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "📊 DEPARTMENTAL ENGAGEMENT BENCHMARKING"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "Tracks participation quotas across all 10 CBK Directorates:\n" \
             "• Finance & Accounts\n" \
             "• IT & Digital Services\n" \
             "• Internal Audit Directorate\n" \
             "• Human Resources\n" \
             "• Banking & Payment Services\n" \
             "• Monetary Policy & Economic Research\n" \
             "• Currency Operations & Logistics\n" \
             "• Governor's Executive Office\n" \
             "• Legal Services & Board Secretariat\n" \
             "• Financial Markets & Reserves\n\n" \
             "Enables HR Wellness committees to identify under-represented directorates and execute targeted health interventions."
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_CBK_DARK

    add_card(s8, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_GOLD)
    tx = s8.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🌟 WELLNESS TRENDS & CHAMPION LEADERBOARD"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Sport Category Distribution: Donut charts illustrating staff preference across Field Sports, Racket, Mind Sports, and Aquatics.\n\n" \
             "• Time-of-Day Engagement Curves: Identifies peak fitness utilization between early morning camps (06:00) vs evening camps (17:00).\n\n" \
             "• Wellness Champions Leaderboard: Recognizes individual staff athletes maintaining the highest continuous dual-verified attendance streaks.\n\n" \
             "• Culture & Morale: Cultivates healthy institutional camaraderie and inter-departmental trust."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CBK_DARK

    # --------------------------------------------------------------------------
    # SLIDE 9: FINANCE & INTERNAL AUDIT COMPLIANCE PORTAL
    # --------------------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    create_slide_header(s9, "Finance & Internal Audit Compliance Portal", "Fiduciary Governance")

    add_card(s9, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s9.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.1), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "💰 AUTOMATED SPORTS ALLOWANCE / STIPEND DISBURSEMENT RECONCILIATION"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(12)

    fin_points = [
        ("Automated Dual-Gate Timestamp Matrix", "Internal Audit can cross-examine exact arrival and departure timestamps down to the second, with calculated active training duration."),
        ("Zero Stipend for Non-Compliant Sessions", "If an employee's recorded workout is less than the mandatory 45-minute policy floor, the system automatically tags the entry as 'INSUFFICIENT_DURATION' and zeroes out the allowance (KES 0)."),
        ("Single-Gate Unpaired Exception Trapping", "If a participant signs Gate 1 but never scans Gate 2 (or vice versa), the system flags the transaction as 'DISQUALIFIED_NO_PRE_GATE', preventing fraudulent payment."),
        ("One-Click Batch Approval for Accounts Payable", "Finance officers can review the consolidated ledger, click 'Batch Approve for Accounts Payable', and export directly to signed Excel (.xlsx) workbooks and CSV files ready for ERP payroll disbursement.")
    ]

    for title, desc in fin_points:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_CBK_DARK

        p2 = tf.add_paragraph()
        p2.text = f"  {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = RGBColor(70, 80, 90)
        p2.space_after = Pt(6)

    # --------------------------------------------------------------------------
    # SLIDE 10: INSTITUTIONAL EMAIL NOTIFICATIONS & DIGITAL CERTIFICATES
    # --------------------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    create_slide_header(s10, "Institutional Email Dispatch & Dual-Verification Receipts", "Automated Comms")

    add_card(s10, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s10.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.4), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "✉️ AUTOMATED INSTITUTIONAL DISPATCH"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Event-Driven Trigger: Automatically generated immediately when Gate 2 (Departure) is scanned and matched with Gate 1.\n\n" \
             "• Direct Institutional Delivery: Delivered to verified '@centralbank.go.ke' inboxes via institutional SMTP relay.\n\n" \
             "• Transparent Record: Provides participants with instant confirmation of their recorded duration, discipline station, and stipend eligibility.\n\n" \
             "• Audit Transparency: Eliminates disputes regarding attendance records or allowance payouts."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CBK_DARK
    p.line_spacing = 1.2

    add_card(s10, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_GOLD)
    tx = s10.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.2), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "🎫 BRANDED CERTIFICATE SPECIFICATIONS"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "Rendered with official CBK Corporate Guidelines:\n" \
             "• Official Bank Colors: Deep Kenya Green (#006633) and Gold (#D4AF37).\n" \
             "• Header: Central Bank of Kenya | Sports Wellness & Attendance Platform.\n" \
             "• Verification Stamp: Dual-Gate Cryptographic Seal.\n" \
             "• Data Summary Table: Staff ID, Name, Discipline, Station, Active Duration.\n" \
             "• Stipend Badge: KES 2,500.00 Approved for Allowance Ledger.\n" \
             "• Official Policy Circular Reference: CBK/HR/WEL/2026."
    p.font.size = Pt(10.5)
    p.font.color.rgb = COLOR_CBK_DARK
    p.line_spacing = 1.2

    # --------------------------------------------------------------------------
    # SLIDE 11: SECURITY, HMAC ANTI-SPOOFING & FRAUD MITIGATION
    # --------------------------------------------------------------------------
    s11 = prs.slides.add_slide(blank_layout)
    create_slide_header(s11, "Security Architecture & Fraud Mitigation Protocol", "Cybersecurity & Audit")

    add_card(s11, Inches(0.8), Inches(1.5), Inches(11.733), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s11.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(11.1), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🔒 MULTI-LAYERED DEFENSE AGAINST ATTENDANCE FRAUD"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(12)

    sec_layers = [
        ("Cryptographic HMAC-SHA256 Signatures", "Dynamic QR payloads include a truncated cryptographic hash generated with a secure salt. Any manual modification to the gate, discipline, or expiry string invalidates the code."),
        ("Time-Bounded Dynamic Rotation", "Captains' terminals refresh QR codes every 15-30 minutes. If a participant takes a smartphone picture and forwards it to a colleague, the code expires before it can be reused."),
        ("Strict Institution Email Whitelisting", "Only authenticated staff with official '@centralbank.go.ke' domain identities are permitted to register and claim sports welfare allowances."),
        ("Impossible Velocity & Re-Check Detection", "The system detects and flags anomalies, such as impossible speeds between disparate venues (e.g. Golf course to Swimming pool within 5 minutes) or multiple simultaneous gate check-ins.")
    ]

    for title, desc in sec_layers:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_CBK_DARK

        p2 = tf.add_paragraph()
        p2.text = f"  {desc}"
        p2.font.size = Pt(11)
        p2.font.color.rgb = RGBColor(70, 80, 90)
        p2.space_after = Pt(6)

    # --------------------------------------------------------------------------
    # SLIDE 12: IMPLEMENTATION ROADMAP & EXECUTIVE CALL TO ACTION
    # --------------------------------------------------------------------------
    s12 = prs.slides.add_slide(blank_layout)
    create_slide_header(s12, "Deployment Roadmap & Executive Recommendations", "Next Steps")

    col_w = Inches(3.6)
    col_h = Inches(5.4)

    # Phase 1
    add_card(s12, Inches(0.8), Inches(1.5), col_w, col_h, COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s12.shapes.add_textbox(Inches(1.0), Inches(1.7), col_w - Inches(0.4), col_h - Inches(0.4))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PHASE 1 (WEEKS 1-2)\nPILOT PROGRAM"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Deploy pilot in 3 representative disciplines: Football, Athletics, and Golf.\n\n" \
             "• Station 50 pilot participants across morning and evening camps.\n\n" \
             "• Validate Google Sheets sync and test mobile responsiveness across iOS and Android devices.\n\n" \
             "• Refine station QR placement at Golf course tees and greens."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CBK_DARK

    # Phase 2
    add_card(s12, Inches(4.8), Inches(1.5), col_w, col_h, COLOR_CBK_WHITE, COLOR_CBK_GOLD)
    tx = s12.shapes.add_textbox(Inches(5.0), Inches(1.7), col_w - Inches(0.4), col_h - Inches(0.4))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PHASE 2 (WEEKS 3-4)\nFULL 18-SPORT ROLLOUT"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Onboard all 18 Discipline Captains and provide station tablet displays.\n\n" \
             "• Roll out institutional communications across all 10 CBK Directorates.\n\n" \
             "• Activate real-time Secretariat and HR Analytics dashboards.\n\n" \
             "• Establish Secretariat helpdesk support."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CBK_DARK

    # Phase 3
    add_card(s12, Inches(8.8), Inches(1.5), col_w, col_h, COLOR_CBK_WHITE, COLOR_CBK_GREEN)
    tx = s12.shapes.add_textbox(Inches(9.0), Inches(1.7), col_w - Inches(0.4), col_h - Inches(0.4))
    tf = tx.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PHASE 3 (WEEKS 5-6)\nFINANCE AUTOMATION"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GREEN
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Link automated disbursement ledgers to CBK ERP/payroll for monthly sports allowance credits.\n\n" \
             "• Hand over audit compliance reports to Internal Audit Directorate.\n\n" \
             "• Establish quarterly wellness awards using DSWAAP analytics.\n\n" \
             "• Executive Sign-Off & Continuous Improvement."
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_CBK_DARK

    # Save presentation
    prs.save(PPTX_PATH)
    print(f"PowerPoint presentation generated at: {PPTX_PATH}")


if __name__ == "__main__":
    generate_markdown_proposal()
    generate_presentation_deck()
    print("DSWAAP presentation and proposal artifacts compiled successfully!")

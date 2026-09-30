"""
DSWAAP - Central Bank of Kenya (CBK) Sports Wellness & Attendance Automation Platform
HR, Finance & Secretariat Executive Presentation Generator (Updated with all latest improvements)
Strictly adheres to official CBK Corporate Branding:
- CBK Royal Blue: #025BBF (Primary Brand Color from centralbank.go.ke)
- CBK Deep Navy:  #10529E (Secondary Brand Color from centralbank.go.ke)
- CBK Saffron Gold: #F8B82D (Official Brand Color from CBK Logo)
- CBK Amber Gold Accent: #F7941D (Website Hero Accent)
- CBK Ice Blue Tint: #EEF6FC (Card Backgrounds)
- Official CBK Coat of Arms Crest Logo embedded on EVERY slide.

Features all recent innovations:
1. 18 Sporting Disciplines (Football, Golf, Athletics, Swimming, Basketball, Tennis, etc.)
2. Financial Privacy Lockdown (Field kiosks stripped of money; Certified Attendance Units; Finance valuation controller)
3. Data Sovereignty & KDPA 2019 (Safaricom Corporate APN, On-Premises Haile Selassie Ave DC & KSMS, internal DNS)
4. 1-Click Cryptographic Magic Link Identity Confirmation (Golfer S. N. Gathigi - CBK-1008)
5. 60-Second Real-Time Google Sheets Master Sync & 5-Second CSV Import

Compiles into:
1. DSWAAP_HR_Finance_GameChanger.pptx
2. DSWAAP_Executive_Presentation.pptx
3. DSWAAP_CBK_Official_Deck.pptx
4. DSWAAP_Secretariat_HR_Finance_Athletics.pptx
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(OUTPUT_DIR, "cbk_logo.png")

# CBK Corporate Color Palette
COLOR_CBK_PRIMARY = RGBColor(2, 91, 191)       # #025BBF Signature Royal Blue
COLOR_CBK_NAVY = RGBColor(16, 82, 158)         # #10529E Deep Navy Blue
COLOR_CBK_GOLD = RGBColor(248, 184, 45)        # #F8B82D Official CBK Saffron Gold
COLOR_CBK_GOLD_AMBER = RGBColor(247, 148, 29)  # #F7941D Website Amber Gold Accent
COLOR_CBK_ICE_BLUE = RGBColor(238, 246, 252)   # #EEF6FC Ice Blue Tint
COLOR_CBK_DARK = RGBColor(15, 23, 42)          # #0F172A Slate Dark
COLOR_CBK_LIGHT = RGBColor(248, 250, 252)      # #F8FAFC Clean Background
COLOR_CBK_WHITE = RGBColor(255, 255, 255)
COLOR_CBK_GREY = RGBColor(100, 116, 139)       # #64748B Slate Grey
COLOR_CBK_RED = RGBColor(220, 38, 38)
COLOR_CBK_SUCCESS = RGBColor(5, 150, 105)

SNIPPET_MOBILE = os.path.join(OUTPUT_DIR, "ui_snippet_mobile_checkin.png")
SNIPPET_CAPTAIN = os.path.join(OUTPUT_DIR, "ui_snippet_captain_terminal.png")
SNIPPET_SECRETARIAT = os.path.join(OUTPUT_DIR, "ui_snippet_secretariat_dashboard.png")
SNIPPET_HR = os.path.join(OUTPUT_DIR, "ui_snippet_hr_command_center.png")
SNIPPET_FINANCE = os.path.join(OUTPUT_DIR, "ui_snippet_finance_compliance.png")
SNIPPET_EMAIL = os.path.join(OUTPUT_DIR, "ui_snippet_email_receipt.png")


def create_header(slide, title_text, category_text="CENTRAL BANK OF KENYA | DSWAAP"):
    """Adds a standard executive CBK banner with official logo to the slide."""
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = COLOR_CBK_PRIMARY
    top_bar.line.fill.background()

    gold_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.08))
    gold_line.fill.solid()
    gold_line.fill.fore_color.rgb = COLOR_CBK_GOLD
    gold_line.line.fill.background()

    if os.path.exists(LOGO_PATH):
        logo_bg = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(0.12), Inches(1.1), Inches(0.9))
        logo_bg.fill.solid()
        logo_bg.fill.fore_color.rgb = COLOR_CBK_WHITE
        logo_bg.line.color.rgb = COLOR_CBK_GOLD
        logo_bg.line.width = Pt(1.5)
        slide.shapes.add_picture(LOGO_PATH, Inches(0.65), Inches(0.15), width=Inches(1.0))
        tx_left = Inches(1.9)
        tx_width = Inches(10.6)
    else:
        tx_left = Inches(0.8)
        tx_width = Inches(11.7)

    tx = slide.shapes.add_textbox(tx_left, Inches(0.12), tx_width, Inches(0.9))
    tf = tx.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CBK_GOLD

    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_CBK_WHITE


def add_card(slide, left, top, width, height, bg_color=COLOR_CBK_WHITE, border_color=COLOR_CBK_GOLD):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        card.line.fill.background()
    return card


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ==========================================================================
    # SLIDE 1: COVER SLIDE
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_CBK_NAVY
    bg.line.fill.background()

    g1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    g1.fill.solid()
    g1.fill.fore_color.rgb = COLOR_CBK_GOLD
    g1.line.fill.background()

    g2 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.35), Inches(13.333), Inches(0.15))
    g2.fill.solid()
    g2.fill.fore_color.rgb = COLOR_CBK_GOLD
    g2.line.fill.background()

    if os.path.exists(LOGO_PATH):
        logo_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.8), Inches(1.9), Inches(1.5))
        logo_card.fill.solid()
        logo_card.fill.fore_color.rgb = COLOR_CBK_WHITE
        logo_card.line.color.rgb = COLOR_CBK_GOLD
        logo_card.line.width = Pt(2)
        s1.shapes.add_picture(LOGO_PATH, Inches(1.1), Inches(0.9), width=Inches(1.7))

    tx = s1.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(11.333), Inches(4.7))
    tf = tx.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "CENTRAL BANK OF KENYA | BANKI KUU YA KENYA"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "CBK STRIDE™"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_WHITE
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = "Sports Telemetry, Roster Integrity & Digital Enrollment Platform"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(14)

    p = tf.add_paragraph()
    p.text = "• 18 Standard Sporting Disciplines • Data Sovereignty (KDPA 2019) • Financial Privacy by Design • Real-Time Cloud Master"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CBK_ICE_BLUE

    # ==========================================================================
    # SLIDE 2: WHY THIS IS AN INSTITUTIONAL GAME CHANGER
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    create_header(s2, "Strategic Value Proposition: The 4 Institutional Pillars", "Executive Perspective")

    cols = [
        ("👥 HUMAN RESOURCES", COLOR_CBK_PRIMARY, [
            "Data-Driven Wellness: Live engagement tracking across 400 staff in all 10 Directorates.",
            "All 18 CBK Disciplines: Full squad rosters for Football, Golf, Athletics, Swimming, Tennis, etc.",
            "Culture & Morale Catalyst: Fosters cross-departmental camaraderie and healthy resilience.",
            "ESG Governance: Produces verified, defensible wellness metrics for CBK Annual Reports."
        ]),
        ("💰 FINANCE & AUDIT", COLOR_CBK_GOLD, [
            "Financial Privacy by Design: Field devices are strictly stripped of monetary data.",
            "Certified Attendance Units: Certifies 1 Unit (Compliant) vs 0 Units (Flagged) for payroll.",
            "Exclusive Valuation Authority: Finance holds sole discretion to apply per-diem rates.",
            "Zero Fiduciary Leakage: Automatically blocks early exits (<45m) and proxy scans."
        ]),
        ("🛡️ DATA SOVEREIGNTY", COLOR_CBK_NAVY, [
            "100% Kenyan Residency: Hosted on-premise at Haile Selassie Ave Data Center & KSMS.",
            "Telecom Private APN: Captain tablets run on Safaricom Corporate APN (no public internet).",
            "Internal DNS: Resolves strictly to dswaap.centralbank.go.ke within CBK network.",
            "KDPA 2019 Compliant: Enforces Section 48 & 50 cross-border data transfer restrictions."
        ])
    ]

    for idx, (title, color, bullets) in enumerate(cols):
        left_pos = Inches(0.8) + (idx * Inches(4.0))
        add_card(s2, left_pos, Inches(1.5), Inches(3.75), Inches(5.4), COLOR_CBK_WHITE, color)
        tx = s2.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.7), Inches(3.35), Inches(5.0))
        tf = tx.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(12)

        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_CBK_DARK
            p.space_after = Pt(8)

    # ==========================================================================
    # SLIDE 3: UI SNIPPET 1 - PARTICIPANT MOBILE CHECK-IN (18 SPORTS & GOLF DEMO)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    create_header(s3, "Participant Mobile Check-In: 18 Sports & 1-Click Verification", "Mobile Experience")

    add_card(s3, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_PRIMARY)
    tx = s3.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(5.4), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "📱 18-SPORT SQUAD ROSTERS & 1-CLICK AUTH"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_PRIMARY
    p.space_after = Pt(12)

    features = [
        ("Master 18-Game Selector", "Athletes toggle between all 18 CBK sports (Football, Golf, Athletics, Swimming, Basketball, Tennis, Chess, etc.) with live enrolled player counts."),
        ("'Who the Players Are' Squad Explorer", "Quick-tap athlete pills and live squad dropdowns showing real-time status (Dual-Verified, On Field, or Ready)."),
        ("1-Click Magic Link Confirmation", "Featured Golfer Demo: S. N. Gathigi (CBK-1008) receives a secure magic link, clicking once to confirm identity and activate boarding pass."),
        ("Dynamic QR Viewfinder", "Embedded QR sensor validates time-bounded station codes, verifying physical presence on the field or clubhouse."),
        ("Financial Privacy on Mobile", "Athlete profile card strictly shows 'Accredited Athlete' and 'Min 45 Mins Threshold'—zero monetary amounts exposed.")
    ]

    for title, desc in features:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_CBK_DARK

        p2 = tf.add_paragraph()
        p2.text = f"  {desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_CBK_GREY
        p2.space_after = Pt(5)

    if os.path.exists(SNIPPET_MOBILE):
        s3.shapes.add_picture(SNIPPET_MOBILE, Inches(7.3), Inches(1.4), width=Inches(3.4))

    # ==========================================================================
    # SLIDE 4: UI SNIPPET 2 - FIELD CAPTAIN TERMINAL & PRIVATE APN
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    create_header(s4, "Field Captain Terminal: Safaricom Corporate APN & Hotspot", "Field Topology")

    if os.path.exists(SNIPPET_CAPTAIN):
        s4.shapes.add_picture(SNIPPET_CAPTAIN, Inches(0.8), Inches(1.5), width=Inches(5.7))

    add_card(s4, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_GOLD)
    tx = s4.shapes.add_textbox(Inches(7.0), Inches(1.7), Inches(5.3), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🏷️ ZERO-DATA CORPORATE FIELD TOPOLOGY"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(12)

    ath_pts = [
        ("Safaricom CBK Corporate Private APN", "Captain tablets are equipped with corporate SIMs on a private APN. Cellular traffic routes directly into CBK's internal firewall with zero public internet transit."),
        ("Zero-Data Athlete Hotspot Gateway", "The Captain tablet broadcasts 'CBK-SPORTS-SECURE'. Athletes connect and scan with ZERO personal data bundles or airtime required."),
        ("Dynamic Rotating QR (60s TTL)", "Codes refresh every 60 seconds with HMAC-SHA256 signatures, preventing WhatsApp screenshot sharing and proxy claims."),
        ("Offline-First Resilient Buffer", "If cellular signal dips at Kasarani or tournament venues, scans buffer safely in local SQLite and auto-flush upon reconnection."),
        ("1-Tap Gate 1 (IN) vs Gate 2 (OUT)", "Captains toggle with one touch between arrival clock-in and departure certification.")
    ]

    for title, desc in ath_pts:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_CBK_DARK

        p2 = tf.add_paragraph()
        p2.text = f"  {desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_CBK_GREY
        p2.space_after = Pt(5)

    # ==========================================================================
    # SLIDE 5: UI SNIPPET 3 - SECRETARIAT OPERATIONAL DASHBOARD
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    create_header(s5, "Secretariat Operational Command: All 18 Disciplines", "Real-Time Matrix")

    add_card(s5, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_PRIMARY)
    tx = s5.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "🏛️ 360° SPORTS SECRETARIAT COMMAND"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_PRIMARY
    p.space_after = Pt(12)

    sec_features = [
        ("Live 18-Sport Turnout Matrix", "Real-time attendance numbers across Football, Golf, Athletics, Swimming, Basketball, Tennis, Chess, Aerobics, and more."),
        ("Sub-Second Scans Activity Ticker", "Instant event logging of athlete entries across all stadium gates and golf clubhouse tee boxes."),
        ("Appointed Captains Roster", "Direct directory link to all 18 appointed Discipline Captains with venue stations and extension contacts (e.g. Capt. Eric Mwangi - Golf)."),
        ("Inter-Bank Tournament Command", "Centralized operations hub ready for Kenya Bankers Association (KBA) inter-bank games coordination and camp audits.")
    ]

    for title, desc in sec_features:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_CBK_DARK

        p2 = tf.add_paragraph()
        p2.text = f"  {desc}"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_CBK_GREY
        p2.space_after = Pt(6)

    if os.path.exists(SNIPPET_SECRETARIAT):
        s5.shapes.add_picture(SNIPPET_SECRETARIAT, Inches(6.6), Inches(1.5), width=Inches(5.9))

    # ==========================================================================
    # SLIDE 6: UI SNIPPET 4 - HR COMMAND CENTER (400 STAFF COHORT)
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    create_header(s6, "HR Analytics Command: Directorate Engagement & Cohorts", "HR Governance")

    if os.path.exists(SNIPPET_HR):
        s6.shapes.add_picture(SNIPPET_HR, Inches(0.8), Inches(1.5), width=Inches(5.9))

    add_card(s6, Inches(7.0), Inches(1.5), Inches(5.5), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_PRIMARY)
    tx = s6.shapes.add_textbox(Inches(7.2), Inches(1.7), Inches(5.1), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "👥 STRATEGIC WELLNESS ANALYTICS"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_PRIMARY
    p.space_after = Pt(12)

    hr_features = [
        ("400 Pre-Enrolled Staff Profiles", "Synthetic testing cohort accurately distributed across all 10 Central Bank Directorates and 18 disciplines."),
        ("Directorate Progress Quotas", "Visual target tracking across divisions (e.g. IT, Currency Operations, Monetary Policy, Banking & Payment Services)."),
        ("Wellness Cohort Distribution", "Evaluates employee engagement across Early Morning (06:00-08:30), Lunchtime, and Evening training sessions."),
        ("Institutional ESG Reporting", "Generates verified, tamper-proof physical activity metrics for the Central Bank Annual Sustainability & HR Report.")
    ]

    for title, desc in hr_features:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11.5)
        p.font.color.rgb = COLOR_CBK_DARK

        p2 = tf.add_paragraph()
        p2.text = f"  {desc}"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = COLOR_CBK_GREY
        p2.space_after = Pt(6)

    # ==========================================================================
    # SLIDE 7: UI SNIPPET 5 - FINANCE PORTAL (FINANCIAL PRIVACY BY DESIGN)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    create_header(s7, "Finance & Audit Verification Portal: Financial Privacy by Design", "Fiduciary Governance")

    add_card(s7, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4), COLOR_CBK_WHITE, COLOR_CBK_GOLD)
    tx = s7.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(5.2), Inches(5.0))
    tf = tx.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "💰 SEGREGATION OF DUTIES & PRIVACY"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(12)

    fin_features = [
        ("Privacy-by-Design Lockdown", "Field devices and participant screens are strictly stripped of monetary values. Athletes and captains only see certified attendance accreditation."),
        ("Certified Attendance Units", "Ledger certifies compliant sessions as '1 Unit (Certified)' vs '0 Units (Flagged)' based on the 45-minute policy floor."),
        ("Confidential Valuation Controller", "Finance holds sole authority: an interactive controller allows Finance to assign discretionary per-diem rates for payroll batch runs."),
        ("Fraud & Leakage Trapping", "In our 720-log live cohort: 310 sessions verified compliant, while 35 premature exits (<45m) were automatically blocked from payment."),
        ("1-Click Accounts Payable Export", "Finance officers approve the verified batch and export certified payroll ledgers in CSV and Excel with 1 click.")
    ]

    for title, desc in fin_features:
        p = tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_CBK_DARK

        p2 = tf.add_paragraph()
        p2.text = f"  {desc}"
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_CBK_GREY
        p2.space_after = Pt(5)

    if os.path.exists(SNIPPET_FINANCE):
        s7.shapes.add_picture(SNIPPET_FINANCE, Inches(6.6), Inches(1.5), width=Inches(5.9))

    # ==========================================================================
    # SLIDE 8: DATA SOVEREIGNTY & CYBERSECURITY ARCHITECTURE
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    create_header(s8, "Data Sovereignty & Cybersecurity: Keeping Data CBK-ONLY", "Sovereign Security")

    sovereignty_cards = [
        ("1. PHYSICAL SOVEREIGNTY & RESIDENCY", COLOR_CBK_PRIMARY, [
            "KDPA 2019 Section 48/50: 100% Kenyan data localization compliance.",
            "Primary Data Center: CBK Head Office (Haile Selassie Avenue, Nairobi).",
            "Secondary DR Site: Kenya School of Monetary Studies (KSMS / Eldoret).",
            "AES-256 Encryption at Rest: Transparent Data Encryption (TDE) on all SAN storage."
        ]),
        ("2. NETWORK PERIMETER RING-FENCE", COLOR_CBK_GOLD, [
            "Telecom Private APN: Captain SIMs on cbk.safaricom.co.ke private circuit.",
            "Zero Public Internet Transit: Cellular data routes via direct MPLS into CBK firewall.",
            "Split-Horizon DNS: dswaap.centralbank.go.ke resolves solely within CBK intranet.",
            "Outside queries receive NXDOMAIN—invisible to the external public internet."
        ]),
        ("3. ZERO-TRUST IDENTITY & ACCESS", COLOR_CBK_NAVY, [
            "Active Directory / Entra ID SSO: Strict authentication via @centralbank.go.ke.",
            "Role-Based Access Control: Segregates Athletes, Captains, HR, and Finance.",
            "Anti-Tamper Audit Chaining: HMAC-SHA256 cryptographic chain prevents retroactive edits.",
            "60-Second Ephemeral QR: Tokens expire in 60s, blocking screenshot sharing."
        ])
    ]

    for idx, (title, color, bullets) in enumerate(sovereignty_cards):
        left_pos = Inches(0.8) + (idx * Inches(4.0))
        add_card(s8, left_pos, Inches(1.5), Inches(3.75), Inches(5.4), COLOR_CBK_WHITE, color)
        tx = s8.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.7), Inches(3.35), Inches(5.0))
        tf = tx.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(12)

        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_CBK_DARK
            p.space_after = Pt(8)

    # ==========================================================================
    # SLIDE 9: REAL-TIME CLOUD MASTER (GOOGLE SHEETS INTEGRATION)
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    create_header(s9, "Cloud Master Synchronization: Real-Time Google Sheets", "Cloud Integration")

    cloud_cards = [
        ("⚡ 60-SEC LIVE WEBHOOK STREAMING", COLOR_CBK_PRIMARY, [
            "Zero-Cloud Setup: Deploys via a 20-line Google Apps Script Web App.",
            "Sub-Second Batch Insertion: Appends all 720 records in <1 second via setValues API.",
            "Real-Time Phone Streaming: Every captain scan at Gate 1 or 2 auto-appends to the cloud sheet.",
            "Automated CBK Royal Blue Header: Generates frozen branded header automatically."
        ]),
        ("📁 5-SECOND DIRECT CSV IMPORT", COLOR_CBK_GOLD, [
            "1-Click Download: Instant download of full 720-record audit ledger from Tab 6.",
            "Instant Drop to sheets.new: Drag CSV into Google Sheets in 3 clicks.",
            "Offline Portability: Works seamlessly even in air-gapped environments without APIs.",
            "Complete Audit Telemetry: Timestamps, staff IDs, disciplines, and compliance flags."
        ]),
        ("🔒 TENANT-RESTRICTED GOOGLE DLP", COLOR_CBK_NAVY, [
            "Restricted to Central Bank of Kenya: External domain sharing strictly disabled.",
            "Data Loss Prevention (DLP): Disables downloading/exporting to personal Google drives.",
            "Context-Aware Access: IP allowlist restricted to CBK enterprise egress ranges.",
            "Full Audit Logging: Google Workspace admin logs track all spreadsheet viewers."
        ])
    ]

    for idx, (title, color, bullets) in enumerate(cloud_cards):
        left_pos = Inches(0.8) + (idx * Inches(4.0))
        add_card(s9, left_pos, Inches(1.5), Inches(3.75), Inches(5.4), COLOR_CBK_WHITE, color)
        tx = s9.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.7), Inches(3.35), Inches(5.0))
        tf = tx.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(12)

        for b in bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(10.5)
            p.font.color.rgb = COLOR_CBK_DARK
            p.space_after = Pt(8)

    # ==========================================================================
    # SLIDE 10: COMPARISON TABLE (MANUAL VS DSWAAP)
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    create_header(s10, "Manual Paper Logs vs. DSWAAP Automation", "Operational Contrast")

    rows = [
        ("Parameter", "Legacy Manual Attendance", "DSWAAP Automated Platform", True),
        ("Verification Method", "Paper sign-in sheets at field entrance", "Dual-gate dynamic QR scanning (Gate 1 & 2)", False),
        ("Staff Data Cost", "N/A (Paper sign-in register)", "Zero Cost: Captain Hotspots Athletes (No bundles needed)", False),
        ("Proxy Check-in Risk", "High (Colleagues sign on behalf of absentees)", "Zero (Dynamic rotating QR with 60s TTL + HMAC tokens)", False),
        ("Duration Verification", "Unenforced (Self-reported hours)", "Automated duration math against 45-min policy floor", False),
        ("Financial Privacy", "Amounts openly discussed / written on sheets", "Field devices 100% stripped of money; Finance exclusive", False),
        ("Data Sovereignty", "Loose paper files susceptible to loss", "100% On-Premises CBK Data Center + Private APN", False),
        ("Reconciliation Speed", "4-6 weeks manual audit and signature delays", "Real-time Google Sheets stream + 1-click AP batch export", False)
    ]

    y_pos = Inches(1.5)
    for r_idx, (p1, p2, p3, is_hdr) in enumerate(rows):
        bg_col = COLOR_CBK_PRIMARY if is_hdr else (COLOR_CBK_ICE_BLUE if r_idx % 2 == 1 else COLOR_CBK_WHITE)
        bd_col = COLOR_CBK_GOLD if is_hdr else COLOR_CBK_GOLD

        add_card(s10, Inches(0.8), y_pos, Inches(11.733), Inches(0.62), bg_col, bd_col)

        tx = s10.shapes.add_textbox(Inches(1.0), y_pos + Inches(0.06), Inches(3.2), Inches(0.5))
        p = tx.text_frame.paragraphs[0]
        p.text = p1
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_CBK_WHITE if is_hdr else COLOR_CBK_DARK

        tx = s10.shapes.add_textbox(Inches(4.4), y_pos + Inches(0.06), Inches(3.8), Inches(0.5))
        p = tx.text_frame.paragraphs[0]
        p.text = p2
        p.font.size = Pt(10)
        p.font.bold = is_hdr
        p.font.color.rgb = COLOR_CBK_GOLD if is_hdr else COLOR_CBK_RED if not is_hdr else COLOR_CBK_DARK

        tx = s10.shapes.add_textbox(Inches(8.4), y_pos + Inches(0.06), Inches(3.9), Inches(0.5))
        p = tx.text_frame.paragraphs[0]
        p.text = p3
        p.font.size = Pt(10)
        p.font.bold = is_hdr
        p.font.color.rgb = COLOR_CBK_WHITE if is_hdr else COLOR_CBK_PRIMARY

        y_pos += Inches(0.68)

    # ==========================================================================
    # SLIDE 11: IMPLEMENTATION ROADMAP & BOARD DECISION
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    create_header(s11, "Implementation Roadmap & Board Decision", "Path to Production")

    phases = [
        ("PHASE 1: PILOT ACCREDITATION", COLOR_CBK_PRIMARY, [
            "Joint HR, Finance & Internal Audit Committee sign-off.",
            "Equip 3 Discipline Captains (Golf, Football, Athletics) with tablets.",
            "Validate Safaricom Corporate Private APN connectivity.",
            "Run 50-staff pilot cohort with 1-click magic link authentication."
        ]),
        ("PHASE 2: 18-SPORT EXPANSION", COLOR_CBK_GOLD, [
            "Provision tablets for all 18 Discipline Captains with field hotspots.",
            "Issue Bank-wide circular introducing DSWAAP Mobile Portal.",
            "Activate Secretariat 360° Operations Command console.",
            "Deploy stations at CBK Sports Club, Kasarani, and tournament venues."
        ]),
        ("PHASE 3: ENTERPRISE GO-LIVE", COLOR_CBK_NAVY, [
            "Bind to on-premises host at dswaap.centralbank.go.ke.",
            "Integrate Microsoft Entra ID Single Sign-On (SSO).",
            "First automated 1-Click Batch Accounts Payable payroll run.",
            "100% decommissioning of manual paper sign-in registers."
        ])
    ]

    for idx, (p_title, p_col, p_bullets) in enumerate(phases):
        p_left = Inches(0.8) + (idx * Inches(4.0))
        add_card(s11, p_left, Inches(1.5), Inches(3.75), Inches(5.4), COLOR_CBK_WHITE, p_col)
        tx = s11.shapes.add_textbox(p_left + Inches(0.2), Inches(1.7), Inches(3.35), Inches(5.0))
        tf = tx.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = p_col
        p.space_after = Pt(12)

        for b in p_bullets:
            p = tf.add_paragraph()
            p.text = f"• {b}"
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_CBK_DARK
            p.space_after = Pt(10)

    # Save to all presentation files
    target_files = [
        "CBK_STRIDE_Executive_Boardroom_Deck.pptx",
        "DSWAAP_HR_Finance_GameChanger.pptx",
        "DSWAAP_CBK_Official_Deck.pptx",
        "DSWAAP_Executive_Presentation.pptx",
        "DSWAAP_Secretariat_HR_Finance_Athletics.pptx"
    ]

    for filename in target_files:
        path = os.path.join(OUTPUT_DIR, filename)
        try:
            prs.save(path)
            print(f"✅ Successfully compiled: {path}")
        except Exception as e:
            print(f"⚠️ Could not save {filename}: {e}")


if __name__ == "__main__":
    build_deck()

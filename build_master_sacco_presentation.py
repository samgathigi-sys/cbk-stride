"""
Master Executive PowerPoint Generator for Banki Kuu Staff SACCO STRIDE™ Platform.
Generates a 15-slide executive presentation covering AGM accreditation, Omni-channel dispatch (Email, SMS, WhatsApp), e-voting, quorum meter, and golf/sports telemetry.
"""

import sys
import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Output Path
TARGET_DIR = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e"
PPTX_FILENAME = os.path.join(TARGET_DIR, "SACCO_AI_Governance_Mobile_App_Integration.pptx")

# Color Palette (Obsidian Navy, Royal Blue, Executive Gold, Cyan Glow, Emerald Green)
COLOR_BG = RGBColor(9, 31, 61)        # Deep Navy
COLOR_CARD = RGBColor(15, 42, 77)      # Card Background
COLOR_GOLD = RGBColor(245, 197, 66)    # Executive Gold
COLOR_CYAN = RGBColor(0, 242, 254)     # Tech Cyan
COLOR_GREEN = RGBColor(16, 185, 129)   # Emerald Success
COLOR_WHITE = RGBColor(255, 255, 255)  # Crisp White
COLOR_MUTED = RGBColor(148, 163, 184) # Muted Gray

def create_slide(prs, bg_color=COLOR_BG):
    slide_layout = prs.slide_layouts[6] # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Background rectangle
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = bg_color
    bg.line.fill.background()
    return slide

def add_header(slide, title_text, subtitle_text):
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD
    
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.name = "Arial"
    p2.font.size = Pt(13)
    p2.font.color.rgb = COLOR_MUTED

def add_card(slide, left, top, width, height, title, body_bullets, border_color=COLOR_CYAN):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_CARD
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    
    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    tf.margin_bottom = Inches(0.2)
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    
    for bullet in body_bullets:
        p_b = tf.add_paragraph()
        p_b.text = f"• {bullet}"
        p_b.font.name = "Arial"
        p_b.font.size = Pt(12)
        p_b.font.color.rgb = COLOR_WHITE
        p_b.space_before = Pt(6)

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # --------------------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # --------------------------------------------------------------------------
    slide1 = create_slide(prs)
    
    # Gold accent line
    line = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(2.2), Inches(11.333), Inches(0.08))
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_GOLD
    line.line.fill.background()

    tb = slide1.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(11.333), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "STRIDE™ ENTERPRISE SUITE"
    p.font.name = "Arial"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    p2 = tf.add_paragraph()
    p2.text = "Banki Kuu Staff SACCO 58th AGM, Encrypted E-Voting, Omni-Channel Dispatch & Sports Telemetry"
    p2.font.name = "Arial"
    p2.font.size = Pt(20)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.space_before = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "Executive Master Dossier for Board of Directors, Executive Committee & Statutory Scrutinizers\nCentral Bank of Kenya | October 2026"
    p3.font.name = "Arial"
    p3.font.size = Pt(13)
    p3.font.color.rgb = COLOR_MUTED
    p3.space_before = Pt(20)

    # --------------------------------------------------------------------------
    # SLIDE 2: EXECUTIVE SUMMARY & STRATEGIC VALUE
    # --------------------------------------------------------------------------
    slide2 = create_slide(prs)
    add_header(slide2, "1. Executive Summary & Strategic Value Proposition", "Transforming statutory AGM governance, accreditation speed, and delegate experience for Banki Kuu SACCO")
    
    add_card(slide2, 0.8, 1.8, 3.6, 5.0, "⚡ 2-Second Gate Speed", [
        "Replaces 2-hour registration queues with dynamic QR scans.",
        "Instant visual & sound gate verification.",
        "Automatic physical lanyard badge printing trigger.",
        "Eliminates manual headcount paperwork."
    ], COLOR_GOLD)

    add_card(slide2, 4.8, 1.8, 3.6, 5.0, "📱 Omni-Channel Dispatch", [
        "Tri-channel dispatch via Email, SMS & WhatsApp.",
        "100% delegate reachability guarantee.",
        "Interactive WhatsApp QR pass card payload.",
        "1-click wa.me & stream link deep integration."
    ], COLOR_CYAN)

    add_card(slide2, 8.8, 1.8, 3.6, 5.0, "🗳️ SASRA & E-Voting Compliance", [
        "Real-time statutory quorum floor meter.",
        "Share-weighted voting power (e.g. 10,000 votes).",
        "Anti-double voting cryptographic security.",
        "Instant returning officer election certification."
    ], COLOR_GREEN)

    # --------------------------------------------------------------------------
    # SLIDE 3: OMNI-CHANNEL DISPATCH ARCHITECTURE
    # --------------------------------------------------------------------------
    slide3 = create_slide(prs)
    add_header(slide3, "2. Tri-Channel Omni-Dispatch Architecture (Email + SMS + WhatsApp)", "Ensuring 100% reachability across office, mobile data, and feature-phone delegates")

    add_card(slide3, 0.8, 1.8, 3.6, 5.0, "📩 Formal Email Dispatch", [
        "Delivers statutory AGM notice & 5-step agenda.",
        "Embedded high-res dynamic QR pass image.",
        "PDF pass attachment for boardroom printing.",
        "Gmail plus-addressing simulation support."
    ])

    add_card(slide3, 4.8, 1.8, 3.6, 5.0, "💬 SMS Gateway Reachability", [
        "98% open rate delivered in < 5 seconds.",
        "Works offline on basic feature phones.",
        "Contains ticket serial ID & 1-tap direct web link.",
        "Safaricom / Airtel network integration."
    ])

    add_card(slide3, 8.8, 1.8, 3.6, 5.0, "📲 WhatsApp Business API", [
        "Rich interactive card with embedded QR image.",
        "Pre-filled delegate credentials & vote weight.",
        "Interactive action buttons: [Open Pass] [Vote].",
        "1-click wa.me instant delivery link."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 4: 2-SECOND ENTRANCE SCANNER & DYNAMIC QR ENGINE
    # --------------------------------------------------------------------------
    slide4 = create_slide(prs)
    add_header(slide4, "3. Fast-Track Entrance Scanner & Dynamic QR Engine", "HMAC-SHA256 signed tokens to prevent ticket duplication and accelerate gate clearance")

    add_card(slide4, 0.8, 1.8, 5.6, 5.0, "🛡️ Cryptographic QR Tamper Protection", [
        "Every QR pass embeds an HMAC-SHA256 signature salt.",
        "Time-bounded validity with gate station parameters.",
        "Prevents screenshot sharing & ticket duplication.",
        "Scans seamlessly from smartphone screen or printed pass."
    ])

    add_card(slide4, 6.8, 1.8, 5.6, 5.0, "📷 Gate Usher Mobile & Terminal Suite", [
        "Operates on any smartphone, iPad, or Android terminal.",
        "Instant sound effect & visual balloon feedback on pass.",
        "Displays delegate department, member ID, and photo.",
        "Auto-triggers physical badge printer at venue entrance."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 5: STATUTORY QUORUM METER & SASRA COMPLIANCE
    # --------------------------------------------------------------------------
    slide5 = create_slide(prs)
    add_header(slide5, "4. Statutory AGM Quorum Meter & SASRA Telemetry", "Real-time compliance auditing under Companies Act 2015 § 284 & SACCO Bylaws")

    add_card(slide5, 0.8, 1.8, 3.6, 5.0, "🏛️ Quorum Floor Enforcement", [
        "Monitors statutory quorum threshold (e.g. 25/50/150 members).",
        "Live progress bar showing percentage to quorum.",
        "Alerts Chairman when assembly is lawfully constituted."
    ])

    add_card(slide5, 4.8, 1.8, 3.6, 5.0, "🗳️ Member & Proxy Classification", [
        "Separates Principal Shareholder Voting Members.",
        "Verifies Duly Appointed Proxy Holders.",
        "Tracks Independent Auditors & SASRA Observers."
    ])

    add_card(slide5, 8.8, 1.8, 3.6, 5.0, "📜 Statutory Export Register", [
        "Instant 1-click download of official accreditation CSV.",
        "Immutable audit log timestamping every check-in.",
        "SASRA regulatory submission ready."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 6: SHARE-WEIGHTED E-VOTING BOOTH & SECRET BALLOT
    # --------------------------------------------------------------------------
    slide6 = create_slide(prs)
    add_header(slide6, "5. Encrypted E-Voting & Share-Weighted Secret Ballot", "Enforcing 1-member-1-vote or share-weighted voting power with instant returning officer certification")

    add_card(slide6, 0.8, 1.8, 5.6, 5.0, "🔒 Auto-Pre-Filled Voting Station", [
        "Automatically unlocks delegate ballot via URL parameter or serial ID.",
        "Pre-calculates certified voting power (e.g. 10,000 votes for Principals, 35,000 for Proxies).",
        "Prevents accidental voter impersonation via locked identity credentials.",
        "Evaluator shortcut toggle for rapid boardroom presentation."
    ])

    add_card(slide6, 6.8, 1.8, 5.6, 5.0, "📊 Live Scrutineer Tally & Certification", [
        "Real-time election results tally across board resolutions.",
        "Single-vote enforcement prevents duplicate ballot submissions.",
        "Instant certificate generation for Chairman & Returning Officer.",
        "Zero manual tallying errors or recount disputes."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 7: MULTILINGUAL NLP SENTIMENT ANALYSIS
    # --------------------------------------------------------------------------
    slide7 = create_slide(prs)
    add_header(slide7, "6. Multilingual NLP Attendee Sentiment & Pulse Survey", "Natural Language Processing extracting operational aspects from English & Swahili feedback")

    add_card(slide7, 0.8, 1.8, 5.6, 5.0, "🤖 Real-Time NLP Aspect Extraction", [
        "Analyzes open-ended comments in English & Swahili.",
        "Extracts operational aspects: Dividends, Gate Speed, Venue Audio, Food Catering.",
        "Calculates sentiment polarity scores (+0.25 Positive to -0.25 Negative).",
        "Auto-pre-fills active delegate name dynamically."
    ])

    add_card(slide7, 6.8, 1.8, 5.6, 5.0, "📈 Board NPS & Executive Telemetry", [
        "Net Promoter Score (NPS) calculation for Board of Directors.",
        "Average star rating analytics (5.0 / 5.0 scale).",
        "Operational Aspects Health Matrix with percentage distribution.",
        "Live feedback stream with color-coded sentiment badges."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 8: MULTI-SPORT & GOLF TOURNAMENT GATEWAY
    # --------------------------------------------------------------------------
    slide8 = create_slide(prs)
    add_header(slide8, "7. Multi-Sport & Golf Tournament Gateway", "Expanding STRIDE™ across 20+ disciplines for CBK Sports Club & Inter-Bank Championships")

    add_card(slide8, 0.8, 1.8, 5.6, 5.0, "⛳ Pro-Shop Golf Check-In & Tee-Times", [
        "Fast-track QR scan at Muthaiga Golf Club & CBK Sports Complex.",
        "Confirms player handicap division (e.g. Handicap 12 Executive).",
        "Assigns tee times (07:30 AM Hole 1) and caddie allocations.",
        "WhatsApp Golf Pass deep-link dispatch."
    ])

    add_card(slide8, 6.8, 1.8, 5.6, 5.0, "🏆 Inter-Bank Discipline Management", [
        "Supports Football, Athletics, Basketball, Swimming, Chess & Volleyball.",
        "Dual-Gate attendance tracking (Pre-Sport & Post-Sport).",
        "Session duration validation (minimum 45 mins floor).",
        "Automated daily stipend allowance qualification (KES 2,500/day)."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 9: M-PESA DARAJA STK PUSH & FINANCIAL RECONCILIATION
    # --------------------------------------------------------------------------
    slide9 = create_slide(prs)
    add_header(slide9, "8. M-Pesa STK Push Settlement & Financial Audit", "Seamless integration with Safaricom M-Pesa Paybill 849200 for instant settlements")

    add_card(slide9, 0.8, 1.8, 5.6, 5.0, "💳 Instant M-Pesa STK Push Prompts", [
        "Direct push prompt sent to member handset upon subscription.",
        "Supports clearance fees, VIP passes, and corporate sponsorships.",
        "Instant payment status callback verification.",
        "Integrated paybill reference matching."
    ])

    add_card(slide9, 6.8, 1.8, 5.6, 5.0, "📊 Commercial Reconciliation Ledger", [
        "Tracks total revenue collected per assembly.",
        "Full exportable financial ledger for internal audit.",
        "Automated PDF tax invoice generator.",
        "Zero cash handling risk at event venue."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 10: END-TO-END DELEGATE JOURNEY WORKFLOW
    # --------------------------------------------------------------------------
    slide10 = create_slide(prs)
    add_header(slide10, "9. End-to-End Delegate Journey Workflow", "5-Stage seamless journey from digital invitation to post-event boardroom reporting")

    add_card(slide10, 0.8, 1.8, 2.2, 5.0, "1. Dispatch", [
        "Email, SMS & WhatsApp notifications sent."
    ], COLOR_GOLD)

    add_card(slide10, 3.2, 1.8, 2.2, 5.0, "2. Digital Pass", [
        "Delegate opens QR pass on phone."
    ], COLOR_CYAN)

    add_card(slide10, 5.6, 1.8, 2.2, 5.0, "3. Gate Scan", [
        "2-sec usher scan & Quorum update."
    ], COLOR_CYAN)

    add_card(slide10, 8.0, 1.8, 2.2, 5.0, "4. E-Vote", [
        "Encrypted ballot with weighted votes."
    ], COLOR_GREEN)

    add_card(slide10, 10.4, 1.8, 2.1, 5.0, "5. NLP Pulse", [
        "Member feedback & Board NPS report."
    ], COLOR_GOLD)

    # --------------------------------------------------------------------------
    # SLIDE 11: SECURITY & CRYPTOGRAPHIC SAFEGUARDS
    # --------------------------------------------------------------------------
    slide11 = create_slide(prs)
    add_header(slide11, "10. Enterprise Security & Role-Based Access Control (RBAC)", "Banki Kuu SACCO multi-tier security framework and cryptographic safeguards")

    add_card(slide11, 0.8, 1.8, 5.6, 5.0, "🔐 Cryptographic Security Controls", [
        "HMAC-SHA256 token signature validation.",
        "SHA-256 hashed admin passkeys.",
        "Encrypted SQLite DB with offline resilience mode.",
        "HTTPS SSL encryption on Streamlit Cloud."
    ])

    add_card(slide11, 6.8, 1.8, 5.6, 5.0, "👔 Role-Based Access Control (RBAC)", [
        "Super Admin: Samuel Gathigi Njuguna (CBK-3428).",
        "Executive Chairman: Johnstone B Angwenyi (CBK-3071).",
        "Secretariat, Finance & HR Compliance Leads.",
        "Audit trail logging for all export & role actions."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 12: COMPARATIVE BENCHMARK: STRIDE™ VS LEGACY MANUAL SYSTEMS
    # --------------------------------------------------------------------------
    slide12 = create_slide(prs)
    add_header(slide12, "11. Comparative Benchmark: STRIDE™ vs Legacy Manual Event Operations", "Why modern AI & mobile automation outperforms traditional paper-based event logistics")

    add_card(slide12, 0.8, 1.8, 5.6, 5.0, "❌ Legacy Manual Operations", [
        "Slow 2-hour queue delays at registration desks.",
        "Paper sign-in sheets prone to lost attendance records.",
        "Manual vote counting with recount disputes.",
        "Uncertain quorum counts during call-to-order.",
        "Low member reachability via paper letters."
    ], COLOR_MUTED)

    add_card(slide12, 6.8, 1.8, 5.6, 5.0, "🟢 STRIDE™ Enterprise Platform", [
        "Fast 2-second QR entrance scan.",
        "100% digital audit trail with CSV export.",
        "Share-weighted e-voting with instant tally.",
        "Live statutory SASRA Quorum meter.",
        "Tri-channel dispatch (Email, SMS, WhatsApp)."
    ], COLOR_GREEN)

    # --------------------------------------------------------------------------
    # SLIDE 13: CLOUD & INFRASTRUCTURE ARCHITECTURE
    # --------------------------------------------------------------------------
    slide13 = create_slide(prs)
    add_header(slide13, "12. Infrastructure & Cloud Deployment Architecture", "High-availability, offline-resilient hybrid deployment model")

    add_card(slide13, 0.8, 1.8, 5.6, 5.0, "☁️ Streamlit Cloud Production Hosting", [
        "Hosted live at https://cbk-stride.streamlit.app/BKS",
        "Automated CI/CD deployment from GitHub main branch.",
        "Responsive glassmorphism UI for mobile, tablet & desktop.",
        "Zero client software installation required."
    ])

    add_card(slide13, 6.8, 1.8, 5.6, 5.0, "🔄 Offline Resilient Data Sync", [
        "Local SQLite database engine for instant zero-latency queries.",
        "Automatic fallback when internet is disrupted.",
        "Google Sheets API (gspread) synchronization.",
        "Scalable to 5,000+ simultaneous delegates."
    ])

    # --------------------------------------------------------------------------
    # SLIDE 14: IMPLEMENTATION ROADMAP & PHASED ROLLOUT
    # --------------------------------------------------------------------------
    slide14 = create_slide(prs)
    add_header(slide14, "13. Phased Implementation Roadmap", "Structured 4-phase deployment plan leading to the 58th Annual General Meeting")

    add_card(slide14, 0.8, 1.8, 2.7, 5.0, "Phase 1: Ingestion", [
        "Upload SACCO delegate roster.",
        "Configure M-Pesa paybill 849200.",
        "Verify RBAC credentials."
    ])

    add_card(slide14, 3.8, 1.8, 2.7, 5.0, "Phase 2: Dispatch", [
        "Execute Tri-channel dispatch (Email/SMS/WhatsApp).",
        "Monitor pass delivery status.",
        "Run dry-run gate tests."
    ])

    add_card(slide14, 6.8, 1.8, 2.7, 5.0, "Phase 3: Live AGM", [
        "Deploy entrance QR gate scanners.",
        "Track live SASRA Quorum meter.",
        "Execute e-voting elections."
    ])

    add_card(slide14, 9.8, 1.8, 2.7, 5.0, "Phase 4: Reporting", [
        "Generate Returning Officer Certificate.",
        "Export SASRA Audit Register.",
        "Publish Board NPS report."
    ], COLOR_GOLD)

    # --------------------------------------------------------------------------
    # SLIDE 15: BOARD APPROVAL & CALL TO ACTION
    # --------------------------------------------------------------------------
    slide15 = create_slide(prs)
    add_header(slide15, "14. Board Resolution & Call to Action", "Formal recommendation for Board adoption of STRIDE™ for Banki Kuu Staff SACCO")

    add_card(slide15, 0.8, 1.8, 11.7, 5.0, "🏛️ Recommended Board Resolutions", [
        "1. ADOPT STRIDE™ Enterprise as the official statutory accreditation, voting, and quorum engine for the 58th AGM.",
        "2. AUTHORIZE Secretariat & IT Directorate to execute Tri-channel dispatch (Email, SMS, WhatsApp) for all 500+ accredited delegates.",
        "3. APPROVE integration of M-Pesa STK push for fast-track clearance and dividend pass verification.",
        "4. COMMENCE live usher gate scanner training and boardroom trial ahead of the upcoming statutory assembly.",
        "\nLive Production Portal: https://cbk-stride.streamlit.app/BKS | Contact: sam.gathigi@gmail.com"
    ], COLOR_GOLD)

    prs.save(PPTX_FILENAME)
    print("==================================================")
    print("🎉 MASTER EXECUTIVE PPTX GENERATED SUCCESSFULLY!")
    print(f"File Location: {PPTX_FILENAME}")
    print("==================================================")

if __name__ == "__main__":
    build_presentation()

"""
DSWAAP - Central Bank of Kenya (CBK) Sports Wellness & Attendance Automation Platform
Dedicated Executive Presentation Generator: DATA SOVEREIGNTY & CYBERSECURITY BLUEPRINT
Target Audience: Board of Directors, CISO, Head of IT Security, Data Protection Officer (DPO), Internal Audit

Adheres strictly to official CBK Corporate Branding:
- CBK Royal Blue: #025BBF (Primary Brand Color from centralbank.go.ke)
- CBK Deep Navy:  #10529E (Secondary Brand Color from centralbank.go.ke)
- CBK Saffron Gold: #F8B82D (Official Brand Color from CBK Logo)
- CBK Amber Gold Accent: #F7941D (Website Hero Accent)
- CBK Ice Blue Tint: #EEF6FC (Card Backgrounds)
- Official CBK Coat of Arms Crest Logo embedded on EVERY slide.

Generates:
- CBK_DSWAAP_Data_Sovereignty_Security_Deck.pptx
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


def create_header(slide, title_text, category_text="CENTRAL BANK OF KENYA | DATA SOVEREIGNTY BLUEPRINT"):
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


def build_sovereignty_deck():
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
    p.text = "DATA SOVEREIGNTY & CYBERSECURITY ARCHITECTURE"
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COLOR_CBK_WHITE
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "Institutional Security Blueprint: Keeping DSWAAP Telemetry 100% CBK-ONLY"
    p.font.size = Pt(19)
    p.font.color.rgb = COLOR_CBK_GOLD
    p.space_after = Pt(16)

    p = tf.add_paragraph()
    p.text = "Statutory Compliance: Kenya Data Protection Act (2019) • CBK Cybersecurity Guidelines • Central Bank of Kenya Act (Cap 491)"
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_CBK_ICE_BLUE

    # ==========================================================================
    # SLIDE 2: THE 5-PILLAR SOVEREIGNTY FRAMEWORK
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    create_header(s2, "The 5-Pillar Defense-in-Depth Sovereignty Model", "Architectural Overview")

    pillars = [
        ("1. PHYSICAL RESIDENCY", COLOR_CBK_PRIMARY, [
            "100% Kenyan Soil: Hosted inside CBK Primary DC (Haile Selassie Ave).",
            "Secondary DR Site: Kenya School of Monetary Studies (KSMS) & Eldoret.",
            "AES-256 Storage: Transparent Data Encryption on all enterprise SAN storage volumes.",
            "Hardware Key Control: Cryptographic root keys safeguarded inside CBK HSMs."
        ]),
        ("2. NETWORK PERIMETER", COLOR_CBK_GOLD, [
            "Telecom Private APN: Captain SIMs on cbk.safaricom.co.ke private circuit.",
            "Zero Public Internet: Cellular packets route via private MPLS to CBK firewall.",
            "Split-Horizon DNS: dswaap.centralbank.go.ke resolves only within CBK intranet.",
            "Invisible to Web: Outside queries receive NXDOMAIN (non-existent domain)."
        ]),
        ("3. ZERO-TRUST IDENTITY", COLOR_CBK_NAVY, [
            "Active Directory SSO: Authenticates strictly via official @centralbank.go.ke.",
            "Domain Restriction: External domains (@gmail.com, etc.) are blocked at ingress.",
            "Segregation of Duties: Captains, Athletes, HR, and Finance have isolated RBAC roles.",
            "Financial Privacy: Field devices are strictly stripped of all monetary data."
        ])
    ]

    for idx, (title, color, bullets) in enumerate(pillars):
        left_pos = Inches(0.8) + (idx * Inches(4.0))
        add_card(s2, left_pos, Inches(1.5), Inches(3.75), Inches(5.4), COLOR_CBK_WHITE, color)
        tx = s2.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.7), Inches(3.35), Inches(5.0))
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
            p.font.size = Pt(11)
            p.font.color.rgb = COLOR_CBK_DARK
            p.space_after = Pt(8)

    # ==========================================================================
    # SLIDE 3: LEGAL & STATUTORY COMPLIANCE (KDPA 2019)
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    create_header(s3, "Legal & Regulatory Framework: Kenya Data Protection Act 2019", "Statutory Compliance")

    kdpa_cards = [
        ("SECTION 48 & 50: DATA LOCALIZATION", COLOR_CBK_PRIMARY, [
            "Statutory Mandate: Personal Identifiable Information (PII) of Kenyan citizens processed by strategic national institutions must reside within Kenyan jurisdiction.",
            "DSWAAP Compliance: Zero employee names, payroll IDs, or physical telemetry traverse foreign public clouds. All primary records reside in Nairobi.",
            "Risk Mitigated: Eliminates compliance penalties from the Office of the Data Protection Commissioner (ODPC)."
        ]),
        ("SECTION 3: PURPOSE LIMITATION & MINIMIZATION", COLOR_CBK_GOLD, [
            "Statutory Mandate: Collect only the minimum data strictly necessary for the authorized purpose.",
            "DSWAAP Compliance: Dynamic QR codes encode only ephemeral nonces and station IDs. No personal health, biometric, or banking details are placed in the optical QR payload.",
            "Field Privacy: Field kiosks display only 'Certified Attendance Units'—monetary figures are stripped."
        ]),
        ("SECTION 40 & CBK AUDIT RULES: IMMUTABILITY", COLOR_CBK_NAVY, [
            "Statutory Mandate: Ensure absolute auditability, integrity, and tamper-evident logging of public records.",
            "DSWAAP Compliance: Append-only SQLite/PostgreSQL ledger with SHA-256 cryptographic audit chaining.",
            "Retention Policy: Attendance archives are retained for 7 years pursuant to National Archives & CBK Financial Regulations."
        ])
    ]

    for idx, (title, color, bullets) in enumerate(kdpa_cards):
        left_pos = Inches(0.8) + (idx * Inches(4.0))
        add_card(s3, left_pos, Inches(1.5), Inches(3.75), Inches(5.4), COLOR_CBK_WHITE, color)
        tx = s3.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.7), Inches(3.35), Inches(5.0))
        tf = tx.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
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
    # SLIDE 4: TELECOM PRIVATE APN ARCHITECTURE (SAFARICOM / AIRTEL)
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    create_header(s4, "Telecom Private Corporate APN: Eliminating Public Internet Transit", "Network Security")

    apn_cards = [
        ("📱 FIELD LAYER: CAPTAIN TABLET", COLOR_CBK_PRIMARY, [
            "CBK MDM Enrolled: Samsung/iPad tablets enrolled in Microsoft Intune / Knox.",
            "Corporate SIM Card: Provisioned exclusively on private APN cbk.safaricom.co.ke.",
            "Hotspot Tethering: Broadcasts encrypted Wi-Fi (CBK-SPORTS-SECURE) to field athletes.",
            "Zero Personal Cost: Athletes require KES 0 personal bundles to scan and check in."
        ]),
        ("📡 CARRIER LAYER: PRIVATE APN", COLOR_CBK_GOLD, [
            "Private IP Allocation: Devices receive non-routable private IPs (10.x.x.x range).",
            "No Public Internet: Packets cannot browse the World Wide Web or social networks.",
            "Direct MPLS Circuit: Safaricom/Airtel tunnels traffic directly to CBK Data Center.",
            "Point-to-Point IPSec: Bank-grade 256-bit encryption across the cellular backhaul."
        ]),
        ("🏛️ PERIMETER LAYER: CBK CORE", COLOR_CBK_NAVY, [
            "Next-Gen Firewalls: Palo Alto / Fortinet deep packet inspection at CBK perimeter.",
            "Internal WAF: Web Application Firewall protects https://dswaap.centralbank.go.ke.",
            "Split-Horizon DNS: Hostname resolves only over the private corporate tunnel.",
            "Hard Drop Policy: Any connection attempt to external IP addresses is terminated instantly."
        ])
    ]

    for idx, (title, color, bullets) in enumerate(apn_cards):
        left_pos = Inches(0.8) + (idx * Inches(4.0))
        add_card(s4, left_pos, Inches(1.5), Inches(3.75), Inches(5.4), COLOR_CBK_WHITE, color)
        tx = s4.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.7), Inches(3.35), Inches(5.0))
        tf = tx.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
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
    # SLIDE 5: ROLE-BASED ACCESS CONTROL & PRIVACY-BY-DESIGN
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    create_header(s5, "Role-Based Access Control (RBAC) & Segregation of Duties", "Identity Governance")

    rbac_rows = [
        ("Role", "Authentication", "Authorized Scope", "Financial Data Access", True),
        ("CBK Athlete (Employee)", "Staff ID + SSO / Magic Link", "View personal pass, scan Gate 1/2, view own history", "NO ACCESS (Stripped for privacy)", False),
        ("Discipline Captain", "CBK SSO + Hardware Tablet PIN", "Generate QR codes & view roster for assigned sport only", "NO ACCESS (Attendance units only)", False),
        ("Secretariat (HR)", "CBK AD SSO + Multi-Factor Auth", "Manage all 18 sports, view live turnout, edit rosters", "NO ACCESS (Attendance units only)", False),
        ("Finance & Accounts", "Privileged Finance AD Group + MFA", "Audit compliance, view duration exceptions, approve AP", "FULL ACCESS (Sole valuation authority)", False),
        ("Internal Audit", "Read-Only Audit Group + Strict MFA", "Inspect tamper-proof hash chain, audit non-compliant logs", "READ-ONLY (Audit verification)", False)
    ]

    y_pos = Inches(1.5)
    for r_idx, (p1, p2, p3, p4, is_hdr) in enumerate(rbac_rows):
        bg_col = COLOR_CBK_PRIMARY if is_hdr else (COLOR_CBK_ICE_BLUE if r_idx % 2 == 1 else COLOR_CBK_WHITE)
        bd_col = COLOR_CBK_GOLD if is_hdr else COLOR_CBK_GOLD

        add_card(s5, Inches(0.8), y_pos, Inches(11.733), Inches(0.82), bg_col, bd_col)

        tx = s5.shapes.add_textbox(Inches(1.0), y_pos + Inches(0.06), Inches(2.4), Inches(0.7))
        p = tx.text_frame.paragraphs[0]
        p.text = p1
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_CBK_WHITE if is_hdr else COLOR_CBK_DARK

        tx = s5.shapes.add_textbox(Inches(3.5), y_pos + Inches(0.06), Inches(2.6), Inches(0.7))
        p = tx.text_frame.paragraphs[0]
        p.text = p2
        p.font.size = Pt(10)
        p.font.bold = is_hdr
        p.font.color.rgb = COLOR_CBK_GOLD if is_hdr else COLOR_CBK_DARK

        tx = s5.shapes.add_textbox(Inches(6.2), y_pos + Inches(0.06), Inches(3.3), Inches(0.7))
        p = tx.text_frame.paragraphs[0]
        p.text = p3
        p.font.size = Pt(10)
        p.font.bold = is_hdr
        p.font.color.rgb = COLOR_CBK_WHITE if is_hdr else COLOR_CBK_DARK

        tx = s5.shapes.add_textbox(Inches(9.6), y_pos + Inches(0.06), Inches(2.7), Inches(0.7))
        p = tx.text_frame.paragraphs[0]
        p.text = p4
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_CBK_GOLD if is_hdr else (COLOR_CBK_SUCCESS if "FULL" in p4 else (COLOR_CBK_RED if "NO ACCESS" in p4 else COLOR_CBK_PRIMARY))

        y_pos += Inches(0.88)

    # ==========================================================================
    # SLIDE 6: CRYPTOGRAPHIC ANTI-FRAUD ENGINE
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    create_header(s6, "Cryptographic Anti-Tampering & Anti-Spoofing Architecture", "Fraud Defense")

    crypto_cards = [
        ("⏱️ 60-SECOND DYNAMIC NONCES", COLOR_CBK_PRIMARY, [
            "Rotating QR Tokens: The QR code on captain tablets refreshes automatically every 60 seconds.",
            "Anti-Screenshot Defense: If an employee takes a photo/screenshot and forwards via WhatsApp, the code has expired before it can be used.",
            "HMAC-SHA256 Signatures: Every token is cryptographically signed with an internal secret key."
        ]),
        ("🔗 TAMPER-PROOF AUDIT HASH CHAIN", COLOR_CBK_GOLD, [
            "Cryptographic Chaining: Each attendance event includes Hash_n = HMAC(Record_n || Hash_n-1).",
            "Immutable Ledger: If any system administrator attempts to alter past timestamps or durations, the hash chain breaks instantly.",
            "Automated Internal Audit Alert: Any hash mismatch flags a critical security exception immediately."
        ]),
        ("📍 GEOFENCE & STATION BINDING", COLOR_CBK_NAVY, [
            "Physical Boundary Enforcement: Validates GPS bounding box of approved CBK venues (CBK Sports Club, Kasarani).",
            "BSSID Proximity Binding: Scans are validated against the Captain tablet's unique Wi-Fi MAC address.",
            "Out-of-Bounds Flag: Any scan attempting to bypass local proximity is tagged as 'OUT_OF_BOUNDS_LOCATION'."
        ])
    ]

    for idx, (title, color, bullets) in enumerate(crypto_cards):
        left_pos = Inches(0.8) + (idx * Inches(4.0))
        add_card(s6, left_pos, Inches(1.5), Inches(3.75), Inches(5.4), COLOR_CBK_WHITE, color)
        tx = s6.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.7), Inches(3.35), Inches(5.0))
        tf = tx.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
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
    # SLIDE 7: TENANT-LOCKED CLOUD REFLECTION (GOOGLE WORKSPACE)
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    create_header(s7, "Restricted Cloud Mirroring: Google Workspace Tenant Isolation", "Cloud Security")

    cloud_cards = [
        ("🔒 DOMAIN SHARING RESTRICTION", COLOR_CBK_PRIMARY, [
            "Central Bank of Kenya Tenant Only: Google Workspace folder permissions are set to 'Restricted — Only people within CBK'.",
            "External Sharing Disabled: Administrative policies block sharing with any external domain (@gmail.com, @yahoo.com).",
            "Denied Access: Even if the spreadsheet link is forwarded outside, Google blocks access with 'You need access'."
        ]),
        ("🛡️ DATA LOSS PREVENTION (DLP)", COLOR_CBK_GOLD, [
            "Export & Download Blocking: Policy checks 'Disable options to download, print, and copy for commenters and viewers'.",
            "Information Rights Management: Prevents local duplication onto unmanaged personal USB drives or cloud storages.",
            "Watermarking: Google Workspace applies persistent institutional metadata watermarks."
        ]),
        ("👁️ CONTEXT-AWARE ACCESS & LOGS", COLOR_CBK_NAVY, [
            "CBK IP Allowlisting: Context-Aware Access policies ensure sheets can only be opened from CBK-managed devices or corporate egress IPs.",
            "Immutable Google Admin Audit Logs: Every sheet open, edit, and access event is logged in Google Workspace Security Center.",
            "7-Year Cloud Audit Retention: Complete historical audit trails accessible to Internal Audit."
        ])
    ]

    for idx, (title, color, bullets) in enumerate(cloud_cards):
        left_pos = Inches(0.8) + (idx * Inches(4.0))
        add_card(s7, left_pos, Inches(1.5), Inches(3.75), Inches(5.4), COLOR_CBK_WHITE, color)
        tx = s7.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.7), Inches(3.35), Inches(5.0))
        tf = tx.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
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
    # SLIDE 8: CISO & DPO SECURITY IMPLEMENTATION MATRIX
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    create_header(s8, "Institutional Cybersecurity Checklist & Next Steps", "Governance Sign-Off")

    matrix_rows = [
        ("Implementation Pillar", "Technical Control", "Responsible Directorate", "Compliance Status", True),
        ("Data Localization", "Host primary DB at Haile Selassie Ave Data Center + KSMS DR", "IT Infrastructure & DBA Team", "✅ Architected / Ready", False),
        ("Perimeter Ring-Fence", "Provision Safaricom CBK Private APN (cbk.safaricom.co.ke)", "Telecoms & Network Services", "🔄 Carrier Provisioning Ready", False),
        ("Domain & SSL", "Bind split-horizon DNS dswaap.centralbank.go.ke with internal SSL", "Network & Cyber Security Ops", "🔄 Ready for Config", False),
        ("Identity Federation", "Hook DSWAAP into Microsoft Entra ID (Azure AD) via SAML 2.0", "Enterprise Identity Management", "🔄 Ready for Config", False),
        ("Financial Privacy", "Strip monetary fields on field kiosks; assign valuation solely to Finance", "Internal Audit & Finance", "✅ Fully Implemented", False),
        ("Security Sign-Off", "Execute Vulnerability Assessment & Penetration Testing (VAPT)", "CISO Office & Internal Audit", "📋 Scheduled for Go-Live", False)
    ]

    y_pos = Inches(1.5)
    for r_idx, (p1, p2, p3, p4, is_hdr) in enumerate(matrix_rows):
        bg_col = COLOR_CBK_PRIMARY if is_hdr else (COLOR_CBK_ICE_BLUE if r_idx % 2 == 1 else COLOR_CBK_WHITE)
        bd_col = COLOR_CBK_GOLD if is_hdr else COLOR_CBK_GOLD

        add_card(s8, Inches(0.8), y_pos, Inches(11.733), Inches(0.72), bg_col, bd_col)

        tx = s8.shapes.add_textbox(Inches(1.0), y_pos + Inches(0.06), Inches(2.5), Inches(0.6))
        p = tx.text_frame.paragraphs[0]
        p.text = p1
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = COLOR_CBK_WHITE if is_hdr else COLOR_CBK_DARK

        tx = s8.shapes.add_textbox(Inches(3.6), y_pos + Inches(0.06), Inches(3.8), Inches(0.6))
        p = tx.text_frame.paragraphs[0]
        p.text = p2
        p.font.size = Pt(10)
        p.font.bold = is_hdr
        p.font.color.rgb = COLOR_CBK_GOLD if is_hdr else COLOR_CBK_DARK

        tx = s8.shapes.add_textbox(Inches(7.5), y_pos + Inches(0.06), Inches(2.4), Inches(0.6))
        p = tx.text_frame.paragraphs[0]
        p.text = p3
        p.font.size = Pt(10)
        p.font.bold = is_hdr
        p.font.color.rgb = COLOR_CBK_WHITE if is_hdr else COLOR_CBK_DARK

        tx = s8.shapes.add_textbox(Inches(10.0), y_pos + Inches(0.06), Inches(2.3), Inches(0.6))
        p = tx.text_frame.paragraphs[0]
        p.text = p4
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_CBK_GOLD if is_hdr else (COLOR_CBK_SUCCESS if "✅" in p4 else (COLOR_CBK_NAVY if "🔄" in p4 else COLOR_CBK_DARK))

        y_pos += Inches(0.78)

    # Save dedicated Data Sovereignty Deck
    out_path = os.path.join(OUTPUT_DIR, "CBK_DSWAAP_Data_Sovereignty_Security_Deck.pptx")
    prs.save(out_path)
    print(f"✅ Data Sovereignty Presentation compiled successfully: {out_path}")
    return out_path


if __name__ == "__main__":
    build_sovereignty_deck()

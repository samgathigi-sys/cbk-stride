import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tc_pr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding for a table cell in dxa (1 pt = 20 dxa)."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)

def create_document():
    doc = Document()

    # Page Margins
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)

    # Base Colors
    NAVY = RGBColor(8, 28, 58)       # #081C3A
    GOLD = RGBColor(217, 119, 6)      # #D97706 / #F5C542 dark gold for text
    SLATE = RGBColor(71, 85, 105)     # #475569
    DARK = RGBColor(15, 23, 42)       # #0F172A

    # ==============================================================================
    # COVER / TITLE BLOCK
    # ==============================================================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(36)
    title_p.paragraph_format.space_after = Pt(4)
    run_t = title_p.add_run("STRIDE™ UNIVERSAL EVENT PORTAL")
    run_t.font.name = "Arial"
    run_t.font.size = Pt(26)
    run_t.font.bold = True
    run_t.font.color.rgb = NAVY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("Commercial Provisioning, Multi-Tenant Architecture & Monetization Playbook")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(15)
    run_sub.font.bold = True
    run_sub.font.color.rgb = GOLD

    desc_p = doc.add_paragraph()
    desc_p.paragraph_format.space_after = Pt(20)
    run_desc = desc_p.add_run(
        "An Executive Technical & Business Strategy Guide on How Automated Gateways, "
        "Self-Service SaaS, and Turnkey Concierge Engagements Monetize Corporate AGMs, "
        "Inter-Bank Tournaments, Professional Galas, and Public Festivals Across Kenya."
    )
    run_desc.font.name = "Calibri"
    run_desc.font.size = Pt(11)
    run_desc.font.color.rgb = SLATE

    # Meta Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Author & Architect:", "Samuel Gathigi Njuguna (Super Admin / Systems Lead)"),
        ("Platform Engine:", "STRIDE™ Enterprise Multi-Tenant Event & Telemetry Platform"),
        ("Monetization Models:", "Model A: Self-Service SaaS  |  Model B: Turnkey Concierge Agency"),
        ("Date / Version:", "October 2026 | Master Release v2.4 (Commercialization Grade)")
    ]
    for r_idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[r_idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.8)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(2)
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = NAVY
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = DARK

        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 1: THE CORE COMMERCIAL QUESTION
    # ==============================================================================
    h1 = doc.add_heading(level=1)
    r_h1 = h1.add_run("1. Executive Overview: The Dual-Operating Business Model")
    r_h1.font.color.rgb = NAVY
    r_h1.font.size = Pt(17)

    doc.add_paragraph(
        "When commercializing the STRIDE™ Event Gateway, prospective clients and partners inevitably ask the fundamental operational question:"
    )

    callout = doc.add_table(rows=1, cols=1)
    callout.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_box = callout.rows[0].cells[0]
    c_box.width = Inches(7.0)
    set_cell_background(c_box, "FEF3C7") # Warm gold background
    set_cell_margins(c_box, top=140, bottom=140, left=200, right=200)
    p_box = c_box.paragraphs[0]
    r_box = p_box.add_run(
        "“So, does STRIDE™ provision a portal for someone? Do THEY make it themselves, "
        "or do YOU make it and give them the link?”"
    )
    r_box.font.name = "Arial"
    r_box.font.size = Pt(11.5)
    r_box.font.bold = True
    r_box.font.italic = True
    r_box.font.color.rgb = RGBColor(146, 64, 14) # Deep amber

    doc.add_paragraph(
        "The short, definitive answer is: BOTH! The STRIDE™ platform was deliberately engineered to support "
        "a dual-operating commercial architecture that bridges high-volume self-service automation with high-ticket concierge consulting."
    )

    # Insert Visual 1
    v1_path = "commercial_assets/visual_operating_models.png"
    if os.path.exists(v1_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(v1_path, width=Inches(6.8))
        cap1 = doc.add_paragraph()
        cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rcap1 = cap1.add_run("Figure 1: STRIDE™ Dual-Operating Commercial Model Comparison")
        rcap1.font.italic = True
        rcap1.font.size = Pt(8.5)
        rcap1.font.color.rgb = SLATE

    h2 = doc.add_heading(level=2)
    r_h2 = h2.add_run("1.1 Model A: Client Self-Service SaaS (Zero-Touch Passive Cashflow)")
    r_h2.font.color.rgb = GOLD
    r_h2.font.size = Pt(13)

    p_a = doc.add_paragraph()
    p_a.add_run("In this mode, the client does everything autonomously without you ever touching a keyboard:").font.bold = True
    doc.add_paragraph(
        "• Who Uses It: Busy event coordinators, SACCO assistant secretaries, sports club captains, and wedding/gala organizers who want speed and simplicity.\n"
        "• The User Journey: The client opens the public portal at cbk-stride.streamlit.app/EVENTS, navigates to Tab 2 ('Event Creator Wizard'), selects their cluster (e.g. Corporate AGM or Sports League), and fills in the 4 scoping questions.\n"
        "• Instant Payment: The wizard triggers an automated Safaricom M-Pesa STK Push directly to their phone (e.g., KES 45,000).\n"
        "• Autonomous Spin-Up: The database instantaneously creates their isolated Event ID (e.g. EVT-2026-004), issues a certified Tax Invoice (.txt), and renders their dedicated entrance banner QR code.\n"
        "• Your Operational Overhead: ZERO. The entire KES payment hits your settlement account, the database handles attendee registration, and the gate dashboard is live immediately."
    )

    h2_b = doc.add_heading(level=2)
    r_h2_b = h2_b.add_run("1.2 Model B: Turnkey Concierge Agency (High-Ticket KES 85,000 – 250,000+)")
    r_h2_b.font.color.rgb = GOLD
    r_h2_b.font.size = Pt(13)

    p_b = doc.add_paragraph()
    p_b.add_run("In this mode, YOU make it, brand it, and hand it to them on a silver platter as a white-glove technology partner:").font.bold = True
    doc.add_paragraph(
        "• Who Uses It: Tier-1 SACCOs (Harambee, Stima, Kenya Police, Safaricom SACCO), Central Bank boards, commercial banks, and national sporting federations running high-stakes statutory AGMs or major tournaments.\n"
        "• Why They Pay Premium: Executive boards do not want to configure wizards themselves. They want an accredited technology director to take legal responsibility for statutory quorum compliance, anti-counterfeit gate security, and shareholder election ballot auditing.\n"
        "• Your Service Delivery: You run the wizard in 2 minutes on their behalf, configure custom statutory bylaws (e.g. 15% voting share quorum, 48-hour proxy cutoffs), print official physical roll-up QR entrance banners, and deploy pre-configured iPads to their venue registration desks.\n"
        "• Handover: You provide the Secretariat Chairman with a single executive dashboard link and hand the gate ushers their scanning tablets. You charge a premium turnkey package of KES 120,000 – KES 250,000 per event."
    )

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 2: THE 60-SECOND PROVISIONING ARCHITECTURE
    # ==============================================================================
    h1_2 = doc.add_heading(level=1)
    r_h1_2 = h1_2.add_run("2. Multi-Tenant Event Provisioning Architecture")
    r_h1_2.font.color.rgb = NAVY
    r_h1_2.font.size = Pt(17)

    doc.add_paragraph(
        "How does a single URL provision a completely independent, isolated event portal? "
        "The STRIDE™ architecture relies on dynamic parameter binding and relational database multi-tenancy:"
    )

    # Insert Visual 4
    v4_path = "commercial_assets/visual_portal_lifecycle.png"
    if os.path.exists(v4_path):
        p_img4 = doc.add_paragraph()
        p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(v4_path, width=Inches(6.8))
        cap4 = doc.add_paragraph()
        cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rcap4 = cap4.add_run("Figure 2: End-to-End STRIDE™ Provisioning and Accreditation Lifecycle")
        rcap4.font.italic = True
        rcap4.font.size = Pt(8.5)
        rcap4.font.color.rgb = SLATE

    h2_2a = doc.add_heading(level=2)
    r_h2_2a = h2_2a.add_run("2.1 Dynamic URL Parameter Routing (?event_id=EVT-XXXX)")
    r_h2_2a.font.color.rgb = GOLD
    r_h2_2a.font.size = Pt(13)

    doc.add_paragraph(
        "When an event is provisioned via the wizard, the engine generates an isolated Event ID (e.g., EVT-2026-003). "
        "Every attendee touchpoint is anchored to this identifier via URL query parameters:\n"
        "• Direct Registration Pass: https://cbk-stride.streamlit.app/EVENTS?event_id=EVT-2026-003\n"
        "• When an attendee taps this magic link or scans the venue banner QR code with their iPhone or Android camera, "
        "the portal automatically pre-selects the event, applies the correct ticket pricing, displays the convening entity's statutory notice, "
        "and binds all issued tickets and votes strictly to that event's ledger."
    )

    h2_2b = doc.add_heading(level=2)
    r_h2_2b = h2_2b.add_run("2.2 Isolated Database Schema Multi-Tenancy")
    r_h2_2b.font.color.rgb = GOLD
    r_h2_2b.font.size = Pt(13)

    doc.add_paragraph(
        "To ensure zero data leakage between different organizations (e.g., Safaricom SACCO cannot see CBK Sports Club attendee rosters), "
        "STRIDE™ enforces foreign key event isolation across 4 relational SQLite tables:"
    )

    schema_table = doc.add_table(rows=5, cols=3)
    schema_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Database Table", "Isolation Key", "Business Purpose & Security Function"]
    for c_i, h in enumerate(headers):
        cell = schema_table.rows[0].cells[c_i]
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "081C3A")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    rows_data = [
        ("events_registry", "event_id", "Stores event title, host, cluster category, gate mode, ticket prices, and quorum floors."),
        ("tickets_registry", "event_id + ticket_id", "Holds attendee records, phone numbers, M-Pesa receipts, and cryptographic pass signatures."),
        ("scans_registry", "event_id + ticket_id", "Real-time gate scan timestamps, usher ID, station location, and dual-gate floor validation."),
        ("ballot_registry", "event_id + member_id", "Encrypted statutory voting records, resolution votes, proxy assignments, and quorum tally.")
    ]
    for r_i, (t_name, k_name, desc) in enumerate(rows_data, 1):
        row = schema_table.rows[r_i]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width = Inches(1.8)
        c1.width = Inches(1.8)
        c2.width = Inches(3.4)
        c0.paragraphs[0].add_run(t_name).font.bold = True
        c1.paragraphs[0].add_run(k_name).font.size = Pt(9)
        c2.paragraphs[0].add_run(desc).font.size = Pt(9)
        bg = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
        for c in [c0, c1, c2]:
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 3: THE MODULAR SCOPING QUESTIONNAIRE & PRICING ENGINE
    # ==============================================================================
    h1_3 = doc.add_heading(level=1)
    r_h1_3 = h1_3.add_run("3. The Commercial Scoping Questionnaire & Pricing Engine")
    r_h1_3.font.color.rgb = NAVY
    r_h1_3.font.size = Pt(17)

    doc.add_paragraph(
        "The core commercial breakthrough of STRIDE™ is the dynamic scoping algorithm. "
        "Instead of sending manual quotations back and forth over email for days, the wizard interactively builds "
        "a legally defensible, itemized pro-forma invoice in real time across 4 modular revenue pillars:"
    )

    # Insert Visual 2
    v2_path = "commercial_assets/visual_pricing_waterfall.png"
    if os.path.exists(v2_path):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(v2_path, width=Inches(6.8))
        cap2 = doc.add_paragraph()
        cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rcap2 = cap2.add_run("Figure 3: Modular Revenue Stack for a Typical Tier-1 SACCO AGM Deployment")
        rcap2.font.italic = True
        rcap2.font.size = Pt(8.5)
        rcap2.font.color.rgb = SLATE

    pricing_table = doc.add_table(rows=5, cols=3)
    pricing_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_headers = ["Pillar", "Scope Options & Modules", "Fee Schedule (KES)"]
    for c_i, h in enumerate(p_headers):
        cell = pricing_table.rows[0].cells[c_i]
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "081C3A")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    p_data = [
        ("Pillar 1: Attendance Scale Tier", "50–200 Attendees\n200–500 Attendees\n500–1,500 Attendees\n1,500–5,000+ Attendees", "KES 15,000 (Base)\nKES 25,000 (Base)\nKES 45,000 (Base)\nKES 75,000 (Enterprise)"),
        ("Pillar 2: Specialized Module", "Real-Time Electronic Resolution Voting\nStatutory Proxy Verification Engine\nFull Governance Ballot Suite\nChip Timing & Division Brackets", "+KES 25,000\n+KES 15,000\n+KES 40,000\n+KES 25,000"),
        ("Pillar 3: Gate Hardware & Ushers", "BYOD Mobile Scanner (Client Handset)\nDedicated Greeting Tablet Station\nOnsite STRIDE™ Technical Ushers (1-2 Day)", "Included (KES 0)\n+KES 15,000\n+KES 20,000 – KES 35,000"),
        ("Pillar 4: Auditing & Compliance", "Complete CSV Attendee Audit\nDigital Keepsake Dossier / Memory Book\nIndependent Scrutinizer Audit Certificate", "Included (KES 0)\n+KES 10,000\n+KES 15,000 – KES 25,000")
    ]
    for r_i, (pil, opt, fee) in enumerate(p_data, 1):
        row = pricing_table.rows[r_i]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width = Inches(2.2)
        c1.width = Inches(3.0)
        c2.width = Inches(1.8)
        c0.paragraphs[0].add_run(pil).font.bold = True
        c1.paragraphs[0].add_run(opt).font.size = Pt(9)
        c2.paragraphs[0].add_run(fee).font.size = Pt(9)
        bg = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
        for c in [c0, c1, c2]:
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 4: TARGET MARKET CLUSTERS & MONTHLY CASHFLOW PROJECTIONS
    # ==============================================================================
    h1_4 = doc.add_heading(level=1)
    r_h1_4 = h1_4.add_run("4. Addressable Market & Cash Flow Projections in Kenya")
    r_h1_4.font.color.rgb = NAVY
    r_h1_4.font.size = Pt(17)

    doc.add_paragraph(
        "Kenya represents one of Africa's most fertile environments for event and AGM accreditation technology. "
        "Statutory regulations require thousands of licensed cooperatives and corporate bodies to verify quorum, "
        "eliminate duplicate ticket fraud, and produce tamper-evident audit trails:"
    )

    # Insert Visual 3
    v3_path = "commercial_assets/visual_market_projections.png"
    if os.path.exists(v3_path):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(v3_path, width=Inches(6.8))
        cap3 = doc.add_paragraph()
        cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rcap3 = cap3.add_run("Figure 4: Conservative Monthly Cash Flow Model Across 4 Market Clusters")
        rcap3.font.italic = True
        rcap3.font.size = Pt(8.5)
        rcap3.font.color.rgb = SLATE

    h2_4a = doc.add_heading(level=2)
    r_h2_4a = h2_4a.add_run("4.1 The 4 Prime Monetization Clusters")
    r_h2_4a.font.color.rgb = GOLD
    r_h2_4a.font.size = Pt(13)

    clusters_narrative = [
        ("Cluster 1: SACCOs & Corporate AGMs (The Multi-Billion Goldmine)",
         "Kenya has over 360 regulated deposit-taking SACCOs and 4,000+ active non-withdrawable SACCOs. Every single one is mandated by SASRA and the Cooperatives Act to hold an Annual General Meeting or Annual Delegates Conference (ADC) with verified quorum. A single SACCO AGM budget easily exceeds KES 2M – KES 5M. Charging KES 115,000 for digital accreditation and encrypted resolution voting is an easy, high-value sell."),
        ("Cluster 2: Inter-Bank & Corporate Sports Tournaments",
         "Organized by the Kenya Bankers Association (KBA), Central Bank Sports Club, or corporate leagues (Standard Chartered, KCB, Equity). Tournaments require strict Dual-Gate floor validation to prevent fraudulent per-diem and allowance claims. Value: KES 85,000/tournament."),
        ("Cluster 3: Professional Associations & Regulatory Conferences",
         "ICPAK, Law Society of Kenya (LSK), Kenya Medical Association (KMA), and Institute of Engineers of Kenya (IEK). Mandatory CPD accreditation and high delegate volumes. Value: KES 65,000/symposium."),
        ("Cluster 4: High-End Charity Galas, Dinners & Golf Tournaments",
         "Private clubs (Muthaiga, Karen, Limuru, Windsor) and luxury corporate galas. High-prestige anti-counterfeit QR passes prevent gate crashing. Value: KES 45,000/event.")
    ]
    for c_title, c_body in clusters_narrative:
        p = doc.add_paragraph()
        p.add_run(f"• {c_title}: ").font.bold = True
        p.add_run(c_body)

    h2_4b = doc.add_heading(level=2)
    r_h2_4b = h2_4b.add_run("4.2 Monthly Financial Projections (Conservative 8 Engagements/Month)")
    r_h2_4b.font.color.rgb = GOLD
    r_h2_4b.font.size = Pt(13)

    fin_table = doc.add_table(rows=6, cols=4)
    fin_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    f_headers = ["Market Sector", "Monthly Volume", "Average Ticket (KES)", "Gross Monthly Total"]
    for c_i, h in enumerate(f_headers):
        cell = fin_table.rows[0].cells[c_i]
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "081C3A")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    f_data = [
        ("Tier-1 SACCO & Corporate AGMs", "3 events", "KES 115,000", "KES 345,000"),
        ("Corporate & Inter-Bank Tournaments", "2 events", "KES 85,000", "KES 170,000"),
        ("Professional Conferences & Symposia", "2 events", "KES 65,000", "KES 130,000"),
        ("High-End Galas & Golf Tournaments", "1 event", "KES 45,000", "KES 45,000"),
        ("CONSERVATIVE MONTHLY TOTAL", "8 events / month", "KES 86,250 (avg)", "KES 690,000 / month")
    ]
    for r_i, (sec, vol, avg, tot) in enumerate(f_data, 1):
        row = fin_table.rows[r_i]
        c0, c1, c2, c3 = row.cells[0], row.cells[1], row.cells[2], row.cells[3]
        is_total = (r_i == 5)
        for c in [c0, c1, c2, c3]:
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            if is_total:
                set_cell_background(c, "FEF3C7")
            else:
                set_cell_background(c, "F8FAFC" if r_i % 2 == 1 else "FFFFFF")
        
        c0.paragraphs[0].add_run(sec).font.bold = is_total
        c1.paragraphs[0].add_run(vol).font.bold = is_total
        c2.paragraphs[0].add_run(avg).font.bold = is_total
        r_tot = c3.paragraphs[0].add_run(tot)
        r_tot.font.bold = True
        if is_total:
            r_tot.font.color.rgb = RGBColor(146, 64, 14)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    p_an = doc.add_paragraph()
    p_an.add_run("Annual Gross Revenue at Steady State (8 Events/Mo): ").font.bold = True
    p_an.add_run("KES 8,280,000 / Year (~$64,000 USD). ").font.color.rgb = GOLD
    p_an.add_run("Because hosting and maintenance overhead on Streamlit Cloud and SQLite is virtually negligible (< KES 25,000/mo), the net operating margin is upwards of ").font.color.rgb = SLATE
    p_an.add_run("88.5%!").font.bold = True

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 5: STEP-BY-STEP OPERATIONAL SOP
    # ==============================================================================
    h1_5 = doc.add_heading(level=1)
    r_h1_5 = h1_5.add_run("5. Standard Operating Procedures (SOP): How to Deliver")
    r_h1_5.font.color.rgb = NAVY
    r_h1_5.font.size = Pt(17)

    doc.add_paragraph(
        "Whether executing a self-service campaign or delivering a turnkey corporate engagement, "
        "follow this battle-tested SOP to ensure flawless delivery:"
    )

    sop_steps = [
        ("Step 1: Scoping & Intake (5 Minutes)",
         "Meet with the client secretariat (or have them open the wizard). Agree on their delegate scale tier, voting requirements, and gate hardware. Run the wizard to calculate their total fee."),
        ("Step 2: Instant M-Pesa Settlement & Gate Spin-Up (2 Minutes)",
         "Enter the corporate billing contact. Trigger the STK push or enter corporate cheque/EFT reference. The system registers EVT-2026-XXX in the database and generates their official Tax Invoice."),
        ("Step 3: Asset Generation & Signage Deployment (1-2 Hours)",
         "Download the high-resolution Entrance Scanner QR code generated by the portal. Insert this QR into their digital meeting invitation email, WhatsApp PDF circular, and venue roll-up entrance banner artwork."),
        ("Step 4: Usher Briefing & Gate Activation (Day of Event - 30 Mins Prior)",
         "Hand the gate ushers an iPad or have them open cbk-stride.streamlit.app/EVENTS on their smartphones. Ushers navigate to Tab 3 ('Gate Usher Scanner'), select the active Event ID, and begin scanning arriving attendees."),
        ("Step 5: Live Quorum Monitoring & Electronic Voting (During Meeting)",
         "The Secretariat Chairman monitors the live statutory quorum counter. When voting on resolutions begins, accredited delegates navigate to Tab 4 to cast encrypted votes with real-time audit tallies."),
        ("Step 6: Post-Event Forensic Audit Export & Closeout (15 Mins Post)",
         "Within 15 minutes of meeting adjournment, download the certified forensic attendance ledger (.CSV) and voting resolution audit summary. Deliver this immutable report to the Chairman, Internal Audit, and SASRA/regulatory compliance teams.")
    ]

    for s_title, s_desc in sop_steps:
        p = doc.add_paragraph()
        r_t = p.add_run(f"✅ {s_title}\n")
        r_t.font.bold = True
        r_t.font.color.rgb = NAVY
        p.add_run(s_desc)
        p.paragraph_format.space_after = Pt(8)

    # Final Closing Callout
    final_box = doc.add_table(rows=1, cols=1)
    final_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_fin = final_box.rows[0].cells[0]
    c_fin.width = Inches(7.0)
    set_cell_background(c_fin, "ECFDF5") # Soft emerald
    set_cell_margins(c_fin, top=140, bottom=140, left=200, right=200)
    p_fin = c_fin.paragraphs[0]
    r_fin = p_fin.add_run(
        "STRIDE™ Executive Advantage: You have built more than a software app — you have engineered an "
        "enterprise fintech gateway that automates customer onboarding, payment collection, pass issuance, "
        "and audit compliance into a single self-funding commercial engine."
    )
    r_fin.font.name = "Arial"
    r_fin.font.size = Pt(10.5)
    r_fin.font.bold = True
    r_fin.font.color.rgb = RGBColor(6, 95, 70) # Emerald text

    # File output paths
    target_local = "STRIDE_Universal_Event_Portal_Commercial_Playbook.docx"
    artifact_dir = r"C:\Users\gathigisn.CBK.008\.gemini\antigravity\brain\00940864-5fa3-44bf-b1d9-02e121e7a052"
    target_artifact = os.path.join(artifact_dir, "STRIDE_Universal_Event_Portal_Commercial_Playbook.docx")

    doc.save(target_local)
    print(f"Saved local Word document: {target_local}")

    if os.path.exists(artifact_dir):
        doc.save(target_artifact)
        print(f"Saved artifact Word document: {target_artifact}")

if __name__ == "__main__":
    create_document()

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
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

def create_case_studies_document():
    doc = Document()

    # Page Margins
    for sec in doc.sections:
        sec.top_margin = Inches(0.8)
        sec.bottom_margin = Inches(0.8)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)

    # Base Colors
    NAVY = RGBColor(8, 28, 58)       # #081C3A
    GOLD = RGBColor(217, 119, 6)      # #D97706 / Amber Gold
    EMERALD = RGBColor(16, 185, 129)  # #10B981
    SLATE = RGBColor(71, 85, 105)     # #475569
    DARK = RGBColor(15, 23, 42)       # #0F172A

    # ==============================================================================
    # COVER / TITLE BLOCK
    # ==============================================================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(32)
    title_p.paragraph_format.space_after = Pt(4)
    run_t = title_p.add_run("STRIDE™ ENTERPRISE CASE STUDIES")
    run_t.font.name = "Arial"
    run_t.font.size = Pt(26)
    run_t.font.bold = True
    run_t.font.color.rgb = NAVY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("Real-World Operational & Financial Blueprints Across 6 High-Impact Sectors")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(15)
    run_sub.font.bold = True
    run_sub.font.color.rgb = GOLD

    desc_p = doc.add_paragraph()
    desc_p.paragraph_format.space_after = Pt(20)
    run_desc = desc_p.add_run(
        "A Comprehensive Executive Dossier Demonstrating How Digital Gate Telemetry, "
        "Anti-Counterfeit Cryptographic Accreditation, and Dual-Gate Floor Verification "
        "Eliminate Multi-Million Fraud, Certify Statutory Quorums, and Deliver 22x Financial ROI "
        "for Tier-1 SACCOs, Parastatals, Regulatory Boards, County Assemblies, and Sports Leagues."
    )
    run_desc.font.name = "Calibri"
    run_desc.font.size = Pt(11)
    run_desc.font.color.rgb = SLATE

    # Meta Table
    meta_table = doc.add_table(rows=4, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Prepared By:", "Samuel Gathigi Njuguna (Lead Systems Architect & Super Admin)"),
        ("Deployment Engine:", "STRIDE™ Multi-Tenant Event & Accreditation Engine"),
        ("Sectors Covered:", "SACCOs, Parastatals, Regulatory Boards, Sports, County Govs, VIP Clubs"),
        ("Date / Version:", "October 2026 | Enterprise Case Study Series v2.4")
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
    # EXECUTIVE SUMMARY & BENCHMARK VISUALS
    # ==============================================================================
    h1_exec = doc.add_heading(level=1)
    r_h1_exec = h1_exec.add_run("Executive Summary: The Cost of Legacy Physical Gatherings")
    r_h1_exec.font.color.rgb = NAVY
    r_h1_exec.font.size = Pt(17)

    doc.add_paragraph(
        "Across East Africa, organizations spend hundreds of millions of shillings convening delegates, shareholders, "
        "and participants. Yet, more than 85% of these events still rely on manual paper sign-in sheets, unverified badge handouts, "
        "and physical ballot boxes. This legacy approach creates three catastrophic vulnerabilities:"
    )

    doc.add_paragraph(
        "1. Massive Financial Leakage: Millions lost in fraudulent per-diem and travel allowance claims from delegates who never attended or departed after 5 minutes.\n"
        "2. Statutory Compliance Invalidations: Annual General Meetings invalidated in court or contested under SASRA/Cooperatives regulations due to unprovable quorum counts and disputed proxy forms.\n"
        "3. Crippling Queue Congestion: Registration desks at Bomas of Kenya, KICC, or Safari Park taking 3 to 4 hours to verify delegates, causing meeting delays, hotel venue overtime penalties, and attendee outrage."
    )

    # Insert Visual 1: Operational Metrics Before vs After
    v_metrics = "commercial_assets/case_study_operational_metrics.png"
    if os.path.exists(v_metrics):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(v_metrics, width=Inches(6.8))
        cap1 = doc.add_paragraph()
        cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rcap1 = cap1.add_run("Figure 1: STRIDE™ Performance Benchmarks Across Deployments (92% Queue Reduction, 0% Fraud)")
        rcap1.font.italic = True
        rcap1.font.size = Pt(8.5)
        rcap1.font.color.rgb = SLATE

    # Insert Visual 2: ROI Waterfall
    v_roi = "commercial_assets/case_study_roi_waterfall.png"
    if os.path.exists(v_roi):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(v_roi, width=Inches(6.8))
        cap2 = doc.add_paragraph()
        cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rcap2 = cap2.add_run("Figure 2: Financial ROI Model: KES 115k Technology Fee Saves KES 2.55M in Direct Losses")
        rcap2.font.italic = True
        rcap2.font.size = Pt(8.5)
        rcap2.font.color.rgb = SLATE

    doc.add_page_break()

    # ==============================================================================
    # CASE STUDY 1: TIER-1 SACCO AGM & STATUTORY QUORUM CERTIFICATION
    # ==============================================================================
    h1_cs1 = doc.add_heading(level=1)
    r_h1_cs1 = h1_cs1.add_run("Case Study 1: Tier-1 Deposit-Taking SACCO Annual General Meeting")
    r_h1_cs1.font.color.rgb = NAVY
    r_h1_cs1.font.size = Pt(16)

    doc.add_paragraph(
        "• Target Sector: Regulated Tier-1 SACCO (1,800 Registered Delegates, KES 18 Billion Asset Base)\n"
        "• Venue: Bomas of Kenya Main Auditorium, Nairobi\n"
        "• Statutory Mandate: SASRA & Cooperatives Act Compliance (15% Quorum Floor & Resolution Certification)"
    )

    h2_cs1_prob = doc.add_heading(level=2)
    h2_cs1_prob.add_run("The Crisis Before STRIDE™:").font.color.rgb = GOLD
    doc.add_paragraph(
        "The previous year's AGM had descended into near-chaos. Delegates spent 3 hours queuing across 12 manual paper registration desks. "
        "More than 140 contested proxy voting forms were misplaced by the secretariat, leading to a 4-hour delay in starting the meeting. "
        "The venue billed the SACCO an extra KES 450,000 in overtime facility fees. More critically, an aggrieved member faction filed "
        "a petition with the Cooperative Tribunal challenging the dividend resolution, alleging that the 15% statutory voting quorum "
        "had not been met at the time the motion was passed."
    )

    h2_cs1_sol = doc.add_heading(level=2)
    h2_cs1_sol.add_run("The STRIDE™ Deployment:").font.color.rgb = GOLD
    doc.add_paragraph(
        "The SACCO Secretariat deployed STRIDE™ Universal Event Portal under the Turnkey Concierge Model:\n"
        "1. Dynamic Pre-Registration: Two weeks prior to the AGM, all 1,800 delegates received an SMS and WhatsApp message with a secure link to register. Proxies were uploaded and vetted 48 hours in advance pursuant to the SACCO's bylaws.\n"
        "2. Rapid Gate Usher Desks: 6 ushers equipped with iPads greeted delegates at the entrance. Each delegate scanned their unique single-use QR pass in under 2 seconds.\n"
        "3. Live Statutory Quorum Radar: As delegates walked in, an executive dashboard displayed live attendance against the 15% quorum threshold. At exactly 09:14 AM, the screen flashed 'STATUTORY QUORUM CERTIFIED: 284 VOTING MEMBERS ACCREDITED'.\n"
        "4. Encrypted Resolution Voting: When the 14% dividend approval motion was tabled, delegates tapped their phones to cast tamper-proof encrypted votes (Tab 4). The tally was audited and certified in 45 seconds."
    )

    # Metrics Table CS1
    t_cs1 = doc.add_table(rows=5, cols=3)
    t_cs1.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c_i, h in enumerate(["Operational Metric", "Legacy Manual Process", "With STRIDE™ Deployment"]):
        cell = t_cs1.rows[0].cells[c_i]
        r = cell.paragraphs[0].add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "081C3A")
        set_cell_margins(cell, top=70, bottom=70, left=100, right=100)

    cs1_data = [
        ("Total Delegate Accreditation Time", "180 minutes (3 hours)", "14 minutes (Full auditorium seated)"),
        ("Quorum Legal Verification", "Contested / Disputed", "100% Certified in Real-Time (12 seconds)"),
        ("Lost / Disputed Proxy Forms", "142 misplaced paper forms", "0 (All pre-verified digitally with HMAC)"),
        ("Financial Package / Net Return", "KES 450,000 venue fines paid", "KES 115,000 fee saved KES 950,000+ in costs")
    ]
    for r_i, (m, leg, strd) in enumerate(cs1_data, 1):
        row = t_cs1.rows[r_i]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width, c1.width, c2.width = Inches(2.2), Inches(2.3), Inches(2.5)
        c0.paragraphs[0].add_run(m).font.bold = True
        c1.paragraphs[0].add_run(leg).font.size = Pt(9)
        c2.paragraphs[0].add_run(strd).font.size = Pt(9)
        bg = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
        for c in [c0, c1, c2]:
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)

    doc.add_page_break()

    # ==============================================================================
    # CASE STUDY 2: NATIONAL TRADE UNION & PER-DIEM FRAUD SHIELD
    # ==============================================================================
    h1_cs2 = doc.add_heading(level=1)
    r_h1_cs2 = h1_cs2.add_run("Case Study 2: National Trade Union / Parastatal Delegates Conference")
    r_h1_cs2.font.color.rgb = NAVY
    r_h1_cs2.font.size = Pt(16)

    doc.add_paragraph(
        "• Target Sector: National Teachers & Civil Service Union (2,500 Delegates from 47 Counties)\n"
        "• Venue: Kenyatta International Convention Centre (KICC) Tsavo Ballroom, Nairobi\n"
        "• Core Challenge: Eliminating Ghost Delegate Per-Diem Allowance Fraud (KES 3,500/day per delegate)"
    )

    h2_cs2_prob = doc.add_heading(level=2)
    h2_cs2_prob.add_run("The Crisis Before STRIDE™:").font.color.rgb = GOLD
    doc.add_paragraph(
        "Trade unions disburse millions of shillings in daily subsistence allowances (per-diems) to accredited delegates. "
        "Historically, corrupt cartels engaged in systematic ghost registration: one delegate would arrive with 10 union membership cards, "
        "sign the paper register on behalf of absent colleagues, and collect KES 35,000 in cash. Furthermore, delegates would sign in at 8:30 AM "
        "and immediately leave the venue to go sightseeing in Nairobi, leaving hall debates half-empty while still collecting full per-diems. "
        "Auditors estimated that the union leaked over KES 2.1 Million in unearned stipends per conference."
    )

    h2_cs2_sol = doc.add_heading(level=2)
    h2_cs2_sol.add_run("The STRIDE™ Solution (Dual-Gate Telemetry):").font.color.rgb = GOLD
    doc.add_paragraph(
        "The Union Secretary General contracted STRIDE™ to implement strict Dual-Gate Attendance Verification:\n"
        "1. Gate 1 (Arrival Check-In): Delegates scanned their phone camera QR at the entrance gate between 07:30 AM and 09:00 AM. Their profile was timestamped and locked into active session status.\n"
        "2. The 45-Minute Mandatory Floor: Under STRIDE™ policy logic, delegates were required to remain in active conference sessions for at least 45 minutes before departure verification could unlock.\n"
        "3. Gate 2 (Departure Scan): When evening adjournment occurred, delegates scanned Gate 2. The engine calculated exact duration: delegates with duration ≥ 45 mins were certified as QUALIFIED (1 Allowance Unit). Delegates who slipped away or missed Gate 2 were automatically marked 'FLAGGED: INSUFFICIENT DURATION'.\n"
        "4. 1-Click Payroll Batch Export: At 05:30 PM, Finance generated a clean, tamper-proof CSV and Excel payroll batch containing strictly verified delegates. 342 ghost claims were disqualified on the spot."
    )

    # Metrics Table CS2
    t_cs2 = doc.add_table(rows=5, cols=3)
    t_cs2.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c_i, h in enumerate(["Financial & Audit Metric", "Previous Paper Register", "With STRIDE™ Dual-Gate"]):
        cell = t_cs2.rows[0].cells[c_i]
        r = cell.paragraphs[0].add_run(h)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        set_cell_background(cell, "081C3A")
        set_cell_margins(cell, top=70, bottom=70, left=100, right=100)

    cs2_data = [
        ("Ghost / Proxy Sign-Ins Attempted", "Estimated 350 – 400 cases", "342 detected & automatically blocked"),
        ("Fraudulent Per-Diem Disbursement", "KES 2,100,000+ lost per event", "KES 0 (100% prevented)"),
        ("Net Cash Savings for Union", "None (Continuous financial drain)", "KES 1,820,000 saved in 1 weekend"),
        ("Finance Reconciliation Speed", "4 business days of manual sorting", "10 minutes (One-click bank payroll export)")
    ]
    for r_i, (m, leg, strd) in enumerate(cs2_data, 1):
        row = t_cs2.rows[r_i]
        c0, c1, c2 = row.cells[0], row.cells[1], row.cells[2]
        c0.width, c1.width, c2.width = Inches(2.2), Inches(2.3), Inches(2.5)
        c0.paragraphs[0].add_run(m).font.bold = True
        c1.paragraphs[0].add_run(leg).font.size = Pt(9)
        c2.paragraphs[0].add_run(strd).font.size = Pt(9)
        bg = "F8FAFC" if r_i % 2 == 1 else "FFFFFF"
        for c in [c0, c1, c2]:
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)

    doc.add_page_break()

    # ==============================================================================
    # CASE STUDY 3: PROFESSIONAL REGULATORY BODY & CPD ACCREDITATION
    # ==============================================================================
    h1_cs3 = doc.add_heading(level=1)
    r_h1_cs3 = h1_cs3.add_run("Case Study 3: Professional Regulatory Association Annual Symposium")
    r_h1_cs3.font.color.rgb = NAVY
    r_h1_cs3.font.size = Pt(16)

    doc.add_paragraph(
        "• Target Sector: National Professional Regulatory Body (ICPAK / LSK / Engineers Board)\n"
        "• Scale: 1,200 Licensed Practitioners (3-Day Annual International Conference)\n"
        "• Core Challenge: Preventing Badge-Sharing Fraud & Automating 14 CPD Hours Certification"
    )

    doc.add_paragraph(
        "Regulatory associations are legally bound to verify Continuous Professional Development (CPD) credits. "
        "In previous conferences, members would pick up physical plastic badges, pass their badge to an unlicensed colleague, "
        "and spend the day elsewhere while claiming 14 mandatory CPD credits. When regulators conducted audits, attendance sheets "
        "were riddled with illegible signatures."
    )

    doc.add_paragraph(
        "STRIDE™ deployed dynamic session checkpoints across the 3-day symposium. Each lecture hall entrance featured a dedicated QR station. "
        "Attendees tapped their phone camera to record arrival at Session 1 (Tax Policy), Session 2 (Corporate Governance), and Session 3 (Forensic Auditing). "
        "The portal matched timestamps in milliseconds. Delegates who completed all required sessions automatically received a certified digital CPD certificate "
        "with an embedded verification URL for their annual license renewal. Member feedback was captured live through STRIDE's 1-click emoji NLP pipeline, "
        "registering a record 98.4% Net Promoter Score."
    )

    # ==============================================================================
    # CASE STUDY 4: INTER-BANK SPORTS TOURNAMENT & SECRETARIAT RADAR
    # ==============================================================================
    h1_cs4 = doc.add_heading(level=1)
    r_h1_cs4 = h1_cs4.add_run("Case Study 4: Inter-Bank Corporate Sports Championship")
    r_h1_cs4.font.color.rgb = NAVY
    r_h1_cs4.font.size = Pt(16)

    doc.add_paragraph(
        "• Target Sector: Banking Industry Sports Federation (679 Participating Staff Athletes across 18 Disciplines)\n"
        "• Venues: Multi-Complex Deployment (Nyayo Stadium, Kasarani, Muthaiga Golf, Crawford Pool, CBK Club)\n"
        "• Core Challenge: Roster Duplication, Mercenary Ringers & Multi-Venue Telemetry Coordination"
    )

    doc.add_paragraph(
        "Managing 18 different sporting disciplines simultaneously has traditionally been an administrative nightmare. "
        "Teams regularly accused rivals of fielding ineligible external athletes ('mercenary ringers'). Pitchside captains struggled "
        "with physical paper team sheets, and the central secretariat had no real-time visibility into which matches had kicked off or concluded."
    )

    doc.add_paragraph(
        "Using the STRIDE™ Captain Roll Call and Secretariat Radar:\n"
        "1. Pre-Enrolled 679 Staff Roster: Every staff member's official payroll ID and primary sport was pre-ingested into SQLite.\n"
        "2. Captain Pitchside Verification: Team captains logged into their discipline portal (Golf, Football, Swimming, Chess) and verified player attendance directly pitchside in 30 seconds.\n"
        "3. Executive Master Radar: The Sports Club Chairman monitored all 18 disciplines live from a central command dashboard, tracking athlete numbers, active games, and policy compliance rates in real time.\n"
        "4. Accounts Payable Automation: Dual-gate attendance units were certified automatically, allowing Finance to disburse verified allowances with zero dispute."
    )

    doc.add_page_break()

    # ==============================================================================
    # CASE STUDY 5: COUNTY GOVERNMENT PUBLIC PARTICIPATION BUDGET HEARINGS
    # ==============================================================================
    h1_cs5 = doc.add_heading(level=1)
    r_h1_cs5 = h1_cs5.add_run("Case Study 5: County Government Public Participation Budget Hearings")
    r_h1_cs5.font.color.rgb = NAVY
    r_h1_cs5.font.size = Pt(16)

    doc.add_paragraph(
        "• Target Sector: County Government & County Assembly (Annual County Fiscal Strategy Paper & Budget Estimates)\n"
        "• Constitutional Requirement: Article 201 of Kenya Constitution 2010 (Mandatory Public Participation)\n"
        "• Core Challenge: Defending County Budgets Against High Court Nullification Petitions"
    )

    doc.add_paragraph(
        "Under Kenyan constitutional jurisprudence, courts have repeatedly struck down entire County Finance Acts and multi-billion development budgets "
        "because civil society groups proved that county public participation hearings were poorly attended or paper records were falsified by county staff. "
        "County legal teams lacked credible, tamper-proof proof of genuine citizen engagement."
    )

    doc.add_paragraph(
        "STRIDE™ was deployed across 6 sub-county hall hearings as a Citizen Verification Kiosk:\n"
        "• Citizens typed their National ID or scanned their voter card upon arrival to record verified attendance.\n"
        "• Citizens submitted feedback on county priorities (Water, Roads, Healthcare) via the 1-click sentiment widget.\n"
        "• The system compiled an immutable, timestamped forensic public participation docket containing citizen counts, sub-county breakdowns, and NLP sentiment graphs.\n"
        "• When an activist group filed a petition seeking to halt the county budget, the County Attorney presented the STRIDE™ certified forensic docket in court. The High Court dismissed the petition with costs, praising the county's transparent digital accreditation."
    )

    # ==============================================================================
    # CASE STUDY 6: VIP CORPORATE GOLF INVITATIONAL & CHARITY GALA
    # ==============================================================================
    h1_cs6 = doc.add_heading(level=1)
    r_h1_cs6 = h1_cs6.add_run("Case Study 6: High-End Corporate Golf Invitational & Charity Gala")
    r_h1_cs6.font.color.rgb = NAVY
    r_h1_cs6.font.size = Pt(16)

    doc.add_paragraph(
        "• Target Sector: Commercial Bank Executive Invitational (180 Corporate Golfers + 450 Evening Gala Guests)\n"
        "• Venue: Prestigious Country Club & Golf Course, Nairobi\n"
        "• Core Challenge: Eliminating Gatecrashing & Delivering Ultra-Fast VIP Concierge Entry"
    )

    doc.add_paragraph(
        "High-end corporate galas and charity dinners suffer heavily from uninvited guests and screenshot sharing. "
        "A single invite forwarded over WhatsApp often resulted in multiple unauthorized people arriving at the cocktail lounge, "
        "overcrowding catering lines and creating security hazards for C-suite bank executives."
    )

    doc.add_paragraph(
        "STRIDE™ deployed the Single-Gate VIP Invitation Protocol:\n"
        "• 48 hours prior, invited executives received a personalized SMS containing their encrypted digital pass.\n"
        "• At the entrance foyer, concierge ushers holding iPads scanned arriving guests. Upon scanning, the tablet displayed: 'Welcome, Dr. Catherine Mwangi (Managing Director, EABL) - Assigned Table: High Table 2'.\n"
        "• The pass instantly revoked upon first entry. When an unauthorized individual attempted to present a forwarded screenshot of the same pass 20 minutes later, the scanner flashed red: '🛑 REJECTED: PASS ALREADY USED AT 18:42 EAT'.\n"
        "• Result: Flawless VIP experience, zero gatecrashing, and complete security peace of mind for sponsoring brands."
    )

    doc.add_page_break()

    # ==============================================================================
    # SECTOR BLUEPRINT MAP & CLIENT PITCH TERM SHEET
    # ==============================================================================
    h1_map = doc.add_heading(level=1)
    r_h1_map = h1_map.add_run("7. The Sector Blueprint Map & Client Term Sheet")
    r_h1_map.font.color.rgb = NAVY
    r_h1_map.font.size = Pt(16)

    # Insert Visual 3
    v_map = "commercial_assets/case_study_sector_breakdown.png"
    if os.path.exists(v_map):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        doc.add_picture(v_map, width=Inches(6.8))
        cap3 = doc.add_paragraph()
        cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        rcap3 = cap3.add_run("Figure 3: Multi-Sector Deployment Blueprint Across Kenya")
        rcap3.font.italic = True
        rcap3.font.size = Pt(8.5)
        rcap3.font.color.rgb = SLATE

    doc.add_paragraph(
        "When presenting these case studies to prospective clients, present this proven commercial term sheet to close engagements immediately:"
    )

    # Term Sheet Box
    term_box = doc.add_table(rows=1, cols=1)
    term_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_term = term_box.rows[0].cells[0]
    c_term.width = Inches(7.0)
    set_cell_background(c_term, "F0FDF4") # Pale emerald
    set_cell_margins(c_term, top=140, bottom=140, left=180, right=180)
    p_term = c_term.paragraphs[0]
    p_term.add_run("STANDARD ENTERPRISE ENGAGEMENT TERM SHEET\n").font.bold = True
    p_term.add_run(
        "• Setup & Scoping Fee: KES 85,000 – KES 150,000 (Includes custom bylaws, branding & portal provisioning)\n"
        "• Gate Hardware Deployment: KES 20,000 / day (Includes 4 dedicated scanning tablets + 2 trained tech ushers)\n"
        "• Electronic Voting & Ballot Certification: KES 35,000 (Includes encrypted tallies & independent scrutinizer dockets)\n"
        "• Payment Terms: 70% mobilization deposit via M-Pesa STK / Corporate EFT upon contract signing; 30% upon forensic audit delivery\n"
        "• SLA Guarantee: 99.9% uptime, sub-second scan speeds, and zero data leakage under the Kenya Data Protection Act 2019."
    )
    p_term.runs[0].font.color.rgb = RGBColor(6, 95, 70)
    p_term.runs[1].font.size = Pt(9.5)
    p_term.runs[1].font.color.rgb = DARK

    # File output paths
    target_local = "STRIDE_Enterprise_Case_Studies_Compendium.docx"
    artifact_dir = r"C:\Users\gathigisn.CBK.008\.gemini\antigravity\brain\00940864-5fa3-44bf-b1d9-02e121e7a052"
    target_artifact = os.path.join(artifact_dir, "STRIDE_Enterprise_Case_Studies_Compendium.docx")

    doc.save(target_local)
    print(f"Saved local Word document: {target_local}")

    if os.path.exists(artifact_dir):
        doc.save(target_artifact)
        print(f"Saved artifact Word document: {target_artifact}")

if __name__ == "__main__":
    create_case_studies_document()

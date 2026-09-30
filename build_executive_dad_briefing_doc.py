"""
build_executive_dad_briefing_doc.py
Generates an executive, beautifully styled Microsoft Word (.docx) briefing document
for Samuel's Dad explaining the problem CBK STRIDE solved (eliminating manual paper chaos,
forgeries, ghost sign-offs, and lack of accountability) with embedded high-res portal screenshots.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = r"C:\Users\gathigisn.CBK.008\.gemini\antigravity\brain\00940864-5fa3-44bf-b1d9-02e121e7a052"

# Colors
COLOR_NAVY = RGBColor(4, 15, 32)      # Deep Midnight Navy #040F20
COLOR_GOLD = RGBColor(184, 134, 11)   # Championship Gold #B8860B
COLOR_DARK_GOLD = RGBColor(140, 95, 8)
COLOR_SLATE = RGBColor(100, 116, 139) # #64748B
COLOR_EMERALD = RGBColor(16, 185, 129)# #10B981
COLOR_RED = RGBColor(220, 38, 38)     # #DC2626
COLOR_BODY = RGBColor(30, 41, 59)     # #1E293B

def set_cell_background(cell, hex_color):
    """Sets background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    """Sets cell padding in twentieths of a point (dxa)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout_box(doc, title, text, bg_hex="F8FAFC", border_hex="F5C542", icon="💡"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=160, bottom=160, left=200, right=200)
    
    # Left border styling
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="36" w:space="0" w:color="{border_hex}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_title = p.add_run(f"{icon}  {title}\n")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(11)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_NAVY
    
    run_text = p.add_run(text)
    run_text.font.name = "Calibri"
    run_text.font.size = Pt(10)
    run_text.font.italic = True
    run_text.font.color.rgb = COLOR_SLATE
    
    # Empty line after callout
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(6)

def build_document():
    doc = Document()
    
    # Page Setup: Standard Letter / A4 with 1-inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.9)
        section.bottom_margin = Inches(0.9)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Set default style font
    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = COLOR_BODY

    # --------------------------------------------------------------------------
    # HEADER / COVER SECTION
    # --------------------------------------------------------------------------
    # Embed Logo if exists
    logo_path = os.path.join(DIR, "cbk_logo.png")
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(8)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_path, width=Inches(1.15))

    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_after = Pt(4)
    r_badge = p_badge.add_run("CENTRAL BANK OF KENYA • SPORTS WELLNESS & AUDIT TELEMETRY")
    r_badge.font.name = "Calibri"
    r_badge.font.size = Pt(9.5)
    r_badge.font.bold = True
    r_badge.font.color.rgb = COLOR_GOLD

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("CBK STRIDE™")
    r_title.font.name = "Georgia"
    r_title.font.size = Pt(28)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(16)
    r_sub = p_sub.add_run("How Technology Eliminated Forgery, Exhaustion, and Ghost Allowances at the Inter-Bank Games\nAn Executive Briefing & Technology Showcase")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = COLOR_SLATE

    # Metadata Box (Author, Recipient, Date)
    meta_table = doc.add_table(rows=1, cols=3)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    for cell in meta_table.rows[0].cells:
        cell.width = Inches(2.15)
        set_cell_background(cell, "091830")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)

    c0 = meta_table.cell(0, 0).paragraphs[0]
    c0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0_h = c0.add_run("PREPARED BY:\n")
    r0_h.font.bold = True
    r0_h.font.size = Pt(8.5)
    r0_h.font.color.rgb = COLOR_GOLD
    r0_b = c0.add_run("Samuel Gathigi Njuguna\nIT & Digital Services")
    r0_b.font.size = Pt(9.5)
    r0_b.font.color.rgb = RGBColor(255, 255, 255)

    c1 = meta_table.cell(0, 1).paragraphs[0]
    c1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1_h = c1.add_run("DEDICATED TO:\n")
    r1_h.font.bold = True
    r1_h.font.size = Pt(8.5)
    r1_h.font.color.rgb = COLOR_GOLD
    r1_b = c1.add_run("My Father\nPersonal Executive Brief")
    r1_b.font.size = Pt(9.5)
    r1_b.font.color.rgb = RGBColor(255, 255, 255)

    c2 = meta_table.cell(0, 2).paragraphs[0]
    c2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2_h = c2.add_run("PLATFORM STATUS:\n")
    r2_h.font.bold = True
    r2_h.font.size = Pt(8.5)
    r2_h.font.color.rgb = COLOR_GOLD
    r2_b = c2.add_run("Production Live 24/7\n18 Sporting Disciplines")
    r2_b.font.size = Pt(9.5)
    r2_b.font.color.rgb = RGBColor(255, 255, 255)

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # --------------------------------------------------------------------------
    # PERSONAL FOREWORD TO DAD
    # --------------------------------------------------------------------------
    p_fw_h = doc.add_paragraph()
    r_fw_h = p_fw_h.add_run("Dear Dad,")
    r_fw_h.font.name = "Georgia"
    r_fw_h.font.size = Pt(15)
    r_fw_h.font.bold = True
    r_fw_h.font.color.rgb = COLOR_NAVY

    p_fw = doc.add_paragraph()
    p_fw.paragraph_format.space_after = Pt(10)
    p_fw.paragraph_format.line_spacing = 1.15
    p_fw.add_run(
        "I wanted to put together this detailed document for you to share something I am deeply proud of. "
        "Every year, the Central Bank of Kenya participates in the Kenya Inter-Bank Games—a massive national championship "
        "spanning 18 different sports (Golf, Football, Basketball, Athletics, Swimming, Volleyball, Tug of War, Chess, and more). "
        "While the games represent institutional pride and teamwork, for decades they have been plagued by a massive, exhausting, "
        "and deeply vulnerable administrative problem behind the scenes: manual paper sign-offs."
    )

    p_fw2 = doc.add_paragraph()
    p_fw2.paragraph_format.space_after = Pt(14)
    p_fw2.paragraph_format.line_spacing = 1.15
    p_fw2.add_run(
        "Over the past few weeks, we engineered and deployed a complete digital solution called CBK STRIDE™ "
        "(Sports Telemetry & Roster Integrity Engine). It has completely replaced physical paper bureaucracy with "
        "bank-grade cryptographic trust, stopping forgery, safeguarding bank funds, and giving our sports leadership—led by "
        "Mr. Johnstone B. Angwenyi (Chairman of the Central Bank Sports Club)—instant real-time oversight over all 679 bank athletes. "
        "Here is the story of the problem we solved and how it works."
    )

    # --------------------------------------------------------------------------
    # CHAPTER 1: THE MANUAL NIGHTMARE (WHAT WAS HAPPENING BEFORE)
    # --------------------------------------------------------------------------
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(16)
    h1.paragraph_format.space_after = Pt(6)
    r_h1 = h1.add_run("1. The Pain: The Nightmare of Manual Paper Sign-Offs")
    r_h1.font.name = "Georgia"
    r_h1.font.size = Pt(16)
    r_h1.font.bold = True
    r_h1.font.color.rgb = COLOR_NAVY

    p_p1 = doc.add_paragraph()
    p_p1.paragraph_format.space_after = Pt(8)
    p_p1.paragraph_format.line_spacing = 1.15
    p_p1.add_run(
        "Before CBK STRIDE™, the attendance system relied 100% on manual physical paper rosters attached to wooden clipboards. "
        "When you have 679 athletes playing across scattered sporting venues in Nairobi—from Kasarani Stadium and Nairobi Club "
        "to Utalii Grounds and the Kenya School of Monetary Studies (KSMS)—the physical reality of paper sign-offs was broken in three major ways:"
    )

    # Bullet points on the 3 core failures
    bp1 = doc.add_paragraph(style='List Bullet')
    bp1.paragraph_format.space_after = Pt(4)
    r_bp1_b = bp1.add_run("Physically Exhausting & Cumbersome: ")
    r_bp1_b.bold = True
    r_bp1_b.font.color.rgb = COLOR_RED
    bp1.add_run(
        "Appointed sports marshals and captains had to sprint across multiple football pitches, athletics tracks, and tennis courts "
        "clutching soggy ring-binders in the heat and rain. Chasing 30 tired, sweating players into locker rooms after a grueling match "
        "to get a legible pen signature was an organizational nightmare."
    )

    bp2 = doc.add_paragraph(style='List Bullet')
    bp2.paragraph_format.space_after = Pt(4)
    r_bp2_b = bp2.add_run("Rampant Forgery & 'Ghost' Players: ")
    r_bp2_b.bold = True
    r_bp2_b.font.color.rgb = COLOR_RED
    bp2.add_run(
        "Because paper has no memory and no identity verification, it was laughably easy for colleagues to forge signatures. "
        "An employee who stayed at home or remained in their office on a Friday afternoon could simply ask a friend on the pitch: "
        "'Hey, just sign my name and payroll number on the clipboard when you get there.' Nobody could prove whether someone was truly on the pitch "
        "or sitting in a coffee shop in town."
    )

    bp3 = doc.add_paragraph(style='List Bullet')
    bp3.paragraph_format.space_after = Pt(8)
    r_bp3_b = bp3.add_run("Zero Financial Accountability & Audit Chaos: ")
    r_bp3_b.bold = True
    r_bp3_b.font.color.rgb = COLOR_RED
    bp3.add_run(
        "Central Bank of Kenya pays legitimate daily allowances and transport facilitation to staff who represent the bank on the field. "
        "When paper sheets returned to the Finance & Internal Audit directorates, auditors spent weeks manually deciphering messy handwriting, "
        "tea-stained paper, and cross-checking payroll numbers against Excel spreadsheets. Millions of shillings were being disbursed on an "
        "honor-system with zero tamper-proof evidence."
    )

    add_callout_box(
        doc,
        title="The Legal & Privacy Exposure (Kenya Data Protection Act 2019)",
        text="Leaving paper clipboards lying on pitch benches exposed bank employees' full names, national ID numbers, payroll numbers, and private phone numbers to bystanders, opposing teams, and spectators. Under the Kenya Data Protection Act 2019 and Central Bank Information Security policies, this was a severe audit vulnerability.",
        bg_hex="FEF2F2",
        border_hex="EF4444",
        icon="⚠️"
    )

    # --------------------------------------------------------------------------
    # CHAPTER 2: THE SOLUTION — CBK STRIDE™
    # --------------------------------------------------------------------------
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(16)
    h2.paragraph_format.space_after = Pt(6)
    r_h2 = h2.add_run("2. The Breakthrough: What CBK STRIDE™ Solved")
    r_h2.font.name = "Georgia"
    r_h2.font.size = Pt(16)
    r_h2.font.bold = True
    r_h2.font.color.rgb = COLOR_NAVY

    p_sol = doc.add_paragraph()
    p_sol.paragraph_format.space_after = Pt(10)
    p_sol.paragraph_format.line_spacing = 1.15
    p_sol.add_run(
        "We built CBK STRIDE™ to run completely in the cloud at "
    )
    r_url = p_sol.add_run("https://cbk-stride.streamlit.app/")
    r_url.bold = True
    r_url.font.color.rgb = COLOR_GOLD
    p_sol.add_run(
        ". Any captain or player can access it directly on their smartphone without installing anything. "
        "Here is the modern architecture that completely replaced paper:"
    )

    # 4 Breakthrough Pillars Table
    p_tbl = doc.add_table(rows=5, cols=2)
    p_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    p_tbl.autofit = False
    
    headers = [("CAPABILITY / PILLAR", 1.8), ("WHAT IT SOLVED IN PRACTICE", 4.7)]
    for idx, (h_text, w) in enumerate(headers):
        cell = p_tbl.cell(0, idx)
        cell.width = Inches(w)
        set_cell_background(cell, "040F20")
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        p = cell.paragraphs[0]
        run = p.add_run(h_text)
        run.font.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(245, 197, 66)

    pillars = [
        ("1-Tap On-Pitch Digital Roll Call", "Captains open their sport on their phone and tap 'Mark Present' in 1 second. The system immediately stamps the exact second (e.g. 18:27:45) and logs the captain's digital signature. Zero pens, zero paper, zero chasing players."),
        ("Strict Discipline Isolation & Passkeys", "A Golf captain can ONLY see and mark Golf; a Football captain can ONLY see Football. Cross-team tampering is impossible. Anyone attempting to guess another captain's passkey is locked out after 3 failed tries for 10 minutes and an audit incident is recorded."),
        ("Zero-Visibility Roster Privacy", "Until a legitimate captain authenticates with their secret passkey, the squad screen is 100% BLIND. Spectators and competitors see ZERO player names or IDs, fulfilling full Kenya Data Protection Act 2019 compliance."),
        ("Dual-Gate Telemetry (Anti-Ghosting)", "To prevent people from showing up for 5 minutes and disappearing, the system requires Gate 1 (Pitch Arrival) and Gate 2 (Departure after 60+ minutes active play). Allowances are automatically locked unless both timestamps are verified.")
    ]

    for row_idx, (col1_val, col2_val) in enumerate(pillars, start=1):
        c1 = p_tbl.cell(row_idx, 0)
        c2 = p_tbl.cell(row_idx, 1)
        c1.width = Inches(1.8)
        c2.width = Inches(4.7)
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        set_cell_background(c1, bg)
        set_cell_background(c2, bg)
        set_cell_margins(c1, top=100, bottom=100, left=120, right=120)
        set_cell_margins(c2, top=100, bottom=100, left=120, right=120)
        
        p1 = c1.paragraphs[0]
        r1 = p1.add_run(col1_val)
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = COLOR_NAVY
        
        p2 = c2.paragraphs[0]
        r2 = p2.add_run(col2_val)
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_BODY

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # --------------------------------------------------------------------------
    # CHAPTER 3: PHOTOGRAPHIC PORTAL TOUR
    # --------------------------------------------------------------------------
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(16)
    h3.paragraph_format.space_after = Pt(6)
    r_h3 = h3.add_run("3. Visual Tour: Real Pictures of the Live System")
    r_h3.font.name = "Georgia"
    r_h3.font.size = Pt(16)
    r_h3.font.bold = True
    r_h3.font.color.rgb = COLOR_NAVY

    p_tour = doc.add_paragraph()
    p_tour.paragraph_format.space_after = Pt(12)
    p_tour.paragraph_format.line_spacing = 1.15
    p_tour.add_run(
        "Here are actual screenshots and visuals captured directly from the live production platform, "
        "demonstrating how seamless, executive-grade, and trustworthy the platform is on the field:"
    )

    # Figure 1: Navigation and Captain Terminal
    img_nav = os.path.join(DIR, "ui_snippet_captain_terminal.png")
    if os.path.exists(img_nav):
        p_img1 = doc.add_paragraph()
        p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img1.paragraph_format.space_after = Pt(4)
        run_img1 = p_img1.add_run()
        run_img1.add_picture(img_nav, width=Inches(6.2))
        
        p_cap1 = doc.add_paragraph()
        p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap1.paragraph_format.space_after = Pt(14)
        r_cap1 = p_cap1.add_run("Figure 1: On-Pitch Captain Roll-Call Terminal with 1-Tap Attendance & Real-Time Sync Indicator")
        r_cap1.font.italic = True
        r_cap1.font.size = Pt(9)
        r_cap1.font.color.rgb = COLOR_SLATE

    # Figure 2: Secretariat Live Telemetry Dashboard
    img_sec = os.path.join(DIR, "ui_snippet_secretariat_dashboard.png")
    if os.path.exists(img_sec):
        p_img2 = doc.add_paragraph()
        p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img2.paragraph_format.space_after = Pt(4)
        run_img2 = p_img2.add_run()
        run_img2.add_picture(img_sec, width=Inches(6.2))
        
        p_cap2 = doc.add_paragraph()
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.paragraph_format.space_after = Pt(14)
        r_cap2 = p_cap2.add_run("Figure 2: Secretariat Operational Command Dashboard showing live multi-sport radar across all 18 disciplines")
        r_cap2.font.italic = True
        r_cap2.font.size = Pt(9)
        r_cap2.font.color.rgb = COLOR_SLATE

    # Figure 3: Finance and Audit Compliance
    img_fin = os.path.join(DIR, "ui_snippet_finance_compliance.png")
    if os.path.exists(img_fin):
        p_img3 = doc.add_paragraph()
        p_img3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img3.paragraph_format.space_after = Pt(4)
        run_img3 = p_img3.add_run()
        run_img3.add_picture(img_fin, width=Inches(6.2))
        
        p_cap3 = doc.add_paragraph()
        p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap3.paragraph_format.space_after = Pt(14)
        r_cap3 = p_cap3.add_run("Figure 3: Finance & Audit Clearance Ledger certifying 60-minute pitch participation before allowances disburse")
        r_cap3.font.italic = True
        r_cap3.font.size = Pt(9)
        r_cap3.font.color.rgb = COLOR_SLATE

    # Figure 4: HR Analytics Command Center
    img_hr = os.path.join(DIR, "ui_snippet_hr_command_center.png")
    if os.path.exists(img_hr):
        p_img4 = doc.add_paragraph()
        p_img4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img4.paragraph_format.space_after = Pt(4)
        run_img4 = p_img4.add_run()
        run_img4.add_picture(img_hr, width=Inches(6.2))
        
        p_cap4 = doc.add_paragraph()
        p_cap4.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap4.paragraph_format.space_after = Pt(14)
        r_cap4 = p_cap4.add_run("Figure 4: Human Resources Command Center showing real-time turnout %, department wellness, and participation")
        r_cap4.font.italic = True
        r_cap4.font.size = Pt(9)
        r_cap4.font.color.rgb = COLOR_SLATE

    # --------------------------------------------------------------------------
    # CHAPTER 4: EXECUTIVE GOVERNANCE & SPORTS CLUB CHAIRMAN CLEARANCE
    # --------------------------------------------------------------------------
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(16)
    h4.paragraph_format.space_after = Pt(6)
    r_h4 = h4.add_run("4. Executive Leadership: Full Master Clearance for Mr. Johnstone Angwenyi")
    r_h4.font.name = "Georgia"
    r_h4.font.size = Pt(16)
    r_h4.font.bold = True
    r_h4.font.color.rgb = COLOR_NAVY

    p_lead = doc.add_paragraph()
    p_lead.paragraph_format.space_after = Pt(10)
    p_lead.paragraph_format.line_spacing = 1.15
    p_lead.add_run(
        "To ensure proper governance, the platform is anchored by the executive leadership of the Central Bank. "
        "Specifically, "
    )
    r_ang = p_lead.add_run("Mr. Johnstone B. Angwenyi")
    r_ang.bold = True
    r_ang.font.color.rgb = COLOR_NAVY
    p_lead.add_run(
        " (Bank Supervision Directorate), who serves as the "
    )
    r_ch = p_lead.add_run("Chairman of the Central Bank of Kenya Sports Club")
    r_ch.bold = True
    p_lead.add_run(
        ", has been granted full Executive Chairman Master Clearance across the entire platform."
    )

    add_callout_box(
        doc,
        title="Chairman Johnstone Angwenyi's Full Executive Clearance",
        text="Staff ID: CBK-3071 | Role: Executive Chairman (Full Master Rights)\n"
             "• Full Master Telemetry: Oversight across all 18 sports simultaneously.\n"
             "• Secretariat Command: Instant oversight of all attendance, walk-ins, and field marshals.\n"
             "• Financial Governance: Direct access to certified allowance ledgers before bank disbursement.\n"
             "• Role Administration: Full governance to appoint, reassign, or revoke team captains and officers.",
        bg_hex="FFFDF5",
        border_hex="B8860B",
        icon="🎖️"
    )

    # --------------------------------------------------------------------------
    # CHAPTER 5: CLOSING REFLECTION
    # --------------------------------------------------------------------------
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(16)
    h5.paragraph_format.space_after = Pt(6)
    r_h5 = h5.add_run("5. Closing Thoughts: Integrity in Public Service")
    r_h5.font.name = "Georgia"
    r_h5.font.size = Pt(16)
    r_h5.font.bold = True
    r_h5.font.color.rgb = COLOR_NAVY

    p_close = doc.add_paragraph()
    p_close.paragraph_format.space_after = Pt(10)
    p_close.paragraph_format.line_spacing = 1.15
    p_close.add_run(
        "Dad, growing up, you taught me the value of integrity, doing things properly, and leaving a system better than you found it. "
        "Building CBK STRIDE™ was not just about writing code; it was about solving a real institutional vulnerability at Kenya's apex financial regulator. "
        "Where there was once exhausted captains with wet paper clipboards, ghost attendees claiming allowances they didn't sweat for, "
        "and auditors sifting through disorganized sheets, there is now an institutional platform that is transparent, automated, and tamper-proof."
    )

    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(14)
    p_sign.paragraph_format.line_spacing = 1.15
    r_sign = p_sign.add_run("With great pride and respect,\n")
    r_sign.font.italic = True
    r_name = p_sign.add_run("Samuel Gathigi Njuguna\n")
    r_name.bold = True
    r_name.font.color.rgb = COLOR_NAVY
    p_sign.add_run("IT & Digital Services Directorate • Central Bank of Kenya")

    # Output paths
    output_docx = os.path.join(DIR, "CBK_STRIDE_Executive_Briefing_For_Dad.docx")
    artifact_docx = os.path.join(ARTIFACTS_DIR, "CBK_STRIDE_Executive_Briefing_For_Dad.docx")
    
    doc.save(output_docx)
    doc.save(artifact_docx)
    print(f"Saved Word Document: {output_docx}")
    print(f"Copied to Artifacts: {artifact_docx}")

if __name__ == "__main__":
    build_document()

"""
Generate StrideAnalytics Executive Whitepaper:
"The Institutional Cadence Framework: Transforming Core Banking Systems into Predictive Sovereign Intelligence"
Tailored for Board Chairs, CEOs, and Supervisory Committees.
Zero Pricing Mentioned - Pure Strategic, Regulatory & Risk Architecture.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "STRIDEANALYTICS • EXECUTIVE WHITEPAPER: INSTITUTIONAL CADENCE INTELLIGENCE")
            self.setStrokeColor(colors.HexColor("#00f3ff"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "EXECUTIVE BRIEFING • STRIDE SYSTEMS LTD • NAIROBI, KENYA • ODPC/CR/2026/0882")
        self.setStrokeColor(colors.HexColor("#334155"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf():
    pdf_path = r"C:\Users\user\.gemini\antigravity\scratch\cbk-stride\strideanalytics_web\stride_cadence_executive_whitepaper.pdf"
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#020408'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0284c7'),
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=12,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155'),
        spaceAfter=7
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0f223f')
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.white
    )

    story = []

    # Title Banner
    story.append(Paragraph("STRIDEANALYTICS STRATEGIC BRIEFING FOR CHIEF EXECUTIVES & BOARDS", ParagraphStyle('SuperTitle', fontName='Helvetica-Bold', fontSize=8.5, textColor=colors.HexColor('#64748b'), spaceAfter=4)))
    story.append(Paragraph("The Institutional Cadence Framework", title_style))
    story.append(Paragraph("Transforming Static Core Banking Systems into Forward-Looking Predictive Sovereign Intelligence", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=12))

    # Executive Summary Box
    summary_data = [[
        Paragraph("<b>EXECUTIVE MEMORANDUM</b><br/>"
                  "Most financial institutions and Deposit-Taking SACCOs operate with an inherent blind spot: their internal Enterprise Resource Planning (ERP) systems — such as Microsoft Dynamics NAV, Bankers Realm, and Finacle — are historical record keepers. They report backward-looking ledger entries. When economic shocks occur or borrowers experience distress, internal software remains silent until accounts are already 30+ days in arrears. This paper introduces the <b>Stride Institutional Cadence Architecture</b>: a synchronized, 4-stage operational heartbeat that converts raw closing balances into proactive supervisory and board intelligence.", callout_style)
    ]]
    summary_table = Table(summary_data, colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284c7')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 10))

    # Section 1: The Core Paradox
    story.append(Paragraph("1. The Enterprise Dilemma: Why Internal Software Has No Predictive Intelligence", h1_style))
    story.append(Paragraph(
        "Commercial and SACCO core banking platforms are engineered for transaction reconciliation, account debiting, and branch balancing. They were never architected as mathematical risk engines. In practice, this creates three structural vulnerabilities for institutional leadership:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>The Latency Trap (30-Day Lag):</b> Legacy ERPs recognize non-performing loans only after 30 days of missed payments. By the time an account appears on an arrears report, the cost of recovery has increased by over 400%.<br/>"
        "• <b>Static Consolidation Drag:</b> Preparing monthly SASRA Form 1 and Form 4 returns requires finance teams to spend up to 10 working days manually compiling, checking, and reconciling spreadsheets.<br/>"
        "• <b>Zero Macro Stress-Test Capability:</b> When the Central Bank of Kenya adjusts the Central Bank Rate (CBR) or macro liquidity tightens, legacy systems cannot project spread compression or model a simultaneous member withdrawal run.",
        body_style
    ))

    # Section 2: The Four Institutional Cadences Table
    story.append(Paragraph("2. The Four Synchronized Institutional Cadences", h1_style))
    story.append(Paragraph(
        "StrideAnalytics introduces a structured rhythm that aligns with statutory deadlines and executive decision cycles:",
        body_style
    ))

    cadence_table_data = [
        [Paragraph("Cadence", table_header), Paragraph("Operational Function", table_header), Paragraph("Legacy System Limitation", table_header), Paragraph("Stride Predictive Breakthrough", table_header)],
        [
            Paragraph("<b>⚡ WEEKLY</b><br/><i>Credit Risk & Underwriting</i>", table_cell),
            Paragraph("Monitors loan repayment velocity and guarantor strength.", table_cell),
            Paragraph("Flags accounts only after 30 days of delinquency.", table_cell),
            Paragraph("<b>Catches early distress at Day 7</b> using savings velocity and mobile flow drops (21 days earlier).", table_cell)
        ],
        [
            Paragraph("<b>🗓️ MONTHLY</b><br/><i>Regulatory Compliance</i>", table_cell),
            Paragraph("Mandatory SASRA Section 24 Form 1 & 4 filings.", table_cell),
            Paragraph("Requires 10–14 days of manual spreadsheet reconciliation.", table_cell),
            Paragraph("<b>Assembles verified returns in &lt; 30 seconds</b> with cryptographic Merkle audit receipts.", table_cell)
        ],
        [
            Paragraph("<b>📈 QUARTERLY</b><br/><i>Board Strategic Defense</i>", table_cell),
            Paragraph("Executive retreat balance sheet risk defense.", table_cell),
            Paragraph("Presents backward-looking historical P&L statements.", table_cell),
            Paragraph("<b>Simulates +300bps CBR hikes</b> and 15% liquidity runs, verifying board fiduciary buffer.", table_cell)
        ],
        [
            Paragraph("<b>🏛️ ANNUAL</b><br/><i>Governance & AGM Assembly</i>", table_cell),
            Paragraph("General assembly voting and dividend optimization.", table_cell),
            Paragraph("Paper ballots prone to quorum disputes and manual tallies.", table_cell),
            Paragraph("<b>Biometric quorum tracking</b>, encrypted balloting, and mathematical dividend optimization (e.g. 11.8%).", table_cell)
        ]
    ]

    c_table = Table(cadence_table_data, colWidths=[95, 125, 135, 149])
    c_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(c_table)
    story.append(Spacer(1, 10))

    # Section 3: Accounting Rigor & Absolute Running Balances
    story.append(Paragraph("3. Accounting Precision: Point-in-Time Running Balances vs Arbitrary Summation", h1_style))
    story.append(Paragraph(
        "A critical distinction appreciated by seasoned banking executives and regulators is the fundamental difference between balance sheet <i>Stock</i> and period <i>Flow</i> accounts:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Absolute Running Balance Standard:</b> Total Loan Book and Member Deposits are cumulative closing positions as at period end (e.g. Dec 31). Stride's ingestion engine treats these balances as point-in-time stock reserves, preventing erroneous year-on-year double counting.<br/>"
        "• <b>Net Annual Mobilization (Δ YoY Flow):</b> By decoupling cumulative closing stock from period delta movements, Stride provides the CEO with dual-lens clarity: exact capital reserves on one axis, and actual net new deposits mobilized on the other.",
        body_style
    ))

    # Section 4: ODPC Sovereign Data Privacy Architecture
    story.append(Paragraph("4. Air-Gapped Ingestion & Legal Immunity Under ODPC Act (2019)", h1_style))
    story.append(Paragraph(
        "Institutional adoption of cloud intelligence historically stalled due to cybersecurity and data leakage fears. Stride eliminates this barrier through its <b>Three-Tier Sovereign Air-Gap Protocol</b>:<br/>"
        "1. <b>Zero Listening Ports:</b> Neither the institution nor Stride requires open inbound firewall ports (such as SQL 1433 or FTP 21). Data ingestion occurs strictly via outbound HTTPS 443.<br/>"
        "2. <b>Single-Use Ephemeral Soft-Tokens:</b> Authorized finance signatories authenticate uploads via a 15-minute, single-use Time-Based One-Time Password (TOTP) delivered directly to corporate email.<br/>"
        "3. <b>Client-Side Mathematical Hashing:</b> Before any trial balance leaves the workstation perimeter, member National IDs and telephone numbers are dynamically salted and tokenized via HMAC-SHA-256. Raw PII never touches the cloud.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Section 5: Institutional Outcomes & Executive Summary
    story.append(Paragraph("5. Measurable Outcomes for Executive Leadership", h1_style))
    
    outcomes_data = [
        [Paragraph("Executive Dimension", table_header), Paragraph("Institutional Impact & Risk Mitigation", table_header)],
        [
            Paragraph("<b>Chief Executive Officer (CEO)</b>", table_cell),
            Paragraph("Instant boardroom defense. 1-click generation of audited stress scenarios proving solvency and capital adequacy under macroeconomic volatility.", table_cell)
        ],
        [
            Paragraph("<b>Chief Financial Officer (CFO)</b>", table_cell),
            Paragraph("100% statutory filing SLA. Automates SASRA Form 1 (Capital Adequacy) and Form 4 (Liquidity Shield) compilation from days into seconds.", table_cell)
        ],
        [
            Paragraph("<b>Chief Risk Officer (CRO)</b>", table_cell),
            Paragraph("Early default containment. Identifies deteriorating borrower liquidity trajectories up to 21 days before conventional 30-day arrears recognition.", table_cell)
        ],
        [
            Paragraph("<b>Board Supervisory Committee</b>", table_cell),
            Paragraph("Fiduciary peace of mind. Cryptographic Merkle-root receipts provide tamper-proof evidentiary audit trails for external statutory reviews.", table_cell)
        ]
    ]

    o_table = Table(outcomes_data, colWidths=[150, 354])
    o_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284c7')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(o_table)
    story.append(Spacer(1, 10))

    # Corporate Sign-off Block
    closing_data = [[
        Paragraph("<b>STRIDE SOVEREIGN GOVERNANCE & PREDICTIVE ANALYTICS</b><br/>"
                  "Stride Systems Ltd • Nairobi Financial Corridor, Upper Hill / Kilimani, Kenya<br/>"
                  "<b>Executive Enquiries:</b> info@strideanalytics.co.ke | <b>Live Portal:</b> https://strideanalytics.co.ke<br/>"
                  "<i>Statutory Registrations: Data Protection Act Certificate #ODPC/CR/2026/0882 • SASRA Tier-1 Compliant</i>", callout_style)
    ]]
    closing_table = Table(closing_data, colWidths=[504])
    closing_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#64748b')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(closing_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Executive Cadence Whitepaper built successfully at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()

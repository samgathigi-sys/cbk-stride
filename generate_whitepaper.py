"""
Generate StrideAnalytics Institutional Whitepaper PDF:
"Secure Sacco Data Ingestion, Navision Integration & Time-Based Soft Token Architecture"
Compliant with Kenya ODPC (2019) and SASRA Cap 490B.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
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
            self.drawString(54, 750, "STRIDEANALYTICS • INSTITUTIONAL WHITEPAPER: SOVEREIGN SACCO DATA INGESTION")
            self.setStrokeColor(colors.HexColor("#00f3ff"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY • STRIDE SYSTEMS LTD • NAIROBI, KENYA • ODPC/CR/2026/0882")
        self.setStrokeColor(colors.HexColor("#334155"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()

def build_pdf():
    pdf_path = r"C:\Users\user\.gemini\antigravity\scratch\cbk-stride\strideanalytics_web\strideanalytics_whitepaper.pdf"
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Brand Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#020408'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0284c7'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#0284c7'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0f223f')
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor('#1e293b')
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.white
    )

    story = []

    # Title Banner
    story.append(Paragraph("STRIDEANALYTICS INSTITUTIONAL WHITEPAPER", ParagraphStyle('SuperTitle', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#64748b'), spaceAfter=4)))
    story.append(Paragraph("Sovereign Ingestion & Email Soft-Token Architecture", title_style))
    story.append(Paragraph("Bridging Microsoft Dynamics NAV / Navision to Stride Sovereign Cloud via Ephemeral Dual-Factor Soft Tokens & Zero-Trust Tokenization", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=14))

    # Executive Summary Callout Box
    summary_data = [[
        Paragraph("<b>EXECUTIVE MANDATE & AUDIT SUMMARY</b><br/>"
                  "Deposit-Taking SACCOs in Kenya running on-premise ERPs (principally Microsoft Dynamics NAV / Business Central) require seamless, daily or monthly data synchronization into StrideAnalytics for automated SASRA Form 1 & 4 returns and stress testing. This whitepaper establishes Stride's <b>Air-Gapped Soft-Token Upload Protocol</b> — delivering banking-grade security with zero IT friction, zero direct port exposure, and 100% ODPC statutory data compliance.", callout_style)
    ]]
    summary_table = Table(summary_data, colWidths=[504])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284c7')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 14))

    # Section 1: The Core Architecture
    story.append(Paragraph("1. The Operational Challenge: Navision Data Extraction Without Opening Firewall Ports", h1_style))
    story.append(Paragraph(
        "Tier-1 SACCO internal core banking servers hosting Microsoft Dynamics NAV (Navision) are strictly isolated behind corporate DMZs. Exposing database ports (e.g. MS-SQL 1433) or direct Web Services (SOAP/OData) directly to the public internet creates intolerable cyber risk and violates CBK/SASRA cybersecurity guidelines.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Stride's Solution:</b> Stride utilizes an <i>Outbound-Push & Ephemeral Token Model</i>. Neither the SACCO nor Stride requires inbound firewall pinholes. Authorized SACCO Finance or IT Officers export standardized XML/CSV general ledgers and trial balances from Navision, and transmit them via Stride's secure, single-use email soft-token gateway.",
        body_style
    ))

    # Section 2: Step-by-Step Soft-Token Lifecycle
    story.append(Paragraph("2. The 4-Step Email Soft-Token Lifecycle (End-to-End Workflow)", h1_style))
    story.append(Paragraph(
        "The authentication workflow eliminates permanently stored static passwords for data uploads, mitigating credential theft and unauthorized batch modifications:",
        body_style
    ))

    flow_data = [
        [Paragraph("Step", table_header), Paragraph("Mechanism", table_header), Paragraph("Security Control & Safeguard", table_header)],
        [
            Paragraph("<b>01. Upload Request Trigger</b>", table_cell),
            Paragraph("Authorized Finance Officer enters registered email on <code>tenant.strideanalytics.co.ke/ingest</code>.", table_cell),
            Paragraph("Whitelisted against SACCO Board authorized signatory database. Rate-limited to prevent enumeration.", table_cell)
        ],
        [
            Paragraph("<b>02. Dual-Hash Token Dispatch</b>", table_cell),
            Paragraph("Stride Auth-Engine issues an encrypted, single-use 6-digit TOTP plus an embedded Magic Link to corporate email.", table_cell),
            Paragraph("Valid for exactly <b>15 minutes</b>. Delivered via end-to-end encrypted SMTP TLS with SPF/DKIM verification.", table_cell)
        ],
        [
            Paragraph("<b>03. Secure Vault Session</b>", table_cell),
            Paragraph("Officer clicks the magic link or enters the 6-digit soft token. An encrypted memory buffer opens.", table_cell),
            Paragraph("Session is client-side pinned. Automatic revocation upon upload completion or window expiry.", table_cell)
        ],
        [
            Paragraph("<b>04. Client-Side ODPC Tokenization</b>", table_cell),
            Paragraph("Navision CSV/Excel file is processed. Member National IDs and phone numbers are SHA-256 salted before upload.", table_cell),
            Paragraph("Zero raw personal identifiers reach the cloud. Merkle root proof returned for SACCO audit files.", table_cell)
        ]
    ]
    flow_table = Table(flow_data, colWidths=[110, 204, 190])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 14))

    # Section 3: Navision Export Formats & Accounting Logic
    story.append(Paragraph("3. Microsoft Dynamics NAV Integration & 'Running Balance' Alignment", h1_style))
    story.append(Paragraph(
        "Following feedback from institutional regulators and executive SACCO management (e.g. Banki Kuu SACCO case study), Stride ingests financial trial balance balances as <b>Absolute Point-in-Time Running Balances</b> rather than arbitrary summation flows:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Balance Sheet Accounts (Loan Book & Member Deposits):</b> Extracted from Navision General Ledger closing positions as at December 31st or month-end. Stride's engine recognizes these as cumulative stock reserves.<br/>"
        "• <b>Income & Expense Accounts (Net Influx Δ Flows):</b> Extracted as period transactions, allowing boardrooms to analyze both total asset size and YoY growth delta simultaneously.<br/>"
        "• <b>Pre-Built Navision XML Port / Dataport:</b> Stride provides an official 1-click XML Port for Dynamics NAV 2013, 2016, 2018, and Business Central that packages required trial balance columns in under 30 seconds.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # Section 4: Security Comparison Matrix
    story.append(Paragraph("4. Institutional Security Evaluation: Stride vs Legacy Methods", h1_style))
    
    comp_data = [
        [Paragraph("Security Dimension", table_header), Paragraph("Traditional FTP / Open Port", table_header), Paragraph("Stride Sovereign Soft-Token Gateway", table_header)],
        [
            Paragraph("<b>Attack Surface</b>", table_cell),
            Paragraph("High (Open ports 1433/21 exposed to public internet).", table_cell),
            Paragraph("<b>Zero Exposure</b> (Outbound HTTPS 443 only; no listening ports).", table_cell)
        ],
        [
            Paragraph("<b>Credential Vulnerability</b>", table_cell),
            Paragraph("Static passwords stored in plaintext configuration files.", table_cell),
            Paragraph("<b>Ephemeral TOTP</b> (Tokens self-destruct in 15 mins).", table_cell)
        ],
        [
            Paragraph("<b>ODPC PII Compliance</b>", table_cell),
            Paragraph("Raw member ID cards and phone numbers uploaded unencrypted.", table_cell),
            Paragraph("<b>Client-Side Dynamic Masking</b> (SHA-256 salted tokens).", table_cell)
        ],
        [
            Paragraph("<b>Audit Trail & Merkle Proof</b>", table_cell),
            Paragraph("Basic server access log; easily manipulated.", table_cell),
            Paragraph("<b>Cryptographic Ledger</b> signed with time-stamped hash.", table_cell)
        ]
    ]
    comp_table = Table(comp_data, colWidths=[130, 184, 190])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284c7')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')])
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 14))

    # Section 5: Regulatory Attestation
    story.append(Paragraph("5. Regulatory Compliance & Statutory Attestation", h1_style))
    story.append(Paragraph(
        "StrideAnalytics operates under full statutory alignment with Kenyan laws governing financial and data institutions:<br/>"
        "• <b>Sacco Societies Act (Cap 490B) Section 24:</b> Automates filing integrity for Form 1 (Capital Adequacy) and Form 4 (Liquidity Shield) directly from verified Navision balances.<br/>"
        "• <b>Kenya Data Protection Act (ODPC 2019):</b> Stride ensures that in the event of an institutional inspection, all data custody is mathematically demonstratable as anonymized.<br/>"
        "• <b>CBK Prudential Guidelines & Cybersecurity Framework:</b> Multi-tenant isolation guarantees zero data leakage between peer SACCO entities.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # Institutional Contact Block
    contact_data = [[
        Paragraph("<b>FOR INSTITUTIONAL PILOTS & NAVISION INTEGRATION KITS</b><br/>"
                  "Stride Systems Ltd • Nairobi Financial Corridor, Upper Hill / Kilimani, Kenya<br/>"
                  "<b>Official Inquiries:</b> info@strideanalytics.co.ke | <b>Web Portal:</b> https://strideanalytics.co.ke<br/>"
                  "<i>ODPC Official Registration Certificate: #ODPC/CR/2026/0882 • SASRA Tier-1 Ready</i>", callout_style)
    ]]
    contact_table = Table(contact_data, colWidths=[504])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#64748b')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(contact_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Whitepaper PDF built successfully at: {pdf_path}")

if __name__ == "__main__":
    build_pdf()

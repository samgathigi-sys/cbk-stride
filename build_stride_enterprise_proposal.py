"""
STRIDE™ Enterprise Commercial & Technical Proposal Generator
Generates:
1. STRIDE_Enterprise_Commercial_Proposal.html (Executive responsive HTML proposal with Print-to-PDF styling)
2. STRIDE_Enterprise_Commercial_Proposal.pdf (Multi-page formal executive vector PDF via ReportLab)
3. STRIDE_Enterprise_Commercial_Proposal.md (Markdown artifact for executive sharing)
"""

import os
import sys
import shutil

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACT_DIR = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e"

# Custom Canvas for Page Numbers & Headers/Footers
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
        if self._pageNumber == 1:
            # Suppress running header/footer on cover page
            return
        
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0A2540"))
        
        # Header
        self.drawString(40, 805, "STRIDE™ ENTERPRISE PROPOSAL")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(555, 805, "CONFIDENTIAL & PROPRIETARY • 2026/2027")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(40, 798, 555, 798)

        # Footer
        self.line(40, 45, 555, 45)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(40, 32, "Platform: https://cbk-stride.streamlit.app | Sovereign Cloud Governance Architecture")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(555, 32, page_str)
        self.restoreState()

def build_pdf_proposal():
    pdf_proj = os.path.join(BASE_DIR, "STRIDE_Enterprise_Commercial_Proposal.pdf")
    pdf_art = os.path.join(ARTIFACT_DIR, "STRIDE_Enterprise_Commercial_Proposal.pdf")

    doc = SimpleDocTemplate(
        pdf_proj,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Define professional styles
    c_primary = colors.HexColor('#0A2540')
    c_gold = colors.HexColor('#D97706')
    c_cyan = colors.HexColor('#0284C7')
    c_dark = colors.HexColor('#0F172A')
    c_muted = colors.HexColor('#475569')

    cover_title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=c_primary
    )
    cover_sub_style = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=c_gold
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=c_primary,
        spaceBefore=14,
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_cyan,
        spaceBefore=10,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=c_dark,
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=c_dark
    )
    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13.5,
        textColor=colors.HexColor('#1E3A8A')
    )

    story = []

    # ================= PAGE 1: COVER PAGE =================
    story.append(Spacer(1, 40))
    # Brand Pill
    pill_data = [[Paragraph("<b>ENTERPRISE COMMERCIAL & TECHNICAL PROPOSAL</b>", ParagraphStyle('Pill', fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#B45309')))]]
    t_pill = Table(pill_data, colWidths=[280])
    t_pill.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF3C7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#F59E0B')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_pill)
    story.append(Spacer(1, 20))

    story.append(Paragraph("STRIDE™ Sovereign Platform", cover_title_style))
    story.append(Paragraph("Zero-Capex Digital Passes, Statutory Quorum Telemetry & ODPC § 25 Compliant Governance Engine", cover_sub_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=3, color=colors.HexColor('#F59E0B'), spaceAfter=20))

    # Meta Table
    meta_data = [
        [Paragraph("<b>Prepared For:</b>", bullet_style), Paragraph("Board of Directors, Executive Management, Company Secretaries & ICT Committees", body_style)],
        [Paragraph("<b>Target Sectors:</b>", bullet_style), Paragraph("Regulated SACCOs, Tier-1 Banks, Listed PLCs, Sports Federations & Professional Associations", body_style)],
        [Paragraph("<b>Platform Solution:</b>", bullet_style), Paragraph("STRIDE™ Sovereign Enterprise Edition (v2.8 Production Architecture)", body_style)],
        [Paragraph("<b>Statutory Mandate:</b>", bullet_style), Paragraph("Kenya Data Protection Act 2019 (ODPC § 25) • SASRA AGM Quorum Standards • Companies Act § 284", body_style)],
        [Paragraph("<b>Cloud Infrastructure:</b>", bullet_style), Paragraph("Zero-Capex Serverless Architecture • AWS Frankfurt Managed PostgreSQL • Streamlit Cloud Edge", body_style)],
        [Paragraph("<b>Production Sandbox:</b>", bullet_style), Paragraph("https://cbk-stride.streamlit.app | Dedicated SACCO Portal: /BKS", body_style)],
        [Paragraph("<b>Date of Issue:</b>", bullet_style), Paragraph("October 2026 | Validity: 90 Calendar Days", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[130, 385])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 30))

    # Executive Summary Highlight Box
    exec_box = [[
        Paragraph(
            "<b>EXECUTIVE BRIEF:</b><br/>"
            "Traditional corporate AGMs, shareholder elections, and large-scale sporting conventions are plagued by "
            "vulnerabilities: fraudulent proxy certifications, contentious manual headcounts, exposed attendee phone numbers, "
            "and exorbitant on-premise AV/IT hardware rental costs. <b>STRIDE™</b> eliminates these vulnerabilities in their entirety. "
            "By pairing zero-capex cloud-native computing with cryptographic digital mobile passes, real-time SASRA quorum telemetry, "
            "and automated Kenya DPA 2019 PII privacy masking, STRIDE™ guarantees indisputable institutional trust at a fraction of the cost.",
            callout_style
        )
    ]]
    t_exec = Table(exec_box, colWidths=[515])
    t_exec.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#3B82F6')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_exec)

    story.append(PageBreak())

    # ================= PAGE 2: PROBLEM STATEMENT & THE STRIDE SOLUTION =================
    story.append(Paragraph("1. The Enterprise Problem & Operational Risk", h1_style))
    story.append(Paragraph(
        "Modern corporate governance, regulated SACCOs, and federations face intense statutory and operational pressures "
        "when convening physical or hybrid statutory meetings. Conventional event management workflows expose institutions to severe liabilities:",
        body_style
    ))

    prob_data = [
        ["Operational Challenge", "The Traditional Breakdown", "The Institutional Liability"],
        [
            "Statutory Quorum Verification",
            "Slow, manual sign-in desks with long queues; physical ledger signatures tallied by hand.",
            "Meeting invalidation under Companies Act § 284 or SASRA regulations; contested voting legitimacy."
        ],
        [
            "PII Exposure & Privacy Breach",
            "Printed attendee rosters placed at door desks revealing executive and member phone numbers & emails.",
            "ODPC § 25 penalties (up to KES 5,000,000 or 1% annual turnover); severe reputational breach."
        ],
        [
            "Proxy Hijacking & Ballot Tampering",
            "Paper voting slips, unverified proxy appointments, and unverifiable manual ballot box counts.",
            "Litigation from aggrieved shareholders, regulatory inquiries, and board governance deadlock."
        ],
        [
            "High Capex Hardware Overhead",
            "Renting expensive badge printers, dedicated server racks, barcode scanners, and proprietary on-premise gear.",
            "Unjustified operational budgets exceeding KES 500,000 to KES 1,500,000 per statutory meeting."
        ]
    ]
    t_prob = Table(prob_data, colWidths=[120, 195, 200])
    t_prob.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#FFFFFF')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFF1F2')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#FECDD3')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#F43F5E')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    story.append(t_prob)
    story.append(Spacer(1, 12))

    story.append(Paragraph("2. The STRIDE™ Sovereign Solution Architecture", h1_style))
    story.append(Paragraph(
        "<b>STRIDE™</b> is an agile, zero-capex cloud-native platform engineered specifically to resolve these challenges. "
        "Built with high-throughput cloud infrastructure and deployable within minutes, STRIDE™ delivers four sovereign capabilities:",
        body_style
    ))

    sol_data = [
        [
            Paragraph("<b>• Zero-Capex Serverless Core</b><br/>Operates entirely on managed cloud-native edge compute (Streamlit Cloud + AWS Frankfurt PostgreSQL). Zero servers to procure, zero software licenses to maintain. Door ushers utilize existing company smartphones or iPads to scan passes.", bullet_style),
            Paragraph("<b>• Kenya DPA 2019 Privacy Pipeline</b><br/>All delegate telephone numbers and institutional emails are masked by default (e.g. 072* *** *56) across public screens and usher desks. Protected by 2FA Secretariat passkey reveal with an automatic 15-minute relock timer.", bullet_style)
        ],
        [
            Paragraph("<b>• SASRA Real-Time Quorum Radar</b><br/>Instantaneous live quorum telemetry against constitutional thresholds. Live categorization of principal members vs. accredited proxies, providing Returning Officers with statutory certainty before motions are tabled.", bullet_style),
            Paragraph("<b>• Decoupled Cryptographic Ballot</b><br/>Strict cryptographic decoupling of the member's identity accreditation token from their voting record. Enables tamper-proof resolutions, candidate elections, and share-weighted corporate ballots.", bullet_style)
        ]
    ]
    t_sol = Table(sol_data, colWidths=[255, 255])
    t_sol.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDF4')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#86EFAC')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#BBF7D0')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sol)

    story.append(PageBreak())

    # ================= PAGE 3: FEATURE MATRIX & USE CASES =================
    story.append(Paragraph("3. Multi-Industry Enterprise Use Cases", h1_style))
    story.append(Paragraph(
        "STRIDE™'s modular architecture spans regulatory, commercial, and athletic institutions:",
        body_style
    ))

    uc_data = [
        ["Sector / Institution", "Core STRIDE™ Application", "Primary Strategic Value"],
        ["Regulated SACCOs & Microfinance", "Annual General Meetings (AGM), Special General Meetings (SGM), Delegate Assemblies", "SASRA quorum compliance, elimination of unaccredited proxy votes, instant attendance book generation."],
        ["Listed PLCs & Commercial Banks", "Annual Shareholder Meetings, Board Elections, Extraordinary General Meetings (EGM)", "Share-weighted vote tallying, ODPC § 25 compliance for VIP/HNI shareholders, zero hardware rental capex."],
        ["Sports Clubs & National Federations", "Inter-Bank Games, National Championships, League Tournaments, Player Registration", "Anti-ghost athlete verification, 18-sport roster management, pitchside captain roll-call & allowances."],
        ["Medical & Professional Unions", "Annual Scientific Conferences, Credential Accreditations, Voting Assemblies", "Instant CPD accreditation clearance, tamper-proof QR check-in, real-time delegate attendance telemetry."]
    ]
    t_uc = Table(uc_data, colWidths=[120, 185, 210])
    t_uc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#F59E0B')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    story.append(t_uc)
    story.append(Spacer(1, 14))

    story.append(Paragraph("4. Institutional Case Study: Central Bank of Kenya Sports Club & Banki Kuu SACCO", h1_style))
    story.append(Paragraph(
        "STRIDE™ was deployed to power the accreditation, athlete telemetry, and statutory AGM infrastructure for the "
        "<b>Central Bank of Kenya (CBK) Sports Club</b> and <b>Banki Kuu Staff SACCO Society</b> (58th AGM Pilot).",
        body_style
    ))

    cs_box = [[
        Paragraph(
            "<b>PILOT RESULTS & BENCHMARK HIGHLIGHTS:</b><br/>"
            "• <b>5-Minute Onboarding:</b> Complete delegate roster ingested and tokenized in under 300 seconds.<br/>"
            "• <b>Zero Hardware Rentals:</b> Gate ushers scanned 100+ arriving delegates using standard iOS/Android devices with zero check-in bottlenecks.<br/>"
            "• <b>100% SASRA Quorum Telemetry:</b> Returning Officers verified statutory constitutional floor (50 delegates minimum) with live surplus telemetry (+51 surplus) before tabling key resolutions.<br/>"
            "• <b>Bulletproof Privacy Audit:</b> All personal contact data remained masked during check-in, satisfying ODPC § 25 guidelines with zero data leak incidents.",
            callout_style
        )
    ]]
    t_cs = Table(cs_box, colWidths=[515])
    t_cs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEFCE8')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#CA8A04')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(t_cs)

    story.append(PageBreak())

    # ================= PAGE 4: COMMERCIAL PRICING & DEPLOYMENT TIMELINE =================
    story.append(Paragraph("5. Commercial Pricing & Investment Tiers", h1_style))
    story.append(Paragraph(
        "STRIDE™ offers transparent, modular pricing with zero hidden setup fees and zero infrastructure maintenance charges. "
        "Clients may procure STRIDE™ per-event or via an Annual Enterprise Sovereign License.",
        body_style
    ))

    pricing_data = [
        ["Tier", "Scope / Capacity", "Event License Fee", "Core Deliverables & Capabilities Included"],
        [
            "Society / Club Tier",
            "Up to 100 Delegates\nor Athletes",
            "KES 15,000\n(One-off / Event)",
            "• Self-Serve Event Wizard Creator\n• Dynamic QR Digital Pass Generation\n• Live Usher Phone/Tablet Scanner Terminal\n• Official CSV Attendance Register Export"
        ],
        [
            "Mid-Sized Corporate /\nRegulated SACCO Tier\n[Recommended]",
            "101 – 500 Delegates\n(Standard AGM)",
            "KES 35,000\n(One-off / Event)",
            "• Everything in Society Tier plus:\n• SASRA Statutory Quorum Radar Gauge\n• Principal vs. Proxy Breakdown Telemetry\n• Decoupled Encrypted Secret Ballot (3 Motions)\n• Kenya DPA 2019 Masking & 2FA RBAC Relock\n• Dedicated Remote Tech Concierge Support"
        ],
        [
            "Large PLC / Tier-1\nEnterprise Tier",
            "501 – 2,500+ Delegates\n(Hybrid / Multi-Gate)",
            "KES 75,000\n(One-off / Event)",
            "• Everything in Mid-Sized Tier plus:\n• Multi-Gate Dual Usher Synchronizer\n• Share-Weighted Voting Matrix & Candidates\n• Dedicated AWS Frankfurt High-Throughput Node\n• White-Glove On-Site Returning Officer Concierge\n• Post-Event Forensic Statutory Audit Dossier"
        ]
    ]
    t_pricing = Table(pricing_data, colWidths=[105, 85, 95, 230])
    t_pricing.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0A2540')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#F5C542')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FFFFFF')),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor('#FEF9C3')), # highlight popular
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#64748B')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    story.append(t_pricing)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Optional Annual Sovereign Enterprise Retainer:</b>", h2_style))
    story.append(Paragraph(
        "For institutions hosting multiple assemblies, sports days, and committee elections throughout the fiscal year, "
        "an <b>Annual Enterprise Retainer (KES 120,000 / year)</b> provides unlimited events, continuous 24/7 PostgreSQL uptime, "
        "and priority white-glove feature development.",
        body_style
    ))
    story.append(Spacer(1, 8))

    story.append(Paragraph("6. Rapid Implementation Roadmap (48-Hour Guarantee)", h1_style))
    roadmap_data = [
        ["Phase", "Milestone / Activity", "Turnaround Time"],
        ["Phase 1: Ingestion", "Client submits delegate/member roster (Excel/CSV) & event agenda parameters.", "Hour 0 – 12"],
        ["Phase 2: Provisioning", "STRIDE™ provisions dedicated tenant, configures quorum thresholds & secret ballot motions.", "Hour 12 – 24"],
        ["Phase 3: Dispatch & Training", "Automated distribution of dynamic mobile passes; 30-minute usher briefing.", "Hour 24 – 36"],
        ["Phase 4: Live AGM / Event", "Live gate check-in, real-time quorum attainment radar, and secret ballot tabulation.", "Hour 48 (Event Day)"]
    ]
    t_road = Table(roadmap_data, colWidths=[95, 320, 100])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#FFFFFF')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
    ]))
    story.append(t_road)

    story.append(PageBreak())

    # ================= PAGE 5: SECURITY, SLA & FORMAL ACCEPTANCE =================
    story.append(Paragraph("7. Enterprise Security, Privacy & SLA Guarantees", h1_style))
    
    sla_data = [
        [
            Paragraph("<b>• 99.98% Service Availability</b><br/>Multi-region high-availability failover backed by AWS Frankfurt PostgreSQL persistence.", bullet_style),
            Paragraph("<b>• End-to-End Encryption</b><br/>All in-transit telemetry secured via TLS 1.3; data at rest protected using AES-256 bit encryption.", bullet_style)
        ],
        [
            Paragraph("<b>• 15-Minute Auto-Relock Security</b><br/>Terminals automatically re-mask PII if inactive, mitigating venue shoulder-surfing.", bullet_style),
            Paragraph("<b>• Post-Event Data De-identification</b><br/>Client-controlled data retention policy with 1-click irreversible sanitization.", bullet_style)
        ]
    ]
    t_sla = Table(sla_data, colWidths=[255, 255])
    t_sla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sla)
    story.append(Spacer(1, 14))

    story.append(Paragraph("8. Formal Commercial Acceptance & Authorization", h1_style))
    story.append(Paragraph(
        "By signing below, the Client authorizes STRIDE™ to initiate event provisioning and onboarding under the selected "
        "tier and terms outlined in this proposal.",
        body_style
    ))
    story.append(Spacer(1, 8))

    sign_data = [
        ["CLIENT AUTHORIZATION (Customer)", "STRIDE™ PLATFORM ACCEPTANCE"],
        [
            "Entity Name: _____________________________________\n\n"
            "Authorized Signatory: _____________________________\n\n"
            "Title / Designation: _______________________________\n\n"
            "Selected Tier: [  ] Society   [  ] Mid-Sized   [  ] PLC\n\n"
            "Signature: _______________________________________\n\n"
            "Date: ___________________________________________",
            "Organization: STRIDE™ Sovereign Technologies\n\n"
            "Designation: Lead Architect & Managing Director\n\n"
            "Portal: https://cbk-stride.streamlit.app\n\n"
            "Accreditation Ref: STRIDE-ENT-2026/27\n\n"
            "Signature: _______________________________________\n\n"
            "Date: October 5, 2026"
        ]
    ]
    t_sign = Table(sign_data, colWidths=[255, 255])
    t_sign.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0A2540')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#F5C542')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#0A2540')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8.5),
    ]))
    story.append(t_sign)

    doc.build(story, canvasmaker=NumberedCanvas)
    shutil.copy2(pdf_proj, pdf_art)
    print(f"✓ Formal Executive Vector PDF Proposal Generated: {pdf_proj}")


def build_html_proposal():
    html_proj = os.path.join(BASE_DIR, "STRIDE_Enterprise_Commercial_Proposal.html")
    html_art = os.path.join(ARTIFACT_DIR, "STRIDE_Enterprise_Commercial_Proposal.html")

    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>STRIDE™ Commercial & Technical Proposal</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Plus Jakarta Sans', sans-serif;
      background-color: #030914;
      color: #E2E8F0;
    }
    .mono { font-family: 'JetBrains Mono', monospace; }
    .gold-gradient {
      background: linear-gradient(135deg, #F5C542 0%, #D97706 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .cyan-gradient {
      background: linear-gradient(135deg, #00F2FE 0%, #0284C7 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    @media print {
      body { background-color: #ffffff; color: #0f172a; }
      .no-print { display: none !important; }
      .page-break { page-break-before: always; }
      .glass-card { background: #ffffff !important; border: 1px solid #cbd5e1 !important; color: #0f172a !important; }
      .text-slate-300, .text-slate-400 { color: #334155 !important; }
      .text-white { color: #0f172a !important; }
    }
    .glass-card {
      background: rgba(10, 26, 52, 0.7);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
  </style>
</head>
<body class="min-h-screen py-10 px-4 sm:px-6 lg:px-8">

  <!-- Top Sticky Print Action Bar -->
  <div class="max-w-5xl mx-auto mb-8 no-print flex flex-col sm:flex-row justify-between items-center gap-4 bg-slate-900/90 p-4 rounded-xl border border-slate-800 shadow-xl backdrop-blur-md">
    <div class="flex items-center gap-3">
      <div class="w-3 h-3 rounded-full bg-emerald-400 animate-pulse"></div>
      <span class="text-sm font-semibold text-slate-200">STRIDE™ Commercial Proposal Document • Official v2.8</span>
    </div>
    <div class="flex items-center gap-3">
      <button onclick="window.print()" class="px-5 py-2.5 bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-500 hover:to-amber-600 text-slate-950 font-bold rounded-lg shadow-lg flex items-center gap-2 transition-all transform hover:scale-105 text-sm">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path></svg>
        Print to PDF / Share
      </button>
      <a href="https://cbk-stride.streamlit.app" target="_blank" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-cyan-400 border border-cyan-500/30 rounded-lg text-sm font-semibold transition-all">
        Launch Live Portal →
      </a>
    </div>
  </div>

  <div class="max-w-5xl mx-auto space-y-12">

    <!-- COVER SECTION -->
    <div class="glass-card rounded-3xl p-8 sm:p-12 border-t-4 border-amber-400 shadow-2xl relative overflow-hidden">
      <div class="absolute -right-20 -top-20 w-80 h-80 bg-amber-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -left-20 -bottom-20 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-400/10 border border-amber-400/30 text-amber-300 text-xs font-bold tracking-wider uppercase mb-6">
        CONFIDENTIAL ENTERPRISE PROPOSAL • 2026/2027
      </div>

      <h1 class="text-4xl sm:text-6xl font-extrabold tracking-tight text-white mb-4">
        CBK STRIDE<span class="text-amber-400">™</span>
      </h1>
      <p class="text-xl sm:text-2xl font-medium text-slate-300 max-w-3xl mb-8 leading-relaxed">
        The Zero-Capex Sovereign Engine for Corporate AGMs, Shareholder Democracy & Multi-Sport Telemetry
      </p>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 pt-6 border-t border-slate-800 text-sm">
        <div>
          <span class="block text-slate-400 text-xs uppercase font-semibold">Prepared For</span>
          <span class="font-bold text-slate-200">Executive Boards, SACCOs & PLCs</span>
        </div>
        <div>
          <span class="block text-slate-400 text-xs uppercase font-semibold">Statutory Standard</span>
          <span class="font-bold text-cyan-400">Kenya DPA 2019 / ODPC § 25 Compliant</span>
        </div>
        <div>
          <span class="block text-slate-400 text-xs uppercase font-semibold">Infrastructure Capex</span>
          <span class="font-bold text-emerald-400">KES 0.00 (100% Serverless Edge)</span>
        </div>
      </div>
    </div>

    <!-- SECTION 1: THE ENTERPRISE PROBLEM -->
    <div class="glass-card rounded-2xl p-8 border border-slate-800 shadow-xl">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-8 h-8 rounded-lg bg-red-500/20 text-red-400 flex items-center justify-center font-bold text-sm">01</div>
        <h2 class="text-2xl font-bold text-white">The Enterprise Challenge: Why Traditional AGMs & Events Fail</h2>
      </div>
      <p class="text-slate-300 leading-relaxed mb-6">
        Every year, corporate secretaries, SACCO boards, and event committees waste millions of shillings renting on-premise hardware, 
        battling chaotic paper registration desks, and managing disputed voting tallies—all while exposing attendee personal phone numbers in direct violation of the <b>Kenya Data Protection Act 2019</b>.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="p-5 rounded-xl bg-red-950/20 border border-red-900/30">
          <div class="font-bold text-red-400 mb-1 flex items-center gap-2">
            <span>⚠️</span> The Quorum Integrity Vulnerability
          </div>
          <p class="text-sm text-slate-300">
            Manual physical ledger headcounts lead to bitter quorum disputes. Without real-time verification of principal delegates vs. unaccredited proxies, AGM resolutions risk being invalidated under <b>Companies Act § 284</b> and <b>SASRA regulations</b>.
          </p>
        </div>
        <div class="p-5 rounded-xl bg-red-950/20 border border-red-900/30">
          <div class="font-bold text-red-400 mb-1 flex items-center gap-2">
            <span>⚖️</span> ODPC § 25 Privacy Breach Liability
          </div>
          <p class="text-sm text-slate-300">
            Open paper sign-in registers at venue usher desks display executive and member phone numbers to the entire auditorium, triggering statutory fines of up to <b>KES 5,000,000</b> or 1% annual turnover by the Data Commissioner.
          </p>
        </div>
        <div class="p-5 rounded-xl bg-red-950/20 border border-red-900/30">
          <div class="font-bold text-red-400 mb-1 flex items-center gap-2">
            <span>🗳️</span> Secret Ballot & Proxy Tampering
          </div>
          <p class="text-sm text-slate-300">
            Paper ballot slips allow rogue proxies to vote without share-weighted authorization. Manual ballot box tallies lack cryptographic audit trails, inviting contentious election petitions.
          </p>
        </div>
        <div class="p-5 rounded-xl bg-red-950/20 border border-red-900/30">
          <div class="font-bold text-red-400 mb-1 flex items-center gap-2">
            <span>💸</span> Exorbitant Infrastructure Capex
          </div>
          <p class="text-sm text-slate-300">
            Renting proprietary badge printers, local servers, badge lanyards, and specialized scanning wands routinely drains between <b>KES 500,000 and KES 1,500,000</b> for a single one-day event.
          </p>
        </div>
      </div>
    </div>

    <!-- SECTION 2: THE STRIDE SOLUTION ARCHITECTURE -->
    <div class="glass-card rounded-2xl p-8 border border-slate-800 shadow-xl">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-8 h-8 rounded-lg bg-cyan-500/20 text-cyan-400 flex items-center justify-center font-bold text-sm">02</div>
        <h2 class="text-2xl font-bold text-white">The STRIDE™ Solution Architecture</h2>
      </div>
      <p class="text-slate-300 leading-relaxed mb-6">
        STRIDE™ replaces paper chaos and expensive hardware with a lightweight, bank-grade, cloud-native sovereign platform.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="p-5 rounded-xl bg-slate-900/60 border border-cyan-500/30 flex flex-col justify-between">
          <div>
            <div class="text-cyan-400 font-bold text-base mb-2">Zero-Capex Serverless</div>
            <p class="text-xs text-slate-300 leading-relaxed mb-4">
              Built on Streamlit Cloud edge and AWS Frankfurt managed PostgreSQL. Zero local servers, zero licensing fees. Ushers scan credentials using standard smartphones or iPads.
            </p>
          </div>
          <div class="text-[11px] font-mono text-cyan-300 bg-cyan-950/40 p-2 rounded">99.98% High Availability</div>
        </div>

        <div class="p-5 rounded-xl bg-slate-900/60 border border-emerald-500/30 flex flex-col justify-between">
          <div>
            <div class="text-emerald-400 font-bold text-base mb-2">ODPC § 25 Privacy Shield</div>
            <p class="text-xs text-slate-300 leading-relaxed mb-4">
              Automatic dynamic masking of all delegate contact data (<code class="text-amber-300">072* *** *56</code>). 2FA Secretariat passkey reveal with 15-minute auto-relock to eliminate shoulder-surfing.
            </p>
          </div>
          <div class="text-[11px] font-mono text-emerald-300 bg-emerald-950/40 p-2 rounded">Forensic Audit Ledger</div>
        </div>

        <div class="p-5 rounded-xl bg-slate-900/60 border border-amber-500/30 flex flex-col justify-between">
          <div>
            <div class="text-amber-400 font-bold text-base mb-2">SASRA Statutory Quorum</div>
            <p class="text-xs text-slate-300 leading-relaxed mb-4">
              Real-time radar gauge tracking constitutional floor attainment, principal vs. proxy ratios, and gate throughput for instant Returning Officer certification.
            </p>
          </div>
          <div class="text-[11px] font-mono text-amber-300 bg-amber-950/40 p-2 rounded">Companies Act § 284</div>
        </div>

        <div class="p-5 rounded-xl bg-slate-900/60 border border-purple-500/30 flex flex-col justify-between">
          <div>
            <div class="text-purple-400 font-bold text-base mb-2">Multi-Sport Telemetry</div>
            <p class="text-xs text-slate-300 leading-relaxed mb-4">
              Comprehensive 18-sport roster engine (Golf, Football, Chess, Athletics). Instant captain roll-call, pitchside allowance clearance, and zero-ghost athlete verification.
            </p>
          </div>
          <div class="text-[11px] font-mono text-purple-300 bg-purple-950/40 p-2 rounded">Zero-Ghost Athlete Audit</div>
        </div>
      </div>
    </div>

    <!-- SECTION 3: COMMERCIAL PRICING & TIERS -->
    <div class="glass-card rounded-2xl p-8 border border-slate-800 shadow-xl">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-sm">03</div>
        <h2 class="text-2xl font-bold text-white">Transparent Commercial Pricing Models</h2>
      </div>
      <p class="text-slate-300 leading-relaxed mb-8">
        Transparent per-event licensing with zero hidden recurring fees. Pick the tier that matches your assembly scale:
      </p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Tier 1 -->
        <div class="p-6 rounded-2xl bg-slate-900/70 border border-slate-700 flex flex-col justify-between">
          <div>
            <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-1">Entry Tier</div>
            <h3 class="text-xl font-bold text-white mb-2">Society / Sports Club</h3>
            <div class="text-3xl font-extrabold text-white mb-1">KES 15,000</div>
            <div class="text-xs text-slate-400 mb-6">Up to 100 Delegates / Athletes</div>
            <ul class="text-xs text-slate-300 space-y-2.5 border-t border-slate-800 pt-4 mb-6">
              <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Self-Serve Event Creator Wizard</li>
              <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Dynamic QR Passes & Email Dispatch</li>
              <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Live Door Usher Scanner Terminal</li>
              <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Official CSV Attendance Register Export</li>
            </ul>
          </div>
          <div class="text-center py-2 px-3 bg-slate-800 text-slate-300 rounded-lg text-xs font-semibold">Standard Provisioning</div>
        </div>

        <!-- Tier 2 -->
        <div class="p-6 rounded-2xl bg-gradient-to-b from-amber-950/40 to-slate-900/90 border-2 border-amber-400 shadow-xl flex flex-col justify-between relative">
          <div class="absolute -top-3 right-6 bg-amber-400 text-slate-950 text-[10px] font-extrabold px-3 py-1 rounded-full uppercase tracking-wider">
            MOST POPULAR
          </div>
          <div>
            <div class="text-xs font-bold uppercase tracking-wider text-amber-400 mb-1">Regulated Assembly</div>
            <h3 class="text-xl font-bold text-white mb-2">Mid-Sized Corporate / SACCO</h3>
            <div class="text-3xl font-extrabold text-white mb-1">KES 35,000</div>
            <div class="text-xs text-amber-200/80 mb-6">101 – 500 Delegates (Standard AGM)</div>
            <ul class="text-xs text-slate-200 space-y-2.5 border-t border-amber-400/20 pt-4 mb-6">
              <li class="flex items-center gap-2"><span class="text-amber-400">✓</span> <b>All Society Tier Capabilities</b></li>
              <li class="flex items-center gap-2"><span class="text-amber-400">✓</span> SASRA Statutory Quorum Radar Gauge</li>
              <li class="flex items-center gap-2"><span class="text-amber-400">✓</span> Principal vs. Proxy Distribution Telemetry</li>
              <li class="flex items-center gap-2"><span class="text-amber-400">✓</span> Decoupled Secret Ballot (3 Resolutions)</li>
              <li class="flex items-center gap-2"><span class="text-amber-400">✓</span> Kenya DPA 2019 Masking & 2FA RBAC</li>
              <li class="flex items-center gap-2"><span class="text-amber-400">✓</span> Dedicated Remote Concierge Tech Support</li>
            </ul>
          </div>
          <div class="text-center py-2 px-3 bg-amber-400 text-slate-950 rounded-lg text-xs font-bold">Recommended for SACCO AGMs</div>
        </div>

        <!-- Tier 3 -->
        <div class="p-6 rounded-2xl bg-slate-900/70 border border-cyan-500/50 flex flex-col justify-between">
          <div>
            <div class="text-xs font-bold uppercase tracking-wider text-cyan-400 mb-1">Enterprise Sovereign</div>
            <h3 class="text-xl font-bold text-white mb-2">Large Listed PLC / Tier-1</h3>
            <div class="text-3xl font-extrabold text-white mb-1">KES 75,000</div>
            <div class="text-xs text-slate-400 mb-6">501 – 2,500+ Delegates (Multi-Gate)</div>
            <ul class="text-xs text-slate-300 space-y-2.5 border-t border-slate-800 pt-4 mb-6">
              <li class="flex items-center gap-2"><span class="text-cyan-400">✓</span> <b>All Mid-Sized Tier Capabilities</b></li>
              <li class="flex items-center gap-2"><span class="text-cyan-400">✓</span> Multi-Gate Dual Usher Synchronizer</li>
              <li class="flex items-center gap-2"><span class="text-cyan-400">✓</span> Share-Weighted Governance & Voting Matrix</li>
              <li class="flex items-center gap-2"><span class="text-cyan-400">✓</span> Dedicated AWS Frankfurt High-Throughput Node</li>
              <li class="flex items-center gap-2"><span class="text-cyan-400">✓</span> White-Glove On-Site Returning Officer Concierge</li>
              <li class="flex items-center gap-2"><span class="text-cyan-400">✓</span> Post-Event Forensic Statutory Audit Dossier</li>
            </ul>
          </div>
          <div class="text-center py-2 px-3 bg-cyan-950 text-cyan-300 border border-cyan-500/40 rounded-lg text-xs font-semibold">Maximum Throughput</div>
        </div>
      </div>
    </div>

    <!-- SECTION 4: FORMAL ACCEPTANCE & AUTHORIZATION -->
    <div class="glass-card rounded-2xl p-8 border border-slate-800 shadow-xl">
      <div class="flex items-center gap-3 mb-6">
        <div class="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-sm">04</div>
        <h2 class="text-2xl font-bold text-white">Commercial Acceptance & Project Authorization</h2>
      </div>
      <p class="text-slate-300 leading-relaxed mb-6 text-sm">
        To commission STRIDE™ for your upcoming statutory AGM, special delegate conference, or tournament, please complete this authorization block:
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 p-6 rounded-xl bg-slate-900/90 border border-slate-800">
        <div class="space-y-4">
          <div class="text-sm font-bold text-amber-400 uppercase tracking-wider border-b border-slate-800 pb-2">Client Authorization</div>
          <div>
            <label class="block text-xs text-slate-400 uppercase font-semibold mb-1">Client Entity / Institution Name</label>
            <div class="h-10 rounded border border-slate-700 bg-slate-950/60 px-3 flex items-center text-sm text-slate-400">__________________________________________</div>
          </div>
          <div>
            <label class="block text-xs text-slate-400 uppercase font-semibold mb-1">Authorized Executive Name & Title</label>
            <div class="h-10 rounded border border-slate-700 bg-slate-950/60 px-3 flex items-center text-sm text-slate-400">__________________________________________</div>
          </div>
          <div>
            <label class="block text-xs text-slate-400 uppercase font-semibold mb-1">Selected Commercial Tier</label>
            <div class="flex items-center gap-4 text-xs text-slate-300 pt-1">
              <span>[ &nbsp; ] Society (15k)</span>
              <span>[ &nbsp; ] Mid-Sized SACCO (35k)</span>
              <span>[ &nbsp; ] PLC (75k)</span>
            </div>
          </div>
          <div>
            <label class="block text-xs text-slate-400 uppercase font-semibold mb-1">Authorized Executive Signature & Date</label>
            <div class="h-14 rounded border border-slate-700 bg-slate-950/60 px-3 flex items-center text-sm text-slate-400">Sign: ____________________ Date: ________</div>
          </div>
        </div>

        <div class="space-y-4">
          <div class="text-sm font-bold text-cyan-400 uppercase tracking-wider border-b border-slate-800 pb-2">STRIDE™ Platform Acceptance</div>
          <div>
            <label class="block text-xs text-slate-400 uppercase font-semibold mb-1">Platform Organization</label>
            <div class="text-sm text-white font-semibold">STRIDE™ Sovereign Governance Technologies</div>
          </div>
          <div>
            <label class="block text-xs text-slate-400 uppercase font-semibold mb-1">Production URL</label>
            <div class="text-sm text-cyan-400 font-mono">https://cbk-stride.streamlit.app</div>
          </div>
          <div>
            <label class="block text-xs text-slate-400 uppercase font-semibold mb-1">Accreditation Reference</label>
            <div class="text-sm text-amber-300 font-mono">STRIDE-ENT-PROPOSAL-2026/27</div>
          </div>
          <div>
            <label class="block text-xs text-slate-400 uppercase font-semibold mb-1">Platform Execution Officer</label>
            <div class="text-sm text-slate-300">Lead Enterprise Architect • Samuel Gathigi</div>
            <div class="text-xs text-emerald-400 mt-1">Verified & Provisioned in Production</div>
          </div>
        </div>
      </div>
    </div>

    <!-- FOOTER -->
    <div class="text-center text-xs text-slate-400 py-6 border-t border-slate-800">
      <p>© 2026 STRIDE™ Sovereign Technologies. All Rights Reserved.</p>
      <p class="mt-1">In Partnership with Central Bank of Kenya Sports Club & Banki Kuu Staff SACCO Society.</p>
    </div>

  </div>
</body>
</html>
"""
    with open(html_proj, "w", encoding="utf-8") as f:
        f.write(html_content)
    shutil.copy2(html_proj, html_art)
    print(f"✓ Executive Interactive HTML Proposal Generated: {html_proj}")

if __name__ == "__main__":
    build_pdf_proposal()
    build_html_proposal()

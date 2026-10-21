"""
Generate high-resolution PDF Slide Deck for Bank of Uganda Cyber Forensics Masterclass
"""
import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

output_pdf = r"C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics\Bank_of_Uganda_Cyber_Forensics_Masterclass.pdf"

doc = SimpleDocTemplate(
    output_pdf,
    pagesize=landscape(letter),
    rightMargin=40,
    leftMargin=40,
    topMargin=35,
    bottomMargin=35
)

styles = getSampleStyleSheet()

# Custom styles
navy = colors.HexColor("#0A192F")
dark_blue = colors.HexColor("#0F2B48")
gold = colors.HexColor("#C5A059")
white = colors.HexColor("#FFFFFF")
light_gray = colors.HexColor("#CBD5E1")

style_eyebrow = ParagraphStyle(
    "Eyebrow",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=11,
    textColor=gold,
    spaceAfter=4,
    textTransform="uppercase"
)

style_title = ParagraphStyle(
    "Title",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=22,
    textColor=white,
    spaceAfter=15
)

style_bullet = ParagraphStyle(
    "Bullet",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=13,
    textColor=light_gray,
    leading=18,
    spaceAfter=10
)

slides_data = [
    {
        "eyebrow": "BANK OF UGANDA | EXECUTIVE MASTERCLASS",
        "title": "5-Day Cyber Forensics & Security Investigations",
        "bullets": [
            "<b>Institutional Mandate:</b> Guarding Uganda's sovereign payment rails, RTGS, and interbank settlement interfaces.",
            "<b>Complete Forensic Lifecycle:</b> Evidence seizure, RAM volatile extraction, C2 telemetry, containment & judicial reporting.",
            "<b>Statutory Defensibility:</b> Built upon Uganda Computer Misuse Act (2011/2022) & Electronic Signatures Act 2011.",
            "<b>Hands-on Case Study:</b> 'Operation Crested Crane' 4.8 Billion UGX settlement breach drill."
        ]
    },
    {
        "eyebrow": "DAY 1: FOUNDATIONS & EVIDENTIARY INTEGRITY",
        "title": "Principles of Forensic Soundness & Order of Volatility",
        "bullets": [
            "<b>Order of Volatility (RFC 3227):</b> CPU Registers -> RAM -> Swap -> NVMe/SAN -> Backup Tapes.",
            "<b>ISO/IEC 27037 Compliance:</b> Never analyze original evidence; duplicate bitstreams under hardware write-blockers.",
            "<b>Cryptographic Redundancy:</b> Simultaneous dual hashing (SHA-256 + MD5) to guarantee immutability.",
            "<b>Forensic Trap Alert:</b> Binary mode ('wb' / 'rb') capture prevents OS CRLF conversion from corrupting legal hashes."
        ]
    },
    {
        "eyebrow": "DAY 2: NETWORK FORENSICS & TELEMETRY",
        "title": "Financial Cyber Attack Vectors & Beacon Dissection",
        "bullets": [
            "<b>C2 Beacon Statistical Triage:</b> Low jitter (&lt; 0.15) flags automated beacon heartbeats vs. organic human browsing.",
            "<b>Payment Gateway Probes:</b> Detecting unauthorized outbound wire payloads and rogue beneficiary IDs.",
            "<b>Protocol Telemetry:</b> Full packet dissection (Wireshark), Zeek metadata logs, and TLS JA3/JA4 fingerprinting.",
            "<b>Lateral Movement Detection:</b> Kerberoasting, Pass-the-Hash, and PsExec activity in financial subnets."
        ]
    },
    {
        "eyebrow": "DAY 3: HOST ARTIFACTS & MEMORY FORENSICS",
        "title": "Forensic Imaging & Volatile Memory Triage",
        "bullets": [
            "<b>Volatile RAM Forensics (Volatility 3):</b> Inspecting unlinked stealth processes ('psscan') and injected DLLs ('malfind').",
            "<b>Windows Endpoint Forensics:</b> $MFT timestamps, Prefetch execution traces, Shimcache, and Event ID 4624/4688 logs.",
            "<b>Anti-Forensics Unmasking:</b> Identifying timestomping ($STANDARD_INFO vs $FILE_NAME discrepancies).",
            "<b>Data Carving & Extraction:</b> Reconstructing deleted transactions and temporary staging buffers."
        ]
    },
    {
        "eyebrow": "DAY 4: INCIDENT RESPONSE & FINANCIAL MALWARE",
        "title": "BoU CSIRT Playbooks & Reverse Engineering Triage",
        "bullets": [
            "<b>Containment Without Reboot:</b> Isolating infected hosts on VLANs to safeguard volatile in-memory evidence.",
            "<b>Active Directory Eviction:</b> Golden Ticket eradication via dual 'krbtgt' password rotation within 10 hours.",
            "<b>Banking Trojan Anatomy:</b> Web-injects, credential scraping, and in-memory payment API hooking.",
            "<b>Threat Signature Engineering:</b> Writing custom YARA rules targeting financial malware strings and headers."
        ]
    },
    {
        "eyebrow": "DAY 5: UGANDA CYBER LAWS & REPORTING",
        "title": "Statutory Admissibility & Executive Briefings",
        "bullets": [
            "<b>Uganda Computer Misuse Act (2011/2022):</b> Section 12 (Unauthorized Access), Section 15 (Modification), Section 20 (Fraud).",
            "<b>Data Protection and Privacy Act 2019:</b> Ensuring custody handling safeguards non-incident financial data.",
            "<b>Courtroom Testimony Standards:</b> Demonstrating unbroken chain of custody and scientifically validated toolsets.",
            "<b>Executive Dossier Delivery:</b> Briefing the Governor, Board Audit Committee, and Judicial Prosecutors."
        ]
    }
]

elements = []

for idx, slide in enumerate(slides_data):
    card_content = []
    card_content.append(Paragraph(slide["eyebrow"], style_eyebrow))
    card_content.append(Paragraph(slide["title"], style_title))
    card_content.append(Spacer(1, 10))
    for b in slide["bullets"]:
        card_content.append(Paragraph(f"• &nbsp; {b}", style_bullet))

    table = Table([[card_content]], colWidths=[712], rowHeights=[490])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), dark_blue),
        ('BOX', (0,0), (-1,-1), 1.5, gold),
        ('TOPPADDING', (0,0), (-1,-1), 25),
        ('BOTTOMPADDING', (0,0), (-1,-1), 25),
        ('LEFTPADDING', (0,0), (-1,-1), 35),
        ('RIGHTPADDING', (0,0), (-1,-1), 35),
    ]))
    
    elements.append(table)

def draw_background(canvas, document):
    canvas.saveState()
    canvas.setFillColor(navy)
    canvas.rect(0, 0, document.pagesize[0], document.pagesize[1], fill=1, stroke=0)
    canvas.setFillColor(gold)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(45, 18, "BANK OF UGANDA © 2026 • CYBER FORENSICS MASTERCLASS")
    canvas.drawRightString(document.pagesize[0] - 45, 18, f"Page {canvas.getPageNumber()} of {len(slides_data)}")
    canvas.restoreState()

doc.build(elements, onFirstPage=draw_background, onLaterPages=draw_background)
print(f"PDF Slide Deck generated at: {output_pdf}")

"""
Generate high-fidelity PowerPoint slide deck for Bank of Uganda Masterclass
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette: BoU Navy and Gold
NAVY = RGBColor(10, 25, 47)
GOLD = RGBColor(197, 160, 89)
WHITE = RGBColor(255, 255, 255)
LIGHT_GRAY = RGBColor(203, 213, 225)
DARK_CARD = RGBColor(15, 43, 72)

slides_data = [
    {
        "eyebrow": "BANK OF UGANDA | EXECUTIVE MASTERCLASS",
        "title": "5-Day Cyber Forensics & Security Investigations",
        "bullets": [
            "Institutional mandate: Protecting sovereign payments, RTGS, and interbank infrastructure.",
            "Complete forensic lifecycle: Evidence seizure, RAM analysis, C2 telemetry, containment & court reporting.",
            "Statutory defensibility: Uganda Computer Misuse Act (2011/2022) & Electronic Signatures Act 2011.",
            "Hands-on case study: 'Operation Crested Crane' 4.8 Billion UGX settlement breach drill."
        ]
    },
    {
        "eyebrow": "DAY 1: FOUNDATIONS & EVIDENTIARY INTEGRITY",
        "title": "Principles of Forensic Soundness & Order of Volatility",
        "bullets": [
            "Order of Volatility (RFC 3227): CPU Registers -> RAM -> Swap -> NVMe/SAN -> Backup Tapes.",
            "ISO/IEC 27037 Compliance: Never analyze original evidence; duplicate bitstreams under hardware write-blockers.",
            "Cryptographic Redundancy: Simultaneous dual hashing (SHA-256 + MD5) to guarantee immutability.",
            "Forensic Trap Alert: Binary mode ('wb' / 'rb') capture prevents OS CRLF conversion from corrupting hashes."
        ]
    },
    {
        "eyebrow": "DAY 2: NETWORK FORENSICS & TELEMETRY",
        "title": "Financial Cyber Attack Vectors & Beacon Dissection",
        "bullets": [
            "C2 Beacon Statistical Triage: Low jitter (< 0.15) flags automated beacon heartbeats vs. human browsing.",
            "Payment Gateway Probes: Detecting unauthorized outbound wire payloads and rogue beneficiary IDs.",
            "Protocol Telemetry: Full packet dissection (Wireshark), Zeek metadata logs, and TLS JA3/JA4 fingerprinting.",
            "Lateral Movement Detection: Kerberoasting, Pass-the-Hash, and PsExec activity in financial subnets."
        ]
    },
    {
        "eyebrow": "DAY 3: HOST ARTIFACTS & MEMORY FORENSICS",
        "title": "Forensic Imaging & Volatile Memory Triage",
        "bullets": [
            "Volatile RAM Forensics (Volatility 3): Inspecting unlinked stealth processes ('psscan') and injected DLLs ('malfind').",
            "Windows Endpoint Forensics: $MFT timestamps, Prefetch execution traces, Shimcache, and Event ID 4624/4688 logs.",
            "Anti-Forensics Unmasking: Identifying timestomping ($STANDARD_INFO vs $FILE_NAME discrepancies).",
            "Data Carving & Extraction: Reconstructing deleted transactions and temporary staging buffers."
        ]
    },
    {
        "eyebrow": "DAY 4: INCIDENT RESPONSE & FINANCIAL MALWARE",
        "title": "BoU CSIRT Playbooks & Reverse Engineering Triage",
        "bullets": [
            "Containment Without Reboot: Isolating infected hosts on VLANs to safeguard volatile in-memory evidence.",
            "Active Directory Eviction: Golden Ticket eradication via dual 'krbtgt' password rotation within 10 hours.",
            "Banking Trojan Anatomy: Web-injects, credential scraping, and in-memory payment API hooking.",
            "Threat Signature Engineering: Writing custom YARA rules targeting financial malware strings and headers."
        ]
    },
    {
        "eyebrow": "DAY 5: UGANDA CYBER LAWS & REPORTING",
        "title": "Statutory Admissibility & Executive Briefings",
        "bullets": [
            "Uganda Computer Misuse Act (2011/2022): Section 12 (Unauthorized Access), Section 15 (Modification), Section 20 (Fraud).",
            "Data Protection and Privacy Act 2019: Ensuring custody handling safeguards non-incident financial data.",
            "Courtroom Testimony Standards: Demonstrating unbroken chain of custody and scientifically validated toolsets.",
            "Executive Dossier Delivery: Briefing the Governor, Board Audit Committee, and Judicial Prosecutors."
        ]
    }
]

for item in slides_data:
    slide = prs.slides.add_slide(prs.slide_layouts[6]) # blank layout
    
    # Background fill
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = NAVY

    # Header Eyebrow
    tx_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.3), Inches(0.5))
    tf = tx_box.text_frame
    p_eye = tf.paragraphs[0]
    p_eye.text = item["eyebrow"]
    p_eye.font.size = Pt(13)
    p_eye.font.bold = True
    p_eye.font.color.rgb = GOLD

    # Title
    p_title = tf.add_paragraph()
    p_title.text = item["title"]
    p_title.font.size = Pt(28)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE
    p_title.space_before = Pt(8)

    # Bullet content card
    shape = slide.shapes.add_shape(
        1, # MSO_SHAPE.RECTANGLE
        Inches(1.0), Inches(2.2), Inches(11.3), Inches(4.3)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_CARD
    shape.line.color.rgb = GOLD
    shape.line.width = Pt(1.5)

    tf_bullets = shape.text_frame
    tf_bullets.word_wrap = True
    tf_bullets.margin_left = Inches(0.4)
    tf_bullets.margin_top = Inches(0.4)
    tf_bullets.margin_right = Inches(0.4)

    for i, bullet in enumerate(item["bullets"]):
        p = tf_bullets.paragraphs[0] if i == 0 else tf_bullets.add_paragraph()
        p.text = f"•   {bullet}"
        p.font.size = Pt(17)
        p.font.color.rgb = LIGHT_GRAY
        p.space_before = Pt(14)

output_path = r"C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics\Bank_of_Uganda_Cyber_Forensics_Masterclass.pptx"
prs.save(output_path)
print(f"Presentation saved successfully to: {output_path}")

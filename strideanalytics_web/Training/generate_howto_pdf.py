"""
Compile HOWTO_MASTERCLASS_TRAINER_GUIDE.md into a high-resolution PDF document
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

output_pdf = r"C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics\HOWTO_MASTERCLASS_TRAINER_GUIDE.pdf"

doc = SimpleDocTemplate(
    output_pdf,
    pagesize=letter,
    rightMargin=45,
    leftMargin=45,
    topMargin=45,
    bottomMargin=45
)

styles = getSampleStyleSheet()

navy = colors.HexColor("#0A192F")
gold = colors.HexColor("#C5A059")
dark_blue = colors.HexColor("#0F2B48")
slate = colors.HexColor("#334155")

style_title = ParagraphStyle(
    "Title",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=18,
    textColor=navy,
    spaceAfter=4
)

style_subtitle = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=11,
    textColor=gold,
    spaceAfter=15,
    textTransform="uppercase"
)

style_h1 = ParagraphStyle(
    "Heading1",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=13,
    textColor=navy,
    spaceBefore=12,
    spaceAfter=6
)

style_body = ParagraphStyle(
    "Body",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9.5,
    textColor=slate,
    leading=14,
    spaceAfter=6
)

style_bullet = ParagraphStyle(
    "Bullet",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9,
    textColor=slate,
    leading=13,
    leftIndent=15,
    spaceAfter=4
)

story = []

# Title & Metadata
story.append(Paragraph("BANK OF UGANDA // CYBER FORENSICS MASTERCLASS", style_subtitle))
story.append(Paragraph("Trainer & Participant How-To Operating Manual", style_title))
story.append(Paragraph("<i>Comprehensive facilitation guide for delivering the 5-day sovereign cyber forensics curriculum, tabletop war room, and PII privacy engine.</i>", style_body))
story.append(HRFlowable(width="100%", thickness=1.5, color=gold, spaceBefore=8, spaceAfter=14))

# Section 1
story.append(Paragraph("1. Executive Masterclass Architecture & Live Resources", style_h1))
story.append(Paragraph("All interactive web simulators, slide decks, and participant exercises are hosted on the live sovereign portal at <b>https://strideanalytics.co.ke/Training/</b>.", style_body))
story.append(Paragraph("• <b>Main Interactive Slides:</b> https://strideanalytics.co.ke/Training/", style_bullet))
story.append(Paragraph("• <b>War Room & Tabletop Simulator (TTX):</b> https://strideanalytics.co.ke/Training/war_room_simulator.html", style_bullet))
story.append(Paragraph("• <b>CyberForensic Chef & PII Shield:</b> https://strideanalytics.co.ke/Training/cyber_forensic_chef.html", style_bullet))
story.append(Paragraph("• <b>Boardroom Presentation PDF:</b> Bank_of_Uganda_Cyber_Forensics_Masterclass.pdf", style_bullet))

# Section 2
story.append(Spacer(1, 8))
story.append(Paragraph("2. 5-Day Curriculum Facilitation Plan", style_h1))
story.append(Paragraph("<b>Day 1 (Foundations & Threat Modeling):</b> Guide participants through the Order of Volatility (RFC 3227) and ISO/IEC 27037. Run <code>evidence_integrity_verifier.py</code>. Crucial lesson: Binary capture mode (wb/rb) avoids OS CRLF corruption of SHA-256 hashes.", style_body))
story.append(Paragraph("<b>Day 2 (Attack Vectors & Network Forensics):</b> Run <code>network_pcap_analyzer.py</code>. Explain statistical Jitter ratio (automated bot beacons exhibit low jitter &lt; 0.15, while human browsing shows high variance &gt; 1.0).", style_body))
story.append(Paragraph("<b>Day 3 (Forensic Tools & Memory Triage):</b> Use the <b>Tools & Workbench</b> tab. In Volatility 3, execute <code>pslist</code> and <code>malfind</code> to unmask the dual-sign bypass hook on PID 4128. Inspect Wireshark hex frames.", style_body))
story.append(Paragraph("<b>Day 4 (Incident Response & Malware Reverse Triage):</b> Guide participants through NIST SP 800-61 containment lifecycles, Kerberos Golden Ticket eviction, and interactive YARA signature compilation.", style_body))
story.append(Paragraph("<b>Day 5 (Uganda Cyber Laws & Judicial Reporting):</b> Audit findings against the <b>Uganda Computer Misuse Act (2011/2022)</b> and <b>Data Protection Act 2019</b>. Demonstrate one-click dossier printing for the Governor.", style_body))

# Section 3
story.append(Spacer(1, 8))
story.append(Paragraph("3. How to Run the War Room Tabletop Simulator (8 Scenarios)", style_h1))
story.append(Paragraph("In <b>Mod 5: Incident Playbooks</b>, click the <b>'🎲 Random Incident Drill'</b> button. The simulator randomly triggers one of 8 crisis scenarios across payment rails, cloud APIs, ransomware, AI voice deepfakes, or supply chain attacks. Have teams select choices under time pressure, watching their live Score and Court Admissibility Index update in real time.", style_body))

# Section 4
story.append(Spacer(1, 8))
story.append(Paragraph("4. How to Use the CyberForensic Chef & PII Privacy Shield", style_h1))
story.append(Paragraph("Access the standalone app at <b>https://strideanalytics.co.ke/Training/cyber_forensic_chef.html</b>. To demonstrate malware deobfuscation, click 'Load Obfuscated Malware' and bake the Base64 + IoC + Entropy recipe. To demonstrate the power of PII privacy under the Uganda Data Protection Act 2019, click 'Load Dirty Bank PII Log' and apply Uganda NIN, phone, and account masking, plus Differential Privacy Laplace noise. Show participants how innocent citizen records are shielded without losing evidentiary value.", style_body))

# Section 5
story.append(Spacer(1, 8))
story.append(Paragraph("5. Cross-Border Threat Intel & Federated Learning (BoU ↔ CBK)", style_h1))
story.append(Paragraph("Open the <b>'🇰🇪 ↔ 🇺🇬 Regional Intel & Federated AI'</b> tab. Walk through equivalent Kenyan incidents (Apex SACCO B2C heist, eCitizen DDoS smokescreen, SIM-swap OTP interception). Click 'Execute Cross-Border Federated Learning Round' to demonstrate how BoU and CBK can collaboratively train sovereign threat models to achieve <b>98.6% zero-day detection</b> with <b>0.00 KB raw customer data transferred</b>.", style_body))

doc.build(story)
print(f"HOWTO PDF generated successfully at: {output_pdf}")

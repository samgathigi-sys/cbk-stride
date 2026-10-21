"""
Generate PDF document for CyberChef & PII Train-the-Trainer Guide
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

output_pdf = r"C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics\CYBERCHEF_AND_PII_TRAIN_THE_TRAINER_GUIDE.pdf"

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
emerald = colors.HexColor("#059669")

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
    spaceBefore=14,
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

story.append(Paragraph("BANK OF UGANDA // TRAIN-THE-TRAINER SPECIAL GUIDE", style_subtitle))
story.append(Paragraph("Mastering CyberForensic Chef & The PII Shield", style_title))
story.append(Paragraph("<i>A 10-Minute Facilitator Primer & Step-by-Step Script for the 5-Day Cyber Forensics Masterclass.</i>", style_body))
story.append(HRFlowable(width="100%", thickness=1.5, color=gold, spaceBefore=8, spaceAfter=14))

# Section 1
story.append(Paragraph("1. What Exactly is CyberChef? (The 60-Second Mental Model)", style_h1))
story.append(Paragraph("Think of CyberChef as an <b>assembly line for digital evidence</b>. Originally built and open-sourced by <b>GCHQ</b> (the UK's intelligence agency), it uses a cooking metaphor: you provide raw ingredients (scrambled malware or dirty bank logs), choose operations (decoders, filters, PII shields), assemble a recipe, and bake it to produce clean, decoded, court-admissible evidence.", style_body))

# Section 2
story.append(Spacer(1, 6))
story.append(Paragraph("2. Core Concepts Translated for Facilitators", style_h1))
story.append(Paragraph("• <b>Base64 / Hex:</b> Standard ways attackers encode binary files to slip past bank firewalls and email scanners.", style_bullet))
story.append(Paragraph("• <b>Shannon Entropy (0.0 to 8.0):</b> Mathematical measure of randomness. Text is ~4.0; packed malware is <b>> 7.0</b> (instant red flag!).", style_bullet))
story.append(Paragraph("• <b>Defanging:</b> Turning live malicious URLs into safe text (e.g. <code>hxxp://malware[.]com</code>) so no one accidentally clicks them in reports.", style_bullet))
story.append(Paragraph("• <b>HMAC Tokenization:</b> Replacing innocent citizen names with irreversible cryptographic hashes, allowing courts to trace money flows without leaking identities.", style_bullet))
story.append(Paragraph("• <b>Differential Privacy (&epsilon;):</b> Injecting Laplace statistical noise so aggregate reconciliation is verified without revealing any individual account balance.", style_bullet))

# Section 3
story.append(Spacer(1, 6))
story.append(Paragraph("3. Live Exercise 1: Malware Deobfuscation Walkthrough", style_h1))
story.append(Paragraph("<b>Script to Room:</b> <i>'Class, our SOC found this suspicious file in C:\\Windows\\Temp. Let us unmask what the attacker was running.'</i>", style_body))
story.append(Paragraph("1. Open: <b>https://strideanalytics.co.ke/Training/cyber_forensic_chef.html</b>", style_bullet))
story.append(Paragraph("2. Click the red button: <b>'Load Obfuscated Malware'</b>.", style_bullet))
story.append(Paragraph("3. Show the room the recipe: <code>From Base64</code> &rarr; <code>Extract IoCs</code> &rarr; <code>Shannon Entropy Analysis</code>.", style_bullet))
story.append(Paragraph("4. Click <b>'Bake &amp; Execute Recipe'</b>. Point out the <b>'MZ'</b> executable header and the high entropy score (7.14/8.00). You just proved it was an executable financial trojan!", style_bullet))

# Section 4
story.append(Spacer(1, 6))
story.append(Paragraph("4. Live Exercise 2: The Sovereign PII Privacy Shield Walkthrough", style_h1))
story.append(Paragraph("<b>Script to Room:</b> <i>'CID detectives subpoenaed our transaction logs. But they contain thousands of innocent Ugandan citizen NINs and phone numbers. If we hand this over unredacted, Bank of Uganda violates the Data Protection and Privacy Act 2019. Here is how we protect citizens while keeping evidence court-admissible.'</i>", style_body))
story.append(Paragraph("1. Click the cyan button: <b>'Load Dirty Bank PII Log'</b>. Show the real Ugandan NINs (CM88019234KL12) and phone numbers.", style_bullet))
story.append(Paragraph("2. Show the recipe: <code>Shield Uganda NIN</code> &rarr; <code>Mask Accounts</code> &rarr; <code>Mask Phones</code> &rarr; <code>HMAC Tokenize</code>.", style_bullet))
story.append(Paragraph("3. Click <b>'Bake &amp; Execute Recipe'</b>. Show how all citizen PII is masked, while the criminal C2 IP (194.26.29.11) and transaction amounts remain intact. The compliance badge turns bright green: <b>100% PROTECTED ✓</b>.", style_bullet))

doc.build(story)
print(f"CyberChef Train-the-Trainer PDF generated at: {output_pdf}")

"""
Dispatch the CyberChef Train-the-Trainer Guide to sam.gathigi@gmail.com
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr, formatdate, make_msgid
import os

PDF_PATH = r"C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics\CYBERCHEF_AND_PII_TRAIN_THE_TRAINER_GUIDE.pdf"
recipient_email = "sam.gathigi@gmail.com"
recipient_name = "Samuel N. Gathigi"

subject = "TRAIN-THE-TRAINER // MASTERING CYBERCHEF & THE PII PRIVACY SHIELD (10-MIN PRIMER)"

html_body = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin: 0; padding: 25px; background-color: #030712; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #f8fafc; line-height: 1.6;">
    <div style="max-width: 680px; margin: 0 auto; background: #0a1124; border: 1px solid rgba(197, 160, 89, 0.4); border-radius: 16px; padding: 32px; box-shadow: 0 20px 60px rgba(0,0,0,0.9);">
        
        <div style="border-bottom: 2px solid #c5a059; padding-bottom: 20px; margin-bottom: 24px;">
            <div style="font-size: 11px; font-weight: 800; color: #c5a059; text-transform: uppercase; letter-spacing: 2px; font-family: monospace;">
                INSTRUCTOR PRIMER &bull; BANK OF UGANDA MASTERCLASS &bull; OCTOBER 2026
            </div>
            <h1 style="margin: 8px 0 4px 0; font-size: 22px; font-weight: 900; color: #ffffff;">
                Train-the-Trainer: Mastering CyberForensic Chef &amp; PII Privacy
            </h1>
            <div style="font-size: 13px; color: #38bdf8; font-family: monospace; font-weight: bold;">
                Everything You Need to Know Before Facilitating the Hands-On Labs
            </div>
        </div>

        <p style="font-size: 14.5px; color: #ffffff; margin-bottom: 16px;">
            Dear <strong>Samuel</strong>,
        </p>

        <p style="font-size: 13.5px; color: #cbd5e1; margin-bottom: 20px; line-height: 1.7;">
            Here is your dedicated <strong>Train-the-Trainer Primer</strong> for CyberChef and the Sovereign PII Privacy Shield. It breaks down the mental model, translates the technical jargon into plain English, and provides exact step-by-step scripts for the two live classroom exercises.
        </p>

        <!-- Quick 60-second Mental Model -->
        <div style="background: #040914; border: 1px solid rgba(197, 160, 89, 0.3); border-radius: 12px; padding: 18px; margin: 20px 0;">
            <div style="font-size: 12px; font-weight: 800; color: #c5a059; text-transform: uppercase; font-family: monospace; margin-bottom: 8px;">
                💡 The 60-Second CyberChef Mental Model (The Kitchen Metaphor)
            </div>
            <div style="font-size: 13px; color: #cbd5e1; line-height: 1.7;">
                Attackers scramble malicious payloads (Base64, Hex, XOR) so bank security can't read them. In CyberChef:
                <ul style="padding-left: 20px; margin: 8px 0;">
                    <li><strong>Ingredients (Input):</strong> Raw scrambled payload or dirty bank logs.</li>
                    <li><strong>Recipe (Operations):</strong> The steps you stack (Decode Base64 &rarr; Extract IPs &rarr; Mask NINs).</li>
                    <li><strong>Bake (Execute):</strong> CyberChef executes the chain and outputs clean, decoded, court-admissible evidence.</li>
                </ul>
            </div>
        </div>

        <!-- The Two Classroom Exercises -->
        <h2 style="font-size: 15px; font-weight: 800; color: #ffffff; margin-top: 20px; margin-bottom: 10px;">
            🎯 The 2 Live Demos to Run in Class:
        </h2>

        <div style="background: rgba(225, 29, 72, 0.1); border: 1px solid #e11d48; border-radius: 10px; padding: 14px; margin-bottom: 14px;">
            <strong style="color: #fda4af; font-size: 13px;">Exercise 1: Malware Deobfuscation (5 Mins)</strong>
            <p style="font-size: 12.5px; color: #fecaca; margin: 6px 0 0 0; line-height: 1.6;">
                1. Click <code>Load Obfuscated Malware</code>.<br>
                2. Show the room the scrambled text. Click <code>⚡ Bake &amp; Execute Recipe</code>.<br>
                3. Point out the <strong>'MZ'</strong> header (proving it was a hidden Windows executable) and the <strong>Shannon Entropy Score (7.14/8.00)</strong> proving encrypted malware!
            </p>
        </div>

        <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 10px; padding: 14px; margin-bottom: 20px;">
            <strong style="color: #6ee7b7; font-size: 13px;">Exercise 2: The Sovereign PII Privacy Shield (5 Mins)</strong>
            <p style="font-size: 12.5px; color: #d1fae5; margin: 6px 0 0 0; line-height: 1.6;">
                1. Click <code>Load Dirty Bank PII Log</code>. Show real citizen Ugandan NINs (<code>CM88...</code>) and phone numbers.<br>
                2. Click <code>⚡ Bake &amp; Execute Recipe</code>.<br>
                3. Show how citizen PII is masked, while the criminal C2 IP (<code>194.26.29.11</code>) remains visible. Point to the green compliance badge: <strong>100% PROTECTED ✓</strong> under the Uganda Data Protection and Privacy Act 2019!
            </p>
        </div>

        <p style="font-size: 13.5px; color: #cbd5e1; margin-bottom: 20px;">
            The complete <strong>PDF Guide</strong> is attached to this email. You can also run the tool live right now:
        </p>

        <div style="text-align: center; margin: 25px 0;">
            <a href="https://strideanalytics.co.ke/Training/cyber_forensic_chef.html" style="background: linear-gradient(135deg, #c5a059, #e6be75); color: #040914; font-weight: 800; font-size: 14px; text-decoration: none; padding: 12px 28px; border-radius: 8px; display: inline-block;">
                🚀 Open CyberForensic Chef &amp; Practice Live
            </a>
        </div>

        <p style="font-size: 12.5px; color: #94a3b8; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 14px;">
            Warm regards,<br>
            <strong>Antigravity Pair Programmer &amp; Masterclass Engineering Desk</strong>
        </p>
    </div>
</body>
</html>
"""

plain_body = """TRAIN-THE-TRAINER: MASTERING CYBERCHEF & PII PRIVACY
=====================================================

Dear Samuel,

Here is your 10-Minute Facilitator Primer for mastering and teaching CyberForensic Chef and the Sovereign PII Privacy Shield at the Bank of Uganda masterclass.

Live Tool URL: https://strideanalytics.co.ke/Training/cyber_forensic_chef.html

The complete PDF Train-the-Trainer Guide is attached!

Warm regards,
Antigravity Engineering Desk
"""

def send():
    print(f"Connecting to Gmail SMTP gateway to deliver to {recipient_email}...")
    server = smtplib.SMTP("smtp.gmail.com", 587, timeout=25)
    server.starttls()
    server.login("sam.gathigi@gmail.com", "kdjk tscr kxgb pjwh")

    msg = MIMEMultipart("mixed")
    msg["From"] = formataddr(("Bank of Uganda Masterclass Desk", "sam.gathigi@gmail.com"))
    msg["To"] = formataddr((recipient_name, recipient_email))
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="gmail.com")

    alt_part = MIMEMultipart("alternative")
    alt_part.attach(MIMEText(plain_body, "plain", "utf-8"))
    alt_part.attach(MIMEText(html_body, "html", "utf-8"))
    msg.attach(alt_part)

    if os.path.exists(PDF_PATH):
        with open(PDF_PATH, "rb") as f:
            part = MIMEBase("application", "pdf")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", 'attachment; filename="CYBERCHEF_AND_PII_TRAIN_THE_TRAINER_GUIDE.pdf"')
            msg.attach(part)
        print("Attached CyberChef Train-the-Trainer PDF.")

    server.sendmail("sam.gathigi@gmail.com", [recipient_email], msg.as_string())
    server.quit()
    print(f"SUCCESS: Train-the-Trainer Guide delivered to {recipient_email}!")

if __name__ == "__main__":
    send()

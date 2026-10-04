"""
Direct WhatsApp Dispatch Script for Banki Kuu SACCO AGM Pass
Sends a real WhatsApp message payload or generates wa.me deep links.
"""

import urllib.parse
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def generate_wa_me_link(phone_number: str, delegate_name: str, ticket_id: str, member_id: str, dept: str) -> str:
    clean_phone = phone_number.replace(" ", "").replace("+", "").replace("-", "")
    if clean_phone.startswith("0"):
        clean_phone = "254" + clean_phone[1:]
    elif not clean_phone.startswith("254"):
        clean_phone = "254" + clean_phone

    pass_url = f"https://cbk-stride.streamlit.app/BKS?confirm={ticket_id}&name={urllib.parse.quote(delegate_name)}"
    
    text_body = (
        f"🏦 *Banki Kuu Staff SACCO — 58th AGM Accreditation Pass*\n\n"
        f"Dear *{delegate_name}*,\n"
        f"Your official AGM pass and voter credentials are confirmed.\n\n"
        f"• *Member ID:* {member_id}\n"
        f"• *Ticket ID:* {ticket_id}\n"
        f"• *Department:* {dept}\n"
        f"• *Voting Power:* 10,000 Certified Votes\n\n"
        f"🎟️ *Open Digital Pass & QR:* {pass_url}\n\n"
        f"Present your QR pass at KICC entrance for fast 2-second gate scanning."
    )
    
    wa_url = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(text_body)}"
    return wa_url

if __name__ == "__main__":
    phone = sys.argv[1] if len(sys.argv) > 1 else "254722849000"
    link = generate_wa_me_link(
        phone_number=phone,
        delegate_name="Stanley Gicho",
        ticket_id="TKT-BK-342805",
        member_id="SACCO-342805",
        dept="Human Resources"
    )
    print("==================================================")
    print("📱 INSTANT WHATSAPP DIRECT DEEP LINK GENERATED")
    print("==================================================")
    print(f"Target Phone: {phone}")
    print(f"Direct WhatsApp URL:\n{link}")
    print("==================================================")

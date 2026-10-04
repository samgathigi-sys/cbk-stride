"""
Golf Tournament WhatsApp Pass Generator
Formats 18-Hole Inter-Bank Championship QR Pass payload for WhatsApp dispatch.
"""

import urllib.parse
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def generate_golf_wa_link(phone_number: str, player_name: str, handicap: str, tee_time: str, venue: str) -> str:
    clean_phone = phone_number.replace(" ", "").replace("+", "").replace("-", "")
    if clean_phone.startswith("0"):
        clean_phone = "254" + clean_phone[1:]
    elif not clean_phone.startswith("254"):
        clean_phone = "254" + clean_phone

    pass_url = f"https://cbk-stride.streamlit.app/BKS?confirm=TKT-GLF-342801&name={urllib.parse.quote(player_name)}"
    
    text_body = (
        f"⛳ *2026 CBK INTER-BANK GOLF CHAMPIONSHIP — PLAYER ACCREDITATION*\n\n"
        f"Dear *{player_name}*,\n"
        f"Your official 18-Hole Tournament Pass & Pro-Shop Fast-Track QR has been issued.\n\n"
        f"🏆 *Tournament:* Inter-Bank Championship Qualifier\n"
        f"📍 *Venue:* {venue}\n"
        f"⏱️ *Tee Time:* {tee_time}\n"
        f"📊 *Player Handicap:* {handicap}\n"
        f"🎟️ *Pass Serial ID:* TKT-GLF-342801\n\n"
        f"📲 *Open Player Digital Pass & QR:* {pass_url}\n\n"
        f"Present your QR code at the Pro-Shop Marshal desk for instant scorecard & caddie dispatch."
    )
    
    wa_url = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(text_body)}"
    return wa_url

if __name__ == "__main__":
    phone = sys.argv[1] if len(sys.argv) > 1 else "254763321365"
    link = generate_golf_wa_link(
        phone_number=phone,
        player_name="Samuel Gathigi Njuguna",
        handicap="Handicap 12 (Executive Division)",
        tee_time="07:30 AM EAT (Hole 1 Tee Box)",
        venue="Muthaiga Golf Club / CBK Sports Complex"
    )
    print("==================================================")
    print("⛳ GOLF CHAMPIONSHIP WHATSAPP LINK GENERATED")
    print("==================================================")
    print(f"Target Phone: {phone}")
    print(f"Direct WhatsApp Link:\n{link}")
    print("==================================================")

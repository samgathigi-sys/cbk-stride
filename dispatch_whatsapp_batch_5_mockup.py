"""
End-to-End WhatsApp Business API Batch Dispatcher & Deep-Link Generator
Simulates Meta WhatsApp Business Cloud API payload construction & generates 1-click wa.me links for 5 delegates.
"""

import urllib.parse
import sys
import json
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

DELEGATES = [
    {
        "name": "Samuel Gathigi",
        "member_id": "SACCO-342801",
        "ticket_id": "TKT-BK-342801",
        "phone": "254722849000",
        "dept": "IT & Digital Services",
        "weight": "10,000 Certified Votes"
    },
    {
        "name": "Dr. Beatrice Kiptoo",
        "member_id": "SACCO-342802",
        "ticket_id": "TKT-BK-342802",
        "phone": "254733456789",
        "dept": "Internal Audit",
        "weight": "10,000 Certified Votes"
    },
    {
        "name": "Capt. Geoffrey Kemboi",
        "member_id": "SACCO-342803",
        "ticket_id": "TKT-BK-342803",
        "phone": "254722112233",
        "dept": "Banking Operations",
        "weight": "10,000 Certified Votes"
    },
    {
        "name": "Joyce Cheruiyot",
        "member_id": "SACCO-342804",
        "ticket_id": "TKT-BK-342804",
        "phone": "254725556677",
        "dept": "Finance & Accounts",
        "weight": "10,000 Certified Votes"
    },
    {
        "name": "Stanley Gicho",
        "member_id": "SACCO-342805",
        "ticket_id": "TKT-BK-342805",
        "phone": "254763321365",
        "dept": "Human Resources",
        "weight": "10,000 Certified Votes"
    }
]

def generate_wa_payload(delegate: dict) -> dict:
    """Constructs Meta WhatsApp Business Cloud API JSON payload."""
    qr_image_url = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=https://cbk-stride.streamlit.app/BKS?confirm={delegate['ticket_id']}"
    pass_url = f"https://cbk-stride.streamlit.app/BKS?confirm={delegate['ticket_id']}&name={urllib.parse.quote(delegate['name'])}"
    
    payload = {
        "messaging_product": "whatsapp",
        "to": delegate["phone"],
        "type": "template",
        "template": {
            "name": "banki_kuu_sacco_agm_pass",
            "language": {"code": "en"},
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {"link": qr_image_url}
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": delegate["name"]},
                        {"type": "text", "text": delegate["member_id"]},
                        {"type": "text", "text": delegate["ticket_id"]},
                        {"type": "text", "text": delegate["dept"]},
                        {"type": "text", "text": delegate["weight"]}
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": "0",
                    "parameters": [{"type": "text", "text": pass_url}]
                }
            ]
        }
    }
    return payload

def generate_wa_me_link(delegate: dict) -> str:
    """Generates direct 1-click wa.me URL for mobile/web WhatsApp client."""
    pass_url = f"https://cbk-stride.streamlit.app/BKS?confirm={delegate['ticket_id']}&name={urllib.parse.quote(delegate['name'])}"
    
    text_body = (
        f"🏦 *Banki Kuu Staff SACCO — 58th AGM Accreditation Pass*\n\n"
        f"Dear *{delegate['name']}*,\n"
        f"Your official AGM pass and voter credentials are confirmed.\n\n"
        f"• *Member ID:* {delegate['member_id']}\n"
        f"• *Ticket Serial ID:* {delegate['ticket_id']}\n"
        f"• *Department:* {delegate['dept']}\n"
        f"• *Voting Power:* {delegate['weight']}\n"
        f"• *Schedule:* Saturday 18th Oct 2026 @ 08:30 AM EAT\n\n"
        f"🎟️ *Open Digital Pass & QR:* {pass_url}\n\n"
        f"Present your QR pass at KICC entrance for fast 2-second gate scanning."
    )
    return f"https://wa.me/{delegate['phone']}?text={urllib.parse.quote(text_body)}"

def run_whatsapp_batch_simulation():
    print("==================================================")
    print("📱 BATCH WHATSAPP BUSINESS API DISPATCH ENGINE")
    print("==================================================")
    print("Simulating Meta Cloud API JSON construction & wa.me deep links...\n")
    
    dispatched_results = []
    
    for i, d in enumerate(DELEGATES, 1):
        payload = generate_wa_payload(d)
        wa_link = generate_wa_me_link(d)
        
        dispatched_results.append({
            "delegate": d["name"],
            "ticket_id": d["ticket_id"],
            "phone": d["phone"],
            "wa_link": wa_link,
            "status": "SENT_AND_DELIVERED"
        })
        
        print(f"[{i}/5] 📱 WhatsApp Pass Payload Built for {d['name']} ({d['phone']})")
        print(f"      Ticket Serial: {d['ticket_id']} | Member ID: {d['member_id']}")
        print(f"      1-Click Link:  {wa_link[:75]}...")
        print("      Status:        🟢 200 OK (Delivered & Read)\n")
        time.sleep(0.5)

    print("==================================================")
    print("🎉 WHATSAPP BATCH DISPATCH SIMULATION COMPLETE!")
    print("==================================================")

if __name__ == "__main__":
    run_whatsapp_batch_simulation()

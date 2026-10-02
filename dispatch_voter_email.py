"""
STRIDE Universal Event & Access Intelligence Platform
End-to-End Electronic Voting & QR Voter Pass Dispatcher
Dispatches an accredited VIP Voter Pass to Google Inbox via Outlook MAPI.
"""

import os
import sys
import time
import hashlib
import sqlite3
import qrcode
from io import BytesIO
from PIL import Image

# Ensure local imports
sys.path.insert(0, os.path.abspath("."))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import utils

def setup_and_send_voter_pass(recipient_email="sam.gathigi@gmail.com"):
    print(f"[*] Initializing End-to-End Voting Pass for: {recipient_email}")
    backend = utils.AttendanceBackend()

    # 1. Target Event: 58th AGM & Shareholder Elections
    target_event_id = "EVT-20261002-855"
    events = backend.get_events()
    target_evt = next((e for e in events if e["event_id"] == target_event_id), None)
    if not target_evt:
        target_evt = next((e for e in events if "AGM" in e.get("category", "") or "AGM" in e.get("title", "")), events[0])
        target_event_id = target_evt["event_id"]

    print(f"[+] Target Assembly: {target_evt['title']} ({target_event_id})")

    # 2. Check or Create Accredited Ticket
    voter_name = "Samuel Gathigi Njuguna"
    voter_org = "Central Bank of Kenya (Equity Block Holder)"
    ticket_tier = "Principal Shareholder / 10,000 Votes"
    phone_num = "+254 722 849 000"

    # Search existing ticket for this email/event
    existing_tkts = backend.get_event_tickets(target_event_id)
    my_tkt = next((t for t in existing_tkts if t.get("email") == recipient_email), None)

    if not my_tkt:
        sim_tx = f"AGM{int(time.time())}"[-10:]
        ok, msg, my_tkt = backend.register_event_ticket(
            event_id=target_event_id,
            attendee_name=voter_name,
            email=recipient_email,
            phone=phone_num,
            organization=voter_org,
            ticket_tier=ticket_tier,
            amount_paid=5000.0,
            mpesa_trans_id=sim_tx
        )
        if not ok:
            print(f"[-] Registration failed: {msg}")
            return False
        print(f"[+] Registered new ticket: {my_tkt['ticket_id']} (Ref: {sim_tx})")
    else:
        print(f"[+] Found existing ticket: {my_tkt['ticket_id']}")

    ticket_id = my_tkt["ticket_id"]

    # 3. Ensure Ticket is ADMITTED (Statutory Quorum check requirement)
    if my_tkt.get("gate_status") != "ADMITTED":
        ok_adm, msg_adm, adm_rec = backend.verify_and_admit_ticket(ticket_id)
        print(f"[+] Gate Accreditation: {msg_adm}")
    else:
        print(f"[+] Gate Accreditation: Already ADMITTED (Quorum satisfied)")

    # 4. Generate QR Code Image locally
    verify_url = f"https://cbk-stride.streamlit.app/EVENTS?verify_tkt={ticket_id}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(verify_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#071933", back_color="#FFFFFF")
    
    qr_filename = os.path.abspath(f"voter_qr_{ticket_id}.png")
    qr_img.save(qr_filename)
    print(f"[+] Generated QR Code Image: {qr_filename}")

    # 5. Dispatch via Outlook MAPI
    try:
        import win32com.client
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0) # 0 = olMailItem

        mail.To = recipient_email
        mail.Subject = f"🗳️ STRIDE Digital Accreditation & Voting Pass: {target_evt['title']} (Ref: {ticket_id})"

        # HTML Body with embedded CID attachment
        attachment = mail.Attachments.Add(qr_filename)
        # Set Content-ID for inline display
        attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "voter_qr")

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background-color: #030A16; margin: 0; padding: 25px; color: #FFFFFF; }}
            .card {{ max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #071F3D 0%, #030F21 100%); border: 2.5px solid #F5C542; border-radius: 16px; overflow: hidden; box-shadow: 0 16px 40px rgba(0,0,0,0.8); }}
            .header {{ background: #020A14; padding: 20px 25px; border-bottom: 2px solid #F5C542; text-align: center; }}
            .header h1 {{ margin: 0; color: #F5C542; font-size: 19px; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 800; }}
            .header p {{ margin: 5px 0 0; color: #94A3B8; font-size: 12px; }}
            .content {{ padding: 25px; text-align: center; color: #E2E8F0; }}
            .badge {{ display: inline-block; background: rgba(0, 242, 254, 0.15); color: #00F2FE; border: 1px solid rgba(0, 242, 254, 0.4); padding: 5px 14px; border-radius: 20px; font-size: 12px; font-weight: bold; margin-bottom: 15px; }}
            .qr-box {{ background: #FFFFFF; padding: 14px; border-radius: 12px; display: inline-block; margin: 15px auto; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }}
            .qr-box img {{ display: block; width: 180px; height: 180px; }}
            .details-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; text-align: left; }}
            .details-table td {{ padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.08); font-size: 13px; }}
            .details-table td.lbl {{ color: #94A3B8; font-weight: 600; width: 42%; }}
            .details-table td.val {{ color: #FFFFFF; font-weight: 700; }}
            .voting-power {{ background: rgba(245, 197, 66, 0.12); border: 1.5px solid #F5C542; border-radius: 8px; padding: 14px; margin: 20px 0; text-align: center; }}
            .voting-power .num {{ font-size: 22px; font-weight: 900; color: #F5C542; }}
            .voting-power .desc {{ font-size: 11px; color: #E2E8F0; text-transform: uppercase; margin-top: 4px; }}
            .btn-vote {{ display: inline-block; background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%); color: #020712 !important; font-weight: 900; text-decoration: none; padding: 14px 28px; border-radius: 8px; font-size: 14px; letter-spacing: 0.5px; box-shadow: 0 6px 20px rgba(0, 242, 254, 0.4); margin-top: 15px; }}
            .footer {{ background: #020710; padding: 16px; text-align: center; font-size: 11px; color: #64748B; border-top: 1px solid rgba(255,255,255,0.08); }}
          </style>
        </head>
        <body>
          <div class="card">
            <div class="header">
              <h1>STRIDE™ Enterprise Digital Pass</h1>
              <p>Official Statutory Accreditation & Electronic Voter Credential</p>
            </div>
            <div class="content">
              <div>
                <span class="badge">ACCREDITED VOTING DELEGATE</span>
              </div>
              <h2 style="margin: 0; color: #FFFFFF; font-size: 18px;">{target_evt['title']}</h2>
              <p style="margin: 4px 0 15px; font-size: 13px; color: #94A3B8;">Event ID: <code>{target_event_id}</code></p>

              <div class="qr-box">
                <img src="cid:voter_qr" alt="Voter Pass QR" />
              </div>
              <div style="font-size: 11px; color: #94A3B8;">Scan QR with phone camera at the venue voting kiosk</div>

              <div class="voting-power">
                <div class="num">⚖️ 10,000 Weighted Votes</div>
                <div class="desc">Tier: Principal Shareholder • SASRA Quorum Certified</div>
              </div>

              <table class="details-table">
                <tr>
                  <td class="lbl">Delegate Name</td>
                  <td class="val">{voter_name}</td>
                </tr>
                <tr>
                  <td class="lbl">Organization / Cohort</td>
                  <td class="val">{voter_org}</td>
                </tr>
                <tr>
                  <td class="lbl">Ticket Serial Pass</td>
                  <td class="val"><code>{ticket_id}</code></td>
                </tr>
                <tr>
                  <td class="lbl">Quorum Gate Status</td>
                  <td class="val" style="color: #10B981;">✓ ADMITTED ON ASSEMBLY FLOOR</td>
                </tr>
                <tr>
                  <td class="lbl">Registered Email</td>
                  <td class="val"><code>{recipient_email}</code></td>
                </tr>
              </table>

              <div style="margin-top: 25px;">
                <a href="https://cbk-stride.streamlit.app/EVENTS?vote_tkt={ticket_id}" class="btn-vote" target="_blank">
                  🗳️ OPEN STRIDE DIGITAL VOTING BOOTH
                </a>
              </div>
              <div style="font-size: 11px; color: #64748B; margin-top: 10px;">
                Direct voting route: Navigate to <strong>Tab 4: Digital Voting & Elections Booth</strong>
              </div>
            </div>
            <div class="footer">
              <p>&copy; 2026 STRIDE™ Universal Event & Access Intelligence Engine | Central Bank of Kenya</p>
              <p>Haile Selassie Avenue, Nairobi • Cryptographic SHA-256 Secret Ballot Standard</p>
            </div>
          </div>
        </body>
        </html>
        """

        mail.HTMLBody = html_body
        mail.Send()
        print(f"[+] SUCCESS! Email successfully dispatched to {recipient_email} via Outlook.")
        return True, ticket_id, target_event_id
    except Exception as e:
        print(f"[-] Outlook Dispatch Error: {e}")
        return False, None, None

if __name__ == "__main__":
    email_to = sys.argv[1] if len(sys.argv) > 1 else "sam.gathigi@gmail.com"
    setup_and_send_voter_pass(email_to)

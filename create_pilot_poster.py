"""
Generates an executive, printable A4-format Pilot Onboarding & Station Poster for CBK DSWAAP.
Used at the field venue (Athletics Track 100m Start Point) to enable frictionless pilot adoption.
"""

import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(OUTPUT_DIR, "cbk_logo.png")

# Fonts
try:
    font_title_lg = ImageFont.truetype("segoeuib.ttf", 42)
    font_title_md = ImageFont.truetype("segoeuib.ttf", 30)
    font_bold_lg = ImageFont.truetype("segoeuib.ttf", 24)
    font_bold_md = ImageFont.truetype("segoeuib.ttf", 19)
    font_bold_sm = ImageFont.truetype("segoeuib.ttf", 15)
    font_bold_xs = ImageFont.truetype("segoeuib.ttf", 13)
    font_reg_lg = ImageFont.truetype("segoeui.ttf", 20)
    font_reg_md = ImageFont.truetype("segoeui.ttf", 16)
    font_reg_sm = ImageFont.truetype("segoeui.ttf", 14)
except Exception:
    font_title_lg = ImageFont.load_default()
    font_title_md = font_title_lg
    font_bold_lg = font_title_lg
    font_bold_md = font_title_lg
    font_bold_sm = font_title_lg
    font_reg_lg = font_title_lg
    font_reg_md = font_title_lg
    font_reg_sm = font_title_lg

# CBK Palette
CBK_ROYAL_BLUE = "#025BBF"
CBK_DEEP_NAVY = "#10529E"
CBK_GOLD = "#F8B82D"
CBK_GOLD_AMBER = "#F7941D"
CBK_ICE_BLUE = "#EEF6FC"
CBK_BORDER_BLUE = "#B9DCF7"
CBK_TEXT_DARK = "#0F172A"
CBK_TEXT_MUTED = "#64748B"
CBK_WHITE = "#FFFFFF"
CBK_BG = "#F8FAFC"


def generate_pilot_poster():
    # A4 proportion at 150 DPI: 1240 x 1754
    w, h = 1240, 1754
    img = Image.new("RGB", (w, h), CBK_BG)
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([20, 20, w-20, h-20], outline=CBK_ROYAL_BLUE, width=4)
    draw.rectangle([26, 26, w-26, h-26], outline=CBK_GOLD, width=3)

    # Top Header Band
    draw.rectangle([30, 30, w-30, 260], fill=CBK_DEEP_NAVY)
    draw.rectangle([30, 254, w-30, 260], fill=CBK_GOLD)

    # Logo
    if os.path.exists(LOGO_PATH):
        raw_logo = Image.open(LOGO_PATH)
        lw, lh = raw_logo.size
        target_h = 160
        target_w = int(lw * (target_h / lh))
        logo_resized = raw_logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
        # White badge
        draw.rounded_rectangle([60, 50, 60+target_w+24, 50+target_h+20], radius=12, fill=CBK_WHITE, outline=CBK_GOLD, width=2)
        img.paste(logo_resized, (72, 60))
        tx = 60 + target_w + 50
    else:
        tx = 70

    # Header Titles
    draw.rounded_rectangle([tx, 55, tx+340, 88], radius=6, fill=CBK_GOLD)
    draw.text((tx+12, 60), "CENTRAL BANK OF KENYA", fill=CBK_DEEP_NAVY, font=font_bold_md)
    draw.text((tx, 105), "DSWAAP PILOT FIELD STATION", fill=CBK_WHITE, font=font_title_lg)
    draw.text((tx, 160), "Sports Wellness & Attendance Automation • Athletics & Track Camp", fill=CBK_ICE_BLUE, font=font_reg_lg)
    draw.text((tx, 200), "📍 Venue: Track 100m Start Point | Camp Marshal: Capt. Geoffrey Kemboi", fill=CBK_GOLD, font=font_bold_sm)

    # Headline Box
    draw.rounded_rectangle([60, 280, w-60, 360], radius=14, fill=CBK_ICE_BLUE, outline=CBK_ROYAL_BLUE, width=2)
    draw.text((90, 295), "⚡ ZERO-FRICTION PARTICIPANT CHECK-IN (NO APP INSTALL REQUIRED)", fill=CBK_ROYAL_BLUE, font=font_bold_lg)
    draw.text((90, 328), "Open your phone camera, scan the QR below, and enter your Staff ID to qualify for allowance.", fill=CBK_TEXT_DARK, font=font_reg_md)

    # Captain Hotspot Banner
    draw.rounded_rectangle([60, 375, w-60, 420], radius=10, fill="#FFFBEB", outline=CBK_GOLD_AMBER, width=2)
    draw.text((90, 388), "📶 ZERO DATA BUNDLES? Connect to Captain's Hotspot: 'CBK-DSWAAP-HOTSPOT' (Pass: CBKSports2026) - No airtime needed!", fill="#92400E", font=font_bold_sm)

    # Central Portal QR Card
    qr_w, qr_h = 540, 540
    qr_x = (w - qr_w) // 2
    qr_y = 440
    draw.rounded_rectangle([qr_x, qr_y, qr_x+qr_w, qr_y+qr_h], radius=20, fill=CBK_WHITE, outline=CBK_GOLD, width=4)

    # Generate QR Code directing to the local pilot portal
    qr = qrcode.QRCode(box_size=11, border=2)
    qr.add_data("http://192.168.1.35:8501")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=CBK_ROYAL_BLUE, back_color=CBK_WHITE).convert("RGB")
    qw, qh = qr_img.size
    img.paste(qr_img, (qr_x + (qr_w - qw)//2, qr_y + 35))

    # Badge under QR
    draw.rounded_rectangle([qr_x+40, qr_y+qr_h-70, qr_x+qr_w-40, qr_y+qr_h-20], radius=10, fill=CBK_DEEP_NAVY)
    draw.text((qr_x+65, qr_y+qr_h-58), "📲 SCAN TO LAUNCH DSWAAP MOBILE PORTAL", fill=CBK_GOLD, font=font_bold_md)

    # 3 Steps Section
    step_y = 1010
    draw.text((60, step_y), "HOW TO COMPLETE YOUR DUAL-GATE VERIFICATION IN 3 STEPS", fill=CBK_DEEP_NAVY, font=font_bold_lg)

    steps = [
        ("STEP 1: ARRIVAL SCAN (GATE 1)", "Point phone camera at this poster or Captain's terminal upon arrival.", "Auto-populates your name & @centralbank.go.ke email. Timestamp is locked."),
        ("STEP 2: COMPLETE TRAINING SESSION", "Participate in the scheduled Athletics camp along the track circuit.", "Policy Rule: Minimum 45 active minutes required to qualify for allowance."),
        ("STEP 3: DEPARTURE SCAN (GATE 2)", "Scan Captain Kemboi's Gate 2 QR code at Perimeter Gate 3 when finishing.", "Reconciles duration, approves KES 2,500 stipend & emails instant voucher.")
    ]

    card_y = step_y + 45
    card_w = (w - 120 - 40) // 3
    for idx, (s_title, s_b1, s_b2) in enumerate(steps):
        cx = 60 + idx * (card_w + 20)
        draw.rounded_rectangle([cx, card_y, cx+card_w, card_y+310], radius=14, fill=CBK_WHITE, outline=CBK_BORDER_BLUE, width=2)

        # Step header banner
        draw.rounded_rectangle([cx, card_y, cx+card_w, card_y+65], radius=14, fill=CBK_ROYAL_BLUE)
        draw.rectangle([cx, card_y+55, cx+card_w, card_y+65], fill=CBK_ROYAL_BLUE)
        draw.text((cx+15, card_y+20), s_title, fill=CBK_WHITE, font=font_bold_sm)

        # Body bullets
        draw.text((cx+15, card_y+85), f"• {s_b1}", fill=CBK_TEXT_DARK, font=font_reg_sm)
        draw.text((cx+15, card_y+175), f"• {s_b2}", fill=CBK_TEXT_MUTED, font=font_reg_sm)

        # Bottom badge
        badge_text = "Gate 1 Locked" if idx == 0 else ("⏱️ >= 45 Mins Floor" if idx == 1 else "KES 2,500 Approved")
        draw.rounded_rectangle([cx+15, card_y+250, cx+card_w-15, card_y+290], radius=8, fill=CBK_ICE_BLUE, outline=CBK_GOLD)
        draw.text((cx+25, card_y+262), badge_text, fill=CBK_DEEP_NAVY, font=font_bold_xs)

    # Footer Information Box
    foot_y = 1400
    draw.rounded_rectangle([60, foot_y, w-60, foot_y+270], radius=14, fill=CBK_DEEP_NAVY)
    draw.rectangle([60, foot_y, w-60, foot_y+8], fill=CBK_GOLD)

    draw.text((90, foot_y+30), "CENTRAL BANK OF KENYA SPORTS ALLOWANCE POLICY COMPLIANCE", fill=CBK_GOLD, font=font_bold_md)
    draw.text((90, foot_y+65), "• Circular Reference: CBK/HR/WEL/2026 - Sports & Physical Wellness Participation Stipend Policy.", fill=CBK_WHITE, font=font_reg_sm)
    draw.text((90, foot_y+95), "• Eligible Directorate Cohort: All verified permanent & contractual Bank staff with valid @centralbank.go.ke ID.", fill=CBK_WHITE, font=font_reg_sm)
    draw.text((90, foot_y+125), "• Fiduciary Audit Floor: Allowance is automatically credited to Finance Accounts Payable batch upon dual-verification.", fill=CBK_WHITE, font=font_reg_sm)

    draw.line([90, foot_y+165, w-90, foot_y+165], fill=CBK_ROYAL_BLUE, width=1)

    draw.text((90, foot_y+185), "PILOT HELPLINE & FIELD SUPPORT:", fill=CBK_GOLD, font=font_bold_sm)
    draw.text((90, foot_y+215), "Track Captain: Geoffrey Kemboi (Ext. 2405) | HR Wellness Secretariat (Ext. 2100) | IT Support (Ext. 2222)", fill=CBK_ICE_BLUE, font=font_reg_sm)

    out_path = os.path.join(OUTPUT_DIR, "pilot_onboarding_poster.png")
    img.save(out_path, quality=95)
    print(f"Pilot Onboarding Poster generated: {out_path}")


if __name__ == "__main__":
    generate_pilot_poster()

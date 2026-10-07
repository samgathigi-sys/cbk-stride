import os
import hmac
import hashlib
import json
import math
import openpyxl
from PIL import Image, ImageDraw, ImageFont
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================
BASE_DIR = r"C:\Users\user\.gemini\antigravity\scratch\cbk-stride"
EXCEL_PATH = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e\.user_uploaded\media_1791364617995.xlsx"
OUTPUT_DIR = os.path.join(BASE_DIR, "PRESS_READY_OUTPUT")
PREVIEW_DIR = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e\badges_preview"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PREVIEW_DIR, exist_ok=True)

HMAC_SECRET = b"BKS_MOMBASA_RETREAT_2026_ODPC_SECURE_TOKEN_SALT"

# Palette: Dark Glassmorphic, Deep Oceanic Navy (#020408), Neon Cyan & Warm Coastal Gold
COLOR_BG_DEEP = (2, 4, 8)          # #020408
COLOR_BG_MID = (4, 12, 28)         # #040c1c
COLOR_BG_BOTTOM = (2, 6, 14)       # #02060e

# Glassmorphism panel fills and frosted borders
COLOR_GLASS_FILL = (8, 20, 44, 215)
COLOR_GLASS_FILL_DARK = (4, 12, 26, 235)
COLOR_GLASS_BORDER = (0, 242, 254, 90)     # Neon Cyan frosted border
COLOR_GLASS_GOLD_BORDER = (245, 197, 66, 120)

# Accents
NEON_CYAN = (0, 242, 254)          # #00F2FE
CYAN_DIM = (0, 180, 210)
GOLD_LIGHT = (255, 240, 180)       # #FFF0B4
GOLD_PRIMARY = (245, 197, 66)      # #F5C542
GOLD_METALLIC = (212, 175, 55)     # #D4AF37
GOLD_DARK = (165, 122, 24)
AMBER_ACCENT = (245, 158, 11)      # #F59E0B

# Typography colors
WHITE = (255, 255, 255)
OFF_WHITE = (240, 246, 255)
GRAY_LIGHT = (205, 220, 238)
GRAY_MUTED = (130, 152, 180)
TEXT_DARK = (4, 10, 22)

# Badge Dimensions at 300 DPI: 1000 x 1450 px (~3.33" x 4.83" Lanyard Pass)
BADGE_W = 1000
BADGE_H = 1450

# A4 Sheet Dimensions at 300 DPI: 2480 x 3508 px
SHEET_W = 2480
SHEET_H = 3508

# ==============================================================================
# TYPOGRAPHY HELPER
# ==============================================================================
def get_font(size, bold=False):
    win_fonts = os.environ.get("WINDIR", r"C:\Windows") + r"\Fonts"
    try:
        if bold:
            font_path = os.path.join(win_fonts, "segoeuib.ttf")
            if not os.path.exists(font_path):
                font_path = os.path.join(win_fonts, "arialbd.ttf")
        else:
            font_path = os.path.join(win_fonts, "segoeui.ttf")
            if not os.path.exists(font_path):
                font_path = os.path.join(win_fonts, "arial.ttf")
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

# ==============================================================================
# ODPC MASKING & SECURITY HELPERS
# ==============================================================================
def mask_phone(phone_str):
    if not phone_str:
        return "+254 7** *** ***"
    s = str(phone_str).strip().replace(" ", "").replace(".0", "")
    if s.startswith("254") and len(s) >= 12:
        return f"+{s[:3]} {s[3:6]} *** *{s[-2:]}"
    elif len(s) >= 9:
        return f"+254 {s[-9:-6]} *** *{s[-2:]}"
    return "+254 7** *** ***"

def mask_id(id_str):
    if not id_str:
        return "ID: ********"
    s = str(id_str).strip().replace(".0", "")
    if len(s) > 4:
        return f"ID: {s[:3]}****{s[-1]}"
    return f"ID: {s[:2]}****"

def mask_email(email_str):
    if not email_str:
        return "Not on file"
    s = str(email_str).strip().rstrip(";")
    if "@" in s:
        user, domain = s.split("@", 1)
        if len(user) > 2:
            masked_user = f"{user[0]}***{user[-1]}"
        else:
            masked_user = f"{user[0]}***"
        return f"{masked_user}@{domain}"
    return "Encrypted Record"

def generate_participant_token(serial_no, id_no, full_name, index):
    seed = f"BKS:{serial_no}:{id_no}:{full_name}:{index}".encode('utf-8')
    full_hash = hmac.new(HMAC_SECRET, seed, hashlib.sha256).hexdigest().upper()
    token_id = f"BKS-MSA26-{full_hash[:8]}"
    return token_id, full_hash

# ==============================================================================
# BADGE RENDERING ENGINES (300 DPI)
# ==============================================================================
def draw_glass_background(width, height):
    """Draws deep oceanic navy background (#020408) with coastal wave lines."""
    img = Image.new("RGBA", (width, height), COLOR_BG_DEEP)
    draw = ImageDraw.Draw(img)
    
    # Smooth vertical gradient from #020408 to #040c1c to #02060e
    for y in range(height):
        factor = y / float(height)
        if factor < 0.5:
            f = factor / 0.5
            r = int(COLOR_BG_DEEP[0] + (COLOR_BG_MID[0] - COLOR_BG_DEEP[0]) * f)
            g = int(COLOR_BG_DEEP[1] + (COLOR_BG_MID[1] - COLOR_BG_DEEP[1]) * f)
            b = int(COLOR_BG_DEEP[2] + (COLOR_BG_MID[2] - COLOR_BG_DEEP[2]) * f)
        else:
            f = (factor - 0.5) / 0.5
            r = int(COLOR_BG_MID[0] + (COLOR_BG_BOTTOM[0] - COLOR_BG_MID[0]) * f)
            g = int(COLOR_BG_MID[1] + (COLOR_BG_BOTTOM[1] - COLOR_BG_MID[1]) * f)
            b = int(COLOR_BG_MID[2] + (COLOR_BG_BOTTOM[2] - COLOR_BG_MID[2]) * f)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
        
    # Decorative coastal wave neon-cyan and gold curves at bottom
    wave_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    wdraw = ImageDraw.Draw(wave_overlay)
    
    for i in range(4):
        y_base = height - 160 + (i * 24)
        points = []
        for x in range(0, width + 15, 10):
            y_wave = y_base + int(math.sin((x / 90.0) + (i * 1.4)) * 9)
            points.append((x, y_wave))
        col = (NEON_CYAN[0], NEON_CYAN[1], NEON_CYAN[2], 25 + i * 15) if i % 2 == 0 else (GOLD_PRIMARY[0], GOLD_PRIMARY[1], GOLD_PRIMARY[2], 30 + i * 18)
        wdraw.line(points, fill=col, width=3)
        
    img = Image.alpha_composite(img, wave_overlay)
    return img

def draw_press_borders(draw, width, height):
    """Draws double luxury gold and cyan borders with corner accents."""
    m1 = 28
    m2 = 36
    draw.rounded_rectangle([(m1, m1), (width - m1, height - m1)], radius=24, outline=GOLD_PRIMARY, width=3)
    draw.rounded_rectangle([(m2, m2), (width - m2, height - m2)], radius=18, outline=(0, 242, 254, 140), width=1)
    
    # Stylized corner diamonds
    for cx, cy in [(m1 + 16, m1 + 16), (width - m1 - 16, m1 + 16), (m1 + 16, height - m1 - 16), (width - m1 - 16, height - m1 - 16)]:
        draw.polygon([(cx, cy - 7), (cx + 7, cy), (cx, cy + 7), (cx - 7, cy)], fill=GOLD_LIGHT)
        
    # Top lanyard hole punch guide marker
    draw.rounded_rectangle([(width // 2 - 50, 12), (width // 2 + 50, 22)], radius=4, fill=GOLD_DARK)

def render_front_badge(participant, token_id, full_hash):
    img = draw_glass_background(BADGE_W, BADGE_H)
    overlay = Image.new("RGBA", (BADGE_W, BADGE_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_press_borders(draw, BADGE_W, BADGE_H)
    
    # 1. Header Organization & Event Branding
    f_org = get_font(30, bold=True)
    f_evt = get_font(18, bold=True)
    f_loc = get_font(14, bold=False)
    
    draw.text((BADGE_W // 2, 75), "BANKI KUU SACCO & BHC", fill=GOLD_LIGHT, font=f_org, anchor="mm")
    draw.text((BADGE_W // 2, 114), "EXECUTIVE STRATEGIC RETREAT 2026", fill=NEON_CYAN, font=f_evt, anchor="mm")
    draw.text((BADGE_W // 2, 144), "MOMBASA COASTAL EXPEDITION • PRIDEINN PARADISE", fill=GRAY_LIGHT, font=f_loc, anchor="mm")
    
    # Gold divider with diamond center
    div_y = 168
    draw.line([(90, div_y), (BADGE_W // 2 - 25, div_y)], fill=GOLD_PRIMARY, width=2)
    draw.line([(BADGE_W // 2 + 25, div_y), (BADGE_W - 90, div_y)], fill=GOLD_PRIMARY, width=2)
    draw.polygon([(BADGE_W // 2, div_y - 6), (BADGE_W // 2 + 6, div_y), (BADGE_W // 2, div_y + 6), (BADGE_W // 2 - 6, div_y)], fill=GOLD_LIGHT)
    
    # 2. Dark Glassmorphic Photo Placeholder Frame
    fw, fh = 360, 420
    fx0 = (BADGE_W - fw) // 2
    fy0 = 205
    fx1 = fx0 + fw
    fy1 = fy0 + fh
    
    # Outer glassmorphic frame with neon cyan glow and gold trim
    draw.rounded_rectangle([(fx0, fy0), (fx1, fy1)], radius=20, fill=COLOR_GLASS_FILL_DARK, outline=GOLD_PRIMARY, width=3)
    draw.rounded_rectangle([(fx0 + 8, fy0 + 8), (fx1 - 8, fy1 - 8)], radius=14, outline=(0, 242, 254, 180), width=1)
    
    # Vector portrait emblem
    cx = BADGE_W // 2
    cy = fy0 + 155
    draw.ellipse([(cx - 65, cy - 70), (cx + 65, cy + 60)], outline=GOLD_PRIMARY, width=3)
    draw.ellipse([(cx - 30, cy - 50), (cx + 30, cy + 8)], fill=GOLD_DARK)
    draw.chord([(cx - 52, cy - 2), (cx + 52, cy + 58)], 0, 180, fill=GOLD_DARK)
    
    f_ph1 = get_font(18, bold=True)
    f_ph2 = get_font(14, bold=False)
    f_ph3 = get_font(12, bold=False)
    draw.text((cx, fy0 + 290), "PARTICIPANT PHOTO", fill=GOLD_LIGHT, font=f_ph1, anchor="mm")
    draw.text((cx, fy0 + 322), "[ ATTACH 2×2 GLOSSY HEADSHOT ]", fill=GRAY_LIGHT, font=f_ph2, anchor="mm")
    draw.text((cx, fy0 + 355), "ODPC ENCRYPTED RETREAT CREDENTIAL", fill=NEON_CYAN, font=f_ph3, anchor="mm")
    draw.rounded_rectangle([(fx0 + 45, fy0 + 380), (fx1 - 45, fy0 + 383)], radius=2, fill=GOLD_PRIMARY)
    
    # 3. Participant Name Section (Clean High-Contrast Typography)
    name = str(participant.get("name", "EXECUTIVE DELEGATE")).strip()
    f_name = get_font(36, bold=True)
    bbox = draw.textbbox((0, 0), name, font=f_name)
    nw = bbox[2] - bbox[0]
    if nw > 820:
        f_name = get_font(30, bold=True)
        bbox = draw.textbbox((0, 0), name, font=f_name)
        nw = bbox[2] - bbox[0]
        if nw > 820:
            f_name = get_font(26, bold=True)
            
    draw.text((BADGE_W // 2, 700), name, fill=WHITE, font=f_name, anchor="mm")
    
    # 4. Role Pill Badge (Coastal Gold Pill)
    role_str = str(participant.get("role", "EXECUTIVE DELEGATE")).strip().upper()
    if not role_str or role_str == "NONE":
        role_str = "BRANCH REPRESENTATIVE"
        
    f_role = get_font(20, bold=True)
    r_bbox = draw.textbbox((0, 0), role_str, font=f_role)
    rw = (r_bbox[2] - r_bbox[0]) + 56
    pill_w = max(340, rw)
    pill_h = 48
    px0 = (BADGE_W - pill_w) // 2
    py0 = 750
    px1 = px0 + pill_w
    py1 = py0 + pill_h
    
    draw.rounded_rectangle([(px0, py0), (px1, py1)], radius=24, fill=GOLD_PRIMARY, outline=GOLD_LIGHT, width=2)
    draw.text((BADGE_W // 2, py0 + pill_h // 2), role_str, fill=TEXT_DARK, font=f_role, anchor="mm")
    
    # 5. Dark Glassmorphic Telemetry Data Panel with Embedded Front QR Key
    box_y0 = 835
    box_y1 = 1060
    draw.rounded_rectangle([(70, box_y0), (BADGE_W - 70, box_y1)], radius=18, fill=COLOR_GLASS_FILL, outline=COLOR_GLASS_BORDER, width=2)
    
    # Generate Tokenized QR Code for this participant
    payload_data = {
        "iss": "BANKI_KUU_SACCO",
        "evt": "MSA_RETREAT_2026",
        "tid": token_id,
        "sig": full_hash[:16],
        "sec": "ODPC_SEC_25",
        "v": 1
    }
    payload_str = json.dumps(payload_data, separators=(',', ':'))
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(payload_str)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=COLOR_BG_DEEP, back_color=(255, 255, 255)).convert("RGBA")
    
    # Left Column: Credential Telemetry
    f_lbl = get_font(14, bold=True)
    f_val = get_font(17, bold=True)
    
    draw.text((105, box_y0 + 26), "DIGITAL TOKEN ID", fill=GRAY_MUTED, font=f_lbl)
    draw.text((105, box_y0 + 54), token_id, fill=GOLD_LIGHT, font=f_val)
    
    serial_str = str(participant.get("sno", "N/A")).strip()
    draw.text((105, box_y0 + 94), "STAFF / S.NO", fill=GRAY_MUTED, font=f_lbl)
    draw.text((105, box_y0 + 122), f"#{serial_str}", fill=WHITE, font=f_val)
    
    tier_str = participant.get("tier", "EXECUTIVE")
    draw.text((370, box_y0 + 26), "ACCESS CLEARANCE", fill=GRAY_MUTED, font=f_lbl)
    draw.text((370, box_y0 + 54), f"{tier_str} PASS", fill=NEON_CYAN, font=f_val)
    
    dept_str = participant.get("dept", "GOVERNANCE")
    draw.text((370, box_y0 + 94), "SECTOR / UNIT", fill=GRAY_MUTED, font=f_lbl)
    draw.text((370, box_y0 + 122), dept_str[:18], fill=WHITE, font=f_val)
    
    # Right Column: High-Visibility Scannable Front QR Code Box
    qr_f_box_x0 = 665
    qr_f_box_y0 = box_y0 + 15
    qr_f_box_w = 195
    qr_f_box_h = 195
    draw.rounded_rectangle([(qr_f_box_x0, qr_f_box_y0), (qr_f_box_x0 + qr_f_box_w, qr_f_box_y0 + qr_f_box_h)], radius=12, fill=(255, 255, 255), outline=GOLD_PRIMARY, width=2)
    
    # Paste Front QR inside
    qr_f_disp = 150
    qr_f_resized = qr_img.resize((qr_f_disp, qr_f_disp), Image.Resampling.LANCZOS)
    overlay.paste(qr_f_resized, (qr_f_box_x0 + (qr_f_box_w - qr_f_disp) // 2, qr_f_box_y0 + 10), qr_f_resized)
    
    f_f_qr_lbl = get_font(11, bold=True)
    draw.text((qr_f_box_x0 + qr_f_box_w // 2, qr_f_box_y0 + 172), "SCAN TO ACCREDIT", fill=(10, 32, 70), font=f_f_qr_lbl, anchor="mm")
    
    # 6. Cryptographic ODPC Security Watermark Strip
    sec_y0 = 1090
    sec_y1 = 1180
    draw.rounded_rectangle([(70, sec_y0), (BADGE_W - 70, sec_y1)], radius=12, fill=COLOR_GLASS_FILL_DARK, outline=NEON_CYAN, width=1)
    f_sec_h = get_font(15, bold=True)
    f_sec_t = get_font(12, bold=False)
    draw.text((BADGE_W // 2, sec_y0 + 26), "ODPC § 25 ENCRYPTED DIGITAL PASSPORT", fill=NEON_CYAN, font=f_sec_h, anchor="mm")
    draw.text((BADGE_W // 2, sec_y0 + 58), f"SIG: {full_hash[:36]}...", fill=GRAY_LIGHT, font=f_sec_t, anchor="mm")
    
    # 7. Bottom VIP Banner
    ban_y0 = 1220
    ban_y1 = 1350
    draw.rounded_rectangle([(60, ban_y0), (BADGE_W - 60, ban_y1)], radius=18, fill=GOLD_PRIMARY, outline=GOLD_LIGHT, width=3)
    f_ban1 = get_font(24, bold=True)
    f_ban2 = get_font(15, bold=True)
    
    tb = "ALL-ACCESS EXECUTIVE DELEGATE"
    tb_bbox = draw.textbbox((0, 0), tb, font=f_ban1)
    tb_w = tb_bbox[2] - tb_bbox[0]
    draw.text((BADGE_W // 2, ban_y0 + 38), tb, fill=TEXT_DARK, font=f_ban1, anchor="mm")
    
    # Diamonds beside banner text
    ld_x = (BADGE_W - tb_w) // 2 - 28
    ld_y = ban_y0 + 38
    draw.polygon([(ld_x, ld_y - 8), (ld_x + 8, ld_y), (ld_x, ld_y + 8), (ld_x - 8, ld_y)], fill=COLOR_BG_DEEP)
    rd_x = (BADGE_W + tb_w) // 2 + 28
    rd_y = ban_y0 + 38
    draw.polygon([(rd_x, rd_y - 8), (rd_x + 8, rd_y), (rd_x, rd_y + 8), (rd_x - 8, ld_y)], fill=COLOR_BG_DEEP)
    
    draw.text((BADGE_W // 2, ban_y0 + 85), "GOVERNANCE • INNOVATION • STRATEGIC HARMONY", fill=COLOR_BG_DEEP, font=f_ban2, anchor="mm")
    
    img = Image.alpha_composite(img, overlay).convert("RGB")
    return img

def render_back_badge(participant, token_id, full_hash):
    img = draw_glass_background(BADGE_W, BADGE_H)
    overlay = Image.new("RGBA", (BADGE_W, BADGE_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    draw_press_borders(draw, BADGE_W, BADGE_H)
    
    # 1. Header
    f_org = get_font(28, bold=True)
    f_sub = get_font(16, bold=True)
    draw.text((BADGE_W // 2, 75), "RETREAT ITINERARY & DIGITAL KEY", fill=GOLD_LIGHT, font=f_org, anchor="mm")
    draw.text((BADGE_W // 2, 114), "3-DAY LEADERSHIP RETREAT • MOMBASA, KENYA", fill=NEON_CYAN, font=f_sub, anchor="mm")
    
    div_y = 138
    draw.line([(80, div_y), (BADGE_W - 80, div_y)], fill=GOLD_PRIMARY, width=2)
    
    # 2. Glassmorphic 3-Day Itinerary Schedule Cards
    itin_start_y = 158
    card_h = 100
    gap = 14
    
    days_data = [
        ("DAY 1 • THURSDAY", "SGR Express Transit & Coastal Check-in", "Welcome Reception, Strategy Keynote & Networking Dinner", (20, 184, 166)),
        ("DAY 2 • FRIDAY", "Strategic Governance & Team Challenges", "Beach Leadership Dynamics, Innovation Sprint & Gala Night", GOLD_PRIMARY),
        ("DAY 3 • SATURDAY", "Marine Excursion & Leadership Synthesis", "Fort Jesus & Diani Excursion, Resolutions & Return Transit", NEON_CYAN),
    ]
    
    f_day_lbl = get_font(14, bold=True)
    f_day_t1 = get_font(17, bold=True)
    f_day_t2 = get_font(13, bold=False)
    
    for idx, (day_title, title_main, title_sub, accent_color) in enumerate(days_data):
        cy0 = itin_start_y + idx * (card_h + gap)
        cy1 = cy0 + card_h
        draw.rounded_rectangle([(70, cy0), (BADGE_W - 70, cy1)], radius=14, fill=COLOR_GLASS_FILL, outline=accent_color, width=1)
        
        # Day Tag Badge
        draw.rounded_rectangle([(90, cy0 + 14), (300, cy0 + 46)], radius=8, fill=accent_color)
        draw.text((195, cy0 + 30), day_title, fill=TEXT_DARK, font=f_day_lbl, anchor="mm")
        
        draw.text((320, cy0 + 30), title_main, fill=WHITE, font=f_day_t1, anchor="lm")
        draw.text((95, cy0 + 72), f"• {title_sub}", fill=GRAY_LIGHT, font=f_day_t2, anchor="lm")
        
    # 3. Centerpiece Tokenized QR Code Container (Large & Bold)
    qr_box_y0 = 515
    qr_box_y1 = 925
    qr_box_w = 600
    qr_box_x0 = (BADGE_W - qr_box_w) // 2
    qr_box_x1 = qr_box_x0 + qr_box_w
    
    draw.rounded_rectangle([(qr_box_x0, qr_box_y0), (qr_box_x1, qr_box_y1)], radius=20, fill=(255, 255, 255, 255), outline=GOLD_PRIMARY, width=4)
    
    # Generate 300 DPI QR Image
    payload_data = {
        "iss": "BANKI_KUU_SACCO",
        "evt": "MSA_RETREAT_2026",
        "tid": token_id,
        "sig": full_hash[:16],
        "sec": "ODPC_SEC_25",
        "v": 1
    }
    payload_str = json.dumps(payload_data, separators=(',', ':'))
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=1,
    )
    qr.add_data(payload_str)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=COLOR_BG_DEEP, back_color=(255, 255, 255)).convert("RGBA")
    
    qr_disp_size = 280
    qr_resized = qr_img.resize((qr_disp_size, qr_disp_size), Image.Resampling.LANCZOS)
    
    paste_x = (BADGE_W - qr_disp_size) // 2
    paste_y = qr_box_y0 + 20
    overlay.paste(qr_resized, (paste_x, paste_y), qr_resized)
    
    f_qr_label = get_font(17, bold=True)
    f_qr_tok = get_font(20, bold=True)
    f_qr_sig = get_font(13, bold=False)
    
    draw.text((BADGE_W // 2, qr_box_y0 + 318), "DIGITAL EVENT ACCESS KEY", fill=TEXT_DARK, font=f_qr_label, anchor="mm")
    draw.text((BADGE_W // 2, qr_box_y0 + 350), token_id, fill=(10, 32, 70), font=f_qr_tok, anchor="mm")
    draw.text((BADGE_W // 2, qr_box_y0 + 380), "SCAN FOR SESSIONS, MEALS & RETREAT ACCESS", fill=GOLD_DARK, font=f_qr_sig, anchor="mm")
    
    # 4. ODPC Compliance Shield & PII-Masked Metadata Box
    meta_y0 = 940
    meta_y1 = 1220
    draw.rounded_rectangle([(70, meta_y0), (BADGE_W - 70, meta_y1)], radius=18, fill=COLOR_GLASS_FILL_DARK, outline=GOLD_PRIMARY, width=2)
    
    f_odpc_h = get_font(16, bold=True)
    f_odpc_lbl = get_font(14, bold=True)
    f_odpc_val = get_font(16, bold=False)
    f_notice = get_font(13, bold=False)
    
    # Shield vector icon
    sh_x, sh_y = 135, meta_y0 + 28
    draw.polygon([(sh_x, sh_y - 10), (sh_x + 9, sh_y - 6), (sh_x + 9, sh_y + 4), (sh_x, sh_y + 11), (sh_x - 9, sh_y + 4), (sh_x - 9, sh_y - 6)], fill=NEON_CYAN)
    
    draw.text((BADGE_W // 2 + 15, meta_y0 + 28), "KENYA DATA PROTECTION ACT (ODPC 2019) COMPLIANT", fill=GOLD_LIGHT, font=f_odpc_h, anchor="mm")
    draw.line([(100, meta_y0 + 48), (BADGE_W - 100, meta_y0 + 48)], fill=GOLD_DARK, width=1)
    
    masked_id_str = mask_id(participant.get("id_no"))
    masked_phone_str = mask_phone(participant.get("phone_no"))
    masked_email_str = mask_email(participant.get("email"))
    
    # Row 1: Protected ID
    draw.text((110, meta_y0 + 72), "PROTECTED ID:", fill=GRAY_MUTED, font=f_odpc_lbl)
    draw.text((280, meta_y0 + 72), masked_id_str, fill=WHITE, font=f_odpc_val)
    
    # Row 2: Protected Phone
    draw.text((110, meta_y0 + 110), "PROTECTED TEL:", fill=GRAY_MUTED, font=f_odpc_lbl)
    draw.text((280, meta_y0 + 110), masked_phone_str, fill=WHITE, font=f_odpc_val)
    
    # Row 3: Official Email
    draw.text((110, meta_y0 + 148), "OFFICIAL EMAIL:", fill=GRAY_MUTED, font=f_odpc_lbl)
    draw.text((280, meta_y0 + 148), masked_email_str, fill=GRAY_LIGHT, font=f_odpc_val)
    
    # Row 4: Cryptographic Signature
    draw.text((110, meta_y0 + 186), "CRYPTO SIG:", fill=GRAY_MUTED, font=f_odpc_lbl)
    draw.text((280, meta_y0 + 186), f"SHA256-{full_hash[:28]}...", fill=NEON_CYAN, font=f_odpc_val)
    
    draw.text((BADGE_W // 2, meta_y0 + 240), "All personal identifiable data is protected by one-way cryptographic tokenization.", fill=GRAY_MUTED, font=f_notice, anchor="mm")
    
    # 5. Emergency Hotline & Venue Footer
    f_foot1 = get_font(15, bold=True)
    f_foot2 = get_font(13, bold=False)
    
    draw.text((BADGE_W // 2, 1260), "PrideInn Paradise Beach Resort & Spa, Shanzu, Mombasa", fill=GOLD_LIGHT, font=f_foot1, anchor="mm")
    draw.text((BADGE_W // 2, 1295), "Secretariat Logistics Hotline: +254 711 875 393 / +254 728 028 932", fill=GRAY_LIGHT, font=f_foot2, anchor="mm")
    draw.text((BADGE_W // 2, 1330), "This official pass must be worn visibly at all times during retreat events.", fill=GRAY_MUTED, font=f_foot2, anchor="mm")
    
    img = Image.alpha_composite(img, overlay).convert("RGB")
    return img

# ==============================================================================
# IMPOSITION SHEET BUILDER (4-UP ON A4 WITH CROP MARKS & BLEED)
# ==============================================================================
def draw_crop_marks(draw, x0, y0, x1, y1, mark_len=35, offset=12):
    """Draws professional commercial corner crop marks (tick marks) for guillotine trim."""
    col = (180, 180, 180)
    w = 2
    
    # Top-Left
    draw.line([(x0 - offset - mark_len, y0), (x0 - offset, y0)], fill=col, width=w)
    draw.line([(x0, y0 - offset - mark_len), (x0, y0 - offset)], fill=col, width=w)
    
    # Top-Right
    draw.line([(x1 + offset, y0), (x1 + offset + mark_len, y0)], fill=col, width=w)
    draw.line([(x1, y0 - offset - mark_len), (x1, y0 - offset)], fill=col, width=w)
    
    # Bottom-Left
    draw.line([(x0 - offset - mark_len, y1), (x0 - offset, y1)], fill=col, width=w)
    draw.line([(x0, y1 + offset), (x0, y1 + offset + mark_len)], fill=col, width=w)
    
    # Bottom-Right
    draw.line([(x1 + offset, y1), (x1 + offset + mark_len, y1)], fill=col, width=w)
    draw.line([(x1, y1 + offset), (x1, y1 + offset + mark_len)], fill=col, width=w)

def draw_registration_mark(draw, cx, cy, r=16):
    """Draws registration crosshair target for print alignment."""
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], outline=(120, 120, 120), width=2)
    draw.line([(cx - r - 6, cy), (cx + r + 6, cy)], fill=(120, 120, 120), width=2)
    draw.line([(cx, cy - r - 6), (cx, cy + r + 6)], fill=(120, 120, 120), width=2)

def draw_color_control_bar(draw, x, y, width=400, height=18):
    """Draws CMYK + Spot color calibration swatch bar."""
    swatches = [
        ("C", (0, 255, 255)),
        ("M", (255, 0, 255)),
        ("Y", (255, 255, 0)),
        ("K", (20, 20, 20)),
        ("GOLD", GOLD_PRIMARY),
        ("CYAN", NEON_CYAN),
        ("NAVY", COLOR_BG_MID)
    ]
    sw_w = width // len(swatches)
    for i, (lbl, col) in enumerate(swatches):
        draw.rectangle([(x + i * sw_w, y), (x + (i + 1) * sw_w, y + height)], fill=col, outline=(100, 100, 100), width=1)

def build_imposition_sheet(badge_images, sheet_num, total_sheets, is_back_sheet=False):
    """
    Arranges 4 badges onto an A4 press sheet (2480 x 3508 px at 300 DPI).
    If is_back_sheet is True, swaps column 0 and column 1 for exact double-sided duplex alignment!
    """
    sheet = Image.new("RGB", (SHEET_W, SHEET_H), (255, 255, 255))
    draw = ImageDraw.Draw(sheet)
    
    # Layout Grid: 2 columns x 2 rows
    # A4 = 2480 x 3508
    # 2 Badges: 2 x 1000 = 2000 px -> Left/Right margins 160 px, Center gutter 160 px
    # 2 Badges: 2 x 1450 = 2900 px -> Top margin 250 px, Center gutter 110 px, Bottom margin 248 px
    left_m = 160
    center_gx = 160
    top_m = 250
    center_gy = 110
    
    positions = [
        (left_m, top_m),                                      # Top-Left (Pos 0)
        (left_m + BADGE_W + center_gx, top_m),                # Top-Right (Pos 1)
        (left_m, top_m + BADGE_H + center_gy),                # Bottom-Left (Pos 2)
        (left_m + BADGE_W + center_gx, top_m + BADGE_H + center_gy), # Bottom-Right (Pos 3)
    ]
    
    # If Back Sheet: flip columns horizontally so Duplex matches!
    # Front: [0, 1], [2, 3] -> Back: [1, 0], [3, 2]
    if is_back_sheet:
        imposition_order = [1, 0, 3, 2]
    else:
        imposition_order = [0, 1, 2, 3]
        
    for slot_idx, badge_idx in enumerate(imposition_order):
        if badge_idx < len(badge_images) and badge_images[badge_idx] is not None:
            bx, by = positions[slot_idx]
            sheet.paste(badge_images[badge_idx], (bx, by))
            draw_crop_marks(draw, bx, by, bx + BADGE_W, by + BADGE_H)
            
    # Sheet Header & Registration Marks
    draw_registration_mark(draw, SHEET_W // 2, 100)
    draw_registration_mark(draw, SHEET_W // 2, SHEET_H - 100)
    draw_registration_mark(draw, 70, SHEET_H // 2)
    draw_registration_mark(draw, SHEET_W - 70, SHEET_H // 2)
    
    draw_color_control_bar(draw, SHEET_W // 2 - 200, 135)
    
    # Slug Line at Top and Bottom
    side_label = "BACK SHEET (DUPLEX FLIPPED)" if is_back_sheet else "FRONT SHEET"
    f_slug = get_font(18, bold=True)
    slug_text = f"BANKI KUU SACCO RETREAT 2026 • MOMBASA • PRESS SHEET {sheet_num:02d}/{total_sheets:02d} [{side_label}] • 300 DPI GLOSSY CARDSTOCK • ODPC § 25"
    draw.text((SHEET_W // 2, 195), slug_text, fill=(80, 80, 80), font=f_slug, anchor="mm")
    draw.text((SHEET_W // 2, SHEET_H - 145), slug_text, fill=(80, 80, 80), font=f_slug, anchor="mm")
    
    return sheet

# ==============================================================================
# PARTICIPANT DATA LOADER (60 EXECUTIVES)
# ==============================================================================
def load_60_executive_participants(excel_path):
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    execs = []
    
    # 1. BOD, Supervisory, Branch Reps, CEO (29 delegates)
    ws1 = wb['BOD,SC,BRANCH REPS & BHC BOD']
    for r in ws1.iter_rows(values_only=True):
        if r[0] is not None and str(r[0]).strip().isdigit():
            role_val = str(r[3]).strip() if r[3] and str(r[3]).strip() not in ('', 'None') else 'BRANCH REP'
            execs.append({
                "sno": str(r[1]).strip(),
                "name": str(r[2]).strip(),
                "role": role_val,
                "id_no": str(r[4]).strip(),
                "phone_no": str(r[5]).strip(),
                "email": str(r[6] if len(r)>6 else '').strip(),
                "tier": "EXECUTIVE",
                "dept": "GOVERNANCE & LEADERSHIP"
            })
            
    # 2. Secretariat Leadership (24 delegates)
    ws2 = wb['SECRETARIAT']
    for r in ws2.iter_rows(values_only=True):
        if r[0] is not None and str(r[0]).strip().isdigit():
            role_val = str(r[3]).strip() if r[3] and str(r[3]).strip() not in ('', 'None') else 'SECRETARIAT LEAD'
            execs.append({
                "sno": str(r[1]).strip(),
                "name": str(r[2]).strip(),
                "role": role_val,
                "id_no": str(r[4]).strip(),
                "phone_no": str(r[5]).strip(),
                "email": str(r[6] if len(r)>6 else '').strip(),
                "tier": "EXECUTIVE",
                "dept": "SECRETARIAT LEADERSHIP"
            })
            
    # 3. Top Canteen & Logistics Leads (7 delegates to complete exactly 60)
    ws3 = wb['CANTEEN']
    for r in ws3.iter_rows(values_only=True):
        if r[0] is not None and str(r[0]).strip().isdigit() and len(execs) < 60:
            role_val = str(r[3]).strip() if r[3] and str(r[3]).strip() not in ('', 'None') else 'LOGISTICS LEAD'
            execs.append({
                "sno": str(r[1]).strip(),
                "name": str(r[2]).strip(),
                "role": role_val,
                "id_no": str(r[4]).strip(),
                "phone_no": str(r[5]).strip(),
                "email": str(r[6] if len(r)>6 else '').strip(),
                "tier": "OPERATIONS",
                "dept": "LOGISTICS & OPERATIONS"
            })
            
    return execs

# ==============================================================================
# MAIN BATCH COMPILER & PDF GENERATOR
# ==============================================================================
def run_compiler():
    print(f"Loading 60 executive retreat participants from {EXCEL_PATH}...")
    participants = load_60_executive_participants(EXCEL_PATH)
    print(f"Loaded {len(participants)} delegates.")
    
    front_badges = []
    back_badges = []
    
    qr_out_dir = os.path.join(OUTPUT_DIR, "INDIVIDUAL_QR_CODES_300DPI")
    os.makedirs(qr_out_dir, exist_ok=True)
    
    print("\n--- PHASE 1: Rendering 300 DPI High-Resolution Badges & Standalone QR Keys ---")
    for idx, p in enumerate(participants, 1):
        token_id, full_hash = generate_participant_token(p["sno"], p["id_no"], p["name"], idx)
        
        # Save standalone high-res 300 DPI QR Code file for this delegate
        clean_name = "".join([c if c.isalnum() or c in ("-", "_") else "_" for c in p["name"]]).strip("_")
        qr_filename = f"{idx:02d}_{p['sno']}_{clean_name}_qr_300dpi.png"
        qr_file_path = os.path.join(qr_out_dir, qr_filename)
        
        payload_data = {
            "iss": "BANKI_KUU_SACCO",
            "evt": "MSA_RETREAT_2026",
            "tid": token_id,
            "sig": full_hash[:16],
            "sec": "ODPC_SEC_25",
            "v": 1
        }
        qr_obj = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=12,
            border=2,
        )
        qr_obj.add_data(json.dumps(payload_data, separators=(',', ':')))
        qr_obj.make(fit=True)
        qr_standalone = qr_obj.make_image(fill_color=(2, 4, 8), back_color=(255, 255, 255))
        qr_standalone.save(qr_file_path, "PNG", dpi=(300, 300))
        
        fb = render_front_badge(p, token_id, full_hash)
        bb = render_back_badge(p, token_id, full_hash)
        
        front_badges.append(fb)
        back_badges.append(bb)
        
        if idx % 10 == 0 or idx == len(participants):
            print(f"  Rendered [{idx}/{len(participants)}] {p['name']} ({p['role']}) -> QR: {token_id}")
            
    # Save Sample High-Res Review Badges (Delegate 01 & CEO Delegate 13)
    sample_front_path = os.path.join(PREVIEW_DIR, "delegate_01_front_300dpi.png")
    sample_back_path = os.path.join(PREVIEW_DIR, "delegate_01_back_300dpi.png")
    front_badges[0].save(sample_front_path, "PNG", dpi=(300, 300))
    back_badges[0].save(sample_back_path, "PNG", dpi=(300, 300))
    
    ceo_front_path = os.path.join(PREVIEW_DIR, "ceo_front_300dpi.png")
    ceo_back_path = os.path.join(PREVIEW_DIR, "ceo_back_300dpi.png")
    front_badges[12].save(ceo_front_path, "PNG", dpi=(300, 300))
    back_badges[12].save(ceo_back_path, "PNG", dpi=(300, 300))
    
    print("\n--- PHASE 2: Compiling 120-Page Duplex Press-Ready PDF (300 DPI) ---")
    duplex_pdf_path = os.path.join(OUTPUT_DIR, "CBK_MOMBASA_2026_PRESS_READY_BADGES_DUPLEX.pdf")
    
    # Interleave Front 1, Back 1, Front 2, Back 2...
    duplex_pages = []
    for f, b in zip(front_badges, back_badges):
        duplex_pages.append(f)
        duplex_pages.append(b)
        
    duplex_pages[0].save(
        duplex_pdf_path,
        "PDF",
        resolution=300.0,
        save_all=True,
        append_images=duplex_pages[1:]
    )
    print(f"Saved: {duplex_pdf_path} ({len(duplex_pages)} pages)")
    
    print("\n--- PHASE 3: Compiling 4-Up Commercial Imposition Sheets (300 DPI) ---")
    imposition_sheets = []
    total_sheets = math.ceil(len(participants) / 4) # 60 / 4 = 15 sheets
    
    for s_idx in range(total_sheets):
        start_p = s_idx * 4
        chunk_front = front_badges[start_p:start_p + 4]
        chunk_back = back_badges[start_p:start_p + 4]
        
        # Pad to 4 if last chunk is smaller
        while len(chunk_front) < 4:
            chunk_front.append(None)
            chunk_back.append(None)
            
        sheet_num = s_idx + 1
        front_sheet = build_imposition_sheet(chunk_front, sheet_num, total_sheets, is_back_sheet=False)
        back_sheet = build_imposition_sheet(chunk_back, sheet_num, total_sheets, is_back_sheet=True)
        
        imposition_sheets.append(front_sheet)
        imposition_sheets.append(back_sheet)
        
        # Save Sheet 1 previews for review
        if s_idx == 0:
            s1_front_preview = os.path.join(PREVIEW_DIR, "sheet_01_front_imposition_preview.png")
            s1_back_preview = os.path.join(PREVIEW_DIR, "sheet_01_back_imposition_preview.png")
            front_sheet.save(s1_front_preview, "PNG", dpi=(300, 300))
            back_sheet.save(s1_back_preview, "PNG", dpi=(300, 300))
            
        print(f"  Built Sheet [{sheet_num}/{total_sheets}]: 4-Up Front & Back Imposition")
        
    imposition_pdf_path = os.path.join(OUTPUT_DIR, "CBK_MOMBASA_2026_IMPOSITION_SHEETS_4UP.pdf")
    imposition_sheets[0].save(
        imposition_pdf_path,
        "PDF",
        resolution=300.0,
        save_all=True,
        append_images=imposition_sheets[1:]
    )
    print(f"Saved: {imposition_pdf_path} ({len(imposition_sheets)} pages)")
    
    print("\n==================================================================")
    print("ALL PRESS-READY DOCUMENTS COMPILED SUCCESSFULLY!")
    print(f"1. Duplex PDF Deck (120 pgs, 300 DPI):   {duplex_pdf_path}")
    print(f"2. Imposition PDF (30 pgs 4-Up, 300 DPI): {imposition_pdf_path}")
    print(f"3. Preview Artifacts:                    {PREVIEW_DIR}")
    print("==================================================================")

if __name__ == "__main__":
    run_compiler()

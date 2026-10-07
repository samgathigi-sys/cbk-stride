import os
import hmac
import hashlib
import json
import math
from PIL import Image, ImageDraw, ImageFont
import qrcode
import openpyxl

# Configuration & Paths
BASE_DIR = r"C:\Users\user\.gemini\antigravity\scratch\cbk-stride"
EXCEL_PATH = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e\.user_uploaded\media_1791364617995.xlsx"
FRONT_DIR = os.path.join(BASE_DIR, "FRONT_CARDS")
BACK_DIR = os.path.join(BASE_DIR, "BACK_CARDS")
QR_DIR = os.path.join(BASE_DIR, "QR_CODES")

for d in [FRONT_DIR, BACK_DIR, QR_DIR]:
    os.makedirs(d, exist_ok=True)

HMAC_SECRET = b"BKS_MOMBASA_RETREAT_2026_ODPC_SECURE_TOKEN_SALT"

# Palette: Oceanic Navy + Warm Coastal Gold/Amber
NAVY_TOP = (5, 18, 42)
NAVY_MID = (10, 32, 70)
NAVY_BOTTOM = (3, 12, 28)
NAVY_CARD = (14, 40, 82)
NAVY_CARD_DARK = (8, 22, 48)

GOLD_LIGHT = (255, 238, 170)
GOLD_PRIMARY = (222, 172, 48)
GOLD_DARK = (165, 122, 24)
GOLD_ACCENT = (245, 185, 45)
AMBER_ACCENT = (245, 158, 11)
CYAN_ACCENT = (0, 215, 240)
TEAL_ACCENT = (20, 184, 166)

WHITE = (255, 255, 255)
OFF_WHITE = (245, 248, 255)
GRAY_LIGHT = (205, 218, 235)
GRAY_MUTED = (140, 160, 185)
TEXT_DARK = (10, 25, 50)

WIDTH = 700
HEIGHT = 1050

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

def draw_gradient_background(width, height):
    """Creates a rich oceanic navy gradient background with coastal wave curves."""
    img = Image.new("RGB", (width, height), NAVY_TOP)
    draw = ImageDraw.Draw(img)
    
    # Smooth vertical gradient
    for y in range(height):
        factor = y / float(height)
        if factor < 0.45:
            f = factor / 0.45
            r = int(NAVY_TOP[0] + (NAVY_MID[0] - NAVY_TOP[0]) * f)
            g = int(NAVY_TOP[1] + (NAVY_MID[1] - NAVY_TOP[1]) * f)
            b = int(NAVY_TOP[2] + (NAVY_MID[2] - NAVY_TOP[2]) * f)
        else:
            f = (factor - 0.45) / 0.55
            r = int(NAVY_MID[0] + (NAVY_BOTTOM[0] - NAVY_MID[0]) * f)
            g = int(NAVY_MID[1] + (NAVY_BOTTOM[1] - NAVY_MID[1]) * f)
            b = int(NAVY_MID[2] + (NAVY_BOTTOM[2] - NAVY_MID[2]) * f)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
        
    # Decorative subtle coastal wave curves at the bottom & top
    wave_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    wdraw = ImageDraw.Draw(wave_overlay)
    
    # Golden horizon lines
    for i in range(4):
        y_base = height - 130 + (i * 18)
        points = []
        for x in range(0, width + 10, 8):
            y_wave = y_base + int(math.sin((x / 65.0) + (i * 1.3)) * 7)
            points.append((x, y_wave))
        wdraw.line(points, fill=(GOLD_PRIMARY[0], GOLD_PRIMARY[1], GOLD_PRIMARY[2], 30 + i * 18), width=2)
        
    img.paste(wave_overlay, (0, 0), wave_overlay)
    return img

def draw_luxury_borders(draw, width, height):
    """Draws double gold border with stylized corner pins and lanyard guide."""
    margin1 = 22
    margin2 = 28
    draw.rounded_rectangle([(margin1, margin1), (width - margin1, height - margin1)], radius=20, outline=GOLD_PRIMARY, width=2)
    draw.rounded_rectangle([(margin2, margin2), (width - margin2, height - margin2)], radius=15, outline=GOLD_DARK, width=1)
    
    # Stylized corner ornaments
    for cx, cy in [
        (margin1 + 12, margin1 + 12),
        (width - margin1 - 12, margin1 + 12),
        (margin1 + 12, height - margin1 - 12),
        (width - margin1 - 12, height - margin1 - 12)
    ]:
        draw.polygon([(cx, cy - 5), (cx + 5, cy), (cx, cy + 5), (cx - 5, cy)], fill=GOLD_LIGHT)
        
    # Top lanyard slot marker guide
    draw.rounded_rectangle([(width // 2 - 38, 9), (width // 2 + 38, 16)], radius=3, fill=GOLD_DARK)

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
        return "Encrypted Record"
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

def generate_qr_image(token_id, full_hash, role_code, out_path):
    """Generates tokenized QR Code strictly without raw plaintext PII (ODPC compliant)."""
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
        border=2,
    )
    qr.add_data(payload_str)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color=NAVY_BOTTOM, back_color=WHITE).convert("RGBA")
    qr_img.save(out_path, "PNG")
    return qr_img

def render_front_card(participant, token_id, full_hash, out_path):
    img = draw_gradient_background(WIDTH, HEIGHT)
    draw = ImageDraw.Draw(img)
    draw_luxury_borders(draw, WIDTH, HEIGHT)
    
    # 1. Header Branding
    f_org = get_font(23, bold=True)
    f_sub = get_font(13, bold=True)
    f_loc = get_font(11, bold=False)
    
    draw.text((WIDTH // 2, 52), "BANKI KUU SACCO & BHC", fill=GOLD_LIGHT, font=f_org, anchor="mm")
    draw.text((WIDTH // 2, 79), "EXECUTIVE STRATEGIC RETREAT 2026", fill=CYAN_ACCENT, font=f_sub, anchor="mm")
    draw.text((WIDTH // 2, 101), "MOMBASA COASTAL EXPEDITION • PRIDEINN PARADISE", fill=GRAY_LIGHT, font=f_loc, anchor="mm")
    
    # Golden divider with center diamond
    div_y = 118
    draw.line([(70, div_y), (WIDTH // 2 - 18, div_y)], fill=GOLD_PRIMARY, width=1)
    draw.line([(WIDTH // 2 + 18, div_y), (WIDTH - 70, div_y)], fill=GOLD_PRIMARY, width=1)
    draw.polygon([(WIDTH // 2, div_y - 4), (WIDTH // 2 + 4, div_y), (WIDTH // 2, div_y + 4), (WIDTH // 2 - 4, div_y)], fill=GOLD_LIGHT)
    
    # 2. Styled Photo Placeholder Frame
    frame_w, frame_h = 260, 300
    frame_x0 = (WIDTH - frame_w) // 2
    frame_y0 = 145
    frame_x1 = frame_x0 + frame_w
    frame_y1 = frame_y0 + frame_h
    
    # Frame background
    draw.rounded_rectangle([(frame_x0, frame_y0), (frame_x1, frame_y1)], radius=16, fill=NAVY_CARD_DARK, outline=GOLD_PRIMARY, width=3)
    draw.rounded_rectangle([(frame_x0 + 6, frame_y0 + 6), (frame_x1 - 6, frame_y1 - 6)], radius=12, outline=GOLD_DARK, width=1)
    
    # Styled photo placeholder interior icon & instructions
    cx = WIDTH // 2
    cy = frame_y0 + 110
    
    # Camera / Portrait silhouette vector icon
    draw.ellipse([(cx - 45, cy - 50), (cx + 45, cy + 40)], outline=GOLD_PRIMARY, width=2)
    # Head circle
    draw.ellipse([(cx - 20, cy - 35), (cx + 20, cy + 5)], fill=GOLD_DARK)
    # Body arc
    draw.chord([(cx - 36, cy - 2), (cx + 36, cy + 40)], 0, 180, fill=GOLD_DARK)
    
    f_ph1 = get_font(14, bold=True)
    f_ph2 = get_font(11, bold=False)
    f_ph3 = get_font(10, bold=False)
    draw.text((cx, frame_y0 + 205), "PARTICIPANT PHOTO", fill=GOLD_LIGHT, font=f_ph1, anchor="mm")
    draw.text((cx, frame_y0 + 228), "[ ATTACH 2×2 COLOUR HEADSHOT ]", fill=GRAY_LIGHT, font=f_ph2, anchor="mm")
    draw.text((cx, frame_y0 + 252), "VERIFIED RETREAT CREDENTIAL", fill=CYAN_ACCENT, font=f_ph3, anchor="mm")
    draw.rounded_rectangle([(frame_x0 + 35, frame_y0 + 270), (frame_x1 - 35, frame_y0 + 272)], radius=1, fill=GOLD_DARK)
    
    # 3. Participant Name Section
    name = str(participant.get("name", "EXECUTIVE DELEGATE")).strip()
    f_name = get_font(26, bold=True)
    
    # Check if name is too wide; shrink or wrap
    bbox = draw.textbbox((0, 0), name, font=f_name)
    name_w = bbox[2] - bbox[0]
    if name_w > 580:
        f_name = get_font(22, bold=True)
        bbox = draw.textbbox((0, 0), name, font=f_name)
        name_w = bbox[2] - bbox[0]
        if name_w > 580:
            f_name = get_font(19, bold=True)
            
    name_y = 500
    draw.text((WIDTH // 2, name_y), name, fill=WHITE, font=f_name, anchor="mm")
    
    # 4. Designation / Role Pill Badge
    role = str(participant.get("role", "EXECUTIVE DELEGATE")).strip()
    if not role or role == "None":
        role = "EXECUTIVE DELEGATE"
    role_display = role.upper()
    
    f_role = get_font(15, bold=True)
    r_bbox = draw.textbbox((0, 0), role_display, font=f_role)
    pill_w = max(260, (r_bbox[2] - r_bbox[0]) + 46)
    pill_h = 38
    pill_x0 = (WIDTH - pill_w) // 2
    pill_y0 = 545
    pill_x1 = pill_x0 + pill_w
    pill_y1 = pill_y0 + pill_h
    
    # Gold gradient / styled pill
    draw.rounded_rectangle([(pill_x0, pill_y0), (pill_x1, pill_y1)], radius=19, fill=GOLD_PRIMARY, outline=GOLD_LIGHT, width=2)
    draw.text((WIDTH // 2, pill_y0 + pill_h // 2), role_display, fill=TEXT_DARK, font=f_role, anchor="mm")
    
    # 5. Access & Identification Card Details Box
    info_box_y0 = 615
    info_box_y1 = 765
    draw.rounded_rectangle([(55, info_box_y0), (WIDTH - 55, info_box_y1)], radius=14, fill=NAVY_CARD, outline=GOLD_DARK, width=1)
    
    f_lbl = get_font(12, bold=True)
    f_val = get_font(14, bold=True)
    f_mono = get_font(13, bold=False)
    
    # Left column: Pass ID & Serial No
    draw.text((85, info_box_y0 + 24), "DIGITAL TOKEN ID", fill=GRAY_MUTED, font=f_lbl)
    draw.text((85, info_box_y0 + 46), token_id, fill=GOLD_LIGHT, font=f_val)
    
    serial_no = str(participant.get("serial", "N/A")).strip()
    draw.text((85, info_box_y0 + 82), "STAFF / S.NO", fill=GRAY_MUTED, font=f_lbl)
    draw.text((85, info_box_y0 + 104), f"#{serial_no}", fill=WHITE, font=f_val)
    
    # Vertical divider inside box
    draw.line([(WIDTH // 2, info_box_y0 + 18), (WIDTH // 2, info_box_y1 - 18)], fill=GOLD_DARK, width=1)
    
    # Right column: Access Level & Retreat Year
    tier = participant.get("tier", "EXECUTIVE")
    draw.text((WIDTH // 2 + 30, info_box_y0 + 24), "ACCESS CLEARANCE", fill=GRAY_MUTED, font=f_lbl)
    draw.text((WIDTH // 2 + 30, info_box_y0 + 46), f"{tier} LEVEL", fill=CYAN_ACCENT, font=f_val)
    
    sgr_time = participant.get("sgr_time", "")
    sgr_text = f"SGR: {sgr_time}" if sgr_time else "MOMBASA 2026"
    draw.text((WIDTH // 2 + 30, info_box_y0 + 82), "LOGISTICS / ITINERARY", fill=GRAY_MUTED, font=f_lbl)
    draw.text((WIDTH // 2 + 30, info_box_y0 + 104), sgr_text, fill=WHITE, font=f_val)
    
    # 6. Cryptographic ODPC Security Watermark Strip
    sec_strip_y0 = 790
    sec_strip_y1 = 860
    draw.rounded_rectangle([(55, sec_strip_y0), (WIDTH - 55, sec_strip_y1)], radius=10, fill=NAVY_CARD_DARK, outline=CYAN_ACCENT, width=1)
    f_sec_h = get_font(11, bold=True)
    f_sec_t = get_font(10, bold=False)
    draw.text((WIDTH // 2, sec_strip_y0 + 18), "ODPC §25 ENCRYPTED DIGITAL PASSPORT", fill=CYAN_ACCENT, font=f_sec_h, anchor="mm")
    draw.text((WIDTH // 2, sec_strip_y0 + 42), f"SIG: {full_hash[:32]}...", fill=GRAY_LIGHT, font=f_sec_t, anchor="mm")
    
    # 7. Bottom VIP Banner
    banner_y0 = 890
    banner_y1 = 980
    draw.rounded_rectangle([(45, banner_y0), (WIDTH - 45, banner_y1)], radius=14, fill=GOLD_PRIMARY, outline=GOLD_LIGHT, width=2)
    f_ban1 = get_font(18, bold=True)
    f_ban2 = get_font(12, bold=True)
    
    # Draw decorative gold diamonds next to text
    text_banner = "ALL-ACCESS EXECUTIVE DELEGATE"
    tb_bbox = draw.textbbox((0, 0), text_banner, font=f_ban1)
    tb_w = tb_bbox[2] - tb_bbox[0]
    draw.text((WIDTH // 2, banner_y0 + 26), text_banner, fill=TEXT_DARK, font=f_ban1, anchor="mm")
    
    # Left diamond
    ld_x = (WIDTH - tb_w) // 2 - 20
    ld_y = banner_y0 + 26
    draw.polygon([(ld_x, ld_y - 6), (ld_x + 6, ld_y), (ld_x, ld_y + 6), (ld_x - 6, ld_y)], fill=NAVY_BOTTOM)
    # Right diamond
    rd_x = (WIDTH + tb_w) // 2 + 20
    rd_y = banner_y0 + 26
    draw.polygon([(rd_x, rd_y - 6), (rd_x + 6, rd_y), (rd_x, rd_y + 6), (rd_x - 6, rd_y)], fill=NAVY_BOTTOM)
    
    draw.text((WIDTH // 2, banner_y0 + 58), "GOVERNANCE • INNOVATION • STRATEGIC HARMONY", fill=NAVY_BOTTOM, font=f_ban2, anchor="mm")
    
    img.save(out_path, "PNG", quality=95)
    return img

def render_back_card(participant, token_id, full_hash, qr_path, out_path):
    img = draw_gradient_background(WIDTH, HEIGHT)
    draw = ImageDraw.Draw(img)
    draw_luxury_borders(draw, WIDTH, HEIGHT)
    
    # 1. Header
    f_org = get_font(21, bold=True)
    f_sub = get_font(12, bold=True)
    
    draw.text((WIDTH // 2, 52), "RETREAT ITINERARY & ACCESS KEY", fill=GOLD_LIGHT, font=f_org, anchor="mm")
    draw.text((WIDTH // 2, 78), "3-DAY LEADERSHIP RETREAT • MOMBASA, KENYA", fill=CYAN_ACCENT, font=f_sub, anchor="mm")
    
    # Divider
    div_y = 96
    draw.line([(60, div_y), (WIDTH - 60, div_y)], fill=GOLD_PRIMARY, width=1)
    
    # 2. Itinerary Schedule Cards
    itin_start_y = 110
    card_h = 74
    gap = 10
    
    days_data = [
        ("DAY 1 • THURSDAY", "SGR Express Transit & Coastal Check-in", "Welcome Reception, Strategy Keynote & Networking Dinner", TEAL_ACCENT),
        ("DAY 2 • FRIDAY", "Strategic Governance & Team Challenges", "Beach Leadership Dynamics, Innovation Sprint & Gala Night", GOLD_ACCENT),
        ("DAY 3 • SATURDAY", "Marine Excursion & Leadership Synthesis", "Fort Jesus & Diani Excursion, Resolutions & Return Transit", CYAN_ACCENT),
    ]
    
    f_day_lbl = get_font(12, bold=True)
    f_day_t1 = get_font(13, bold=True)
    f_day_t2 = get_font(11, bold=False)
    
    for idx, (day_title, title_main, title_sub, accent_color) in enumerate(days_data):
        cy0 = itin_start_y + idx * (card_h + gap)
        cy1 = cy0 + card_h
        draw.rounded_rectangle([(50, cy0), (WIDTH - 50, cy1)], radius=10, fill=NAVY_CARD, outline=accent_color, width=1)
        
        # Day Tag Badge
        draw.rounded_rectangle([(65, cy0 + 10), (220, cy0 + 34)], radius=6, fill=accent_color)
        draw.text((142, cy0 + 22), day_title, fill=TEXT_DARK, font=f_day_lbl, anchor="mm")
        
        draw.text((235, cy0 + 22), title_main, fill=WHITE, font=f_day_t1, anchor="lm")
        draw.text((68, cy0 + 52), f"• {title_sub}", fill=GRAY_LIGHT, font=f_day_t2, anchor="lm")
        
    # 3. QR Code Section (Centerpiece)
    qr_box_y0 = 385
    qr_box_y1 = 665
    qr_box_w = 420
    qr_box_x0 = (WIDTH - qr_box_w) // 2
    qr_box_x1 = qr_box_x0 + qr_box_w
    
    draw.rounded_rectangle([(qr_box_x0, qr_box_y0), (qr_box_x1, qr_box_y1)], radius=16, fill=WHITE, outline=GOLD_PRIMARY, width=3)
    
    # Load and paste QR code inside
    qr_img = Image.open(qr_path).convert("RGBA")
    qr_display_size = 190
    qr_resized = qr_img.resize((qr_display_size, qr_display_size), Image.Resampling.LANCZOS)
    
    paste_x = (WIDTH - qr_display_size) // 2
    paste_y = qr_box_y0 + 16
    img.paste(qr_resized, (paste_x, paste_y), qr_resized)
    
    f_qr_label = get_font(13, bold=True)
    f_qr_tok = get_font(14, bold=True)
    f_qr_sig = get_font(10, bold=False)
    
    draw.text((WIDTH // 2, qr_box_y0 + 220), "DIGITAL EVENT ACCESS KEY", fill=TEXT_DARK, font=f_qr_label, anchor="mm")
    draw.text((WIDTH // 2, qr_box_y0 + 242), token_id, fill=NAVY_MID, font=f_qr_tok, anchor="mm")
    draw.text((WIDTH // 2, qr_box_y0 + 262), "SCAN FOR SESSIONS, MEALS & RETREAT ACCESS", fill=GOLD_DARK, font=f_qr_sig, anchor="mm")
    
    # 4. ODPC Compliance Shield & PII-Masked Metadata Box
    meta_y0 = 685
    meta_y1 = 880
    draw.rounded_rectangle([(50, meta_y0), (WIDTH - 50, meta_y1)], radius=14, fill=NAVY_CARD_DARK, outline=GOLD_PRIMARY, width=1)
    
    f_odpc_h = get_font(12, bold=True)
    f_odpc_lbl = get_font(11, bold=True)
    f_odpc_val = get_font(12, bold=False)
    f_notice = get_font(10, bold=False)
    
    # Shield vector icon
    sh_x, sh_y = 120, meta_y0 + 20
    draw.polygon([(sh_x, sh_y - 8), (sh_x + 7, sh_y - 5), (sh_x + 7, sh_y + 2), (sh_x, sh_y + 8), (sh_x - 7, sh_y + 2), (sh_x - 7, sh_y - 5)], fill=CYAN_ACCENT)
    
    # ODPC Shield header
    draw.text((WIDTH // 2 + 10, meta_y0 + 20), "KENYA DATA PROTECTION ACT (ODPC 2019) COMPLIANT", fill=GOLD_LIGHT, font=f_odpc_h, anchor="mm")
    draw.line([(70, meta_y0 + 36), (WIDTH - 70, meta_y0 + 36)], fill=GOLD_DARK, width=1)
    
    # Masked Metadata grid
    masked_id_str = mask_id(participant.get("id_no"))
    masked_phone_str = mask_phone(participant.get("phone_no"))
    masked_email_str = mask_email(participant.get("email"))
    
    # Col 1: Masked ID & Masked Phone
    draw.text((80, meta_y0 + 54), "PROTECTED ID:", fill=GRAY_MUTED, font=f_odpc_lbl)
    draw.text((210, meta_y0 + 54), masked_id_str, fill=WHITE, font=f_odpc_val)
    
    draw.text((80, meta_y0 + 82), "PROTECTED TEL:", fill=GRAY_MUTED, font=f_odpc_lbl)
    draw.text((210, meta_y0 + 82), masked_phone_str, fill=WHITE, font=f_odpc_val)
    
    draw.text((80, meta_y0 + 110), "OFFICIAL EMAIL:", fill=GRAY_MUTED, font=f_odpc_lbl)
    draw.text((210, meta_y0 + 110), masked_email_str, fill=GRAY_LIGHT, font=f_odpc_val)
    
    draw.text((80, meta_y0 + 138), "CRYPTO SIG:", fill=GRAY_MUTED, font=f_odpc_lbl)
    draw.text((210, meta_y0 + 138), f"SHA256-{full_hash[:20]}...", fill=CYAN_ACCENT, font=f_odpc_val)
    
    draw.text((WIDTH // 2, meta_y0 + 172), "All personal identifiable data is protected by one-way tokenization.", fill=GRAY_MUTED, font=f_notice, anchor="mm")
    
    # 5. Emergency Contacts & Venue Footer
    f_foot1 = get_font(12, bold=True)
    f_foot2 = get_font(10, bold=False)
    
    draw.text((WIDTH // 2, 915), "PrideInn Paradise Beach Resort & Spa, Shanzu, Mombasa", fill=GOLD_LIGHT, font=f_foot1, anchor="mm")
    draw.text((WIDTH // 2, 940), "Secretariat Logistics Desk Hotline: +254 711 875 393 / +254 728 028 932", fill=GRAY_LIGHT, font=f_foot2, anchor="mm")
    draw.text((WIDTH // 2, 965), "This official pass must be worn visibly at all times during retreat events.", fill=GRAY_MUTED, font=f_foot2, anchor="mm")
    
    img.save(out_path, "PNG", quality=95)
    return img

def load_all_participants(excel_path):
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    participants = []
    
    # 1. BOD, Supervisory, Branch Reps, CEO
    ws1 = wb['BOD,SC,BRANCH REPS & BHC BOD']
    for row in ws1.iter_rows(values_only=True):
        if row[0] is not None and str(row[0]).strip().isdigit():
            raw_role = str(row[3]).strip() if row[3] is not None else ""
            if not raw_role or raw_role.upper() == "NONE":
                raw_role = "BRANCH REPRESENTATIVE"
            participants.append({
                "no": int(row[0]),
                "serial": str(row[1] or "").strip(),
                "name": str(row[2] or "").strip(),
                "role": raw_role,
                "id_no": str(row[4] or "").strip(),
                "phone_no": str(row[5] or "").strip(),
                "email": str(row[6] or "").strip() if len(row) > 6 else "",
                "tier": "EXECUTIVE",
                "category": "BOD / SUPERVISORY / BRANCH REP",
                "sgr_time": "15:00 HRS"
            })
            
    # 2. Secretariat
    ws2 = wb['SECRETARIAT']
    for row in ws2.iter_rows(values_only=True):
        if row[0] is not None and str(row[0]).strip().isdigit():
            role_val = str(row[3] or "SECRETARIAT").strip()
            participants.append({
                "no": len(participants) + 1,
                "serial": str(row[1] or "").strip(),
                "name": str(row[2] or "").strip(),
                "role": role_val,
                "id_no": str(row[4] or "").strip(),
                "phone_no": str(row[5] or "").strip(),
                "email": str(row[6] or "").strip() if len(row) > 6 else "",
                "tier": "EXECUTIVE" if "INTERN" not in role_val.upper() else "SUPPORT",
                "category": "SECRETARIAT LEADERSHIP",
                "sgr_time": "15:00 HRS"
            })
            
    # 3. Canteen & Casual Staff
    ws3 = wb['CANTEEN']
    for row in ws3.iter_rows(values_only=True):
        if row[0] is not None and str(row[0]).strip().isdigit():
            role_val = str(row[3] or "OPERATIONS STAFF").strip()
            participants.append({
                "no": len(participants) + 1,
                "serial": str(row[1] or "").strip(),
                "name": str(row[2] or "").strip(),
                "role": role_val,
                "id_no": str(row[4] or "").strip(),
                "phone_no": str(row[5] or "").strip(),
                "email": str(row[6] or "").strip() if len(row) > 6 else "",
                "tier": "OPERATIONS",
                "category": "OPERATIONS & HOSPITALITY",
                "sgr_time": "08:00 HRS"
            })
            
    return participants

def sanitize_filename(name):
    clean = "".join([c if c.isalnum() or c in ("-", "_") else "_" for c in name])
    while "__" in clean:
        clean = clean.replace("__", "_")
    return clean.strip("_")

def run_pipeline():
    print(f"Loading participant records from: {EXCEL_PATH}")
    participants = load_all_participants(EXCEL_PATH)
    print(f"Loaded {len(participants)} total participants.")
    
    registry = []
    
    for idx, p in enumerate(participants, 1):
        serial_no = p["serial"] or f"{idx:04d}"
        clean_name = sanitize_filename(p["name"])
        file_prefix = f"{idx:02d}_{serial_no}_{clean_name}"
        
        token_id, full_hash = generate_participant_token(serial_no, p["id_no"], p["name"], idx)
        
        qr_filename = f"{file_prefix}_qr.png"
        front_filename = f"{file_prefix}_front.png"
        back_filename = f"{file_prefix}_back.png"
        
        qr_path = os.path.join(QR_DIR, qr_filename)
        front_path = os.path.join(FRONT_DIR, front_filename)
        back_path = os.path.join(BACK_DIR, back_filename)
        
        # 1. Generate QR Code
        generate_qr_image(token_id, full_hash, p["tier"], qr_path)
        
        # 2. Render Front Card
        render_front_card(p, token_id, full_hash, front_path)
        
        # 3. Render Back Card
        render_back_card(p, token_id, full_hash, qr_path, back_path)
        
        registry.append({
            "index": idx,
            "serial": serial_no,
            "full_name": p["name"],
            "role": p["role"],
            "category": p["category"],
            "tier": p["tier"],
            "token_id": token_id,
            "crypto_sig": full_hash,
            "masked_id": mask_id(p["id_no"]),
            "masked_phone": mask_phone(p["phone_no"]),
            "masked_email": mask_email(p["email"]),
            "qr_code_file": qr_filename,
            "front_card_file": front_filename,
            "back_card_file": back_filename
        })
        
        if idx % 10 == 0 or idx == len(participants):
            print(f"  Processed [{idx}/{len(participants)}] {p['name']} ({p['role']})")
            
    # Save registry JSON and CSV
    reg_json_path = os.path.join(BASE_DIR, "RETREAT_BADGES_REGISTRY.json")
    with open(reg_json_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)
        
    import csv
    reg_csv_path = os.path.join(BASE_DIR, "RETREAT_BADGES_REGISTRY.csv")
    with open(reg_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(registry[0].keys()))
        writer.writeheader()
        writer.writerows(registry)
        
    print("\n=======================================================")
    print(f"Successfully generated all {len(participants)} retreat badges!")
    print(f"• FRONT_CARDS: {FRONT_DIR} ({len(os.listdir(FRONT_DIR))} files)")
    print(f"• BACK_CARDS:  {BACK_DIR} ({len(os.listdir(BACK_DIR))} files)")
    print(f"• QR_CODES:    {QR_DIR} ({len(os.listdir(QR_DIR))} files)")
    print(f"• Registry:    {reg_csv_path}")
    print("=======================================================")

if __name__ == "__main__":
    run_pipeline()


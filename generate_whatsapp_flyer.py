"""
CBK STRIDE - Creative WhatsApp E-Flyer Generator
Produces ultra-sharp, executive-grade mobile flyers for WhatsApp sharing:
1. 1080x1920 (9:16 Portrait - Ideal for WhatsApp Status / Fullscreen View)
2. 1080x1350 (4:5 Portrait - Ideal for WhatsApp Chat Feed & Group Sharing)
"""

import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(OUTPUT_DIR, "cbk_logo.png")
PORTAL_URL = "https://cbk-stride.streamlit.app"

# CBK Corporate Palette
COLOR_NAVY_BG = (8, 20, 40)            # #081428 Deep Midnight Navy
COLOR_NAVY_CARD = (15, 30, 58)          # #0F1E3A Dark Sapphire Card
COLOR_NAVY_ACCENT = (22, 45, 84)        # Card Header / border
COLOR_ROYAL_BLUE = (2, 91, 191)         # #025BBF Official CBK Blue
COLOR_GOLD = (248, 184, 45)             # #F8B82D Official CBK Saffron Gold
COLOR_AMBER = (247, 148, 29)            # #F7941D Amber Accent
COLOR_ICE_BLUE = (238, 246, 252)        # #EEF6FC Ice Blue Tint
COLOR_WHITE = (255, 255, 255)
COLOR_TEXT_MUTED = (165, 185, 210)      # Slate Silver
COLOR_EMERALD = (16, 185, 129)          # Verified Green
COLOR_BORDER_GOLD = (248, 184, 45, 220)
COLOR_BORDER_SUBTLE = (35, 65, 110)

WIN_FONTS = os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts")

def get_font(font_name, size):
    path = os.path.join(WIN_FONTS, font_name)
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines


# ==============================================================================
# FLYER 1: 1080 x 1920 (9:16 Full Screen / Status)
# ==============================================================================
def build_fullscreen_flyer():
    WIDTH = 1080
    HEIGHT = 1920
    im = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_NAVY_BG)
    draw = ImageDraw.Draw(im)

    # 1. Subtle Radial / Gradient Glow in Header
    for y in range(500):
        intensity = 1.0 - (y / 500.0)
        alpha = int(90 * intensity)
        draw.line([(0, y), (WIDTH, y)], fill=(2, 91, 191, alpha))

    # Top & Bottom Gold Framing Stripes
    draw.rectangle([(0, 0), (WIDTH, 14)], fill=COLOR_GOLD)
    draw.rectangle([(0, HEIGHT - 14), (WIDTH, HEIGHT)], fill=COLOR_GOLD)

    # 2. Header & Logo
    logo_y = 48
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo_w = 125
            ratio = logo_w / float(logo.width)
            logo_h = int(float(logo.height) * ratio)
            logo_res = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
            
            # White Pill Badge for Crest
            pill_pad = 12
            pill_box = [
                (WIDTH // 2 - logo_w // 2 - pill_pad, logo_y - 6),
                (WIDTH // 2 + logo_w // 2 + pill_pad, logo_y + logo_h + 6)
            ]
            draw.rounded_rectangle(pill_box, radius=20, fill=(255, 255, 255, 255), outline=COLOR_GOLD, width=3)
            im.paste(logo_res, (WIDTH // 2 - logo_w // 2, logo_y), logo_res)
            curr_y = logo_y + logo_h + 22
        except Exception:
            curr_y = logo_y + 40
    else:
        curr_y = logo_y + 40

    # Institutional Text
    font_sub_inst = get_font("segoeuib.ttf", 20)
    inst_txt = "BANKI KUU YA KENYA  •  CENTRAL BANK OF KENYA"
    bbox = draw.textbbox((0, 0), inst_txt, font=font_sub_inst)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, curr_y), inst_txt, font=font_sub_inst, fill=COLOR_GOLD)
    curr_y += 30

    font_sub_dept = get_font("segoeui.ttf", 19)
    dept_txt = "SPORTS SECRETARIAT  &  HUMAN RESOURCES"
    bbox = draw.textbbox((0, 0), dept_txt, font=font_sub_dept)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, curr_y), dept_txt, font=font_sub_dept, fill=COLOR_ICE_BLUE)
    curr_y += 45

    # 3. Hero Acronym Block
    hero_w = WIDTH - 120
    hero_h = 240
    hero_top = curr_y
    draw.rounded_rectangle([(60, hero_top), (WIDTH - 60, hero_top + hero_h)], radius=24, fill=COLOR_NAVY_CARD, outline=COLOR_GOLD, width=3)

    # Accent Stripe in Hero Card
    draw.rounded_rectangle([(68, hero_top + 8), (WIDTH - 68, hero_top + 20)], radius=6, fill=COLOR_ROYAL_BLUE)

    font_hero = get_font("ariblk.ttf", 80)
    hero_txt = "CBK STRIDE™"
    bbox = draw.textbbox((0, 0), hero_txt, font=font_hero)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, hero_top + 34), hero_txt, font=font_hero, fill=COLOR_GOLD)

    font_acronym = get_font("segoeuib.ttf", 21)
    acronym_full = "SPORTS TELEMETRY, ROSTER INTEGRITY & DIGITAL ENROLLMENT"
    bbox = draw.textbbox((0, 0), acronym_full, font=font_acronym)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, hero_top + 135), acronym_full, font=font_acronym, fill=COLOR_WHITE)

    font_hero_tag = get_font("segoeuib.ttf", 24)
    tag_hero = ">> THE SMART DIGITAL STADIUM IN YOUR POCKET <<"
    bbox = draw.textbbox((0, 0), tag_hero, font=font_hero_tag)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, hero_top + 180), tag_hero, font=font_hero_tag, fill=COLOR_AMBER)

    curr_y = hero_top + hero_h + 36

    # 4. 4-Pillar Feature Grid (2x2)
    grid_w = (WIDTH - 120 - 24) // 2
    grid_h = 210

    cards_data = [
        {
            "badge": "ZERO PAPERWORK",
            "title": "2-Sec Pitch Check-In",
            "desc": "Athletes flash dynamic anti-tamper QR pass at Gate 1 & pitch-side. Done instantly.",
            "accent": COLOR_GOLD
        },
        {
            "badge": "18 DISCIPLINES",
            "title": "All Sports Unified",
            "desc": "Golf, Athletics, Football, Netball, Volleyball, Tug of War, Darts & Table Tennis.",
            "accent": COLOR_ICE_BLUE
        },
        {
            "badge": "REAL-TIME SYNC",
            "title": "Live Google Sheets",
            "desc": "Automated attendance rosters and tournament analytics stream live to Secretariat & HR.",
            "accent": COLOR_EMERALD
        },
        {
            "badge": "100% RING-FENCED",
            "title": "CBK Data Sovereignty",
            "desc": "KDPA 2019 compliant. Encrypted telemetry strictly confined to Central Bank network.",
            "accent": COLOR_GOLD
        }
    ]

    font_card_badge = get_font("segoeuib.ttf", 17)
    font_card_title = get_font("segoeuib.ttf", 25)
    font_card_desc = get_font("segoeui.ttf", 19)

    for i, card in enumerate(cards_data):
        c_col = i % 2
        c_row = i // 2
        x0 = 60 + c_col * (grid_w + 24)
        y0 = curr_y + c_row * (grid_h + 20)
        x1 = x0 + grid_w
        y1 = y0 + grid_h

        draw.rounded_rectangle([(x0, y0), (x1, y1)], radius=20, fill=COLOR_NAVY_CARD, outline=COLOR_BORDER_SUBTLE, width=2)
        
        # Mini Badge
        b_box = [(x0 + 16, y0 + 16), (x0 + 200, y0 + 44)]
        draw.rounded_rectangle(b_box, radius=8, fill=COLOR_ROYAL_BLUE)
        draw.text((x0 + 26, y0 + 19), card["badge"], font=font_card_badge, fill=card["accent"])

        # Title
        draw.text((x0 + 16, y0 + 58), card["title"], font=font_card_title, fill=COLOR_WHITE)

        # Description wrapped
        lines = wrap_text(draw, card["desc"], font_card_desc, grid_w - 32)
        dy = y0 + 104
        for ln in lines:
            draw.text((x0 + 16, dy), ln, font=font_card_desc, fill=COLOR_TEXT_MUTED)
            dy += 28

    curr_y += (grid_h * 2) + 40

    # 5. Step-by-Step Flow (3 Simple Steps)
    flow_h = 105
    draw.rounded_rectangle([(60, curr_y), (WIDTH - 60, curr_y + flow_h)], radius=18, fill=COLOR_NAVY_CARD, outline=COLOR_ROYAL_BLUE, width=2)

    font_step_num = get_font("ariblk.ttf", 24)
    font_step_title = get_font("segoeuib.ttf", 19)
    font_step_sub = get_font("segoeui.ttf", 15)

    step_w = (WIDTH - 120) // 3
    steps = [
        ("1", "FLASH BADGE", "Show digital pass"),
        ("2", "CAPTAIN SCANS", "2-sec verification"),
        ("3", "ROSTER UPDATED", "Synced to Google Sheet")
    ]
    for idx, (num, stitle, ssub) in enumerate(steps):
        sx = 60 + idx * step_w
        # Circle badge
        draw.ellipse([(sx + 20, curr_y + 24), (sx + 74, curr_y + 78)], fill=COLOR_ROYAL_BLUE, outline=COLOR_GOLD, width=2)
        draw.text((sx + 38, curr_y + 34), num, font=font_step_num, fill=COLOR_GOLD)
        draw.text((sx + 88, curr_y + 28), stitle, font=font_step_title, fill=COLOR_WHITE)
        draw.text((sx + 88, curr_y + 56), ssub, font=font_step_sub, fill=COLOR_TEXT_MUTED)

    curr_y += flow_h + 36

    # 6. Live Portal QR Action Box
    qr_card_top = curr_y
    qr_card_h = 360
    draw.rounded_rectangle([(60, qr_card_top), (WIDTH - 60, qr_card_top + qr_card_h)], radius=24, fill=COLOR_NAVY_CARD, outline=COLOR_GOLD, width=3)

    # QR Code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=8, border=2)
    qr.add_data(PORTAL_URL)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#081428", back_color="#FFFFFF").convert("RGBA")
    qr_size = 230
    qr_res = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    qr_x = 90
    qr_y = qr_card_top + 45
    # White background for QR code
    draw.rounded_rectangle([(qr_x - 10, qr_y - 10), (qr_x + qr_size + 10, qr_y + qr_size + 10)], radius=16, fill=COLOR_WHITE, outline=COLOR_GOLD, width=2)
    im.paste(qr_res, (qr_x, qr_y), qr_res)

    font_qr_label = get_font("segoeuib.ttf", 15)
    qr_lbl = "SCAN WITH CAMERA"
    bbox = draw.textbbox((0, 0), qr_lbl, font=font_qr_label)
    draw.text((qr_x + (qr_size - (bbox[2] - bbox[0])) // 2, qr_y + qr_size + 18), qr_lbl, font=font_qr_label, fill=COLOR_GOLD)

    # Right Column inside QR Card
    rx = qr_x + qr_size + 45
    ry = qr_card_top + 40

    font_action_tag = get_font("segoeuib.ttf", 16)
    draw.text((rx, ry), "LIVE CLOUDFLARE BOARDROOM PORTAL", font=font_action_tag, fill=COLOR_GOLD)
    ry += 30

    font_action_h = get_font("ariblk.ttf", 36)
    draw.text((rx, ry), "Experience It Live", font=font_action_h, fill=COLOR_WHITE)
    ry += 52

    action_points = [
        "• Instant Athlete Enrollment & ID verification",
        "• Live Golfers & Athletics rosters",
        "• Real-time attendance counter & chart",
        "• 100% Mobile friendly - zero installation"
    ]
    font_point = get_font("segoeui.ttf", 19)
    for pt in action_points:
        draw.text((rx, ry), pt, font=font_point, fill=COLOR_ICE_BLUE)
        ry += 32

    ry += 14
    draw.rounded_rectangle([(rx, ry), (rx + 420, ry + 44)], radius=10, fill=COLOR_ROYAL_BLUE, outline=COLOR_GOLD, width=1)
    font_url_txt = get_font("segoeuib.ttf", 16)
    draw.text((rx + 20, ry + 11), "variations-ribbon-cached-expires...", font=font_url_txt, fill=COLOR_WHITE)

    curr_y = qr_card_top + qr_card_h + 35

    # 7. Sports Disciplines Pill Strip
    draw.text((60, curr_y), "OFFICIAL CBK DISCIPLINES POWERED:", font=font_action_tag, fill=COLOR_GOLD)
    curr_y += 28

    sports_tags_1 = "GOLF  •  ATHLETICS  •  FOOTBALL  •  NETBALL  •  VOLLEYBALL"
    sports_tags_2 = "BASKETBALL  •  TABLE TENNIS  •  DARTS  •  CHESS  •  TUG OF WAR"
    font_sports = get_font("segoeuib.ttf", 18)
    draw.text((60, curr_y), sports_tags_1, font=font_sports, fill=COLOR_ICE_BLUE)
    curr_y += 28
    draw.text((60, curr_y), sports_tags_2, font=font_sports, fill=COLOR_ICE_BLUE)
    curr_y += 42

    # 8. Creative Acronym Alternatives Section (Subtle Pill Strip)
    font_acronym_header = get_font("segoeuib.ttf", 17)
    draw.text((60, curr_y), "CREATIVE ACRONYM NOMINATIONS FOR CBK BOARD:", font=font_acronym_header, fill=COLOR_GOLD)
    curr_y += 28

    font_acronym_item = get_font("segoeui.ttf", 17)
    acronym_list = [
        "1. CBK STRIDE™ : Sports Telemetry, Roster Integrity & Digital Enrollment (Recommended)",
        "2. CBK SWIFT™ : Sports Wellness & Integrity Field Terminal (Banking Nod)",
        "3. CBK PULSE™ : Participation, Unified Logistics & Sports Engagement"
    ]
    for ac in acronym_list:
        draw.text((60, curr_y), ac, font=font_acronym_item, fill=COLOR_TEXT_MUTED)
        curr_y += 26

    # 8. Footer
    font_footer = get_font("segoeuib.ttf", 16)
    ftxt = "CENTRAL BANK OF KENYA  •  OFFICIAL SPORTS SECRETARIAT  •  SEPTEMBER 2026"
    bbox = draw.textbbox((0, 0), ftxt, font=font_footer)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, HEIGHT - 54), ftxt, font=font_footer, fill=COLOR_GOLD)

    out_png = os.path.join(OUTPUT_DIR, "CBK_STRIDE_WhatsApp_Story_9x16.png")
    out_jpg = os.path.join(OUTPUT_DIR, "CBK_STRIDE_WhatsApp_Story_9x16.jpg")
    rgb_im = im.convert("RGB")
    rgb_im.save(out_png, "PNG", optimize=True)
    rgb_im.save(out_jpg, "JPEG", quality=88, optimize=True)
    print(f"✅ Generated 9:16 Fullscreen Flyer: {out_jpg} ({os.path.getsize(out_jpg)/1024:.1f} KB)")


# ==============================================================================
# FLYER 2: 1080 x 1350 (4:5 WhatsApp Post - Compact & Punchy)
# ==============================================================================
def build_compact_flyer():
    WIDTH = 1080
    HEIGHT = 1350
    im = Image.new("RGBA", (WIDTH, HEIGHT), COLOR_NAVY_BG)
    draw = ImageDraw.Draw(im)

    # Gradient header
    for y in range(400):
        intensity = 1.0 - (y / 400.0)
        alpha = int(80 * intensity)
        draw.line([(0, y), (WIDTH, y)], fill=(2, 91, 191, alpha))

    # Framing borders
    draw.rectangle([(0, 0), (WIDTH, 12)], fill=COLOR_GOLD)
    draw.rectangle([(0, HEIGHT - 12), (WIDTH, HEIGHT)], fill=COLOR_GOLD)

    # Logo & Crest
    logo_y = 35
    if os.path.exists(LOGO_PATH):
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
            logo_w = 110
            ratio = logo_w / float(logo.width)
            logo_h = int(float(logo.height) * ratio)
            logo_res = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

            pill_pad = 10
            pill_box = [
                (WIDTH // 2 - logo_w // 2 - pill_pad, logo_y - 4),
                (WIDTH // 2 + logo_w // 2 + pill_pad, logo_y + logo_h + 4)
            ]
            draw.rounded_rectangle(pill_box, radius=18, fill=(255, 255, 255, 255), outline=COLOR_GOLD, width=2)
            im.paste(logo_res, (WIDTH // 2 - logo_w // 2, logo_y), logo_res)
            curr_y = logo_y + logo_h + 18
        except Exception:
            curr_y = logo_y + 35
    else:
        curr_y = logo_y + 35

    font_sub_inst = get_font("segoeuib.ttf", 19)
    inst_txt = "CENTRAL BANK OF KENYA  •  SPORTS & WELLNESS"
    bbox = draw.textbbox((0, 0), inst_txt, font=font_sub_inst)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, curr_y), inst_txt, font=font_sub_inst, fill=COLOR_GOLD)
    curr_y += 38

    # Hero Card
    hero_w = WIDTH - 120
    hero_h = 210
    hero_top = curr_y
    draw.rounded_rectangle([(60, hero_top), (WIDTH - 60, hero_top + hero_h)], radius=22, fill=COLOR_NAVY_CARD, outline=COLOR_GOLD, width=3)
    draw.rounded_rectangle([(68, hero_top + 6), (WIDTH - 68, hero_top + 16)], radius=5, fill=COLOR_ROYAL_BLUE)

    font_hero = get_font("ariblk.ttf", 74)
    hero_txt = "CBK STRIDE™"
    bbox = draw.textbbox((0, 0), hero_txt, font=font_hero)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, hero_top + 26), hero_txt, font=font_hero, fill=COLOR_GOLD)

    font_acronym = get_font("segoeuib.ttf", 20)
    acronym_full = "SPORTS TELEMETRY, ROSTER INTEGRITY & DIGITAL ENROLLMENT"
    bbox = draw.textbbox((0, 0), acronym_full, font=font_acronym)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, hero_top + 115), acronym_full, font=font_acronym, fill=COLOR_WHITE)

    font_hero_tag = get_font("segoeuib.ttf", 22)
    tag_hero = ">> THE SMART DIGITAL STADIUM IN YOUR POCKET <<"
    bbox = draw.textbbox((0, 0), tag_hero, font=font_hero_tag)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, hero_top + 155), tag_hero, font=font_hero_tag, fill=COLOR_AMBER)

    curr_y = hero_top + hero_h + 30

    # 4 Highlights in a 2x2 Grid (compact)
    grid_w = (WIDTH - 120 - 20) // 2
    grid_h = 165
    font_b = get_font("segoeuib.ttf", 16)
    font_t = get_font("segoeuib.ttf", 22)
    font_d = get_font("segoeui.ttf", 17)

    cards = [
        ("ZERO PAPERWORK", "2-Sec Pitch Check-In", "Dynamic QR pass scanned at pitch-side instantly. Zero queues.", COLOR_GOLD),
        ("18 DISCIPLINES", "All Sports Unified", "Golf, Athletics, Football, Netball, Volleyball, Tug of War & more.", COLOR_ICE_BLUE),
        ("REAL-TIME SYNC", "Live Google Sheets", "Attendance rosters & tournament stats stream live to HR.", COLOR_EMERALD),
        ("SOVEREIGN DATA", "100% CBK Network", "KDPA 2019 compliant. Encrypted & ring-fenced to Central Bank.", COLOR_GOLD)
    ]

    for idx, (badge, title, desc, acc) in enumerate(cards):
        col = idx % 2
        row = idx // 2
        x0 = 60 + col * (grid_w + 20)
        y0 = curr_y + row * (grid_h + 16)
        x1 = x0 + grid_w
        y1 = y0 + grid_h

        draw.rounded_rectangle([(x0, y0), (x1, y1)], radius=16, fill=COLOR_NAVY_CARD, outline=COLOR_BORDER_SUBTLE, width=2)
        draw.rounded_rectangle([(x0 + 14, y0 + 14), (x0 + 175, y0 + 38)], radius=6, fill=COLOR_ROYAL_BLUE)
        draw.text((x0 + 22, y0 + 16), badge, font=font_b, fill=acc)
        draw.text((x0 + 14, y0 + 48), title, font=font_t, fill=COLOR_WHITE)
        
        lines = wrap_text(draw, desc, font_d, grid_w - 28)
        dy = y0 + 85
        for l in lines:
            draw.text((x0 + 14, dy), l, font=font_d, fill=COLOR_TEXT_MUTED)
            dy += 24

    curr_y += (grid_h * 2) + 26

    # QR Code Card
    qr_card_h = 290
    draw.rounded_rectangle([(60, curr_y), (WIDTH - 60, curr_y + qr_card_h)], radius=20, fill=COLOR_NAVY_CARD, outline=COLOR_GOLD, width=3)

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=6, border=2)
    qr.add_data(PORTAL_URL)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#081428", back_color="#FFFFFF").convert("RGBA")
    qr_size = 190
    qr_res = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)

    qx = 90
    qy = curr_y + 35
    draw.rounded_rectangle([(qx - 8, qy - 8), (qx + qr_size + 8, qy + qr_size + 8)], radius=14, fill=COLOR_WHITE, outline=COLOR_GOLD, width=2)
    im.paste(qr_res, (qx, qy), qr_res)

    font_ql = get_font("segoeuib.ttf", 14)
    draw.text((qx + 18, qy + qr_size + 14), "SCAN TO OPEN PORTAL", font=font_ql, fill=COLOR_GOLD)

    rx = qx + qr_size + 40
    ry = curr_y + 30
    font_rh = get_font("ariblk.ttf", 30)
    draw.text((rx, ry), "Try It Live Right Now", font=font_rh, fill=COLOR_WHITE)
    ry += 45

    bullet_font = get_font("segoeui.ttf", 17)
    draw.text((rx, ry), "• Instant Gate 1 athlete check-in simulation", font=bullet_font, fill=COLOR_ICE_BLUE)
    ry += 28
    draw.text((rx, ry), "• Live Golf & Athletics roster tracking", font=bullet_font, fill=COLOR_ICE_BLUE)
    ry += 28
    draw.text((rx, ry), "• Automatic Google Sheets synchronization", font=bullet_font, fill=COLOR_ICE_BLUE)
    ry += 28
    draw.text((rx, ry), "• No app download required (Runs on any phone)", font=bullet_font, fill=COLOR_ICE_BLUE)
    ry += 32

    draw.rounded_rectangle([(rx, ry), (rx + 380, ry + 38)], radius=8, fill=COLOR_ROYAL_BLUE, outline=COLOR_GOLD, width=1)
    font_link = get_font("segoeuib.ttf", 15)
    draw.text((rx + 15, ry + 9), "variations-ribbon-cached-expires...", font=font_link, fill=COLOR_WHITE)

    curr_y += qr_card_h + 24

    # 3-Step Process Flow in Compact Flyer
    flow_h = 88
    draw.rounded_rectangle([(60, curr_y), (WIDTH - 60, curr_y + flow_h)], radius=16, fill=COLOR_NAVY_CARD, outline=COLOR_ROYAL_BLUE, width=2)
    step_w = (WIDTH - 120) // 3
    steps = [
        ("1", "SHOW PASS", "Flash dynamic QR"),
        ("2", "CAPTAIN SCANS", "Instant 2-sec check"),
        ("3", "AUTO SYNCED", "Live on Google Sheet")
    ]
    font_s_num = get_font("ariblk.ttf", 20)
    font_s_t = get_font("segoeuib.ttf", 17)
    font_s_d = get_font("segoeui.ttf", 14)
    for idx, (num, stitle, ssub) in enumerate(steps):
        sx = 60 + idx * step_w
        draw.ellipse([(sx + 16, curr_y + 18), (sx + 62, curr_y + 64)], fill=COLOR_ROYAL_BLUE, outline=COLOR_GOLD, width=2)
        draw.text((sx + 32, curr_y + 26), num, font=font_s_num, fill=COLOR_GOLD)
        draw.text((sx + 74, curr_y + 22), stitle, font=font_s_t, fill=COLOR_WHITE)
        draw.text((sx + 74, curr_y + 46), ssub, font=font_s_d, fill=COLOR_TEXT_MUTED)

    curr_y += flow_h + 22

    # Sports Strip
    sports_txt = "OFFICIAL DISCIPLINES:  GOLF  •  ATHLETICS  •  FOOTBALL  •  NETBALL  •  VOLLEYBALL  •  DARTS"
    font_sp = get_font("segoeuib.ttf", 15)
    bbox = draw.textbbox((0, 0), sports_txt, font=font_sp)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, curr_y), sports_txt, font=font_sp, fill=COLOR_ICE_BLUE)

    # Footer
    font_footer = get_font("segoeuib.ttf", 15)
    ftxt = "CENTRAL BANK OF KENYA  •  OFFICIAL SPORTS SECRETARIAT  •  SEPTEMBER 2026"
    bbox = draw.textbbox((0, 0), ftxt, font=font_footer)
    draw.text(((WIDTH - (bbox[2] - bbox[0])) // 2, HEIGHT - 38), ftxt, font=font_footer, fill=COLOR_GOLD)

    out_png = os.path.join(OUTPUT_DIR, "CBK_STRIDE_WhatsApp_Post_4x5.png")
    out_jpg = os.path.join(OUTPUT_DIR, "CBK_STRIDE_WhatsApp_Post_4x5.jpg")
    rgb_im = im.convert("RGB")
    rgb_im.save(out_png, "PNG", optimize=True)
    rgb_im.save(out_jpg, "JPEG", quality=88, optimize=True)
    print(f"✅ Generated 4:5 WhatsApp Feed Flyer: {out_jpg} ({os.path.getsize(out_jpg)/1024:.1f} KB)")


if __name__ == "__main__":
    build_fullscreen_flyer()
    build_compact_flyer()

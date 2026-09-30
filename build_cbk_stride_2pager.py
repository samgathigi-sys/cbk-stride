import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode
from pptx import Presentation
from pptx.util import Inches
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DIR = os.path.dirname(os.path.abspath(__file__))
PAGE1_INPUT = r"C:/Users/gathigisn.CBK.008/.gemini/antigravity/brain/00940864-5fa3-44bf-b1d9-02e121e7a052/.user_uploaded/media_1790766692303.jpg"
LOGO_PATH = os.path.join(DIR, "cbk_logo_transparent.png")

url_file = os.path.join(DIR, "CURRENT_LIVE_URL.txt")
PORTAL_URL = "https://amend-jacket-drugs-bacterial.trycloudflare.com"
if os.path.exists(url_file):
    try:
        with open(url_file, "r", encoding="utf-8") as f:
            v = f.read().strip()
            if v and v.startswith("http"):
                PORTAL_URL = v
    except Exception:
        pass

WIDTH = 1080
HEIGHT = 1920

# Palette matching Page 1
C_NAVY_BG = (4, 15, 32)           # #040F20 Deep Midnight Sapphire Navy
C_CARD_BG = (9, 24, 48)           # #091830 Glassmorphic Sapphire Card
C_CARD_BORDER = (245, 197, 66)     # #F5C542 Championship Gold
C_CARD_BORDER_SUBTLE = (38, 72, 118) # Deep Slate Blue
C_GOLD = (245, 197, 66)           # #F5C542 Gold
C_GOLD_LIGHT = (255, 235, 143)    # Light Gold
C_CYAN = (0, 242, 254)            # #00F2FE Neon Telemetry Cyan
C_WHITE = (255, 255, 255)
C_SLATE = (148, 163, 184)         # Slate Gray
C_ICE = (226, 232, 240)           # High-legibility Ice White
C_EMERALD = (52, 211, 153)        # #34D399 Mint Green
C_AMBER = (251, 146, 60)          # #FB923C Amber Orange
C_PURPLE = (192, 132, 252)        # #C084FC Lavender

WIN_FONTS = "C:\\Windows\\Fonts"
def get_font(name, size):
    path = os.path.join(WIN_FONTS, name)
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()

# Fonts (Strictly ASCII-safe to prevent rectangle glyphs)
font_title = get_font("segoeuib.ttf", 44)
font_subtitle = get_font("segoeui.ttf", 22)
font_card_num = get_font("segoeuib.ttf", 16)
font_card_tag = get_font("segoeuib.ttf", 14)
font_card_h = get_font("segoeuib.ttf", 22)
font_card_body = get_font("segoeui.ttf", 17)
font_card_bullet = get_font("segoeuib.ttf", 17)
font_bottom_h = get_font("segoeuib.ttf", 22)
font_bottom_sub = get_font("segoeui.ttf", 16)
font_badge = get_font("segoeuib.ttf", 13)

# ------------------------------------------------------------------------------
# 1. PROCESS PAGE 1
# ------------------------------------------------------------------------------
print("Processing Page 1...")
page1_raw = Image.open(PAGE1_INPUT)
page1 = page1_raw.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
page1_path_png = os.path.join(DIR, "CBK_STRIDE_Flyer_Page1.png")
page1_path_jpg = os.path.join(DIR, "CBK_STRIDE_Flyer_Page1.jpg")
page1.save(page1_path_png, "PNG")
page1.convert("RGB").save(page1_path_jpg, "JPEG", quality=95)

# ------------------------------------------------------------------------------
# 2. BUILD PAGE 2
# ------------------------------------------------------------------------------
print("Building Page 2...")
page2 = Image.new("RGBA", (WIDTH, HEIGHT), C_NAVY_BG)
draw = ImageDraw.Draw(page2)

# Gradient background (deep sapphire glow at top, warm gold glow at base)
for y in range(450):
    intensity = 1.0 - (y / 450.0)
    alpha = int(32 * intensity)
    draw.line([(0, y), (WIDTH, y)], fill=(2, 91, 191, alpha))

for y in range(HEIGHT - 450, HEIGHT):
    intensity = (y - (HEIGHT - 450)) / 450.0
    alpha = int(28 * intensity)
    draw.line([(0, y), (WIDTH, y)], fill=(245, 197, 66, alpha))

# Framing Stripes
draw.rectangle([(0, 0), (WIDTH, 14)], fill=C_GOLD)
draw.rectangle([(0, HEIGHT - 14), (WIDTH, HEIGHT)], fill=C_GOLD)

# Top Bar Header
header_y = 38
if os.path.exists(LOGO_PATH):
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo_w = 95
        ratio = logo_w / float(logo.width)
        logo_h = int(float(logo.height) * ratio)
        logo_res = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
        page2.paste(logo_res, (50, header_y), logo_res)
    except Exception as e:
        print("Logo error:", e)

# Header Title Block
draw.text((165, header_y + 2), "CENTRAL BANK OF KENYA", fill=C_GOLD, font=get_font("segoeuib.ttf", 22))
draw.text((165, header_y + 32), "SPORTS TELEMETRY & ROSTER INTEGRITY (CBK STRIDE™)", fill=C_SLATE, font=get_font("segoeuib.ttf", 14))

# Page Title
title_y = header_y + 80
draw.text((50, title_y), "SYSTEM ARCHITECTURE & FEATURES", fill=C_GOLD, font=font_title)
draw.text((50, title_y + 56), "A Frictionless, Dual-Gate Trust Engine Engineered for Central Bank Governance", fill=C_WHITE, font=font_subtitle)

# Gold divider line
draw.line([(50, title_y + 98), (WIDTH - 50, title_y + 98)], fill=(245, 197, 66, 140), width=2)

# ------------------------------------------------------------------------------
# 6 FEATURE CARDS (2 Columns x 3 Rows)
# ------------------------------------------------------------------------------
cards_data = [
    {
        "num": "01",
        "tag": "FRICTIONLESS BYOD",
        "tag_bg": (0, 35, 65),
        "tag_border": C_CYAN,
        "tag_fg": C_CYAN,
        "title": "Zero-App Native Web Access",
        "points": [
            "No App Store or Google Play install needed.",
            "Native smartphone camera scans station QR.",
            "Instant browser launch in < 3 seconds.",
            "Works seamlessly on all iOS & Android devices.",
            "Zero personal phone storage or memory used."
        ]
    },
    {
        "num": "02",
        "tag": "AUDIT-CERTIFIED",
        "tag_bg": (45, 35, 10),
        "tag_border": C_GOLD,
        "tag_fg": C_GOLD,
        "title": "Dual-Gate Time Verification",
        "points": [
            "Mandatory Gate 1 (In) & Gate 2 (Out) stamps.",
            "Automated >= 45 min physical activity floor.",
            "Auto-flags short sessions & early departures.",
            "Eliminates ghost check-ins and proxy claims.",
            "Certifies non-repudiable attendance units."
        ]
    },
    {
        "num": "03",
        "tag": "MASTER REGISTRY",
        "tag_bg": (10, 40, 28),
        "tag_border": C_EMERALD,
        "tag_fg": C_EMERALD,
        "title": "4-Digit Instant Staff ID Lookup",
        "points": [
            "Pre-loaded with 679 CBK athletes (18 sports).",
            "Type 4-digit payroll ID (e.g. 3428) + tap Find.",
            "Auto-detects sport, captain, and home venue.",
            "Generates dynamic cryptographic athlete pass.",
            "Zero manual forms or tedious typing on field."
        ]
    },
    {
        "num": "04",
        "tag": "KENYA DPA 2019",
        "tag_bg": (45, 25, 10),
        "tag_border": C_AMBER,
        "tag_fg": C_AMBER,
        "title": "Banking-Grade Data Privacy",
        "points": [
            "Option B asterisk masking on pitch monitors.",
            "Public views display: Sam*** Gat*** Nju***.",
            "Cloaks staff emails, phones & payroll numbers.",
            "Zero-trust RBAC with passkey authorization.",
            "Full details restricted to Secretariat & Audit."
        ]
    },
    {
        "num": "05",
        "tag": "ZERO DATA LOSS",
        "tag_bg": (35, 18, 55),
        "tag_border": C_PURPLE,
        "tag_fg": C_PURPLE,
        "title": "Offline Resilience & Hotspot",
        "points": [
            "Captain tablet broadcasts CBK-DSWAAP-HOTSPOT.",
            "Athletes use zero personal cellular airtime.",
            "Local SQLite buffer caches scans in dead zones.",
            "Tamper-proof HMAC verification offline.",
            "1-click cloud sync to Google Sheets Master."
        ]
    },
    {
        "num": "06",
        "tag": "FINANCE & HR",
        "tag_bg": (10, 40, 28),
        "tag_border": C_EMERALD,
        "tag_fg": C_EMERALD,
        "title": "Automated Ledgers & Receipts",
        "points": [
            "Instant HTML receipts sent to @centralbank.go.ke.",
            "Live roll-call monitor for on-pitch captains.",
            "1-click certified CSV & Excel workbook exports.",
            "Real-time KPI analytics for HR & Secretariat.",
            "Immutable audit trail logging every export."
        ]
    }
]

col_w = 475
col_gap = 30
start_x = 50
start_y = title_y + 115
card_h = 350
row_gap = 25

for idx, c in enumerate(cards_data):
    col_idx = idx % 2
    row_idx = idx // 2
    
    cx = start_x + col_idx * (col_w + col_gap)
    cy = start_y + row_idx * (card_h + row_gap)
    
    # Draw card background
    draw.rounded_rectangle([(cx, cy), (cx + col_w, cy + card_h)], radius=18, fill=C_CARD_BG, outline=C_CARD_BORDER_SUBTLE, width=2)
    
    # Top card border accent line in category color
    draw.line([(cx + 25, cy + 2), (cx + col_w - 25, cy + 2)], fill=c["tag_border"], width=3)
    
    # Number badge & Tag Pill
    # Number badge
    draw.text((cx + 20, cy + 18), f"[{c['num']}]", fill=C_GOLD, font=font_card_num)
    
    # Tag Pill
    tag_text = c["tag"]
    tbox = draw.textbbox((0, 0), tag_text, font=font_badge)
    tw = tbox[2] - tbox[0] + 16
    th = tbox[3] - tbox[1] + 8
    draw.rounded_rectangle([(cx + 62, cy + 16), (cx + 62 + tw, cy + 16 + th)], radius=6, fill=c["tag_bg"], outline=c["tag_border"], width=1)
    draw.text((cx + 70, cy + 20), tag_text, fill=c["tag_fg"], font=font_badge)
    
    # Card Title
    draw.text((cx + 20, cy + 54), c["title"], fill=C_WHITE, font=font_card_h)
    
    # Divider inside card
    draw.line([(cx + 20, cy + 92), (cx + col_w - 20, cy + 92)], fill=(30, 58, 95), width=1)
    
    # Bullet points
    by = cy + 106
    for p in c["points"]:
        draw.text((cx + 22, by), ">", fill=c["tag_border"], font=font_card_bullet)
        draw.text((cx + 38, by), p, fill=C_ICE, font=font_card_body)
        by += 45

# ------------------------------------------------------------------------------
# BOTTOM ENTERPRISE SHOWCASE CONTAINER (WIDTH - 100 x 320 px)
# ------------------------------------------------------------------------------
bot_y = start_y + 3 * (card_h + row_gap) + 10
bot_h = 320
bot_x = 50
bot_w = WIDTH - 100

draw.rounded_rectangle([(bot_x, bot_y), (bot_x + bot_w, bot_y + bot_h)], radius=20, fill=(7, 24, 48), outline=C_GOLD, width=3)

# Inside bottom showcase:
left_w = bot_w - 290

draw.text((bot_x + 28, bot_y + 22), "CENTRAL BANK DATA SOVEREIGNTY & AUDIT GOVERNANCE", fill=C_GOLD, font=font_bottom_h)

summary_p1 = "From pitch-side athletics to executive committee governance, CBK STRIDE™"
summary_p2 = "replaces paper bureaucracy with an audit-certified, tamper-proof trust engine."
summary_p3 = "Strictly compliant with Kenya DPA 2019, CBK Infosec & Internal Audit standards."

draw.text((bot_x + 28, bot_y + 64), summary_p1, fill=C_WHITE, font=font_bottom_sub)
draw.text((bot_x + 28, bot_y + 92), summary_p2, fill=C_WHITE, font=font_bottom_sub)
draw.text((bot_x + 28, bot_y + 120), summary_p3, fill=C_SLATE, font=font_bottom_sub)

# Live Portal Callout Box
callout_y = bot_y + 162
draw.rounded_rectangle([(bot_x + 25, callout_y), (bot_x + left_w - 15, callout_y + 126)], radius=12, fill=(4, 14, 28), outline=(0, 242, 254, 150), width=1)

draw.text((bot_x + 38, callout_y + 12), "TEST THE LIVE PRODUCTION CLOUD PORTAL:", fill=C_CYAN, font=get_font("segoeuib.ttf", 15))
draw.text((bot_x + 38, callout_y + 38), PORTAL_URL, fill=C_WHITE, font=get_font("segoeui.ttf", 13))

draw.text((bot_x + 38, callout_y + 68), "PRE-CONFIGURED AUDIT ACCESS CLEARANCE:", fill=C_GOLD, font=get_font("segoeuib.ttf", 15))
draw.text((bot_x + 38, callout_y + 94), "Staff ID: 3428  |  Passkey: 3428 (Super Admin Full Clearance)", fill=C_ICE, font=get_font("segoeui.ttf", 14))

# Generate Live Portal QR Code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_M,
    box_size=7,
    border=2,
)
qr.add_data(PORTAL_URL)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="#040D1A", back_color="#FFFFFF").convert("RGBA")

# Frame the QR Code on the right with Championship Gold Glow
qr_box_size = 230
qr_res = qr_img.resize((qr_box_size, qr_box_size), Image.Resampling.LANCZOS)
qr_x = bot_x + bot_w - qr_box_size - 30
qr_y = bot_y + 34

# Gold outer glow box
draw.rounded_rectangle([(qr_x - 12, qr_y - 12), (qr_x + qr_box_size + 12, qr_y + qr_box_size + 12)], radius=18, fill=(12, 32, 60), outline=C_GOLD, width=3)
page2.paste(qr_res, (qr_x, qr_y), qr_res)

draw.text((qr_x - 6, qr_y + qr_box_size + 18), "POINT PHONE CAMERA TO TEST", fill=C_GOLD, font=get_font("segoeuib.ttf", 13))

# Save Page 2
page2_path_png = os.path.join(DIR, "CBK_STRIDE_Flyer_Page2.png")
page2_path_jpg = os.path.join(DIR, "CBK_STRIDE_Flyer_Page2.jpg")
page2.save(page2_path_png, "PNG")
page2.convert("RGB").save(page2_path_jpg, "JPEG", quality=95)

# ------------------------------------------------------------------------------
# 3. BUILD 2-PAGE SPREAD (2160 x 1920)
# ------------------------------------------------------------------------------
print("Creating side-by-side spread...")
spread = Image.new("RGB", (WIDTH * 2 + 30, HEIGHT), (4, 15, 32))
spread.paste(page1.convert("RGB"), (0, 0))
# Gold vertical divider
draw_spread = ImageDraw.Draw(spread)
draw_spread.rectangle([(WIDTH, 0), (WIDTH + 30, HEIGHT)], fill=C_GOLD)
spread.paste(page2.convert("RGB"), (WIDTH + 30, 0))
spread_path = os.path.join(DIR, "CBK_STRIDE_Flyer_2Page_Spread.jpg")
spread.save(spread_path, "JPEG", quality=95)

# ------------------------------------------------------------------------------
# 4. BUILD MULTI-PAGE EXECUTIVE PDF
# ------------------------------------------------------------------------------
print("Building 2-page PDF...")
pdf_path = os.path.join(DIR, "CBK_STRIDE_Executive_2Pager_Flyer.pdf")
im_list = [page2.convert("RGB")]
page1.convert("RGB").save(pdf_path, "PDF", resolution=150.0, save_all=True, append_images=im_list)

# ------------------------------------------------------------------------------
# 5. BUILD POWERPOINT PRESENTATION (.PPTX)
# ------------------------------------------------------------------------------
print("Building 2-page PPTX presentation...")
pptx_path = os.path.join(DIR, "CBK_STRIDE_Executive_2Pager_Flyer.pptx")
prs = Presentation()
prs.slide_width = Inches(7.5)
prs.slide_height = Inches(13.33)
blank_layout = prs.slide_layouts[6]

# Slide 1: Page 1
slide1 = prs.slides.add_slide(blank_layout)
slide1.shapes.add_picture(page1_path_jpg, Inches(0), Inches(0), Inches(7.5), Inches(13.33))

# Slide 2: Page 2
slide2 = prs.slides.add_slide(blank_layout)
slide2.shapes.add_picture(page2_path_jpg, Inches(0), Inches(0), Inches(7.5), Inches(13.33))

prs.save(pptx_path)

print("All outputs successfully generated!")

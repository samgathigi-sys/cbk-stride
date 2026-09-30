"""
Generates high-resolution UI snippet mockup images for the CBK DSWAAP presentation deck.
Features Athletics & Track as the primary discipline and includes the Secretariat Operational Dashboard.
Strictly adheres to the Central Bank of Kenya (CBK) official corporate branding:
- CBK Royal Blue: #025BBF (Primary Brand Color from centralbank.go.ke)
- CBK Deep Navy:  #10529E (Secondary Brand Color from centralbank.go.ke)
- CBK Saffron Gold: #F8B82D (Official Brand Color from CBK Logo & centralbank.go.ke)
- CBK Amber Gold Accent: #F7941D (Website Hero Banner Accent)
- CBK Ice Blue Tint: #EEF6FC (Card Backgrounds)
- Official CBK Coat of Arms Crest Logo embedded on every terminal and dashboard.
"""

import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(OUTPUT_DIR, "cbk_logo.png")
LOGO_TRANSPARENT_PATH = os.path.join(OUTPUT_DIR, "cbk_logo_transparent.png")

# Fonts
try:
    font_bold_xl = ImageFont.truetype("segoeuib.ttf", 32)
    font_bold_lg = ImageFont.truetype("segoeuib.ttf", 26)
    font_bold_md = ImageFont.truetype("segoeuib.ttf", 20)
    font_bold_sm = ImageFont.truetype("segoeuib.ttf", 15)
    font_bold_xs = ImageFont.truetype("segoeuib.ttf", 12)
    font_reg_lg = ImageFont.truetype("segoeui.ttf", 22)
    font_reg_md = ImageFont.truetype("segoeui.ttf", 16)
    font_reg_sm = ImageFont.truetype("segoeui.ttf", 14)
    font_reg_xs = ImageFont.truetype("segoeui.ttf", 11)
except Exception:
    font_bold_xl = ImageFont.load_default()
    font_bold_lg = font_bold_xl
    font_bold_md = font_bold_xl
    font_bold_sm = font_bold_xl
    font_bold_xs = font_bold_xl
    font_reg_lg = font_bold_xl
    font_reg_md = font_bold_xl
    font_reg_sm = font_bold_xl
    font_reg_xs = font_bold_xl

# CBK Corporate Palette (Directly sampled from centralbank.go.ke and official assets)
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
CBK_CARD = "#FFFFFF"
CBK_BORDER = "#CBD5E1"
CBK_SUCCESS = "#059669"
CBK_DANGER = "#DC2626"


def get_cbk_logo_badge(target_h=60):
    """Returns a resized CBK logo on a crisp white container badge."""
    try:
        raw_logo = Image.open(LOGO_PATH)
        w, h = raw_logo.size
        target_w = int(w * (target_h / h))
        return raw_logo.resize((target_w, target_h), Image.Resampling.LANCZOS)
    except Exception:
        return None


# ==============================================================================
# 1. MOBILE CHECK-IN SNIPPET (ATHLETICS & TRACK)
# ==============================================================================
def create_mobile_checkin_snippet():
    w, h = 640, 1020
    img = Image.new("RGB", (w, h), "#E2E8F0")
    draw = ImageDraw.Draw(img)

    # Smartphone outer body
    draw.rounded_rectangle([15, 15, w-15, h-15], radius=32, fill="#0F172A", outline="#334155", width=4)
    # Screen inner
    draw.rounded_rectangle([25, 25, w-25, h-25], radius=24, fill=CBK_BG)

    # Status Bar
    draw.text((45, 34), "06:45", fill="#0F172A", font=font_bold_xs)
    draw.text((w-110, 34), "5G  92%", fill="#0F172A", font=font_bold_xs)

    # CBK Header Top Bar
    draw.rounded_rectangle([35, 55, w-35, 155], radius=14, fill=CBK_DEEP_NAVY)
    draw.rectangle([35, 151, w-35, 155], fill=CBK_GOLD)

    # Logo badge on mobile header
    logo = get_cbk_logo_badge(target_h=50)
    if logo:
        draw.rounded_rectangle([45, 68, 45+logo.width+12, 68+logo.height+4], radius=6, fill=CBK_WHITE)
        img.paste(logo, (51, 70))
        text_x = 45 + logo.width + 22
    else:
        text_x = 45

    draw.rounded_rectangle([text_x, 68, text_x+195, 86], radius=4, fill=CBK_GOLD)
    draw.text((text_x+6, 70), "CENTRAL BANK OF KENYA", fill=CBK_DEEP_NAVY, font=font_bold_xs)
    draw.text((text_x, 92), "DSWAAP Mobile Check-In", fill="#FFFFFF", font=font_bold_md)
    draw.text((text_x, 120), "Dual-Gate QR Tracking • Athletics & Track", fill=CBK_ICE_BLUE, font=font_reg_xs)

    # Gate Toggle
    y = 170
    draw.rounded_rectangle([35, y, (w//2)-5, y+50], radius=10, fill=CBK_ROYAL_BLUE, outline=CBK_DEEP_NAVY, width=2)
    draw.text((50, y+10), "Gate 1: Pre-Sport", fill="#FFFFFF", font=font_bold_sm)
    draw.text((50, y+28), "Arrival Gate (Active)", fill=CBK_GOLD, font=font_reg_xs)

    draw.rounded_rectangle([(w//2)+5, y, w-35, y+50], radius=10, fill="#FFFFFF", outline=CBK_BORDER, width=1)
    draw.text(((w//2)+20, y+10), "Gate 2: Post-Sport", fill=CBK_TEXT_MUTED, font=font_bold_sm)
    draw.text(((w//2)+20, y+28), "Departure Check-Out", fill="#94A3B8", font=font_reg_xs)

    # Staff Info Card
    y = 235
    draw.rounded_rectangle([35, y, w-35, y+255], radius=14, fill=CBK_CARD, outline=CBK_BORDER_BLUE, width=2)
    draw.text((50, y+15), "STAFF ATHLETE IDENTIFICATION", fill=CBK_ROYAL_BLUE, font=font_bold_xs)

    # Staff ID Field
    draw.rounded_rectangle([50, y+40, (w//2)-10, y+85], radius=8, fill="#F1F5F9", outline=CBK_BORDER)
    draw.text((60, y+45), "Staff ID", fill=CBK_TEXT_MUTED, font=font_reg_xs)
    draw.text((60, y+60), "CBK-1024", fill=CBK_TEXT_DARK, font=font_bold_sm)

    # Full Name Field
    draw.rounded_rectangle([(w//2)+5, y+40, w-50, y+85], radius=8, fill="#F1F5F9", outline=CBK_BORDER)
    draw.text(((w//2)+15, y+45), "Full Name", fill=CBK_TEXT_MUTED, font=font_reg_xs)
    draw.text(((w//2)+15, y+60), "Brian Kimani", fill=CBK_TEXT_DARK, font=font_bold_sm)

    # Directorate & Email Field
    draw.rounded_rectangle([50, y+95, w-50, y+145], radius=8, fill="#F1F5F9", outline=CBK_BORDER)
    draw.text((60, y+99), "Directorate & Institutional Email (@centralbank.go.ke)", fill=CBK_TEXT_MUTED, font=font_reg_xs)
    draw.text((60, y+116), "Monetary Policy & Research • bkimani@centralbank.go.ke", fill=CBK_ROYAL_BLUE, font=font_bold_xs)

    # Discipline & Station (ATHLETICS)
    draw.rounded_rectangle([50, y+150, (w//2)-10, y+240], radius=8, fill="#F1F5F9", outline=CBK_BORDER)
    draw.text((60, y+155), "Sporting Discipline", fill=CBK_TEXT_MUTED, font=font_reg_xs)
    draw.text((60, y+175), "🏃 Athletics & Track", fill=CBK_ROYAL_BLUE, font=font_bold_sm)
    draw.text((60, y+205), "Capt. Geoffrey Kemboi", fill="#64748B", font=font_reg_xs)

    draw.rounded_rectangle([(w//2)+5, y+150, w-50, y+240], radius=8, fill="#F1F5F9", outline=CBK_BORDER)
    draw.text(((w//2)+15, y+155), "Circuit Station / Post", fill=CBK_TEXT_MUTED, font=font_reg_xs)
    draw.text(((w//2)+15, y+175), "Track 100m Start", fill=CBK_TEXT_DARK, font=font_bold_sm)
    draw.text(((w//2)+15, y+205), "Perimeter Loop Checkpoint", fill="#64748B", font=font_reg_xs)

    # QR Scanner / Verification Section
    y = 510
    draw.rounded_rectangle([35, y, w-35, y+265], radius=14, fill=CBK_CARD, outline=CBK_BORDER_BLUE, width=2)
    draw.text((50, y+15), "DYNAMIC QR SCAN SENSOR", fill=CBK_ROYAL_BLUE, font=font_bold_xs)

    # Draw QR code in center
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data("CBK_DSWAAP|ATH|PRE_SPORT|TRACK100M|20260930")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=CBK_ROYAL_BLUE, back_color="#FFFFFF").convert("RGB")
    qr_w, qr_h = qr_img.size
    qr_x = (w - qr_w) // 2
    img.paste(qr_img, (qr_x, y+45))

    # Scanner viewfinder borders
    v_pad = 12
    draw.arc([qr_x - v_pad, y+45 - v_pad, qr_x + qr_w + v_pad, y+45 + qr_h + v_pad], 0, 360, fill=CBK_GOLD, width=2)
    draw.text(((w//2)-110, y+235), "Dynamic Code Auto-Refreshes: 14:15", fill=CBK_TEXT_MUTED, font=font_bold_xs)

    # Big Submit Button (CBK Royal Blue)
    y = 795
    draw.rounded_rectangle([35, y, w-35, y+60], radius=12, fill=CBK_ROYAL_BLUE, outline=CBK_DEEP_NAVY, width=2)
    draw.text(((w//2)-130, y+18), "🚀 SUBMIT GATE CHECK-IN", fill="#FFFFFF", font=font_bold_md)

    # Bottom Live Attendance Pass Card
    y = 870
    draw.rounded_rectangle([35, y, w-35, y+115], radius=12, fill=CBK_ICE_BLUE, outline=CBK_BORDER_BLUE, width=2)
    draw.rounded_rectangle([50, y+12, 240, y+34], radius=10, fill=CBK_ROYAL_BLUE)
    draw.text((62, y+16), "PRE-SPORT VALIDATED", fill="#FFFFFF", font=font_bold_xs)
    draw.text((50, y+45), "Brian Kimani (CBK-1024) • Athletics & Track", fill=CBK_TEXT_DARK, font=font_bold_sm)
    draw.text((50, y+70), "Arrival Timestamp: 06:45:10 | Awaiting Gate 2 Post-Sport", fill=CBK_TEXT_MUTED, font=font_reg_xs)
    draw.text((50, y+90), "Policy Floor: 45+ mins activity required for attendance accreditation", fill=CBK_DEEP_NAVY, font=font_bold_xs)

    path = os.path.join(OUTPUT_DIR, "ui_snippet_mobile_checkin.png")
    img.save(path, quality=95)
    print(f"Mobile Check-in Snippet saved: {path}")


# ==============================================================================
# 2. FIELD CAPTAIN QR BROADCAST TERMINAL (ATHLETICS & TRACK)
# ==============================================================================
def create_captain_terminal_snippet():
    w, h = 760, 680
    img = Image.new("RGB", (w, h), CBK_BG)
    draw = ImageDraw.Draw(img)

    # Top Header
    draw.rounded_rectangle([20, 20, w-20, 95], radius=12, fill=CBK_DEEP_NAVY)
    draw.rectangle([20, 91, w-20, 95], fill=CBK_GOLD)

    # Logo
    logo = get_cbk_logo_badge(target_h=55)
    if logo:
        draw.rounded_rectangle([35, 28, 35+logo.width+12, 28+logo.height+4], radius=6, fill=CBK_WHITE)
        img.paste(logo, (41, 30))
        tx = 35 + logo.width + 22
    else:
        tx = 40

    draw.text((tx, 32), "CENTRAL BANK OF KENYA | ATHLETICS MARSHAL TERMINAL", fill=CBK_GOLD, font=font_bold_xs)
    draw.text((tx, 52), "Dynamic Station QR Code Broadcast • Track & Perimeter Circuit", fill="#FFFFFF", font=font_bold_md)

    # Left Card: Live QR Display
    qr_card_w = 420
    draw.rounded_rectangle([20, 110, 20+qr_card_w, h-20], radius=12, fill=CBK_CARD, outline=CBK_GOLD, width=2)
    draw.rounded_rectangle([40, 125, 230, 148], radius=6, fill=CBK_GOLD)
    draw.text((48, 130), "ATHLETICS • ARRIVAL GATE 1", fill=CBK_DEEP_NAVY, font=font_bold_xs)

    draw.text((40, 158), "Track 100m Start Point", fill=CBK_ROYAL_BLUE, font=font_bold_md)
    draw.text((40, 185), "Station ID: ATH-STN-01 | Capt. Geoffrey Kemboi", fill=CBK_TEXT_MUTED, font=font_reg_xs)

    # QR Code inside card
    qr = qrcode.QRCode(box_size=7, border=1)
    qr.add_data("CBK_DSWAAP_SECURE|ATH|PRE|TRACK100M|EXPIRES_15MIN")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color=CBK_ROYAL_BLUE, back_color="#FFFFFF").convert("RGB")
    qr_w, qr_h = qr_img.size
    qr_x = 20 + (qr_card_w - qr_w) // 2
    img.paste(qr_img, (qr_x, 220))

    # Hotspot status badge and Countdown/HMAC badge
    draw.rounded_rectangle([40, 535, 20+qr_card_w-20, 568], radius=8, fill="#FFFBEB", outline=CBK_GOLD_AMBER, width=2)
    draw.text((55, 544), "📶 Field Hotspot: 'CBK-DSWAAP-HOTSPOT' Active (Zero Athlete Bundles)", fill="#92400E", font=font_bold_xs)

    draw.rounded_rectangle([40, 575, 20+qr_card_w-20, 608], radius=8, fill=CBK_ICE_BLUE, outline=CBK_BORDER_BLUE)
    draw.text((55, 585), "⏱️ Dynamic QR expires in 13:20 • HMAC-SHA256 Signed", fill=CBK_DEEP_NAVY, font=font_bold_xs)

    draw.text((55, 620), "Scan with CBK Mobile Check-In to validate track arrival", fill=CBK_ROYAL_BLUE, font=font_bold_xs)

    # Right Card: Athletics Circuit Station Switcher
    rt_x = 460
    rt_w = 280
    draw.rounded_rectangle([rt_x, 110, rt_x+rt_w, h-20], radius=12, fill=CBK_CARD, outline=CBK_BORDER, width=1)
    draw.text((rt_x+20, 125), "🏃 ATHLETICS TOPOLOGY", fill=CBK_ROYAL_BLUE, font=font_bold_sm)
    draw.text((rt_x+20, 145), "Track & Perimeter Circuit Posts", fill=CBK_TEXT_MUTED, font=font_reg_xs)

    stations = [
        ("Track 100m Start Point", "Sprint & Track Arrival (Active)", True),
        ("Perimeter Gate 3", "Jogging Loop Exit Gate", False),
        ("Main Stadium Pavilion", "Grandstand Warmup Area", False),
        ("Cross-Country Trail", "Outer Perimeter Loop", False),
        ("Finish Line Marshals", "Session Departure Verification", False),
        ("Field Events Area", "Jumps & Throws Training", False)
    ]

    y_stn = 180
    for s_name, s_desc, is_act in stations:
        stn_bg = CBK_ICE_BLUE if is_act else "#F8F9FA"
        stn_bd = CBK_ROYAL_BLUE if is_act else CBK_BORDER
        draw.rounded_rectangle([rt_x+20, y_stn, rt_x+rt_w-20, y_stn+55], radius=8, fill=stn_bg, outline=stn_bd, width=2 if is_act else 1)
        draw.text((rt_x+30, y_stn+8), s_name, fill=CBK_ROYAL_BLUE if is_act else CBK_TEXT_DARK, font=font_bold_xs)
        draw.text((rt_x+30, y_stn+28), s_desc, fill=CBK_TEXT_MUTED, font=font_reg_xs)
        y_stn += 68

    path = os.path.join(OUTPUT_DIR, "ui_snippet_captain_terminal.png")
    img.save(path, quality=95)
    print(f"Captain Terminal Snippet saved: {path}")


# ==============================================================================
# 3. SECRETARIAT OPERATIONAL DASHBOARD SNIPPET
# ==============================================================================
def create_secretariat_dashboard_snippet():
    w, h = 980, 620
    img = Image.new("RGB", (w, h), CBK_BG)
    draw = ImageDraw.Draw(img)

    # Top Header
    draw.rounded_rectangle([20, 20, w-20, 95], radius=12, fill=CBK_DEEP_NAVY)
    draw.rectangle([20, 91, w-20, 95], fill=CBK_GOLD)

    # Logo
    logo = get_cbk_logo_badge(target_h=55)
    if logo:
        draw.rounded_rectangle([35, 28, 35+logo.width+12, 28+logo.height+4], radius=6, fill=CBK_WHITE)
        img.paste(logo, (41, 30))
        tx = 35 + logo.width + 22
    else:
        tx = 40

    draw.text((tx, 32), "CENTRAL BANK OF KENYA | SPORTS & WELLNESS SECRETARIAT", fill=CBK_GOLD, font=font_bold_xs)
    draw.text((tx, 52), "Real-Time 18-Discipline Turnout Matrix & Live Scans Activity Ticker", fill="#FFFFFF", font=font_bold_lg)

    # 4 Headline Metric KPI Cards
    kpi_w = 220
    kpis = [
        ("TODAY'S TOTAL SCANS", "168 Scans", "Across 18 Disciplines", CBK_ROYAL_BLUE),
        ("ACTIVE ON FIELD (GATE 1)", "44 Athletes", "Awaiting Post-Gate", CBK_GOLD_AMBER),
        ("DUAL-VERIFIED (COMPLETED)", "112 Sessions", "Reconciled & Compliant", CBK_DEEP_NAVY),
        ("POLICY COMPLIANCE RATE", "98.2%", "Sessions >= 45 Minutes", CBK_ROYAL_BLUE)
    ]
    for idx, (title, val, sub, col) in enumerate(kpis):
        k_x = 20 + (idx * (kpi_w + 13))
        draw.rounded_rectangle([k_x, 110, k_x+kpi_w, 195], radius=10, fill=CBK_CARD, outline=col, width=2)
        draw.text((k_x+12, 118), title, fill=CBK_TEXT_MUTED, font=font_bold_xs)
        draw.text((k_x+12, 136), val, fill=col, font=font_bold_md)
        draw.text((k_x+12, 170), sub, fill=CBK_TEXT_DARK, font=font_reg_xs)

    # Left Section: 18 Disciplines Status Grid (6 Featured Cards)
    grid_w = 540
    draw.rounded_rectangle([20, 210, 20+grid_w, h-20], radius=12, fill=CBK_CARD, outline=CBK_BORDER_BLUE, width=2)
    draw.text((35, 222), "18 SPORTING DISCIPLINES LIVE TURNOUT GRID", fill=CBK_ROYAL_BLUE, font=font_bold_sm)

    featured_disciplines = [
        ("🏃 Athletics & Track", "Capt. Geoffrey Kemboi (2405)", "16 Active", "28 Done", "Active Session", CBK_ROYAL_BLUE),
        ("⚽ Football (Soccer)", "Capt. David Ochieng (2401)", "12 Active", "22 Done", "Active Session", CBK_ROYAL_BLUE),
        ("🏀 Basketball", "Capt. Angela Mutua (2402)", "8 Active", "14 Done", "Active Session", CBK_ROYAL_BLUE),
        ("🏊 Swimming", "Capt. Kevin Kariuki (2410)", "4 Active", "10 Done", "Active Session", CBK_ROYAL_BLUE),
        ("🎾 Lawn Tennis", "Capt. Beatrice Nduta (2407)", "2 Active", "8 Done", "Active Session", CBK_ROYAL_BLUE),
        ("⛳ Golf", "Capt. Eric Mwangi (2406)", "2 Active", "16 Done", "Active Session", CBK_ROYAL_BLUE),
        ("🏐 Volleyball", "Capt. Kiprono Bett (2403)", "0 Active", "8 Done", "Concluded", CBK_TEXT_MUTED),
        ("♟️ Chess & Mind", "Capt. Peter Maina (2414)", "0 Active", "6 Done", "Standby", CBK_GOLD)
    ]

    y_grid = 250
    for idx, (d_name, d_capt, act, comp, stat, col_stat) in enumerate(featured_disciplines):
        col_offset = (idx % 2) * 260
        row_offset = (idx // 2) * 80
        cx = 35 + col_offset
        cy = y_grid + row_offset

        draw.rounded_rectangle([cx, cy, cx+250, cy+70], radius=8, fill="#F8F9FA", outline=CBK_BORDER)
        draw.text((cx+10, cy+8), d_name, fill=CBK_TEXT_DARK, font=font_bold_xs)
        draw.text((cx+10, cy+26), d_capt, fill=CBK_TEXT_MUTED, font=font_reg_xs)

        badge_bg = CBK_ICE_BLUE if stat == "Active Session" else ("#F1F5F9" if stat == "Concluded" else "#FEF3C7")
        draw.rounded_rectangle([cx+155, cy+8, cx+240, cy+26], radius=6, fill=badge_bg)
        draw.text((cx+162, cy+11), stat[:7], fill=col_stat, font=font_bold_xs)

        draw.text((cx+10, cy+46), f"On Field: {act} • Completed: {comp}", fill=CBK_ROYAL_BLUE if "Active" in stat else CBK_TEXT_MUTED, font=font_bold_xs)

    # Right Section: Real-Time Live Activity Stream Ticker
    rt_x = 580
    rt_w = 380
    draw.rounded_rectangle([rt_x, 210, rt_x+rt_w, h-20], radius=12, fill=CBK_CARD, outline=CBK_BORDER, width=1)
    draw.text((rt_x+20, 222), "⚡ LIVE CHECK-IN ACTIVITY STREAM", fill=CBK_ROYAL_BLUE, font=font_bold_sm)
    draw.text((rt_x+20, 240), "Real-time scans from venue turnstiles & gates", fill=CBK_TEXT_MUTED, font=font_reg_xs)

    live_events = [
        ("06:45:10", "Brian Kimani", "Athletics", "Gate 1 (Arrival)", CBK_ROYAL_BLUE),
        ("06:48:32", "Grace Mutisya", "Basketball", "Gate 1 (Arrival)", CBK_ROYAL_BLUE),
        ("07:50:14", "Bernard Kiprono", "Football", "Gate 2 (Departure)", CBK_DEEP_NAVY),
        ("07:52:05", "Joyce Cheruiyot", "Tennis", "Gate 2 (Departure)", CBK_DEEP_NAVY),
        ("08:10:22", "Alice Chebet", "Athletics", "Gate 2 [FLAGGED 22m]", CBK_DANGER),
        ("08:15:35", "Brian Kimani", "Athletics", "Gate 2 [DUAL-VERIFIED]", CBK_SUCCESS)
    ]

    y_ev = 265
    for t_str, s_name, s_disc, s_gate, s_col in live_events:
        draw.line([rt_x+20, y_ev, rt_x+rt_w-20, y_ev], fill="#F1F5F9", width=1)
        draw.text((rt_x+20, y_ev+8), t_str, fill=CBK_TEXT_MUTED, font=font_bold_xs)
        draw.text((rt_x+85, y_ev+8), s_name[:14], fill=CBK_TEXT_DARK, font=font_bold_xs)
        draw.text((rt_x+85, y_ev+24), s_disc, fill=CBK_TEXT_MUTED, font=font_reg_xs)

        draw.text((rt_x+210, y_ev+8), s_gate, fill=s_col, font=font_bold_xs)
        y_ev += 48

    path = os.path.join(OUTPUT_DIR, "ui_snippet_secretariat_dashboard.png")
    img.save(path, quality=95)
    print(f"Secretariat Dashboard Snippet saved: {path}")


# ==============================================================================
# 4. HR COMMAND CENTER SNIPPET
# ==============================================================================
def create_hr_command_center_snippet():
    w, h = 980, 620
    img = Image.new("RGB", (w, h), CBK_BG)
    draw = ImageDraw.Draw(img)

    # Top Header
    draw.rounded_rectangle([20, 20, w-20, 95], radius=12, fill=CBK_DEEP_NAVY)
    draw.rectangle([20, 91, w-20, 95], fill=CBK_GOLD)

    # Logo
    logo = get_cbk_logo_badge(target_h=55)
    if logo:
        draw.rounded_rectangle([35, 28, 35+logo.width+12, 28+logo.height+4], radius=6, fill=CBK_WHITE)
        img.paste(logo, (41, 30))
        tx = 35 + logo.width + 22
    else:
        tx = 40

    draw.text((tx, 32), "CENTRAL BANK OF KENYA | HUMAN RESOURCES ANALYTICS COMMAND CENTER", fill=CBK_GOLD, font=font_bold_xs)
    draw.text((tx, 52), "Directorate Wellness Engagement & Participation Benchmarks", fill="#FFFFFF", font=font_bold_lg)

    # Left Card: Directorate Progress Bars
    card_w = 540
    card_h = 490
    draw.rounded_rectangle([20, 110, 20+card_w, 110+card_h], radius=12, fill=CBK_CARD, outline=CBK_BORDER_BLUE, width=2)
    draw.text((40, 125), "DIRECTORATE PARTICIPATION VS TARGET QUOTAS", fill=CBK_ROYAL_BLUE, font=font_bold_sm)
    draw.text((40, 145), "Quota Target: Minimum 15 active staff per directorate", fill=CBK_TEXT_MUTED, font=font_reg_xs)

    dept_data = [
        ("Finance & Accounts", 14, 93, CBK_ROYAL_BLUE),
        ("IT & Digital Services", 15, 100, CBK_ROYAL_BLUE),
        ("Internal Audit Directorate", 6, 40, CBK_DANGER),
        ("Human Resources", 15, 100, CBK_ROYAL_BLUE),
        ("Banking & Payment Services", 12, 80, CBK_ROYAL_BLUE),
        ("Monetary Policy & Research", 10, 67, CBK_GOLD),
        ("Currency Operations & Logistics", 11, 73, CBK_GOLD),
        ("Governor's Executive Office", 7, 47, CBK_DANGER),
        ("Legal Services & Board Secretariat", 8, 53, CBK_GOLD),
        ("Financial Markets & Reserves", 13, 87, CBK_ROYAL_BLUE),
    ]

    y_bar = 175
    for dept_name, count, pct, bar_col in dept_data:
        draw.text((40, y_bar), dept_name, fill=CBK_TEXT_DARK, font=font_bold_xs)
        draw.text((360, y_bar), f"{count}/15 staff ({pct}%)", fill=bar_col, font=font_bold_xs)

        draw.rounded_rectangle([40, y_bar+18, 520, y_bar+26], radius=4, fill="#E2E8F0")
        fill_w = int(480 * (pct / 100.0))
        draw.rounded_rectangle([40, y_bar+18, 40+fill_w, y_bar+26], radius=4, fill=bar_col)
        y_bar += 38

    # Right Column: HR Insights Cards
    rt_x = 580
    rt_w = 380

    # Top Right: Participation Heatmap
    draw.rounded_rectangle([rt_x, 110, rt_x+rt_w, 320], radius=12, fill=CBK_CARD, outline=CBK_BORDER, width=1)
    draw.text((rt_x+20, 125), "WELLNESS COHORT ENGAGEMENT", fill=CBK_ROYAL_BLUE, font=font_bold_sm)
    draw.text((rt_x+20, 145), "Active participation by time of day", fill=CBK_TEXT_MUTED, font=font_reg_xs)

    cohorts = [
        ("🌅 Early Morning Camp (06:00 - 08:30)", "142 Athletes", "74% Total", CBK_ROYAL_BLUE),
        ("☀️ Mid-Day Break (12:30 - 14:00)", "38 Athletes", "20% Total", CBK_GOLD_AMBER),
        ("🌇 Evening Camp (16:30 - 18:30)", "12 Athletes", "6% Total", CBK_TEXT_MUTED)
    ]
    y_c = 175
    for c_title, c_val, c_sub, c_col in cohorts:
        draw.rounded_rectangle([rt_x+20, y_c, rt_x+rt_w-20, y_c+40], radius=8, fill=CBK_ICE_BLUE, outline=CBK_BORDER_BLUE)
        draw.text((rt_x+30, y_c+6), c_title, fill=CBK_TEXT_DARK, font=font_bold_xs)
        draw.text((rt_x+30, y_c+22), f"{c_val} • {c_sub}", fill=c_col, font=font_bold_xs)
        y_c += 46

    # Bottom Right: HR Policy Impact Card
    draw.rounded_rectangle([rt_x, 335, rt_x+rt_w, 600], radius=12, fill=CBK_ICE_BLUE, outline=CBK_ROYAL_BLUE, width=2)
    draw.text((rt_x+20, 350), "HR EXECUTIVE POLICY HIGHLIGHT", fill=CBK_DEEP_NAVY, font=font_bold_sm)
    draw.text((rt_x+20, 375), "• 100% Digital Shift from Manual Paper Logs", fill=CBK_TEXT_DARK, font=font_bold_xs)
    draw.text((rt_x+20, 400), "• Real-Time Sick Leave & Burnout Mitigation", fill=CBK_TEXT_DARK, font=font_bold_xs)
    draw.text((rt_x+20, 425), "• Directorate Wellness Inter-Cup Points Table", fill=CBK_TEXT_DARK, font=font_bold_xs)
    draw.text((rt_x+20, 450), "• Proactive Reminders for Inactive Divisions", fill=CBK_TEXT_DARK, font=font_bold_xs)
    draw.text((rt_x+20, 475), "• Institutional Health Strategy & Defensible ESG Data", fill=CBK_ROYAL_BLUE, font=font_bold_xs)

    draw.rounded_rectangle([rt_x+20, 520, rt_x+rt_w-20, 575], radius=8, fill=CBK_DEEP_NAVY)
    draw.text((rt_x+35, 532), "HR Wellness Engagement Score", fill=CBK_GOLD, font=font_bold_xs)
    draw.text((rt_x+35, 550), "94.6% Overall Bank Attendance", fill="#FFFFFF", font=font_bold_md)

    path = os.path.join(OUTPUT_DIR, "ui_snippet_hr_command_center.png")
    img.save(path, quality=95)
    print(f"HR Command Center Snippet saved: {path}")


# ==============================================================================
# 5. FINANCE COMPLIANCE & AUDIT PORTAL SNIPPET
# ==============================================================================
def create_finance_compliance_snippet():
    w, h = 980, 620
    img = Image.new("RGB", (w, h), CBK_BG)
    draw = ImageDraw.Draw(img)

    # Top Header
    draw.rounded_rectangle([20, 20, w-20, 95], radius=12, fill=CBK_DEEP_NAVY)
    draw.rectangle([20, 91, w-20, 95], fill=CBK_GOLD)

    # Logo
    logo = get_cbk_logo_badge(target_h=55)
    if logo:
        draw.rounded_rectangle([35, 28, 35+logo.width+12, 28+logo.height+4], radius=6, fill=CBK_WHITE)
        img.paste(logo, (41, 30))
        tx = 35 + logo.width + 22
    else:
        tx = 40

    draw.text((tx, 32), "CENTRAL BANK OF KENYA | FINANCE & INTERNAL AUDIT COMPLIANCE PORTAL", fill=CBK_GOLD, font=font_bold_xs)
    draw.text((tx, 52), "Sports Allowance Governance Ledger & 1-Click Accounts Payable Approval", fill="#FFFFFF", font=font_bold_lg)

    # 4 Metric Cards
    kpi_w = 220
    kpis = [
        ("APPROVED ATTENDANCES", "112 Sessions", "Dual-Gate Certified (≥45m)", CBK_ROYAL_BLUE),
        ("BLOCKED EXCEPTIONS", "6 Sessions", "Under 45m / Unpaired", CBK_DANGER),
        ("PAYROLL AUDIT INTEGRITY", "100%", "Dual Gate Server Proof", CBK_DEEP_NAVY),
        ("RECONCILIATION SPEED", "< 1 Second", "Direct ERP / EFT Feed", CBK_GOLD_AMBER)
    ]
    for idx, (title, val, sub, col) in enumerate(kpis):
        k_x = 20 + (idx * (kpi_w + 13))
        draw.rounded_rectangle([k_x, 110, k_x+kpi_w, 195], radius=10, fill=CBK_CARD, outline=col, width=2)
        draw.text((k_x+12, 118), title, fill=CBK_TEXT_MUTED, font=font_bold_xs)
        draw.text((k_x+12, 136), val, fill=col, font=font_bold_md)
        draw.text((k_x+12, 170), sub, fill=CBK_TEXT_DARK, font=font_reg_xs)

    # Main Ledger Table Card
    table_w = w - 40
    table_h = 390
    draw.rounded_rectangle([20, 210, 20+table_w, 210+table_h], radius=12, fill=CBK_CARD, outline=CBK_BORDER_BLUE, width=2)
    draw.text((35, 222), "CERTIFIED ATTENDANCE RECONCILIATION LEDGER (CIRCULAR CBK/HR/WEL/2026)", fill=CBK_ROYAL_BLUE, font=font_bold_sm)

    # Table Header Row
    headers = [
        ("Staff Name & ID", 35, 200),
        ("Discipline & Station", 240, 180),
        ("Gate 1", 425, 80),
        ("Gate 2", 510, 80),
        ("Active Duration", 595, 110),
        ("Audit Status", 710, 120),
        ("Certified Unit", 835, 95)
    ]
    draw.rounded_rectangle([30, 245, w-30, 275], radius=6, fill=CBK_ICE_BLUE)
    for h_name, h_x, _ in headers:
        draw.text((h_x, 252), h_name, fill=CBK_DEEP_NAVY, font=font_bold_xs)

    # Table Rows
    records = [
        ("Brian Kimani (CBK-1024)", "Athletics (Track 100m)", "06:45:10", "08:00:10", "75.0 mins", "DUAL_VERIFIED", "1 UNIT (CERT)", CBK_SUCCESS),
        ("Grace Mutisya (CBK-1088)", "Basketball (Court 1)", "06:48:32", "07:49:15", "60.7 mins", "DUAL_VERIFIED", "1 UNIT (CERT)", CBK_SUCCESS),
        ("Bernard Kiprono (CBK-1045)", "Football (Pitch A)", "06:30:00", "07:50:14", "80.2 mins", "DUAL_VERIFIED", "1 UNIT (CERT)", CBK_SUCCESS),
        ("Alice Chebet (CBK-1099)", "Athletics (Gate 3)", "07:48:00", "08:10:22", "22.3 mins", "SHORT_SESSION", "0 UNITS [BLOCK]", CBK_DANGER),
        ("David Koech (CBK-1012)", "Swimming (Poolside)", "07:00:15", "07:55:00", "54.7 mins", "DUAL_VERIFIED", "1 UNIT (CERT)", CBK_SUCCESS),
        ("Lucy Wanjiru (CBK-1067)", "Lawn Tennis (Court 2)", "06:50:00", "--:--:--", "--", "AWAITING_GATE2", "PENDING", CBK_GOLD_AMBER),
    ]

    y_row = 285
    for r_name, r_disc, r_g1, r_g2, r_dur, r_stat, r_disb, r_col in records:
        draw.line([30, y_row, w-30, y_row], fill="#F1F5F9", width=1)
        draw.text((35, y_row+8), r_name, fill=CBK_TEXT_DARK, font=font_bold_xs)
        draw.text((240, y_row+8), r_disc, fill=CBK_TEXT_MUTED, font=font_reg_xs)
        draw.text((425, y_row+8), r_g1, fill=CBK_TEXT_MUTED, font=font_reg_xs)
        draw.text((510, y_row+8), r_g2, fill=CBK_TEXT_MUTED, font=font_reg_xs)
        draw.text((595, y_row+8), r_dur, fill=CBK_TEXT_DARK, font=font_bold_xs)

        draw.text((710, y_row+8), r_stat, fill=r_col, font=font_bold_xs)
        draw.text((835, y_row+8), r_disb, fill=r_col, font=font_bold_xs)
        y_row += 38

    # 1-Click Approval Action Bar at bottom
    draw.rounded_rectangle([30, 540, w-30, 585], radius=8, fill=CBK_DEEP_NAVY)
    draw.text((45, 552), "TOTAL CERTIFIED ATTENDANCES: 112 SESSIONS (VALUATION RESERVED FOR FINANCE)", fill=CBK_GOLD, font=font_bold_sm)

    draw.rounded_rectangle([w-270, 546, w-40, 578], radius=6, fill=CBK_ROYAL_BLUE, outline=CBK_GOLD, width=2)
    draw.text((w-255, 554), "⚡ 1-CLICK BATCH AP DISPATCH", fill="#FFFFFF", font=font_bold_xs)

    path = os.path.join(OUTPUT_DIR, "ui_snippet_finance_compliance.png")
    img.save(path, quality=95)
    print(f"Finance Compliance Snippet saved: {path}")


# ==============================================================================
# 6. EMAIL INSTITUTIONAL RECEIPT SNIPPET
# ==============================================================================
def create_email_receipt_snippet():
    w, h = 640, 800
    img = Image.new("RGB", (w, h), CBK_BG)
    draw = ImageDraw.Draw(img)

    # Email Container
    draw.rounded_rectangle([20, 20, w-20, h-20], radius=16, fill=CBK_CARD, outline=CBK_BORDER_BLUE, width=2)

    # Header Bar
    draw.rounded_rectangle([20, 20, w-20, 115], radius=16, fill=CBK_DEEP_NAVY)
    draw.rectangle([20, 111, w-20, 115], fill=CBK_GOLD)

    # Logo
    logo = get_cbk_logo_badge(target_h=55)
    if logo:
        draw.rounded_rectangle([35, 32, 35+logo.width+12, 32+logo.height+4], radius=6, fill=CBK_WHITE)
        img.paste(logo, (41, 34))
        tx = 35 + logo.width + 20
    else:
        tx = 35

    draw.text((tx, 35), "CENTRAL BANK OF KENYA", fill=CBK_GOLD, font=font_bold_xs)
    draw.text((tx, 55), "DSWAAP Dual-Verification Receipt", fill="#FFFFFF", font=font_bold_md)
    draw.text((tx, 82), "Official Attendance Accreditation Voucher", fill=CBK_ICE_BLUE, font=font_reg_xs)

    # Receipt Metadata
    y = 135
    draw.text((40, y), "VOUCHER ID: CBK-DSWAAP-20260930-ATH-1024", fill=CBK_ROYAL_BLUE, font=font_bold_xs)
    draw.text((40, y+22), "Date: Wednesday, 30 September 2026 | Domain: @centralbank.go.ke", fill=CBK_TEXT_MUTED, font=font_reg_xs)

    # Verified Banner
    y = 190
    draw.rounded_rectangle([40, y, w-40, y+60], radius=10, fill=CBK_ICE_BLUE, outline=CBK_ROYAL_BLUE, width=2)
    draw.text((55, y+10), "OFFICIALLY CERTIFIED (1 ATTENDANCE UNIT)", fill=CBK_ROYAL_BLUE, font=font_bold_sm)
    draw.text((55, y+32), "Active Session Duration: 75.0 Mins (Policy Floor: >= 45 Mins)", fill=CBK_TEXT_DARK, font=font_reg_xs)

    # Details Grid
    y = 270
    fields = [
        ("Participant Name", "Brian Kimani"),
        ("Staff ID", "CBK-1024"),
        ("Directorate", "Monetary Policy & Economic Research"),
        ("Institutional Email", "bkimani@centralbank.go.ke"),
        ("Sporting Discipline", "Athletics & Track (10K / 5K Running Camp)"),
        ("Gate 1 (Arrival Post)", "Track 100m Start Point [06:45:10]"),
        ("Gate 2 (Departure Post)", "Perimeter Track Gate 3 [08:00:10]"),
        ("Session Duration", "75.0 Minutes (Reconciled)"),
        ("Attendance Accreditation", "1 Compliant Session Unit (Verified)"),
    ]

    for f_label, f_val in fields:
        draw.line([40, y, w-40, y], fill="#F1F5F9", width=1)
        draw.text((40, y+8), f_label, fill=CBK_TEXT_MUTED, font=font_reg_xs)
        draw.text((230, y+8), f_val, fill=CBK_TEXT_DARK, font=font_bold_xs)
        y += 34

    # Audit Seal Box
    y = 595
    draw.rounded_rectangle([40, y, w-40, y+105], radius=10, fill=CBK_ICE_BLUE, outline=CBK_BORDER_BLUE, width=2)
    draw.text((55, y+12), "🔒 CBK INTERNAL AUDIT CRYPTOGRAPHIC STAMP", fill=CBK_ROYAL_BLUE, font=font_bold_xs)
    draw.text((55, y+32), "HMAC-SHA256 Token: 929f7218a378d6c3...[Verified]", fill=CBK_TEXT_MUTED, font=font_reg_xs)
    draw.text((55, y+52), "Persistence: Reconciled in CBK SQLite Ledger & Google Sheets Mirror", fill=CBK_TEXT_MUTED, font=font_reg_xs)
    draw.text((55, y+72), "Authority: Head of HR & Director of Finance & Accounts", fill=CBK_DEEP_NAVY, font=font_bold_xs)

    # Footer
    draw.text((40, 740), "Central Bank of Kenya • Haile Selassie Avenue, Nairobi • centralbank.go.ke", fill=CBK_TEXT_MUTED, font=font_reg_xs)

    path = os.path.join(OUTPUT_DIR, "ui_snippet_email_receipt.png")
    img.save(path, quality=95)
    print(f"Email Receipt Snippet saved: {path}")


def generate_all_snippets():
    print("=" * 65)
    print("GENERATING OFFICIAL CBK DSWAAP UI SNIPPETS")
    print("Corporate Colors: Royal Blue (#025BBF), Navy (#10529E), Gold (#F8B82D)")
    print("=" * 65)
    create_mobile_checkin_snippet()
    create_captain_terminal_snippet()
    create_secretariat_dashboard_snippet()
    create_hr_command_center_snippet()
    create_finance_compliance_snippet()
    create_email_receipt_snippet()
    print("All 6 CBK UI Snippets generated successfully!")


if __name__ == "__main__":
    generate_all_snippets()

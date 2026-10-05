"""
Generate High-Converting, High-Resolution Marketing Flyer for STRIDE™ Enterprise Platform
Produces:
1. STRIDE_Enterprise_Marketing_Flyer.png (1600 x 2560 - 4K High-Res Portrait Flyer)
2. STRIDE_Enterprise_Marketing_Flyer.jpg (Optimized for WhatsApp / Email)
3. STRIDE_Enterprise_Executive_Flyer.pdf (Executive Vector PDF via ReportLab)
Outputs saved to both project directory and artifact directory.
"""

import os
import sys
import shutil

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACT_DIR = r"C:\Users\user\.gemini\antigravity\brain\13019df5-c73e-40a7-9dbf-48db7e5f7a5e"

WIDTH = 1600
HEIGHT = 2560

# Palette
C_NAVY_DEEP = (3, 9, 20)
C_NAVY_MID = (8, 24, 48)
C_NAVY_LIGHT = (14, 38, 74)
C_GOLD = (245, 197, 66)
C_GOLD_LIGHT = (255, 235, 140)
C_CYAN = (0, 242, 254)
C_CYAN_LIGHT = (165, 243, 252)
C_EMERALD = (16, 185, 129)
C_WHITE = (255, 255, 255)
C_SLATE = (203, 213, 225)
C_SLATE_MUTED = (148, 163, 184)
C_CARD_BG = (10, 26, 52, 230)
C_BORDER_GOLD = (245, 197, 66, 100)
C_BORDER_CYAN = (0, 242, 254, 80)
C_BORDER_SLATE = (51, 65, 85)

def get_font(name: str, size: int):
    try:
        return ImageFont.truetype(name, size)
    except Exception:
        try:
            return ImageFont.truetype("arial.ttf", size)
        except Exception:
            return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, fill=None, outline=None, width=1, radius=16):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def generate_image_flyer():
    im = Image.new("RGBA", (WIDTH, HEIGHT), C_NAVY_DEEP)
    draw = ImageDraw.Draw(im)

    # 1. Subtle radial gradient & glow effects
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(C_NAVY_DEEP[0] + (12 - C_NAVY_DEEP[0]) * (1 - ratio) + (2 - C_NAVY_DEEP[0]) * ratio)
        g = int(C_NAVY_DEEP[1] + (32 - C_NAVY_DEEP[1]) * (1 - ratio) + (7 - C_NAVY_DEEP[1]) * ratio)
        b = int(C_NAVY_DEEP[2] + (64 - C_NAVY_DEEP[2]) * (1 - ratio) + (18 - C_NAVY_DEEP[2]) * ratio)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))

    # Top & Bottom accent lines
    draw.line([(0, 0), (WIDTH, 0)], fill=C_GOLD, width=10)
    draw.line([(0, HEIGHT-6), (WIDTH, HEIGHT-6)], fill=C_GOLD, width=6)

    # 2. HEADER SECTION
    pad = 80
    y_cursor = 70

    # Top Tag
    tag_font = get_font("segoeuib.ttf", 22)
    tag_text = "ENTERPRISE ACCREDITATION & STATUTORY GOVERNANCE PLATFORM • v2.8"
    draw_rounded_rect(draw, [pad, y_cursor, pad + 820, y_cursor + 44], fill=(245, 197, 66, 35), outline=C_GOLD, width=2, radius=8)
    draw.text((pad + 18, y_cursor + 9), tag_text, fill=C_GOLD_LIGHT, font=tag_font)

    y_cursor += 65

    # Main Hero Title
    hero_font = get_font("segoeuib.ttf", 86)
    draw.text((pad, y_cursor), "CBK STRIDE™", fill=C_GOLD, font=hero_font)
    
    # Sub-heading
    y_cursor += 105
    sub_font = get_font("segoeuib.ttf", 34)
    draw.text((pad, y_cursor), "The Zero-Capex Sovereign Engine for Corporate AGMs, Digital Passes & Multi-Sport Telemetry", fill=C_WHITE, font=sub_font)

    # Right info badge in header
    h_badge_box = [WIDTH - pad - 460, 60, WIDTH - pad, 250]
    draw_rounded_rect(draw, h_badge_box, fill=(6, 20, 42, 220), outline=C_CYAN, width=2, radius=14)
    badge_f1 = get_font("segoeuib.ttf", 22)
    badge_f2 = get_font("segoeui.ttf", 20)
    draw.text((h_badge_box[0] + 20, h_badge_box[1] + 18), "• ODPC § 25 Compliance Certified", fill=C_CYAN, font=badge_f1)
    draw.text((h_badge_box[0] + 20, h_badge_box[1] + 58), "Infrastructure Capex: KES 0.00", fill=C_EMERALD, font=badge_f1)
    draw.text((h_badge_box[0] + 20, h_badge_box[1] + 98), "Onboarding Speed: < 5 Minutes", fill=C_GOLD, font=badge_f1)
    draw.text((h_badge_box[0] + 20, h_badge_box[1] + 138), "Dispatch: SMS • Email • WhatsApp", fill=C_SLATE, font=badge_f2)

    y_cursor += 75
    draw.line([(pad, y_cursor), (WIDTH - pad, y_cursor)], fill=C_BORDER_SLATE, width=2)
    y_cursor += 35

    # 3. FOUR PILLARS ROW
    sec_title_f = get_font("segoeuib.ttf", 36)
    draw.text((pad, y_cursor), "Four Pillars of Institutional Trust", fill=C_WHITE, font=sec_title_f)
    y_cursor += 50

    pillar_w = (WIDTH - (2 * pad) - (3 * 24)) // 4
    pillar_h = 240
    pillars = [
        ("STATUTORY AGM & QUORUM", "Real-time SASRA floor compliance, share-weighted voting power, proxy audits & instant returning officer certification.", "Companies Act § 284", C_GOLD),
        ("KENYA DPA 2019 PRIVACY", "Default public shielding of delegate phone numbers & institutional emails. 2FA Secretariat passkey reveal.", "ODPC § 25 Certified", C_CYAN),
        ("ZERO-CAPEX SERVERLESS", "Cloud-native high-availability PostgreSQL. Zero servers to buy, zero licensing fees, zero infrastructure overhead.", "99.98% High Availability", C_EMERALD),
        ("MULTI-SPORT TELEMETRY", "18-discipline sports management (Golf, Football, Chess, Athletics). Instant captain pitchside roll call & allowance audits.", "Zero-Ghost Athlete Audit", C_GOLD)
    ]

    for i, (p_title, p_desc, p_badge, p_col) in enumerate(pillars):
        px = pad + i * (pillar_w + 24)
        box = [px, y_cursor, px + pillar_w, y_cursor + pillar_h]
        draw_rounded_rect(draw, box, fill=(8, 22, 44, 200), outline=p_col, width=2, radius=12)
        
        # Title
        draw.text((px + 16, y_cursor + 18), p_title, fill=p_col, font=get_font("segoeuib.ttf", 20))
        
        # Desc (wrap roughly)
        words = p_desc.split()
        lines = []
        cur_l = []
        for w in words:
            if len(" ".join(cur_l + [w])) > 28:
                lines.append(" ".join(cur_l))
                cur_l = [w]
            else:
                cur_l.append(w)
        if cur_l:
            lines.append(" ".join(cur_l))
        
        desc_y = y_cursor + 54
        for l in lines[:4]:
            draw.text((px + 16, desc_y), l, fill=C_SLATE, font=get_font("segoeui.ttf", 17))
            desc_y += 26

        # Footer badge
        draw.line([(px + 16, y_cursor + pillar_h - 40), (px + pillar_w - 16, y_cursor + pillar_h - 40)], fill=C_BORDER_SLATE, width=1)
        draw.text((px + 16, y_cursor + pillar_h - 30), f"• {p_badge}", fill=p_col, font=get_font("segoeuib.ttf", 16))

    y_cursor += pillar_h + 45

    # 4. LIVE EXECUTIVE TELEMETRY MOCKUPS
    draw.text((pad, y_cursor), "Live Executive Telemetry Mockups (As Deployed for Central Bank & SACCO)", fill=C_WHITE, font=sec_title_f)
    y_cursor += 50

    mock_h = 440
    # Left Mockup (Quorum Meter & Gate Scanner) - 60% width
    left_w = int((WIDTH - (2 * pad) - 30) * 0.62)
    left_box = [pad, y_cursor, pad + left_w, y_cursor + mock_h]
    draw_rounded_rect(draw, left_box, fill=(5, 18, 36, 230), outline=C_CYAN, width=2, radius=14)

    # Header of Mockup
    draw.text((pad + 24, y_cursor + 18), "Gate Usher Scanner & Statutory Quorum Meter", fill=C_CYAN_LIGHT, font=get_font("segoeuib.ttf", 24))
    draw_rounded_rect(draw, [pad + left_w - 290, y_cursor + 16, pad + left_w - 20, y_cursor + 48], fill=(16, 185, 129, 40), outline=C_EMERALD, width=1, radius=6)
    draw.text((pad + left_w - 280, y_cursor + 22), "• STATUTORY QUORUM ATTAINED", fill=C_EMERALD, font=get_font("segoeuib.ttf", 16))

    # KPI Grid inside left mockup
    kpi_y = y_cursor + 66
    kpi_w = (left_w - 48 - (3 * 16)) // 4
    kpis = [
        ("QUORUM FLOOR", "50", C_GOLD),
        ("IN AUDITORIUM", "101", C_EMERALD),
        ("PRINCIPALS", "92", C_CYAN),
        ("PROXIES", "9", C_WHITE)
    ]
    for ki, (kt, kv, kc) in enumerate(kpis):
        kx = pad + 24 + ki * (kpi_w + 16)
        draw_rounded_rect(draw, [kx, kpi_y, kx + kpi_w, kpi_y + 70], fill=(2, 10, 22, 220), outline=C_BORDER_SLATE, width=1, radius=8)
        draw.text((kx + 12, kpi_y + 10), kt, fill=C_SLATE_MUTED, font=get_font("segoeuib.ttf", 13))
        draw.text((kx + 12, kpi_y + 30), kv, fill=kc, font=get_font("segoeuib.ttf", 30))

    # Progress bar
    pb_y = kpi_y + 88
    draw.text((pad + 24, pb_y), "Constitutional Floor Progress: 100% (Surplus +51 Delegates)", fill=C_SLATE, font=get_font("segoeuib.ttf", 16))
    draw_rounded_rect(draw, [pad + 24, pb_y + 24, pad + left_w - 24, pb_y + 40], fill=(2, 8, 18), outline=C_BORDER_SLATE, width=1, radius=8)
    draw_rounded_rect(draw, [pad + 26, pb_y + 26, pad + left_w - 26, pb_y + 38], fill=C_EMERALD, radius=6)

    # Masked Roster Table
    tbl_y = pb_y + 54
    draw_rounded_rect(draw, [pad + 24, tbl_y, pad + left_w - 24, y_cursor + mock_h - 20], fill=(2, 8, 18, 230), outline=C_BORDER_SLATE, width=1, radius=8)
    
    t_hdr_font = get_font("segoeuib.ttf", 14)
    t_row_font = get_font("segoeui.ttf", 15)
    draw.text((pad + 38, tbl_y + 10), "PASS ID", fill=C_SLATE_MUTED, font=t_hdr_font)
    draw.text((pad + 170, tbl_y + 10), "DELEGATE NAME", fill=C_SLATE_MUTED, font=t_hdr_font)
    draw.text((pad + 390, tbl_y + 10), "PHONE (ODPC MASKED)", fill=C_SLATE_MUTED, font=t_hdr_font)
    draw.text((pad + 580, tbl_y + 10), "CLEARANCE REF", fill=C_SLATE_MUTED, font=t_hdr_font)
    draw.text((pad + left_w - 140, tbl_y + 10), "STATUS", fill=C_SLATE_MUTED, font=t_hdr_font)
    draw.line([(pad + 24, tbl_y + 32), (pad + left_w - 24, tbl_y + 32)], fill=C_BORDER_SLATE, width=1)

    sample_rows = [
        ("TKT-BK-342801", "Samuel Gathigi (IT)", "072* *** *01", "BKS-ACC-01", "ADMITTED", C_EMERALD),
        ("TKT-BK-3366", "Andrew Ogola (Chess)", "072* *** *90", "BK3366", "ADMITTED", C_EMERALD),
        ("TKT-BK-342802", "Dr. Beatrice Kiptoo", "072* *** *22", "BKS-ACC-02", "ADMITTED", C_EMERALD),
        ("TKT-BK-342803", "Capt. Geoffrey Kemboi", "072* *** *03", "BKS-ACC-03", "REGISTERED", C_CYAN)
    ]
    ry = tbl_y + 42
    for r_id, r_name, r_ph, r_ref, r_st, r_col in sample_rows:
        draw.text((pad + 38, ry), r_id, fill=C_GOLD, font=t_row_font)
        draw.text((pad + 170, ry), r_name, fill=C_WHITE, font=t_row_font)
        draw.text((pad + 390, ry), r_ph, fill=C_SLATE_MUTED, font=t_row_font)
        draw.text((pad + 580, ry), r_ref, fill=C_CYAN, font=t_row_font)
        draw.text((pad + left_w - 140, ry), r_st, fill=r_col, font=get_font("segoeuib.ttf", 15))
        ry += 30

    # Right Mockup (Encrypted Digital Mobile Pass Card) - 38% width
    right_x = pad + left_w + 30
    right_w = WIDTH - pad - right_x
    right_box = [right_x, y_cursor, right_x + right_w, y_cursor + mock_h]
    draw_rounded_rect(draw, right_box, fill=(9, 28, 56, 230), outline=C_GOLD, width=2, radius=14)

    draw.text((right_x + 24, y_cursor + 18), "Universal Digital Mobile Pass", fill=C_GOLD, font=get_font("segoeuib.ttf", 24))
    draw.text((right_x + 24, y_cursor + 48), "Banki Kuu SACCO 58th AGM Official Pass", fill=C_SLATE, font=get_font("segoeui.ttf", 16))

    # Inner Pass Card graphic
    card_box = [right_x + 24, y_cursor + 80, right_x + right_w - 24, y_cursor + mock_h - 24]
    draw_rounded_rect(draw, card_box, fill=(4, 14, 30), outline=C_GOLD, width=2, radius=12)

    draw.text((right_x + 44, y_cursor + 100), "STRIDE™ ENCRYPTED ACCREDITATION", fill=C_GOLD_LIGHT, font=get_font("segoeuib.ttf", 16))
    draw.text((right_x + 44, y_cursor + 125), "Delegate: Andrew Ogola", fill=C_WHITE, font=get_font("segoeuib.ttf", 22))
    draw.text((right_x + 44, y_cursor + 155), "Role: Chess Captain / Principal Shareholder", fill=C_CYAN, font=get_font("segoeui.ttf", 16))
    draw.text((right_x + 44, y_cursor + 180), "Department: IT & Digital Services", fill=C_SLATE, font=get_font("segoeui.ttf", 15))

    # Mock QR Code Box
    qr_box = [right_x + 44, y_cursor + 215, right_x + 190, y_cursor + 360]
    draw_rounded_rect(draw, qr_box, fill=C_WHITE, radius=8)
    draw.text((qr_box[0] + 16, qr_box[1] + 55), "[ DYNAMIC ]\n[ QR PASS ]", fill=(0, 0, 0), font=get_font("segoeuib.ttf", 18))

    # Pass Metadata
    draw.text((right_x + 210, y_cursor + 225), "Pass Serial ID:", fill=C_SLATE_MUTED, font=get_font("segoeui.ttf", 14))
    draw.text((right_x + 210, y_cursor + 245), "TKT-BK-3366", fill=C_GOLD, font=get_font("segoeuib.ttf", 18))

    draw.text((right_x + 210, y_cursor + 275), "Accreditation Ref:", fill=C_SLATE_MUTED, font=get_font("segoeui.ttf", 14))
    draw.text((right_x + 210, y_cursor + 295), "BK3366 (Pre-Paid)", fill=C_CYAN, font=get_font("segoeuib.ttf", 18))

    # Badge in Pass
    draw_rounded_rect(draw, [right_x + 44, y_cursor + 375, right_x + right_w - 44, y_cursor + 405], fill=(16, 185, 129, 35), outline=C_EMERALD, width=1, radius=6)
    draw.text((right_x + 60, y_cursor + 382), "• STATUTORY ACCREDITATION CONFIRMED • KES 0.00", fill=C_EMERALD, font=get_font("segoeuib.ttf", 15))

    y_cursor += mock_h + 45

    # 5. ZERO-CAPEX VS BULLETPROOF PRIVACY (2 LARGE CARDS)
    draw.text((pad, y_cursor), "Enterprise Architecture & Security Guarantees", fill=C_WHITE, font=sec_title_f)
    y_cursor += 50

    half_w = (WIDTH - (2 * pad) - 30) // 2
    comp_h = 320

    # Card Left: Zero-Capex
    cl_box = [pad, y_cursor, pad + half_w, y_cursor + comp_h]
    draw_rounded_rect(draw, cl_box, fill=(6, 20, 40, 220), outline=C_CYAN, width=2, radius=14)
    draw.text((pad + 24, y_cursor + 20), "Zero-Capex Cloud-Native AI Architecture", fill=C_CYAN, font=get_font("segoeuib.ttf", 24))
    
    ca_items = [
        "Cloud-Native Serverless Compute: Zero hardware servers or local VM licensing.",
        "AWS Frankfurt Enterprise PostgreSQL: Multi-region auto-failover with SSL encryption.",
        "Self-Serve Event Creator Wizard: Launch an AGM or Marathon in under 4 minutes.",
        "Camera & iPad Scanner Ready: Door ushers use existing phones or tablets.",
        "Instant CSV & Excel Reporting: Direct export of statutory attendance books."
    ]
    cy_text = y_cursor + 65
    for item in ca_items:
        draw.text((pad + 24, cy_text), "•", fill=C_EMERALD, font=get_font("segoeuib.ttf", 20))
        draw.text((pad + 52, cy_text + 2), item, fill=C_SLATE, font=get_font("segoeui.ttf", 17))
        cy_text += 46

    # Card Right: Privacy
    cr_box = [pad + half_w + 30, y_cursor, pad + (2 * half_w) + 30, y_cursor + comp_h]
    draw_rounded_rect(draw, cr_box, fill=(4, 24, 20, 220), outline=C_EMERALD, width=2, radius=14)
    draw.text((pad + half_w + 54, y_cursor + 20), "Bulletproof Kenya DPA 2019 Privacy Pipeline", fill=C_EMERALD, font=get_font("segoeuib.ttf", 24))

    pr_items = [
        "Dynamic Cryptographic Masking: Delegate phones (072* *** *56) & emails shielded.",
        "Two-Factor Secretariat RBAC: Staff ID + Security Passkey unlock barrier.",
        "15-Minute Auto-Relock: Gate terminals auto-mask if unattended to stop shoulder-surfing.",
        "Decoupled Secret Ballot: Statutory voter identity strictly separated from ballot choices.",
        "Forensic Audit Ledger: Immutable recording of every unmasking & CSV export."
    ]
    cy_text2 = y_cursor + 65
    for item in pr_items:
        draw.text((pad + half_w + 54, cy_text2), "•", fill=C_EMERALD, font=get_font("segoeuib.ttf", 20))
        draw.text((pad + half_w + 82, cy_text2 + 2), item, fill=C_SLATE, font=get_font("segoeui.ttf", 17))
        cy_text2 += 46

    y_cursor += comp_h + 45

    # 6. COMMERCIAL ROI & PRICING TIERS
    draw.text((pad, y_cursor), "Transparent Modular Pricing (Zero Hidden Fees)", fill=C_WHITE, font=sec_title_f)
    y_cursor += 50

    tier_w = (WIDTH - (2 * pad) - 40) // 3
    tier_h = 280
    tiers = [
        ("Society / Sports Club Tier", "KES 15,000", "Up to 100 Delegates", ["• Self-Serve Event Creator Wizard", "• Dynamic QR Passes & Email Dispatch", "• Live Door Usher Scanner Terminal", "• Official CSV Attendance Register"], C_SLATE),
        ("Mid-Sized Corporate / SACCO", "KES 35,000", "101 – 500 Delegates (Most Popular)", ["• All Society Tier Capabilities", "• SASRA Statutory Quorum Radar Meter", "• Encrypted Digital Secret Ballot (3 Motions)", "• Kenya DPA 2019 PII Masking & 2FA RBAC"], C_GOLD),
        ("Large Listed PLC / Tier-1", "KES 75,000", "501 – 2,500+ Delegates", ["• All Mid-Sized Tier Capabilities", "• Multi-Gate Dual Usher Synchronizer", "• Share-Weighted Governance & Candidate Matrix", "• Dedicated PostgreSQL High-Throughput Node"], C_CYAN)
    ]

    for ti, (t_name, t_price, t_del, t_feats, t_col) in enumerate(tiers):
        tx = pad + ti * (tier_w + 20)
        t_box = [tx, y_cursor, tx + tier_w, y_cursor + tier_h]
        is_pop = (ti == 1)
        draw_rounded_rect(draw, t_box, fill=(8, 24, 48, 230), outline=t_col if is_pop else C_BORDER_SLATE, width=3 if is_pop else 1, radius=12)

        if is_pop:
            draw_rounded_rect(draw, [tx + tier_w - 180, y_cursor, tx + tier_w, y_cursor + 28], fill=C_GOLD, radius=6)
            draw.text((tx + tier_w - 170, y_cursor + 5), "MOST POPULAR", fill=(0, 0, 0), font=get_font("segoeuib.ttf", 13))

        draw.text((tx + 20, y_cursor + 16), t_name, fill=t_col, font=get_font("segoeuib.ttf", 20))
        draw.text((tx + 20, y_cursor + 44), t_price, fill=C_WHITE, font=get_font("segoeuib.ttf", 36))
        draw.text((tx + 20, y_cursor + 90), t_del, fill=C_SLATE_MUTED, font=get_font("segoeui.ttf", 16))
        draw.line([(tx + 20, y_cursor + 115), (tx + tier_w - 20, y_cursor + 115)], fill=C_BORDER_SLATE, width=1)

        fy = y_cursor + 128
        for f in t_feats:
            draw.text((tx + 20, fy), f, fill=C_SLATE, font=get_font("segoeui.ttf", 15))
            fy += 30

    y_cursor += tier_h + 45

    # 7. FOOTER CALL TO ACTION BAR
    footer_box = [pad, y_cursor, WIDTH - pad, y_cursor + 140]
    draw_rounded_rect(draw, footer_box, fill=(10, 30, 60), outline=C_GOLD, width=2, radius=16)

    draw.text((pad + 30, y_cursor + 24), "DEPLOY STRIDE™ FOR YOUR NEXT AGM, MARATHON, OR CORPORATE SUMMIT", fill=C_WHITE, font=get_font("segoeuib.ttf", 24))
    draw.text((pad + 30, y_cursor + 62), "Experience instant zero-capex digital passes, real-time quorum transparency, and bulletproof privacy.", fill=C_SLATE, font=get_font("segoeui.ttf", 18))
    draw.text((pad + 30, y_cursor + 94), "Official Production URL: https://cbk-stride.streamlit.app • Pilot Partner: Central Bank Sports Club", fill=C_GOLD_LIGHT, font=get_font("segoeuib.ttf", 17))

    # CTA Button graphic on right
    cta_btn = [WIDTH - pad - 340, y_cursor + 35, WIDTH - pad - 30, y_cursor + 105]
    draw_rounded_rect(draw, cta_btn, fill=C_GOLD, radius=10)
    draw.text((cta_btn[0] + 35, cta_btn[1] + 20), "Schedule Live Demo", fill=(2, 8, 18), font=get_font("segoeuib.ttf", 22))

    # Save PNG and JPG
    out_png_proj = os.path.join(BASE_DIR, "STRIDE_Enterprise_Marketing_Flyer.png")
    out_jpg_proj = os.path.join(BASE_DIR, "STRIDE_Enterprise_Marketing_Flyer.jpg")
    out_png_art = os.path.join(ARTIFACT_DIR, "STRIDE_Enterprise_Marketing_Flyer.png")
    out_jpg_art = os.path.join(ARTIFACT_DIR, "STRIDE_Enterprise_Marketing_Flyer.jpg")

    im.save(out_png_proj, "PNG")
    im.convert("RGB").save(out_jpg_proj, "JPEG", quality=95)
    shutil.copy2(out_png_proj, out_png_art)
    shutil.copy2(out_jpg_proj, out_jpg_art)

    print(f"✓ High-Resolution Flyer PNG: {out_png_proj}")
    print(f"✓ Optimized Flyer JPG: {out_jpg_proj}")

def generate_pdf_flyer():
    pdf_proj = os.path.join(BASE_DIR, "STRIDE_Enterprise_Executive_Flyer.pdf")
    pdf_art = os.path.join(ARTIFACT_DIR, "STRIDE_Enterprise_Executive_Flyer.pdf")

    doc = SimpleDocTemplate(
        pdf_proj,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#F5C542')
    )
    sub_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#00F2FE')
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1E293B')
    )
    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155')
    )

    story = []

    # Header
    story.append(Paragraph("<b>CBK STRIDE™</b> — Enterprise Digital Pass & Governance Platform", title_style))
    story.append(Paragraph("The Zero-Capex Platform for Corporate AGMs, Shareholder Democracy & Multi-Sport Telemetry", sub_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#F5C542'), spaceAfter=12))

    # Core Value Summary
    story.append(Paragraph(
        "<b>STRIDE™</b> replaces chaotic physical registers, credential forgery, and ballot tampering with bank-grade "
        "cryptographic digital passes, real-time quorum telemetry, and strict adherence to the <b>Kenya Data Protection Act 2019 (ODPC § 25)</b>. "
        "Built on cloud-native PostgreSQL and deployed on Streamlit Cloud, it requires zero capital expenditure (Zero Capex) and zero on-premise hardware.",
        body_style
    ))
    story.append(Spacer(1, 12))

    # 4 Pillars Table
    pillar_data = [
        [
            Paragraph("<b>• Statutory AGM & Quorum</b><br/>SASRA floor compliance, share-weighted voting power, proxy audits, and instant returning officer gazetting.", bullet_style),
            Paragraph("<b>• Kenya DPA 2019 Privacy</b><br/>Default public shielding of delegate contact data (072* *** *56). 2FA Secretariat passkey reveal with 15-min auto-relock.", bullet_style)
        ],
        [
            Paragraph("<b>• Zero-Capex Serverless</b><br/>AWS Frankfurt PostgreSQL persistence. Instant onboarding in &lt; 5 mins. Door ushers scan via standard phone cameras.", bullet_style),
            Paragraph("<b>• Multi-Sport Telemetry</b><br/>18-discipline sports management (Golf, Football, Chess, Athletics). Instant captain roll call & allowance audits.", bullet_style)
        ]
    ]

    p_table = Table(pillar_data, colWidths=[260, 260])
    p_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(p_table)
    story.append(Spacer(1, 14))

    # Pricing Table
    story.append(Paragraph("<b>Transparent Modular Pricing (Zero Hidden Setup Fees)</b>", sub_style))
    story.append(Spacer(1, 6))

    tier_data = [
        ["Tier", "Capacity", "Platform Fee", "Key Included Capabilities"],
        ["Society / Club", "Up to 100", "KES 15,000", "Wizard Creator, Dynamic QR Passes, Gate Scanner, CSV Export"],
        ["Mid-Sized Corporate / SACCO", "101 – 500", "KES 35,000", "SASRA Quorum Meter, Encrypted Secret Ballot, DPA 2019 Masking"],
        ["Large PLC / Tier-1 Enterprise", "501 – 2,500+", "KES 75,000", "Multi-Gate Dual Usher Sync, Share-Weighted Matrix, Priority Node"]
    ]
    t_table = Table(tier_data, colWidths=[120, 70, 85, 245])
    t_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#041021')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#F5C542')),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8.5),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#FFFFFF')),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_table)
    story.append(Spacer(1, 16))

    # CTA Footer Box
    cta_data = [[
        Paragraph(
            "<b>DEPLOY STRIDE™ IN PRODUCTION TODAY</b><br/>"
            "Official Platform: <b>https://cbk-stride.streamlit.app</b><br/>"
            "Technology Partner: Central Bank of Kenya Sports Club & Banki Kuu Staff SACCO Society.<br/>"
            "To schedule an executive 15-minute briefing or launch a complimentary pilot, visit the portal above.",
            bullet_style
        )
    ]]
    cta_table = Table(cta_data, colWidths=[520])
    cta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#3B82F6')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(cta_table)

    doc.build(story)
    shutil.copy2(pdf_proj, pdf_art)
    print(f"✓ Executive PDF Flyer: {pdf_proj}")

if __name__ == "__main__":
    generate_image_flyer()
    generate_pdf_flyer()

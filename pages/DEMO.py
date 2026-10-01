"""
================================================================================
STRIDE™ — INTERACTIVE EVALUATOR SANDBOX & BRAND SPONSOR PAVILION
Dedicated Demo Environment | Enterprise Tournament Telemetry
URL Route: /DEMO
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import time
import os
import sys

# Ensure root directory is on sys.path for utils import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils import (
    CBK_DISCIPLINES,
    AttendanceBackend,
    get_eat_now,
    mask_name_banking
)

# ------------------------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="STRIDE™ | Sandbox & Sponsor Showcase",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Backend
backend = AttendanceBackend()

# ------------------------------------------------------------------------------
# DYNAMIC MULTI-THEME ENGINE (DEFAULT: CYBER ULTRAVIOLET & AMETHYST)
# ------------------------------------------------------------------------------
DEMO_THEMES = {
    "cyber_violet": {
        "name": "🔮 Cyber Ultraviolet & Amethyst",
        "tagline": "Futuristic Web3 & Quantum R&D Sandbox",
        "bg_gradient": "radial-gradient(circle at 50% 0%, #280b54 0%, #120326 45%, #06010c 100%)",
        "bg_color": "#06010c",
        "topbar_bg": "linear-gradient(135deg, #1b0636 0%, #370d66 50%, #140226 100%)",
        "primary": "#C084FC",          # Radiant Amethyst Orchid
        "primary_dark": "#9333EA",     # Deep Neon Violet
        "primary_light": "#F0ABFC",    # Lilac Shimmer
        "accent": "#00F5D4",           # Electric Turquoise
        "accent_glow": "#38BDF8",      # Cyber Cyan
        "border": "rgba(192, 132, 252, 0.45)",
        "card_bg": "rgba(24, 9, 48, 0.88)",
        "card_border": "rgba(192, 132, 252, 0.35)",
        "btn_primary": "linear-gradient(135deg, #F472B6 0%, #C084FC 40%, #9333EA 100%)",
        "btn_text": "#FFFFFF",
        "badge_bg": "linear-gradient(135deg, #F0ABFC 0%, #C084FC 50%, #9333EA 100%)",
        "badge_text": "#0F0221",
        "tab_active": "linear-gradient(135deg, rgba(192, 132, 252, 0.35) 0%, rgba(236, 72, 153, 0.25) 100%)",
        "tab_color": "#F0ABFC",
        "shadow_glow": "0 0 25px rgba(192, 132, 252, 0.35)",
    },
    "matrix_emerald": {
        "name": "🌲 Matrix Cyber Emerald",
        "tagline": "High-Tech Biotech & Alpine Mint Matrix",
        "bg_gradient": "radial-gradient(circle at 50% 0%, #062b1a 0%, #03140d 45%, #010805 100%)",
        "bg_color": "#020a06",
        "topbar_bg": "linear-gradient(135deg, #052617 0%, #0b452b 50%, #041c11 100%)",
        "primary": "#34D399",
        "primary_dark": "#059669",
        "primary_light": "#A7F3D0",
        "accent": "#F59E0B",
        "accent_glow": "#FBBF24",
        "border": "rgba(52, 211, 153, 0.45)",
        "card_bg": "rgba(6, 32, 20, 0.88)",
        "card_border": "rgba(52, 211, 153, 0.35)",
        "btn_primary": "linear-gradient(135deg, #6EE7B7 0%, #10B981 40%, #047857 100%)",
        "btn_text": "#021A0F",
        "badge_bg": "linear-gradient(135deg, #A7F3D0 0%, #34D399 50%, #059669 100%)",
        "badge_text": "#021A0F",
        "tab_active": "linear-gradient(135deg, rgba(52, 211, 153, 0.35) 0%, rgba(16, 185, 129, 0.25) 100%)",
        "tab_color": "#A7F3D0",
        "shadow_glow": "0 0 25px rgba(52, 211, 153, 0.35)",
    },
    "solar_crimson": {
        "name": "🔥 Solar Flare Crimson",
        "tagline": "Volcanic Cyberpunk & Radiant Amber",
        "bg_gradient": "radial-gradient(circle at 50% 0%, #360a12 0%, #170408 45%, #080103 100%)",
        "bg_color": "#080103",
        "topbar_bg": "linear-gradient(135deg, #2b080e 0%, #520f1b 50%, #1f050a 100%)",
        "primary": "#FB7185",
        "primary_dark": "#E11D48",
        "primary_light": "#FECDD3",
        "accent": "#F59E0B",
        "accent_glow": "#FBBF24",
        "border": "rgba(251, 113, 133, 0.45)",
        "card_bg": "rgba(35, 8, 14, 0.88)",
        "card_border": "rgba(251, 113, 133, 0.35)",
        "btn_primary": "linear-gradient(135deg, #FDA4AF 0%, #F43F5E 40%, #BE123C 100%)",
        "btn_text": "#FFFFFF",
        "badge_bg": "linear-gradient(135deg, #FECDD3 0%, #FB7185 50%, #E11D48 100%)",
        "badge_text": "#1F0409",
        "tab_active": "linear-gradient(135deg, rgba(244, 63, 94, 0.35) 0%, rgba(249, 115, 22, 0.25) 100%)",
        "tab_color": "#FDA4AF",
        "shadow_glow": "0 0 25px rgba(244, 63, 94, 0.35)",
    },
    "arctic_ice": {
        "name": "🧊 Arctic Glacier Cyan",
        "tagline": "Polar Titanium & Deep Frost Azure",
        "bg_gradient": "radial-gradient(circle at 50% 0%, #0c213b 0%, #061120 45%, #02060d 100%)",
        "bg_color": "#02060d",
        "topbar_bg": "linear-gradient(135deg, #0a1f38 0%, #11355e 50%, #07172b 100%)",
        "primary": "#38BDF8",
        "primary_dark": "#0284C7",
        "primary_light": "#BAE6FD",
        "accent": "#A78BFA",
        "accent_glow": "#C084FC",
        "border": "rgba(56, 189, 248, 0.45)",
        "card_bg": "rgba(8, 26, 48, 0.88)",
        "card_border": "rgba(56, 189, 248, 0.35)",
        "btn_primary": "linear-gradient(135deg, #7DD3FC 0%, #0EA5E9 40%, #0369A1 100%)",
        "btn_text": "#031525",
        "badge_bg": "linear-gradient(135deg, #BAE6FD 0%, #38BDF8 50%, #0284C7 100%)",
        "badge_text": "#031525",
        "tab_active": "linear-gradient(135deg, rgba(56, 189, 248, 0.35) 0%, rgba(14, 165, 233, 0.25) 100%)",
        "tab_color": "#BAE6FD",
        "shadow_glow": "0 0 25px rgba(56, 189, 248, 0.35)",
    }
}

# Determine Active Theme: Query param override or session state (Default: cyber_violet)
qp = st.query_params
qp_theme = qp.get("theme", "").lower()
if qp_theme in DEMO_THEMES:
    st.session_state["demo_theme_key"] = qp_theme

current_theme_key = st.session_state.get("demo_theme_key", "cyber_violet")
th = DEMO_THEMES.get(current_theme_key, DEMO_THEMES["cyber_violet"])

# ------------------------------------------------------------------------------
# HIGH-PRECISION LUXURY THEME CSS (DYNAMIC CYBER ULTRAVIOLET / AMETHYST)
# ------------------------------------------------------------------------------
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');

    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: {th['bg_gradient']} !important;
        background-color: {th['bg_color']} !important;
        color: #FFFFFF !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background: {th['bg_gradient']} !important;
    }}

    [data-testid="stSidebarNav"] {{ display: none !important; }}

    .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 98% !important;
    }}

    /* Topbar styling */
    .demo-topbar {{
        background: {th['topbar_bg']} !important;
        padding: 1.35rem 1.7rem !important;
        border-radius: 18px !important;
        color: #FFFFFF !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.8), {th['shadow_glow']} !important;
        margin-bottom: 1.2rem !important;
        border: 1.5px solid {th['border']} !important;
        border-bottom: 4px solid {th['primary']} !important;
    }}

    /* Streamlit Tabs Navigation Bar */
    div[data-baseweb="tab-list"] {{
        gap: 10px !important;
        background: {th['card_bg']} !important;
        padding: 10px 14px !important;
        border-radius: 16px !important;
        border: 1.5px solid {th['border']} !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), {th['shadow_glow']} !important;
        margin-top: 0.8rem !important;
        margin-bottom: 1.5rem !important;
        display: flex !important;
        flex-wrap: wrap !important;
    }}

    button[data-baseweb="tab"] {{
        border-radius: 10px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        color: #E2E8F0 !important;
        padding: 0.75rem 1.4rem !important;
        background: rgba(12, 5, 25, 0.7) !important;
        border: 1px solid {th['border']} !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    button[data-baseweb="tab"]:hover {{
        color: {th['primary_light']} !important;
        border-color: {th['primary']} !important;
        transform: translateY(-2px) !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        background: {th['tab_active']} !important;
        color: {th['tab_color']} !important;
        font-weight: 800 !important;
        border: 2px solid {th['primary']} !important;
        box-shadow: {th['shadow_glow']} !important;
        transform: translateY(-2px) !important;
    }}

    button[data-baseweb="tab"][aria-selected="true"] * {{
        color: {th['tab_color']} !important;
        font-weight: 800 !important;
    }}

    div[data-baseweb="tab-highlight"] {{
        background: {th['primary']} !important;
        height: 3px !important;
        border-radius: 3px !important;
    }}

    div[data-baseweb="tab-border"] {{ display: none !important; }}

    /* KPI Cards */
    .kpi-card {{
        background: {th['card_bg']} !important;
        border: 1px solid {th['border']} !important;
        border-left: 5px solid {th['primary']} !important;
        border-radius: 12px !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 0.8rem !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5), {th['shadow_glow']} !important;
        transition: all 0.2s ease !important;
    }}

    .kpi-card:hover {{
        transform: translateY(-2px) !important;
        border-color: {th['primary']} !important;
    }}

    .kpi-title {{
        color: #CBD5E1 !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
    }}

    .kpi-value {{
        font-size: 1.85rem !important;
        font-weight: 900 !important;
        margin: 4px 0 !important;
        color: {th['primary_light']} !important;
        text-shadow: 0 0 15px {th['border']} !important;
    }}

    .kpi-sub {{
        color: #94A3B8 !important;
        font-size: 0.75rem !important;
    }}

    /* Buttons */
    .stButton>button[kind="primary"] {{
        background: {th['btn_primary']} !important;
        color: {th['btn_text']} !important;
        font-weight: 900 !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 18px {th['border']} !important;
        transition: all 0.2s ease !important;
    }}

    .stButton>button[kind="primary"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 25px {th['primary']} !important;
    }}

    .stButton>button[kind="secondary"] {{
        background: {th['card_bg']} !important;
        color: {th['primary_light']} !important;
        border: 1.5px solid {th['border']} !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
    }}

    .stButton>button[kind="secondary"]:hover {{
        background: rgba(45, 18, 80, 0.4) !important;
        border-color: {th['primary']} !important;
        color: #FFFFFF !important;
        transform: translateY(-1px) !important;
    }}

    /* Inputs & Selectboxes */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stTextInput input,
    .stSelectbox select {{
        background: rgba(14, 5, 30, 0.95) !important;
        border: 1.5px solid {th['border']} !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
    }}

    div[data-baseweb="select"] svg {{
        fill: {th['primary']} !important;
    }}

    /* Popovers / Dropdowns */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] ul[role="listbox"] {{
        background-color: {th['bg_color']} !important;
        background: {th['bg_color']} !important;
        border: 1.5px solid {th['primary']} !important;
        border-radius: 12px !important;
        box-shadow: 0 15px 40px rgba(0,0,0,0.9), {th['shadow_glow']} !important;
    }}

    div[data-baseweb="popover"] li {{
        background: {th['bg_color']} !important;
        color: #FFFFFF !important;
    }}

    div[data-baseweb="popover"] li:hover {{
        background: {th['primary_dark']} !important;
        color: #FFFFFF !important;
    }}
</style>
""", unsafe_allow_html=True)

now_dt = get_eat_now()

# ------------------------------------------------------------------------------
# 0. 1-CLICK THEME PALETTE SWITCHER BAR
# ------------------------------------------------------------------------------
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem; flex-wrap: wrap; gap: 8px;">
    <div style="font-size: 0.74rem; font-weight: 800; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.8px;">
        🎨 Live Sandbox Theme Palette (Click any to transform instantly):
    </div>
</div>
""", unsafe_allow_html=True)

th_col1, th_col2, th_col3, th_col4 = st.columns(4)
with th_col1:
    if st.button("🔮 Cyber Ultraviolet (Default)", key="btn_th_violet", use_container_width=True, type="primary" if current_theme_key == "cyber_violet" else "secondary"):
        st.session_state["demo_theme_key"] = "cyber_violet"
        st.rerun()
with th_col2:
    if st.button("🌲 Matrix Cyber Emerald", key="btn_th_emerald", use_container_width=True, type="primary" if current_theme_key == "matrix_emerald" else "secondary"):
        st.session_state["demo_theme_key"] = "matrix_emerald"
        st.rerun()
with th_col3:
    if st.button("🔥 Solar Flare Crimson", key="btn_th_crimson", use_container_width=True, type="primary" if current_theme_key == "solar_crimson" else "secondary"):
        st.session_state["demo_theme_key"] = "solar_crimson"
        st.rerun()
with th_col4:
    if st.button("🧊 Arctic Glacier Cyan", key="btn_th_ice", use_container_width=True, type="primary" if current_theme_key == "arctic_ice" else "secondary"):
        st.session_state["demo_theme_key"] = "arctic_ice"
        st.rerun()

# ------------------------------------------------------------------------------
# 1. HEADER & TOP BAR
# ------------------------------------------------------------------------------
st.markdown(f"""
<div class="demo-topbar">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
        <div style="display: flex; align-items: center; gap: 18px;">
            <div style="background: rgba(192, 132, 252, 0.15); border: 2px solid {th['primary']}; border-radius: 12px; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; font-size: 1.9rem; box-shadow: {th['shadow_glow']};">
                🧪
            </div>
            <div>
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="background: {th['badge_bg']}; color: {th['badge_text']}; font-weight: 900; font-size: 0.72rem; padding: 2px 10px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px;">
                        Interactive Sandbox Mode
                    </span>
                    <span style="color: {th['accent']}; font-size: 0.8rem; font-weight: 700;">
                        ● Full Capabilities Unlocked
                    </span>
                    <span style="background: rgba(255,255,255,0.1); color: #E2E8F0; font-size: 0.72rem; padding: 2px 8px; border-radius: 4px;">
                        {th['name']}
                    </span>
                </div>
                <h1 style="margin: 4px 0 0 0; font-size: 1.85rem; font-weight: 900; color: #FFFFFF; letter-spacing: -0.5px;">
                    STRIDE™ <span style="font-weight: 400; color: {th['primary']}; font-size: 1.1rem;">| Evaluator Sandbox & Sponsor Pavilion</span>
                </h1>
                <div style="font-size: 0.8rem; color: #CBD5E1; margin-top: 2px;">
                    Sports Telemetry & Roster Integrity • Enterprise Tournament Management • {th['tagline']}
                </div>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="background: rgba(12, 4, 25, 0.7); border: 1px solid {th['border']}; border-radius: 8px; padding: 6px 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: {th['primary_light']};">
                🕒 {now_dt.strftime('%A, %d %B %Y | %H:%M:%S')} (EAT)
            </div>
            <div style="margin-top: 6px; font-size: 0.76rem; color: #94A3B8;">
                Zero-Risk Sandbox • Production Database Protected
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. EVALUATOR BANNER & OFFICIAL PORTAL RETURN LINK
# ------------------------------------------------------------------------------
c_ban1, c_ban2 = st.columns([3.2, 1.2])
with c_ban1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(192, 132, 252, 0.14) 0%, rgba(0, 245, 212, 0.10) 100%); border: 1.5px solid {th['primary']}; border-radius: 12px; padding: 12px 18px; margin-bottom: 1rem; box-shadow: {th['shadow_glow']};">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.4rem;">💡</span>
            <div>
                <strong style="color: {th['primary_light']}; font-size: 0.92rem;">Welcome to the STRIDE™ Interactive Evaluation Sandbox</strong>
                <p style="margin: 2px 0 0 0; color: #CBD5E1; font-size: 0.82rem;">
                    Test-drive pitchside roll-calls, captain diaries, dual-gate QR check-ins, HR/Finance analytics, and commercial sponsor packages freely with synthetic data.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with c_ban2:
    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display: flex; gap: 8px; flex-direction: column;">
        <a href="/" target="_self" style="display: block; text-decoration: none;">
            <div style="background: {th['card_bg']}; border: 1.5px solid {th['border']}; border-radius: 8px; padding: 7px 10px; text-align: center; color: {th['primary']}; font-weight: 800; font-size: 0.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.4);">
                🏛️ Official CBK Portal
            </div>
        </a>
        <a href="/EVENTS" target="_self" style="display: block; text-decoration: none;">
            <div style="background: rgba(0, 245, 212, 0.12); border: 1.5px solid {th['accent']}; border-radius: 8px; padding: 7px 10px; text-align: center; color: {th['accent']}; font-weight: 800; font-size: 0.8rem;">
                🎟️ STRIDE™ Events & M-Pesa Gateway
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. CORPORATE BRAND PARTNER MARQUEE RIBBON
# ------------------------------------------------------------------------------
st.markdown(f"""
<div style="background: {th['card_bg']}; border: 1.5px solid {th['border']}; border-radius: 12px; padding: 9px 18px; margin-bottom: 1.2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
        <span style="background: {th['badge_bg']}; color: {th['badge_text']}; font-weight: 900; font-size: 0.72rem; padding: 3px 10px; border-radius: 6px; letter-spacing: 0.8px; text-transform: uppercase;">
            🏆 Official Brand Partners
        </span>
        <span style="color: #FFFFFF; font-size: 0.83rem; font-weight: 600;">
            <strong style="color: {th['primary']};">KCB Bank Group</strong> (Title) &bull; <strong style="color: #34D399;">Safaricom M-Pesa</strong> (Fintech) &bull; <strong style="color: {th['accent']};">Britam</strong> (Wellness & Health) &bull; <strong style="color: #F7941D;">Brookside Dairy</strong> (Hydration)
        </span>
    </div>
    <div>
        <span style="font-size: 0.76rem; color: #CBD5E1;">Audience Reach: <strong>18 Disciplines • 1,500+ Corporate Athletes</strong></span>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 4. INTERACTIVE PERSONA & DISCIPLINE SWITCHER
# ------------------------------------------------------------------------------
with st.expander("🎛️ Sandbox Persona & Sporting Discipline Switcher (Click to Customize Demo)", expanded=False):
    st.caption("Switch perspectives on the fly to see how STRIDE™ customizes telemetry for each user type:")
    c_sw1, c_sw2, c_sw3 = st.columns([1.5, 1.5, 1])
    with c_sw1:
        demo_discipline = st.selectbox(
            "Target Sporting Discipline:",
            list(CBK_DISCIPLINES.keys()),
            index=list(CBK_DISCIPLINES.keys()).index("Football (Soccer)") if "Football (Soccer)" in CBK_DISCIPLINES else 0,
            key="demo_sel_disc"
        )
    with c_sw2:
        demo_role = st.selectbox(
            "Simulated Executive Role:",
            [
                "👑 Super Administrator (Full Control)",
                "🏛️ Secretariat Executive (Tournament Governance)",
                "🎖️ Team Captain (Field Operations)",
                "📊 HR Analytics Lead (Staff Telemetry)",
                "💰 Finance & Internal Audit (Payroll Verification)",
                "🤝 Corporate Sponsor / Advertiser"
            ],
            key="demo_sel_role"
        )
    with c_sw3:
        st.write("")
        st.write("")
        if st.button("🔄 Refresh Demo Telemetry", use_container_width=True):
            st.toast("Telemetry refreshed for selected discipline!", icon="🔄")
            st.rerun()

# ------------------------------------------------------------------------------
# 5. ALL 8 FULLY UNLOCKED DEMO TABS
# ------------------------------------------------------------------------------
tab_titles = [
    "📋 Captain's Squad Roll Call",
    "📅 Captain's Tactical Diary",
    "📱 Mobile Check-In",
    "🏷️ Captain QR Station",
    "🎟️ Self-Registration & Ticketing",
    "🏛️ Secretariat Operations",
    "📊 HR Analytics Command",
    "💰 Finance & Audit Portal",
    "🤝 Sponsor Pavilion",
    "⚙️ Sandbox Data Tools"
]

tabs = st.tabs(tab_titles)
tab_dict = {title: tab for title, tab in zip(tab_titles, tabs)}

# ==============================================================================
# TAB 1: CAPTAIN'S SQUAD ROLL CALL (LIVE INTERACTIVE)
# ==============================================================================
with tab_dict["📋 Captain's Squad Roll Call"]:
    st.markdown(f"### 📋 Pitchside Squad Roll Call & Dual-Gate Roster ({demo_discipline})")
    st.caption("1-tap participant verification, automated duration calculation, and instant certified allowance qualification.")

    # Fetch registered players for this discipline
    disc_players = backend.get_players_by_discipline(demo_discipline)
    if not disc_players:
        disc_players = backend.get_players_by_discipline("Football (Soccer)")
    disc_players = sorted(disc_players, key=lambda p: p["full_name"].strip().lower())[:15]

    # Quick Action Simulation Buttons
    c_b1, c_b2, c_b3 = st.columns(3)
    with c_b1:
        if st.button("⚡ Simulate Full Squad Arrival (Gate 1)", use_container_width=True):
            for p in disc_players:
                backend.log_checkin(
                    staff_id=p["staff_id"],
                    full_name=p["full_name"],
                    cbk_email=p.get("cbk_email", ""),
                    department=p["department"],
                    discipline=demo_discipline,
                    gate="GATE 1: ARRIVAL (IN)",
                    station="Main Pitch",
                    notes="SANDBOX_SIMULATOR"
                )
            st.toast("✅ All squad athletes checked into Gate 1!", icon="⚡")
            st.rerun()
    with c_b2:
        if st.button("🎯 Simulate Full Squad Dual-Verified (Gate 2)", use_container_width=True):
            for p in disc_players:
                backend.log_checkin(
                    staff_id=p["staff_id"],
                    full_name=p["full_name"],
                    cbk_email=p.get("cbk_email", ""),
                    department=p["department"],
                    discipline=demo_discipline,
                    gate="GATE 2: DEPARTURE (OUT)",
                    station="Main Pitch",
                    notes="SANDBOX_SIMULATOR"
                )
            st.toast("🎯 All athletes dual-verified! 60-min session certified.", icon="🎯")
            st.rerun()
    with c_b3:
        if st.button("🗑️ Reset Today's Roll Call to 0", use_container_width=True):
            backend.clear_discipline_attendance(demo_discipline)
            st.toast("Attendance telemetry reset for demonstration.", icon="🗑️")
            st.rerun()

    # Roster Table
    st.markdown(f"##### 🏃 Registered {demo_discipline} Squad Roster ({len(disc_players)} Athletes)")
    roster_rows = []
    for p in disc_players:
        today_stat = p.get("today_status", "READY")
        roster_rows.append({
            "Staff ID": p["staff_id"],
            "Full Name": p["full_name"],
            "Department": p["department"],
            "Today Status": "CERTIFIED (KES 2,500)" if today_stat == "DUAL_VERIFIED" else ("ON FIELD (ACTIVE)" if today_stat == "PRE_GATE" else "READY"),
            "Duration (Mins)": p.get("today_duration", 0),
            "Gate Mode": p.get("last_gate", "NONE")
        })
    df_roster = pd.DataFrame(roster_rows)
    st.dataframe(df_roster, use_container_width=True, hide_index=True)

    # Export Button
    st.download_button(
        label=f"📥 Download Certified {demo_discipline} Squad CSV",
        data=df_roster.to_csv(index=False).encode('utf-8'),
        file_name=f"STRIDE_Demo_RollCall_{demo_discipline.split()[0]}_{now_dt.strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==============================================================================
# TAB 2: CAPTAIN'S TACTICAL CALENDAR & DIARY
# ==============================================================================
with tab_dict["📅 Captain's Tactical Diary"]:
    st.markdown(f"### 📅 Captain's Tactical Calendar, Fixtures & Squad Diary ({demo_discipline})")
    st.caption("Discipline-isolated match fixtures, conditioning drills, and coach instructions.")

    cal_events = backend.get_calendar_notes(demo_discipline)

    col_e1, col_e2 = st.columns([1.6, 1.1])
    with col_e1:
        st.markdown(f"##### 📋 Scheduled Fixtures & Squad Diary ({len(cal_events)} Events)")
        if not cal_events:
            st.info(f"No scheduled fixtures recorded for {demo_discipline}. Add one on the right!")
        else:
            for ev in cal_events:
                ev_type = ev.get("event_type", "Drill")
                b_color = th["primary"] if "Tournament" in ev_type else (th["accent"] if "Friendly" in ev_type else "#34D399")
                st.markdown(f"""
                <div style="background: {th['card_bg']}; border-left: 4.5px solid {b_color}; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; border: 1px solid {th['border']};">
                    <span style="color: {b_color}; font-size: 0.75rem; font-weight: 800; text-transform: uppercase;">
                        {ev_type}
                    </span>
                    <h4 style="margin: 4px 0 2px 0; color: #FFF;">{ev.get('title')}</h4>
                    <p style="margin: 0; font-size: 0.8rem; color: #CBD5E1;">
                        🗓️ {ev.get('event_date')} at {ev.get('event_time')} • 📍 {ev.get('venue') or 'Main Pitch'}
                    </p>
                    <div style="margin-top: 6px; font-size: 0.84rem; color: #94A3B8;">
                        📝 <em>{ev.get('notes') or 'No notes.'}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("🗑️ Remove Event", key=f"del_demo_ev_{ev['id']}"):
                    backend.delete_calendar_note(ev['id'])
                    st.rerun()

    with col_e2:
        st.markdown("##### ➕ Schedule Fixture or Tactical Note")
        with st.form(key="form_demo_cal"):
            fd_date = st.date_input("Event Date:")
            fd_time = st.text_input("Kick-off / Start Time:", value="17:00")
            fd_type = st.selectbox("Event Category:", ["🏆 Tournament Fixture", "⚽ Friendly Match", "🏋️ Conditioning Drill", "📋 Tactical Briefing"])
            fd_title = st.text_input("Event Title / Opponent:", placeholder="e.g. Friendly vs Standard Chartered")
            fd_venue = st.text_input("Venue / Station:", value="CBK Sports Club Pitch 1")
            fd_notes = st.text_area("Tactical Notes:", placeholder="Full match kit required...")
            if st.form_submit_button("💾 Save to Squad Calendar", use_container_width=True):
                if fd_title.strip():
                    backend.add_calendar_note(demo_discipline, fd_date.strftime("%Y-%m-%d"), fd_time, fd_type, fd_title, fd_notes, fd_venue, "Demo Captain")
                    st.toast("✅ Fixture added to squad calendar!", icon="📅")
                    st.rerun()

# ==============================================================================
# TAB 3: PARTICIPANT MOBILE CHECK-IN SIMULATOR
# ==============================================================================
with tab_dict["📱 Mobile Check-In"]:
    st.markdown("### 📱 Participant Mobile Check-In & Digital Boarding Pass")
    st.caption("Demonstration of the athlete smartphone lookup and cryptographic allowance ticket.")

    m_col1, m_col2 = st.columns([1.2, 1.6])
    with m_col1:
        st.markdown("##### 🔍 Athlete Lookup")
        test_sid = st.text_input("Enter Staff ID / Payroll #:", value="CBK-10009", key="demo_m_sid")
        p_match = backend.get_staff_by_id(test_sid.strip())

        if p_match:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {th['bg_color']} 0%, {th['primary_dark']} 100%); border: 1.5px solid {th['border']}; border-radius: 12px; padding: 16px; margin-top: 10px; box-shadow: {th['shadow_glow']};">
                <span style="background: {th['badge_bg']}; color: {th['badge_text']}; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 800;">VERIFIED ATHLETE</span>
                <h3 style="margin: 8px 0 2px 0; color: #FFF;">{p_match['full_name']}</h3>
                <p style="margin: 0; color: #CBD5E1; font-size: 0.85rem;">{p_match['department']} • {p_match.get('primary_sport', demo_discipline)}</p>
                <div style="margin-top: 10px; font-size: 0.8rem; color: {th['accent']}; font-weight: 700;">
                    ● ALLOWANCE ELIGIBLE (KES 2,500 FLOOR)
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✅ Confirm Gate 1 Arrival Scan", key="btn_demo_g1", type="primary", use_container_width=True):
                backend.log_checkin(
                    staff_id=p_match["staff_id"],
                    full_name=p_match["full_name"],
                    cbk_email=p_match.get("cbk_email", ""),
                    department=p_match["department"],
                    discipline=p_match.get("primary_sport", demo_discipline),
                    gate="GATE 1: ARRIVAL (IN)",
                    station="Demo Station",
                    notes="MOBILE_SIMULATOR"
                )
                st.balloons()
                st.toast("Gate 1 scan confirmed!", icon="✅")
                st.rerun()
        else:
            st.warning("Try typing: CBK-10009, CBK-10248, CBK-3428, or 1024")

    with m_col2:
        st.markdown("##### 🎟️ Digital Mobile Pass Preview")
        st.markdown(f"""
        <div style="background: {th['card_bg']}; border: 2px dashed {th['border']}; border-radius: 14px; padding: 20px; text-align: center; box-shadow: {th['shadow_glow']};">
            <div style="font-size: 0.76rem; color: {th['primary']}; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">STRIDE™ Enterprise Sports Network</div>
            <h4 style="margin: 6px 0; color: #FFF;">OFFICIAL TOURNAMENT PARTICIPATION PASS</h4>
            <div style="font-size: 2.5rem; margin: 10px 0;">📱</div>
            <div style="background: rgba(0, 245, 212, 0.12); border: 1px solid {th['accent']}; border-radius: 8px; padding: 8px; margin-bottom: 10px;">
                <span style="color: {th['accent']}; font-weight: 800; font-size: 0.9rem;">VERIFIED SESSION RATE: KES 2,500</span><br>
                <span style="color: #94A3B8; font-size: 0.75rem;">Requires Dual-Gate Scan & 45-Minute Activity Floor</span>
            </div>
            <div style="font-size: 0.78rem; color: #64748B;">Cryptographically timestamped • Kenya Data Protection Act 2019 Compliant</div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 4: CAPTAIN QR STATION
# ==============================================================================
with tab_dict["🏷️ Captain QR Station"]:
    st.markdown(f"### 🏷️ Captain Pitchside Dynamic QR Station ({demo_discipline})")
    st.caption("Large kiosk QR code for field tablets. Point your smartphone camera to scan.")

    q_col1, q_col2 = st.columns([1.5, 1.2])
    with q_col1:
        qr_mode = st.radio("Select Active Verification Gate:", ["GATE 1: ARRIVAL (IN)", "GATE 2: DEPARTURE (OUT)"], horizontal=True)
        st.markdown(f"""
        <div style="background: {th['card_bg']}; border: 2px solid {th['primary']}; border-radius: 14px; padding: 22px; text-align: center; margin-top: 12px; box-shadow: {th['shadow_glow']};">
            <span style="background: {th['badge_bg']}; color: {th['badge_text']}; font-weight: 900; font-size: 0.78rem; padding: 3px 12px; border-radius: 6px;">
                {qr_mode}
            </span>
            <h3 style="margin: 10px 0 4px 0; color: #FFF;">{demo_discipline} Check-In Point</h3>
            <p style="margin: 0 0 16px 0; color: #94A3B8; font-size: 0.85rem;">Display on Captain's official tablet at pitch entrance</p>
            <div style="background: #FFFFFF; display: inline-block; padding: 18px; border-radius: 14px; box-shadow: {th['shadow_glow']};">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=https://cbk-stride.streamlit.app/" alt="Station QR Code" style="display: block; width: 220px; height: 220px;" />
            </div>
            <div style="margin-top: 14px; font-size: 0.8rem; color: {th['accent']}; font-weight: 700;">
                ● Live Station Ready for Scans
            </div>
        </div>
        """, unsafe_allow_html=True)
    with q_col2:
        st.markdown("##### ℹ️ Operational Protocol")
        st.markdown("""
        1. **Arrival Scan (Gate 1):** Athletes point smartphone cameras at this tablet upon entering the sports venue.
        2. **Field Activity:** Athlete participates in the designated discipline training session or tournament fixture.
        3. **Departure Scan (Gate 2):** Captain flips toggle to Gate 2. Athletes scan out before leaving.
        4. **Automatic Compliance:** System automatically calculates elapsed session duration. Sessions ≥ 45 minutes achieve **Dual-Verified (Certified)** status.
        """)

# ==============================================================================
# TAB: SELF-REGISTRATION & TICKETING SHOWCASE (M-PESA STK INTEGRATION)
# ==============================================================================
with tab_dict["🎟️ Self-Registration & Ticketing"]:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0A2540 0%, #061527 100%); border: 1.5px solid rgba(0, 242, 254, 0.4); border-left: 5px solid #00F2FE; border-radius: 14px; padding: 18px 22px; margin-bottom: 1.5rem; box-shadow: 0 8px 30px rgba(0,0,0,0.45);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%); color: #040E1C; font-weight: 900; font-size: 0.72rem; padding: 3px 10px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.8px;">COMMERCIAL SAAS ENGINE</span>
                <h2 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.5rem; font-weight: 900;">🎟️ Public Self-Registration, M-Pesa STK Ticketing & Functions Gateway</h2>
                <p style="margin: 0; color: #94A3B8; font-size: 0.88rem;">
                    How external organizations monetize and manage rosters across <strong>Sports Derbies, Corporate AGMs, Conferences, Dinners, and Marathons</strong>.
                </p>
            </div>
            <div style="text-align: right;">
                <span style="background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid #10B981; padding: 4px 12px; border-radius: 20px; font-size: 0.78rem; font-weight: 800;">
                    🟢 Safaricom Daraja API Ready
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Commercial Value Highlights
    h_col1, h_col2, h_col3, h_col4 = st.columns(4)
    with h_col1:
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #00F2FE;">
            <div class="kpi-title">Zero Special Hardware</div>
            <div class="kpi-value" style="color: #00F2FE; font-size: 1.3rem;">100% Mobile</div>
            <div class="kpi-sub">Attendees use phone, ushers scan with phone cameras</div>
        </div>
        """, unsafe_allow_html=True)
    with h_col2:
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #34D399;">
            <div class="kpi-title">M-Pesa STK Push</div>
            <div class="kpi-value" style="color: #34D399; font-size: 1.3rem;">&lt; 10 Seconds</div>
            <div class="kpi-sub">Instant prompt on customer phone, zero manual reference entry</div>
        </div>
        """, unsafe_allow_html=True)
    with h_col3:
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #F5C542;">
            <div class="kpi-title">Universal Functions</div>
            <div class="kpi-value" style="color: #F5C542; font-size: 1.3rem;">Any Event</div>
            <div class="kpi-sub">AGMs, Galas, Derbies, Marathons, Conferences, Weddings</div>
        </div>
        """, unsafe_allow_html=True)
    with h_col4:
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #A78BFA;">
            <div class="kpi-title">Anti-Counterfeit QR</div>
            <div class="kpi-value" style="color: #A78BFA; font-size: 1.3rem;">Single-Use</div>
            <div class="kpi-sub">Instant duplicate pass detection prevents scalping & pass-sharing</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧪 Live Interactive Simulation: Register, Pay via M-Pesa & Scan In")
    st.caption("Test the complete attendee journey: fill the self-registration form below, trigger an instant M-Pesa STK push simulation, receive your encrypted QR pass, and simulate gate verification:")

    reg_col1, reg_col2 = st.columns([1.2, 1])

    with reg_col1:
        st.markdown("#### 📝 Step 1: Attendee Self-Registration")
        event_chosen = st.selectbox(
            "Select Event / Function:*",
            [
                "🏆 2026 Inter-Bank Sports Championship (Nairobi)",
                "👔 Annual General Meeting (AGM) & Stakeholder Dinner",
                "🏃 Great Rift Valley 10K Charity Marathon & Family Fun Day",
                "💡 Africa Fintech & Banking Innovation Summit 2026",
                "🎉 Corporate End-of-Year Gala & Awards Night"
            ],
            key="demo_ticket_event"
        )

        ticket_tier = st.selectbox(
            "Select Ticket / Roster Tier:*",
            [
                "Standard Participant / Athlete Pass — KES 1,000",
                "VIP Executive / Delegate Pass (Includes Hospitality) — KES 3,500",
                "Corporate Team Bundle (Squad of 15) — KES 12,500",
                "Guest / Spectator Entry Pass — KES 500"
            ],
            key="demo_ticket_tier"
        )

        tier_price_map = {
            "Standard Participant / Athlete Pass — KES 1,000": 1000,
            "VIP Executive / Delegate Pass (Includes Hospitality) — KES 3,500": 3500,
            "Corporate Team Bundle (Squad of 15) — KES 12,500": 12500,
            "Guest / Spectator Entry Pass — KES 500": 500
        }
        ticket_amount = tier_price_map.get(ticket_tier, 1000)

        f_name = st.text_input("Full Name:*", value="Wallace Mbugua", key="demo_tick_name")
        f_email = st.text_input("Email Address:*", value="wallace.mbugua@enterprise.co.ke", key="demo_tick_email")
        f_org = st.text_input("Company / Organization / Branch:*", value="Finance & Accounts Division", key="demo_tick_org")
        f_phone = st.text_input("Safaricom M-Pesa Phone Number:*", value="0712345678", help="Format: 07XX or 2547XX", key="demo_tick_phone")

        btn_pay_mpesa = st.button("📲 Pay with M-Pesa STK Push", type="primary", use_container_width=True)

        if btn_pay_mpesa:
            clean_phone = f_phone.strip()
            if not f_name.strip():
                st.error("Please provide your Full Name.")
            elif not clean_phone or len(clean_phone) < 9:
                st.error("Please provide a valid Safaricom phone number for STK Push.")
            else:
                st.session_state["ticket_reg_success"] = True
                st.session_state["ticket_attendee_name"] = f_name.strip()
                st.session_state["ticket_attendee_org"] = f_org.strip()
                st.session_state["ticket_event"] = event_chosen
                st.session_state["ticket_tier_name"] = ticket_tier.split("—")[0].strip()
                st.session_state["ticket_amount"] = ticket_amount
                st.session_state["ticket_phone"] = clean_phone
                st.session_state["ticket_trans_id"] = f"QK{int(time.time())}"[-10:]
                st.session_state["ticket_gate_scanned"] = False
                st.rerun()

    with reg_col2:
        st.markdown("#### 📱 Step 2: Instant Ticket Pass & Verification")
        if not st.session_state.get("ticket_reg_success", False):
            st.info("👈 Fill out the registration form on the left and tap **'Pay with M-Pesa STK Push'** to generate an instant QR pass.")
            st.markdown("""
            <div style="background: rgba(8, 24, 48, 0.6); border: 2px dashed rgba(255,255,255,0.15); border-radius: 12px; padding: 30px; text-align: center; color: #64748B;">
                <div style="font-size: 3rem; margin-bottom: 10px;">🎟️</div>
                <div style="font-weight: 700; color: #94A3B8;">Awaiting Attendee Registration...</div>
                <div style="font-size: 0.8rem; margin-top: 6px;">Upon checkout, the digital pass is dynamically generated and sent to the attendee's phone/WhatsApp.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            att_name = st.session_state.get("ticket_attendee_name", "Wallace Mbugua")
            att_org = st.session_state.get("ticket_attendee_org", "Enterprise Corp")
            ev_name = st.session_state.get("ticket_event", "Corporate Championship")
            t_tier = st.session_state.get("ticket_tier_name", "Standard Pass")
            t_amt = st.session_state.get("ticket_amount", 1000)
            t_phone = st.session_state.get("ticket_phone", "0712345678")
            t_tx = st.session_state.get("ticket_trans_id", "QK92837194")
            
            # STK Push Success Notification
            st.success(f"📲 **M-Pesa STK Push Completed!** Confirmed KES {t_amt:,} from {t_phone}. Trans ID: `{t_tx}`.")

            # Dynamic QR Pass Card
            qr_data = f"STRIDE_TICKET:{t_tx}:{att_name}:{ev_name[:20]}"
            qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={qr_data}"

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {th['bg_color']} 0%, {th['primary_dark']} 100%); border: 2px solid {th['primary']}; border-radius: 14px; padding: 18px; box-shadow: {th['shadow_glow']}; text-align: center;">
                <div style="font-size: 0.72rem; color: {th['primary_light']}; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase;">STRIDE™ ENTERPRISE DIGITAL PASS</div>
                <h3 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.15rem; font-weight: 800;">{ev_name}</h3>
                <span style="background: rgba(0, 245, 212, 0.2); color: {th['accent']}; border: 1px solid rgba(0,245,212,0.4); padding: 2px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">
                    {t_tier}
                </span>
                
                <div style="background: #FFFFFF; border-radius: 10px; padding: 10px; display: inline-block; margin: 14px 0 8px 0; box-shadow: 0 4px 12px rgba(0,0,0,0.4);">
                    <img src="{qr_url}" alt="Ticket QR" style="display: block; width: 150px; height: 150px;" />
                </div>
                
                <h4 style="margin: 2px 0; color: #FFFFFF; font-size: 1.1rem;">{att_name}</h4>
                <div style="font-size: 0.8rem; color: #94A3B8;">{att_org}</div>
                
                <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; border-radius: 8px; padding: 6px 12px; margin-top: 10px; font-size: 0.78rem; color: #34D399; font-weight: 700;">
                    ✓ M-PESA CONFIRMED • KES {t_amt:,} • REF: {t_tx}
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("#### 🚪 Step 3: Gate Usher Scanner Simulator")
            st.caption("When this attendee arrives at the venue gate, the usher points their smartphone camera at the pass above:")

            scanned = st.session_state.get("ticket_gate_scanned", False)
            if not scanned:
                if st.button("📷 Simulate Usher Scanning This Pass at Entrance", type="secondary", use_container_width=True):
                    st.session_state["ticket_gate_scanned"] = True
                    st.session_state["ticket_scan_time"] = get_eat_now().strftime("%H:%M:%S")
                    st.rerun()
            else:
                scan_t = st.session_state.get("ticket_scan_time", "Now")
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.2); border: 2px solid #10B981; border-radius: 10px; padding: 14px; text-align: center;">
                    <div style="font-size: 1.8rem;">✅</div>
                    <strong style="color: #34D399; font-size: 1rem;">TICKET VERIFIED & ADMITTED!</strong>
                    <div style="color: #E2E8F0; font-size: 0.85rem; margin-top: 4px;">
                        Welcome <strong>{att_name}</strong> • Gate 1 Main Entrance<br>
                        <span style="font-size: 0.75rem; color: #94A3B8;">Check-in Timestamp: {scan_t} EAT • Status: ADMITTED</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.caption("🔒 **Anti-Pass-Sharing Test:** If someone takes a screenshot and tries to scan the same ticket again:")
                if st.button("⚠️ Attempt Re-scanning Same Ticket (Duplicate Prevention Test)", use_container_width=True):
                    st.error(f"🛑 REJECTED: TICKET ALREADY USED AT {scan_t} EAT! Duplicate entry prevented.")

            if st.button("🔄 Reset Simulator & Register Another Attendee", use_container_width=True):
                st.session_state["ticket_reg_success"] = False
                st.session_state["ticket_gate_scanned"] = False
                st.rerun()

# ==============================================================================
# TAB 6: SECRETARIAT OPERATIONS DASHBOARD
# ==============================================================================
with tab_dict["🏛️ Secretariat Operations"]:
    st.markdown("### 🏛️ Secretariat Operations & Tournament Control Command")
    st.caption("Live monitoring of real-time check-ins, discipline activity, and dual-gate fulfillment across all 18 sports.")

    # 4 KPI Cards
    sk1, sk2, sk3, sk4 = st.columns(4)
    with sk1:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: {th['primary']};">
            <div class="kpi-title">Today's Scans</div>
            <div class="kpi-value" style="color: {th['primary_light']};">342</div>
            <div class="kpi-sub">Across All 18 Sports</div>
        </div>
        """, unsafe_allow_html=True)
    with sk2:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: {th['accent']};">
            <div class="kpi-title">Active on Field</div>
            <div class="kpi-value" style="color: {th['accent']};">58</div>
            <div class="kpi-sub">Awaiting Gate 2 Departure</div>
        </div>
        """, unsafe_allow_html=True)
    with sk3:
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #10B981;">
            <div class="kpi-title">Dual-Verified Units</div>
            <div class="kpi-value" style="color: #10B981;">284</div>
            <div class="kpi-sub">Certified for KES 2,500 Allowance</div>
        </div>
        """, unsafe_allow_html=True)
    with sk4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: {th['primary_dark']};">
            <div class="kpi-title">Policy Compliance</div>
            <div class="kpi-value" style="color: {th['primary_light']};">98.4%</div>
            <div class="kpi-sub">0 Short Sessions Flagged</div>
        </div>
        """, unsafe_allow_html=True)

    # 18-Sport Matrix Overview
    st.markdown("##### 🏃 18 Sporting Disciplines Status Matrix")
    matrix_data = []
    for sport in sorted(list(CBK_DISCIPLINES.keys())):
        matrix_data.append({
            "Sport": sport,
            "Venue": CBK_DISCIPLINES[sport]["default_venue"],
            "Squad Size": 24,
            "Today's Scans": 18,
            "Dual-Verified": 16,
            "Status": "🟢 ACTIVE SESSION"
        })
    df_matrix = pd.DataFrame(matrix_data)
    st.dataframe(df_matrix, use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 6: HR ANALYTICS COMMAND
# ==============================================================================
with tab_dict["📊 HR Analytics Command"]:
    st.markdown("### 📊 Human Resources Wellness & Athletic Analytics")
    st.caption("Departmental athletic participation, health wellness indicators, and staff engagement telemetry.")

    hr_c1, hr_c2 = st.columns(2)
    with hr_c1:
        st.markdown("##### 🏢 Participation by Bank Department")
        dept_data = pd.DataFrame({
            "Department": ["Banking & Currency Operations", "Financial Markets", "Bank Supervision", "IT & Digital Services", "Human Resources", "Legal & Secretariat"],
            "Athletes": [48, 42, 39, 35, 28, 24]
        })
        st.bar_chart(dept_data.set_index("Department"), color=th["primary"])

    with hr_c2:
        st.markdown("##### 🏆 Inter-Departmental Sports Engagement Rankings")
        st.dataframe(dept_data.assign(Participation_Rate=["92.4%", "88.6%", "85.2%", "81.0%", "78.4%", "74.2%"]), use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 7: FINANCE & AUDIT PORTAL
# ==============================================================================
with tab_dict["💰 Finance & Audit Portal"]:
    st.markdown("### 💰 Finance & Internal Audit Disbursement Reconciliation")
    st.caption("Cryptographically certified per diem disbursement schedules. Zero payments without verified 45-minute dual-gate compliance.")

    f_k1, f_k2, f_k3 = st.columns(3)
    with f_k1:
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #10B981;">
            <div class="kpi-title">Certified Allowance Payable</div>
            <div class="kpi-value" style="color: #10B981;">KES 710,000</div>
            <div class="kpi-sub">284 Qualified Units @ KES 2,500</div>
        </div>
        """, unsafe_allow_html=True)
    with f_k2:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: {th['accent']};">
            <div class="kpi-title">Prevented Phantom Payouts</div>
            <div class="kpi-value" style="color: {th['accent']};">KES 145,000</div>
            <div class="kpi-sub">58 Incomplete Single-Gate Scans Disallowed</div>
        </div>
        """, unsafe_allow_html=True)
    with f_k3:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: {th['primary']};">
            <div class="kpi-title">Audit Trail Integrity</div>
            <div class="kpi-value" style="color: {th['primary_light']};">100.0%</div>
            <div class="kpi-sub">Zero Forged Paper Sign-Offs</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("##### 📑 Certified Financial Disbursement Schedule")
    demo_fin_rows = [
        {"Payroll #": "CBK-10009", "Full Name": "Ramtu Abdallah", "Department": "Mombasa Branch", "Sport": "Football", "Session Date": now_dt.strftime("%Y-%m-%d"), "Duration": "65 Mins", "Status": "DUAL_VERIFIED", "Allowance Payable": "KES 2,500"},
        {"Payroll #": "CBK-10248", "Full Name": "Boniface Thuo", "Department": "Meru Currency Centre", "Sport": "Football", "Session Date": now_dt.strftime("%Y-%m-%d"), "Duration": "72 Mins", "Status": "DUAL_VERIFIED", "Allowance Payable": "KES 2,500"},
        {"Payroll #": "CBK-3428", "Full Name": "Samuel Gathigi", "Department": "IT Services", "Sport": "Golf", "Session Date": now_dt.strftime("%Y-%m-%d"), "Duration": "180 Mins", "Status": "DUAL_VERIFIED", "Allowance Payable": "KES 2,500"},
        {"Payroll #": "CBK-1014", "Full Name": "Faith Mwende", "Department": "Financial Markets", "Sport": "Athletics", "Session Date": now_dt.strftime("%Y-%m-%d"), "Duration": "50 Mins", "Status": "DUAL_VERIFIED", "Allowance Payable": "KES 2,500"},
        {"Payroll #": "CBK-1033", "Full Name": "Dennis Kiprono", "Department": "Supervision", "Sport": "Basketball", "Session Date": now_dt.strftime("%Y-%m-%d"), "Duration": "60 Mins", "Status": "DUAL_VERIFIED", "Allowance Payable": "KES 2,500"}
    ]
    df_fin = pd.DataFrame(demo_fin_rows)
    st.dataframe(df_fin, use_container_width=True, hide_index=True)

    st.download_button(
        label="📥 Download Certified Finance Disbursement Schedule (.CSV)",
        data=df_fin.to_csv(index=False).encode('utf-8'),
        file_name=f"STRIDE_Certified_Allowance_Schedule_{now_dt.strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==============================================================================
# TAB 8: CORPORATE SPONSOR PAVILION & BRAND SHOWCASE
# ==============================================================================
with tab_dict["🤝 Sponsor Pavilion"]:
    st.markdown("### 🤝 Corporate Brand Pavilion & Sponsorship Showcase")
    st.caption("Commercial partnership opportunities, high-impact brand visibility, and tournament engagement across the corporate sports ecosystem.")

    # Commercial Reach KPIs
    sp_k1, sp_k2, sp_k3, sp_k4 = st.columns(4)
    with sp_k1:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: {th['primary']};">
            <div class="kpi-title">Active Sporting Disciplines</div>
            <div class="kpi-value" style="color: {th['primary_light']};">18 Sports</div>
            <div class="kpi-sub">Golf, Football, Athletics & More</div>
        </div>
        """, unsafe_allow_html=True)
    with sp_k2:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: {th['accent']};">
            <div class="kpi-title">Audience & Athletes</div>
            <div class="kpi-value" style="color: {th['accent']};">1,500+</div>
            <div class="kpi-sub">Bank Staff, C-Suite & Competitors</div>
        </div>
        """, unsafe_allow_html=True)
    with sp_k3:
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #10B981;">
            <div class="kpi-title">Tournament Scans</div>
            <div class="kpi-value" style="color: #10B981;">25,000+</div>
            <div class="kpi-sub">100% Mobile QR Engagements</div>
        </div>
        """, unsafe_allow_html=True)
    with sp_k4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: {th['primary_dark']};">
            <div class="kpi-title">Brand Exposure ROI</div>
            <div class="kpi-value" style="color: {th['primary_light']};">99.8%</div>
            <div class="kpi-sub">Real-Time Digital & Field Touchpoints</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Official Brand Partners
    st.markdown("#### 🏆 Official Corporate Brand Partners")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown(f"""
        <div style="background: {th['card_bg']}; border: 1.5px solid {th['border']}; border-radius: 12px; padding: 18px; margin-bottom: 14px; box-shadow: {th['shadow_glow']};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: {th['accent']}; font-size: 1.15rem; font-weight: 800;">🦁 KCB Bank Group</h4>
                <span style="background: rgba(0, 245, 212, 0.2); color: {th['accent']}; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">Platinum Partner</span>
            </div>
            <p style="margin: 8px 0 4px 0; font-size: 0.88rem; color: #E2E8F0;">
                <strong>Official Banking & Financial Services Partner</strong> of the STRIDE™ Corporate Championship.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: {th['card_bg']}; border: 1.5px solid {th['border']}; border-radius: 12px; padding: 18px; margin-bottom: 14px; box-shadow: {th['shadow_glow']};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: {th['primary']}; font-size: 1.15rem; font-weight: 800;">🛡️ Britam Holdings</h4>
                <span style="background: rgba(192, 132, 252, 0.2); color: {th['primary']}; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">Wellness Underwriter</span>
            </div>
            <p style="margin: 8px 0 4px 0; font-size: 0.88rem; color: #E2E8F0;">
                <strong>Official Sports Injury, Health & Wellness Underwriter</strong> for all tournament athletes.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with p_col2:
        st.markdown(f"""
        <div style="background: {th['card_bg']}; border: 1.5px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 18px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #10B981; font-size: 1.15rem; font-weight: 800;">📱 Safaricom M-Pesa</h4>
                <span style="background: rgba(16, 185, 129, 0.2); color: #10B981; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">Tech Innovation</span>
            </div>
            <p style="margin: 8px 0 4px 0; font-size: 0.88rem; color: #E2E8F0;">
                <strong>Official Digital Payments & Connectivity Partner</strong> powering cashless tournament zones.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background: {th['card_bg']}; border: 1.5px solid {th['border']}; border-radius: 12px; padding: 18px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: {th['primary_light']}; font-size: 1.15rem; font-weight: 800;">🥛 Brookside Dairy</h4>
                <span style="background: rgba(192, 132, 252, 0.2); color: {th['primary_light']}; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">Nutrition Partner</span>
            </div>
            <p style="margin: 8px 0 4px 0; font-size: 0.88rem; color: #E2E8F0;">
                <strong>Official Nutrition & Athlete Hydration Partner</strong> across all 18 sporting venues.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Sponsorship Tiers Matrix
    st.markdown("#### 💎 Corporate Sponsorship Packages & Advertising Tiers")
    t1, t2, t3, t4 = st.columns(4)
    with t1:
        st.markdown(f"""
        <div style="background: {th['card_bg']}; border: 2px solid {th['primary']}; border-radius: 12px; padding: 16px; height: 100%; box-shadow: {th['shadow_glow']};">
            <div style="text-align: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem;">🥇</span>
                <h4 style="margin: 2px 0; color: {th['primary']};">PLATINUM TITLE</h4>
                <div style="font-size: 1.05rem; font-weight: 900; color: #FFF;">KES 2,500,000</div>
            </div>
            <ul style="font-size: 0.78rem; color: #CBD5E1; padding-left: 16px; line-height: 1.5;">
                <li>Header Ribbon branding across entire portal</li>
                <li>Main Stadium perimeter & board</li>
                <li>Championship trophy naming rights</li>
                <li>VIP Executive hospitality tent</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown(f"""
        <div style="background: {th['card_bg']}; border: 2px solid {th['accent']}; border-radius: 12px; padding: 16px; height: 100%;">
            <div style="text-align: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem;">🥈</span>
                <h4 style="margin: 2px 0; color: {th['accent']};">GOLD DISCIPLINE</h4>
                <div style="font-size: 1.05rem; font-weight: 900; color: #FFF;">KES 1,200,000</div>
            </div>
            <ul style="font-size: 0.78rem; color: #CBD5E1; padding-left: 16px; line-height: 1.5;">
                <li>Exclusive naming for 1 sport (Golf/Football)</li>
                <li>Squad jersey chest branding</li>
                <li>Captain Roll Call station endorsement</li>
                <li>Pitchside display boards</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown(f"""
        <div style="background: {th['card_bg']}; border: 2px solid #10B981; border-radius: 12px; padding: 16px; height: 100%;">
            <div style="text-align: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem;">🥉</span>
                <h4 style="margin: 2px 0; color: #10B981;">SILVER WELLNESS</h4>
                <div style="font-size: 1.05rem; font-weight: 900; color: #FFF;">KES 600,000</div>
            </div>
            <ul style="font-size: 0.78rem; color: #CBD5E1; padding-left: 16px; line-height: 1.5;">
                <li>Training bibs & kit co-branding</li>
                <li>Hydration station flags</li>
                <li>Athlete recovery lounge banner</li>
                <li>Digital schedule inclusion</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with t4:
        st.markdown(f"""
        <div style="background: {th['card_bg']}; border: 2px solid {th['primary_dark']}; border-radius: 12px; padding: 16px; height: 100%;">
            <div style="text-align: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem;">🎖️</span>
                <h4 style="margin: 2px 0; color: {th['primary_light']};">BRONZE DIGITAL</h4>
                <div style="font-size: 1.05rem; font-weight: 900; color: #FFF;">KES 250,000</div>
            </div>
            <ul style="font-size: 0.78rem; color: #CBD5E1; padding-left: 16px; line-height: 1.5;">
                <li>Digital directory showcase listing</li>
                <li>Tournament handbook 1-page profile</li>
                <li>Fan zone spectator banner</li>
                <li>Official donor recognition</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Inquiry Form
    c_df1, c_df2 = st.columns([1.4, 1.0])
    with c_df1:
        st.markdown("#### 📝 Register Corporate Sponsorship / Brand Advertising")
        with st.form(key="form_demo_sponsor"):
            s_org = st.text_input("Brand / Company Name:*", placeholder="e.g. Standard Chartered Bank")
            s_name = st.text_input("Contact Person & Title:*", placeholder="e.g. Jane Mutua (Head of Marketing)")
            s_email = st.text_input("Official Email Address:*", placeholder="e.g. jmutua@brand.co.ke")
            s_phone = st.text_input("Phone Number:", placeholder="e.g. +254 700 123 456")
            s_tier = st.selectbox("Preferred Sponsorship Package:", ["🥇 Platinum Title Partner (KES 2.5M)", "🥈 Gold Discipline Partner (KES 1.2M)", "🥉 Silver Wellness Partner (KES 600K)", "🎖️ Bronze Digital Partner (KES 250K)"])
            s_notes = st.text_area("Marketing Objectives:", placeholder="Target demographics...")
            if st.form_submit_button("🚀 Submit Corporate Partnership Inquiry", use_container_width=True):
                if s_org.strip() and s_name.strip() and s_email.strip():
                    backend.record_sponsor_inquiry(s_org, s_name, s_email, s_phone, s_tier.split(" (")[0], demo_discipline, s_notes)
                    st.balloons()
                    st.success(f"🎉 Inquiry registered for {s_org}! Our commercial directorate will reach out.")
                    st.rerun()

    with c_df2:
        st.markdown("#### 📞 Direct Secretariat Contacts")
        st.markdown(f"""
        <div style="background: {th['card_bg']}; border: 1px solid {th['border']}; border-radius: 12px; padding: 18px; box-shadow: {th['shadow_glow']};">
            <h5 style="margin: 0 0 6px 0; color: {th['primary']};">STRIDE™ Enterprise Operations</h5>
            <p style="margin: 0 0 8px 0; font-size: 0.85rem; color: #CBD5E1;">
                Secretariat & Commercial Sponsorship Directorate<br>
                Corporate Sports Complex, Nairobi, Kenya
            </p>
            <div style="font-size: 0.84rem; color: #94A3B8; line-height: 1.6;">
                📧 <strong>Email:</strong> <span style="color: {th['accent']};">partnerships@stride-enterprise.io</span><br>
                📞 <strong>Direct Line:</strong> +254 (020) 286 1000<br>
                🕒 <strong>Office Hours:</strong> Monday – Friday: 08:00 – 17:00 EAT
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# TAB 9: SANDBOX SETTINGS & DATA TOOLS
# ==============================================================================
with tab_dict["⚙️ Sandbox Data Tools"]:
    st.markdown("### ⚙️ Sandbox Data Controls & Demonstration Tools")
    st.caption("Safely reset telemetry, inspect synthetic data tables, or test administrative capabilities:")

    cs1, cs2 = st.columns(2)
    with cs1:
        if st.button("🔄 Re-Seed Synthetic Demo Data (32+ Records)", use_container_width=True):
            backend.seed_demo_data()
            st.success("Re-seeded synthetic demonstration telemetry across all 18 disciplines!")
            st.rerun()
    with cs2:
        if st.button("🗑️ Purge Synthetic Attendance Scans to 0", use_container_width=True):
            backend.clear_all_attendance()
            st.toast("Synthetic attendance logs cleared to zero.", icon="🗑️")
            st.rerun()

# ------------------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------------------
st.markdown(f"""
<div style="text-align: center; margin-top: 2.5rem; padding: 1.4rem; border-top: 1px solid {th['border']}; color: #94A3B8; font-size: 0.82rem; background: {th['card_bg']}; border-radius: 12px; box-shadow: {th['shadow_glow']};">
    <strong style="color: {th['primary']};">STRIDE™</strong> • Interactive Evaluation Sandbox & Corporate Sponsor Pavilion<br>
    <span style="font-size: 0.75rem; color: #64748B;">Enterprise Sports Telemetry & Tournament Operations • <a href="/" style="color: {th['accent']}; text-decoration: none;">Return to Official CBK Portal</a> • <a href="/EVENTS" style="color: {th['primary']}; text-decoration: none;">🎟️ STRIDE™ Events & Ticketing</a></span>
</div>
""", unsafe_allow_html=True)

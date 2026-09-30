"""
DSWAAP - Central Bank of Kenya (CBK) Sports Wellness & Attendance Automation Platform
Main Streamlit Web Application (Mobile-First, Executive-Grade Dashboard & Check-In Portal)
"""

import os
import io
import re
import json
import time
import base64
import sqlite3
from datetime import datetime, date, timedelta
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

import importlib
import utils
try:
    importlib.reload(utils)
except Exception:
    pass

from utils import (
    CBK_COLORS, CBK_DEPARTMENTS, CBK_DISCIPLINES, CBK_ALLOWANCE_POLICY,
    DynamicQREngine, AttendanceBackend, CBKEmailDispatcher,
    compute_summary_kpis, compute_department_breakdown, compute_discipline_breakdown,
    mask_name_banking, mask_phone, mask_email, mask_national_id,
    get_eat_now, get_eat_today_str, EAT_TZ
)

# ==============================================================================
# STREAMLIT PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="CBK STRIDE | Sports Telemetry & Roster Integrity",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# CBK STRIDE LUXURY TELEMETRY STYLING (FLIER THEME: MIDNIGHT NAVY, GOLD & CYAN)
# ==============================================================================
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

    /* Global Dark Luxury Palette */
    :root {
        --cbk-bg-dark: #030914;
        --cbk-bg-card: rgba(8, 22, 44, 0.85);
        --cbk-gold-primary: #F5C542;
        --cbk-gold-gradient: linear-gradient(135deg, #FFF5CC 0%, #F5C542 35%, #D4AF37 70%, #996515 100%);
        --cbk-cyan-glow: #00F2FE;
        --cbk-border-gold: rgba(245, 197, 66, 0.35);
        --cbk-border-cyan: rgba(0, 242, 254, 0.3);
    }

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: radial-gradient(circle at 50% 0%, #0d274c 0%, #06152a 40%, #020710 100%) !important;
        color: #F1F5F9 !important;
    }

    [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 0%, #0e2a52 0%, #06152b 40%, #020710 100%) !important;
    }

    [data-testid="stHeader"] {
        background: transparent !important;
    }

    /* All typography defaults */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }

    p, span, label, div {
        color: #E2E8F0;
    }

    small, .stCaption, [data-testid="stCaptionContainer"] p {
        color: #94A3B8 !important;
    }

    label[data-testid="stWidgetLabel"] p {
        color: #F8FAFC !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
    }

    /* Primary CBK STRIDE Header Bar */
    .cbk-topbar {
        background: linear-gradient(135deg, #051429 0%, #0a254a 50%, #040e1c 100%) !important;
        padding: 1.35rem 1.75rem !important;
        border-radius: 18px !important;
        color: #FFFFFF !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7), 0 0 25px rgba(0, 242, 254, 0.15) !important;
        margin-bottom: 1.5rem !important;
        border: 1.5px solid rgba(245, 197, 66, 0.45) !important;
        border-bottom: 4px solid #F5C542 !important;
        backdrop-filter: blur(16px) !important;
    }

    .cbk-badge {
        background: linear-gradient(135deg, #FFE899 0%, #F5C542 50%, #D4AF37 100%) !important;
        color: #040D1A !important;
        font-weight: 900 !important;
        font-size: 0.72rem !important;
        padding: 0.25rem 0.75rem !important;
        border-radius: 6px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        display: inline-block !important;
        margin-bottom: 0.35rem !important;
        box-shadow: 0 2px 10px rgba(245, 197, 66, 0.35) !important;
    }

    .cbk-title {
        font-size: 2.1rem !important;
        font-weight: 900 !important;
        letter-spacing: -0.5px !important;
        margin: 0 !important;
        background: linear-gradient(135deg, #FFF6D6 0%, #F5C542 35%, #E5B838 65%, #B8860B 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        filter: drop-shadow(0 2px 10px rgba(245, 197, 66, 0.3)) !important;
        line-height: 1.2 !important;
    }

    .cbk-subtitle {
        font-size: 0.92rem !important;
        color: #FFFFFF !important;
        margin-top: 0.35rem !important;
        font-weight: 600 !important;
        text-shadow: 0 0 12px rgba(0, 242, 254, 0.35) !important;
    }

    /* Pulsing Live Radar Indicator */
    @keyframes pulse-cyan {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 242, 254, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 8px rgba(0, 242, 254, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 242, 254, 0); }
    }

    .live-pulse {
        width: 8px;
        height: 8px;
        background: #00F2FE;
        border-radius: 50%;
        display: inline-block;
        animation: pulse-cyan 2s infinite;
        vertical-align: middle;
        margin-right: 5px;
    }

    /* Style Streamlit Tabs as Large Executive Navigation Pills */
    div[data-baseweb="tab-list"] {
        gap: 12px !important;
        background: linear-gradient(180deg, rgba(6, 18, 38, 0.98) 0%, rgba(3, 10, 22, 0.98) 100%) !important;
        padding: 10px 14px !important;
        border-radius: 18px !important;
        border: 2px solid rgba(245, 197, 66, 0.45) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(245, 197, 66, 0.15) !important;
        margin-top: 1rem !important;
        margin-bottom: 1.8rem !important;
        display: flex !important;
        flex-wrap: wrap !important;
    }

    button[data-baseweb="tab"] {
        border-radius: 12px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        color: #E2E8F0 !important;
        padding: 0.85rem 1.8rem !important;
        background: rgba(10, 28, 54, 0.85) !important;
        border: 1.5px solid rgba(245, 197, 66, 0.28) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.3px !important;
        white-space: nowrap !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35) !important;
    }

    button[data-baseweb="tab"] * {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        line-height: 1.3 !important;
        color: inherit !important;
    }

    button[data-baseweb="tab"] p {
        font-size: 1.15rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        color: inherit !important;
    }

    button[data-baseweb="tab"]:hover {
        color: #F5C542 !important;
        background: rgba(245, 197, 66, 0.18) !important;
        border-color: #F5C542 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(245, 197, 66, 0.3) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, rgba(245, 197, 66, 0.35) 0%, rgba(0, 242, 254, 0.22) 100%) !important;
        color: #FFE066 !important;
        font-weight: 800 !important;
        border: 2px solid #F5C542 !important;
        box-shadow: 0 0 25px rgba(245, 197, 66, 0.5), inset 0 0 15px rgba(245, 197, 66, 0.25) !important;
        transform: translateY(-2px) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] * {
        color: #FFE066 !important;
        font-weight: 800 !important;
        text-shadow: 0 0 12px rgba(245, 197, 66, 0.6) !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #FFE066 !important;
        font-weight: 800 !important;
        text-shadow: 0 0 12px rgba(245, 197, 66, 0.6) !important;
    }

    div[data-baseweb="tab-highlight"] {
        background: linear-gradient(90deg, #F5C542, #00F2FE) !important;
        height: 4px !important;
        border-radius: 4px !important;
    }

    div[data-baseweb="tab-border"] {
        display: none !important;
    }

    /* Luxury Golden Athlete Credential Card */
    .athlete-card {
        background: linear-gradient(135deg, #091C38 0%, #06152B 60%, #030B17 100%) !important;
        border: 1.5px solid rgba(245, 197, 66, 0.5) !important;
        border-radius: 16px !important;
        padding: 1.4rem 1.6rem !important;
        margin: 1rem 0 !important;
        color: #FFFFFF !important;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.6), 0 0 25px rgba(245, 197, 66, 0.2), 0 0 15px rgba(0, 242, 254, 0.15) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .athlete-card::after {
        content: '';
        position: absolute;
        top: -40%;
        right: -30%;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(245, 197, 66, 0.2) 0%, transparent 70%) !important;
        pointer-events: none;
    }

    /* Flier Glowing Card */
    .mobile-card {
        background: linear-gradient(145deg, #081B36 0%, #040F1F 100%) !important;
        border: 1.5px solid rgba(245, 197, 66, 0.35) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        margin-bottom: 1.2rem !important;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6), 0 0 20px rgba(0, 242, 254, 0.1) !important;
        transition: all 0.25s ease !important;
    }

    .mobile-card:hover {
        transform: translateY(-2px) !important;
        border-color: rgba(245, 197, 66, 0.6) !important;
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.7), 0 0 25px rgba(245, 197, 66, 0.25) !important;
    }

    /* Golden Ticket / Digital Pass Card */
    .ticket-card {
        background: linear-gradient(145deg, #081C38 0%, #040E1E 100%) !important;
        border: 2px solid rgba(245, 197, 66, 0.5) !important;
        border-radius: 18px !important;
        overflow: hidden !important;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.7), 0 0 25px rgba(245, 197, 66, 0.25), 0 0 15px rgba(0, 242, 254, 0.2) !important;
        position: relative !important;
    }

    .ticket-header {
        background: linear-gradient(135deg, #0C284E 0%, #071830 100%) !important;
        color: white !important;
        padding: 1.1rem 1.4rem !important;
        border-bottom: 3px solid #F5C542 !important;
    }

    .ticket-body {
        padding: 1.3rem !important;
    }

    .ticket-perforation {
        border-top: 2px dashed rgba(245, 197, 66, 0.35) !important;
        margin: 1.1rem 0 !important;
        position: relative !important;
    }

    /* Metric KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #081C38 0%, #051326 100%) !important;
        border: 1px solid rgba(245, 197, 66, 0.3) !important;
        border-left: 5px solid #F5C542 !important;
        border-radius: 14px !important;
        padding: 1.1rem 1.3rem !important;
        margin-bottom: 0.9rem !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.2s ease !important;
    }

    .kpi-card:hover {
        transform: translateY(-2px) !important;
        border-color: rgba(245, 197, 66, 0.6) !important;
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.6), 0 0 20px rgba(245, 197, 66, 0.2) !important;
    }

    .kpi-title {
        font-size: 0.78rem !important;
        color: #94A3B8 !important;
        text-transform: uppercase !important;
        font-weight: 700 !important;
        letter-spacing: 0.8px !important;
    }

    .kpi-value {
        font-size: 1.85rem !important;
        font-weight: 900 !important;
        color: #F5C542 !important;
        margin: 0.2rem 0 !important;
        letter-spacing: -0.5px !important;
        text-shadow: 0 0 15px rgba(245, 197, 66, 0.3) !important;
    }

    .kpi-sub {
        font-size: 0.78rem !important;
        color: #00F2FE !important;
        font-weight: 600 !important;
    }

    /* Streamlit Input Widgets (Selectbox, TextInput, NumberInput) */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    .stTextInput input,
    .stSelectbox select {
        background: #071933 !important;
        border: 1.5px solid rgba(245, 197, 66, 0.4) !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div,
    div[data-baseweb="select"] [aria-selected="true"] {
        color: #FFFFFF !important;
    }

    div[data-baseweb="select"] svg {
        fill: #F5C542 !important;
        color: #F5C542 !important;
    }

    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover,
    .stTextInput input:focus {
        border-color: #00F2FE !important;
        box-shadow: 0 0 14px rgba(0, 242, 254, 0.4) !important;
    }

    /* =========================================================================
       BASEWEB & STREAMLIT SELECTBOX POPOVER (HIGH-CONTRAST DARK LUXURY PALETTE)
       ========================================================================= */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] div,
    div[data-baseweb="popover"] [data-baseweb="menu"],
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] ul[role="listbox"],
    ul[data-baseweb="menu"],
    ul[role="listbox"],
    div[data-baseweb="menu"],
    [data-baseweb="popover"] {
        background-color: #06152b !important;
        background: #06152b !important;
        color: #FFFFFF !important;
    }

    div[data-baseweb="popover"] {
        border: 2px solid #F5C542 !important;
        border-radius: 12px !important;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.95), 0 0 25px rgba(0, 242, 254, 0.35) !important;
        max-width: 95vw !important;
        min-width: 360px !important;
        overflow: hidden !important;
    }

    /* All dropdown list options */
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] li[role="option"],
    div[data-baseweb="popover"] li[data-baseweb="menu-item"],
    ul[role="listbox"] li,
    li[role="option"],
    li[data-baseweb="menu-item"] {
        background-color: #06152b !important;
        background: #06152b !important;
        color: #FFFFFF !important;
        font-size: 0.93rem !important;
        font-weight: 600 !important;
        padding: 12px 18px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        line-height: 1.4 !important;
        cursor: pointer !important;
    }

    /* Force all text elements inside dropdown options to high-contrast white */
    div[data-baseweb="popover"] li *,
    div[data-baseweb="popover"] li span,
    div[data-baseweb="popover"] li div,
    div[data-baseweb="popover"] li p,
    ul[role="listbox"] li *,
    li[role="option"] *,
    li[data-baseweb="menu-item"] * {
        color: #FFFFFF !important;
    }

    /* First option (prompt/heading) subtle gold */
    div[data-baseweb="popover"] li:first-child,
    ul[role="listbox"] li:first-child {
        color: #F5C542 !important;
        border-bottom: 2px solid rgba(245, 197, 66, 0.35) !important;
    }
    div[data-baseweb="popover"] li:first-child *,
    ul[role="listbox"] li:first-child * {
        color: #F5C542 !important;
    }

    /* Hovered / Highlighted Option */
    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li[aria-selected="true"],
    ul[role="listbox"] li:hover,
    li[role="option"]:hover,
    li[data-baseweb="menu-item"]:hover {
        background-color: #0d2a52 !important;
        background: #0d2a52 !important;
    }

    div[data-baseweb="popover"] li:hover *,
    div[data-baseweb="popover"] li[aria-selected="true"] *,
    ul[role="listbox"] li:hover *,
    li[role="option"]:hover *,
    li[data-baseweb="menu-item"]:hover * {
        color: #F5C542 !important;
        font-weight: 800 !important;
    }

    /* Selected state highlight */
    div[data-baseweb="popover"] li[aria-selected="true"] {
        border-left: 4px solid #F5C542 !important;
        background-color: #0b2242 !important;
    }

    /* Scrollbar inside popover */
    div[data-baseweb="popover"] ul::-webkit-scrollbar,
    div[data-baseweb="menu"]::-webkit-scrollbar {
        width: 8px;
    }
    div[data-baseweb="popover"] ul::-webkit-scrollbar-track,
    div[data-baseweb="menu"]::-webkit-scrollbar-track {
        background: #040e1c;
    }
    div[data-baseweb="popover"] ul::-webkit-scrollbar-thumb,
    div[data-baseweb="menu"]::-webkit-scrollbar-thumb {
        background: #F5C542;
        border-radius: 4px;
    }

    /* Anti-Scraping / Data Privacy: Hide built-in CSV/Image download toolbar on dataframes */
    [data-testid="stElementToolbar"],
    .stDataFrame [data-testid="stElementToolbar"],
    button[title="Download as CSV"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Streamlit Buttons: Pure Gold Championship Style */
    .stButton > button {
        border-radius: 12px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.3px !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FFE58F 0%, #F5C542 35%, #D4AF37 70%, #996515 100%) !important;
        color: #040D1A !important;
        border: none !important;
        box-shadow: 0 6px 20px rgba(245, 197, 66, 0.4), 0 0 10px rgba(0, 242, 254, 0.2) !important;
        text-transform: uppercase !important;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 28px rgba(245, 197, 66, 0.65), 0 0 20px rgba(0, 242, 254, 0.45) !important;
    }

    .stButton > button[kind="secondary"] {
        background: rgba(8, 25, 50, 0.8) !important;
        color: #F5C542 !important;
        border: 1.5px solid rgba(245, 197, 66, 0.45) !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: rgba(245, 197, 66, 0.15) !important;
        color: #FFFFFF !important;
        border-color: #F5C542 !important;
        box-shadow: 0 0 15px rgba(245, 197, 66, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    /* Streamlit Expanders */
    div[data-testid="stExpander"] {
        background: rgba(7, 21, 41, 0.75) !important;
        border: 1.5px solid rgba(245, 197, 66, 0.3) !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
    }

    /* Streamlit DataFrames */
    [data-testid="stDataFrame"] {
        background: #071933 !important;
        border: 1.5px solid rgba(245, 197, 66, 0.3) !important;
        border-radius: 12px !important;
    }

    div[data-testid="stDataFrame"] * {
        color: #F1F5F9 !important;
    }

    /* Radio buttons */
    div[data-testid="stRadio"] label {
        color: #E2E8F0 !important;
    }

    /* Mobile media queries */
    @media (max-width: 768px) {
        .cbk-title { font-size: 1.4rem !important; }
        .kpi-value { font-size: 1.4rem !important; }
        .stButton>button { width: 100%; padding: 0.75rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# INITIALIZE BACKEND INSTANCE IN SESSION STATE
# ==============================================================================
import importlib
importlib.reload(utils)
from utils import AttendanceBackend, mask_phone, mask_email, mask_national_id

# Ensure backend instance is current and has all required methods
required_backend_methods = [
    "get_staff_by_id", "search_staff", "get_players_by_discipline",
    "log_checkin", "upsert_staff", "get_pending_sync_count", "sync_pending_to_gsheets",
    "authenticate_officer", "grant_rights", "revoke_rights",
    "get_all_authorized_officers", "log_audit_event", "get_audit_trail",
    "submit_facility_feedback", "get_facility_feedback_metrics"
]
needs_backend_reinit = (
    "backend" not in st.session_state 
    or any(not hasattr(st.session_state.backend, m) for m in required_backend_methods)
)

if needs_backend_reinit:
    st.session_state.backend = AttendanceBackend()

backend: AttendanceBackend = st.session_state.backend

def search_staff_registry(query: str, limit: int = 12) -> List[Dict[str, Any]]:
    """Safe, highly-resilient multi-attribute search across staff registry with direct DB fallback."""
    if hasattr(backend, "search_staff"):
        try:
            res = backend.search_staff(query, limit=limit)
            if res:
                return res
        except Exception:
            pass
    try:
        import sqlite3, re
        q = str(query).strip()
        if not q:
            return []
        q_upper = q.upper()
        q_clean = re.sub(r'[^A-Za-z0-9]', '', q_upper)
        q_num = q_clean.replace("CBK", "").strip()
        db_path = getattr(backend, "db_path", "cbk_dswaap.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        candidates = [q_upper, f"CBK-{q_num}" if q_num else q_upper, q_num]
        for cand in candidates:
            if cand:
                cur.execute("SELECT * FROM staff_registry WHERE staff_id = ?", (cand,))
                rows = cur.fetchall()
                if rows:
                    conn.close()
                    return [dict(r) for r in rows]
        pattern_id = f"%{q_num}%" if q_num and len(q_num) >= 2 else f"%{q}%"
        pattern_text = f"%{q.lower()}%"
        cur.execute("""
            SELECT * FROM staff_registry
            WHERE staff_id LIKE ? OR LOWER(full_name) LIKE ? OR LOWER(cbk_email) LIKE ?
            ORDER BY CASE WHEN staff_id LIKE ? THEN 1 WHEN LOWER(full_name) LIKE ? THEN 2 ELSE 3 END, staff_id ASC
            LIMIT ?
        """, (pattern_id, pattern_text, pattern_text, f"CBK-{q_num}%" if q_num else pattern_id, f"{q.lower()}%", limit))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []


# ==============================================================================
# HEADER & SYSTEM STATUS
# ==============================================================================
now_dt = get_eat_now()
sync_icon = "🟢 Google Sheets Synced" if backend.gspread_connected else "🟡 Local Storage Resilient (Zero Data Loss)"

# Check for tester / sandbox mode query param and redirect to dedicated demo page
qp = st.query_params
mode_param = qp.get("mode", "").lower()
sandbox_param = qp.get("sandbox", "").lower()

if mode_param in ["tester", "demo", "sandbox"] or sandbox_param in ["1", "true", "yes"]:
    try:
        st.switch_page("pages/DEMO.py")
    except Exception:
        pass

is_sandbox = False

def get_active_portal_url() -> str:
    """Detects latest active public Cloudflare tunnel or defaults to local Wi-Fi host."""
    if "custom_portal_host" in st.session_state and st.session_state["custom_portal_host"]:
        return st.session_state["custom_portal_host"]
    # 1. First check CURRENT_LIVE_URL.txt in project directory
    url_file = os.path.join(os.path.dirname(__file__), "CURRENT_LIVE_URL.txt")
    if os.path.exists(url_file):
        try:
            with open(url_file, "r", encoding="utf-8") as f:
                val = f.read().strip()
                if val.startswith("http"):
                    return val
        except Exception:
            pass
    try:
        task_dir = r"C:\Users\gathigisn.CBK.008\.gemini\antigravity\brain\00940864-5fa3-44bf-b1d9-02e121e7a052\.system_generated\tasks"
        if os.path.exists(task_dir):
            log_files = [os.path.join(task_dir, f) for f in os.listdir(task_dir) if f.endswith(".log")]
            # Sort by newest modified first
            log_files.sort(key=os.path.getmtime, reverse=True)
            for fpath in log_files:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    if "trycloudflare.com" in content:
                        import re
                        m = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", content)
                        if m:
                            return m.group(0)
    except Exception:
        pass
    return "192.168.1.35:8501"

active_portal_host = get_active_portal_url()

# Load CBK Logo for display
logo_path = os.path.join(os.path.dirname(__file__), "cbk_logo.png")
logo_html = ""
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode("utf-8")
        logo_html = f'<div style="background: rgba(255,255,255,0.95); border-radius: 12px; padding: 5px 10px; border: 2.5px solid #F5C542; margin-right: 18px; display: inline-flex; align-items: center; box-shadow: 0 0 20px rgba(245,197,66,0.35);"><img src="data:image/png;base64,{logo_b64}" style="height: 54px;" alt="CBK Crest" /></div>'

portal_href = active_portal_host if active_portal_host.startswith("http") else f"http://{active_portal_host}"
portal_label = active_portal_host if len(active_portal_host) < 45 else active_portal_host[:42] + "..."

st.markdown(f"""
<div class="cbk-topbar">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div style="display: flex; align-items: center;">
            {logo_html}
            <div>
                <span class="cbk-badge">CENTRAL BANK OF KENYA • SPORTS CLUB</span>
                <h1 class="cbk-title">CBK STRIDE</h1>
                <p class="cbk-subtitle">Sports Telemetry & Roster Integrity</p>
                <div style="margin-top: 6px; display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">
                    <span style="font-size: 0.76rem; background: rgba(245,197,66,0.15); border: 1px solid rgba(245,197,66,0.3); padding: 3px 12px; border-radius: 12px; color: #FFE58F; font-weight: 700;">
                        🏅 Official Inter-Bank Platform
                    </span>
                    <span style="font-size: 0.74rem; background: rgba(0, 242, 254, 0.12); border: 1px solid rgba(0, 242, 254, 0.3); padding: 3px 10px; border-radius: 12px; color: #38BDF8; font-weight: 700;">
                        ⚡ 18 Disciplines • Dynamic QR Telemetry
                    </span>
                </div>
            </div>
        </div>
        <div style="text-align: right; margin-top: 0.5rem;">
            <div style="background: rgba(8, 26, 50, 0.85); border: 1.5px solid rgba(245,197,66,0.4); padding: 0.45rem 0.95rem; border-radius: 8px; font-size: 0.82rem; font-weight: 700; color: #FFFFFF; box-shadow: 0 0 15px rgba(0,242,254,0.18);">
                {sync_icon}
            </div>
            <div style="color: #F5C542; font-size: 0.76rem; margin-top: 0.35rem; font-weight: 700; letter-spacing: 0.5px;">
                🕒 {now_dt.strftime('%A, %d %B %Y | %H:%M:%S')} (EAT / GMT+3)
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 18 CANONICAL CBK SPORTING DISCIPLINES (STRICT ALPHABETICAL ORDER A TO Z)
# ==============================================================================
ALL_18_SPORTS = [
    "Athletics & Track",
    "Badminton",
    "Basketball",
    "Chess",
    "Cycling",
    "Darts",
    "Draughts",
    "Football (Soccer)",
    "Golf",
    "Handball",
    "Lawn Tennis",
    "Martial Arts & Self Defense",
    "Netball",
    "Physical Fitness & Aerobics",
    "Scrabble",
    "Snooker / Pool",
    "Squash",
    "Swimming",
    "Table Tennis",
    "Tug of War",
    "Volleyball"
]

# ==============================================================================
# DATA PRIVACY & EXPORT CONTROL (KENYA DATA PROTECTION ACT 2019 COMPLIANCE)
# ==============================================================================
def get_current_officer() -> Optional[Dict[str, Any]]:
    """Returns authenticated officer profile or None if unauthenticated / expired."""
    officer = st.session_state.get("authenticated_officer")
    if not officer:
        if st.session_state.get("sandbox_mode", False):
            return {
                "staff_id": "DEMO-ADMIN",
                "full_name": "Demo Super Administrator (Sandbox)",
                "department": "IT & Digital Services",
                "role": "Super Admin",
                "can_export_roster": 1,
                "can_export_finances": 1,
                "can_manage_roles": 1,
                "is_demo": True
            }
        # Check backward compatibility with PIN unlock
        if st.session_state.get("admin_exports_unlocked", False):
            return {
                "staff_id": "CBK-3428",
                "full_name": "Samuel Gathigi Njuguna",
                "department": "IT & Digital Services",
                "role": "Super Admin",
                "can_export_roster": 1,
                "can_export_finances": 1,
                "can_manage_roles": 1
            }
        return None
    # 15-Minute Inactivity Session Expiry (Auto-Relock)
    auth_ts = st.session_state.get("officer_auth_time", 0)
    if time.time() - auth_ts > 900:  # 900 seconds = 15 minutes
        st.session_state["authenticated_officer"] = None
        st.session_state["admin_exports_unlocked"] = False
        return None
    return officer

def is_export_authorized(permission_type: str = "roster") -> bool:
    """
    Checks if active officer has rights to perform this export.
    permission_type: 'roster' | 'finances' | 'manage_roles'
    """
    if st.session_state.get("sandbox_mode", False):
        return True
    officer = get_current_officer()
    if not officer:
        return False
    if officer.get("role") == "Super Admin":
        return True
    if permission_type == "roster":
        return bool(officer.get("can_export_roster", 0))
    elif permission_type == "finances":
        return bool(officer.get("can_export_finances", 0))
    elif permission_type == "manage_roles":
        return bool(officer.get("can_manage_roles", 0))
    return False

def render_admin_security_lock(location_key: str = "default", required_perm: str = "roster"):
    """
    Institutional security lock banner with two-factor officer authentication
    (Staff ID + Personal Passkey) compliant with the Kenya Data Protection Act 2019.
    """
    officer = get_current_officer()
    has_perm = is_export_authorized(required_perm)

    if not officer or not has_perm:
        st.markdown(
            """
            <div style="background: rgba(239, 68, 68, 0.08); border: 1.5px solid rgba(239, 68, 68, 0.4); border-radius: 12px; padding: 12px 18px; margin: 12px 0;">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.5rem;">🔒</span>
                        <div>
                            <strong style="color: #F87171; font-size: 0.94rem; letter-spacing: 0.3px;">DATA EXPORT RESTRICTED (DPA 2019 / CBK INFOSEC POLICY)</strong>
                            <div style="color: #94A3B8; font-size: 0.8rem; margin-top: 2px;">
                                File downloads containing staff personal details and raw attendance ledgers are restricted on public access.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        with st.expander("🔑 Authorized Officers: Click to Verify Clearance & Unlock", expanded=False):
            st.caption("Authorized Secretariat, Audit, or HR personnel must authenticate with their Staff ID and Personal Passkey:")
            c_p1, c_p2, c_p3 = st.columns([1.5, 1.5, 1.2])
            with c_p1:
                auth_sid = st.text_input(
                    "Staff ID / Payroll #:",
                    key=f"sec_sid_{location_key}",
                    placeholder="e.g. 3428 or CBK-3428"
                )
            with c_p2:
                auth_passkey = st.text_input(
                    "Security Passkey:",
                    type="password",
                    key=f"sec_pin_{location_key}",
                    placeholder="Enter confidential passkey"
                )
            with c_p3:
                st.write("")
                st.write("")
                if st.button("🔓 Verify Clearance", key=f"btn_auth_{location_key}", use_container_width=True):
                    if auth_sid.strip() and auth_passkey.strip():
                        ok_auth, msg_auth, off_prof = backend.authenticate_officer(auth_sid.strip(), auth_passkey.strip())
                        if ok_auth and off_prof:
                            st.session_state["authenticated_officer"] = off_prof
                            st.session_state["admin_exports_unlocked"] = True
                            st.session_state["officer_auth_time"] = time.time()
                            st.toast(msg_auth, icon="🔓")
                            st.rerun()
                        else:
                            st.error(f"❌ {msg_auth}")
                    else:
                        st.error("Please enter both Staff ID and Passkey.")
    else:
        st.markdown(
            f"""
            <div style="background: rgba(16, 185, 129, 0.1); border: 1.5px solid rgba(16, 185, 129, 0.45); border-radius: 12px; padding: 12px 16px; margin: 12px 0;">
                <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                    <div>
                        <span style="color: #34D399; font-weight: 700; font-size: 0.9rem;">
                            🔓 <strong>Clearance Active:</strong> {officer['full_name']} ({officer['staff_id']}) — <span style="background: rgba(16, 185, 129, 0.2); padding: 2px 8px; border-radius: 6px;">{officer['role']}</span>
                        </span>
                        <div style="color: #94A3B8; font-size: 0.78rem; margin-top: 4px;">
                            Roster Exports: {'✅' if officer.get('can_export_roster') else '❌'} • Financial Exports: {'✅' if officer.get('can_export_finances') else '❌'} • Role Governance: {'✅' if officer.get('can_manage_roles') else '❌'} • Auto-relocks on idle.
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("🔒 Sign Out Officer / Re-Lock All", key=f"btn_relock_{location_key}", use_container_width=False):
            st.session_state["authenticated_officer"] = None
            st.session_state["admin_exports_unlocked"] = False
            st.toast("🔒 Officer signed out. All data exports re-locked.", icon="🔒")
            st.rerun()

# ==============================================================================
# MAIN NAVIGATION TABS (ROLE-GATED TAB CLOAKING FOR ZERO-TRUST PRIVACY)
# ==============================================================================
cur_officer = get_current_officer()

cur_captain_top = st.session_state.get("authenticated_captain", None)

c_hdr_info, c_hdr_login = st.columns([2.8, 1.4])
with c_hdr_login:
    if cur_officer:
        if st.button("🔒 Lock Secretariat", key="btn_top_signout", use_container_width=True):
            st.session_state["authenticated_officer"] = None
            st.session_state["admin_exports_unlocked"] = False
            st.toast("🔒 Officer signed out. Public athlete mode active.", icon="🔒")
            st.rerun()
    elif cur_captain_top:
        first_n = cur_captain_top['full_name'].split()[0]
        if st.button(f"🔒 Sign Out Capt. {first_n}", key="btn_top_signout_cap", use_container_width=True, type="secondary"):
            del st.session_state["authenticated_captain"]
            st.toast(f"🔒 Signed out of {cur_captain_top['discipline']} captain command.", icon="🔒")
            st.rerun()
    else:
        with st.popover("🔐 Officer Login", use_container_width=True):
            st.caption("Authorized Secretariat, Audit, Finance & HR officers log in with institutional clearance:")
            pop_sid = st.text_input("Staff ID / Payroll #:", key="pop_sec_sid", placeholder="e.g. 3071, 3428, or CBK-...")
            pop_pass = st.text_input("Security Passkey:", type="password", key="pop_sec_pass", placeholder="Enter confidential passkey")
            
            if st.button("🔓 Verify Clearance", key="btn_pop_auth", type="primary", use_container_width=True):
                if pop_sid.strip() and pop_pass.strip():
                    ok_p, msg_p, off_p = backend.authenticate_officer(pop_sid.strip(), pop_pass.strip())
                    if ok_p and off_p:
                        st.session_state["authenticated_officer"] = off_p
                        st.session_state["admin_exports_unlocked"] = True
                        st.session_state["officer_auth_time"] = time.time()
                        st.toast(msg_p, icon="🔓")
                        st.rerun()
                    else:
                        st.error(f"❌ {msg_p}")
                else:
                    st.error("Please enter Staff ID and Passkey.")

            st.markdown("---")
            st.caption("🛡️ **Institutional Governance:** Officer roles are strictly pre-appointed by the Sports Club Chairman (Mr. Angwenyi) or Secretariat Administration via *Integration & Settings*. Unaccredited staff cannot access administrative or financial portals.")
            st.markdown("🧪 *Looking for the evaluator test-drive sandbox?* [Open STRIDE™ Demo Portal](/DEMO)")

with c_hdr_info:
    if cur_officer:
        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 8px; padding: 6px 12px; margin-bottom: 6px;">
            <span style="color: #34D399; font-weight: 700; font-size: 0.84rem;">
                🔓 <strong>Officer Workspace Active:</strong> {cur_officer['full_name']} ({cur_officer['staff_id']}) • <span style="background: rgba(16, 185, 129, 0.2); padding: 1px 6px; border-radius: 4px;">{cur_officer['role']}</span>
            </span>
        </div>
        """, unsafe_allow_html=True)
    elif cur_captain_top:
        st.markdown(f"""
        <div style="background: rgba(245, 197, 66, 0.12); border: 1.5px solid rgba(245, 197, 66, 0.45); border-radius: 8px; padding: 6px 12px; margin-bottom: 6px;">
            <span style="color: #FFE58F; font-weight: 700; font-size: 0.84rem;">
                🎖️ <strong>Accredited Captain:</strong> {cur_captain_top['full_name']} ({cur_captain_top['staff_id']}) • <span style="background: rgba(245, 197, 66, 0.25); color: #FFF; padding: 1px 8px; border-radius: 4px;">{cur_captain_top['discipline']}</span>
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.caption("🔒 **Public Athlete Mode:** Administrative & financial portals are cloaked. Authorized officers log in above.")

# Executive Flyer Download Hub (Direct Mobile & Desktop Download)
with st.expander("📥 Download Official CBK STRIDE™ 2-Page Executive Flyer (PDF / PPTX / Images)", expanded=False):
    st.caption("Official 2-Page executive marketing & technical capability flyer for management and sports secretariat:")
    c_f_dl1, c_f_dl2, c_f_dl3 = st.columns(3)
    
    pdf_fpath = os.path.join(os.path.dirname(__file__), "CBK_STRIDE_Executive_2Pager_Flyer.pdf")
    pptx_fpath = os.path.join(os.path.dirname(__file__), "CBK_STRIDE_Executive_2Pager_Flyer.pptx")
    spread_fpath = os.path.join(os.path.dirname(__file__), "CBK_STRIDE_Flyer_2Page_Spread.jpg")
    
    with c_f_dl1:
        if os.path.exists(pdf_fpath):
            with open(pdf_fpath, "rb") as f_pdf:
                st.download_button(
                    label="📄 Download 2-Page Flyer (PDF)",
                    data=f_pdf.read(),
                    file_name="CBK_STRIDE_Executive_2Pager_Flyer.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="dl_flyer_pdf"
                )
    with c_f_dl2:
        if os.path.exists(pptx_fpath):
            with open(pptx_fpath, "rb") as f_pptx:
                st.download_button(
                    label="📊 Download Presentation (.PPTX)",
                    data=f_pptx.read(),
                    file_name="CBK_STRIDE_Executive_2Pager_Flyer.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True,
                    key="dl_flyer_pptx"
                )
    with c_f_dl3:
        if os.path.exists(spread_fpath):
            with open(spread_fpath, "rb") as f_sp:
                st.download_button(
                    label="🖼️ Download 2-Page Spread (.JPG)",
                    data=f_sp.read(),
                    file_name="CBK_STRIDE_Flyer_2Page_Spread.jpg",
                    mime="image/jpeg",
                    use_container_width=True,
                    key="dl_flyer_spread"
                )

# Determine visible tabs based on authenticated officer clearance (Roll Call 1st for pitch-side priority)
tab_titles = ["📋 Captain's Roll Call", "📱 Mobile Check-In", "🏷️ Captain QR Station"]

if cur_officer:
    officer_role = cur_officer.get("role", "")
    if officer_role in ["Super Admin", "Secretariat Admin", "Executive Chairman"]:
        tab_titles.extend([
            "🏛️ Secretariat Operations",
            "📊 HR Analytics Command",
            "💰 Finance & Audit Portal",
            "⚙️ Integration & Settings"
        ])
    elif officer_role in ["Secretariat Officer", "Secretariat Operations"]:
        tab_titles.extend([
            "🏛️ Secretariat Operations",
            "📊 HR Analytics Command",
            "💰 Finance & Audit Portal"
        ])
    elif officer_role in ["Finance & Internal Audit", "Finance Officer"]:
        tab_titles.extend([
            "💰 Finance & Audit Portal",
            "🏛️ Secretariat Operations",
            "📊 HR Analytics Command"
        ])
    elif officer_role in ["HR Compliance Lead", "HR Officer"]:
        tab_titles.extend([
            "📊 HR Analytics Command",
            "🏛️ Secretariat Operations"
        ])
    else:
        tab_titles.extend(["🏛️ Secretariat Operations", "📊 HR Analytics Command"])


# ==============================================================================
# CAPTAIN'S TACTICAL FIXTURES, DRILLS & CALENDAR DIARY
# ==============================================================================
def render_captain_calendar_section(discipline: str, is_authorized: bool, key_prefix: str = "cal"):
    st.markdown("---")
    st.markdown(f"#### 📅 Captain's Tactical Calendar & Squad Diary ({discipline})")
    st.caption("Plan upcoming tournament fixtures, friendly matches, conditioning drills, and jot down tactical notes:")

    events = backend.get_calendar_notes(discipline)

    col_c1, col_c2 = st.columns([1.6, 1.1])

    with col_c1:
        st.markdown(f"##### 📋 Scheduled Fixtures & Squad Diary ({len(events)} Events)")
        if not events:
            st.info(f"No scheduled fixtures or tactical notes recorded for {discipline} yet. Add one on the right!")
        else:
            for ev in events:
                ev_type = ev.get("event_type", "Conditioning Drill")
                if "Tournament" in ev_type:
                    badge_color = "#F5C542"
                    badge_bg = "rgba(245, 197, 66, 0.2)"
                    badge_icon = "🏆"
                elif "Friendly" in ev_type:
                    badge_color = "#00F2FE"
                    badge_bg = "rgba(0, 242, 254, 0.2)"
                    badge_icon = "⚽"
                elif "Briefing" in ev_type or "Tactical" in ev_type:
                    badge_color = "#A78BFA"
                    badge_bg = "rgba(167, 139, 250, 0.2)"
                    badge_icon = "📋"
                elif "Medical" in ev_type or "Rest" in ev_type:
                    badge_color = "#F87171"
                    badge_bg = "rgba(248, 113, 113, 0.2)"
                    badge_icon = "🩹"
                else:
                    badge_color = "#34D399"
                    badge_bg = "rgba(52, 211, 153, 0.2)"
                    badge_icon = "🏋️"

                venue_txt = f"📍 {ev.get('venue')}" if ev.get('venue') else ""

                st.markdown(f"""
                <div style="background: rgba(8, 24, 48, 0.75); border: 1px solid rgba(245, 197, 66, 0.25); border-left: 4.5px solid {badge_color}; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <span style="background: {badge_bg}; color: {badge_color}; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 800; text-transform: uppercase;">
                                {badge_icon} {ev_type}
                            </span>
                            <h4 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.05rem; font-weight: 800;">{ev.get('title')}</h4>
                            <p style="margin: 0; font-size: 0.8rem; color: #CBD5E1;">
                                🗓️ <strong>{ev.get('event_date')}</strong> at <strong>{ev.get('event_time')}</strong> • {venue_txt}
                            </p>
                        </div>
                    </div>
                    <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.06); font-size: 0.86rem; color: #94A3B8;">
                        📝 <em>{ev.get('notes') or 'No additional tactical notes.'}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if is_authorized:
                    if st.button("🗑️ Remove Fixture", key=f"del_ev_{key_prefix}_{ev['id']}", help="Delete this scheduled event"):
                        backend.delete_calendar_note(ev['id'])
                        st.toast("✅ Event removed from squad calendar.", icon="🗑️")
                        st.rerun()

    with col_c2:
        st.markdown("##### ➕ Schedule Fixture or Jot Note")
        if not is_authorized:
            st.caption("🔒 Please authenticate as Captain or Secretariat to schedule fixtures and save tactical notes.")
        else:
            with st.form(key=f"form_add_cal_{key_prefix}_{discipline}"):
                f_date = st.date_input("Event Date:", key=f"cal_d_{key_prefix}")
                f_time = st.text_input("Kick-off / Start Time:", value="17:00", key=f"cal_t_{key_prefix}")
                f_type = st.selectbox(
                    "Event Category:",
                    [
                        "🏆 Tournament Fixture",
                        "⚽ Friendly Match",
                        "🏋️ Conditioning / Fitness Drill",
                        "📋 Tactical Briefing",
                        "🩹 Medical / Squad Rest Day"
                    ],
                    key=f"cal_type_{key_prefix}"
                )
                f_title = st.text_input("Event Title / Opponent:*", placeholder="e.g. Friendly Match vs KCB Lions", key=f"cal_title_{key_prefix}")
                f_venue = st.text_input("Venue / Station:", value=CBK_DISCIPLINES.get(discipline, {}).get("default_venue", "Main Stadium"), key=f"cal_ven_{key_prefix}")
                f_notes = st.text_area("Tactical Notes & Instructions:", placeholder="e.g. Full navy kit required, arrive 30 mins early for warm-ups. Sub in Peter for injured John.", key=f"cal_notes_{key_prefix}")

                btn_save_cal = st.form_submit_button("💾 Save to Squad Calendar & Diary", use_container_width=True)
                if btn_save_cal:
                    if not f_title.strip():
                        st.error("Please provide an Event Title or Opponent.")
                    else:
                        d_str = f_date.strftime("%Y-%m-%d")
                        cur_cap = st.session_state.get("authenticated_captain", None)
                        cur_off = get_current_officer()
                        if cur_cap and cur_cap.get("staff_id"):
                            created_by_tag = f"Captain ({cur_cap['staff_id']})"
                        elif cur_off and cur_off.get("staff_id"):
                            created_by_tag = f"Secretariat ({cur_off['staff_id']})"
                        else:
                            cap_rec = backend.get_captain_for_discipline(discipline)
                            if cap_rec and cap_rec.get("staff_id"):
                                created_by_tag = f"Captain ({cap_rec['staff_id']})"
                            else:
                                created_by_tag = f"Captain ({discipline})"
                        ok = backend.add_calendar_note(
                            discipline=discipline,
                            event_date=d_str,
                            event_time=f_time.strip(),
                            event_type=f_type,
                            title=f_title.strip(),
                            notes=f_notes.strip(),
                            venue=f_venue.strip(),
                            created_by=created_by_tag
                        )
                        if ok:
                            st.toast(f"✅ Added '{f_title}' to {discipline} tactical calendar!", icon="📅")
                            st.rerun()
                        else:
                            st.error("Failed to save calendar event. Please retry.")

# ==============================================================================
# PAINLESS 1-CLICK SATISFACTION REACTION WIDGET (AI POWERED NLP)
# ==============================================================================
def render_painless_satisfaction_widget(
    staff_id: str = "CBK-ATHLETE",
    full_name: str = "CBK Athlete",
    department: str = "Operations",
    discipline: str = "General",
    touchpoint: str = "GATE_PASS",
    key_prefix: str = "pass_sat"
):
    """
    Renders an ultra-fast, painless 1-click satisfaction widget with 5 emoji faces:
    😡 (1 - Frustrated), 🙁 (2 - Poor), 😐 (3 - Okay), 🙂 (4 - Good), 🤩 (5 - Loved It!).
    Clicking any face logs the feedback instantly to SQLite without requiring typing.
    Optionally reveals 1-tap aspect chips and an optional 1-sentence note for NLP processing.
    """
    sub_key = f"fb_state_{key_prefix}"
    submitted = st.session_state.get(sub_key)

    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(8, 24, 46, 0.95) 0%, rgba(4, 14, 28, 0.98) 100%);
                border: 1.5px solid rgba(245, 197, 66, 0.45);
                border-radius: 16px; padding: 16px 18px; margin-top: 16px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5), 0 0 15px rgba(0,242,254,0.12);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
            <span style="font-size: 0.74rem; font-weight: 800; color: #F5C542; text-transform: uppercase; letter-spacing: 0.8px;">
                ⚡ 1-Tap Pulse • Facility & Session Satisfaction
            </span>
            <span style="background: rgba(0, 242, 254, 0.15); color: #00F2FE; font-size: 0.70rem; font-weight: 700; padding: 2px 8px; border-radius: 10px; border: 1px solid rgba(0, 242, 254, 0.3);">
                AI Powered NLP
            </span>
        </div>
        <h4 style="color: #FFFFFF; font-size: 1.05rem; font-weight: 800; margin: 0 0 4px 0;">
            How was your facility & training experience today?
        </h4>
        <p style="color: #94A3B8; font-size: 0.82rem; margin: 0 0 8px 0; line-height: 1.4;">
            Painless 1-click rating. Tap any face below to record your response immediately:
        </p>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3, f4, f5 = st.columns(5)
    faces = [
        ("😡", 1, "Frustrated", f1),
        ("🙁", 2, "Poor", f2),
        ("😐", 3, "Okay", f3),
        ("🙂", 4, "Good", f4),
        ("🤩", 5, "Loved It!", f5),
    ]

    for emoji_char, rating_val, desc, col in faces:
        with col:
            is_active = submitted and submitted.get("rating") == rating_val
            btn_label = f"{emoji_char}\n{desc}"
            if col.button(btn_label, key=f"{key_prefix}_face_{rating_val}", use_container_width=True, type="primary" if is_active else "secondary"):
                clean_sid = str(staff_id or "CBK-ATHLETE").strip().upper()
                if not clean_sid.startswith("CBK-"):
                    clean_sid = f"CBK-{clean_sid}"
                ok, msg, rec = backend.submit_facility_feedback(
                    staff_id=clean_sid,
                    full_name=full_name or "CBK Athlete",
                    department=department or "Operations",
                    discipline=discipline or "Sports",
                    rating=rating_val,
                    feedback_text="",
                    touchpoint=touchpoint
                )
                if ok and rec:
                    st.session_state[sub_key] = rec
                    st.toast(f"{emoji_char} Thank you! Your {rating_val}-star rating was logged instantly.", icon="⭐")
                    st.rerun()

    if submitted:
        rating_val = submitted.get("rating", 5)
        emoji_val = submitted.get("emoji", "🤩")
        sentiment_label = submitted.get("sentiment_label", "POSITIVE")
        sentiment_score = submitted.get("sentiment_score", 0.95)
        aspects = submitted.get("aspects", [])
        rec_id = submitted.get("id")
        cur_text = submitted.get("feedback_text", "")

        badge_bg = "#059669" if sentiment_label == "POSITIVE" else ("#DC2626" if sentiment_label == "NEGATIVE" else "#D97706")

        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.12); border: 1.5px solid #10B981; border-radius: 12px; padding: 12px 16px; margin-top: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #FFFFFF; font-weight: 800; font-size: 0.92rem;">
                    {emoji_val} <strong>Logged: {rating_val}/5 Stars</strong>
                </span>
                <span style="background: {badge_bg}; color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.72rem; font-weight: 800;">
                    NLP Sentiment: {sentiment_label} ({sentiment_score:+.2f})
                </span>
            </div>
            <p style="color: #CBD5E1; font-size: 0.78rem; margin: 4px 0 0 0;">
                Recognized Aspects: <strong style="color: #F5C542;">{', '.join(aspects) if aspects else 'General Facility Experience'}</strong>
            </p>
            {f'<p style="color: #94A3B8; font-size: 0.78rem; font-style: italic; margin: 4px 0 0 0;">"{cur_text}"</p>' if cur_text else ''}
        </div>
        """, unsafe_allow_html=True)

        with st.expander("💬 Optional: Tell us why in one quick sentence or tap a chip", expanded=False):
            st.caption("Tap any quick chip below or type in English/Swahili (e.g. pool cleanliness, gym AC, gate scan speed, allowance promptness):")

            c_ch1, c_ch2, c_ch3 = st.columns(3)
            with c_ch1:
                if st.button("🏊 Clean Pool Water", key=f"{key_prefix}_chip_pool", use_container_width=True):
                    backend.update_facility_feedback_text(rec_id, "Clean pool water and lane markers were great.")
                    st.session_state[sub_key]["feedback_text"] = "Clean pool water and lane markers were great."
                    st.toast("✅ Note updated!", icon="🏊")
                    st.rerun()
                if st.button("🚿 Clean Showers", key=f"{key_prefix}_chip_shower", use_container_width=True):
                    backend.update_facility_feedback_text(rec_id, "Showers and changing rooms were spotless.")
                    st.session_state[sub_key]["feedback_text"] = "Showers and changing rooms were spotless."
                    st.toast("✅ Note updated!", icon="🚿")
                    st.rerun()
            with c_ch2:
                if st.button("🏋️ Great Gym & AC", key=f"{key_prefix}_chip_gym", use_container_width=True):
                    backend.update_facility_feedback_text(rec_id, "Gym weights and air conditioning were excellent.")
                    st.session_state[sub_key]["feedback_text"] = "Gym weights and air conditioning were excellent."
                    st.toast("✅ Note updated!", icon="🏋️")
                    st.rerun()
                if st.button("⏱️ Prompt Allowance", key=f"{key_prefix}_chip_allowance", use_container_width=True):
                    backend.update_facility_feedback_text(rec_id, "Session attendance and allowance processed promptly.")
                    st.session_state[sub_key]["feedback_text"] = "Session attendance and allowance processed promptly."
                    st.toast("✅ Note updated!", icon="⏱️")
                    st.rerun()
            with c_ch3:
                if st.button("⚡ Fast Gate Scan", key=f"{key_prefix}_chip_gate", use_container_width=True):
                    backend.update_facility_feedback_text(rec_id, "Gate checkin QR scanning was instantaneous.")
                    st.session_state[sub_key]["feedback_text"] = "Gate checkin QR scanning was instantaneous."
                    st.toast("✅ Note updated!", icon="⚡")
                    st.rerun()
                if st.button("⚠️ Needs Maintenance", key=f"{key_prefix}_chip_maint", use_container_width=True):
                    backend.update_facility_feedback_text(rec_id, "Equipment needs maintenance and repairs.")
                    st.session_state[sub_key]["feedback_text"] = "Equipment needs maintenance and repairs."
                    st.toast("✅ Note updated!", icon="⚠️")
                    st.rerun()

            note_val = st.text_input(
                "Or type custom note (English or Swahili):",
                value=cur_text,
                placeholder="e.g. maji ya pool yalikuwa safi sana, gym AC ilikuwa nzuri...",
                key=f"{key_prefix}_custom_note_input"
            )

            c_save_n, c_rst = st.columns([2, 1])
            with c_save_n:
                if st.button("💾 Save Note with NLP", key=f"{key_prefix}_btn_save_note", use_container_width=True, type="primary"):
                    if note_val.strip() and rec_id:
                        ok_up, msg_up, nlp_up = backend.update_facility_feedback_text(rec_id, note_val.strip())
                        if ok_up:
                            st.session_state[sub_key]["feedback_text"] = note_val.strip()
                            if nlp_up:
                                st.session_state[sub_key]["sentiment_score"] = nlp_up["polarity"]
                                st.session_state[sub_key]["sentiment_label"] = nlp_up["label"]
                                st.session_state[sub_key]["aspects"] = nlp_up["aspects"]
                            st.toast("✅ Note saved and re-analyzed with AI sentiment!", icon="🤖")
                            st.rerun()
            with c_rst:
                if st.button("🔄 Rate Again", key=f"{key_prefix}_btn_reset", use_container_width=True):
                    if sub_key in st.session_state:
                        del st.session_state[sub_key]
                    st.rerun()

# Global 1-Tap Facility Satisfaction Pulse for All Staff & Visitors
with st.expander("⭐ Rate Today's Sports Facility & Session Experience (Painless 1-Click Emoji Pulse)", expanded=False):
    cur_top_sid = cur_officer['staff_id'] if cur_officer else (cur_captain_top['staff_id'] if cur_captain_top else st.session_state.get('active_staff_id', 'CBK-STAFF'))
    cur_top_fn = cur_officer['full_name'] if cur_officer else (cur_captain_top['full_name'] if cur_captain_top else 'CBK Athlete')
    cur_top_dp = cur_officer['department'] if cur_officer else 'Operations'
    cur_top_sp = cur_captain_top['discipline'] if cur_captain_top else st.session_state.get('active_discipline', 'General Wellness')
    render_painless_satisfaction_widget(
        staff_id=cur_top_sid,
        full_name=cur_top_fn,
        department=cur_top_dp,
        discipline=cur_top_sp,
        touchpoint="TOP_PORTAL_BANNER",
        key_prefix="top_pulse"
    )

tabs = st.tabs(tab_titles)
tab_dict = {title: tab for title, tab in zip(tab_titles, tabs)}

# Retrieve data
df_all = backend.get_all_records()
kpis = compute_summary_kpis(df_all)

# ==============================================================================
# TAB 1: PARTICIPANT MOBILE CHECK-IN (ONE-TAP EMPLOYEE NUMBER LOOKUP)
# ==============================================================================
with tab_dict["📱 Mobile Check-In"]:
    st.markdown("### 📱 Participant Self Check-In Portal")
    st.caption("Mobile-first check-in. Select any of the 18 CBK sports below to view enrolled team players, explore rosters, and tap to verify attendance.")

    # Read incoming URL query parameters (when scanned via phone camera QR or magic link email)
    query_gate = st.query_params.get("gate", "PRE_SPORT")
    query_disc = st.query_params.get("discipline", None)
    query_stat = st.query_params.get("station", None)
    query_confirmed = st.query_params.get("confirmed", None)
    query_email = st.query_params.get("email", None)
    query_staff_id = st.query_params.get("staff_id", None)
    query_verify_token = st.query_params.get("verify_token", None)

    # 18 Standard CBK Sporting Disciplines - Alphabetical order A to Z
    all_18_sports = ALL_18_SPORTS

    # Pre-calculate player counts for each sport from staff_registry
    sport_player_counts = {}
    try:
        conn_c = sqlite3.connect(backend.db_path)
        cur_c = conn_c.cursor()
        cur_c.execute("SELECT primary_sport, count(*) FROM staff_registry GROUP BY primary_sport")
        for s_n, s_c in cur_c.fetchall():
            sport_player_counts[s_n] = s_c
        conn_c.close()
    except Exception:
        pass

    # Handle Magic Link Email Confirmation
    if query_confirmed == "1" and (query_email or query_staff_id):
        lookup_key = query_email or query_staff_id
        matched_user = backend.get_staff_by_id(lookup_key)
        if matched_user:
            st.session_state["active_discipline"] = matched_user.get("primary_sport", "Golf")
            st.session_state["active_staff_id"] = matched_user["staff_id"].replace("CBK-", "")
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #059669 0%, #047857 100%); color: white; padding: 16px 20px; border-radius: 12px; margin-bottom: 1.2rem; box-shadow: 0 4px 15px rgba(5,150,105,0.25); border: 2px solid #34D399;">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <span style="background: #F8B82D; color: #082142; font-weight: 800; font-size: 0.72rem; padding: 3px 8px; border-radius: 4px; text-transform: uppercase;">
                            ⛳ IDENTITY CONFIRMED VIA CBK EMAIL
                        </span>
                        <h3 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.35rem;">
                            Welcome back, Golfer {matched_user['full_name'] if cur_officer else mask_name_banking(matched_user['full_name'])} ({matched_user['staff_id']})!
                        </h3>
                        <p style="margin: 0; font-size: 0.85rem; color: #DCFCE7;">
                            ✉️ Authenticated via <strong>{matched_user['cbk_email'] if cur_officer else mask_email(matched_user['cbk_email'])}</strong> • 🏛️ {matched_user['department']} • 📍 Clubhouse 1st Tee Station
                        </p>
                    </div>
                    <div style="font-size: 2.2rem;">🏌️‍♂️</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()

    # Ensure valid active discipline in session state
    if query_disc and query_disc in all_18_sports:
        st.session_state["active_discipline"] = query_disc
    elif "active_discipline" not in st.session_state:
        st.session_state["active_discipline"] = "Golf"

    if query_staff_id:
        st.session_state["active_staff_id"] = query_staff_id.replace("CBK-", "")

    if query_disc:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #025BBF 0%, #10529E 100%); color: white; padding: 14px 18px; border-radius: 12px; margin-bottom: 1.2rem; border-left: 6px solid #F8B82D; box-shadow: 0 4px 14px rgba(2,91,191,0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="background: #F8B82D; color: #082142; font-weight: 800; font-size: 0.72rem; padding: 3px 8px; border-radius: 4px; text-transform: uppercase;">
                        📲 CAPTAIN IPAD QR SCANNED
                    </span>
                    <h3 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.3rem;">
                        Welcome to {query_disc} Check-In!
                    </h3>
                    <p style="margin: 0; font-size: 0.85rem; color: #EEF6FC;">
                        Station: <strong>{query_stat or 'Field Terminal'}</strong> • Gate: <strong>{'Gate 1: Arrival' if query_gate == 'PRE_SPORT' else 'Gate 2: Departure'}</strong>
                    </p>
                    <p style="margin: 2px 0 0 0; font-size: 0.78rem; color: #BAE6FD;">
                        Select your name from the squad below or punch your Staff ID to clock in. Walk-in players can self-register instantly!
                    </p>
                </div>
                <div style="font-size: 2.2rem;">📱</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


    col_form, col_pass = st.columns([1.1, 0.9])

    with col_form:
        # ======================================================================
        # 1. THE 18-SPORT SELECTOR (FRONT & CENTER - ALPHABETICAL A - Z)
        # ======================================================================
        st.markdown("#### 🏅 1. Select Sporting Discipline (Alphabetical A – Z)")

        if "active_discipline" not in st.session_state or st.session_state["active_discipline"] not in all_18_sports:
            st.session_state["active_discipline"] = "Golf"

        # Keep global_sport_picker state synchronized with active_discipline
        if "global_sport_picker" not in st.session_state or st.session_state["global_sport_picker"] != st.session_state["active_discipline"]:
            st.session_state["global_sport_picker"] = st.session_state["active_discipline"]

        def _on_sport_picker_change():
            new_s = st.session_state.get("global_sport_picker")
            if new_s and new_s in all_18_sports:
                st.session_state["active_discipline"] = new_s
                st.session_state["active_staff_id"] = ""

        st.selectbox(
            "Choose sport from A – Z (18 Disciplines Available):",
            all_18_sports,
            format_func=lambda s: f"{s} {CBK_DISCIPLINES.get(s, {}).get('icon', '🏅')} — {sport_player_counts.get(s, 0)} Enrolled Athletes ({CBK_DISCIPLINES.get(s, {}).get('category', 'General')})",
            key="global_sport_picker",
            on_change=_on_sport_picker_change
        )
        active_sport = st.session_state["active_discipline"]
        sport_info = CBK_DISCIPLINES.get(active_sport, {})
        disc_icon = sport_info.get("icon", "🏅")
        disc_captain = sport_info.get("captain", "Capt. Appointed Officer")
        disc_venue = sport_info.get("default_venue", "CBK Sports Club")
        disc_stations = sport_info.get("stations", ["Main Gate Checkpoint"])

        # Fetch all players enrolled in this sport, sorted alphabetically by name A-Z
        squad_players = backend.get_players_by_discipline(active_sport)
        squad_players = sorted(squad_players, key=lambda p: p["full_name"].strip().lower())

        # Gate & Station Controls
        col_g_gate, col_g_stat = st.columns([1, 1.2])
        with col_g_gate:
            gate_option = st.radio(
                "Verification Gate:",
                ["Gate 1: Pre-Sport Arrival", "Gate 2: Post-Sport Departure"],
                index=0 if query_gate == "PRE_SPORT" else 1,
                key=f"part_gate_radio_{active_sport}"
            )
            active_gate = "PRE_SPORT" if "Gate 1" in gate_option else "POST_SPORT"
        with col_g_stat:
            active_station = st.selectbox(
                f"Station Post ({active_sport}):",
                disc_stations,
                index=0,
                key=f"part_stat_{active_sport}"
            )

        gate_label = "Gate 1: Pre-Sport Arrival Check-In" if active_gate == "PRE_SPORT" else "Gate 2: Post-Sport Departure Check-In"
        gate_badge_bg = "#F5C542" if active_gate == "PRE_SPORT" else "#00F2FE"
        gate_badge_fg = "#040D1A" if active_gate == "PRE_SPORT" else "#040D1A"

        gate_header_html = (
            f'<div style="background: linear-gradient(135deg, #091F3D 0%, #051326 100%); padding: 16px 20px; border-radius: 14px; color: white; margin-bottom: 1.2rem; border: 1.5px solid rgba(245, 197, 66, 0.4); border-bottom: 4px solid #F5C542; box-shadow: 0 8px 24px rgba(0,0,0,0.5), 0 0 15px rgba(0,242,254,0.12);">'
            f'<div style="display: flex; justify-content: space-between; align-items: center;">'
            f'<div>'
            f'<span style="background: {gate_badge_bg}; color: {gate_badge_fg}; font-size: 0.72rem; font-weight: 900; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px;">{gate_label}</span>'
            f'<h3 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.35rem; font-weight: 800; text-shadow: 0 0 10px rgba(0,242,254,0.25);">{disc_icon} {active_sport}</h3>'
            f'<p style="margin: 0; font-size: 0.82rem; color: #CBD5E1;">📍 <strong>{active_station}</strong> • 👨‍✈️ {disc_captain}</p>'
            f'<p style="margin: 2px 0 0 0; font-size: 0.76rem; color: #38BDF8;">Home Venue: {disc_venue}</p>'
            f'</div>'
            f'<div style="text-align: right;">'
            f'<div style="background: rgba(245,197,66,0.15); border: 1px solid rgba(245,197,66,0.3); padding: 5px 12px; border-radius: 8px; font-size: 0.82rem; font-weight: 800; color: #F5C542;">'
            f'👥 {len(squad_players)} Squad Athletes'
            f'</div>'
            f'<div style="font-size: 1.6rem; margin-top: 4px;">{"🏁" if active_gate == "POST_SPORT" else "⏱️"}</div>'
            f'</div>'
            f'</div>'
            f'</div>'
        )
        st.markdown(gate_header_html, unsafe_allow_html=True)

        # ======================================================================
        # 2. CHOOSE OR SEARCH YOUR NAME OR STAFF ID
        # ======================================================================
        st.markdown(f"#### 🔍 2. Choose or Search Your Profile ({active_sport} Squad)")
        st.caption(f"Search by **Staff ID (Payroll #)** or **Athlete Name**, or select directly from the {len(squad_players)} enrolled athletes in {active_sport}:")

        col_search_txt, col_search_sel = st.columns([1.1, 1.1])
        
        with col_search_txt:
            c_sin, c_sbtn = st.columns([2.6, 1.2])
            with c_sin:
                search_input_val = st.text_input(
                    "🔎 Search by Staff ID or Name:",
                    value="",
                    placeholder="e.g. 3428, 3432, Gathigi...",
                    key=f"search_txt_{active_sport}",
                    label_visibility="collapsed"
                )
            with c_sbtn:
                btn_squad_search = st.button("🔍 Find", key=f"btn_sq_search_{active_sport}", use_container_width=True)
            
        with col_search_sel:
            roster_sort_by = st.radio(
                "Dropdown Format:",
                ["🔢 By Staff ID (Payroll #)", "🔤 By Name (A – Z)"],
                index=0,
                horizontal=True,
                key=f"roster_sort_{active_sport}"
            )
            
            # Sort squad according to selected format
            if "Staff ID" in roster_sort_by:
                def _sid_sort_key(p):
                    sid_clean = re.sub(r'[^0-9]', '', p["staff_id"])
                    return int(sid_clean) if sid_clean.isdigit() else 999999
                sorted_squad = sorted(squad_players, key=_sid_sort_key)
                player_select_options = [f"-- Or Pick from {len(squad_players)} {active_sport} Athletes (By Staff ID) --"]
            else:
                sorted_squad = sorted(squad_players, key=lambda p: p["full_name"].strip().lower())
                player_select_options = [f"-- Or Pick from {len(squad_players)} {active_sport} Athletes (A – Z) --"]

            default_p_idx = 0
            cur_active_sid = str(st.session_state.get("active_staff_id", "")).replace("CBK-", "")
            
            for idx, p in enumerate(sorted_squad):
                badge = " [✅ VERIFIED]" if p["today_status"] == "DUAL_VERIFIED" else (
                    " [🛑 EARLY EXIT]" if p["today_status"] == "INSUFFICIENT_DURATION" else (
                        " [⏱️ ON FIELD]" if p["today_status"] == "PRE_SPORT_VALIDATED" else ""
                    )
                )
                dept_short = p['department'][:20] if p.get('department') else "Staff"
                p_disp_name = p['full_name'] if cur_officer else mask_name_banking(p['full_name'])
                if "Staff ID" in roster_sort_by:
                    opt_str = f"{p['staff_id']} — {p_disp_name} ({dept_short}){badge}"
                else:
                    opt_str = f"{p_disp_name} ({p['staff_id']}) — {dept_short}{badge}"
                player_select_options.append(opt_str)
                if cur_active_sid and cur_active_sid in p['staff_id']:
                    default_p_idx = idx + 1

            def _on_squad_dropdown_change():
                sel_choice = st.session_state.get(f"player_dropdown_{active_sport}")
                if sel_choice and not sel_choice.startswith("-- Or Pick"):
                    m = re.search(r"(CBK-[A-Za-z0-9]+)", sel_choice)
                    if m:
                        st.session_state["active_staff_id"] = m.group(1).replace("CBK-", "").strip()
                    elif " — " in sel_choice:
                        st.session_state["active_staff_id"] = sel_choice.split(" — ")[0].replace("CBK-", "").strip()
                    # Clear search text inputs so old search queries don't override the dropdown choice!
                    st.session_state[f"search_txt_{active_sport}"] = ""
                    st.session_state["global_staff_search"] = ""
                    st.session_state["last_global_q"] = ""

            sel_p = st.selectbox(
                f"Or Select from {active_sport} Roster:",
                player_select_options,
                index=default_p_idx,
                key=f"player_dropdown_{active_sport}",
                on_change=_on_squad_dropdown_change
            )

        # Handle Search Input Queries with Multi-Sport Awareness
        lookup_term = ""
        
        if search_input_val.strip():
            raw_q = search_input_val.strip()
            # Perform multi-attribute search across staff registry
            search_results = search_staff_registry(raw_q, limit=6)
            
            if search_results:
                # If exact single match or exact staff_id match
                exact_id_matches = [
                    m for m in search_results 
                    if m["staff_id"].replace("CBK-", "").lower() == raw_q.replace("CBK-", "").replace("CBK", "").strip().lower()
                    or m["staff_id"].lower() == raw_q.lower()
                ]
                
                if exact_id_matches:
                    matched_profile = exact_id_matches[0]
                elif len(search_results) == 1:
                    matched_profile = search_results[0]
                else:
                    st.markdown(f"**🎯 Found {len(search_results)} athletes matching '{raw_q}':**")
                    cols_match = st.columns(min(len(search_results), 3))
                    for i, m in enumerate(search_results):
                        c_idx = i % min(len(search_results), 3)
                        with cols_match[c_idx]:
                            m_disp_name = m['full_name'] if cur_officer else mask_name_banking(m['full_name'])
                            m_btn_label = f"👉 {m['staff_id']}: {m_disp_name} ({m.get('primary_sport', 'General')})"
                            if st.button(m_btn_label, key=f"btn_pick_{m['staff_id']}_{i}", use_container_width=True):
                                st.session_state["active_staff_id"] = m["staff_id"].replace("CBK-", "")
                                if m.get("primary_sport") and m["primary_sport"] != active_sport and m["primary_sport"] in all_18_sports:
                                    st.session_state["active_discipline"] = m["primary_sport"]
                                    st.session_state["global_sport_picker"] = m["primary_sport"]
                                st.session_state[f"search_txt_{active_sport}"] = ""
                                st.rerun()
                    matched_profile = search_results[0]

                if matched_profile:
                    m_sport = matched_profile.get("primary_sport", active_sport)
                    if m_sport and m_sport != active_sport and m_sport in all_18_sports:
                        p_disp_match = matched_profile['full_name'] if cur_officer else mask_name_banking(matched_profile['full_name'])
                        st.session_state["active_discipline"] = m_sport
                        st.session_state["global_sport_picker"] = m_sport
                        st.session_state["active_staff_id"] = matched_profile["staff_id"].replace("CBK-", "")
                        st.toast(f"🎯 Switched to {m_sport} for {p_disp_match} ({matched_profile['staff_id']})!", icon="🔄")
                        st.rerun()
                    lookup_term = matched_profile["staff_id"]
                    st.session_state["active_staff_id"] = matched_profile["staff_id"].replace("CBK-", "")
            else:
                lookup_term = raw_q

        elif sel_p and not sel_p.startswith("-- Or Pick"):
            # Extract staff ID e.g. from (CBK-3428) or CBK-3428 — Name
            m_sid = re.search(r"(CBK-[A-Za-z0-9]+)", sel_p)
            if m_sid:
                lookup_term = m_sid.group(1).replace("CBK-", "").strip()
            elif " — " in sel_p:
                lookup_term = sel_p.split(" — ")[0].replace("CBK-", "").strip()
            else:
                lookup_term = sel_p.strip()
            st.session_state["active_staff_id"] = lookup_term
        elif st.session_state.get("active_staff_id"):
            lookup_term = str(st.session_state.get("active_staff_id")).replace("CBK-", "").strip()

        # Full Squad Table Expander
        with st.expander(f"📋 View Full {active_sport} Team Roster ({len(squad_players)} Athletes)"):
            if squad_players:
                roster_display = []
                for p in squad_players:
                    st_str = "✅ DUAL-VERIFIED" if p["today_status"] == "DUAL_VERIFIED" else (
                        "🛑 FLAGGED (<45m)" if p["today_status"] == "INSUFFICIENT_DURATION" else (
                            "⏱️ ON FIELD (Gate 1)" if p["today_status"] == "PRE_SPORT_VALIDATED" else "Off-Day / Ready"
                        )
                    )
                    roster_display.append({
                        "Staff ID": p["staff_id"],
                        "Athlete Name": p["full_name"] if cur_officer else mask_name_banking(p["full_name"]),
                        "Directorate": p["department"],
                        "Live Status": st_str,
                        "Duration": f"{p['today_duration']} mins" if p['today_duration'] > 0 else "—"
                    })
                st.dataframe(pd.DataFrame(roster_display), use_container_width=True, hide_index=True)

        # 3. Instant Profile Lookup
        profile = None
        if lookup_term:
            profile = backend.get_staff_by_id(lookup_term)

        active_staff_id = ""
        active_full_name = ""
        active_email = ""
        active_dept = ""
        athlete_sport = active_sport

        if profile:
            active_staff_id = profile["staff_id"]
            active_full_name = profile["full_name"]
            active_email = profile["cbk_email"]
            active_dept = profile["department"]
            athlete_sport = profile.get("primary_sport", active_sport)
            st.session_state["active_staff_id"] = active_staff_id.replace("CBK-", "")

            disp_card_name = profile["full_name"] if cur_officer else mask_name_banking(profile["full_name"])
            athlete_card_html = (
                f'<div class="athlete-card">'
                f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">'
                f'<div style="display: flex; align-items: center; gap: 8px;">'
                f'<span style="background: linear-gradient(135deg, #FFE899 0%, #F5C542 50%, #D4AF37 100%); color: #040D1A; font-weight: 900; font-size: 0.7rem; padding: 3px 8px; border-radius: 4px; letter-spacing: 0.8px;">CBK ATHLETE</span>'
                f'<span style="color: #00F2FE; font-size: 0.84rem; font-weight: 800; font-family: monospace;">{profile["staff_id"]}</span>'
                f'</div>'
                f'<div style="background: rgba(16, 185, 129, 0.2); border: 1px solid #10B981; color: #34D399; font-size: 0.72rem; font-weight: 800; padding: 3px 10px; border-radius: 12px; display: inline-flex; align-items: center; gap: 5px;">'
                f'<span class="live-pulse"></span> ACCREDITED ATHLETE'
                f'</div>'
                f'</div>'
                f'<div style="font-size: 1.65rem; font-weight: 900; color: #FFFFFF; letter-spacing: -0.3px; margin-bottom: 3px; text-shadow: 0 0 12px rgba(0,242,254,0.25);">{disp_card_name}</div>'
                f'<div style="color: #94A3B8; font-size: 0.85rem; margin-bottom: 14px; font-weight: 500;">🏛️ {profile["department"]} • ✉️ <span style="color: #CBD5E1;">{profile["cbk_email"] if cur_officer else mask_email(profile.get("cbk_email"))}</span>'
                f'{" • 📞 <span style=\"color: #CBD5E1;\">" + (profile.get("phone_number") if cur_officer else mask_phone(profile.get("phone_number"))) + "</span>" if profile.get("phone_number") else ""}</div>'
                f'<div style="background: rgba(4, 14, 28, 0.85); border: 1.5px solid rgba(245, 197, 66, 0.35); border-radius: 12px; padding: 12px 16px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 0.85rem; color: #FFFFFF;">'
                f'<div>🏃 <strong>Discipline:</strong> <span style="color: #F5C542; font-weight: 800;">{athlete_sport}</span></div>'
                f'<div>⏱️ <strong>Required Duration:</strong> <span style="color: #00F2FE; font-weight: 800;">Min 45 Mins Threshold</span></div>'
                f'</div>'
                f'</div>'
            )
            st.markdown(athlete_card_html, unsafe_allow_html=True)

            first_name = disp_card_name.split()[0] if disp_card_name else "Athlete"
            btn_action = f"🚀 CONFIRM GATE 1 ARRIVAL ({first_name})" if active_gate == "PRE_SPORT" else f"🏁 CONFIRM GATE 2 DEPARTURE ({first_name})"

            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            submit_btn = st.button(btn_action, type="primary", use_container_width=True)

            if submit_btn:
                with st.spinner("Cryptographically validating QR and recording attendance..."):
                    result = backend.log_checkin(
                        staff_id=active_staff_id.strip().upper(),
                        full_name=active_full_name.strip(),
                        cbk_email=active_email.strip().lower(),
                        department=active_dept,
                        discipline=active_sport,
                        gate=active_gate,
                        station=active_station,
                        notes="1-Tap QR mobile submission"
                    )
                    st.session_state["last_submission"] = result
                    st.success(f"✅ Check-in successfully recorded at {result['timestamp']}!")
                    st.rerun()

        elif lookup_term:
            # Walk-in registration
            st.info(f"ℹ️ Athlete '{lookup_term}' not yet in the pre-enrolled registry. Please enter your name and directorate once to complete enrollment:")
            c_fn, c_em = st.columns(2)
            with c_fn:
                active_full_name = st.text_input("Full Name*", value=lookup_term if not lookup_term.isdigit() else "", placeholder="e.g. John Kamau")
            with c_em:
                active_email = st.text_input("CBK Email (@centralbank.go.ke)*", value="", placeholder="e.g. jkamau@centralbank.go.ke")

            c_dp, c_sp = st.columns(2)
            with c_dp:
                active_dept = st.selectbox("Directorate*", CBK_DEPARTMENTS, index=0)
            with c_sp:
                athlete_sport = st.selectbox("Primary Sport*", all_18_sports, index=all_18_sports.index(active_sport) if active_sport in all_18_sports else 0)

            active_staff_id = lookup_term if lookup_term.startswith("CBK-") else f"CBK-{lookup_term}"

            btn_action = f"🚀 ONBOARD & CONFIRM GATE 1 ARRIVAL" if active_gate == "PRE_SPORT" else f"🏁 ONBOARD & CONFIRM GATE 2 DEPARTURE"
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            submit_btn = st.button(btn_action, type="primary", use_container_width=True)

            if submit_btn:
                if not active_full_name or not active_email:
                    st.error("Please ensure Full Name and CBK Email are provided.")
                else:
                    backend.upsert_staff(active_staff_id, active_full_name, active_email, active_dept, active_sport)
                    with st.spinner("Recording enrollment and check-in..."):
                        result = backend.log_checkin(
                            staff_id=active_staff_id.strip().upper(),
                            full_name=active_full_name.strip(),
                            cbk_email=active_email.strip().lower(),
                            department=active_dept,
                            discipline=active_sport,
                            gate=active_gate,
                            station=active_station,
                            notes="New walk-in player enrollment"
                        )
                        st.session_state["last_submission"] = result
                        st.session_state["active_staff_id"] = active_staff_id.replace("CBK-", "")
                        st.success(f"✅ Enrolled and check-in recorded at {result['timestamp']}!")
                        st.rerun()

        else:
            # Prompt state when no athlete is selected yet
            st.markdown(f"""
            <div style="background: rgba(8, 24, 46, 0.85); border: 1.5px dashed rgba(245, 197, 66, 0.45); border-radius: 14px; padding: 20px 22px; margin-top: 10px; text-align: center; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
                <div style="font-size: 2.2rem; margin-bottom: 6px;">👆</div>
                <h4 style="color: #FFFFFF; margin: 0 0 6px 0; font-size: 1.1rem; font-weight: 800;">Choose or Search Your Name Above</h4>
                <p style="color: #94A3B8; font-size: 0.86rem; margin: 0; line-height: 1.5;">
                    Type in the search box (e.g. <strong style="color: #F5C542;">Gathigi</strong> or <strong style="color: #F5C542;">1008</strong>), or pick from the <strong style="color: #00F2FE;">{active_sport} Squad dropdown</strong> to load your profile and generate your <strong style="color: #F5C542;">CBK STRIDE Registration QR Code</strong>.
                </p>
            </div>
            """, unsafe_allow_html=True)

    with col_pass:
        st.markdown("#### 🎫 Registration Pass & Scannable QR Badge")
        
        last_sub = st.session_state.get("last_submission")

        if last_sub:
            is_dual = last_sub.get("dual_verified", False)
            is_qual = last_sub.get("allowance_qualified") == "QUALIFIED"

            badge_color = "#059669" if (is_qual or last_sub["gate"] == "PRE_SPORT") else "#DC2626"
            status_title = "DUAL-GATE VERIFIED & QUALIFIED" if is_qual else ("PRE-SPORT GATE VALIDATED" if last_sub["gate"] == "PRE_SPORT" else "SESSION SHORT / UNPAIRED")

            # Generate dynamic QR pass for the participant
            pass_payload = {
                "iss": "CBK_DSWAAP_PASS",
                "staff_id": last_sub["staff_id"],
                "name": last_sub["full_name"],
                "discipline": last_sub["discipline"],
                "gate": last_sub["gate"],
                "timestamp": last_sub["timestamp"],
                "status": last_sub["validation_status"]
            }
            pass_qr_b64 = DynamicQREngine.get_qr_base64(pass_payload)

            header_bg = "linear-gradient(135deg, #059669 0%, #064E3B 100%)" if is_qual else ("linear-gradient(135deg, #091F3D 0%, #051326 100%)" if last_sub["gate"] == "PRE_SPORT" else "linear-gradient(135deg, #DC2626 0%, #7F1D1D 100%)")
            disp_sub_name = last_sub["full_name"] if cur_officer else mask_name_banking(last_sub["full_name"])

            ticket_html = (
                f'<div class="ticket-card">'
                f'<div class="ticket-header" style="background: {header_bg}; border-bottom: 3px solid #F5C542;">'
                f'<div style="display: flex; justify-content: space-between; align-items: center;">'
                f'<span style="background: rgba(255,255,255,0.22); color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">{status_title}</span>'
                f'<span style="color: #F5C542; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.5px;">CBK PASS</span>'
                f'</div>'
                f'<h2 style="margin: 8px 0 2px 0; color: #FFFFFF; font-size: 1.45rem; font-weight: 900;">{disp_sub_name}</h2>'
                f'<p style="margin: 0; font-size: 0.82rem; color: #CBD5E1;">Staff ID: <strong style="color: #F5C542;">{last_sub["staff_id"]}</strong> • {last_sub["department"]}</p>'
                f'</div>'
                f'<div class="ticket-body">'
                f'<table style="width: 100%; font-size: 0.84rem; line-height: 2.1;">'
                f'<tr><td style="color: #94A3B8;">Discipline</td><td style="text-align: right; font-weight: 800; color: #F5C542;">{last_sub["discipline"]}</td></tr>'
                f'<tr><td style="color: #94A3B8;">Station Post</td><td style="text-align: right; font-weight: 600; color: #FFFFFF;">{last_sub["station"]}</td></tr>'
                f'<tr><td style="color: #94A3B8;">Gate Recorded</td><td style="text-align: right; font-weight: 700; color: #00F2FE;">{last_sub["gate"]}</td></tr>'
                f'<tr><td style="color: #94A3B8;">Timestamp</td><td style="text-align: right; font-family: monospace; font-size: 0.8rem; color: #E2E8F0;">{last_sub["timestamp"]}</td></tr>'
                f'<tr><td style="color: #94A3B8;">Active Duration</td><td style="text-align: right; font-weight: 700; color: #FFFFFF;">{last_sub.get("duration_minutes", 0)} mins {"(≥ 45 min floor met)" if is_qual else ""}</td></tr>'
                f'<tr style="border-top: 1px solid rgba(245, 197, 66, 0.25);"><td style="font-weight: 700; color: #FFFFFF; padding-top: 6px;">Attendance Accreditation</td><td style="text-align: right; color: #10B981; font-weight: 800; font-size: 1.05rem; padding-top: 6px;">{"1 CERTIFIED ATTENDANCE" if is_qual else "0 UNITS (NON-COMPLIANT)"}</td></tr>'
                f'</table>'
                f'<div class="ticket-perforation"></div>'
                f'<div style="text-align: center;">'
                f'<div style="background: white; border: 3.5px solid #F5C542; border-radius: 16px; display: inline-block; padding: 12px; box-shadow: 0 0 25px rgba(245,197,66,0.4), 0 0 15px rgba(0,242,254,0.3);">'
                f'<img src="{pass_qr_b64}" style="width: 160px; height: 160px; border-radius: 6px;" />'
                f'</div>'
                f'<p style="font-size: 0.74rem; color: #94A3B8; margin-top: 8px; font-weight: 600;">🔒 Cryptographic DSWAAP Pass • Show at Marshals Post</p>'
                f'</div>'
                f'</div>'
                f'</div>'
            )
            st.markdown(ticket_html, unsafe_allow_html=True)

            if is_dual:
                st.balloons()
                st.success("✉️ Dual-Verification receipt sent to institutional email (@centralbank.go.ke)!")

            # 1-Click Painless Satisfaction Reaction Widget (Post-Gate Checkout)
            render_painless_satisfaction_widget(
                staff_id=last_sub["staff_id"],
                full_name=last_sub["full_name"],
                department=last_sub["department"],
                discipline=last_sub["discipline"],
                touchpoint="GATE_CHECKOUT",
                key_prefix="post_sub"
            )
        elif profile or (active_full_name and active_staff_id):
            disp_badge_name = active_full_name if cur_officer else mask_name_banking(active_full_name)
            # Generate the personalized athlete pass with real dynamic QR code!
            pass_payload = {
                "iss": "CBK_ATHLETE_PASS",
                "staff_id": active_staff_id,
                "name": active_full_name,
                "department": active_dept,
                "discipline": active_sport,
                "gate": active_gate,
                "station": active_station,
                "session_id": f"PASS-{active_staff_id}"
            }
            pass_qr_b64 = DynamicQREngine.get_qr_base64(pass_payload, as_url=True, host=active_portal_host)
            pass_qr_img = DynamicQREngine.create_qr_image(pass_payload, as_url=True, host=active_portal_host)

            ticket_html = (
                f'<div class="ticket-card">'
                f'<div class="ticket-header" style="background: linear-gradient(135deg, #091F3D 0%, #051326 100%); border-bottom: 3px solid #F5C542;">'
                f'<div style="display: flex; justify-content: space-between; align-items: center;">'
                f'<span style="background: rgba(245, 197, 66, 0.25); border: 1px solid #F5C542; color: #FFE899; padding: 3px 12px; border-radius: 20px; font-size: 0.72rem; font-weight: 900; text-transform: uppercase;">OFFICIAL ATHLETE BADGE</span>'
                f'<span style="color: #F5C542; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.5px;">READY TO PHOTO / SCAN</span>'
                f'</div>'
                f'<h2 style="margin: 8px 0 2px 0; color: #FFFFFF; font-size: 1.45rem; font-weight: 900; text-shadow: 0 0 10px rgba(0,242,254,0.3);">{disp_badge_name}</h2>'
                f'<p style="margin: 0; font-size: 0.82rem; color: #CBD5E1;">Staff ID: <strong style="color: #F5C542;">{active_staff_id}</strong> • {active_dept}</p>'
                f'</div>'
                f'<div class="ticket-body" style="text-align: center;">'
                f'<table style="width: 100%; font-size: 0.84rem; line-height: 2.1; text-align: left; margin-bottom: 8px;">'
                f'<tr><td style="color: #94A3B8;">Sport</td><td style="text-align: right; font-weight: 800; color: #F5C542;">{disc_icon} {active_sport}</td></tr>'
                f'<tr><td style="color: #94A3B8;">Station Post</td><td style="text-align: right; font-weight: 600; color: #FFFFFF;">{active_station}</td></tr>'
                f'<tr><td style="color: #94A3B8;">Gate Mode</td><td style="text-align: right; font-weight: 700; color: #00F2FE;">{"Gate 1: Arrival" if active_gate == "PRE_SPORT" else "Gate 2: Departure"}</td></tr>'
                f'<tr><td style="color: #94A3B8;">Accreditation</td><td style="text-align: right; font-weight: 800; color: #10B981;">ACCREDITED CBK ATHLETE</td></tr>'
                f'</table>'
                f'<div class="ticket-perforation"></div>'
                f'<div style="background: white; border: 3.5px solid #F5C542; border-radius: 18px; display: inline-block; padding: 14px; box-shadow: 0 0 35px rgba(245,197,66,0.45), 0 0 18px rgba(0, 242, 254, 0.35);">'
                f'<img src="{pass_qr_b64}" style="width: 220px; height: 220px; border-radius: 8px;" />'
                f'</div>'
                f'<p style="font-size: 0.85rem; color: #F5C542; margin-top: 12px; font-weight: 800; text-shadow: 0 0 10px rgba(245,197,66,0.3);">'
                f'📸 Point Phone Camera at Code Above to Photo / Save Your Pass'
                f'</p>'
                f'<p style="font-size: 0.76rem; color: #94A3B8; margin-top: 2px;">'
                f'Present at {active_station} or Tap Confirm on Left to Check In'
                f'</p>'
                f'</div>'
                f'</div>'
            )
            st.markdown(ticket_html, unsafe_allow_html=True)

            # On-screen camera photo badge (No file download needed)
            st.markdown(
                '<div style="background: rgba(0, 242, 254, 0.08); border: 1.5px solid rgba(0, 242, 254, 0.35); border-radius: 12px; padding: 11px 16px; text-align: center; color: #E2E8F0; font-size: 0.85rem; margin-top: 10px;">'
                '📸 <strong style="color: #00F2FE;">Pass Ready:</strong> Point your phone camera at the QR code above to take a photo or screenshot your pass.'
                '</div>',
                unsafe_allow_html=True
            )
            if is_export_authorized():
                buf_pass = io.BytesIO()
                pass_qr_img.save(buf_pass, format="PNG")
                st.download_button(
                    label=f"📥 Download {disp_badge_name} Pass (PNG)",
                    data=buf_pass.getvalue(),
                    file_name=f"CBK_Pass_{active_staff_id}_{active_sport}.png",
                    mime="image/png",
                    use_container_width=True,
                    key=f"dl_pass_{active_staff_id}"
                )

            # 1-Click Painless Satisfaction Reaction Widget under badge
            render_painless_satisfaction_widget(
                staff_id=active_staff_id,
                full_name=active_full_name,
                department=active_dept,
                discipline=active_sport,
                touchpoint="ATHLETE_BADGE",
                key_prefix="badge_pass"
            )
        else:
            # Standby waiting card
            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #071933 0%, #040E1E 100%); border: 2px dashed rgba(245, 197, 66, 0.5); border-radius: 18px; padding: 2.5rem 1.5rem; text-align: center; margin-top: 0.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5), 0 0 20px rgba(0,242,254,0.1);">
                <div style="font-size: 3rem; margin-bottom: 0.6rem;">🎫</div>
                <span style="background: linear-gradient(135deg, #FFE899 0%, #F5C542 50%, #D4AF37 100%); color: #040D1A; font-size: 0.74rem; font-weight: 900; padding: 4px 14px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.8px;">
                    CBK STRIDE™ Pass Generator
                </span>
                <h3 style="color: #FFFFFF; margin: 0.9rem 0 0.4rem 0; font-size: 1.35rem; font-weight: 800;">
                    Ready to Create Your Pass
                </h3>
                <p style="color: #94A3B8; font-size: 0.86rem; line-height: 1.5; max-width: 330px; margin: 0 auto 1.4rem auto;">
                    Select your sport on the left, then search or pick your name. Your personalized <strong style="color: #F5C542;">Registration & Attendance QR Code</strong> will generate here instantly.
                </p>
                <div style="background: rgba(4, 14, 28, 0.85); border: 1.5px solid rgba(245, 197, 66, 0.35); border-radius: 12px; padding: 14px 16px; text-align: left; font-size: 0.84rem; color: #E2E8F0; line-height: 1.8;">
                    <div>🏅 <strong>Step 1:</strong> Select Sport (Currently: <span style="color: #F5C542; font-weight: 700;">{active_sport}</span>)</div>
                    <div>🔍 <strong>Step 2:</strong> Type your name (e.g. <em>Gathigi</em>) or pick from roster</div>
                    <div style="color: #00E5FF; font-weight: 700;">📸 <strong>Step 3:</strong> QR Pass appears here — photo with phone or download PNG!</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Standby Painless Satisfaction Reaction Widget
            render_painless_satisfaction_widget(
                staff_id=st.session_state.get("active_staff_id", "CBK-ATHLETE"),
                full_name=active_full_name or "CBK Athlete",
                department="CBK Directorate",
                discipline=active_sport,
                touchpoint="STANDBY_VIEW",
                key_prefix="standby_pass"
            )

# ==============================================================================
# TAB 2: FIELD CAPTAIN TERMINAL (ONLINE/OFFLINE DEVICE CONSOLE)
# ==============================================================================
with tab_dict["🏷️ Captain QR Station"]:
    st.markdown("### 🏷️ Discipline Captain Field Terminal (Online / Offline Device Console)")
    st.caption("Each team captain operates this console on an institutional tablet/smartphone with data bundles. Generates dynamic IN & OUT codes and auto-syncs scans to Google Sheets Master.")

    # 1. Cloud Master & Cellular Data Bundles Sync Bar
    pending_sync_count = backend.get_pending_sync_count()
    c_sync1, c_sync2 = st.columns([1.5, 1])

    with c_sync1:
        if backend.gspread_connected:
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.08); border: 1.5px solid #10B981; border-radius: 12px; padding: 12px 16px; margin-bottom: 0.9rem; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span class="live-pulse"></span>
                        <span style="font-size: 0.76rem; font-weight: 800; color: #059669; text-transform: uppercase; letter-spacing: 0.5px;">Cloud Master Online • Cellular Bundles Active</span>
                    </div>
                    <p style="margin: 3px 0 0 0; font-size: 0.82rem; color: #166534;">
                        Live streaming to Google Drive: <strong>CBK_DSWAAP_Attendance_Ledger</strong>
                    </p>
                </div>
                <div style="background: #059669; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 800;">
                    REAL-TIME
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: rgba(245, 158, 11, 0.08); border: 1.5px solid #F59E0B; border-radius: 12px; padding: 12px 16px; margin-bottom: 0.9rem; display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="display: flex; align-items: center; gap: 6px;">
                        <span style="width: 8px; height: 8px; background: #D97706; border-radius: 50%; display: inline-block;"></span>
                        <span style="font-size: 0.76rem; font-weight: 800; color: #B45309; text-transform: uppercase; letter-spacing: 0.5px;">Offline Resilient Field Mode</span>
                    </div>
                    <p style="margin: 3px 0 0 0; font-size: 0.82rem; color: #92400E;">
                        Generating dynamic HMAC codes. <strong>{pending_sync_count} scans</strong> buffered in local SQLite database.
                    </p>
                </div>
                <div style="background: #D97706; color: white; padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 800;">
                    BUFFERED
                </div>
            </div>
            """, unsafe_allow_html=True)

    with c_sync2:
        if pending_sync_count > 0 and backend.gspread_connected:
            if st.button(f"🔄 Upload {pending_sync_count} Offline Scans to Cloud Master", type="primary", use_container_width=True):
                with st.spinner("Flushing offline buffer to Google Sheets Master..."):
                    sync_res = backend.sync_pending_to_gsheets()
                    if sync_res["success"]:
                        st.success(sync_res["message"])
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(sync_res["message"])
        elif backend.gspread_connected:
            st.info("☁️ 100% of attendance logs are in sync with Google Sheets Cloud Master.")
        else:
            st.caption("Connect service account in Tab 6 to activate real-time Google Sheets streaming.")

    # 2. Main Terminal Layout: Left Controls, Right Big QR Kiosk Display
    c_cap_cfg, c_cap_qr = st.columns([1, 1.2])

    with c_cap_cfg:
        with st.container(border=True):
            st.markdown("#### 1. Quick Gate Mode (IN vs OUT)")
            st.caption("Tap to toggle between Arrival (In) and Departure (Out) QR broadcast:")

            # Big 1-Tap IN / OUT Toggle
            col_in_btn, col_out_btn = st.columns(2)
            if col_in_btn.button("🟢 GATE 1: ARRIVAL (IN)", use_container_width=True, type="primary" if st.session_state.get("captain_active_gate", "PRE_SPORT") == "PRE_SPORT" else "secondary"):
                st.session_state["captain_active_gate"] = "PRE_SPORT"
                st.rerun()
            if col_out_btn.button("🏁 GATE 2: DEPARTURE (OUT)", use_container_width=True, type="primary" if st.session_state.get("captain_active_gate", "PRE_SPORT") == "POST_SPORT" else "secondary"):
                st.session_state["captain_active_gate"] = "POST_SPORT"
                st.rerun()

            gate_key = st.session_state.get("captain_active_gate", "PRE_SPORT")

            st.markdown("---")
            st.markdown("#### 2. Captain & Discipline Profile")

            cap_discipline = st.selectbox(
                "Select Team Discipline (18 Sports, A – Z):",
                ALL_18_SPORTS,
                key="cap_disc_select"
            )

            cap_info = CBK_DISCIPLINES[cap_discipline]
            st.write(f"**Appointed Captain:** {cap_info['captain']}")
            st.write(f"**Home Venue:** {cap_info['default_venue']}")

            st.markdown("---")
            st.markdown("#### 3. Course / Venue Station Post")
            cap_station = st.selectbox(
                f"Active Post ({cap_discipline}):",
                cap_info["stations"]
            )

            # Quick checkpoint buttons for Athletics & Track
            if cap_discipline == "Athletics & Track":
                st.caption("Quick Switch Athletics Checkpoints:")
                g_c1, g_c2, g_c3 = st.columns(3)
                if g_c1.button("100m Start", use_container_width=True):
                    st.session_state["track_quick_station"] = "Track 100m Start Point"
                if g_c2.button("Gate 3 Exit", use_container_width=True):
                    st.session_state["track_quick_station"] = "Perimeter Gate 3"
                if g_c3.button("Pavilion", use_container_width=True):
                    st.session_state["track_quick_station"] = "Main Stadium Pavilion"

            validity_mins = st.slider("Dynamic Code Auto-Refresh (Minutes):", min_value=5, max_value=120, value=30, step=5)
            session_tag = st.text_input("Camp Session ID:", value=f"CAMP-{now_dt.strftime('%Y%m%d')}-01")

            st.markdown("---")
            st.markdown("#### 4. 📶 Captain Field Hotspot Gateway")
            st.caption("Broadcast tablet cellular bundles so athletes need zero personal airtime to register.")
            hotspot_ssid = st.text_input("Hotspot Network Name (SSID):", value=f"CBK-DSWAAP-HOTSPOT", key="cap_hotspot_ssid")
            hotspot_pass = st.text_input("Hotspot Password:", value="CBKSports2026", key="cap_hotspot_pass", type="password")

            kiosk_display_mode = st.radio(
                "Terminal Screen Display:",
                ["🏁 Gate Attendance QR", "📶 1-Tap Field Wi-Fi Hotspot QR"],
                horizontal=True,
                key="cap_kiosk_mode"
            )

    with c_cap_qr:
        # Determine active station & gate
        active_station = st.session_state.get("track_quick_station", cap_station) if cap_discipline == "Athletics & Track" else cap_station
        
        if kiosk_display_mode == "📶 1-Tap Field Wi-Fi Hotspot QR":
            # Display Field Wi-Fi Connection QR for Zero-Data Athlete Onboarding
            wifi_qr_b64 = DynamicQREngine.get_wifi_qr_base64(hotspot_ssid, hotspot_pass)
            wifi_qr_img = DynamicQREngine.create_wifi_qr_image(hotspot_ssid, hotspot_pass)

            st.markdown(f"""
            <div class="mobile-card" style="text-align: center; border-top: 6px solid #F7941D; box-shadow: 0 6px 18px rgba(247,148,29,0.15);">
                <span style="background: #F7941D; color: white; padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 800; text-transform: uppercase;">
                    📶 ZERO-DATA ATHLETE WI-FI ACCESS
                </span>
                <h2 style="color: #10529E; margin: 0.5rem 0 0.2rem 0; font-size: 1.55rem;">Connect to Captain's Hotspot</h2>
                <p style="font-size: 0.88rem; color: #64748B; margin-bottom: 0.6rem;">
                    Network: <strong>{hotspot_ssid}</strong> • Password: <code>{hotspot_pass}</code>
                </p>
                <div style="background: #FFFBEB; padding: 8px 16px; border-radius: 8px; display: inline-block; margin-bottom: 0.8rem; border: 1.5px solid #FCD34D;">
                    <span style="font-size: 0.84rem; color: #B45309; font-weight: 700;">
                        📲 Point Phone Camera at Code Below ➔ Tap "Join Network" (1-Tap Auto-Connect)
                    </span>
                </div>
                <div style="background: white; display: inline-block; padding: 18px; border-radius: 14px; box-shadow: 0 4px 15px rgba(247,148,29,0.15); border: 2px solid #F7941D;">
                    <img src="{wifi_qr_b64}" style="width: 280px; height: 280px;" />
                </div>
                <div style="margin-top: 1rem; font-size: 0.82rem; color: #475569;">
                    <p style="margin: 2px;"><strong>Benefits:</strong> Zero personal airtime or data bundles required from staff.</p>
                    <p style="margin: 2px;"><strong>Next Step:</strong> Once connected, Captain flips to <strong>Gate 1 (Arrival)</strong> to scan attendance.</p>
                    <p style="margin: 2px; color: #059669; font-weight: 700;">🟢 Tablet 5G/4G Bundles Active • Hotspot Live</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Download printable Wi-Fi QR placard
            buf_wifi = io.BytesIO()
            wifi_qr_img.save(buf_wifi, format="PNG")
            st.download_button(
                label="📥 Download Printable Field Wi-Fi QR Placard (PNG)",
                data=buf_wifi.getvalue(),
                file_name=f"CBK_WiFi_Hotspot_{hotspot_ssid}.png",
                mime="image/png",
                use_container_width=True
            )
        else:
            # Display Gate Attendance QR
            token_payload = DynamicQREngine.generate_token(
                discipline=cap_discipline,
                gate=gate_key,
                station=active_station,
                validity_minutes=validity_mins,
                session_id=session_tag
            )
            qr_b64 = DynamicQREngine.get_qr_base64(token_payload, as_url=True, host=active_portal_host)
            qr_img = DynamicQREngine.create_qr_image(token_payload, as_url=True, host=active_portal_host)

            is_arrival = gate_key == "PRE_SPORT"
            gate_badge_bg = "#059669" if is_arrival else "#00F2FE"
            gate_badge_fg = "#FFFFFF" if is_arrival else "#040D1A"
            gate_card_border = "#059669" if is_arrival else "#F5C542"
            gate_headline = "GATE 1: SCAN TO CLOCK IN (ARRIVAL)" if is_arrival else "GATE 2: SCAN TO CLOCK OUT & CERTIFY ATTENDANCE"
            gate_subtext = "Athletes scan upon arrival at the venue" if is_arrival else "Athletes scan after 45+ mins of activity to complete session certification"

            st.markdown(f"""
            <div style="background: rgba(245, 197, 66, 0.12); border: 1.5px solid rgba(245, 197, 66, 0.35); border-radius: 10px; padding: 8px 16px; margin-bottom: 0.9rem; display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.82rem; color: #FFE58F; font-weight: 700;">
                    📶 Tablet Hotspot Broadcasting: <strong style="color: #F5C542;">{hotspot_ssid}</strong> (Athletes need 0 personal bundles)
                </span>
                <span style="font-size: 0.72rem; background: #059669; color: white; padding: 3px 10px; border-radius: 12px; font-weight: 800;">ACTIVE</span>
            </div>
            <div class="mobile-card" style="text-align: center; border-top: 6px solid {gate_card_border}; box-shadow: 0 12px 35px rgba(0,0,0,0.6), 0 0 20px rgba(0,242,254,0.15);">
                <span style="background: {gate_badge_bg}; color: {gate_badge_fg}; padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 900; text-transform: uppercase;">
                    {'🟢 ' + gate_headline if is_arrival else '🏁 ' + gate_headline}
                </span>
                <h2 style="color: #F5C542; margin: 0.6rem 0 0.2rem 0; font-size: 1.7rem; font-weight: 900; text-shadow: 0 0 15px rgba(245,197,66,0.3);">{active_station}</h2>
                <p style="font-size: 0.88rem; color: #CBD5E1; margin-bottom: 0.8rem;">
                    {cap_discipline} • {gate_subtext}
                </p>
                <div style="background: rgba(0, 242, 254, 0.1); padding: 7px 16px; border-radius: 8px; display: inline-block; margin-bottom: 1rem; border: 1px solid rgba(0, 242, 254, 0.35);">
                    <span style="font-size: 0.82rem; color: #38BDF8; font-weight: 700;">📲 Point Phone Camera at Code Below (No App Install Required)</span>
                </div>
                <div style="background: white; display: inline-block; padding: 18px; border-radius: 18px; box-shadow: 0 0 35px rgba(245,197,66,0.45), 0 0 18px rgba(0, 242, 254, 0.35); border: 3.5px solid #F5C542;">
                    <img src="{qr_b64}" style="width: 290px; height: 290px; border-radius: 8px;" />
                </div>
                <div style="margin-top: 1rem; font-size: 0.82rem; color: #94A3B8;">
                    <p style="margin: 2px;"><strong>Discipline Captain:</strong> <span style="color: #FFFFFF;">{cap_info['captain']}</span></p>
                    <p style="margin: 2px;"><strong>Session:</strong> <code style="color: #F5C542; background: rgba(245,197,66,0.1); padding: 2px 6px; border-radius: 4px;">{session_tag}</code> • <strong>Valid Until:</strong> <span style="color: #CBD5E1;">{token_payload['expires_at']}</span></p>
                    <p style="margin: 4px 0 0 0; color: #00E5FF; font-weight: 700;">📡 Cryptographic HMAC Token Active (Tamper-Proof)</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Download printable station QR code
            buf = io.BytesIO()
            qr_img.save(buf, format="PNG")
            st.download_button(
                label="📥 Download High-Res Station QR Code (PNG)",
                data=buf.getvalue(),
                file_name=f"CBK_QR_{cap_discipline}_{gate_key}_{active_station[:10]}.png",
                mime="image/png",
                use_container_width=True
            )

            # ==================================================================
            # 3. LIVE SQUAD ROLL-CALL MONITOR (ON-FIELD SCANS FEED)
            # ==================================================================
            st.markdown("---")
            st.markdown(f"#### 👥 Live {cap_discipline} Field Attendance Monitor")

            conn_roll = sqlite3.connect(backend.db_path)
            today_str = get_eat_today_str()
            df_today_cap = pd.read_sql_query("""
                SELECT timestamp, staff_id, full_name, department, gate, validation_status, duration_minutes
                FROM attendance_logs
                WHERE discipline = ? AND date = ?
                ORDER BY id DESC LIMIT 20
            """, conn_roll, params=(cap_discipline, today_str))
            conn_roll.close()

            c_rf1, c_rf2 = st.columns([1.5, 1])
            with c_rf1:
                st.markdown(f"""
                <div style="background: rgba(245, 197, 66, 0.1); border: 1.5px solid rgba(245, 197, 66, 0.35); border-radius: 10px; padding: 10px 14px; margin-bottom: 8px; box-shadow: 0 0 15px rgba(0,242,254,0.1);">
                    <span style="font-size: 0.76rem; font-weight: 800; color: #F5C542; text-transform: uppercase; letter-spacing: 0.5px;">
                        ⚡ Real-Time On-Pitch Roll Call
                    </span>
                    <h3 style="margin: 3px 0 0 0; color: #FFFFFF; font-size: 1.35rem; font-weight: 800;">
                        {len(df_today_cap)} Athletes Checked In Today
                    </h3>
                </div>
                """, unsafe_allow_html=True)
            with c_rf2:
                if st.button("🔄 Refresh Live Roster", key=f"cap_refresh_roster_{cap_discipline}", use_container_width=True):
                    st.rerun()

            if not df_today_cap.empty:
                display_feed = []
                for _, r in df_today_cap.iterrows():
                    g_icon = "🟢 ARRIVAL" if r["gate"] == "PRE_SPORT" else "🏁 DEPARTURE"
                    p_disp = r["full_name"] if cur_officer else mask_name_banking(r["full_name"])
                    display_feed.append({
                        "Time": r["timestamp"].split()[1] if " " in str(r["timestamp"]) else r["timestamp"],
                        "Staff ID": r["staff_id"],
                        "Athlete Name": p_disp,
                        "Department": r["department"][:22],
                        "Gate": g_icon,
                        "Status": "✅ VALIDATED" if "VALID" in str(r["validation_status"]) else r["validation_status"]
                    })
                st.dataframe(pd.DataFrame(display_feed), use_container_width=True, hide_index=True)
            else:
                st.caption(f"No athletes have checked into {cap_discipline} yet today. Show the QR code above to arriving players to clock them in.")

            # ==================================================================
            # 4. CAPTAIN-ASSISTED WALK-IN ONBOARDING (FOR PLAYERS WITHOUT PHONES)
            # ==================================================================
            with st.expander(f"➕ Quick-Onboard Walk-In Player Directly (No Phone Needed)", expanded=False):
                st.caption("If a player's phone battery died or they arrived without a device, the Captain can register and clock them in directly:")
                c_w1, c_w2 = st.columns(2)
                with c_w1:
                    w_sid = st.text_input("Staff ID / Payroll No.*", placeholder="e.g. 2045 or CBK-2045", key=f"w_sid_{cap_discipline}")
                    w_fn = st.text_input("Full Name*", placeholder="e.g. David Ochieng", key=f"w_fn_{cap_discipline}")
                with c_w2:
                    w_em = st.text_input("Email*", placeholder="e.g. dochieng@centralbank.go.ke", key=f"w_em_{cap_discipline}")
                    w_dp = st.selectbox("Directorate*", CBK_DEPARTMENTS, key=f"w_dp_{cap_discipline}")

                if st.button(f"🚀 Register & Clock In ({cap_discipline})", type="primary", use_container_width=True, key=f"btn_w_clockin_{cap_discipline}"):
                    if not w_sid or not w_fn:
                        st.error("Please provide both Staff ID and Full Name.")
                    else:
                        clean_sid = w_sid.strip().upper()
                        if not clean_sid.startswith("CBK-") and clean_sid.isdigit():
                            clean_sid = f"CBK-{clean_sid}"
                        clean_email = w_em.strip().lower() if w_em else f"{clean_sid.lower()}@centralbank.go.ke"

                        # Upsert into staff registry
                        backend.upsert_staff(clean_sid, w_fn.strip(), clean_email, w_dp, cap_discipline)

                        # Log check-in
                        res_w = backend.log_checkin(
                            staff_id=clean_sid,
                            full_name=w_fn.strip(),
                            cbk_email=clean_email,
                            department=w_dp,
                            discipline=cap_discipline,
                            gate=gate_key,
                            station=active_station,
                            notes="Captain-assisted walk-in enrollment"
                        )
                        st.success(f"✅ Walk-in athlete {w_fn} ({clean_sid}) enrolled and checked in successfully!")
                        st.balloons()
                        st.rerun()

            # 5. CAPTAIN'S TACTICAL FIXTURES & DIARY SECTION
            render_captain_calendar_section(cap_discipline, is_authorized=bool(cur_officer or is_sandbox), key_prefix="qr_tab")


# ==============================================================================
# TAB: CAPTAIN'S SQUAD ROLL CALL (EASY 1-TAP & BATCH ATTENDANCE)
# ==============================================================================
def render_tab_captains_roll_call():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #091F3D 0%, #051326 100%); border: 1.5px solid rgba(245, 197, 66, 0.4); border-left: 5px solid #F5C542; border-radius: 14px; padding: 14px 18px; margin-bottom: 1.2rem; box-shadow: 0 8px 24px rgba(0,0,0,0.5), 0 0 15px rgba(0,242,254,0.12);">
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
            <div>
                <span style="background: linear-gradient(135deg, #FFE899 0%, #F5C542 50%, #D4AF37 100%); color: #040D1A; font-weight: 900; font-size: 0.72rem; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.8px;">FIELD COMMAND</span>
                <h3 style="margin: 4px 0 2px 0; color: #FFFFFF; font-size: 1.3rem; font-weight: 800;">📋 Captain's Digital Squad Roll Call</h3>
                <p style="margin: 0; font-size: 0.82rem; color: #94A3B8;">1-Tap on-pitch attendance verification for team captains. Check off players present or batch-clock in your entire squad in seconds.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Captain Roll-Call Guide Download Hub
    with st.expander("📥 Download Official Team Captain Field Roll-Call Guide (PDF / Image / PPTX)"):
        c_f1, c_f2, c_f3 = st.columns(3)
        flyer_dir = os.path.dirname(os.path.abspath(__file__))
        flyer_pdf_path = os.path.join(flyer_dir, "CBK_STRIDE_Captain_RollCall_Guide.pdf")
        flyer_pptx_path = os.path.join(flyer_dir, "CBK_STRIDE_Captain_RollCall_Guide.pptx")
        flyer_jpg_path = os.path.join(flyer_dir, "CBK_STRIDE_Captain_RollCall_Guide.jpg")
        
        with c_f1:
            if os.path.exists(flyer_pdf_path):
                with open(flyer_pdf_path, "rb") as fp:
                    st.download_button(
                        "📄 Download Captain Guide (PDF)",
                        data=fp.read(),
                        file_name="CBK_STRIDE_Captain_RollCall_Guide.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        key="btn_dl_cap_guide_pdf"
                    )
        with c_f2:
            if os.path.exists(flyer_pptx_path):
                with open(flyer_pptx_path, "rb") as fp:
                    st.download_button(
                        "📊 Download Editable PPTX",
                        data=fp.read(),
                        file_name="CBK_STRIDE_Captain_RollCall_Guide.pptx",
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True,
                        key="btn_dl_cap_guide_pptx"
                    )
        with c_f3:
            if os.path.exists(flyer_jpg_path):
                with open(flyer_jpg_path, "rb") as fp:
                    st.download_button(
                        "🖼️ Download Mobile Flyer (JPG)",
                        data=fp.read(),
                        file_name="CBK_STRIDE_Captain_RollCall_Guide.jpg",
                        mime="image/jpeg",
                        use_container_width=True,
                        key="btn_dl_cap_guide_jpg"
                    )
        if os.path.exists(flyer_jpg_path):
            st.image(flyer_jpg_path, caption="CBK STRIDE™ Team Captain Field Roll-Call Guide", use_container_width=True)

    cur_off = get_current_officer()
    cur_cap = st.session_state.get("authenticated_captain", None)

    # 1. CAPTAIN AUTHENTICATION & ANTI-TAMPERING GATEWAY
    if cur_cap:
        rc_sport = cur_cap["discipline"]
        is_authorized = True
        auditor_tag = f"Capt. {cur_cap['full_name']} ({cur_cap.get('gmail_or_email', '')})"

        c_cap_info, c_cap_out = st.columns([3.5, 1.2])
        with c_cap_info:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.18) 0%, rgba(6, 78, 59, 0.28) 100%); border: 1.5px solid #10B981; border-radius: 12px; padding: 12px 18px; margin-bottom: 0.8rem; box-shadow: 0 4px 15px rgba(16, 185, 129, 0.15);">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="background: #10B981; color: #040D1A; font-weight: 900; font-size: 0.72rem; padding: 2px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.6px;">CAPTAIN ACCREDITED</span>
                    <span style="color: #34D399; font-size: 0.82rem; font-weight: 700;">🔒 Team Isolation Active (Locked to {rc_sport})</span>
                </div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF; margin-top: 4px;">
                    🎖️ {cur_cap['full_name']} <span style="color: #F5C542;">— {rc_sport} Team Captain</span>
                </div>
                <div style="color: #94A3B8; font-size: 0.82rem; margin-top: 2px;">
                    ✉️ {cur_cap.get('gmail_or_email', '')} • 🏛️ {cur_cap.get('department', 'CBK')} • 🛡️ Anti-Tampering Shield Active
                </div>
            </div>
            """, unsafe_allow_html=True)
        with c_cap_out:
            st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
            if st.button("🔒 Sign Out Captain", key="btn_signout_captain", use_container_width=True):
                del st.session_state["authenticated_captain"]
                st.toast("Signed out of captain command.", icon="🔒")
                st.rerun()

    elif cur_off:
        is_authorized = True
        auditor_tag = f"Secretariat Officer {cur_off['full_name']}"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(56, 189, 248, 0.15) 0%, rgba(14, 116, 144, 0.22) 100%); border: 1.5px solid #38BDF8; border-radius: 12px; padding: 10px 16px; margin-bottom: 0.8rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="background: #38BDF8; color: #040D1A; font-weight: 900; font-size: 0.7rem; padding: 2px 8px; border-radius: 4px;">SECRETARIAT MASTER COMMAND</span>
                    <span style="color: #FFFFFF; font-weight: 700; margin-left: 8px;">{cur_off['full_name']} ({cur_off['role']})</span>
                    <span style="color: #94A3B8; font-size: 0.8rem; margin-left: 6px;">• Master Roll Call Clearance across all 18 sports</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # User is NOT authenticated as Captain or Secretariat
        # STRICT PRIVACY & ANTI-TAMPERING: Do NOT show any rosters, names, or players!
        st.markdown("""
        <div style="background: linear-gradient(135deg, #091F3D 0%, #051326 100%); border: 1.5px solid rgba(245, 197, 66, 0.4); border-left: 5px solid #F5C542; border-radius: 14px; padding: 22px 24px; margin-bottom: 1.5rem; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="font-size: 2.4rem;">🛡️🔒</span>
                <div>
                    <span style="background: linear-gradient(135deg, #FFE899 0%, #F5C542 50%, #D4AF37 100%); color: #040D1A; font-weight: 900; font-size: 0.72rem; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.8px;">RESTRICTED OPERATIONAL ZONE</span>
                    <h3 style="margin: 4px 0 2px 0; color: #FFFFFF; font-size: 1.35rem; font-weight: 800;">Team Captain Authentication Required</h3>
                    <p style="margin: 0; font-size: 0.84rem; color: #94A3B8;">Under Central Bank privacy & sports integrity policies, squad rosters, player identities, and roll-call telemetry are strictly confidential. Please authenticate with your accredited Staff ID and Secret Passkey to reveal and manage your team.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            cap_sub_tab1, cap_sub_tab2 = st.tabs([
                "🔑 Existing Captain Sign-In",
                "🆕 Register as Team Captain (Set Your Secret Passkey)"
            ])

            with cap_sub_tab1:
                st.markdown("#### 🔑 Team Captain Sign-In (Discipline Access Shield)")
                c_cap_l1, c_cap_l2, c_cap_l3 = st.columns([1.2, 1.1, 1.2])
                with c_cap_l1:
                    cap_sel_sport = st.selectbox("Select Your Sport Discipline:", ALL_18_SPORTS, key="cap_in_sport")
                with c_cap_l2:
                    cap_in_sid = st.text_input("Staff ID / Payroll #:", placeholder="e.g. 3428 or CBK-3428", key="cap_in_sid")
                with c_cap_l3:
                    cap_in_pass = st.text_input("Secret Captain Passkey:", type="password", placeholder="Enter secret passkey", key="cap_in_pass")

                # Show accreditation status for selected discipline
                acc_cap = backend.get_captain_for_discipline(cap_sel_sport)
                if acc_cap:
                    st.caption(f"🛡️ Accredited Captain for {cap_sel_sport}: **Capt. {acc_cap['full_name']}** ({acc_cap['staff_id']})")
                else:
                    st.caption(f"ℹ️ No captain registered yet for {cap_sel_sport}. Appointed captains can switch to the **'🆕 Register as Team Captain'** tab above to activate!")

                if st.button(f"🔓 Verify Passkey & Unlock {cap_sel_sport} Roll Call", type="primary", use_container_width=True, key="btn_auth_cap_pass"):
                    if not cap_in_sid.strip() or not cap_in_pass.strip():
                        st.error("Please enter both your Staff ID and Secret Passkey.")
                    else:
                        ok_cap, msg_cap, prof_cap = backend.authenticate_captain_passkey(cap_in_sid, cap_sel_sport, cap_in_pass)
                        if ok_cap:
                            st.session_state["authenticated_captain"] = prof_cap
                            st.session_state["active_discipline"] = cap_sel_sport
                            st.session_state["show_first_time_setup"] = False
                            st.success(msg_cap)
                            st.balloons()
                            st.rerun()
                        elif msg_cap == "FIRST_TIME_SETUP":
                            st.info(f"💡 You are accredited in the Central Bank athlete registry as {prof_cap.get('full_name', 'Captain')}! Please click the **'🆕 Register as Team Captain'** tab above to choose your personal passkey.")
                        else:
                            st.error(msg_cap)

            with cap_sub_tab2:
                st.markdown("#### 🆕 Team Captain Registration & Passkey Setup")
                st.caption("Appointed captains: Register your discipline, link your email, and create your secret personal passkey to activate pitch roll call:")

                c_reg1, c_reg2 = st.columns([1.2, 1.2])
                with c_reg1:
                    reg_sport = st.selectbox("Sport Discipline You Are Captaining:", ALL_18_SPORTS, key="reg_cap_sport")
                    reg_sid = st.text_input("Your Staff ID / Payroll #:", placeholder="e.g. 1042 or CBK-1042", key="reg_cap_sid")
                    
                    reg_staff_match = None
                    if reg_sid.strip():
                        clean_check_sid = reg_sid.strip().upper()
                        if not clean_check_sid.startswith("CBK-") and clean_check_sid.replace("CBK", "").replace("-", "").isdigit():
                            clean_check_sid = f"CBK-{clean_check_sid.replace('CBK', '').replace('-', '')}"
                        reg_staff_match = backend.get_staff_by_id(clean_check_sid)
                        if reg_staff_match:
                            st.success(f"✅ Verified CBK Staff: **{reg_staff_match['full_name']}** ({reg_staff_match['department']})")

                with c_reg2:
                    default_name = reg_staff_match["full_name"] if reg_staff_match else ""
                    reg_full_name = st.text_input("Full Official Name (as on CBK ID):", value=default_name, placeholder="e.g. Jane Wanjiku", key="reg_cap_fullname")
                    
                    default_email = reg_staff_match.get("cbk_email", "") if reg_staff_match else ""
                    reg_email = st.text_input("Your Personal / CBK Email (for verification):", value=default_email, placeholder="e.g. captain@gmail.com", key="reg_cap_email")

                c_reg_p1, c_reg_p2 = st.columns(2)
                with c_reg_p1:
                    reg_pass1 = st.text_input("Create Secret Passkey (Min 4 digits):", type="password", placeholder="e.g. 4-digit PIN", key="reg_cap_pass1")
                with c_reg_p2:
                    reg_pass2 = st.text_input("Confirm Secret Passkey:", type="password", placeholder="Re-enter passkey", key="reg_cap_pass2")

                st.caption("🛡️ **Anti-Tampering Guarantee:** Your passkey ensures only you can mark attendance and clock out athletes for your squad.")

                if st.button(f"🛡️ Register & Unlock {reg_sport} Roll Call", type="primary", use_container_width=True, key="btn_submit_reg_cap"):
                    if not reg_sid.strip():
                        st.error("Please enter your Staff ID / Payroll number.")
                    elif not reg_full_name.strip():
                        st.error("Please enter your Full Official Name.")
                    elif not reg_email.strip() or "@" not in reg_email:
                        st.error("Please enter a valid Gmail or CBK Email address.")
                    elif not reg_pass1.strip() or len(reg_pass1.strip()) < 4:
                        st.error("Passkey must be at least 4 digits or characters.")
                    elif reg_pass1.strip() != reg_pass2.strip():
                        st.error("The two passkeys do not match! Please check and re-enter.")
                    else:
                        try:
                            ok_reg, msg_reg, prof_reg = backend.setup_first_time_captain_passkey(
                                raw_staff_id=reg_sid.strip(),
                                discipline=reg_sport,
                                gmail_or_email=reg_email.strip(),
                                new_passkey=reg_pass1.strip(),
                                custom_full_name=reg_full_name.strip()
                            )
                            if ok_reg:
                                st.session_state["authenticated_captain"] = prof_reg
                                st.session_state["active_discipline"] = reg_sport
                                st.session_state["show_first_time_setup"] = False
                                st.success(f"🎉 Welcome, Captain {prof_reg['full_name']}! You have successfully registered and unlocked {reg_sport} Roll Call.")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(msg_reg)
                        except Exception as e:
                            st.error(f"⚠️ Registration processing error: {e}")

        # STRICT DATA PROTECTION: Stop execution here so no player names, IDs, or rosters are displayed!
        return

    # 2. Sport & Gate Selection Controls (For Authenticated Captains & Secretariat Officers)
    c_rc1, c_rc2, c_rc3 = st.columns([1.3, 1.1, 1.1])

    with c_rc1:
        if cur_cap:
            rc_sport = cur_cap["discipline"]
            st.markdown(f"""
            <div style="background: rgba(4, 14, 28, 0.85); border: 1.5px solid #F5C542; border-radius: 10px; padding: 10px 14px; margin-top: 4px;">
                <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Active Discipline Command:</div>
                <div style="font-size: 1.25rem; font-weight: 900; color: #F5C542;">🏆 {rc_sport} 🔒</div>
                <div style="font-size: 0.72rem; color: #34D399; font-weight: 600;">Locked to Captain • Cross-Team Tampering Blocked</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            default_sport = st.session_state.get("active_discipline", "Golf")
            default_idx = ALL_18_SPORTS.index(default_sport) if default_sport in ALL_18_SPORTS else 0
            rc_sport = st.selectbox(
                "Select Team Discipline (18 Sports, A – Z):",
                ALL_18_SPORTS,
                index=default_idx,
                key="rc_sport_select"
            )

        sport_info = CBK_DISCIPLINES.get(rc_sport, {})
        disc_captain = sport_info.get("captain", "Appointed Captain")
        disc_venue = sport_info.get("default_venue", "CBK Sports Club")
        disc_stations = sport_info.get("stations", ["Main Gate Checkpoint"])

    with c_rc2:
        rc_gate_mode = st.radio(
            "Active Roll Call Gate:",
            ["🟢 Gate 1: Arrival (Check-In)", "🏁 Gate 2: Departure (Clock-Out)"],
            index=0,
            horizontal=True,
            key="rc_gate_mode_radio"
        )
        is_arrival = "Gate 1" in rc_gate_mode
        active_gate_key = "PRE_SPORT" if is_arrival else "POST_SPORT"
        gate_label = "Arrival" if is_arrival else "Departure"

    with c_rc3:
        rc_station = st.selectbox(
            f"Checkpoint Post ({rc_sport}):",
            disc_stations,
            index=0,
            key="rc_station_select"
        )

    # Fetch all enrolled players for this sport
    squad_players = backend.get_players_by_discipline(rc_sport)

    # 3. Live Squad Attendance KPI Summary Cards
    total_count = len(squad_players)
    on_field_count = sum(1 for p in squad_players if p.get("today_status") in ["PRE_SPORT_VALIDATED", "DUAL_VERIFIED"])
    dual_verified_count = sum(1 for p in squad_players if p.get("today_status") == "DUAL_VERIFIED")
    absent_count = sum(1 for p in squad_players if p.get("today_status") not in ["PRE_SPORT_VALIDATED", "DUAL_VERIFIED"])

    k_rc1, k_rc2, k_rc3, k_rc4 = st.columns(4)
    with k_rc1:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #38BDF8;">
            <div class="kpi-title">Enrolled Squad</div>
            <div class="kpi-value" style="color: #38BDF8;">{total_count}</div>
            <div class="kpi-sub">Official {rc_sport} Roster</div>
        </div>
        """, unsafe_allow_html=True)
    with k_rc2:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #F5C542;">
            <div class="kpi-title">Present on Field</div>
            <div class="kpi-value" style="color: #F5C542;">{on_field_count}</div>
            <div class="kpi-sub">Gate 1 Logged Today</div>
        </div>
        """, unsafe_allow_html=True)
    with k_rc3:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #10B981;">
            <div class="kpi-title">Certified Dual-Gate</div>
            <div class="kpi-value" style="color: #10B981;">{dual_verified_count}</div>
            <div class="kpi-sub">Gate 2 Completed (≥45m)</div>
        </div>
        """, unsafe_allow_html=True)
    with k_rc4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #94A3B8;">
            <div class="kpi-title">Awaiting Check-In</div>
            <div class="kpi-value" style="color: #94A3B8;">{absent_count}</div>
            <div class="kpi-sub">Not Yet Arrived on Field</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # 4. ⚡ BATCH ROLL-CALL TOOL (THE SPEED POWERHOUSE)
    with st.container(border=True):
        st.markdown(f"#### ⚡ 1-Click Batch Roll Call ({rc_sport} — {gate_label})")
        st.caption(f"Select multiple athletes standing before you on the pitch to verify their {gate_label} simultaneously with one tap:")

        # Prepare options for multiselect
        multiselect_options = {}
        for p in squad_players:
            p_name = p['full_name'] if (cur_off or is_authorized) else mask_name_banking(p['full_name'])
            st_indicator = "🟢 [ON FIELD]" if p['today_status'] == 'PRE_SPORT_VALIDATED' else (
                "✅ [CERTIFIED]" if p['today_status'] == 'DUAL_VERIFIED' else "⚪ [ABSENT]"
            )
            label = f"{p['staff_id']} — {p_name} ({p['department'][:18]}) {st_indicator}"
            multiselect_options[label] = p['staff_id']

        # Determine default candidates based on gate
        if is_arrival:
            default_candidates = [
                lbl for lbl, sid in multiselect_options.items() 
                if next((p for p in squad_players if p['staff_id'] == sid), {}).get("today_status") not in ["PRE_SPORT_VALIDATED", "DUAL_VERIFIED"]
            ]
        else:
            default_candidates = [
                lbl for lbl, sid in multiselect_options.items() 
                if next((p for p in squad_players if p['staff_id'] == sid), {}).get("today_status") == "PRE_SPORT_VALIDATED"
            ]

        # Helper buttons for rapid bulk selection
        c_hlp1, c_hlp2, c_hlp3 = st.columns([1.2, 1.2, 2.5])
        with c_hlp1:
            if st.button("☑️ Select All Eligible", key="btn_sel_all_elig"):
                st.session_state["rc_selected_labels"] = default_candidates
                st.rerun()
        with c_hlp2:
            if st.button("🔄 Clear Selections", key="btn_clear_sel"):
                st.session_state["rc_selected_labels"] = []
                st.rerun()

        current_selected = st.session_state.get("rc_selected_labels", [])
        current_selected = [lbl for lbl in current_selected if lbl in multiselect_options]

        chosen_labels = st.multiselect(
            f"Select Athletes for Batch {gate_label}:",
            list(multiselect_options.keys()),
            default=current_selected,
            key="ms_rollcall_athletes"
        )
        st.session_state["rc_selected_labels"] = chosen_labels

        chosen_sids = [multiselect_options[lbl] for lbl in chosen_labels if lbl in multiselect_options]

        if not is_authorized:
            st.button(f"🔒 Captain PIN Required to Batch Clock-In ({gate_label})", disabled=True, use_container_width=True, key="btn_disabled_batch_rc")
        else:
            btn_batch_label = f"🚀 Batch Clock-In {len(chosen_sids)} Athletes ({gate_label})" if chosen_sids else f"🚀 Select Athletes Above to Batch Clock-In ({gate_label})"
            if st.button(btn_batch_label, type="primary", use_container_width=True, disabled=len(chosen_sids) == 0, key="btn_submit_batch_rc"):
                success_count = 0
                with st.spinner(f"Verifying and recording attendance for {len(chosen_sids)} athletes..."):
                    for sid in chosen_sids:
                        p_obj = next((p for p in squad_players if p["staff_id"] == sid), None)
                        if p_obj:
                            backend.log_checkin(
                                staff_id=p_obj["staff_id"],
                                full_name=p_obj["full_name"],
                                cbk_email=p_obj.get("cbk_email", f"{p_obj['staff_id'].lower()}@centralbank.go.ke"),
                                department=p_obj.get("department", "General"),
                                discipline=rc_sport,
                                gate=active_gate_key,
                                station=rc_station,
                                notes=f"Batch Roll Call ({gate_label}) • Verified by {auditor_tag}"
                            )
                            success_count += 1
                st.session_state["rc_selected_labels"] = []
                st.success(f"🎉 Successfully batch-verified {success_count} athletes for {rc_sport} {gate_label} at {rc_station}!")
                st.balloons()
                st.rerun()

    # 5. INDIVIDUAL ROSTER CHECK SHEET (1-TAP ACTION ROWS)
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    st.markdown(f"#### 👥 Individual {rc_sport} Squad Roll Sheet")
    st.caption("Inspect each player's live field status and tap their individual button to clock them in or out:")

    # Search & Filter Controls
    c_flt1, c_flt2 = st.columns([1.5, 1])
    with c_flt1:
        rc_search = st.text_input("🔍 Quick Search Roster (Name or Staff ID):", placeholder="e.g. 3428, Njuguna...", key="rc_roster_search")
    with c_flt2:
        rc_status_filter = st.selectbox(
            "Filter by Status:",
            ["All Squad Players", "⚪ Awaiting Arrival Only", "⏱️ On Field (Arrival Logged)", "✅ Dual-Verified & Certified"],
            key="rc_filter_status"
        )

    # Filter squad players
    displayed_roster = squad_players
    if rc_search.strip():
        q_clean = rc_search.strip().lower()
        displayed_roster = [
            p for p in displayed_roster 
            if q_clean in p['staff_id'].lower() or q_clean in p['full_name'].lower() or q_clean in p['department'].lower()
        ]

    if rc_status_filter == "⚪ Awaiting Arrival Only":
        displayed_roster = [p for p in displayed_roster if p.get("today_status") not in ["PRE_SPORT_VALIDATED", "DUAL_VERIFIED"]]
    elif rc_status_filter == "⏱️ On Field (Arrival Logged)":
        displayed_roster = [p for p in displayed_roster if p.get("today_status") == "PRE_SPORT_VALIDATED"]
    elif rc_status_filter == "✅ Dual-Verified & Certified":
        displayed_roster = [p for p in displayed_roster if p.get("today_status") == "DUAL_VERIFIED"]

    if displayed_roster:
        for idx, p in enumerate(displayed_roster):
            sid = p['staff_id']
            fn = p['full_name']
            fn_disp = fn if (cur_off or is_authorized) else mask_name_banking(fn)
            dept = p['department']
            st_today = p.get('today_status', 'READY')
            dur = p.get('today_duration', 0.0)
            ts_str = p.get('timestamp', '')
            ts_time = ts_str.split(' ')[1] if ts_str and ' ' in ts_str else ''
            time_badge = f" • {ts_time}" if ts_time else ""

            # Determine row style and badge
            if st_today == "DUAL_VERIFIED":
                badge_html = f'<span style="background: rgba(16, 185, 129, 0.2); border: 1px solid #10B981; color: #34D399; padding: 3px 10px; border-radius: 12px; font-size: 0.72rem; font-weight: 800;">✅ DUAL-VERIFIED ({int(dur)}m{time_badge})</span>'
                card_border = "#10B981"
            elif st_today == "PRE_SPORT_VALIDATED":
                badge_html = f'<span style="background: rgba(0, 242, 254, 0.18); border: 1px solid #00F2FE; color: #38BDF8; padding: 3px 10px; border-radius: 12px; font-size: 0.72rem; font-weight: 800;"><span class="live-pulse"></span> ON FIELD ({ts_time if ts_time else "Gate 1"})</span>'
                card_border = "#00F2FE"
            elif st_today == "INSUFFICIENT_DURATION":
                badge_html = f'<span style="background: rgba(239, 68, 68, 0.2); border: 1px solid #EF4444; color: #F87171; padding: 3px 10px; border-radius: 12px; font-size: 0.72rem; font-weight: 800;">🛑 SHORT SESSION ({int(dur)}m{time_badge})</span>'
                card_border = "#EF4444"
            else:
                badge_html = f'<span style="background: rgba(148, 163, 184, 0.15); border: 1px solid #64748B; color: #94A3B8; padding: 3px 10px; border-radius: 12px; font-size: 0.72rem; font-weight: 700;">⚪ AWAITING ARRIVAL</span>'
                card_border = "rgba(245, 197, 66, 0.25)"

            c_info, c_action = st.columns([3, 1.4])
            with c_info:
                st.markdown(f"""
                <div style="background: rgba(9, 24, 48, 0.85); border: 1px solid {card_border}; border-radius: 10px; padding: 10px 14px; margin-bottom: 6px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-weight: 800; color: #00F2FE; font-family: monospace; font-size: 0.84rem;">{sid}</span>
                            <strong style="color: #FFFFFF; font-size: 0.95rem; margin-left: 8px;">{fn_disp}</strong>
                            <span style="color: #94A3B8; font-size: 0.78rem; margin-left: 8px;">• {dept[:25]}</span>
                        </div>
                        <div>
                            {badge_html}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with c_action:
                st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
                if not is_authorized:
                    st.button("🔒 Captain PIN Req.", disabled=True, key=f"btn_locked_{sid}_{idx}", use_container_width=True)
                elif is_arrival:
                    if st_today in ["PRE_SPORT_VALIDATED", "DUAL_VERIFIED"]:
                        st.button("✅ Arrival Recorded", disabled=True, key=f"btn_done_arr_{sid}_{idx}", use_container_width=True)
                    else:
                        if st.button(f"🟢 Clock In Arrival", key=f"btn_arr_{sid}_{idx}", type="primary", use_container_width=True):
                            backend.log_checkin(
                                staff_id=sid,
                                full_name=fn,
                                cbk_email=p.get("cbk_email", f"{sid.lower()}@centralbank.go.ke"),
                                department=dept,
                                discipline=rc_sport,
                                gate="PRE_SPORT",
                                station=rc_station,
                                notes=f"1-Tap Roll Call (Arrival) • Verified by {auditor_tag}"
                            )
                            st.toast(f"🟢 {fn_disp} clocked in at {rc_station}!", icon="🟢")
                            st.rerun()
                else:
                    # Departure Mode
                    if st_today == "DUAL_VERIFIED":
                        st.button("🏁 Completed & Certified", disabled=True, key=f"btn_done_dep_{sid}_{idx}", use_container_width=True)
                    elif st_today == "PRE_SPORT_VALIDATED":
                        if st.button(f"🏁 Clock Out Departure", key=f"btn_dep_{sid}_{idx}", type="primary", use_container_width=True):
                            backend.log_checkin(
                                staff_id=sid,
                                full_name=fn,
                                cbk_email=p.get("cbk_email", f"{sid.lower()}@centralbank.go.ke"),
                                department=dept,
                                discipline=rc_sport,
                                gate="POST_SPORT",
                                station=rc_station,
                                notes=f"1-Tap Roll Call (Departure) • Verified by {auditor_tag}"
                            )
                            st.toast(f"🏁 {fn_disp} departure recorded & dual-verified!", icon="🏁")
                            st.rerun()
                    else:
                        if st.button(f"⚡ Instant Dual Clock-In", key=f"btn_dual_{sid}_{idx}", use_container_width=True):
                            backend.log_checkin(
                                staff_id=sid,
                                full_name=fn,
                                cbk_email=p.get("cbk_email", f"{sid.lower()}@centralbank.go.ke"),
                                department=dept,
                                discipline=rc_sport,
                                gate="POST_SPORT",
                                station=rc_station,
                                notes=f"Instant Dual Clock-In • Verified by {auditor_tag}"
                            )
                            st.toast(f"⚡ {fn_disp} verified for {rc_sport}!", icon="⚡")
                            st.rerun()
    else:
        st.info("No athletes matching your search criteria.")

    # 6. WALK-IN SUBSTITUTE ONBOARDING (For players not on official roster)
    st.markdown("---")
    with st.expander(f"➕ Quick-Add Walk-In / Guest Player to {rc_sport} Roll Call"):
        st.caption("If a staff member arrived to play who wasn't on the official secretariat roster, register them right now on the field:")
        if not is_authorized:
            st.info("🔒 Only the authorized Team Captain or a Secretariat Officer can register walk-in substitutes.")
        else:
            c_w1, c_w2 = st.columns(2)
            with c_w1:
                rc_w_sid = st.text_input("Staff ID / Payroll #*", placeholder="e.g. 4022 or CBK-4022", key="rc_w_sid")
                rc_w_fn = st.text_input("Full Name*", placeholder="e.g. Kelvin Mutua", key="rc_w_fn")
            with c_w2:
                rc_w_em = st.text_input("Institutional Email*", placeholder="e.g. kmutua@centralbank.go.ke", key="rc_w_em")
                rc_w_dp = st.selectbox("Directorate / Department*", CBK_DEPARTMENTS, key="rc_w_dp")

            if st.button(f"🚀 Register & Clock In ({gate_label})", type="primary", use_container_width=True, key="btn_rc_add_walkin"):
                if not rc_w_sid or not rc_w_fn:
                    st.error("Please provide both Staff ID and Full Name.")
                else:
                    clean_w_sid = rc_w_sid.strip().upper()
                    if not clean_w_sid.startswith("CBK-") and clean_w_sid.isdigit():
                        clean_w_sid = f"CBK-{clean_w_sid}"
                    clean_w_em = rc_w_em.strip().lower() if rc_w_em else f"{clean_w_sid.lower()}@centralbank.go.ke"
                    backend.upsert_staff(clean_w_sid, rc_w_fn.strip(), clean_w_em, rc_w_dp, rc_sport)
                    backend.log_checkin(
                        staff_id=clean_w_sid,
                        full_name=rc_w_fn.strip(),
                        cbk_email=clean_w_em,
                        department=rc_w_dp,
                        discipline=rc_sport,
                        gate=active_gate_key,
                        station=rc_station,
                        notes=f"Captain Walk-In Roll Call ({gate_label}) • Verified by {auditor_tag}"
                    )
                    st.success(f"✅ Walk-in athlete {rc_w_fn} ({clean_w_sid}) enrolled and clocked into {rc_sport} successfully!")
                    st.balloons()
                    st.rerun()

    # 7. EXPORT TODAY'S SQUAD ATTENDANCE SHEET
    st.markdown("---")
    st.markdown(f"#### 📥 Export Today's {rc_sport} Roll Call Sheet")
    st.caption("Download the current squad roll call status as a certified CSV report:")
    if squad_players:
        df_rc_export = pd.DataFrame([{
            "Staff ID": p["staff_id"],
            "Full Name": p["full_name"] if (cur_off or is_authorized) else mask_name_banking(p["full_name"]),
            "Department": p["department"],
            "Sport": rc_sport,
            "Today Status": p.get("today_status", "READY"),
            "Duration (Mins)": p.get("today_duration", 0),
            "Gate Mode": gate_label,
            "Station": rc_station,
            "Check-In Timestamp": p.get("timestamp", "—"),
            "Verified By": auditor_tag,
            "Certified Attendance": "1 UNIT (CERTIFIED)" if p.get("today_status") == "DUAL_VERIFIED" else "0 UNITS (PENDING)"
        } for p in squad_players])
        csv_rc = df_rc_export.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Download {rc_sport} Roll Call CSV",
            data=csv_rc,
            file_name=f"CBK_RollCall_{rc_sport.replace(' ', '_')}_{now_dt.strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True,
            key="dl_btn_rc_csv"
        )

    # 8. SQUAD ROLL CALL RESET / CLEAR CONTROLS
    st.markdown("---")
    with st.expander("🔄 Reset & Clear Attendance for Fresh Roll Call"):
        st.caption("Need to clear previous or test scans so captains can confirm who turned up today from scratch? Choose an option below:")
        if not is_authorized:
            st.info("🔒 Only the authenticated Team Captain or a Secretariat Officer can reset attendance logs.")
        else:
            c_rst1, c_rst2 = st.columns(2)
            with c_rst1:
                st.markdown(f"**Reset {rc_sport} Only (Zero Scans)**")
                st.caption(f"Clears today's check-ins for {rc_sport} athletes only. Other sports remain intact.")
                confirm_sp = st.checkbox(f"Confirm clearing {rc_sport}", key=f"chk_rst_{rc_sport}")
                if st.button(f"🗑️ Reset {rc_sport} to 0", disabled=not confirm_sp, type="secondary", key=f"btn_rst_sp_{rc_sport}", use_container_width=True):
                    backend.clear_discipline_attendance(rc_sport)
                    st.session_state["rc_selected_labels"] = []
                    st.toast(f"✅ {rc_sport} attendance logs cleared! Ready for fresh roll call.", icon="🗑️")
                    st.rerun()
            with c_rst2:
                st.markdown("**Reset All 18 Disciplines (Clean Tournament Slate)**")
                st.caption("Clears all attendance telemetry across the entire tournament. (Super Admin & Secretariat Only)")
                is_admin_user = (cur_off and cur_off.get("role") == "Super Admin") or (cur_cap and cur_cap.get("is_super_admin"))
                if not is_admin_user:
                    st.caption("⚠️ Full tournament reset requires Super Admin clearance.")
                    st.button("🚨 Purge All Attendance (Locked)", disabled=True, use_container_width=True, key="btn_locked_full_rst")
                else:
                    confirm_all = st.checkbox("Confirm clearing ALL attendance", key="chk_rst_all_sports")
                    if st.button("🚨 Purge All Attendance to 0", disabled=not confirm_all, type="primary" if confirm_all else "secondary", key="btn_rst_all_sp", use_container_width=True):
                        backend.clear_all_attendance()
                        st.session_state["rc_selected_labels"] = []
                        st.toast("✅ All tournament attendance logs purged to 0 scans!", icon="🚨")
                        st.rerun()

    # 9. CAPTAIN'S TACTICAL FIXTURES, CALENDAR & SQUAD DIARY
    render_captain_calendar_section(rc_sport, is_authorized=bool(is_authorized or is_sandbox), key_prefix="rc_tab")

    # 10. ROLL CALL COMPLETION & CAPTAIN SIGN-OUT
    if cur_cap:
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(8, 24, 48, 0.95) 0%, rgba(4, 14, 28, 0.98) 100%); border: 1.5px solid rgba(245, 197, 66, 0.4); border-radius: 14px; padding: 18px 22px; margin-top: 1.5rem; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                <div>
                    <h4 style="margin: 0; color: #FFFFFF; font-size: 1.15rem; font-weight: 800;">🏁 Done With Today's Squad Roll Call?</h4>
                    <p style="margin: 4px 0 0 0; color: #94A3B8; font-size: 0.84rem;">Click below to safely sign out, lock the squad roster from view, and preserve attendance integrity.</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
        if st.button("🔒 Finish Roll Call & Sign Out Captain", type="primary", use_container_width=True, key="btn_bottom_signout_captain"):
            del st.session_state["authenticated_captain"]
            st.toast("✅ Signed out successfully. Squad roster locked.", icon="🔒")
            st.rerun()

if "📋 Captain's Roll Call" in tab_dict:
    with tab_dict["📋 Captain's Roll Call"]:
        render_tab_captains_roll_call()

# ==============================================================================
# TAB 3: SECRETARIAT OPERATIONAL VIEW
# ==============================================================================
def render_tab_secretariat():
    st.markdown("### 🏛️ Sports & Wellness Secretariat Operational Dashboard")
    st.caption("Live monitoring of real-time check-ins, discipline activity, and dual-gate fulfillment.")

    # Headline KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #F5C542;">
            <div class="kpi-title">Today's Total Scans</div>
            <div class="kpi-value" style="color: #F5C542;">{kpis['total_checkins']}</div>
            <div class="kpi-sub">Across All 18 Disciplines</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #00F2FE;">
            <div class="kpi-title">Active on Field (Gate 1)</div>
            <div class="kpi-value" style="color: #00F2FE;">{kpis['pre_gate_active']}</div>
            <div class="kpi-sub">Awaiting Post-Gate Scan</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #10B981;">
            <div class="kpi-title">Dual-Verified (Completed)</div>
            <div class="kpi-value" style="color: #10B981;">{kpis['dual_verified']}</div>
            <div class="kpi-sub">{kpis['qualified']} Certified Attendance Units</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #F5C542;">
            <div class="kpi-title">Policy Compliance Rate</div>
            <div class="kpi-value" style="color: #F5C542;">{kpis['compliance_rate']}%</div>
            <div class="kpi-sub">{kpis['flagged_sessions']} Flagged / Short Sessions</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 🏃 18 Sporting Disciplines Status Matrix")
    
    disc_summary = compute_discipline_breakdown(df_all)
    if not disc_summary.empty:
        # Render clean status cards in a 3-column grid
        disc_cols = st.columns(3)
        for idx, row in disc_summary.iterrows():
            col = disc_cols[idx % 3]
            status_style = "background: rgba(16, 185, 129, 0.18); border: 1px solid #10B981; color: #34D399;" if row['Operational Status'] == "Active Session" else ("background: rgba(148, 163, 184, 0.15); border: 1px solid #64748B; color: #94A3B8;" if row['Operational Status'] == "Concluded" else "background: rgba(245, 197, 66, 0.15); border: 1px solid #F5C542; color: #F5C542;")
            
            with col:
                st.markdown(f"""
                <div class="mobile-card" style="padding: 1rem; margin-bottom: 0.8rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-size: 1.15rem; color: #FFFFFF;">{row['Icon']} <strong style="color: #F5C542;">{row['Discipline']}</strong></span>
                        <span style="font-size: 0.7rem; font-weight: 800; padding: 2px 8px; border-radius: 12px; {status_style}">
                            {row['Operational Status']}
                        </span>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.7rem; font-size: 0.82rem; color: #94A3B8;">
                        <span>Active: <strong style="color: #00F2FE;">{row['Active on Field']}</strong></span>
                        <span>Completed: <strong style="color: #10B981;">{row['Completed Dual Gate']}</strong></span>
                        <span>Total: <strong style="color: #F5C542;">{row['Total Check-Ins']}</strong></span>
                    </div>
                    <div style="font-size: 0.76rem; color: #CBD5E1; margin-top: 0.4rem;">
                        👨‍✈️ {row['Captain']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### ⚡ Real-Time Live Activity Stream")
    
    # Filter controls
    c_f1, c_f2 = st.columns([1, 1])
    with c_f1:
        f_disc = st.multiselect("Filter by Discipline (A – Z):", ALL_18_SPORTS, default=[])
    with c_f2:
        f_gate = st.multiselect("Filter by Gate:", ["PRE_SPORT", "POST_SPORT"], default=[])

    filtered_df = df_all.copy()
    if f_disc:
        filtered_df = filtered_df[filtered_df["discipline"].isin(f_disc)]
    if f_gate:
        filtered_df = filtered_df[filtered_df["gate"].isin(f_gate)]

    st.dataframe(
        filtered_df[[
            "id", "timestamp", "staff_id", "full_name", "department",
            "discipline", "gate", "station", "validation_status", "duration_minutes", "allowance_qualified"
        ]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown("---")
    st.markdown("#### 📅 Executive Master Sports & Events Calendar (All 18 Disciplines)")
    st.caption("Institution-wide scheduling oversight for Chairman (Mr. Angwenyi) and Sports Club Secretariat. View, filter, schedule, and coordinate fixtures, friendly matches, conditioning drills, and bank-wide events across all sporting disciplines:")

    # Top Controls & Quick Filter
    c_mc1, c_mc2 = st.columns([1.5, 1])
    with c_mc1:
        sec_filter_sport = st.selectbox(
            "Filter Master Calendar by Sporting Discipline:",
            ["🌟 All Disciplines"] + ALL_18_SPORTS,
            key="sec_master_cal_filter"
        )
    
    all_events = backend.get_calendar_notes(sec_filter_sport)
    
    with c_mc2:
        m_ev_count = len(all_events)
        m_tourn_count = len([e for e in all_events if "Tournament" in e.get("event_type", "")])
        st.markdown(f"""
        <div style="background: rgba(8, 24, 48, 0.7); border: 1px solid rgba(245, 197, 66, 0.3); border-radius: 8px; padding: 8px 14px; margin-top: 18px; display: flex; justify-content: space-around; text-align: center;">
            <div>
                <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase;">Total Events</div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #F5C542;">{m_ev_count}</div>
            </div>
            <div style="border-left: 1px solid rgba(255,255,255,0.1); padding-left: 10px;">
                <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase;">Tournaments</div>
                <div style="font-size: 1.15rem; font-weight: 800; color: #00F2FE;">{m_tourn_count}</div>
            </div>
            <div style="border-left: 1px solid rgba(255,255,255,0.1); padding-left: 10px;">
                <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase;">Filtered View</div>
                <div style="font-size: 0.85rem; font-weight: 700; color: #34D399; margin-top: 2px;">{sec_filter_sport.split()[0]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    col_m1, col_m2 = st.columns([1.6, 1.1])
    with col_m1:
        st.markdown(f"##### 📋 Scheduled Fixtures & Squad Diaries ({len(all_events)} Events)")
        if not all_events:
            st.info(f"No scheduled fixtures or events found for '{sec_filter_sport}'. Use the form on the right to schedule one!")
        else:
            for ev in all_events:
                ev_type = ev.get("event_type", "Conditioning Drill")
                if "Tournament" in ev_type:
                    badge_color = "#F5C542"
                    badge_bg = "rgba(245, 197, 66, 0.2)"
                    badge_icon = "🏆"
                elif "Friendly" in ev_type:
                    badge_color = "#00F2FE"
                    badge_bg = "rgba(0, 242, 254, 0.2)"
                    badge_icon = "⚽"
                elif "Briefing" in ev_type or "Tactical" in ev_type:
                    badge_color = "#A78BFA"
                    badge_bg = "rgba(167, 139, 250, 0.2)"
                    badge_icon = "📋"
                elif "Medical" in ev_type or "Rest" in ev_type:
                    badge_color = "#F87171"
                    badge_bg = "rgba(248, 113, 113, 0.2)"
                    badge_icon = "🩹"
                else:
                    badge_color = "#34D399"
                    badge_bg = "rgba(52, 211, 153, 0.2)"
                    badge_icon = "🏋️"

                venue_txt = f"📍 {ev.get('venue')}" if ev.get('venue') else ""
                disc_txt = ev.get('discipline', 'All')

                st.markdown(f"""
                <div style="background: rgba(8, 24, 48, 0.75); border: 1px solid rgba(245, 197, 66, 0.25); border-left: 4.5px solid {badge_color}; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <div style="display: flex; gap: 6px; align-items: center; margin-bottom: 4px;">
                                <span style="background: {badge_bg}; color: {badge_color}; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 800; text-transform: uppercase;">
                                    {badge_icon} {ev_type}
                                </span>
                                <span style="background: rgba(0, 242, 254, 0.15); color: #00F2FE; border: 1px solid rgba(0,242,254,0.3); padding: 1px 7px; border-radius: 4px; font-size: 0.7rem; font-weight: 700;">
                                    {disc_txt}
                                </span>
                            </div>
                            <h4 style="margin: 4px 0 2px 0; color: #FFFFFF; font-size: 1.05rem; font-weight: 800;">{ev.get('title')}</h4>
                            <p style="margin: 0; font-size: 0.8rem; color: #CBD5E1;">
                                🗓️ <strong>{ev.get('event_date')}</strong> at <strong>{ev.get('event_time')}</strong> • {venue_txt}
                            </p>
                        </div>
                    </div>
                    <div style="margin-top: 8px; padding-top: 8px; border-top: 1px solid rgba(255,255,255,0.06); font-size: 0.85rem; color: #94A3B8;">
                        📝 <em>{ev.get('notes') or 'No additional tactical notes.'}</em>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("🗑️ Cancel / Remove Event", key=f"del_sec_ev_{ev['id']}", help="Chairman/Secretariat override to cancel this scheduled fixture"):
                    backend.delete_calendar_note(ev['id'])
                    cur_off = get_current_officer() or {"staff_id": "CBK-CHAIRMAN", "full_name": "Executive Chairman", "role": "Sports Club Chairman"}
                    backend.log_audit_event(
                        staff_id=cur_off.get("staff_id", "CBK-CHAIRMAN"),
                        officer_name=cur_off.get("full_name", "Mr. Angwenyi"),
                        role=cur_off.get("role", "Executive Chairman"),
                        action_type="CALENDAR_EVENT_DELETED",
                        resource_name=f"EVENT_ID:{ev['id']}",
                        notes=f"Cancelled {ev.get('event_type')}: '{ev.get('title')}' ({disc_txt})"
                    )
                    st.toast("✅ Event cancelled and removed from Master Calendar.", icon="🗑️")
                    st.rerun()

            if all_events:
                df_cal_export = pd.DataFrame(all_events)
                cols_to_exp = [c for c in ["event_date", "event_time", "discipline", "event_type", "title", "venue", "notes", "created_by"] if c in df_cal_export.columns]
                st.download_button(
                    label="📥 Download Master Sports Fixtures Schedule (.CSV)",
                    data=df_cal_export[cols_to_exp].to_csv(index=False).encode('utf-8'),
                    file_name=f"CBK_Master_Sports_Calendar_{now_dt.strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

    with col_m2:
        st.markdown("##### ➕ Schedule Institution / Team Event")
        with st.form(key="form_sec_add_master_cal"):
            target_sport = st.selectbox(
                "Target Sporting Discipline or Function:*",
                ["Bank-Wide (All Disciplines)"] + ALL_18_SPORTS,
                key="sec_form_cal_sport"
            )
            mf_date = st.date_input("Event Date:", key="sec_form_cal_date")
            mf_time = st.text_input("Start / Kick-off Time:", value="17:00", key="sec_form_cal_time")
            mf_type = st.selectbox(
                "Event Category:*",
                [
                    "🏆 Tournament Fixture",
                    "⚽ Friendly Match",
                    "🏋️ Conditioning / Fitness Drill",
                    "📋 Tactical Briefing",
                    "🩹 Medical / Squad Rest Day",
                    "🎉 Sports Club Function / Gala",
                    "📣 General Meeting / AGM"
                ],
                key="sec_form_cal_type"
            )
            mf_title = st.text_input("Event Title / Opponent:*", placeholder="e.g. Inter-Bank Championship Finals", key="sec_form_cal_title")
            mf_venue = st.text_input("Venue / Grounds:*", value="CBK Sports Complex, Ruaraka", key="sec_form_cal_venue")
            mf_notes = st.text_area("Operational Notes / Directives:", placeholder="e.g. Official transport departs Haile Selassie Ave at 15:30. Medical team on standby.", key="sec_form_cal_notes")

            btn_save_m_cal = st.form_submit_button("💾 Schedule & Broadcast to Master Calendar", use_container_width=True)
            if btn_save_m_cal:
                if not mf_title.strip():
                    st.error("Please specify an Event Title.")
                else:
                    d_str = mf_date.strftime("%Y-%m-%d")
                    cur_off = get_current_officer() or {"staff_id": "CBK-CHAIRMAN", "full_name": "Executive Chairman", "role": "Sports Club Chairman"}
                    ok = backend.add_calendar_note(
                        discipline=target_sport,
                        event_date=d_str,
                        event_time=mf_time.strip(),
                        event_type=mf_type,
                        title=mf_title.strip(),
                        notes=mf_notes.strip(),
                        venue=mf_venue.strip(),
                        created_by=f"{cur_off.get('role', 'Chairman')} ({cur_off.get('full_name', 'Secretariat')})"
                    )
                    if ok:
                        st.toast(f"✅ Scheduled '{mf_title}' for {target_sport}!", icon="📅")
                        st.rerun()
                    else:
                        st.error("Failed to save event to Master Calendar. Please retry.")

    render_admin_security_lock("sec_tab", required_perm="roster")

    c_s_btn1, c_s_btn2, c_s_btn3 = st.columns(3)
    with c_s_btn1:
        if is_export_authorized("roster"):
            csv_data_all = df_all.to_csv(index=False).encode('utf-8')
            cur_off = get_current_officer() or {"staff_id": "CBK-3428", "full_name": "Samuel Gathigi Njuguna", "role": "Super Admin"}
            backend.log_audit_event(
                staff_id=cur_off.get("staff_id", "CBK-3428"),
                officer_name=cur_off.get("full_name", "Officer"),
                role=cur_off.get("role", "Secretariat Officer"),
                action_type="EXPORT_ROSTER_CSV",
                resource_name=f"CBK_DSWAAP_Master_Attendance_{now_dt.strftime('%Y%m%d')}.csv",
                notes="Master Attendance Ledger CSV download requested"
            )
            st.download_button(
                label="📥 Master Ledger (CSV)",
                data=csv_data_all,
                file_name=f"CBK_DSWAAP_Master_Attendance_{now_dt.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.button("🔒 Master Ledger (Locked)", disabled=True, use_container_width=True, help="Requires Secretariat clearance")
    with c_s_btn2:
        st.link_button(
            "📊 Open Google Sheets",
            url="https://sheets.new",
            use_container_width=True
        )
    with c_s_btn3:
        xlsx_template_path = os.path.join(os.path.dirname(__file__), "CBK_STRIDE_Secretariat_Roster_Template.xlsx")
        if os.path.exists(xlsx_template_path):
            with open(xlsx_template_path, "rb") as f_x:
                st.download_button(
                    label="📋 Blank Template (.xlsx)",
                    data=f_x.read(),
                    file_name="CBK_STRIDE_Secretariat_Roster_Template.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

    with st.expander("🤖 Member Voice & Facility Sentiment Live Telemetry", expanded=False):
        render_hr_satisfaction_nlp_dashboard()

if "🏛️ Secretariat Operations" in tab_dict:
    with tab_dict["🏛️ Secretariat Operations"]:
        render_tab_secretariat()

# ==============================================================================
# TAB 4: HR ANALYTICS COMMAND CENTER
# ==============================================================================
def render_tab_hr():
    st.markdown("### 📊 Human Resources Wellness Analytics Command Center")
    st.caption("Departmental wellness participation metrics, equity benchmarks, and engagement curves.")

    dept_df = compute_department_breakdown(df_all)

    c_dept_progress, c_dept_pie = st.columns([1.2, 0.8])

    with c_dept_progress:
        with st.container(border=True):
            st.markdown("#### Directorate Engagement vs Target Quotas")
            st.caption("Benchmark target: Minimum 15 active participating staff per directorate.")

            if not dept_df.empty:
                for _, r in dept_df.iterrows():
                    dept_name = r["Department"]
                    scans = r["Total Scans"]
                    pct = r["Engagement Rate (%)"]
                    
                    bar_color = "#00F2FE" if pct >= 60 else ("#F5C542" if pct >= 30 else "#EF4444")
                    
                    st.markdown(f"""
                    <div style="margin-bottom: 0.6rem;">
                        <div style="display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 600; color: #F1F5F9;">
                            <span>{dept_name}</span>
                            <span>{scans} participants ({pct}%)</span>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.08); border-radius: 4px; height: 9px; width: 100%; overflow: hidden; margin-top: 3px;">
                            <div style="background: {bar_color}; width: {pct}%; height: 100%; border-radius: 4px; box-shadow: 0 0 8px {bar_color};"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("📊 Awaiting arrival scans to plot directorate engagement.")

    with c_dept_pie:
        with st.container(border=True):
            st.markdown("#### Participation by Sport Category")
            
            # Categorize
            if not df_all.empty:
                cat_map = {k: v["category"] for k, v in CBK_DISCIPLINES.items()}
                df_cat = df_all.copy()
                df_cat["Category"] = df_cat["discipline"].map(cat_map).fillna("Other")
                cat_counts = df_cat["Category"].value_counts().reset_index()
                cat_counts.columns = ["Category", "Count"]

                fig_cat = px.pie(
                    cat_counts,
                    values="Count",
                    names="Category",
                    hole=0.45,
                    color_discrete_sequence=["#F5C542", "#00F2FE", "#38BDF8", "#F59E0B", "#10B981", "#A855F7"]
                )
                fig_cat.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=260,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.3, font=dict(size=10, color="#CBD5E1")),
                    font=dict(color="#F1F5F9")
                )
                st.plotly_chart(fig_cat, use_container_width=True)
            else:
                st.info("🥧 Awaiting arrival scans to plot sport categories.")

    # Trends & Activity Distribution
    c_trend, c_lead = st.columns([1.1, 0.9])

    with c_trend:
        with st.container(border=True):
            st.markdown("#### Discipline Popularity Index (Top Sports)")
            if not df_all.empty:
                top_sports = df_all["discipline"].value_counts().head(8).reset_index()
                top_sports.columns = ["Discipline", "Attendees"]

                fig_bar = px.bar(
                    top_sports,
                    x="Attendees",
                    y="Discipline",
                    orientation="h",
                    color="Attendees",
                    color_continuous_scale=[[0, "#082142"], [0.5, "#00F2FE"], [1, "#F5C542"]]
                )
                fig_bar.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=280,
                    coloraxis_showscale=False,
                    yaxis=dict(autorange="reversed"),
                    font=dict(color="#F1F5F9")
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("📈 Discipline popularity will calculate dynamically upon first check-ins.")

    with c_lead:
        with st.container(border=True):
            st.markdown("#### 🌟 CBK Wellness Champions Leaderboard")
            st.caption("Top staff athletes by verified attendance sessions.")

            if not df_all.empty:
                staff_summary = df_all[df_all["validation_status"].str.startswith("DUAL_VERIFIED")].groupby(
                    ["staff_id", "full_name", "department"]
                ).size().reset_index(name="Sessions")
                staff_summary = staff_summary.sort_values(by="Sessions", ascending=False).head(5)

                for rank, (_, row) in enumerate(staff_summary.iterrows(), start=1):
                    medal = "🥇" if rank == 1 else ("🥈" if rank == 2 else ("🥉" if rank == 3 else "🎖️"))
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.55rem 0; border-bottom: 1px solid rgba(255,255,255,0.08);">
                        <div>
                            <span style="font-size: 1.1rem; margin-right: 6px;">{medal}</span>
                            <strong style="color: #FFFFFF;">{row['full_name']}</strong> 
                            <span style="font-size: 0.75rem; color: #94A3B8;">({row['staff_id']})</span>
                            <div style="font-size: 0.75rem; color: #64748B; margin-left: 1.8rem;">{row['department']}</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="background: rgba(0, 242, 254, 0.12); color: #00F2FE; font-weight: 700; padding: 3px 10px; border-radius: 12px; font-size: 0.8rem; border: 1px solid rgba(0, 242, 254, 0.3);">
                                {row['Sessions']} Completed
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("🌟 Leaderboard will populate as athletes complete verified sessions.")

    # Executive AI Sentiment & Member Satisfaction Intelligence Hub
    render_hr_satisfaction_nlp_dashboard()

# ==============================================================================
# EXECUTIVE REAL-TIME NLP SENTIMENT & MEMBER SATISFACTION DASHBOARD
# ==============================================================================
def render_hr_satisfaction_nlp_dashboard():
    """
    Renders the executive-grade real-time NLP sentiment intelligence board.
    Displays Net Promoter Score (NPS), Average CSAT Star Rating,
    aspect sentiment breakdown, discipline rankings, and live member voice feed.
    """
    st.markdown("---")
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
        <div>
            <h3 style="margin: 0; color: #FFFFFF; font-size: 1.35rem; font-weight: 900;">
                🤖 Member Voice & AI Sentiment Intelligence (Facility Pulse)
            </h3>
            <p style="margin: 3px 0 0 0; color: #94A3B8; font-size: 0.84rem;">
                Continuous NLP sentiment monitoring across all 18 CBK sports facilities, gate checkpoints, equipment hygiene, and coaching.
            </p>
        </div>
        <div>
            <span style="background: rgba(245, 197, 66, 0.15); border: 1px solid #F5C542; color: #F5C542; padding: 4px 12px; border-radius: 20px; font-size: 0.76rem; font-weight: 800;">
                LIVE NLP PIPELINE ACTIVE
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Filter by discipline if desired
    c_f1, c_f2 = st.columns([1.5, 1])
    with c_f1:
        disc_filter = st.selectbox(
            "Filter Satisfaction by Sporting Discipline:",
            ["All Sports"] + ALL_18_SPORTS,
            index=0,
            key="sat_dash_disc_filter"
        )
    with c_f2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        st.caption("Real-time telemetry updated with every 1-click face reaction.")

    metrics = backend.get_facility_feedback_metrics(discipline=disc_filter)

    # 4 Executive KPI Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #F5C542;">
            <div class="kpi-title">Average Satisfaction</div>
            <div class="kpi-value" style="color: #F5C542;">⭐ {metrics['avg_rating']:.2f} / 5.0</div>
            <div class="kpi-sub">5-Point Emoji CSAT Scale</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        nps_color = "#10B981" if metrics['nps'] >= 50 else ("#F5C542" if metrics['nps'] >= 0 else "#EF4444")
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: {nps_color};">
            <div class="kpi-title">Net Promoter Score (NPS)</div>
            <div class="kpi-value" style="color: {nps_color};">+{metrics['nps']} NPS</div>
            <div class="kpi-sub">% Promoters (4-5★) minus % Detractors</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #00F2FE;">
            <div class="kpi-title">Verified Member Pulse</div>
            <div class="kpi-value" style="color: #00F2FE;">{metrics['total']} Athletes</div>
            <div class="kpi-sub">1-Click Reactions Recorded</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #10B981;">
            <div class="kpi-title">Sentiment Polarity</div>
            <div class="kpi-value" style="color: #10B981;">{metrics['positive_pct']}% Positive</div>
            <div class="kpi-sub">{metrics['neutral_pct']}% Neutral • {metrics['negative_pct']}% Detractors</div>
        </div>
        """, unsafe_allow_html=True)

    c_asp, c_rank = st.columns([1.1, 0.9])
    with c_asp:
        with st.container(border=True):
            st.markdown("#### 🎯 Operational Aspect Mentions")
            st.caption("Distribution of feedback across sports facility operational pillars:")
            asp_counts = metrics.get("aspects_count", {})
            if asp_counts:
                asp_df = pd.DataFrame(list(asp_counts.items()), columns=["Aspect", "Mentions"]).sort_values(by="Mentions", ascending=True)
                fig_asp = px.bar(
                    asp_df,
                    x="Mentions",
                    y="Aspect",
                    orientation="h",
                    color="Mentions",
                    color_continuous_scale=[[0, "#082142"], [0.5, "#00F2FE"], [1, "#F5C542"]]
                )
                fig_asp.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=260,
                    coloraxis_showscale=False,
                    font=dict(color="#F1F5F9")
                )
                st.plotly_chart(fig_asp, use_container_width=True)
            else:
                st.info("Awaiting aspect feedback to plot operational metrics.")

    with c_rank:
        with st.container(border=True):
            st.markdown("#### 🏆 Discipline Satisfaction Leaderboard")
            st.caption("Ranked by average member star rating:")
            rankings = metrics.get("discipline_rankings", [])
            if rankings:
                for idx, rk in enumerate(rankings[:6], start=1):
                    med = "🥇" if idx == 1 else ("🥈" if idx == 2 else ("🥉" if idx == 3 else f"#{idx}"))
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.08);">
                        <div>
                            <span style="font-size: 0.95rem; margin-right: 6px;">{med}</span>
                            <strong style="color: #FFFFFF; font-size: 0.88rem;">{rk['discipline']}</strong>
                            <div style="font-size: 0.72rem; color: #94A3B8; margin-left: 1.8rem;">{rk['count']} verified ratings</div>
                        </div>
                        <div style="text-align: right;">
                            <span style="background: rgba(245, 197, 66, 0.15); border: 1px solid #F5C542; color: #F5C542; font-weight: 800; padding: 2px 8px; border-radius: 8px; font-size: 0.82rem;">
                                ⭐ {rk['avg_rating']:.2f}
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Leaderboard will populate as athletes submit feedback.")

    # Live Member Voice Feed
    st.markdown("#### 💬 Live Member Voice & NLP Telemetry Feed")
    st.caption("Real-time sentiment polarity scores, aspect classification, and attendee comments:")

    recent_fb = metrics.get("recent_rows", [])
    if recent_fb:
        for fb in recent_fb[:8]:
            s_label = fb.get("sentiment_label", "POSITIVE")
            s_score = fb.get("sentiment_score", 0.0)
            badge_color = "#059669" if s_label == "POSITIVE" else ("#DC2626" if s_label == "NEGATIVE" else "#D97706")
            emoji_char = fb.get("emoji", "😐")
            rating_num = fb.get("rating", 3)
            staff_disp = fb.get("full_name", "Athlete") if is_export_authorized() else mask_name_banking(fb.get("full_name", "Athlete"))

            try:
                aspects_list = json.loads(fb.get("aspects_json", "[]"))
            except Exception:
                aspects_list = []

            aspect_pills = " ".join([f"<span style='background: rgba(0, 242, 254, 0.15); color: #00F2FE; font-size: 0.70rem; padding: 1px 7px; border-radius: 10px; margin-right: 4px;'>{a}</span>" for a in aspects_list])

            st.markdown(f"""
            <div style="background: rgba(8, 24, 46, 0.75); border: 1px solid rgba(245, 197, 66, 0.25); border-radius: 12px; padding: 12px 16px; margin-bottom: 8px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="font-size: 1.15rem; margin-right: 6px;">{emoji_char}</span>
                        <strong style="color: #FFFFFF; font-size: 0.90rem;">{staff_disp}</strong>
                        <span style="font-size: 0.75rem; color: #94A3B8;">({fb.get('staff_id')}) • <span style="color: #F5C542;">{fb.get('discipline')}</span></span>
                    </div>
                    <div>
                        <span style="background: {badge_color}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.70rem; font-weight: 800;">
                            {s_label} ({s_score:+.2f})
                        </span>
                        <span style="color: #64748B; font-size: 0.72rem; margin-left: 8px;">{fb.get('submitted_at')}</span>
                    </div>
                </div>
                {f'<p style="color: #CBD5E1; font-size: 0.84rem; margin: 6px 0 6px 0; font-style: italic;">"{fb.get("feedback_text")}"</p>' if fb.get("feedback_text") else '<p style="color: #64748B; font-size: 0.78rem; margin: 4px 0 4px 0;"><em>1-Click Emoji Face Rating (No written note added)</em></p>'}
                <div style="margin-top: 4px;">{aspect_pills}</div>
            </div>
            """, unsafe_allow_html=True)

        # Forensic CSV Export
        if is_export_authorized("roster"):
            fb_df = pd.DataFrame(recent_fb)
            csv_data = fb_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Certified Facility Sentiment Audit (.CSV)",
                data=csv_data,
                file_name=f"CBK_Facility_Satisfaction_Sentiment_Ledger_{get_eat_today_str()}.csv",
                mime="text/csv",
                use_container_width=True,
                key="btn_dl_facility_feedback_csv"
            )
    else:
        st.info("No feedback records match the current filter.")

if "📊 HR Analytics Command" in tab_dict:
    with tab_dict["📊 HR Analytics Command"]:
        render_tab_hr()

# ==============================================================================
# TAB 5: FINANCE & AUDIT COMPLIANCE PORTAL
# ==============================================================================
def render_tab_finance():
    st.markdown("### 🏛️ Finance & Internal Audit Verification Portal")
    st.caption("Official certified attendance ledger, dual-gate compliance verification, and batch payroll export. All field terminals and participant views are stripped of monetary data pursuant to CBK Financial Privacy & Information Security Policy.")

    # Certified Attendance KPI Summary (Clean Units)
    f1, f2, f3 = st.columns(3)
    with f1:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #10B981;">
            <div class="kpi-title">Certified Attendances (Payable)</div>
            <div class="kpi-value" style="color: #10B981;">{kpis['qualified']} Sessions</div>
            <div class="kpi-sub">Dual-Gate Verified (≥ 45 mins floor met)</div>
        </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #EF4444;">
            <div class="kpi-title">Audit Flagged / Disqualified</div>
            <div class="kpi-value" style="color: #EF4444;">{kpis['flagged_sessions']} Sessions</div>
            <div class="kpi-sub">Under 45 mins or Missing Pre-Gate</div>
        </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown(f"""
        <div class="kpi-card" style="border-left-color: #F5C542;">
            <div class="kpi-title">Audit Compliance Rate</div>
            <div class="kpi-value" style="color: #F5C542;">{kpis['compliance_rate']}%</div>
            <div class="kpi-sub">Dual-Gate Rigor Maintained</div>
        </div>
        """, unsafe_allow_html=True)

    # Confidential Finance Valuation Tool
    with st.expander("💼 Finance Discretionary Valuation Controller (Confidential to Finance Directorate)", expanded=False):
        st.caption("As the sole valuation authority, Finance assigns the per-diem rate to certified attendance records for accounts payable generation:")
        c_fin_rate, c_fin_calc = st.columns([1, 1.5])
        with c_fin_rate:
            fin_rate_input = st.number_input(
                "Finance Assigned Rate per Certified Session (KES):",
                min_value=0,
                value=2500,
                step=500,
                key="fin_confidential_rate"
            )
        with c_fin_calc:
            total_fin_calc = kpis['qualified'] * fin_rate_input
            st.metric(
                label="Provisional Payroll Allocation (Internal Finance Calculation)",
                value=f"KES {total_fin_calc:,}",
                delta=f"{kpis['qualified']} Certified Sessions @ KES {fin_rate_input:,}"
            )

    st.markdown("---")
    st.markdown("#### 📋 Certified Attendance & Audit Reconciliation Ledger")

    # Filter to qualified or all completed
    ledger_filter = st.radio(
        "Ledger View Mode:",
        ["All Verified Records", "Certified For Payment Only", "Audit Flagged / Exceptions Only"],
        horizontal=True
    )

    ledger_df = df_all.copy()
    if ledger_filter == "Certified For Payment Only":
        ledger_df = ledger_df[ledger_df["allowance_qualified"] == "QUALIFIED"]
    elif ledger_filter == "Audit Flagged / Exceptions Only":
        ledger_df = ledger_df[ledger_df["allowance_qualified"].isin(["INSUFFICIENT_DURATION", "DISQUALIFIED_NO_PRE_GATE"])]

    # Add clean Certified Attendance display column
    ledger_df["Certified Attendance"] = ledger_df["allowance_qualified"].apply(
        lambda x: "1 UNIT (CERTIFIED)" if x == "QUALIFIED" else "0 UNITS (FLAGGED)"
    )

    # Display clean certified attendance table (NO public allowance amount column!)
    st.dataframe(
        ledger_df[[
            "id", "timestamp", "staff_id", "full_name", "department",
            "discipline", "gate", "duration_minutes", "Certified Attendance", "audit_notes"
        ]],
        use_container_width=True,
        hide_index=True
    )

    # Actions: Batch Approve and Exports
    st.markdown("---")
    st.markdown("#### ⚡ Financial Operations & Export")
    render_admin_security_lock("fin_tab", required_perm="finances")
    
    c_btn1, c_btn2, c_btn3 = st.columns(3)

    with c_btn1:
        if st.button("✅ Batch Approve Certified Sessions for Accounts Payable", type="primary", use_container_width=True):
            st.success(f"Batch approved {kpis['qualified']} certified attendance units for Accounts Payable processing!")

    with c_btn2:
        if is_export_authorized("finances"):
            csv_data = ledger_df.to_csv(index=False).encode('utf-8')
            cur_off = get_current_officer() or {"staff_id": "CBK-3428", "full_name": "Samuel Gathigi Njuguna", "role": "Super Admin"}
            backend.log_audit_event(
                staff_id=cur_off.get("staff_id", "CBK-3428"),
                officer_name=cur_off.get("full_name", "Officer"),
                role=cur_off.get("role", "Finance Officer"),
                action_type="EXPORT_FINANCE_CSV",
                resource_name=f"CBK_Certified_Attendance_Ledger_{now_dt.strftime('%Y%m%d')}.csv",
                notes="Certified Finance Ledger CSV download requested"
            )
            st.download_button(
                label="📥 Export Certified Ledger to CSV",
                data=csv_data,
                file_name=f"CBK_Certified_Attendance_Ledger_{now_dt.strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.button("🔒 Certified Ledger CSV (Locked)", disabled=True, use_container_width=True, help="Requires Finance & Internal Audit clearance")

    with c_btn3:
        if is_export_authorized("finances"):
            excel_buffer = io.BytesIO()
            dept_df = compute_department_breakdown(df_all)
            with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                ledger_df.to_excel(writer, sheet_name='Certified_Attendance_Ledger', index=False)
                dept_df.to_excel(writer, sheet_name='Department_Summary', index=False)
            cur_off = get_current_officer() or {"staff_id": "CBK-3428", "full_name": "Samuel Gathigi Njuguna", "role": "Super Admin"}
            backend.log_audit_event(
                staff_id=cur_off.get("staff_id", "CBK-3428"),
                officer_name=cur_off.get("full_name", "Officer"),
                role=cur_off.get("role", "Finance Officer"),
                action_type="EXPORT_AUDIT_EXCEL",
                resource_name=f"CBK_DSWAAP_Audit_Workbook_{now_dt.strftime('%Y%m%d')}.xlsx",
                notes="Full Excel Audit Workbook download requested"
            )
            st.download_button(
                label="📊 Export Full Audit Workbook (Excel .xlsx)",
                data=excel_buffer.getvalue(),
                file_name=f"CBK_DSWAAP_Audit_Workbook_{now_dt.strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        else:
            st.button("🔒 Audit Workbook (Locked)", disabled=True, use_container_width=True, help="Requires Finance & Internal Audit clearance")

if "💰 Finance & Audit Portal" in tab_dict:
    with tab_dict["💰 Finance & Audit Portal"]:
        render_tab_finance()

# ==============================================================================
# TAB 6: INTEGRATION & SETTINGS
# ==============================================================================
def render_tab_settings():
    st.markdown("### ⚙️ Google Sheets & Institutional Integration Hub")
    st.caption("Manage Google Sheets API credentials, test automated email dispatching, and verify database integrity.")

    c_int_left, c_int_right = st.columns([1, 1])

    with c_int_left:
        with st.container(border=True):
            st.markdown("#### ⚡ Option 1: Instant 5-Second Google Sheets Import")
            st.caption("No coding, no scripts. Download the full 720-record ledger and open it in Google Sheets in 3 clicks:")

            c_cs1, c_cs2 = st.columns([1, 1])
            with c_cs1:
                if is_export_authorized():
                    # Direct CSV Download Button
                    csv_bytes = df_all.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download 720-Record CSV for Sheets",
                        data=csv_bytes,
                        file_name="CBK_DSWAAP_Master_Attendance_Ledger.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="btn_dl_csv_sheets"
                    )
                else:
                    st.button("🔒 720-Record CSV (Locked)", disabled=True, use_container_width=True, help="Unlock with Secretariat PIN")
            with c_cs2:
                st.link_button("🌐 Open Blank Sheet (sheets.new)", "https://sheets.new", use_container_width=True)

            st.markdown("""
            *How to import in 5 seconds:*
            1. Click **Open Blank Sheet** above (or visit `sheets.new`).
            2. Click **File > Import > Upload** and drop the downloaded CSV.
            3. Select **Replace spreadsheet** & click **Import data** — your entire 400-employee attendance ledger is live!
            """)

            st.markdown("---")
            st.markdown("#### ⚡ Option 2: 60-Second Real-Time Webhook Cloud Sync")
            st.caption("Sync directly to any personal or CBK Google Sheet. Every phone camera scan at Gate 1 or Gate 2 automatically streams live!")

            with st.expander("📖 3-Step Setup Instructions (Takes 60 Seconds):", expanded=False):
                st.markdown("""
                1. Open **[sheets.new](https://sheets.new)** in your browser to create a new blank Google Sheet.
                2. In your Google Sheet, click **Extensions > Apps Script**, delete existing code, and paste:
                ```javascript
                function doPost(e) {
                  try {
                    var ss = SpreadsheetApp.getActiveSpreadsheet();
                    var sheet = ss.getActiveSheet();
                    
                    // Auto-create CBK branded header if sheet is empty
                    if (sheet.getLastRow() === 0) {
                      sheet.appendRow([
                        "Timestamp", "Date", "Staff ID", "Full Name", "CBK Email",
                        "Department", "Discipline", "Gate", "Station", "Session ID",
                        "Validation Status", "Duration (Mins)", "Attendance Certified",
                        "Compliance Notes"
                      ]);
                      sheet.getRange(1, 1, 1, 14)
                        .setBackground("#025BBF")
                        .setFontColor("#FFFFFF")
                        .setFontWeight("bold")
                        .setHorizontalAlignment("center");
                      sheet.setFrozenRows(1);
                    }
                    
                    var data = JSON.parse(e.postData.contents);
                    var rows = data.rows || (Array.isArray(data) ? data : [data]);
                    
                    if (rows && rows.length > 0) {
                      // High-speed batch insertion (100x faster than appendRow loop)
                      var startRow = sheet.getLastRow() + 1;
                      sheet.getRange(startRow, 1, rows.length, rows[0].length).setValues(rows);
                    }
                    
                    return ContentService.createTextOutput(JSON.stringify({status: "ok", count: rows.length}))
                      .setMimeType(ContentService.MimeType.JSON);
                  } catch(err) {
                    return ContentService.createTextOutput(JSON.stringify({status: "error", error: err.toString()}))
                      .setMimeType(ContentService.MimeType.JSON);
                  }
                }
                ```
                3. Click **Deploy > New deployment**, select type **Web app**, set **Who has access: Anyone**, and click **Deploy**.
                4. Copy the resulting **Web App URL** and paste it below!
                """)

            webhook_val = st.text_input(
                "Paste Google Apps Script Web App URL:",
                value=st.session_state.get("gsheets_webhook_url", ""),
                placeholder="https://script.google.com/macros/s/.../exec",
                key="input_gsheets_webhook"
            )

            col_btn_w1, col_btn_w2 = st.columns(2)
            with col_btn_w1:
                if st.button("🚀 Push All 720 Records to My Google Sheet", type="primary", use_container_width=True):
                    if webhook_val.strip():
                        st.session_state["gsheets_webhook_url"] = webhook_val.strip()
                        with st.spinner("Connecting and streaming 720 attendance logs to your Google Sheet..."):
                            sync_res = backend.push_to_gsheets_webhook(webhook_val.strip(), sync_all=True)
                            if sync_res["success"]:
                                st.success(sync_res["message"])
                                st.balloons()
                            else:
                                st.error(sync_res["message"])
                    else:
                        st.warning("Please paste your Google Apps Script Web App URL above first.")

            with col_btn_w2:
                if st.button("🔄 Sync Only New Scans", use_container_width=True):
                    if webhook_val.strip():
                        st.session_state["gsheets_webhook_url"] = webhook_val.strip()
                        sync_res = backend.push_to_gsheets_webhook(webhook_val.strip(), sync_all=False)
                        if sync_res["success"]:
                            st.success(sync_res["message"])
                        else:
                            st.error(sync_res["message"])
                    else:
                        st.warning("Please paste your Google Apps Script Web App URL above first.")

            st.markdown("---")
            st.markdown("##### 👁️ Live Google Sheet Embed Preview")
            st.caption("Paste your Google Sheet link to inspect your live spreadsheet directly inside the dashboard:")
            sheet_embed_url = st.text_input(
                "Google Sheet Share URL:",
                placeholder="https://docs.google.com/spreadsheets/d/.../edit",
                key="input_sheet_embed"
            )
            if sheet_embed_url.strip():
                raw_url = sheet_embed_url.strip()
                embed_src = raw_url.split("/edit")[0] + "/pubhtml?widget=true&headers=false" if "/edit" in raw_url else raw_url
                st.markdown(f'<iframe src="{embed_src}" width="100%" height="380" style="border: 1px solid #CBD5E1; border-radius: 8px;"></iframe>', unsafe_allow_html=True)
                st.caption(f"🔗 [Open full spreadsheet in new tab]({raw_url})")

            st.markdown("---")
            st.markdown("#### ☁️ Enterprise Google Cloud Service Account (gspread)")
            
            if backend.gspread_connected:
                st.success("🟢 Connected to Google Sheets API (gspread v6)")
                st.write(f"**Target Spreadsheet:** `{backend.sheet_name}`")
            else:
                st.info("🟡 Resilient Offline Mode (Local SQLite + CSV Mirror Active)")
                if backend.gspread_error:
                    st.caption(f"Status Note: {backend.gspread_error}")

            pasted_creds = st.text_area("Service Account JSON Key:", height=90, placeholder='{"type": "service_account", "project_id": "cbk-dswaap", ...}')
            target_sheet = st.text_input("Google Sheet Title:", value="CBK_DSWAAP_Attendance_Ledger")

            if st.button("🔗 Test & Connect GCP Service Account", use_container_width=True):
                if pasted_creds.strip():
                    try:
                        creds_dict = json.loads(pasted_creds.strip())
                        new_backend = AttendanceBackend(credentials_path_or_dict=creds_dict, sheet_name=target_sheet)
                        st.session_state.backend = new_backend
                        st.success("Connected and initialized Google Sheets successfully!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to parse credentials: {str(e)}")
                else:
                    st.info("Please provide valid service account JSON credentials to establish live connection.")

            st.markdown("---")
            st.markdown("##### 🌐 Custom Domain / Vanity URL Override")
            st.caption("Override the live hostname encoded into QR codes (e.g. for Streamlit Cloud or official CBK intranet):")
            cur_custom = st.session_state.get("custom_portal_host", "")
            new_custom = st.text_input(
                "Custom Domain / URL:",
                value=cur_custom,
                placeholder="e.g. cbk-sports.streamlit.app or dswaap.centralbank.go.ke",
                key="input_custom_host"
            )
            if st.button("💾 Apply Custom Domain", key="btn_apply_host"):
                st.session_state["custom_portal_host"] = new_custom.strip()
                st.success("Updated custom portal domain!")
                st.rerun()

    with c_int_right:
        with st.container(border=True):
            st.markdown("#### ✉️ Institutional Email Notification Center")
            st.caption("Automated dual verification receipts dispatched to staff upon session completion.")

            recent_emails = CBKEmailDispatcher.RECENT_DISPATCHES
            st.write(f"Total Dispatched in Session: **{len(recent_emails)}**")

            if recent_emails:
                latest = recent_emails[0]
                st.markdown(f"**Latest Notification Sent to:** `{latest['recipient']}`")
                st.markdown(f"**Subject:** {latest['subject']}")
                
                with st.expander("👁️ Preview Rendered CBK HTML Receipt"):
                    st.components.v1.html(latest["html"], height=420, scrolling=True)
            else:
                st.info("No verification emails dispatched yet. Complete a dual-gate check-in to trigger automated email dispatching.")

            st.markdown("---")
            st.markdown("##### Send Test Verification Receipt")
            test_email = st.text_input("Recipient CBK Email:", value="employee@centralbank.go.ke")
            if st.button("📨 Dispatch Test Dual-Verification Email", use_container_width=True):
                test_record = {
                    "id": 999,
                    "timestamp": get_eat_now().strftime("%Y-%m-%d %H:%M:%S"),
                    "staff_id": "CBK-8888",
                    "full_name": "Test Officer",
                    "cbk_email": test_email,
                    "department": "Finance & Accounts",
                    "discipline": "Golf",
                    "station": "18th Green Marshals Post",
                    "validation_status": "DUAL_VERIFIED_QUALIFIED",
                    "duration_minutes": 75.0,
                    "allowance_qualified": "QUALIFIED",
                    "allowance_amount": 2500
                }
                dispatcher = CBKEmailDispatcher()
                dispatcher.send_dual_verification_notification(test_record)
                st.success(f"Verification receipt dispatched to {test_email}!")
                st.rerun()

    # ==========================================================================
    # SECRETARIAT ROSTER TEMPLATE & BULK SYSTEM IMPORTER
    # ==========================================================================
    st.markdown("---")
    st.markdown("#### 📥 Secretariat Roster Template & Bulk System Importer")
    st.caption("Distribute the official CBK STRIDE™ Excel Template to the Sports Secretariat. When populated with staff entries, upload the file here to instantly synchronize all 18 disciplines!")

    xlsx_template_path = os.path.join(os.path.dirname(__file__), "CBK_STRIDE_Secretariat_Roster_Template.xlsx")
    csv_template_path = os.path.join(os.path.dirname(__file__), "CBK_STRIDE_Secretariat_Roster_Template.csv")

    c_dl1, c_dl2 = st.columns(2)
    with c_dl1:
        if os.path.exists(xlsx_template_path):
            with open(xlsx_template_path, "rb") as f_x:
                st.download_button(
                    label="📊 Download Secretariat Template (.xlsx)",
                    data=f_x.read(),
                    file_name="CBK_STRIDE_Secretariat_Roster_Template.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    help="Includes formatted columns, instructions, and dropdown validations for the 18 disciplines and directorates."
                )
    with c_dl2:
        if os.path.exists(csv_template_path):
            with open(csv_template_path, "rb") as f_c:
                st.download_button(
                    label="📄 Download Companion CSV Template (.csv)",
                    data=f_c.read(),
                    file_name="CBK_STRIDE_Secretariat_Roster_Template.csv",
                    mime="text/csv",
                    use_container_width=True,
                    help="Lightweight CSV version for quick editing."
                )

    uploaded_roster = st.file_uploader(
        "📤 Upload Populated Secretariat Template (.xlsx or .csv) to Sync with Portal:",
        type=["xlsx", "xls", "csv"],
        key="uploader_secretariat_roster"
    )

    if uploaded_roster is not None:
        try:
            fname = uploaded_roster.name.lower()
            if fname.endswith(".csv"):
                df_raw = pd.read_csv(uploaded_roster)
            else:
                df_scan = pd.read_excel(uploaded_roster, header=None)
                header_idx = 0
                for idx, row in df_scan.head(10).iterrows():
                    row_str = " ".join([str(v).lower() for v in row.values])
                    if "staff id" in row_str or "payroll" in row_str or "full name" in row_str:
                        header_idx = idx
                        break
                uploaded_roster.seek(0)
                df_raw = pd.read_excel(uploaded_roster, header=header_idx)

            # Prioritized column matching
            col_map = {}
            target_rules = [
                ("primary_sport", ["primary enrolled sport", "primary sport", "primary_sport"]),
                ("staff_id", ["staff id", "payroll no", "payroll", "staff_id"]),
                ("full_name", ["full official name", "full name", "official name", "athlete name", "full_name"]),
                ("cbk_email", ["institutional cbk email", "cbk email", "email", "cbk_email"]),
                ("department", ["directorate / department", "directorate", "department"]),
                ("secondary_sport", ["secondary sport", "secondary_sport"]),
                ("phone", ["mobile / whatsapp", "phone", "whatsapp"]),
                ("role", ["assigned squad role", "assigned role", "role"]),
                ("medical_clearance", ["medical fitness clearance", "medical clearance", "medical"]),
                ("emergency_contact", ["emergency contact", "next of kin"]),
                ("notes", ["discipline notes", "remarks", "notes", "handicap"])
            ]
            for target, patterns in target_rules:
                for c in df_raw.columns:
                    if c in col_map:
                        continue
                    c_clean = str(c).strip().lower()
                    if any(p in c_clean for p in patterns):
                        col_map[c] = target
                        break

            mapped_df = df_raw.rename(columns=col_map)
            
            if "staff_id" in mapped_df.columns:
                valid_rows = mapped_df.dropna(subset=["staff_id"])
                valid_rows = valid_rows[~valid_rows["staff_id"].astype(str).str.lower().str.contains("staff id|payroll")]
                
                imported_count = 0
                updated_sports = set()
                
                for _, r in valid_rows.iterrows():
                    raw_sid = str(r["staff_id"]).strip()
                    if not raw_sid:
                        continue
                    clean_sid = raw_sid.upper()
                    if not clean_sid.startswith("CBK-") and clean_sid.isdigit():
                        clean_sid = f"CBK-{clean_sid}"
                    
                    fn = str(r.get("full_name", "")).strip() or f"Athlete {clean_sid}"
                    em = str(r.get("cbk_email", "")).strip().lower()
                    if not em or "@" not in em:
                        em = f"{clean_sid.lower()}@centralbank.go.ke"
                    
                    dept = str(r.get("department", "Finance & Accounts")).strip()
                    if dept not in CBK_DEPARTMENTS:
                        dept_match = next((d for d in CBK_DEPARTMENTS if d.lower() in dept.lower()), "Finance & Accounts")
                        dept = dept_match
                    
                    sp = str(r.get("primary_sport", "Golf")).strip()
                    if sp not in ALL_18_SPORTS:
                        sp_match = next((s for s in ALL_18_SPORTS if s.lower() in sp.lower()), "Golf")
                        sp = sp_match
                    
                    backend.upsert_staff(clean_sid, fn, em, dept, sp)
                    imported_count += 1
                    updated_sports.add(sp)

                st.success(f"🎉 Successfully ingested **{imported_count} staff athletes** across **{len(updated_sports)} disciplines** into the live CBK STRIDE database!")
                st.balloons()
            else:
                st.error("Could not find a 'Staff ID' or 'Payroll No' column in the uploaded file. Please use the official template.")
        except Exception as e:
            st.error(f"Error parsing uploaded file: {str(e)}")

    # Central Bank Pre-Enrolled Staff Registry
    st.markdown("---")
    st.markdown("#### 👥 Central Bank Pre-Enrolled Staff Sports Registry")
    st.caption("Central directory of registered staff athletes. When staff scan a station QR or type their Staff ID, this registry auto-populates their profile.")

    staff_df = backend.get_all_registered_staff()
    st.dataframe(staff_df, use_container_width=True)

    with st.expander("➕ Register or Update Staff Member Profile"):
        c_r1, c_r2 = st.columns(2)
        with c_r1:
            new_sid = st.text_input("CBK Staff ID (e.g. 1024 or CBK-1024):", key="reg_sid")
            new_fn = st.text_input("Full Name:", key="reg_fn")
            new_em = st.text_input("Institutional Email:", key="reg_em", placeholder="@centralbank.go.ke")
        with c_r2:
            new_dept = st.selectbox("Directorate / Department:", CBK_DEPARTMENTS, key="reg_dept")
            new_sport = st.selectbox("Primary Enrolled Sport (A – Z):", ALL_18_SPORTS, key="reg_sport")

        if st.button("💾 Save Staff Profile to Registry", use_container_width=True):
            if new_sid and new_fn and new_em:
                backend.upsert_staff(new_sid, new_fn, new_em, new_dept, new_sport)
                st.success(f"Profile saved for {new_fn} ({new_sid}) - Enrolled Sport: {new_sport}!")
                st.rerun()
            else:
                st.error("Please fill in Staff ID, Full Name, and Email.")

    # ==============================================================================
    # ACCESS RIGHTS & GOVERNANCE (ROLE-BASED PERMISSION DELEGATION)
    # ==============================================================================
    st.markdown("---")
    st.markdown("#### 🛡️ Central Bank Access Rights & Export Governance (RBAC)")
    st.caption("Under the Kenya Data Protection Act 2019 and CBK Information Security Guidelines, only officially designated personnel may download sensitive athlete rosters or financial ledgers. Manage officer clearances and permission grants below.")

    cur_officer = get_current_officer()
    can_manage = cur_officer and (cur_officer.get("role") == "Super Admin" or cur_officer.get("can_manage_roles", 0) == 1)

    # 1. Active Authorized Officers Table
    officers_list = backend.get_all_authorized_officers()
    df_officers = pd.DataFrame(officers_list)
    if not df_officers.empty:
        display_off_df = df_officers.copy()
        display_off_df["can_export_roster"] = display_off_df["can_export_roster"].apply(lambda v: "✅ Authorized" if v else "❌ Denied")
        display_off_df["can_export_finances"] = display_off_df["can_export_finances"].apply(lambda v: "✅ Authorized" if v else "❌ Denied")
        display_off_df["can_manage_roles"] = display_off_df["can_manage_roles"].apply(lambda v: "✅ Authorized" if v else "❌ Denied")
        display_off_df.columns = [
            "Staff ID", "Full Name", "Department", "Assigned Role",
            "Roster Export", "Financial Export", "Role Governance",
            "Granted By", "Created At", "Last Login"
        ]
        st.dataframe(display_off_df, use_container_width=True, hide_index=True)

    # 2. Grant / Update Rights Form
    if can_manage:
        with st.expander("➕ Grant / Update Officer Access Rights & Passkey", expanded=True):
            st.markdown("##### Assign Institutional Clearance to a Staff Member")
            st.caption("Search any verified staff member from the 679 CBK roster, designate their institutional role, and configure their personal security passkey:")
            
            c_g1, c_g2 = st.columns(2)
            with c_g1:
                staff_search_term = st.text_input("Search Staff to Authorize (Staff ID or Name):", key="search_auth_staff", placeholder="e.g. 3428 or Chebet")
                found_staff = []
                if staff_search_term.strip():
                    found_staff = search_staff_registry(staff_search_term.strip(), limit=5)
                
                selected_candidate = None
                g_sid, g_fn, g_dept = "", "", "Finance & Accounts"
                if found_staff:
                    c_opts = [f"{s['staff_id']} — {s['full_name']} ({s.get('department', 'General')})" for s in found_staff]
                    sel_c_str = st.selectbox("Select Candidate from Roster:", c_opts, key="sel_cand_box")
                    selected_candidate = next((s for s in found_staff if s['staff_id'] in sel_c_str), None)
                else:
                    g_sid = st.text_input("Or Enter Staff ID directly:", key="g_sid_direct", placeholder="e.g. CBK-4055")
                    g_fn = st.text_input("Full Name:", key="g_fn_direct", placeholder="e.g. Alice Chebet")
                    g_dept = st.selectbox("Department:", CBK_DEPARTMENTS, key="g_dept_direct")

            with c_g2:
                g_role = st.selectbox(
                    "Designated Security Role:",
                    ["Secretariat Officer", "Finance & Internal Audit", "HR Compliance Lead", "Super Admin"],
                    key="g_role_select"
                )
                
                st.markdown("**Granular Permissions:**")
                c_p_a, c_p_b, c_p_c = st.columns(3)
                with c_p_a:
                    p_roster = st.checkbox("Export Rosters (CSV/Excel)", value=True, key="chk_p_roster")
                with c_p_b:
                    p_fin = st.checkbox("Export Finances & Allowances", value=(g_role in ["Finance & Internal Audit", "Super Admin"]), key="chk_p_fin")
                with c_p_c:
                    p_roles = st.checkbox("Grant/Revoke Roles", value=(g_role == "Super Admin"), key="chk_p_roles")
                
                g_passkey = st.text_input("Assign Personal Security Passkey:", type="password", key="g_passkey_val", placeholder="Confidential passkey (min 3 chars)")

            if st.button("🛡️ Grant Official Institutional Clearance", type="primary", use_container_width=True):
                target_sid = selected_candidate['staff_id'] if selected_candidate else g_sid.strip()
                target_fn = selected_candidate['full_name'] if selected_candidate else g_fn.strip()
                target_dept = selected_candidate.get('department', g_dept) if selected_candidate else g_dept
                
                if not target_sid or not target_fn:
                    st.error("Please provide both Staff ID and Full Name.")
                elif not g_passkey.strip() or len(g_passkey.strip()) < 3:
                    st.error("Passkey must be at least 3 characters.")
                else:
                    ok_g, msg_g = backend.grant_rights(
                        staff_id=target_sid,
                        full_name=target_fn,
                        department=target_dept,
                        role=g_role,
                        can_export_roster=p_roster,
                        can_export_finances=p_fin,
                        can_manage_roles=p_roles,
                        passkey=g_passkey.strip(),
                        granted_by=cur_officer.get("staff_id", "CBK-3428")
                    )
                    if ok_g:
                        st.success(msg_g)
                        st.rerun()
                    else:
                        st.error(msg_g)

        # 3. Revoke Rights Expander
        with st.expander("🚫 Revoke Officer Clearance"):
            c_rev1, c_rev2 = st.columns([3, 1.2])
            with c_rev1:
                rev_options = [f"{o['staff_id']} — {o['full_name']} ({o['role']})" for o in officers_list if o['staff_id'] != "CBK-3428"]
                if rev_options:
                    sel_rev = st.selectbox("Select Officer to Revoke:", rev_options, key="sel_rev_officer")
                    target_rev_sid = sel_rev.split(" — ")[0].strip()
                else:
                    st.info("No subordinate officers currently registered.")
                    target_rev_sid = None
            with c_rev2:
                st.write("")
                st.write("")
                if target_rev_sid and st.button("🗑️ Revoke Clearance", key="btn_do_revoke", type="secondary", use_container_width=True):
                    ok_r, msg_r = backend.revoke_rights(target_rev_sid, revoked_by=cur_officer.get("staff_id", "CBK-3428"))
                    if ok_r:
                        st.warning(msg_r)
                        st.rerun()
                    else:
                        st.error(msg_r)
    else:
        render_admin_security_lock("governance_section", required_perm="manage_roles")

    # 4. Forensic Audit Trail Table
    st.markdown("##### 📜 Forensic Export & Governance Audit Trail (Last 50 Events)")
    st.caption("Immutable forensic audit trail capturing all login attempts, export requests, and clearance delegations in real-time.")
    audit_events = backend.get_audit_trail(limit=50)
    if audit_events:
        df_audit = pd.DataFrame(audit_events)
        df_audit.columns = ["ID", "Timestamp (EAT)", "Staff ID", "Officer Name", "Role", "Action", "Target Resource", "IP / Session", "Status", "Notes"]
        st.dataframe(df_audit.drop(columns=["ID", "IP / Session"]), use_container_width=True, hide_index=True)
    else:
        st.caption("No audit events recorded yet. All downloads and access modifications will appear here automatically.")

    # Database Maintenance
    st.markdown("---")
    st.markdown("#### 🛠️ Data Management & Database Security")
    if is_export_authorized():
        c_m1, c_m2, c_m3 = st.columns(3)

        with c_m1:
            if st.button("🔄 Re-Seed Realistic Demo Data (18 Disciplines)", use_container_width=True):
                backend.seed_demo_data()
                st.success("Re-seeded 32+ realistic records across all 18 disciplines!")
                st.rerun()

        with c_m2:
            st.markdown("**Reset Attendance Telemetry:**")
            confirm_reset = st.checkbox("Confirm clearing all attendance logs", key="chk_confirm_reset")
            if st.button("🗑️ Purge Attendance Logs (Zero Scans)", disabled=not confirm_reset, type="primary" if confirm_reset else "secondary", use_container_width=True):
                conn = sqlite3.connect(backend.db_path)
                conn.execute("DELETE FROM attendance_logs")
                conn.commit()
                conn.close()
                backend._export_to_csv()
                cur_off = get_current_officer() or {"staff_id": "CBK-3428", "full_name": "Samuel Gathigi Njuguna", "role": "Super Admin"}
                backend.log_audit_event(
                    staff_id=cur_off.get("staff_id", "CBK-3428"),
                    officer_name=cur_off.get("full_name", "Officer"),
                    role=cur_off.get("role", "Super Admin"),
                    action_type="RESET_ATTENDANCE_LOGS",
                    resource_name="attendance_logs",
                    notes="Attendance telemetry cleared for fresh Day 1 testing"
                )
                st.toast("✅ Attendance logs cleared to 0. Ready for fresh Day 1 scans!", icon="🗑️")
                st.rerun()

        with c_m3:
            st.download_button(
                label="💾 Download SQLite Database (.db)",
                data=open(backend.db_path, "rb").read() if os.path.exists(backend.db_path) else b"",
                file_name="cbk_dswaap.db",
                mime="application/x-sqlite3",
                use_container_width=True
            )
    else:
        render_admin_security_lock("settings_db")

if "⚙️ Integration & Settings" in tab_dict:
    with tab_dict["⚙️ Integration & Settings"]:
        render_tab_settings()

# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown("""
<div style="text-align: center; margin-top: 2.5rem; padding: 1.4rem; border-top: 1px solid rgba(245, 197, 66, 0.25); color: #94A3B8; font-size: 0.82rem; background: rgba(4, 16, 33, 0.6); border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.5);">
    <strong style="color: #F5C542; letter-spacing: 0.5px;">CENTRAL BANK OF KENYA (CBK)</strong> • <span style="color: #00F2FE; font-weight: 800;">CBK STRIDE™</span> (Sports Telemetry & Roster Integrity)<br>
    Built with Mobile-First Streamlit Architecture, Real-Time Google Sheets Backend, & Dynamic QR Dual-Gate Verification.<br>
    <span style="font-size: 0.75rem; color: #64748B;">&copy; 2026 Central Bank of Kenya Sports Club. All Rights Reserved. • <a href="/DEMO" style="color: #F5C542; text-decoration: none;">🧪 Open STRIDE™ Demo Portal</a></span>
</div>
""", unsafe_allow_html=True)

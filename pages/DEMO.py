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
# HIGH-PRECISION LUXURY THEME CSS (CBK GOLD, ROYAL NAVY & GLASSMORPHISM)
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #020710 !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebarNav"] { display: none !important; }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 98% !important;
    }

    /* Topbar styling */
    .demo-topbar {
        background: linear-gradient(135deg, #051429 0%, #0a254a 50%, #040e1c 100%) !important;
        padding: 1.25rem 1.6rem !important;
        border-radius: 16px !important;
        color: #FFFFFF !important;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7), 0 0 25px rgba(245, 197, 66, 0.2) !important;
        margin-bottom: 1.2rem !important;
        border: 1.5px solid rgba(245, 197, 66, 0.45) !important;
        border-bottom: 4px solid #F5C542 !important;
    }

    .kpi-card {
        background: rgba(8, 24, 48, 0.82) !important;
        border: 1px solid rgba(245, 197, 66, 0.25) !important;
        border-left: 5px solid #F5C542 !important;
        border-radius: 12px !important;
        padding: 1rem 1.2rem !important;
        margin-bottom: 0.8rem !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
    }

    .kpi-title {
        color: #94A3B8 !important;
        font-size: 0.78rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.6px !important;
    }

    .kpi-value {
        font-size: 1.85rem !important;
        font-weight: 900 !important;
        margin: 4px 0 !important;
        color: #FFFFFF !important;
    }

    .kpi-sub {
        color: #CBD5E1 !important;
        font-size: 0.75rem !important;
    }

    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #FFE899 0%, #F5C542 50%, #D4AF37 100%) !important;
        color: #040E1C !important;
        font-weight: 800 !important;
        border: none !important;
        border-radius: 8px !important;
    }

    .stButton>button[kind="secondary"] {
        background: rgba(8, 24, 48, 0.75) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(245, 197, 66, 0.35) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

now_dt = get_eat_now()

# ------------------------------------------------------------------------------
# 1. HEADER & TOP BAR
# ------------------------------------------------------------------------------
st.markdown(f"""
<div class="demo-topbar">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
        <div style="display: flex; align-items: center; gap: 18px;">
            <div style="background: rgba(245, 197, 66, 0.15); border: 2px solid #F5C542; border-radius: 12px; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; font-size: 1.9rem; box-shadow: 0 0 18px rgba(245, 197, 66, 0.35);">
                🧪
            </div>
            <div>
                <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                    <span style="background: linear-gradient(135deg, #FFE899 0%, #F5C542 100%); color: #040D1A; font-weight: 900; font-size: 0.72rem; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">
                        Interactive Sandbox Mode
                    </span>
                    <span style="color: #00F2FE; font-size: 0.8rem; font-weight: 700;">
                        ● Full Capabilities Unlocked
                    </span>
                </div>
                <h1 style="margin: 4px 0 0 0; font-size: 1.85rem; font-weight: 900; color: #FFFFFF; letter-spacing: -0.5px;">
                    STRIDE™ <span style="font-weight: 400; color: #F5C542; font-size: 1.1rem;">| Evaluator Sandbox & Sponsor Pavilion</span>
                </h1>
                <div style="font-size: 0.8rem; color: #94A3B8; margin-top: 2px;">
                    Sports Telemetry & Roster Integrity • Enterprise Tournament Management
                </div>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="background: rgba(4, 16, 33, 0.7); border: 1px solid rgba(245, 197, 66, 0.3); border-radius: 8px; padding: 6px 14px; font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #F5C542;">
                🕒 {now_dt.strftime('%A, %d %B %Y | %H:%M:%S')} (EAT)
            </div>
            <div style="margin-top: 6px; font-size: 0.76rem; color: #64748B;">
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
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(245, 197, 66, 0.14) 0%, rgba(0, 242, 254, 0.12) 100%); border: 1.5px solid #F5C542; border-radius: 12px; padding: 12px 18px; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.4rem;">💡</span>
            <div>
                <strong style="color: #FFE899; font-size: 0.92rem;">Welcome to the STRIDE™ Interactive Evaluation Sandbox</strong>
                <p style="margin: 2px 0 0 0; color: #CBD5E1; font-size: 0.82rem;">
                    Test-drive pitchside roll-calls, captain diaries, dual-gate QR check-ins, HR/Finance analytics, and commercial sponsor packages freely with synthetic data.
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with c_ban2:
    st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; gap: 8px; flex-direction: column;">
        <a href="/" target="_self" style="display: block; text-decoration: none;">
            <div style="background: rgba(8, 24, 48, 0.85); border: 1.5px solid rgba(245, 197, 66, 0.5); border-radius: 8px; padding: 7px 10px; text-align: center; color: #F5C542; font-weight: 800; font-size: 0.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                🏛️ Official CBK Portal
            </div>
        </a>
        <a href="/register" target="_self" style="display: block; text-decoration: none;">
            <div style="background: rgba(0, 242, 254, 0.15); border: 1.5px solid #00F2FE; border-radius: 8px; padding: 7px 10px; text-align: center; color: #00F2FE; font-weight: 800; font-size: 0.8rem;">
                🎟️ Public Registration & M-Pesa Gateway
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 3. CORPORATE BRAND PARTNER MARQUEE RIBBON
# ------------------------------------------------------------------------------
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(8, 24, 48, 0.95) 0%, rgba(4, 14, 28, 0.98) 100%); border: 1.5px solid rgba(245, 197, 66, 0.35); border-radius: 12px; padding: 9px 18px; margin-bottom: 1.2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
        <span style="background: linear-gradient(135deg, #FFE899 0%, #F5C542 100%); color: #040D1A; font-weight: 900; font-size: 0.72rem; padding: 3px 10px; border-radius: 6px; letter-spacing: 0.8px; text-transform: uppercase;">
            🏆 Official Brand Partners
        </span>
        <span style="color: #FFFFFF; font-size: 0.83rem; font-weight: 600;">
            <strong style="color: #F5C542;">KCB Bank Group</strong> (Title) &bull; <strong style="color: #34D399;">Safaricom M-Pesa</strong> (Fintech) &bull; <strong style="color: #00F2FE;">Britam</strong> (Wellness & Health) &bull; <strong style="color: #F7941D;">Brookside Dairy</strong> (Hydration)
        </span>
    </div>
    <div>
        <span style="font-size: 0.76rem; color: #94A3B8;">Audience Reach: <strong>18 Disciplines • 1,500+ Corporate Athletes</strong></span>
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
                b_color = "#F5C542" if "Tournament" in ev_type else ("#00F2FE" if "Friendly" in ev_type else "#34D399")
                st.markdown(f"""
                <div style="background: rgba(8, 24, 48, 0.75); border-left: 4.5px solid {b_color}; border-radius: 10px; padding: 12px 16px; margin-bottom: 10px;">
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
            <div style="background: linear-gradient(135deg, #071F3D 0%, #025BBF 100%); border: 1.5px solid rgba(245, 197, 66, 0.4); border-radius: 12px; padding: 16px; margin-top: 10px;">
                <span style="background: #F5C542; color: #040E1C; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 800;">VERIFIED ATHLETE</span>
                <h3 style="margin: 8px 0 2px 0; color: #FFF;">{p_match['full_name']}</h3>
                <p style="margin: 0; color: #CBD5E1; font-size: 0.85rem;">{p_match['department']} • {p_match.get('primary_sport', demo_discipline)}</p>
                <div style="margin-top: 10px; font-size: 0.8rem; color: #34D399; font-weight: 700;">
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
        st.markdown("""
        <div style="background: rgba(8, 24, 48, 0.9); border: 2px dashed rgba(245, 197, 66, 0.5); border-radius: 14px; padding: 20px; text-align: center;">
            <div style="font-size: 0.76rem; color: #F5C542; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">STRIDE™ Enterprise Sports Network</div>
            <h4 style="margin: 6px 0; color: #FFF;">OFFICIAL TOURNAMENT PARTICIPATION PASS</h4>
            <div style="font-size: 2.5rem; margin: 10px 0;">📱</div>
            <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; border-radius: 8px; padding: 8px; margin-bottom: 10px;">
                <span style="color: #34D399; font-weight: 800; font-size: 0.9rem;">VERIFIED SESSION RATE: KES 2,500</span><br>
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
        <div style="background: rgba(8, 24, 48, 0.85); border: 2px solid #F5C542; border-radius: 14px; padding: 22px; text-align: center; margin-top: 12px;">
            <span style="background: #F5C542; color: #040E1C; font-weight: 900; font-size: 0.78rem; padding: 3px 12px; border-radius: 6px;">
                {qr_mode}
            </span>
            <h3 style="margin: 10px 0 4px 0; color: #FFF;">{demo_discipline} Check-In Point</h3>
            <p style="margin: 0 0 16px 0; color: #94A3B8; font-size: 0.85rem;">Display on Captain's official tablet at pitch entrance</p>
            <div style="background: #FFFFFF; display: inline-block; padding: 18px; border-radius: 14px; box-shadow: 0 0 25px rgba(245, 197, 66, 0.35);">
                <img src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=https://cbk-stride.streamlit.app/" alt="Station QR Code" style="display: block; width: 220px; height: 220px;" />
            </div>
            <div style="margin-top: 14px; font-size: 0.8rem; color: #34D399; font-weight: 700;">
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
            <div style="background: linear-gradient(135deg, #091F3D 0%, #030F21 100%); border: 2px solid #F5C542; border-radius: 14px; padding: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); text-align: center;">
                <div style="font-size: 0.72rem; color: #F5C542; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase;">STRIDE™ ENTERPRISE DIGITAL PASS</div>
                <h3 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.15rem; font-weight: 800;">{ev_name}</h3>
                <span style="background: rgba(0, 242, 254, 0.2); color: #00F2FE; border: 1px solid rgba(0,242,254,0.4); padding: 2px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">
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
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #F5C542;">
            <div class="kpi-title">Today's Scans</div>
            <div class="kpi-value" style="color: #F5C542;">342</div>
            <div class="kpi-sub">Across All 18 Sports</div>
        </div>
        """, unsafe_allow_html=True)
    with sk2:
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #00F2FE;">
            <div class="kpi-title">Active on Field</div>
            <div class="kpi-value" style="color: #00F2FE;">58</div>
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
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #A78BFA;">
            <div class="kpi-title">Policy Compliance</div>
            <div class="kpi-value" style="color: #A78BFA;">98.4%</div>
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
        st.bar_chart(dept_data.set_index("Department"), color="#F5C542")

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
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #00F2FE;">
            <div class="kpi-title">Prevented Phantom Payouts</div>
            <div class="kpi-value" style="color: #00F2FE;">KES 145,000</div>
            <div class="kpi-sub">58 Incomplete Single-Gate Scans Disallowed</div>
        </div>
        """, unsafe_allow_html=True)
    with f_k3:
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #F5C542;">
            <div class="kpi-title">Audit Trail Integrity</div>
            <div class="kpi-value" style="color: #F5C542;">100.0%</div>
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
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #F5C542;">
            <div class="kpi-title">Active Sporting Disciplines</div>
            <div class="kpi-value" style="color: #F5C542;">18 Sports</div>
            <div class="kpi-sub">Golf, Football, Athletics & More</div>
        </div>
        """, unsafe_allow_html=True)
    with sp_k2:
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #00F2FE;">
            <div class="kpi-title">Audience & Athletes</div>
            <div class="kpi-value" style="color: #00F2FE;">1,500+</div>
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
        st.markdown("""
        <div class="kpi-card" style="border-left-color: #A78BFA;">
            <div class="kpi-title">Brand Exposure ROI</div>
            <div class="kpi-value" style="color: #A78BFA;">99.8%</div>
            <div class="kpi-sub">Real-Time Digital & Field Touchpoints</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Official Brand Partners
    st.markdown("#### 🏆 Official Corporate Brand Partners")
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        st.markdown("""
        <div style="background: rgba(8, 24, 48, 0.85); border: 1.5px solid rgba(0, 242, 254, 0.4); border-radius: 12px; padding: 18px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #00F2FE; font-size: 1.15rem; font-weight: 800;">🦁 KCB Bank Group</h4>
                <span style="background: rgba(0, 242, 254, 0.2); color: #00F2FE; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">Platinum Partner</span>
            </div>
            <p style="margin: 8px 0 4px 0; font-size: 0.88rem; color: #E2E8F0;">
                <strong>Official Banking & Financial Services Partner</strong> of the STRIDE™ Corporate Championship.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(8, 24, 48, 0.85); border: 1.5px solid rgba(245, 197, 66, 0.4); border-radius: 12px; padding: 18px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #F5C542; font-size: 1.15rem; font-weight: 800;">🛡️ Britam Holdings</h4>
                <span style="background: rgba(245, 197, 66, 0.2); color: #F5C542; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">Wellness Underwriter</span>
            </div>
            <p style="margin: 8px 0 4px 0; font-size: 0.88rem; color: #E2E8F0;">
                <strong>Official Sports Injury, Health & Wellness Underwriter</strong> for all tournament athletes.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with p_col2:
        st.markdown("""
        <div style="background: rgba(8, 24, 48, 0.85); border: 1.5px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 18px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #10B981; font-size: 1.15rem; font-weight: 800;">📱 Safaricom M-Pesa</h4>
                <span style="background: rgba(16, 185, 129, 0.2); color: #10B981; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">Tech Innovation</span>
            </div>
            <p style="margin: 8px 0 4px 0; font-size: 0.88rem; color: #E2E8F0;">
                <strong>Official Digital Payments & Connectivity Partner</strong> powering cashless tournament zones.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(8, 24, 48, 0.85); border: 1.5px solid rgba(167, 139, 250, 0.4); border-radius: 12px; padding: 18px; margin-bottom: 14px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="margin: 0; color: #A78BFA; font-size: 1.15rem; font-weight: 800;">🥛 Brookside Dairy</h4>
                <span style="background: rgba(167, 139, 250, 0.2); color: #A78BFA; padding: 3px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">Nutrition Partner</span>
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
        st.markdown("""
        <div style="background: rgba(8, 24, 48, 0.95); border: 2px solid #F5C542; border-radius: 12px; padding: 16px; height: 100%;">
            <div style="text-align: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem;">🥇</span>
                <h4 style="margin: 2px 0; color: #F5C542;">PLATINUM TITLE</h4>
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
        st.markdown("""
        <div style="background: rgba(8, 24, 48, 0.95); border: 2px solid #00F2FE; border-radius: 12px; padding: 16px; height: 100%;">
            <div style="text-align: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem;">🥈</span>
                <h4 style="margin: 2px 0; color: #00F2FE;">GOLD DISCIPLINE</h4>
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
        st.markdown("""
        <div style="background: rgba(8, 24, 48, 0.95); border: 2px solid #10B981; border-radius: 12px; padding: 16px; height: 100%;">
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
        st.markdown("""
        <div style="background: rgba(8, 24, 48, 0.95); border: 2px solid #A78BFA; border-radius: 12px; padding: 16px; height: 100%;">
            <div style="text-align: center; margin-bottom: 8px;">
                <span style="font-size: 1.5rem;">🎖️</span>
                <h4 style="margin: 2px 0; color: #A78BFA;">BRONZE DIGITAL</h4>
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
        st.markdown("""
        <div style="background: rgba(8, 24, 48, 0.7); border: 1px solid rgba(245, 197, 66, 0.3); border-radius: 12px; padding: 18px;">
            <h5 style="margin: 0 0 6px 0; color: #F5C542;">STRIDE™ Enterprise Operations</h5>
            <p style="margin: 0 0 8px 0; font-size: 0.85rem; color: #CBD5E1;">
                Secretariat & Commercial Sponsorship Directorate<br>
                Corporate Sports Complex, Nairobi, Kenya
            </p>
            <div style="font-size: 0.84rem; color: #94A3B8; line-height: 1.6;">
                📧 <strong>Email:</strong> <span style="color: #00F2FE;">partnerships@stride-enterprise.io</span><br>
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
st.markdown("""
<div style="text-align: center; margin-top: 2.5rem; padding: 1.4rem; border-top: 1px solid rgba(245, 197, 66, 0.25); color: #94A3B8; font-size: 0.82rem; background: rgba(4, 16, 33, 0.6); border-radius: 12px;">
    <strong style="color: #F5C542;">STRIDE™</strong> • Interactive Evaluation Sandbox & Corporate Sponsor Pavilion<br>
    <span style="font-size: 0.75rem; color: #64748B;">Enterprise Sports Telemetry & Tournament Operations • <a href="/" style="color: #00F2FE; text-decoration: none;">Return to Official CBK Portal</a> • <a href="/register" style="color: #F5C542; text-decoration: none;">🎟️ Public Accreditation & Ticketing Gateway</a></span>
</div>
""", unsafe_allow_html=True)

"""
================================================================================
STRIDE™ — PUBLIC SELF-REGISTRATION, M-PESA STK TICKETING & EVENT CREATOR WIZARD
Universal Event Accreditation & Digital Pass Platform
URL Route: /EVENTS
================================================================================
"""

import streamlit as st
import pandas as pd
import datetime
import time
import os
import sys
import textwrap
import importlib

# Ensure root directory is on sys.path for utils import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import utils
try:
    importlib.reload(utils)
except Exception:
    pass

from utils import (
    AttendanceBackend,
    get_eat_now
)

# ------------------------------------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------------------------------------
try:
    st.set_page_config(
        page_title="STRIDE™ | Event Registration & Ticketing",
        page_icon="🎟️",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
except Exception:
    pass

# ------------------------------------------------------------------------------
# LUXURY CSS THEME (ROYAL NAVY, GOLD & CYAN GLASSMORPHISM)
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }
    .stApp {
        background: radial-gradient(circle at 50% -20%, #061B33 0%, #020712 100%) !important;
        color: #F8FAFC !important;
    }
    .kpi-card {
        background: linear-gradient(135deg, rgba(7, 25, 51, 0.75) 0%, rgba(3, 13, 28, 0.95) 100%);
        border: 1px solid rgba(245, 197, 66, 0.25);
        border-left: 4.5px solid #F5C542;
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    }
    .kpi-title {
        font-size: 0.72rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #94A3B8;
    }
    .kpi-value {
        font-size: 1.65rem;
        font-weight: 900;
        margin: 4px 0 2px 0;
        color: #FFFFFF;
    }
    .kpi-sub {
        font-size: 0.78rem;
        color: #CBD5E1;
    }
    .event-card {
        background: rgba(8, 24, 48, 0.7);
        border: 1.5px solid rgba(0, 242, 254, 0.3);
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 16px;
    }
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 800 !important;
        transition: all 0.2s ease-in-out !important;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# BACKEND INITIALIZATION
# ------------------------------------------------------------------------------
if "backend" not in st.session_state:
    st.session_state.backend = AttendanceBackend()

backend: AttendanceBackend = st.session_state.backend
now_dt = get_eat_now()

# ------------------------------------------------------------------------------
# READ QUERY PARAMS (IF ACCESSED VIA DIRECT EVENT QR OR LINK)
# ------------------------------------------------------------------------------
param_event_id = st.query_params.get("event_id", "")
is_bks_mode = (param_event_id == "EVT-BANKI-KUU-SACCO" or "bks" in st.query_params or "bksacco" in st.query_params or "bankikuu" in st.query_params or st.query_params.get("bks", "") == "1")
if is_bks_mode:
    param_event_id = "EVT-BANKI-KUU-SACCO"

# ------------------------------------------------------------------------------
# TOP GLOBAL NAVIGATION BAR
# ------------------------------------------------------------------------------
if is_bks_mode:
    c_nav1, c_nav2 = st.columns([2.2, 1.1])
    with c_nav1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 14px; padding: 10px 0;">
            <div style="background: linear-gradient(135deg, #F5C542 0%, #D4AF37 50%, #996515 100%); width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.6rem; box-shadow: 0 4px 18px rgba(245,197,66,0.4);">
                🏦
            </div>
            <div>
                <h2 style="margin: 0; font-size: 1.45rem; font-weight: 900; color: #FFFFFF; letter-spacing: -0.5px;">
                    Banki Kuu SACCO <span style="font-weight: 500; color: #F5C542; font-size: 1rem;">| Shareholder Accreditation & E-Voting Portal</span>
                </h2>
                <div style="font-size: 0.78rem; color: #94A3B8;">
                    Central Bank of Kenya Staff SACCO Society Ltd. • 58th AGM & Board Elections • KICC Main Auditorium
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_nav2:
        st.markdown(f"""
        <div style="text-align: right; margin-top: 8px;">
            <span style="background: rgba(245, 197, 66, 0.15); border: 1.5px solid #F5C542; color: #F5C542; padding: 5px 14px; border-radius: 20px; font-size: 0.76rem; font-weight: 900; letter-spacing: 0.5px; box-shadow: 0 0 12px rgba(245,197,66,0.2);">
                👑 BANKI KUU SACCO LIVE PORTAL
            </span>
            <div style="font-size: 0.72rem; color: #64748B; margin-top: 4px;">
                <span style="color: #94A3B8;">Central Bank of Kenya</span> • <a href="/DEMO" style="color: #00F2FE; text-decoration: none;">🧪 Evaluator Sandbox</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    c_nav1, c_nav2 = st.columns([2, 1.2])
    with c_nav1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 14px; padding: 10px 0;">
            <div style="background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%); width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; box-shadow: 0 4px 15px rgba(0,242,254,0.3);">
                🎟️
            </div>
            <div>
                <h2 style="margin: 0; font-size: 1.45rem; font-weight: 900; color: #FFFFFF; letter-spacing: -0.5px;">
                    STRIDE™ <span style="font-weight: 400; color: #F5C542; font-size: 1rem;">| Public Accreditation & Event Gateway</span>
                </h2>
                <div style="font-size: 0.78rem; color: #94A3B8;">
                    Self-Registration • M-Pesa STK Ticketing • Universal Event Creator • Anti-Counterfeit QR Gates
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_nav2:
        st.markdown(f"""
        <div style="text-align: right; margin-top: 10px;">
            <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #34D399; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 800;">
                ● M-PESA DARAJA LIVE GATEWAY
            </span>
            <div style="font-size: 0.72rem; color: #64748B; margin-top: 4px;">
                <span style="color: #94A3B8;">STRIDE™ Enterprise</span> • <a href="/DEMO" style="color: #F5C542; text-decoration: none;">🧪 Evaluator Sandbox</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Track active delegate ticket across tabs
active_ticket_param = (
    st.query_params.get("confirm")
    or st.query_params.get("ticket_id")
    or st.query_params.get("tkt")
    or st.query_params.get("vote_tkt")
    or st.query_params.get("verify_tkt")
)
if active_ticket_param:
    st.session_state["active_ticket_id"] = active_ticket_param.strip()

# ------------------------------------------------------------------------------
# MAIN PORTAL TABS
# ------------------------------------------------------------------------------
if is_bks_mode:
    tab_reg, tab_wizard, tab_verify, tab_ballot, tab_nlp = st.tabs([
        "🎟️ Shareholder Accreditation & Bulk Roster",
        "💳 SACCO Finance Manager Payment & Scoping",
        "📷 Gate Usher Scanner & Quorum Meter",
        "🗳️ Digital Voting & Elections Booth",
        "🤖 Member Feedback & Sentiment Analysis"
    ])
else:
    tab_reg, tab_wizard, tab_verify, tab_ballot, tab_nlp = st.tabs([
        "🎟️ Attendee Registration & Digital Pass",
        "🪄 Event Creator Wizard (Organizers)",
        "📷 Gate Usher Scanner & Accreditation Roster",
        "🗳️ Digital Voting & Elections Booth",
        "🤖 NLP Attendee Sentiment & Pulse Survey"
    ])

# ==============================================================================
# TAB 1: ATTENDEE REGISTRATION & M-PESA TICKETING
# ==============================================================================
with tab_reg:
    # Ensure Banki Kuu SACCO ready-to-demo event exists in database
    bk_event = backend.ensure_banki_kuu_sacco_event()

    if is_bks_mode:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(245, 197, 66, 0.22) 0%, rgba(9, 31, 61, 0.95) 100%); border: 2px solid #F5C542; border-radius: 12px; padding: 16px 20px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; gap: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.5);">
            <div>
                <span style="background: #F5C542; color: #020712; font-weight: 900; padding: 3px 10px; border-radius: 4px; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.2px;">
                    🏦 CENTRAL BANK OF KENYA STAFF SACCO SOCIETY LTD.
                </span>
                <h3 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.25rem; font-weight: 900;">
                    58th Annual General Meeting & Board Elections Platform
                </h3>
                <div style="font-size: 0.82rem; color: #CBD5E1;">
                    Statutory Shareholder Accreditation • M-Pesa Digital Pass • Live SASRA Quorum Telemetry • Encrypted E-Voting
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(245, 197, 66, 0.18) 0%, rgba(9, 31, 61, 0.85) 100%); border: 2px solid #F5C542; border-radius: 12px; padding: 14px 18px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; gap: 12px; box-shadow: 0 6px 20px rgba(0,0,0,0.45);">
            <div>
                <span style="background: #F5C542; color: #020712; font-weight: 900; padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 1px;">
                    🏦 READY-TO-DEMO SUITE
                </span>
                <h4 style="margin: 4px 0 2px 0; color: #FFFFFF; font-size: 1.1rem; font-weight: 800;">
                    Banki Kuu SACCO — 58th AGM & Board Elections Platform
                </h4>
                <div style="font-size: 0.78rem; color: #CBD5E1;">
                    Pre-configured for statutory shareholder accreditation, M-Pesa digital pass, live SASRA quorum tracking & encrypted e-voting.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if is_bks_mode:
        with st.expander("🎬 WATCH LIVE MOTION DEMO: 5-Step SACCO AGM Delegate Journey (Interactive Boardroom Video)", expanded=True):
            try:
                import streamlit.components.v1 as components
                import motion_demo
                motion_html = motion_demo.get_bks_motion_html()
                components.html(motion_html, height=620, scrolling=True)
            except Exception as ex:
                st.info("💡 Interactive Motion Video Simulation ready for Board Presentation.")

    if is_bks_mode:
        st.markdown("### 🎟️ Banki Kuu SACCO Delegate Accreditation & Dynamic QR Pass")
        st.caption("Accredit for the Banki Kuu Staff SACCO 58th AGM & Board Elections. Receive your certified mobile pass & secret voting token instantly:")
    else:
        st.markdown("### 🎟️ Attendee Self-Registration & Dynamic QR Ticket Pass")
        st.caption("Register for upcoming corporate sports championships, AGMs, conferences, galas, or marathons. Pay via Safaricom M-Pesa STK Push and receive an encrypted digital pass instantly:")

    # Retrieve published events from SQLite
    all_events = backend.get_events(status="ACTIVE")
    if not all_events:
        st.warning("No active events currently published. Use the 'Event Creator Wizard' tab to create your first event!")
    else:
        if is_bks_mode:
            selected_event = bk_event
        else:
            # Category Filter Pull-Down
            col_flt1, col_flt2 = st.columns([1.4, 2])
            with col_flt1:
                cat_filter = st.selectbox(
                    "Filter Events by Type (Pull-Down):*",
                    [
                        "🌟 All Events & Assemblies",
                        "👔 Annual General Meetings (AGM) & Shareholder Assemblies",
                        "🏆 Sports Tournaments & Derbies",
                        "🏃 Marathons, Fun Runs & Athletics",
                        "💡 Industry Conferences & Summits",
                        "🎉 Corporate Galas & Dinners"
                    ],
                    key="pub_cat_filter"
                )

            # Filter events list based on category pull-down
            filtered_events = all_events
            if "AGM" in cat_filter:
                filtered_events = [e for e in all_events if "AGM" in e['category'].upper() or "AGM" in e['title'].upper() or "SHAREHOLDER" in e['title'].upper() or "GENERAL MEETING" in e['title'].upper()]
            elif "Sports" in cat_filter:
                filtered_events = [e for e in all_events if "SPORTS" in e['category'].upper() or "DERBY" in e['title'].upper()]
            elif "Marathon" in cat_filter:
                filtered_events = [e for e in all_events if "MARATHON" in e['category'].upper() or "RUN" in e['title'].upper()]
            elif "Conference" in cat_filter:
                filtered_events = [e for e in all_events if "CONFERENCE" in e['category'].upper() or "SUMMIT" in e['title'].upper()]
            elif "Gala" in cat_filter:
                filtered_events = [e for e in all_events if "GALA" in e['category'].upper() or "DINNER" in e['title'].upper()]

            if not filtered_events:
                filtered_events = all_events

            event_options = {f"{e['title']} ({e['event_id']})": e for e in filtered_events}
            
            # Default index preference for Banki Kuu SACCO if available
            default_idx = 0
            for idx, k in enumerate(event_options.keys()):
                if "BANKI-KUU-SACCO" in k.upper() or "BANKI KUU" in k.upper():
                    default_idx = idx
                    break
            if param_event_id:
                for idx, k in enumerate(event_options.keys()):
                    if param_event_id.upper() in k.upper():
                        default_idx = idx
                        break

            selected_label = st.selectbox(
                "Select Event / Function to Register For:*",
                list(event_options.keys()),
                index=default_idx,
                key="pub_reg_event_sel"
            )
            selected_event = event_options[selected_label]

        is_agm = ("AGM" in selected_event['category'].upper() or "AGM" in selected_event['title'].upper() or "SHAREHOLDER" in selected_event['title'].upper() or "GENERAL MEETING" in selected_event['title'].upper())

        # Display Event Overview Card
        badge_border_color = "#F5C542" if is_agm else "#00F2FE"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(8, 28, 58, 0.8) 0%, rgba(4, 14, 30, 0.9) 100%); border: 1.5px solid rgba(245, 197, 66, 0.4); border-left: 5px solid {badge_border_color}; border-radius: 12px; padding: 16px 20px; margin: 12px 0 20px 0;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px;">
                <div>
                    <span style="background: rgba(0, 242, 254, 0.15); color: #00F2FE; border: 1px solid rgba(0,242,254,0.3); padding: 2px 8px; border-radius: 4px; font-size: 0.72rem; font-weight: 800; text-transform: uppercase;">
                        {selected_event['category']}
                    </span>
                    <h3 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.25rem; font-weight: 800;">{selected_event['title']}</h3>
                    <p style="margin: 0; font-size: 0.85rem; color: #CBD5E1;">
                        🏢 Organized by <strong>{selected_event['organizer_name']}</strong>
                    </p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.85rem; color: #F5C542; font-weight: 700;">
                        🗓️ {selected_event['event_date']} at {selected_event['event_time']}
                    </div>
                    <div style="font-size: 0.78rem; color: #94A3B8;">
                        📍 {selected_event['venue']}
                    </div>
                </div>
            </div>
            <div style="margin-top: 10px; font-size: 0.82rem; color: #94A3B8; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 8px;">
                📝 <em>{selected_event['description'] or 'Official event accredited under STRIDE™ Enterprise System.'}</em>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_reg_f, col_reg_pass = st.columns([1.2, 1])

        with col_reg_f:
            st.markdown("#### 👤 Attendee Information")
            with st.form(key=f"form_pub_reg_{selected_event['event_id']}"):
                std_p = float(selected_event.get("standard_price", 1000.0))
                vip_p = float(selected_event.get("vip_price", 3500.0))
                is_free_event = (std_p == 0.0 and vip_p == 0.0)

                # AGM-SPECIFIC ACCREDITATION PULL-DOWN
                if is_agm:
                    st.markdown("""
                    <div style="background: rgba(245, 197, 66, 0.12); border: 1px solid #F5C542; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;">
                        <strong style="color: #F5C542; font-size: 0.88rem;">🏛️ Statutory AGM Shareholder Accreditation Mode</strong>
                        <p style="margin: 2px 0 0 0; color: #CBD5E1; font-size: 0.78rem;">
                            Please select your shareholder voting credential below to receive your certified voting pass and record your presence towards quorum.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    agm_del_status = st.selectbox(
                        "Accredited Member / Shareholder Status (Pull-down):*",
                        [
                            "🗳️ Principal Shareholder / Voting Member (Direct Voting Rights)",
                            "📜 Duly Appointed Proxy Holder (Signed Proxy Form Deposited)",
                            "👔 Executive Board Director / Committee Member",
                            "🏛️ Institutional Shareholder / Fund Representative",
                            "⚖️ Company Secretary & Legal Counsel",
                            "👁️ Independent Auditor / Regulatory Observer (CMA / SASRA)"
                        ],
                        key=f"agm_del_{selected_event['event_id']}"
                    )

                    default_acc = "SACCO-3428" if "BANKI-KUU-SACCO" in selected_event['event_id'].upper() else ""
                    agm_acc_num = st.text_input(
                        "Shareholder / CDSC / Member Account Number:*",
                        value=default_acc,
                        placeholder="e.g. CDSC-8492019 / SACCO-1049 / MEM-3428",
                        key=f"agm_acc_{selected_event['event_id']}"
                    )

                    agm_voting_shares = st.selectbox(
                        "Voting Power / Share Capital Bracket (Pull-down):*",
                        [
                            "1 Vote (Standard Ordinary Member / 1-Person 1-Vote)",
                            "1,000 – 10,000 Shares (Tier 1 Voting Block)",
                            "10,001 – 100,000 Shares (Tier 2 Voting Block)",
                            "100,000+ Shares (Institutional Investor / Major Block)",
                            "0 Votes (Non-Voting Delegate / Observer)"
                        ],
                        key=f"agm_shares_{selected_event['event_id']}"
                    )

                    tier_clean_name = agm_del_status.split("(")[0].strip()
                    chosen_amt = 0.0 if is_bks_mode else 5000.0  # Paid centrally by SACCO Finance Manager for BKS mode

                else:
                    # Standard Non-AGM Ticket Tier Selection
                    tier_choice = st.radio(
                        "Select Registration Tier:*",
                        [
                            f"Standard Athlete / Participant Pass — KES {std_p:,.0f}",
                            f"VIP Executive Delegate (Includes Hospitality) — KES {vip_p:,.0f}"
                        ],
                        key="reg_tier_radio"
                    )
                    chosen_amt = std_p if "Standard" in tier_choice else vip_p
                    tier_clean_name = "Standard Pass" if "Standard" in tier_choice else "VIP Executive Pass"

                def_name = ""
                def_email = ""
                def_org = "Banki Kuu Staff SACCO Society" if "BANKI-KUU-SACCO" in selected_event['event_id'].upper() else ""
                def_phone = ""

                att_name = st.text_input("Full Name (as per Official ID / National ID):*", value=def_name, placeholder="e.g. Samuel Gathigi")
                att_email = st.text_input("Email Address (for pass delivery):*", value=def_email, placeholder="e.g. member@centralbank.go.ke")
                att_org = st.text_input("Organization / Company / Sacco Branch:*", value=def_org, placeholder="e.g. Governor's Secretariat / Bank Supervision")
                phone_lbl = "Mobile Phone Number (for WhatsApp Pass delivery):*" if is_bks_mode else "Safaricom M-Pesa Phone Number:*"
                phone_hlp = "Mobile number to receive instant WhatsApp pass & voting credentials" if is_bks_mode else "Mobile number for STK Push prompt"
                att_phone = st.text_input(phone_lbl, placeholder="07XX XXX XXX", value=def_phone, help=phone_hlp)

                if is_bks_mode:
                    st.markdown(f"""
                    <div style="background: rgba(16, 185, 129, 0.15); border: 1.5px solid #10B981; border-radius: 8px; padding: 12px 16px; margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #34D399; font-weight: 800; font-size: 0.92rem;">🏛️ Member Accreditation: KES 0 (Complimentary)</span>
                            <span style="background: #10B981; color: #020712; font-size: 0.68rem; font-weight: 900; padding: 2px 6px; border-radius: 4px;">SACCO PRE-PAID</span>
                        </div>
                        <span style="color: #CBD5E1; font-size: 0.76rem;">Platform deployment & accreditation fees paid centrally by <strong>Banki Kuu Staff SACCO Secretariat</strong>. Members do not pay.</span>
                    </div>
                    """, unsafe_allow_html=True)
                    btn_sub_ticket = st.form_submit_button("✅ Accredit Member & Generate Mobile Pass", type="primary", use_container_width=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(16, 185, 129, 0.12); border: 1.5px solid #10B981; border-radius: 8px; padding: 12px 16px; margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #34D399; font-weight: 800; font-size: 0.92rem;">💰 Total Payable: KES {chosen_amt:,.0f}</span>
                            <span style="background: #10B981; color: #020712; font-size: 0.68rem; font-weight: 900; padding: 2px 6px; border-radius: 4px;">DARAJA STK</span>
                        </div>
                        <span style="color: #94A3B8; font-size: 0.74rem;">Paybill: <strong>{selected_event['mpesa_paybill']}</strong> • Instant Automated Handset Push</span>
                    </div>
                    """, unsafe_allow_html=True)
                    btn_sub_ticket = st.form_submit_button(f"📲 Pay KES {chosen_amt:,.0f} via M-Pesa STK & Register", type="primary", use_container_width=True)

                if btn_sub_ticket:
                    if not att_name.strip():
                        st.error("Please enter your Full Name.")
                    elif not att_email.strip() or "@" not in att_email:
                        st.error("Please provide a valid email address.")
                    elif not att_phone.strip() or len(att_phone.strip()) < 9:
                        st.error("Please provide a valid Safaricom phone number.")
                    elif is_agm and not agm_acc_num.strip():
                        st.error("Please provide your Shareholder / CDSC / Member Account Number.")
                    else:
                        org_tag = f"{att_org.strip()} (Ref: {agm_acc_num.strip()})" if is_agm else att_org.strip()
                        
                        if is_bks_mode:
                            # Direct complimentary accreditation for Banki Kuu SACCO member
                            sim_tx = f"BKS-ACC-{int(time.time())}"[-10:]
                            ok_t, msg_t, tkt_obj = backend.register_event_ticket(
                                event_id=selected_event["event_id"],
                                attendee_name=att_name.strip(),
                                email=att_email.strip(),
                                phone=att_phone.strip(),
                                organization=org_tag or "Banki Kuu SACCO Member",
                                ticket_tier=tier_clean_name,
                                amount_paid=0.0,
                                mpesa_trans_id=sim_tx
                            )
                            if ok_t:
                                st.session_state["pub_active_ticket"] = tkt_obj
                                st.session_state["pub_active_event"] = selected_event
                                st.session_state["stk_pending_payload"] = None
                                st.success(f"🎉 Accredited! {att_name.strip()} has been recorded. Digital mobile pass issued.")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error(msg_t)
                        else:
                            # Set STK Pending Payload to trigger interactive handset simulator for paid tickets
                            st.session_state["stk_pending_payload"] = {
                                "event_id": selected_event["event_id"],
                                "event_title": selected_event["title"],
                                "attendee_name": att_name.strip(),
                                "email": att_email.strip(),
                                "phone": att_phone.strip(),
                                "organization": org_tag or "Independent Delegate",
                                "ticket_tier": tier_clean_name,
                                "amount_paid": chosen_amt,
                                "paybill": selected_event.get("mpesa_paybill", "849200"),
                                "acc_num": agm_acc_num.strip() if is_agm else att_phone.strip()[-4:],
                                "is_agm": is_agm
                            }
                            st.session_state["pub_active_ticket"] = None
                            st.rerun()

            # ==================================================================
            # BULK ROSTER UPLOAD & BATCH DELEGATE PIPELINE
            # ==================================================================
            st.markdown("---")
            with st.expander("⚡ Bulk Member Roster Pipeline & 500-Delegate Batch Pass Engine", expanded=(selected_event["event_id"] == "EVT-BANKI-KUU-SACCO")):
                st.markdown("""
                <div style="background: rgba(8, 24, 48, 0.7); border: 1.5px solid rgba(245, 197, 66, 0.4); border-radius: 10px; padding: 12px 16px; margin-bottom: 12px;">
                    <strong style="color: #F5C542; font-size: 0.9rem;">🚀 Enterprise Bulk Accreditation Pipeline</strong>
                    <p style="margin: 4px 0 0 0; color: #CBD5E1; font-size: 0.78rem;">
                        Eliminate manual registration for 500+ delegates. Upload a confirmed attendance CSV/Excel file or generate a synthetic 500-member Banki Kuu SACCO cohort with 1 click to achieve instant SASRA quorum accreditation.
                    </p>
                </div>
                """, unsafe_allow_html=True)

                col_blk1, col_blk2 = st.columns(2)
                with col_blk1:
                    sample_template_df = pd.DataFrame([{
                        "Member_ID": "SACCO-1001",
                        "Full_Name": "Samuel Gathigi Njuguna",
                        "Email": "sam.gathigi@gmail.com",
                        "Phone": "0722849000",
                        "Organization_Branch": "Banki Kuu Staff SACCO — Governor's Secretariat",
                        "Accreditation_Role": "🗳️ Principal Shareholder / Voting Member",
                        "Amount_Paid": 5000.0,
                        "Attendance_Confirmed": "YES"
                    }, {
                        "Member_ID": "SACCO-1002",
                        "Full_Name": "Dr. Beatrice Kiptoo",
                        "Email": "b.kiptoo@centralbank.go.ke",
                        "Phone": "0733456789",
                        "Organization_Branch": "Banki Kuu Staff SACCO — Bank Supervision",
                        "Accreditation_Role": "👔 Executive Board Director / Committee Member",
                        "Amount_Paid": 5000.0,
                        "Attendance_Confirmed": "YES"
                    }])
                    
                    st.download_button(
                        label="📥 Download Roster Template (.csv)",
                        data=sample_template_df.to_csv(index=False).encode('utf-8'),
                        file_name="Banki_Kuu_SACCO_Master_Delegate_Template.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                with col_blk2:
                    if st.button("⚡ Generate & Ingest 500-Delegate Cohort", type="primary", use_container_width=True, key="btn_gen_500_sacco"):
                        with st.spinner("Generating 500 Banki Kuu SACCO accredited delegates..."):
                            df_500 = backend.generate_synthetic_sacco_roster_df(500)
                            ok_bulk, msg_bulk, stats_bulk = backend.bulk_ingest_event_tickets(selected_event["event_id"], df_500)
                            if ok_bulk:
                                st.success(f"🎉 SUCCESS! {stats_bulk['total_ingested']} Banki Kuu SACCO delegates accredited and loaded into SQLite DB!")
                                st.balloons()
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(msg_bulk)

                st.markdown("##### 📂 Or Drag & Drop Custom CSV / Excel Attendance File:")
                uploaded_roster = st.file_uploader(
                    "Upload Delegate Attendance Roster (CSV / XLSX):",
                    type=["csv", "xlsx", "xls"],
                    key=f"uploader_roster_{selected_event['event_id']}"
                )

                if uploaded_roster is not None:
                    try:
                        if uploaded_roster.name.endswith(".csv"):
                            df_up = pd.read_csv(uploaded_roster)
                        else:
                            df_up = pd.read_excel(uploaded_roster)
                        
                        st.dataframe(df_up.head(5), use_container_width=True)
                        st.info(f"Loaded file '{uploaded_roster.name}' containing {len(df_up)} delegates.")

                        if st.button(f"🚀 Execute Bulk Accreditation for {len(df_up)} Delegates", type="primary", use_container_width=True, key="btn_exec_bulk_up"):
                            ok_b, msg_b, stats_b = backend.bulk_ingest_event_tickets(selected_event["event_id"], df_up)
                            if ok_b:
                                st.success(msg_b)
                                st.balloons()
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(msg_b)
                    except Exception as ex_up:
                        st.error(f"Error reading file: {ex_up}")

        with col_reg_pass:
            stk_p = st.session_state.get("stk_pending_payload", None)
            cur_ticket = st.session_state.get("pub_active_ticket", None)
            cur_evt = st.session_state.get("pub_active_event", selected_event)

            if stk_p:
                st.markdown("#### 📱 Safaricom M-Pesa STK Push Simulator")
                st.markdown(f"""
                <div style="background: radial-gradient(circle, #0F172A 0%, #020617 100%); border: 3px solid #22C55E; border-radius: 20px; padding: 22px; text-align: center; box-shadow: 0 14px 40px rgba(34, 197, 94, 0.45); margin-bottom: 16px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(34, 197, 94, 0.3); padding-bottom: 8px;">
                        <span style="color: #22C55E; font-weight: 900; font-size: 0.82rem; letter-spacing: 1.2px;">● SAFARICOM M-PESA DARAJA STK</span>
                        <span style="background: rgba(34, 197, 94, 0.2); color: #4ADE80; font-size: 0.68rem; font-weight: 800; padding: 2px 8px; border-radius: 10px;">HANDSET POPUP</span>
                    </div>
                    <div style="margin: 16px 0 6px 0; color: #FFFFFF; font-size: 1.15rem; font-weight: 800;">
                        Pay KES {stk_p['amount_paid']:,.0f} to<br><span style="color: #38BDF8;">STRIDE™ AGM GATEWAY</span>?
                    </div>
                    <div style="font-size: 0.78rem; color: #94A3B8; margin-bottom: 12px;">
                        Paybill: <strong>{stk_p['paybill']}</strong> • Ref: <strong>{stk_p['acc_num']}</strong><br>
                        Prompt dispatched to: <strong>{stk_p['phone']}</strong>
                    </div>
                    <div style="background: rgba(30, 41, 59, 0.9); border: 1.5px solid #22C55E; border-radius: 8px; padding: 10px; margin: 12px 0; color: #22C55E; font-family: monospace; font-size: 1.4rem; letter-spacing: 6px;">
                        ••••
                    </div>
                    <div style="font-size: 0.72rem; color: #94A3B8;">
                        Tap below to simulate entering your M-Pesa PIN on handset:
                    </div>
                </div>
                """, unsafe_allow_html=True)

                c_s1, c_s2 = st.columns([1.5, 1])
                with c_s1:
                    btn_auth_stk = st.button(
                        f"✅ Enter PIN & Authorize (KES {stk_p['amount_paid']:,.0f})",
                        type="primary",
                        use_container_width=True,
                        key="btn_confirm_stk_handset"
                    )
                with c_s2:
                    btn_cancel_stk = st.button("❌ Cancel", use_container_width=True, key="btn_cancel_stk_handset")

                if btn_auth_stk:
                    sim_tx = f"QK{int(time.time())}"[-10:]
                    ok_t, msg_t, tkt_obj = backend.register_event_ticket(
                        event_id=stk_p["event_id"],
                        attendee_name=stk_p["attendee_name"],
                        email=stk_p["email"],
                        phone=stk_p["phone"],
                        organization=stk_p["organization"],
                        ticket_tier=stk_p["ticket_tier"],
                        amount_paid=stk_p["amount_paid"],
                        mpesa_trans_id=sim_tx
                    )
                    if ok_t:
                        st.session_state["pub_active_ticket"] = tkt_obj
                        st.session_state["pub_active_event"] = selected_event
                        st.session_state["stk_pending_payload"] = None
                        st.success(f"🎉 M-Pesa Confirmed! KES {stk_p['amount_paid']:,.0f} paid. Receipt: `{sim_tx}`. Digital pass issued.")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(msg_t)

                if btn_cancel_stk:
                    st.session_state["stk_pending_payload"] = None
                    st.info("Transaction cancelled.")
                    st.rerun()

            elif not cur_ticket:
                st.markdown("#### 🎟️ Digital Mobile Pass")
                info_msg = "👈 Fill out the form on the left and tap **'Accredit Member & Generate Mobile Pass'** to generate your official pass." if is_bks_mode else "👈 Fill out the registration form on the left and tap **'Pay KES 5,000 via M-Pesa STK & Register'** to generate your official pass."
                st.info(info_msg)
                st.markdown("""
                <div style="background: rgba(8, 24, 48, 0.6); border: 2px dashed rgba(255,255,255,0.15); border-radius: 12px; padding: 30px 20px; text-align: center; color: #64748B; margin-bottom: 12px;">
                    <div style="font-size: 3rem; margin-bottom: 8px;">🎟️</div>
                    <div style="font-weight: 700; color: #94A3B8; font-size: 0.95rem;">No Active Member Pass Rendered Yet</div>
                    <div style="font-size: 0.78rem; margin-top: 4px;">Your encrypted dynamic QR ticket pass will render here immediately following accreditation.</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("⚡ Quick Demo: Load Sample Accredited Pass", use_container_width=True, key="btn_quick_demo_pass"):
                    st.session_state["pub_active_ticket"] = {
                        "ticket_id": "TKT-BK-342801",
                        "attendee_name": "Samuel Gathigi Njuguna",
                        "organization": "Banki Kuu SACCO — Governor's Secretariat",
                        "ticket_tier": "Principal Shareholder / Voting Member",
                        "amount_paid": 0.0,
                        "mpesa_trans_id": "BKS-ACC-342801",
                        "gate_status": "REGISTERED"
                    }
                    st.session_state["pub_active_event"] = selected_event
                    st.rerun()
            else:
                st.markdown("#### 🎟️ Digital Mobile Pass")
                t_tx = cur_ticket["mpesa_trans_id"]
                t_id = cur_ticket["ticket_id"]
                t_name = cur_ticket["attendee_name"]
                t_org = cur_ticket["organization"]
                t_tier = cur_ticket["ticket_tier"]
                t_amt = cur_ticket["amount_paid"]

                # Generate dynamic scannable QR Code pointing to instant verification URL
                verify_qr_data = f"https://cbk-stride.streamlit.app/EVENTS?verify_tkt={t_id}"
                qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={verify_qr_data}"

                st.markdown(textwrap.dedent(f"""
                <div style="background: linear-gradient(135deg, #091F3D 0%, #030F21 100%); border: 2.5px solid #F5C542; border-radius: 16px; padding: 20px; box-shadow: 0 12px 36px rgba(0,0,0,0.65); text-align: center;">
                    <div style="font-size: 0.72rem; color: #F5C542; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase;">STRIDE™ ENTERPRISE DIGITAL PASS</div>
                    <h3 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.15rem; font-weight: 800;">{cur_evt['title']}</h3>
                    <div style="margin: 4px 0 10px 0;">
                        <span style="background: rgba(0, 242, 254, 0.2); color: #00F2FE; border: 1px solid rgba(0,242,254,0.4); padding: 3px 12px; border-radius: 6px; font-size: 0.72rem; font-weight: 800;">
                            {t_tier}
                        </span>
                    </div>
                    <div style="background: #FFFFFF; border-radius: 12px; padding: 10px; display: inline-block; margin: 10px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                        <img src="{qr_code_url}" alt="Ticket QR" style="display: block; width: 160px; height: 160px;" />
                    </div>
                    <h3 style="margin: 4px 0 1px 0; color: #FFFFFF; font-size: 1.2rem; font-weight: 800;">{t_name}</h3>
                    <div style="font-size: 0.82rem; color: #94A3B8;">{t_org}</div>
                    <div style="margin-top: 12px; padding: 8px 12px; background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; border-radius: 8px; font-size: 0.78rem; color: #34D399; font-weight: 800;">
                        ✓ M-PESA CONFIRMED • KES {t_amt:,.0f} • REF: {t_tx}
                    </div>
                    <div style="margin-top: 6px; font-size: 0.7rem; color: #64748B;">
                        Ticket Serial: <code>{t_id}</code> • Status: <strong>{cur_ticket.get('gate_status', 'REGISTERED')}</strong>
                    </div>
                </div>
                """), unsafe_allow_html=True)

                c_p1, c_p2 = st.columns(2)
                with c_p1:
                    st.download_button(
                        label="📥 Download Pass (.txt)",
                        data=f"STRIDE DIGITAL PASS\nEvent: {cur_evt['title']}\nAttendee: {t_name}\nOrg: {t_org}\nTier: {t_tier}\nTicket ID: {t_id}\nReceipt: {t_tx}\nAmount: KES {t_amt:,}\nScan URL: {verify_qr_data}".encode('utf-8'),
                        file_name=f"STRIDE_Ticket_{t_id}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with c_p2:
                    if st.button("🔄 Register Another Person", use_container_width=True):
                        st.session_state["pub_active_ticket"] = None
                        st.rerun()

        # Accredited Member Roster Feed (Un-categorized for SACCO)
        sacco_tickets = backend.get_tickets_by_event(selected_event['event_id'])
        if sacco_tickets:
            st.markdown("---")
            st.markdown(f"### 📜 Live Accredited Member Roster & SASRA Quorum Feed ({len(sacco_tickets)} Members Recorded)")
            st.caption("Live statutory shareholder accreditation feed. Shows all confirmed Banki Kuu SACCO members, proxy holders, board directors, and independent auditors:")

            df_display = pd.DataFrame(sacco_tickets)
            
            show_cols = ["ticket_id", "attendee_name", "organization", "ticket_tier", "email", "phone", "gate_status", "mpesa_trans_id"]
            avail_cols = [c for c in show_cols if c in df_display.columns]
            df_show = df_display[avail_cols].copy()
            
            rename_map = {
                "ticket_id": "Ticket Serial ID",
                "attendee_name": "Delegate Full Name",
                "organization": "Department / SACCO Branch Ref",
                "ticket_tier": "Accreditation Role",
                "email": "Email Address",
                "phone": "Phone Number",
                "gate_status": "Check-in Status",
                "mpesa_trans_id": "M-Pesa Receipt Ref"
            }
            df_show.rename(columns=rename_map, inplace=True)

            search_query = st.text_input("🔍 Search Live Roster (by Name, Account Ref, or Role):", placeholder="e.g. Samuel Gathigi / SACCO-3428 / Board Director", key=f"srch_roster_{selected_event['event_id']}")
            if search_query.strip():
                q = search_query.strip().lower()
                df_show = df_show[
                    df_show.apply(lambda r: any(q in str(v).lower() for v in r.values), axis=1)
                ]

            st.dataframe(df_show, use_container_width=True, height=380)

            total_members = len(sacco_tickets)
            quorum_needed = 50  # SASRA Statutory Quorum Floor
            quorum_pct = min(100.0, (total_members / quorum_needed) * 100)
            status_badge = "✅ STATUTORY AGM QUORUM ACHIEVED" if total_members >= quorum_needed else "⚠️ PENDING QUORUM ACCREDITATION"
            
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.12); border: 1.5px solid #10B981; border-radius: 10px; padding: 14px 18px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <span style="color: #34D399; font-weight: 800; font-size: 0.9rem;">{status_badge}</span>
                    <div style="font-size: 0.8rem; color: #CBD5E1; margin-top: 2px;">
                        Total Accredited Delegates: <strong>{total_members}</strong> • SASRA Statutory Quorum Floor: <strong>{quorum_needed} Members</strong> ({quorum_pct:.1f}% Reached)
                    </div>
                </div>
                <div>
                    <span style="background: #10B981; color: #020712; font-weight: 900; padding: 6px 14px; border-radius: 6px; font-size: 0.85rem;">
                        {total_members} / {quorum_needed} DELEGATES RECORDED
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# TAB 2: EVENT CREATOR WIZARD (FOR ORGANIZERS & CORPORATES)
# ==============================================================================
CLUSTER_CONFIGS = {
    "👔 Corporate AGM & Shareholder Assembly": {
        "title": "58th Annual General Meeting & Shareholder Elections",
        "host": "Apex Capital Holdings PLC Board & Secretariat",
        "venue": "Kenyatta International Convention Centre (KICC) / Grand Ballroom, Nairobi",
        "gate_mode": "SINGLE_GATE",
        "time": "09:00",
        "std_price": 0.0,
        "vip_price": 0.0,
        "is_paid": False,
        "desc": "Notice is hereby given that the Annual General Meeting will convene to: 1. Table the audited financial statements for FY2025. 2. Elect executive committee members. 3. Appoint external statutory auditors. 4. Transact any other ordinary business.",
        "scale_opts": [
            "🐥 Tier 1: Small Society / Club AGM (Up to 100 Delegates) — KES 15,000",
            "🏢 Tier 2: Mid-Sized Corporate / SACCO (101 – 500 Delegates) — KES 35,000",
            "🏛️ Tier 3: Large Listed PLC / Tier-1 SACCO (501 – 2,500 Delegates) — KES 75,000",
            "🌐 Tier 4: Mega National Assembly (2,500+ Delegates) — KES 150,000"
        ],
        "scale_fees": {"Tier 1": 15000.0, "Tier 2": 35000.0, "Tier 3": 75000.0, "Tier 4": 150000.0},
        "q2_label": "Q2: Voting Resolution & Committee Election Engine (Pull-Down):*",
        "q2_opts": [
            "✋ Voice Vote & Statutory Quorum Floor Tracking — Included (KES 0)",
            "⚖️ Weighted Voting Engine (Shares / Capital Bracket Weighting) — +KES 15,000",
            "🗳️ Digital Secret Ballot & Committee Elections with Real-Time Tally Screen — +KES 25,000",
            "📱 SMS OTP Multi-Factor Verification for Proxies & Remote Voting — +KES 20,000"
        ],
        "q3_label": "Q3: Gate Usher Hardware & Access Station Mode (Pull-Down):*",
        "q3_opts": [
            "📲 Mobile BYOD Usher Mode (Ushers scan using any smartphone/tablet - Included) — KES 0",
            "📟 STRIDE™ Rugged Barcode Gate Station Terminals (Pair Rental) — +KES 20,000",
            "🖨️ Rapid Thermal Badge & Lanyard Printing Station — +KES 30,000"
        ],
        "q4_label": "Q4: Statutory Compliance & Scrutineer Auditing (Pull-Down):*",
        "q4_opts": [
            "📄 Standard CSV Scrutineer & Company Secretary Export — Included (KES 0)",
            "🔒 Certified Tamper-Evident SHA-256 Audit Pack (CMA / SASRA Regulatory Dossier) — +KES 15,000",
            "👨‍💼 Dedicated On-Site STRIDE™ Certified Technical Marshal (1 Day Deployment) — +KES 25,000"
        ]
    },
    "🏆 Sports Tournament & Derby": {
        "title": "Annual Corporate Inter-Bank Sports Championship & Derby",
        "host": "Kenya Bankers Association Sports Secretariat",
        "venue": "Sports Complex Main Arena & Training Grounds, Nairobi",
        "gate_mode": "DUAL_GATE",
        "time": "08:00",
        "std_price": 500.0,
        "vip_price": 2500.0,
        "is_paid": True,
        "desc": "Official corporate sporting championship across 18 disciplines. Dual-gate check-in required for training allowance validation. Athlete kit mandatory upon arrival.",
        "scale_opts": [
            "🏅 Tier 1: Departmental / Club Derby (Up to 150 Participants) — KES 15,000",
            "🏆 Tier 2: Corporate Championship (151 – 750 Participants) — KES 45,000",
            "🏃 Tier 3: Regional Multi-Sport Derby (751 – 2,500 Participants) — KES 95,000",
            "🌍 Tier 4: National Inter-Industry Games (2,500+ Participants) — KES 180,000"
        ],
        "scale_fees": {"Tier 1": 15000.0, "Tier 2": 45000.0, "Tier 3": 95000.0, "Tier 4": 180000.0},
        "q2_label": "Q2: Player Telemetry & Allowance Rules Engine (Pull-Down):*",
        "q2_opts": [
            "⏱️ Standard Check-In Attendance Tracking — Included (KES 0)",
            "⏱️ Dual-Gate Duration Enforcement (Pre-sport + Post-sport allowance floor) — +KES 15,000",
            "📊 Live Public Scoreboard & Discipline Leaderboards — +KES 20,000",
            "🏅 Automated Allowance Payment Batch CSV Export — +KES 15,000"
        ],
        "q3_label": "Q3: Gate Marshalling & Hardware Stations (Pull-Down):*",
        "q3_opts": [
            "📲 Mobile BYOD Gate Marshalling (Included) — KES 0",
            "📟 Handheld Referee & Field Marshal QR Scanners — +KES 20,000",
            "👨‍💼 Dedicated STRIDE™ Pitch-Side Timekeeper & Tech Marshal — +KES 25,000"
        ],
        "q4_label": "Q4: Integrity & Disciplinary Auditing (Pull-Down):*",
        "q4_opts": [
            "📄 Standard Match Roster & Attendance CSV — Included (KES 0)",
            "🛡️ Anti-Mercenary Player Verification & HR Employee Audit Dossier — +KES 15,000",
            "⚖️ Complete Tournament Disciplinary & Allowance Audit Pack — +KES 25,000"
        ]
    },
    "🏃 Marathon, Fun Run & Athletics": {
        "title": "Nairobi Corporate 21km Half Marathon & 10km Charity Fun Run",
        "host": "Athletics Kenya & Corporate Health Initiative",
        "venue": "Nyayo National Stadium & Expressway Circuit, Nairobi",
        "gate_mode": "DUAL_GATE",
        "time": "06:30",
        "std_price": 1500.0,
        "vip_price": 5000.0,
        "is_paid": True,
        "desc": "Official 21km Half Marathon, 10km Corporate Challenge, and 5km Family Fun Run. Start chute scan and finish line timing gate. Refreshments and medical aid along the route.",
        "scale_opts": [
            "🏃 Tier 1: Club / Community Fun Run (Up to 300 Runners) — KES 20,000",
            "👟 Tier 2: Mid Corporate Marathon (301 – 1,500 Runners) — KES 55,000",
            "🏅 Tier 3: Major City Marathon (1,501 – 5,000 Runners) — KES 110,000",
            "🌍 Tier 4: International Mega Marathon (5,000+ Runners) — KES 210,000"
        ],
        "scale_fees": {"Tier 1": 20000.0, "Tier 2": 55000.0, "Tier 3": 110000.0, "Tier 4": 210000.0},
        "q2_label": "Q2: Timing Protocol & Route Telemetry (Pull-Down):*",
        "q2_opts": [
            "⏱️ Start Chute & Finish Line Gun Time Scan — Included (KES 0)",
            "📍 Checkpoint Hydration Mats & Intermediate Split Pace Tracking — +KES 25,000",
            "📊 Live Public Split Pace Leaderboard & Category Podium — +KES 20,000",
            "🏅 Instant Digital Finisher E-Certificate & SMS Time Dispatch — +KES 20,000"
        ],
        "q3_label": "Q3: Athlete Bib & Hardware Terminals (Pull-Down):*",
        "q3_opts": [
            "📲 Mobile BYOD Chute Marshalling (Included) — KES 0",
            "🖨️ Rapid Thermal Athlete Bib & Waterproof QR Badge Station — +KES 30,000",
            "📟 High-Throughput Ultra-Fast Gun Finish Scanners — +KES 25,000"
        ],
        "q4_label": "Q4: Timing Certification & Results Dossier (Pull-Down):*",
        "q4_opts": [
            "📄 Standard Runner Time Export CSV — Included (KES 0)",
            "🏆 Official Athletics Kenya Certified Results Ledger & Category Rank Dossier — +KES 20,000",
            "👨‍💼 Dedicated Chief Timekeeper & Emergency Marshal Deployment — +KES 30,000"
        ]
    },
    "💡 Industry Conference & Tech Summit": {
        "title": "East Africa Banking, FinTech & Cyber Security Summit 2026",
        "host": "FinTech Association & East Africa Financial Forum",
        "venue": "Radisson Blu Hotel / KICC Tsavo Ballroom, Nairobi",
        "gate_mode": "SINGLE_GATE",
        "time": "08:30",
        "std_price": 7500.0,
        "vip_price": 25000.0,
        "is_paid": True,
        "desc": "Premier financial industry summit featuring 4 plenary sessions, 6 technical tracks, and corporate exhibition. CPD accredited by statutory professional boards.",
        "scale_opts": [
            "🐥 Tier 1: Executive Roundtable / Workshop (Up to 150 Delegates) — KES 25,000",
            "🏢 Tier 2: Mid Industry Summit (151 – 600 Delegates) — KES 60,000",
            "🏛️ Tier 3: Regional Conference & Expo (601 – 2,000 Delegates) — KES 120,000",
            "🌐 Tier 4: International Mega Convention (2,000+ Delegates) — KES 220,000"
        ],
        "scale_fees": {"Tier 1": 25000.0, "Tier 2": 60000.0, "Tier 3": 120000.0, "Tier 4": 220000.0},
        "q2_label": "Q2: Breakout Tracking & Professional CPD Engine (Pull-Down):*",
        "q2_opts": [
            "🎟️ Plenary Hall Access Clearance — Included (KES 0)",
            "🎯 Multi-Room Breakout Hall Tracking & Sub-Session Analytics — +KES 20,000",
            "🎓 Continuous Professional Development (CPD) Clock-Hour Audit Engine — +KES 25,000",
            "💼 Exhibitor Lead-Retrieval QR Badge Scanner Integration — +KES 30,000"
        ],
        "q3_label": "Q3: Badge Printing & Registration Kiosks (Pull-Down):*",
        "q3_opts": [
            "📲 Mobile BYOD Delegate Scanner — Included (KES 0)",
            "🖨️ Rapid Full-Color Lanyard Nametag & RFID Printing Station — +KES 35,000",
            "📟 Executive Self-Service QR Kiosk Terminals — +KES 40,000"
        ],
        "q4_label": "Q4: Delegate Analytics & CPD Certification (Pull-Down):*",
        "q4_opts": [
            "📄 Standard Delegate Attendance CSV — Included (KES 0)",
            "📜 Automated CPD Certificate Generation & Email Dispatch Pack — +KES 20,000",
            "📊 Executive Post-Event ROI & Session Popularity Dossier — +KES 25,000"
        ]
    },
    "🎉 Corporate Gala Dinner & Awards": {
        "title": "Annual Corporate Excellence Gala Dinner & CEO Awards Night",
        "host": "Executive Welfare Board & Awards Committee",
        "venue": "Villa Rosa Kempinski / Safari Park Grand Ballroom, Nairobi",
        "gate_mode": "SINGLE_GATE",
        "time": "18:30",
        "std_price": 5000.0,
        "vip_price": 15000.0,
        "is_paid": True,
        "desc": "Black-tie annual awards dinner celebrating leadership excellence and top milestones. 5-course banquet, live orchestra, and executive award presentations.",
        "scale_opts": [
            "🥂 Tier 1: Intimate Banquet (Up to 100 Guests / 10 Tables) — KES 20,000",
            "🍾 Tier 2: Mid Corporate Gala (101 – 350 Guests / 35 Tables) — KES 50,000",
            "👑 Tier 3: Grand Ballroom Gala (351 – 1,000 Guests / 100 Tables) — KES 95,000",
            "🌟 Tier 4: Mega Presidential Dinner (1,000+ Guests) — KES 180,000"
        ],
        "scale_fees": {"Tier 1": 20000.0, "Tier 2": 50000.0, "Tier 3": 95000.0, "Tier 4": 180000.0},
        "q2_label": "Q2: Seating Concierge & Live Audience Voting (Pull-Down):*",
        "q2_opts": [
            "🥂 Standard Guestlist Red Carpet Admission — Included (KES 0)",
            "🪑 Dynamic Table Seating Allocation & VIP Protocol Concierge — +KES 20,000",
            "🏆 Live Audience SMS / Smartphone Award Voting & Big-Screen Tally — +KES 25,000",
            "📸 Digital Red Carpet Guestbook & Photo Memory Wall — +KES 15,000"
        ],
        "q3_label": "Q3: Red Carpet Ushering & Hostess Hardware (Pull-Down):*",
        "q3_opts": [
            "📲 Hostess BYOD Smartphone Scanner — Included (KES 0)",
            "📟 Illuminated Red Carpet Welcome Screen & Guest Greeting Terminal — +KES 25,000",
            "👩‍💼 Dedicated STRIDE™ Protocol Marshal & Red Carpet Tech Host — +KES 25,000"
        ],
        "q4_label": "Q4: Seating Audit & Dignitary Reconciliation (Pull-Down):*",
        "q4_opts": [
            "📄 Standard Seating & Attendance CSV — Included (KES 0)",
            "🔒 VIP Dignitary Security Clearance & Catering Headcount Audit — +KES 15,000",
            "🎁 Complete Award Voting Audit Certificate & Gala Keepsake Report — +KES 20,000"
        ]
    },
    "🎓 School / University Sports Day": {
        "title": "Inter-Collegiate Track & Field Championship 2026",
        "host": "Sports Department & Student Affairs Committee",
        "venue": "Kasarani Stadium Upper Arena, Nairobi",
        "gate_mode": "DUAL_GATE",
        "time": "08:00",
        "std_price": 200.0,
        "vip_price": 1000.0,
        "is_paid": False,
        "desc": "Annual inter-house sports festival featuring sprint heats, field events, and house marching band. Dual gate attendance check-in for house points and student safety.",
        "scale_opts": [
            "🏅 Tier 1: Academy Sports Day (Up to 250 Students) — KES 10,000",
            "🏆 Tier 2: Secondary / College Games (251 – 1,000 Students) — KES 30,000",
            "🏃 Tier 3: University Sports Festival (1,001 – 3,000 Students) — KES 65,000",
            "🌍 Tier 4: National Inter-University Games (3,000+ Students) — KES 120,000"
        ],
        "scale_fees": {"Tier 1": 10000.0, "Tier 2": 30000.0, "Tier 3": 65000.0, "Tier 4": 120000.0},
        "q2_label": "Q2: House Roster & Event Scoring Engine (Pull-Down):*",
        "q2_opts": [
            "⏱️ Basic Student Attendance Check-In — Included (KES 0)",
            "🏠 Inter-House Points Tally & Real-Time Big-Screen Trophy Standings — +KES 15,000",
            "📋 Age-Grade Eligibility & House Squad Roster Enforcement — +KES 15,000",
            "🏅 Digital Student Participation Certificate Generator — +KES 15,000"
        ],
        "q3_label": "Q3: Teacher Marshalling & Field Wristbands (Pull-Down):*",
        "q3_opts": [
            "📲 Teacher / Prefect BYOD Scanner — Included (KES 0)",
            "🏷️ Color-Coded House Wristband & Athlete Number Station — +KES 15,000",
            "📟 Multi-Pitch Field Master Scanners (Pair Rental) — +KES 20,000"
        ],
        "q4_label": "Q4: Student Safety & House Championship Audit (Pull-Down):*",
        "q4_opts": [
            "📄 Standard House Roster & Results CSV — Included (KES 0)",
            "🛡️ Student Safety Roll-Call & Departure Reconciliation Pack — +KES 10,000",
            "🏆 Official Sports Day Championship Trophy & Record-Holder Ledger — +KES 15,000"
        ]
    },
    "💒 Private Reception / Social Gala": {
        "title": "Exclusive Evening Reception & Celebration",
        "host": "Host Secretariat & Family Committee",
        "venue": "Windsor Golf & Country Club / Zen Garden, Nairobi",
        "gate_mode": "SINGLE_GATE",
        "time": "14:00",
        "std_price": 0.0,
        "vip_price": 0.0,
        "is_paid": False,
        "desc": "Private guest-list celebration. Entry strictly by personalized QR invitation pass. Complimentary valet parking and welcome cocktails upon gate clearance.",
        "scale_opts": [
            "🥂 Tier 1: Intimate Reception (Up to 80 Invited Guests) — KES 12,000",
            "🍾 Tier 2: Classic Celebration (81 – 250 Guests) — KES 28,000",
            "👑 Tier 3: Grand Reception (251 – 600 Guests) — KES 55,000",
            "🌟 Tier 4: High-Society Gala (600+ Guests) — KES 95,000"
        ],
        "scale_fees": {"Tier 1": 12000.0, "Tier 2": 28000.0, "Tier 3": 55000.0, "Tier 4": 95000.0},
        "q2_label": "Q2: RSVP Security & Guest Registry Engine (Pull-Down):*",
        "q2_opts": [
            "🎟️ Strict 1-Pass-Per-Guest QR Security Clearance — Included (KES 0)",
            "🪑 Reserved Family / Table Allocation Concierge — +KES 15,000",
            "🎁 Digital Gift Registry & Automated Thank-You SMS Dispatch — +KES 15,000",
            "📸 Interactive Guest Memory Wall & Live Photo Upload Screen — +KES 20,000"
        ],
        "q3_label": "Q3: Gate Concierge & Host Hardware (Pull-Down):*",
        "q3_opts": [
            "📲 Host BYOD Mobile Scanner — Included (KES 0)",
            "📟 Personalized Guest Greeting Tablet Station — +KES 15,000",
            "👩‍💼 Dedicated STRIDE™ Concierge Gate Usher (1 Day Deployment) — +KES 20,000"
        ],
        "q4_label": "Q4: Guest Attendance & Keepsake Dossier (Pull-Down):*",
        "q4_opts": [
            "📄 Complete Guest Attendance List CSV — Included (KES 0)",
            "📖 Digital Memory Book & Keepsake Guest Signatures PDF — +KES 10,000",
            "🔒 VIP Gate Security & Parking Headcount Report — +KES 15,000"
        ]
    }
}

def clean_html_card(raw_html: str) -> str:
    """Strips leading/trailing indentation from each line and removes blank lines to prevent CommonMark from treating HTML as code blocks."""
    lines = [line.strip() for line in raw_html.strip().splitlines() if line.strip()]
    return "".join(lines)

if tab_wizard is not None:
    with tab_wizard:
        if is_bks_mode:
            st.markdown("### 💳 Banki Kuu SACCO Finance Manager Payment & Scoping")
            st.caption("Central platform fee settlement portal for the Banki Kuu Staff SACCO Finance Manager & Secretariat. Settle platform deployment fee via M-Pesa STK Push and generate official tax invoice:")
        else:
            st.markdown("### 🪄 Universal Event & AGM Commercial Scoping Wizard")
            st.caption("Answer 4 quick scoping questions to determine your platform deployment scope, calculate your customized fee, and provision certified gate scanners instantly via M-Pesa:")

        wz_col1, wz_col2 = st.columns([1.35, 1])

        with wz_col1:
            # Category Selector outside form for reactive pricing
            cluster_list = list(CLUSTER_CONFIGS.keys())
            wz_cat = st.selectbox(
                "Select Event Type / Assembly Category (Pull-Down):*",
                cluster_list,
                key="wz_event_category_selector"
            )
            cfg = CLUSTER_CONFIGS.get(wz_cat, CLUSTER_CONFIGS["👔 Corporate AGM & Shareholder Assembly"])
            is_wz_agm = ("AGM" in wz_cat or "Shareholder" in wz_cat)

            # Reactive defaults synchronization when category switches
            if "wz_active_cat_tracker" not in st.session_state or st.session_state.get("wz_active_cat_tracker") != wz_cat:
                st.session_state["wz_active_cat_tracker"] = wz_cat
                st.session_state["wz_e_title"] = cfg["title"]
                st.session_state["wz_e_host"] = cfg["host"]
                st.session_state["wz_e_venue"] = cfg["venue"]
                st.session_state["wz_e_time"] = cfg["time"]
                st.session_state["wz_e_desc"] = cfg["desc"]
                st.session_state["wz_paid_chk"] = cfg["is_paid"]
                st.session_state["wz_std_price"] = float(cfg["std_price"])
                st.session_state["wz_vip_price"] = float(cfg["vip_price"])

            st.markdown("#### 1️⃣ Assembly Identity & Schedule")
            e_title = st.text_input("Official Event / Assembly Name:*", key="wz_e_title")
            e_host = st.text_input("Society / Convening Corporate Body:*", key="wz_e_host")

            if is_wz_agm:
                c_agm_sub1, c_agm_sub2 = st.columns(2)
                with c_agm_sub1:
                    e_agm_subtype = st.selectbox(
                        "Meeting Statutory Sub-Type (Pull-down):*",
                        [
                            "Annual General Meeting (Ordinary Business - Financial Statements & Elections)",
                            "Extraordinary General Meeting (EGM - Special Resolutions & Bylaw Amendments)",
                            "SACCO Annual Delegates Conference (ADC)",
                            "Corporate Sports Club Annual General Meeting"
                        ],
                        key="wz_agm_subtype"
                    )
                with c_agm_sub2:
                    e_quorum_threshold = st.selectbox(
                        "Statutory Quorum Floor Rule (Pull-down):*",
                        [
                            "25 Members in Good Standing (Bylaws Standard Floor)",
                            "50 Members or 15% Voting Capital",
                            "100 Accredited Shareholders or Delegated Proxies",
                            "150 Delegates (Tier-1 Sacco / Cooperative Quorum Floor)"
                        ],
                        key="wz_quorum_rule"
                    )

                c_agm_prx1, c_agm_prx2 = st.columns(2)
                with c_agm_prx1:
                    e_proxy_cutoff = st.selectbox(
                        "Proxy Form Deposit Cut-Off (Pull-down):*",
                        [
                            "48 Hours prior to meeting commencement (Statutory Standard)",
                            "24 Hours prior to meeting commencement",
                            "Deposited at Secretariat registration desk on arrival"
                        ],
                        key="wz_proxy_cutoff"
                    )
                with c_agm_prx2:
                    e_admit_mode = st.selectbox(
                        "Delegate Admission Model (Pull-down):*",
                        [
                            "Complimentary Free Admission (Accredited Shareholders & Proxies)",
                            "Paid Annual Subscription / Clearance Fee (KES via M-Pesa STK)"
                        ],
                        key="wz_admit_mode"
                    )

            ec1, ec2 = st.columns(2)
            with ec1:
                e_date = st.date_input("Event Date:", value=now_dt.date() + datetime.timedelta(days=14), key="wz_e_date")
            with ec2:
                e_time = st.text_input("Start / Call-to-Order Time:", key="wz_e_time")

            e_venue = st.text_input("Venue & Physical Address:*", key="wz_e_venue")

            if not is_wz_agm:
                tc1, tc2, tc3 = st.columns(3)
                with tc1:
                    e_paid = st.checkbox("Paid Event (Collect via M-Pesa)", key="wz_paid_chk")
                with tc2:
                    e_std_price = st.number_input("Standard Ticket (KES):", min_value=0.0, step=100.0, key="wz_std_price")
                with tc3:
                    e_vip_price = st.number_input("VIP / Delegate (KES):", min_value=0.0, step=500.0, key="wz_vip_price")

                e_paybill = st.text_input("M-Pesa Paybill / Till Number for Settlements:", value="849200", key="wz_paybill")
                default_gate_idx = 0 if cfg["gate_mode"] == "DUAL_GATE" else 1
                e_gate_mode = st.selectbox(
                    "Gate Scanning Protocol:*",
                    [
                        "DUAL_GATE (Arrival Scan + Departure Scan for Allowance Floor Verification)",
                        "SINGLE_GATE (Entry Scan Only for Galas, AGMs & Conferences)"
                    ],
                    index=default_gate_idx,
                    key=f"wz_gate_mode_{wz_cat[:6]}"
                )
                clean_gate_mode = "DUAL_GATE" if "DUAL_GATE" in e_gate_mode else "SINGLE_GATE"
            else:
                if "Paid" in e_admit_mode:
                    tc1, tc2 = st.columns(2)
                    with tc1:
                        e_std_price = st.number_input("Shareholder Clearance Fee (KES):", min_value=0.0, value=5000.0, step=500.0, key="wz_std_price_agm")
                    with tc2:
                        e_vip_price = st.number_input("VIP / Board Delegate (KES):", min_value=0.0, value=5000.0, step=500.0, key="wz_vip_price_agm")
                    e_paid = True
                    e_paybill = st.text_input("M-Pesa Paybill / Till Number for Settlements:", value="849200", key="wz_paybill")
                else:
                    e_std_price = 0.0
                    e_vip_price = 0.0
                    e_paid = False
                    e_paybill = "N/A (COMPLIMENTARY)"
                clean_gate_mode = "SINGLE_GATE"

            e_desc = st.text_area("Event Description / Statutory Notice & Instructions:*", key="wz_e_desc")

            st.markdown("---")
            st.markdown("#### 2️⃣ Commercial Scope Questionnaire (Pricing Engine)")
            st.caption(f"Configuring specialized telemetry and compliance architecture for **{wz_cat}**:")

            # Q1: Scale Selection
            sc_scale = st.selectbox(
                f"Q1: Expected Attendance Scale ({wz_cat.split(' ')[1]} Tier):*",
                cfg["scale_opts"],
                key=f"sc_scale_{wz_cat[:6]}"
            )
            base_fee = 15000.0
            for tier_k, tier_amt in cfg["scale_fees"].items():
                if tier_k in sc_scale:
                    base_fee = tier_amt
                    break
            scale_tag = sc_scale.split("—")[0].strip()

            # Helper to extract +KES amount
            def extract_module_fee(opt_str: str) -> float:
                if "+KES" in opt_str:
                    try:
                        raw_val = opt_str.split("+KES")[-1].split(")")[0].strip().replace(",", "")
                        return float(raw_val)
                    except Exception:
                        return 0.0
                return 0.0

            # Q2: Specialized Module
            sc_q2 = st.selectbox(
                cfg["q2_label"],
                cfg["q2_opts"],
                key=f"sc_q2_{wz_cat[:6]}"
            )
            voting_fee = extract_module_fee(sc_q2)
            voting_tag = sc_q2.split("—")[0].strip()

            # Q3: Hardware & Marshals
            sc_q3 = st.selectbox(
                cfg["q3_label"],
                cfg["q3_opts"],
                key=f"sc_q3_{wz_cat[:6]}"
            )
            hw_fee = extract_module_fee(sc_q3)
            hw_tag = sc_q3.split("—")[0].strip()

            # Q4: Auditing & Compliance
            sc_q4 = st.selectbox(
                cfg["q4_label"],
                cfg["q4_opts"],
                key=f"sc_q4_{wz_cat[:6]}"
            )
            audit_fee = extract_module_fee(sc_q4)
            audit_tag = sc_q4.split("—")[0].strip()

            if is_bks_mode:
                base_fee = 10000.0
                voting_fee = 0.0
                hw_fee = 0.0
                audit_fee = 0.0
                subtotal = 10000.0
                vat_amt = 0.0
                grand_total = 10000.0
            else:
                subtotal = base_fee + voting_fee + hw_fee + audit_fee
                vat_amt = subtotal * 0.16
                grand_total = subtotal + vat_amt

            st.markdown("---")
            if is_bks_mode:
                st.markdown("#### 3️⃣ Banki Kuu SACCO Finance Manager M-Pesa STK Settlement")
                def_b_org = "Banki Kuu Staff SACCO Society Ltd."
                def_b_email = "finance@bankikuusacco.co.ke"
                def_b_phone = "0722849000"
            else:
                st.markdown("#### 3️⃣ Organizer Billing & Instant M-Pesa Settlement")
                def_b_org = e_host if e_host else "Corporate Client"
                def_b_email = ""
                def_b_phone = "0722123456"

            b_org = st.text_input("Billing Entity / Organization Name:*", value=def_b_org, key="wz_b_org")
            b_email = st.text_input("Billing Email Address (for Official Tax Invoice):*", value=def_b_email, placeholder="finance@bankikuusacco.co.ke", key="wz_b_email")
            b_phone = st.text_input("Safaricom M-Pesa Mobile Number for STK Push (Finance Manager Handset):*", value=def_b_phone, help="STK Push prompt will be dispatched to Finance Manager handset", key="wz_b_phone")

            btn_pay_provision = st.button(
                f"💳 Settle KES {grand_total:,.0f} via M-Pesa STK & Provision Platform",
                type="primary",
                use_container_width=True,
                key="btn_wz_pay_provision"
            )

            if btn_pay_provision:
                if not e_title.strip():
                    st.error("Please provide an Event / Assembly Name.")
                elif not e_host.strip():
                    st.error("Please provide the Convening Entity Name.")
                elif not e_venue.strip():
                    st.error("Please specify the Venue / Assembly Hall.")
                elif not b_email.strip() or "@" not in b_email:
                    st.error("Please provide a valid Billing Email Address.")
                elif not b_phone.strip() or len(b_phone.strip()) < 9:
                    st.error("Please provide a valid Safaricom phone number.")
                else:
                    d_str = e_date.strftime("%Y-%m-%d")
                    inv_ref = f"INV-2026-{int(time.time())}"[-8:]
                    mpesa_ref = f"QK{int(time.time())}"[-10:]
                
                    scoping_meta = f"{e_desc.strip()} [STRIDE Scope: Category={wz_cat}, Tier={scale_tag}, Module={voting_tag}, HW={hw_tag}, Fee=KES {grand_total:,.0f}, Inv={inv_ref}, M-Pesa={mpesa_ref}]"
                
                    if is_bks_mode:
                        new_eid = "EVT-BANKI-KUU-SACCO"
                        ok_ev = True
                        msg_ev = "Payment settled for Banki Kuu SACCO 58th AGM!"
                    else:
                        ok_ev, msg_ev, new_eid = backend.create_event(
                            title=e_title.strip(),
                            organizer_name=e_host.strip(),
                            category=wz_cat,
                            event_date=d_str,
                            event_time=e_time.strip(),
                            venue=e_venue.strip(),
                            description=scoping_meta,
                            gate_mode=clean_gate_mode,
                            is_paid=e_paid,
                            standard_price=e_std_price,
                            vip_price=e_vip_price,
                            mpesa_paybill=e_paybill.strip()
                        )
                    if ok_ev:
                        invoice_record = {
                            "inv_ref": inv_ref,
                            "event_id": new_eid,
                            "title": e_title.strip(),
                            "org": b_org.strip() or e_host.strip(),
                            "email": b_email.strip(),
                            "phone": b_phone.strip(),
                            "mpesa_ref": mpesa_ref,
                            "timestamp": now_dt.strftime("%Y-%m-%d %H:%M:%S"),
                            "base_fee": base_fee,
                            "scale_tag": scale_tag,
                            "voting_fee": voting_fee,
                            "voting_tag": voting_tag,
                            "hw_fee": hw_fee,
                            "hw_tag": hw_tag,
                            "audit_fee": audit_fee,
                            "audit_tag": audit_tag,
                            "subtotal": subtotal,
                            "vat_amt": vat_amt,
                            "grand_total": grand_total
                        }
                        st.session_state["wz_last_invoice"] = invoice_record
                        st.session_state["wz_last_created_id"] = new_eid
                        st.session_state["wz_last_created_title"] = e_title.strip()
                        st.success(f"🎉 M-Pesa Payment Confirmed! Invoice `{inv_ref}` generated. Event `{new_eid}` provisioned.")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(msg_ev)

        with wz_col2:
            # Check if an invoice was recently generated
            cur_inv = st.session_state.get("wz_last_invoice", None)
        
            # Display Live Scope Quotation Card with zero leading markdown indentation
            quote_card_html = f"""
    <div style="background: linear-gradient(135deg, rgba(8, 28, 58, 0.95) 0%, rgba(4, 14, 30, 0.98) 100%); border: 2px solid #F5C542; border-radius: 14px; padding: 18px 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(245, 197, 66, 0.25); padding-bottom: 8px;">
            <span style="color: #F5C542; font-weight: 900; font-size: 0.82rem; letter-spacing: 1.2px; text-transform: uppercase;">
                STRIDE™ SCOPE QUOTATION
            </span>
            <span style="background: rgba(245, 197, 66, 0.18); border: 1px solid #F5C542; color: #F5C542; font-size: 0.72rem; padding: 2px 8px; border-radius: 4px; font-weight: 800;">
                {"🎉 INTRODUCTORY SACCO OFFER (KES 10,000 FLAT)" if is_bks_mode else "LIVE PRO-FORMA"}
            </span>
        </div>
    
        <div style="margin: 12px 0 6px 0; font-size: 0.8rem; color: #CBD5E1;">
            <div style="font-size: 0.76rem; color: #00F2FE; font-weight: 700; margin-bottom: 8px;">
                Cluster: {wz_cat}
            </div>
            <table style="width: 100%; border-collapse: collapse; line-height: 1.8;">
                <tr>
                    <td style="color: #94A3B8;">Base Scale License:</td>
                    <td style="text-align: right; font-weight: 700; color: #FFFFFF;">KES {base_fee:,.0f}</td>
                </tr>
                <tr>
                    <td style="color: #94A3B8;">Specialized Module:</td>
                    <td style="text-align: right; font-weight: 700; color: #FFFFFF;">KES {voting_fee:,.0f}</td>
                </tr>
                <tr>
                    <td style="color: #94A3B8;">Gate Hardware & Scanners:</td>
                    <td style="text-align: right; font-weight: 700; color: #FFFFFF;">KES {hw_fee:,.0f}</td>
                </tr>
                <tr>
                    <td style="color: #94A3B8;">Auditing & Compliance:</td>
                    <td style="text-align: right; font-weight: 700; color: #FFFFFF;">KES {audit_fee:,.0f}</td>
                </tr>
                <tr style="border-top: 1px dashed rgba(255,255,255,0.15);">
                    <td style="color: #CBD5E1; font-weight: 700; padding-top: 4px;">Net Platform Subtotal:</td>
                    <td style="text-align: right; font-weight: 800; color: #00F2FE; padding-top: 4px;">KES {subtotal:,.0f}</td>
                </tr>
                <tr>
                    <td style="color: #94A3B8;">VAT (16% Statutory):</td>
                    <td style="text-align: right; font-weight: 700; color: #FFFFFF;">KES {vat_amt:,.0f}</td>
                </tr>
                <tr style="border-top: 1.5px solid #F5C542; font-size: 0.95rem;">
                    <td style="color: #F5C542; font-weight: 900; padding-top: 6px;">TOTAL SETUP FEE:</td>
                    <td style="text-align: right; font-weight: 900; color: #F5C542; padding-top: 6px;">KES {grand_total:,.0f}</td>
                </tr>
            </table>
        </div>
    
        <div style="font-size: 0.72rem; color: #64748B; margin-top: 6px; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 6px;">
            Includes unlimited attendee QR passes, dynamic check-in gate dashboard, and real-time reconciliation.
        </div>
    </div>
    """
            st.markdown(clean_html_card(quote_card_html), unsafe_allow_html=True)

            if cur_inv:
                inv_card_html = f"""
    <div style="background: rgba(16, 185, 129, 0.12); border: 2px solid #10B981; border-radius: 12px; padding: 14px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="color: #34D399; font-weight: 900; font-size: 0.85rem;">✓ TAX INVOICE: {cur_inv['inv_ref']}</span>
            <span style="background: #10B981; color: #020712; padding: 2px 6px; border-radius: 4px; font-weight: 900; font-size: 0.68rem;">PAID</span>
        </div>
        <div style="font-size: 0.78rem; color: #CBD5E1; margin: 6px 0;">
            Billed to: <strong>{cur_inv['org']}</strong><br>
            M-Pesa Receipt: <code>{cur_inv['mpesa_ref']}</code> • KES {cur_inv['grand_total']:,.0f}
        </div>
    </div>
    """
                st.markdown(clean_html_card(inv_card_html), unsafe_allow_html=True)

                inv_txt = f"""=======================================================
    STRIDE™ ENTERPRISE EVENT PLATFORM TAX INVOICE
    =======================================================
    Invoice No:    {cur_inv['inv_ref']}
    Date:          {cur_inv['timestamp']}
    Billed Entity: {cur_inv['org']}
    Contact Email: {cur_inv['email']}
    M-Pesa Phone:  {cur_inv['phone']}
    Payment Ref:   {cur_inv['mpesa_ref']}
    Payment Status: PAID IN FULL VIA M-PESA STK PUSH
    -------------------------------------------------------
    ITEMIZED SCOPE & SERVICES
    -------------------------------------------------------
    1. Platform Scale License ({cur_inv['scale_tag']}): KES {cur_inv['base_fee']:,.2f}
    2. Specialized Module ({cur_inv['voting_tag']}): KES {cur_inv['voting_fee']:,.2f}
    3. Hardware Deployment ({cur_inv['hw_tag']}): KES {cur_inv['hw_fee']:,.2f}
    4. Compliance & Auditing ({cur_inv['audit_tag']}): KES {cur_inv['audit_fee']:,.2f}
    -------------------------------------------------------
    Subtotal (Excl. VAT):  KES {cur_inv['subtotal']:,.2f}
    VAT (16%):             KES {cur_inv['vat_amt']:,.2f}
    TOTAL PAID IN FULL:    KES {cur_inv['grand_total']:,.2f}
    =======================================================
    Provisioned Event ID:  {cur_inv['event_id']}
    Gate Scanner URL:      https://cbk-stride.streamlit.app/EVENTS?event_id={cur_inv['event_id']}
    =======================================================
    Thank you for powering your event on STRIDE™ Enterprise."""

                st.download_button(
                    label=f"📥 Download Tax Invoice ({cur_inv['inv_ref']}.txt)",
                    data=inv_txt.encode('utf-8'),
                    file_name=f"STRIDE_Invoice_{cur_inv['inv_ref']}.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            # Gate QR Card
            last_eid = st.session_state.get("wz_last_created_id", "EVT-2026-002")
            last_title = st.session_state.get("wz_last_created_title", "👔 Annual General Meeting & Corporate Gala")

            reg_share_url = f"https://cbk-stride.streamlit.app/EVENTS?event_id={last_eid}"
            gate_qr_img = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={reg_share_url}"

            gate_desk_html = f"""
    <div style="background: rgba(8, 24, 48, 0.85); border: 2px solid #00F2FE; border-radius: 14px; padding: 18px; text-align: center;">
        <div style="font-size: 0.72rem; color: #00F2FE; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">
            OFFICIAL ENTRANCE SCANNER DESK
        </div>
        <h4 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.02rem;">{last_title}</h4>
        <div style="font-size: 0.75rem; color: #94A3B8; margin-bottom: 10px;">Event ID: <code>{last_eid}</code></div>
    
        <div style="background: #FFFFFF; border-radius: 10px; padding: 10px; display: inline-block; margin-bottom: 10px;">
            <img src="{gate_qr_img}" alt="Gate Entrance QR" style="display: block; width: 155px; height: 155px;" />
        </div>
    
        <div style="font-size: 0.76rem; color: #CBD5E1; line-height: 1.4;">
            📢 <strong>Entrance Instructions:</strong> Display this QR on an iPad/tablet at the gate or print on venue banners. Attendees scan it to register or check in instantly.
        </div>
    
        <div style="background: rgba(0, 242, 254, 0.1); border: 1px dashed rgba(0,242,254,0.4); border-radius: 8px; padding: 8px; margin-top: 10px; font-size: 0.72rem; word-break: break-all; color: #00F2FE;">
            🔗 {reg_share_url}
        </div>
    </div>
    """
            st.markdown(clean_html_card(gate_desk_html), unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("##### 📊 Live Published Events Directory")
            ev_list = backend.get_events(status="ALL")
            if ev_list:
                df_ev_display = pd.DataFrame(ev_list)[["event_id", "title", "category", "event_date", "venue", "standard_price", "status"]]
                st.dataframe(df_ev_display, use_container_width=True, hide_index=True)

        st.markdown("---")
        with st.expander("📜 Returning Officer AGM Ballot Builder & Candidate Manager", expanded=is_bks_mode or is_wz_agm):
            st.markdown("""
            <div style="background: rgba(245, 197, 66, 0.1); border: 1.5px solid #F5C542; border-radius: 10px; padding: 12px 16px; margin-bottom: 14px;">
                <span style="color: #F5C542; font-weight: 800; font-size: 0.9rem;">🏛️ SECRETARIAT & RETURNING OFFICER BALLOT EDITOR</span>
                <p style="margin: 4px 0 0 0; color: #CBD5E1; font-size: 0.78rem;">
                    Configure and lock the official AGM agenda, candidate nominations, and ordinary resolutions before voting opens. Changes saved here dynamically update the <strong>Digital Voting Booth (Tab 4)</strong> for all accredited delegates.
                </p>
            </div>
            """, unsafe_allow_html=True)

            cur_cfg = st.session_state.get("sacco_ballot_config", {
                "res1_title": "Ordinary Resolution 1: Approval of Audited Financial Statements for FY2025 and Declaration of a 14% First & Final Dividend",
                "res1_options": ["FOR (Approve Accounts & 14% Dividend)", "AGAINST (Reject Accounts)", "ABSTAIN"],
                "res2_title": "Item 2: Election of Supervisory Board Member (Nairobi East & Central Region)",
                "res2_candidates": [
                    "Sarah Wanjiru CPA(K) (Independent, Audit & Finance)",
                    "Eng. David Ndung'u (Incumbent, Risk & Governance)",
                    "Dr. Peter Otieno (Institutional Nominee)"
                ],
                "res3_title": "Ordinary Resolution 2: Appointment of External Statutory Auditors for FY2026",
                "res3_auditors": ["Re-appoint KPMG Kenya", "Appoint PKF Kenya", "Appoint Deloitte East Africa", "ABSTAIN"]
            })

            b_col1, b_col2, b_col3 = st.columns(3)
            with b_col1:
                st.markdown("##### 📜 Item 1: Ordinary Resolution 1")
                cfg_r1_title = st.text_input("Resolution Title / Motion Description:", value=cur_cfg["res1_title"], key="cfg_r1_title")
                cfg_r1_opts_raw = st.text_area("Voting Options (one per line):", value="\n".join(cur_cfg["res1_options"]), height=120, key="cfg_r1_opts_raw")

            with b_col2:
                st.markdown("##### 🗳️ Item 2: Board Candidate List")
                cfg_r2_title = st.text_input("Election / Position Title:", value=cur_cfg["res2_title"], key="cfg_r2_title")
                cfg_r2_cands_raw = st.text_area("Nominated Candidates (one per line):", value="\n".join(cur_cfg["res2_candidates"]), height=120, key="cfg_r2_cands_raw")

            with b_col3:
                st.markdown("##### 🏛️ Item 3: Statutory Auditors")
                cfg_r3_title = st.text_input("Auditor Appointment Motion Title:", value=cur_cfg["res3_title"], key="cfg_r3_title")
                cfg_r3_auds_raw = st.text_area("Auditor Choices (one per line):", value="\n".join(cur_cfg["res3_auditors"]), height=120, key="cfg_r3_auds_raw")

            if st.button("🔒 Save & Lock Official AGM Ballot Paper", type="primary", use_container_width=True, key="btn_save_ballot_config"):
                r1_opts = [line.strip() for line in cfg_r1_opts_raw.splitlines() if line.strip()]
                r2_cands = [line.strip() for line in cfg_r2_cands_raw.splitlines() if line.strip()]
                r3_auds = [line.strip() for line in cfg_r3_auds_raw.splitlines() if line.strip()]

                if not r1_opts:
                    r1_opts = ["FOR (Approve Accounts)", "AGAINST (Reject Accounts)", "ABSTAIN"]
                if not r2_cands:
                    r2_cands = ["Candidate A", "Candidate B"]
                if not r3_auds:
                    r3_auds = ["Re-appoint KPMG Kenya", "ABSTAIN"]

                st.session_state["sacco_ballot_config"] = {
                    "res1_title": cfg_r1_title.strip() or cur_cfg["res1_title"],
                    "res1_options": r1_opts,
                    "res2_title": cfg_r2_title.strip() or cur_cfg["res2_title"],
                    "res2_candidates": r2_cands,
                    "res3_title": cfg_r3_title.strip() or cur_cfg["res3_title"],
                    "res3_auditors": r3_auds
                }
                st.success("✅ Ballot Configuration Saved & Locked! Delegate voting booth (Tab 4) updated live.")
                st.balloons()
                st.rerun()


    # ==============================================================================
# TAB 3: GATE USHER SCANNER & ACCREDITATION ROSTER
# ==============================================================================
with tab_verify:
    st.markdown("### 📷 Gate Usher Entrance Scanner & Live Roster")
    st.caption("Venue ushers, security coordinators, and AGM scrutinizers: enter an attendee's Ticket ID or simulate scanning their QR code to verify admission, validate proxies, and track statutory quorum:")

    v_col1, v_col2 = st.columns([1.1, 1.4])

    # Read ticket from query params or active session state
    qp_confirm_tkt = st.session_state.get("active_ticket_id") or st.query_params.get("confirm", st.query_params.get("tkt", st.query_params.get("ticket_id", "")))
    default_verify_val = qp_confirm_tkt if qp_confirm_tkt else ("TKT-BK-342805" if is_bks_mode else "TKT-849201-11")

    with v_col1:
        st.markdown("#### 🔍 Gate Scanner Simulator")
        test_tkt_id = st.text_input("Enter Ticket ID to Verify:*", value=default_verify_val, placeholder="e.g. TKT-BK-342805", key="input_gate_verify_tkt")
        
        btn_admit_gate = st.button("✅ Admit Attendee / Delegate at Gate", type="primary", use_container_width=True)

        if btn_admit_gate:
            if not test_tkt_id.strip() or test_tkt_id.strip() == "TKT-":
                st.error("Please provide a valid Ticket ID.")
            else:
                ok_adm, msg_adm, adm_ticket = backend.verify_and_admit_ticket(test_tkt_id.strip())
                if ok_adm:
                    st.session_state["active_ticket_id"] = test_tkt_id.strip()
                    st.success(msg_adm)
                    st.balloons()
                else:
                    st.error(msg_adm)

        st.markdown("---")
        st.caption("💡 **Quick Test Tickets:** You can copy any Ticket ID from the accredited roster on the right and test admission.")

        if is_bks_mode:
            st.markdown("<div style='font-size: 0.78rem; color: #F5C542; font-weight: 800; margin-top: 10px;'>💡 Quick Demo Banki Kuu SACCO Delegates:</div>", unsafe_allow_html=True)
            c_gb1, c_gb2 = st.columns(2)
            with c_gb1:
                if st.button("👤 Samuel Gathigi", key="btn_quick_tkt_sam", use_container_width=True):
                    st.session_state["active_ticket_id"] = "TKT-BK-342801"
                    st.rerun()
                if st.button("👤 Capt. Geoffrey", key="btn_quick_tkt_geoff", use_container_width=True):
                    st.session_state["active_ticket_id"] = "TKT-BK-342803"
                    st.rerun()
            with c_gb2:
                if st.button("👤 Dr. Beatrice Kiptoo", key="btn_quick_tkt_bea", use_container_width=True):
                    st.session_state["active_ticket_id"] = "TKT-BK-342802"
                    st.rerun()
                if st.button("👤 Joyce Cheruiyot", key="btn_quick_tkt_joyce", use_container_width=True):
                    st.session_state["active_ticket_id"] = "TKT-BK-342804"
                    st.rerun()

    with v_col2:
        st.markdown("#### 📋 Live Event Accredited Roster")
        roster_evt_options = [e["event_id"] + " — " + e["title"] for e in all_events] if all_events else ["None"]
        default_roster_idx = 0
        if is_bks_mode or param_event_id:
            for idx, opt in enumerate(roster_evt_options):
                if "BANKI-KUU-SACCO" in opt.upper():
                    default_roster_idx = idx
                    break

        v_evt_choice = st.selectbox(
            "Filter Roster by Event / Assembly (Pull-Down):",
            roster_evt_options,
            index=default_roster_idx,
            key="sel_roster_evt"
        )
        if all_events and v_evt_choice != "None":
            target_eid = v_evt_choice.split("—")[0].strip()
            event_tickets = backend.get_tickets_by_event(target_eid)
            cur_roster_evt = backend.get_event_by_id(target_eid)
            is_roster_agm = ("AGM" in target_eid or "AGM" in v_evt_choice.upper() or "SHAREHOLDER" in v_evt_choice.upper() or "GENERAL MEETING" in v_evt_choice.upper())

            if is_roster_agm:
                # STATUTORY AGM QUORUM DASHBOARD
                admitted_tickets = [t for t in event_tickets if t.get("gate_status") == "ADMITTED"]
                principals = [t for t in admitted_tickets if "Principal" in t.get("ticket_tier", "")]
                proxies = [t for t in admitted_tickets if "Proxy" in t.get("ticket_tier", "")]
                officers = [t for t in admitted_tickets if any(k in t.get("ticket_tier", "") for k in ["Director", "Secretary", "Auditor", "Observer", "Institutional"])]
                
                voting_delegates = len(principals) + len(proxies)
                quorum_target = 25  # Statutory floor standard
                if cur_roster_evt and cur_roster_evt.get("description"):
                    desc_str = cur_roster_evt["description"]
                    if "150 Delegates" in desc_str or "Tier-1 Sacco" in desc_str:
                        quorum_target = 150
                    elif "100 Accredited" in desc_str:
                        quorum_target = 100
                    elif "50 Members" in desc_str:
                        quorum_target = 50

                quorum_pct = min(100, int((voting_delegates / quorum_target) * 100))

                st.markdown("""
                <div style="background: rgba(245, 197, 66, 0.12); border: 1.5px solid #F5C542; border-radius: 10px; padding: 12px 16px; margin-bottom: 12px;">
                    <div style="font-weight: 800; color: #F5C542; font-size: 0.9rem; display: flex; justify-content: space-between; align-items: center;">
                        <span>🏛️ STATUTORY AGM QUORUM & ACCREDITATION TELEMETRY</span>
                        <span style="font-size: 0.72rem; background: rgba(245, 197, 66, 0.2); padding: 2px 8px; border-radius: 4px; border: 1px solid rgba(245, 197, 66, 0.4);">
                            COMPANIES ACT 2015 § 284
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                k_q1, k_q2, k_q3, k_q4 = st.columns(4)
                with k_q1:
                    st.metric("Quorum Threshold", f"{quorum_target} Members")
                with k_q2:
                    st.metric("Voting In Room", f"{voting_delegates}", delta=f"{voting_delegates - quorum_target} vs Floor" if voting_delegates >= quorum_target else f"-{quorum_target - voting_delegates} to Quorum")
                with k_q3:
                    st.metric("Principal Voting", f"{len(principals)}")
                with k_q4:
                    st.metric("Proxies Verified", f"{len(proxies)}")

                # Quorum Status Banner
                if voting_delegates >= quorum_target:
                    st.markdown(f"""
                    <div style="background: rgba(16, 185, 129, 0.2); border: 1.5px solid #10B981; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;">
                        <span style="color: #34D399; font-weight: 800; font-size: 0.85rem;">🟢 STATUTORY QUORUM ATTAINED ({voting_delegates}/{quorum_target} Voting Delegates Present • {quorum_pct}%)</span>
                        <div style="color: #CBD5E1; font-size: 0.75rem; margin-top: 2px;">
                            Assembly is lawfully constituted under corporate bylaws. The Chairman may call the meeting to order and proceed with table motions.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    needed = quorum_target - voting_delegates
                    st.markdown(f"""
                    <div style="background: rgba(245, 197, 66, 0.15); border: 1.5px solid #F5C542; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;">
                        <span style="color: #F5C542; font-weight: 800; font-size: 0.85rem;">🟡 PENDING STATUTORY QUORUM ({voting_delegates}/{quorum_target} Voting Delegates Present • {needed} Needed)</span>
                        <div style="color: #CBD5E1; font-size: 0.75rem; margin-top: 2px;">
                            Door ushers and secretarial scrutinizers are accrediting arrivals. Quorum floor is required before resolutions can be enacted.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                st.progress(voting_delegates / quorum_target if voting_delegates < quorum_target else 1.0)

            else:
                # Standard Event Metrics
                k_t1, k_t2, k_t3 = st.columns(3)
                with k_t1:
                    st.metric("Total Passes Issued", len(event_tickets))
                with k_t2:
                    admitted_cnt = len([t for t in event_tickets if t.get("gate_status") == "ADMITTED"])
                    st.metric("Admitted at Gate", admitted_cnt)
                with k_t3:
                    rev_total = sum([float(t.get("amount_paid", 0.0)) for t in event_tickets])
                    st.metric("M-Pesa Revenue (KES)", f"{rev_total:,.0f}")

            if not event_tickets:
                st.info("No tickets registered for this event yet.")
            else:
                df_tkt_show = pd.DataFrame(event_tickets)[[
                    "ticket_id", "attendee_name", "organization", "ticket_tier",
                    "amount_paid", "mpesa_trans_id", "gate_status", "checkin_time"
                ]]
                st.dataframe(df_tkt_show, use_container_width=True, hide_index=True)

                # Export accreditation register
                csv_data = df_tkt_show.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Official Statutory Accreditation Register (.csv)",
                    data=csv_data,
                    file_name=f"Accreditation_Register_{target_eid}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# ==============================================================================
# TAB 4: DIGITAL VOTING & ELECTIONS BOOTH
# ==============================================================================
with tab_ballot:
    st.markdown("### 🗳️ Digital Secret Ballot & Live Scrutineer Tally")
    st.caption("Statutory secret balloting for SACCO, PLC, and union AGMs. Anti-double voting enforcement, share-weighted voting power, and instant returning officer certification:")

    # Event selection for voting
    v_events = backend.get_events(status="ACTIVE")
    if not v_events:
        st.info("No active events currently published.")
    else:
        v_evt_opts = {f"{e['title']} ({e['event_id']})": e for e in v_events}
        default_v_idx = 0
        for idx, (k, e) in enumerate(v_evt_opts.items()):
            if "BANKI-KUU-SACCO" in e["event_id"].upper() or "BANKI KUU" in e["title"].upper():
                default_v_idx = idx
                break
        qp_vote_tkt = (
            st.query_params.get("confirm")
            or st.query_params.get("ticket_id")
            or st.query_params.get("tkt")
            or st.query_params.get("vote_tkt")
            or st.query_params.get("verify_tkt")
            or st.session_state.get("active_ticket_id")
        )
        if qp_vote_tkt:
            for idx, (k, e) in enumerate(v_evt_opts.items()):
                e_tkts = backend.get_event_tickets(e["event_id"])
                if any(qp_vote_tkt.strip().upper() in t.get("ticket_id", "").upper() for t in e_tkts):
                    default_v_idx = idx
                    break

        v_sel_label = st.selectbox("Select Assembly / Event for Voting:*", list(v_evt_opts.keys()), index=default_v_idx, key="v_sel_event")
        v_selected_evt = v_evt_opts[v_sel_label]
        v_eid = v_selected_evt["event_id"]

        col_ballot_in, col_ballot_scrut = st.columns([1.1, 1.35])

        with col_ballot_in:
            st.markdown("#### 🔒 Secure Delegate Voting Station")
            st.markdown("""
            <div style="background: rgba(8, 28, 58, 0.7); border: 1.5px solid rgba(0, 242, 254, 0.4); border-radius: 10px; padding: 10px 14px; margin-bottom: 12px;">
                <span style="color: #00F2FE; font-weight: 800; font-size: 0.82rem;">🛡️ VOTER IDENTITY & BALLOT SECURITY</span>
                <p style="margin: 2px 0 0 0; color: #CBD5E1; font-size: 0.76rem;">
                    In live AGMs, delegates unlock <strong>only their own ballot</strong> by clicking their personal encrypted pass link or entering their confidential <strong>Ticket Serial ID / Member Account ID</strong>. Dropdown selection is disabled for voters to prevent accidental impersonation.
                </p>
            </div>
            """, unsafe_allow_html=True)

            ev_tickets = backend.get_tickets_by_event(v_eid) if hasattr(backend, "get_tickets_by_event") else backend.get_event_tickets(v_eid)

            # Map all tickets by ticket_id, mpesa_trans_id, organization/member_id, and name
            tkt_lookup = {}
            for t in ev_tickets:
                tkt_lookup[t["ticket_id"].upper()] = t
                if t.get("mpesa_trans_id"):
                    tkt_lookup[t["mpesa_trans_id"].upper()] = t
                if "Ref:" in t.get("organization", ""):
                    ref_part = t["organization"].split("Ref:")[-1].replace(")", "").strip().upper()
                    tkt_lookup[ref_part] = t

            if not ev_tickets:
                st.warning("No accredited delegates found for this assembly yet.")
                st.info("💡 Tap below to generate your certified 500-member cohort:")
                if st.button("⚡ Generate 500 Accredited SACCO Delegates", type="primary", use_container_width=True, key="btn_quick_accredit_voter"):
                    df_500 = backend.generate_synthetic_sacco_roster_df(500)
                    backend.bulk_ingest_event_tickets(v_eid, df_500)
                    st.success("Accredited! Refreshing voting booth...")
                    st.rerun()
            else:
                default_v_tkt = qp_vote_tkt or st.session_state.get("active_ticket_id") or ev_tickets[0]["ticket_id"]
                
                eval_mode = st.checkbox("🧪 Evaluator Shortcut (Show Delegate Dropdown for Quick Demo)", value=False, key="chk_eval_voter_mode")
                
                if is_bks_mode and not eval_mode:
                    st.markdown("<div style='font-size: 0.78rem; color: #00F2FE; font-weight: 800; margin-bottom: 6px;'>💡 Quick Demo Voters:</div>", unsafe_allow_html=True)
                    c_vb1, c_vb2, c_vb3 = st.columns(3)
                    with c_vb1:
                        if st.button("👤 Samuel (IT)", key="btn_vote_sam", use_container_width=True):
                            st.session_state["active_ticket_id"] = "TKT-BK-342801"
                            st.rerun()
                    with c_vb2:
                        if st.button("👤 Dr. Beatrice", key="btn_vote_bea", use_container_width=True):
                            st.session_state["active_ticket_id"] = "TKT-BK-342802"
                            st.rerun()
                    with c_vb3:
                        if st.button("👤 Capt. Geoffrey", key="btn_vote_geoff", use_container_width=True):
                            st.session_state["active_ticket_id"] = "TKT-BK-342803"
                            st.rerun()
                
                sel_tkt = None
                if eval_mode:
                    tkt_voter_opts = {f"{t['attendee_name']} ({t['ticket_id']} — {t['ticket_tier']})": t for t in ev_tickets}
                    default_drop_idx = 0
                    if default_v_tkt:
                        for i, (k_opt, t_opt) in enumerate(tkt_voter_opts.items()):
                            if default_v_tkt.strip().upper() in t_opt["ticket_id"].upper() or default_v_tkt.strip().upper() in k_opt.upper():
                                default_drop_idx = i
                                break
                    sel_voter_key = st.selectbox("Select Accredited Delegate (Demo Shortcut):*", list(tkt_voter_opts.keys()), index=default_drop_idx, key="sel_voter_ticket_demo")
                    sel_tkt = tkt_voter_opts[sel_voter_key]
                else:
                    v_input_tkt = st.text_input(
                        "🔑 Enter Your Confidential Ticket Serial ID / Member Account ID:*",
                        value=default_v_tkt,
                        placeholder="e.g. TKT-BK-342805 or SACCO-342805",
                        help="Enter the Ticket Serial ID printed on your digital pass to unlock your ballot paper."
                    )
                    clean_input = v_input_tkt.strip().upper()
                    if clean_input in tkt_lookup:
                        sel_tkt = tkt_lookup[clean_input]
                    else:
                        for t in ev_tickets:
                            if clean_input and (clean_input in t["ticket_id"].upper() or clean_input in t["attendee_name"].upper() or clean_input in t.get("organization","").upper()):
                                sel_tkt = t
                                break

                if not sel_tkt:
                    st.error(f"❌ Ticket Serial ID '{v_input_tkt}' not found in accredited roster.")
                    st.info("💡 Try entering your Ticket Serial ID (e.g. `TKT-BK-342805`) or check 'Evaluator Shortcut' above.")
                else:
                    # Compute voting weight based on ticket tier
                    v_weight = 1
                    if "Principal Shareholder" in sel_tkt["ticket_tier"]:
                        v_weight = 10000
                    elif "Institutional" in sel_tkt["ticket_tier"]:
                        v_weight = 100000
                    elif "Proxy Holder" in sel_tkt["ticket_tier"]:
                        v_weight = 35000
                    elif "Board Director" in sel_tkt["ticket_tier"]:
                        v_weight = 50000

                    gate_badge = '<span style="background: rgba(16, 185, 129, 0.2); color: #34D399; font-size: 0.72rem; font-weight: 800; padding: 2px 8px; border-radius: 4px; border: 1px solid #10B981;">🟢 GATE ACCREDITED</span>' if sel_tkt.get("gate_status") == "ADMITTED" else '<span style="background: rgba(245, 197, 66, 0.2); color: #F5C542; font-size: 0.72rem; font-weight: 800; padding: 2px 8px; border-radius: 4px; border: 1px solid #F5C542;">🌐 HYBRID / REMOTE VOTER</span>'

                    # Delegate Voting Credentials Card
                    st.markdown(f"""
                    <div style="background: rgba(8, 28, 58, 0.85); border: 2px solid #00F2FE; border-radius: 12px; padding: 14px 18px; margin: 8px 0 16px 0; box-shadow: 0 6px 20px rgba(0,242,254,0.2);">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="color: #00F2FE; font-weight: 900; font-size: 0.82rem; letter-spacing: 1px;">🔒 AUTHENTICATED DELEGATE BALLOT</span>
                            {gate_badge}
                        </div>
                        <div style="font-size: 1.1rem; font-weight: 800; color: #FFFFFF; margin-top: 6px;">{sel_tkt['attendee_name']}</div>
                        <div style="font-size: 0.8rem; color: #94A3B8;">{sel_tkt['organization']} • Serial: <code>{sel_tkt['ticket_id']}</code></div>
                        <div style="margin-top: 8px; padding-top: 8px; border-top: 1px dashed rgba(255,255,255,0.1); font-size: 0.88rem; color: #F5C542; font-weight: 800;">
                            ⚖️ Certified Voting Power: <strong>{v_weight:,} Votes</strong> ({sel_tkt['ticket_tier'].split('/')[0].strip()})
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                existing_ballots = backend.get_event_ballots(v_eid)
                has_voted = any(b["ticket_id"] == sel_tkt["ticket_id"] for b in existing_ballots)

                if has_voted:
                    voted_ballot = next(b for b in existing_ballots if b["ticket_id"] == sel_tkt["ticket_id"])
                    st.success(f"✓ Ballot Cast & Certified! Vote was recorded on {voted_ballot['cast_time']}.")
                    st.code(f"Cryptographic Proof: {voted_ballot['ballot_hash']}")
                else:
                    b_config = st.session_state.get("sacco_ballot_config", {
                        "res1_title": "Ordinary Resolution 1: Approval of Audited Financial Statements for FY2025 and Declaration of a 14% First & Final Dividend",
                        "res1_options": ["FOR (Approve Accounts & 14% Dividend)", "AGAINST (Reject Accounts)", "ABSTAIN"],
                        "res2_title": "Item 2: Election of Supervisory Board Member (Nairobi East & Central Region)",
                        "res2_candidates": [
                            "Sarah Wanjiru CPA(K) (Independent, Audit & Finance)",
                            "Eng. David Ndung'u (Incumbent, Risk & Governance)",
                            "Dr. Peter Otieno (Institutional Nominee)"
                        ],
                        "res3_title": "Ordinary Resolution 2: Appointment of External Statutory Auditors for FY2026",
                        "res3_auditors": ["Re-appoint KPMG Kenya", "Appoint PKF Kenya", "Appoint Deloitte East Africa", "ABSTAIN"]
                    })

                    with st.form(key=f"form_ballot_{sel_tkt['ticket_id']}"):
                        st.markdown(f"##### 📜 {b_config['res1_title']}")
                        st.caption("Cast your vote on Item 1 Ordinary Resolution:")
                        v_res1 = st.radio(
                            "Your Vote on Resolution 1:*",
                            b_config["res1_options"],
                            index=None,
                            key=f"v_res1_radio_{sel_tkt['ticket_id']}"
                        )

                        st.markdown(f"##### 🗳️ {b_config['res2_title']}")
                        st.caption("Select one nominated candidate for Item 2:")
                        v_res2 = st.radio(
                            "Candidate Selection:*",
                            b_config["res2_candidates"],
                            index=None,
                            key=f"v_res2_radio_{sel_tkt['ticket_id']}"
                        )

                        st.markdown(f"##### 🏛️ {b_config['res3_title']}")
                        st.caption("Select statutory auditor for Item 3:")
                        aud_options = ["Select Statutory Auditor..."] + [a for a in b_config["res3_auditors"] if a != "Select Statutory Auditor..."]
                        v_res3 = st.selectbox(
                            "Statutory Auditor Appointment:*",
                            aud_options,
                            index=0,
                            key=f"v_res3_sel_{sel_tkt['ticket_id']}"
                        )

                        btn_submit_ballot = st.form_submit_button(
                            f"🔒 Cast Confidential Ballot ({v_weight:,} Votes)",
                            type="primary",
                            use_container_width=True
                        )

                        if btn_submit_ballot:
                            if not v_res1:
                                st.error("❌ Please cast your vote on Item 1 (Ordinary Resolution 1).")
                            elif not v_res2:
                                st.error("❌ Please select a candidate for Item 2 (Supervisory Board Member).")
                            elif not v_res3 or v_res3.startswith("Select"):
                                st.error("❌ Please select an option for Item 3 (Statutory Auditor Appointment).")
                            else:
                                ok_b, msg_b, b_rec = backend.cast_event_ballot(
                                    event_id=v_eid,
                                    ticket_id=sel_tkt["ticket_id"],
                                    voter_name=sel_tkt["attendee_name"],
                                    voter_organization=sel_tkt["organization"],
                                    voting_weight=v_weight,
                                    res1_vote=v_res1,
                                    res2_candidate=v_res2,
                                    res3_auditor=v_res3
                                )
                                if ok_b:
                                    if sel_tkt.get("gate_status") != "ADMITTED":
                                        backend.verify_and_admit_ticket(sel_tkt["ticket_id"])
                                    st.session_state["last_cast_ballot"] = b_rec
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error(msg_b)

        with col_ballot_scrut:
            st.markdown("#### 📊 Returning Officer Live Telemetry Screen")
            st.caption("Official scrutineer board updating dynamically in real time as ballots are verified:")

            el_res = backend.get_election_results(v_eid)
            tot_b = el_res["total_ballots"]
            tot_w = el_res["total_weighted_votes"]

            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.metric("Total Ballots Cast", f"{tot_b}")
            with sc2:
                st.metric("Weighted Voting Power", f"{tot_w:,}")
            with sc3:
                st.metric("Integrity Status", "100% SHA-256", delta="VERIFIED")

            st.markdown("---")

            # Tally Display: Resolution 1
            st.markdown("##### 📜 Resolution 1: FY2025 Accounts & 14% Dividend")
            r1_weighted = el_res["res1"]["weighted"]
            for opt, cnt in r1_weighted.items():
                pct = (cnt / tot_w * 100) if tot_w > 0 else 0
                bar_color = "#10B981" if "FOR" in opt else ("#EF4444" if "AGAINST" in opt else "#94A3B8")
                st.markdown(f"""
                <div style="margin-bottom: 6px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 700; color: #CBD5E1;">
                        <span>{opt}</span>
                        <span style="color: {bar_color};">{cnt:,} votes ({pct:.1f}%)</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.08); border-radius: 6px; height: 10px; width: 100%; overflow: hidden; margin-top: 2px;">
                        <div style="background: {bar_color}; height: 100%; width: {pct}%; border-radius: 6px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # Tally Display: Supervisory Committee Election
            st.markdown("##### 🗳️ Supervisory Committee Election Tally")
            r2_weighted = el_res["res2"]["weighted"]
            leader = max(r2_weighted.items(), key=lambda x: x[1])[0] if r2_weighted else "None"
            for cand, cnt in r2_weighted.items():
                pct = (cnt / tot_w * 100) if tot_w > 0 else 0
                is_lead = (cand == leader and cnt > 0)
                badge_icon = "🏆 " if is_lead else ""
                cand_color = "#F5C542" if is_lead else "#38BDF8"
                st.markdown(f"""
                <div style="margin-bottom: 6px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.8rem; font-weight: 700; color: #CBD5E1;">
                        <span style="color: {cand_color};">{badge_icon}{cand}</span>
                        <span style="color: {cand_color};">{cnt:,} votes ({pct:.1f}%)</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.08); border-radius: 6px; height: 10px; width: 100%; overflow: hidden; margin-top: 2px;">
                        <div style="background: {cand_color}; height: 100%; width: {pct}%; border-radius: 6px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # Scrutineer Certificate Export
            cert_txt = f"""=======================================================
STRIDE™ CERTIFIED RETURNING OFFICER ELECTION RETURN
=======================================================
Assembly:             {v_selected_evt['title']}
Event ID:             {v_eid}
Certified Date:       {get_eat_now().strftime('%Y-%m-%d %H:%M:%S')}
Scrutineer Standard:  SHA-256 Cryptographic Audit Ledger
-------------------------------------------------------
STATUTORY QUORUM & PARTICIPATION
Total Ballots Cast:   {tot_b}
Total Weighted Power: {tot_w:,} Votes
Double-Voting Cases:  0 (Anti-Passback Enforced)
-------------------------------------------------------
RESOLUTION 1: FY2025 ACCOUNTS & 14% DIVIDENDS
""" + "\n".join([f"- {k}: {v:,} votes ({(v/tot_w*100) if tot_w>0 else 0:.1f}%)" for k, v in r1_weighted.items()]) + f"""
-------------------------------------------------------
SUPERVISORY COMMITTEE ELECTION RESULTS
""" + "\n".join([f"- {k}: {v:,} votes ({(v/tot_w*100) if tot_w>0 else 0:.1f}%)" for k, v in r2_weighted.items()]) + f"""
DECLARATION: Duly Elected Candidate: {leader}
-------------------------------------------------------
STATUTORY AUDITOR APPOINTMENT
""" + "\n".join([f"- {k}: {v:,} votes ({(v/tot_w*100) if tot_w>0 else 0:.1f}%)" for k, v in el_res['res3']['weighted'].items()]) + f"""
=======================================================
Certified by Chief Scrutineer & Company Secretary
SASRA & Cooperative Societies Compliance Code 2026"""

            st.download_button(
                label="📥 Download Certified Returning Officer Return (.txt)",
                data=cert_txt.encode('utf-8'),
                file_name=f"CERTIFIED_ELECTION_RETURN_{v_eid}.txt",
                mime="text/plain",
                use_container_width=True
            )

# ==============================================================================
# TAB 5: NLP ATTENDEE SENTIMENT & PULSE SURVEY ENGINE
# ==============================================================================
with tab_nlp:
    st.markdown("### 🤖 NLP Attendee Satisfaction & Sentiment Telemetry")
    st.caption("Real-time Natural Language Processing (NLP) analyzing open-ended attendee feedback, extracting operational aspects, and calculating Net Promoter Score (NPS) for the Board:")

    col_fb_in, col_fb_board = st.columns([1.1, 1.35])

    with col_fb_in:
        st.markdown("#### 💬 Attendee Exit Pulse (Survey)")
        st.caption("Delegates and athletes share honest post-event feedback in natural English or Swahili:")

        fb_ev_opts = {f"{e['title']} ({e['event_id']})": e for e in v_events}
        default_fb_idx = 0
        if is_bks_mode or param_event_id == "EVT-BANKI-KUU-SACCO":
            for idx, (k, e) in enumerate(fb_ev_opts.items()):
                if "BANKI-KUU-SACCO" in e["event_id"].upper():
                    default_fb_idx = idx
                    break
        else:
            for idx, (k, e) in enumerate(fb_ev_opts.items()):
                if "AGM" in e['category'].upper() or "AGM" in e['title'].upper() or "SHAREHOLDER" in e['title'].upper():
                    default_fb_idx = idx
                    break

        fb_sel_label = st.selectbox("Assembly / Event to Review:*", list(fb_ev_opts.keys()), index=default_fb_idx, key="fb_sel_event")
        fb_selected_evt = fb_ev_opts[fb_sel_label]
        fb_eid = fb_selected_evt["event_id"]

        # Dynamically resolve delegate name from URL or active ticket
        nlp_qp_name = st.query_params.get("name", "").strip()
        nlp_active_tkt = st.session_state.get("active_ticket_id") or st.query_params.get("confirm", st.query_params.get("tkt", st.query_params.get("ticket_id", "")))
        
        default_nlp_name = ""
        if nlp_qp_name:
            default_nlp_name = nlp_qp_name
        elif nlp_active_tkt:
            fb_tkts = backend.get_event_tickets(fb_eid)
            for t in fb_tkts:
                if nlp_active_tkt.strip().upper() in t.get("ticket_id", "").upper():
                    default_nlp_name = t.get("attendee_name", "")
                    break
        
        if not default_nlp_name:
            default_nlp_name = "Stanley Gicho" if is_bks_mode else "Accredited Delegate"

        fb_name = st.text_input("Your Name / Delegate Identifier:*", value=default_nlp_name, key="fb_in_name")
        fb_rating = st.slider("Overall Satisfaction Rating (1 to 5 Stars):*", min_value=1, max_value=5, value=5, key="fb_in_rating")

        # Test Chip Injectors
        st.markdown("<div style='font-size: 0.76rem; color: #94A3B8; margin-top: 6px;'>💡 <strong>Instant Test Presets (Tap to Inject & Test NLP):</strong></div>", unsafe_allow_html=True)
        c_ch1, c_ch2 = st.columns(2)
        with c_ch1:
            if st.button("🚀 Fast M-Pesa & Quorum", key="btn_chip_pos", use_container_width=True):
                st.session_state["nlp_sample_box"] = "The M-Pesa STK self-registration was lightning fast! Zero lines at the gate and the digital quorum screen was completely transparent."
        with c_ch2:
            if st.button("⚠️ Good QR, Slow Food", key="btn_chip_mix", use_container_width=True):
                st.session_state["nlp_sample_box"] = "QR check-in was seamless, but lunch catering was delayed and the sound in the back was muffled."

        c_ch3, c_ch4 = st.columns(2)
        with c_ch3:
            if st.button("❌ Terrible Queues & Mic", key="btn_chip_neg", use_container_width=True):
                st.session_state["nlp_sample_box"] = "Terrible experience with registration queues! Microphones failed and the sitting allowance payout was disorganized."
        with c_ch4:
            if st.button("🇰🇪 Swahili Feedback", key="btn_chip_swa", use_container_width=True):
                st.session_state["nlp_sample_box"] = "Chakula kilichelewa kidogo ukumbini lakini usajili wa simu na kura ya kidijitali ilikuwa safi na haraka sana!"

        default_preset = "The M-Pesa STK self-registration and WhatsApp QR gate pass were lightning fast! Zero lines at KICC main entrance, and the digital quorum screen gave us total transparency on the 14% dividend vote." if is_bks_mode else "The M-Pesa STK self-registration and QR gate pass was lightning fast! Zero lines at venue entrance, and the digital quorum screen gave us total transparency on the dividend vote."
        preset_val = st.session_state.get("nlp_sample_box", default_preset)
        fb_text = st.text_area("Your Open-Ended Feedback:*", value=preset_val, height=110, key="fb_in_text")

        # Live Pre-Flight NLP Preview
        nlp_preview = backend.analyze_feedback_nlp(fb_text)
        prev_color = "#10B981" if nlp_preview["label"] == "POSITIVE" else ("#EF4444" if nlp_preview["label"] == "NEGATIVE" else "#F5C542")

        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.7); border: 1.5px dashed {prev_color}; border-radius: 8px; padding: 10px 14px; margin: 8px 0 14px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.72rem; color: #94A3B8; font-weight: 800; text-transform: uppercase;">REAL-TIME NLP PREVIEW</span>
                <span style="background: {prev_color}; color: #020617; font-size: 0.7rem; font-weight: 900; padding: 2px 6px; border-radius: 4px;">
                    {nlp_preview['label']} ({nlp_preview['polarity']:+.2f})
                </span>
            </div>
            <div style="margin-top: 6px; font-size: 0.75rem; color: #CBD5E1;">
                <strong>Extracted Aspects:</strong> {', '.join(f'`{a}`' for a in nlp_preview['aspects'])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("📤 Submit Attendee Feedback & Analyze NLP", type="primary", use_container_width=True, key="btn_sub_fb"):
            if not fb_name.strip():
                st.error("Please provide your name or delegate identifier.")
            elif not fb_text.strip():
                st.error("Please enter your feedback comments.")
            else:
                ok_f, msg_f, f_rec = backend.submit_event_feedback(
                    event_id=fb_eid,
                    ticket_id="TKT-DIRECT",
                    attendee_name=fb_name.strip(),
                    rating=fb_rating,
                    feedback_text=fb_text.strip()
                )
                if ok_f:
                    st.success(msg_f)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(msg_f)

    with col_fb_board:
        st.markdown("#### 📈 Executive Sentiment & NPS Board")
        st.caption("Live AI analytics dashboard for the Chairman, Board of Directors, and Secretariat:")

        feedbacks = backend.get_event_feedback(fb_eid)
        tot_fb = len(feedbacks)

        if tot_fb == 0:
            st.info("No feedback submitted yet for this assembly. Be the first to submit above!")
        else:
            avg_rating = sum(f["rating"] for f in feedbacks) / tot_fb
            avg_polarity = sum(f["sentiment_score"] for f in feedbacks) / tot_fb

            promoters = sum(1 for f in feedbacks if f["rating"] == 5)
            detractors = sum(1 for f in feedbacks if f["rating"] <= 3)
            nps_score = round(((promoters - detractors) / tot_fb) * 100)

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric("Net Promoter Score", f"+{nps_score}" if nps_score > 0 else f"{nps_score}", delta="WORLD CLASS" if nps_score >= 50 else "GOOD")
            with m2:
                st.metric("Avg Star Rating", f"{avg_rating:.1f} / 5.0", "⭐")
            with m3:
                st.metric("Sentiment Polarity", f"{avg_polarity:+.2f}", "🟢 POSITIVE" if avg_polarity >= 0.15 else ("🔴 NEGATIVE" if avg_polarity <= -0.15 else "🟡 NEUTRAL"))
            with m4:
                st.metric("Total Responses", f"{tot_fb}")

            st.markdown("---")

            # Aspect Sentiment Breakdown
            st.markdown("##### 🔍 Operational Aspects Health Matrix")
            aspect_counts = {}
            for f in feedbacks:
                for a in f.get("aspects", []):
                    aspect_counts[a] = aspect_counts.get(a, 0) + 1

            for a_name, cnt in sorted(aspect_counts.items(), key=lambda x: x[1], reverse=True):
                pct = (cnt / tot_fb) * 100
                st.markdown(f"""
                <div style="margin-bottom: 6px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.78rem; font-weight: 700; color: #CBD5E1;">
                        <span>🏷️ {a_name}</span>
                        <span style="color: #00F2FE;">{cnt} mentions ({pct:.0f}%)</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.08); border-radius: 4px; height: 6px; width: 100%; overflow: hidden; margin-top: 2px;">
                        <div style="background: #00F2FE; height: 100%; width: {pct}%; border-radius: 4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # Live Feed of Feedback with Sentiment Badges
            st.markdown("##### 📢 Recent Attendee Feedback Stream")
            for fb in feedbacks[:6]:
                sc_col = "#10B981" if fb["sentiment_label"] == "POSITIVE" else ("#EF4444" if fb["sentiment_label"] == "NEGATIVE" else "#F5C542")
                stars = "⭐" * fb["rating"]
                st.markdown(f"""
                <div style="background: rgba(8, 24, 48, 0.7); border-left: 4px solid {sc_col}; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="font-weight: 800; font-size: 0.85rem; color: #FFFFFF;">{fb['attendee_name']}</span>
                        <span style="background: rgba(255,255,255,0.1); padding: 1px 6px; border-radius: 4px; font-size: 0.7rem; color: #F5C542;">{stars}</span>
                    </div>
                    <div style="font-size: 0.8rem; color: #CBD5E1; margin: 4px 0 6px 0; font-style: italic;">
                        "{fb['feedback_text']}"
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.68rem; color: #64748B;">
                        <span>Aspects: {', '.join(fb.get('aspects', []))}</span>
                        <span style="color: {sc_col}; font-weight: 800;">{fb['sentiment_label']} ({fb['sentiment_score']:+.2f})</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------------------
if is_bks_mode:
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 1.4rem; border-top: 1.5px solid rgba(245, 197, 66, 0.35); color: #94A3B8; font-size: 0.82rem; background: rgba(4, 16, 33, 0.8); border-radius: 12px;">
        <strong style="color: #F5C542;">Banki Kuu Staff SACCO Society Ltd.</strong> • 58th AGM & Board Elections Governance Portal<br>
        <span style="font-size: 0.75rem; color: #64748B;">Powered by STRIDE™ Enterprise Telemetry & E-Voting Platform • SASRA Statutory Compliance Certified • <a href="/DEMO" style="color: #00F2FE; text-decoration: none;">🧪 Evaluator Sandbox</a></span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; margin-top: 3rem; padding: 1.4rem; border-top: 1px solid rgba(245, 197, 66, 0.25); color: #94A3B8; font-size: 0.82rem; background: rgba(4, 16, 33, 0.6); border-radius: 12px;">
        <strong style="color: #F5C542;">STRIDE™</strong> • Enterprise Event Telemetry, Accreditation & M-Pesa Ticketing Platform<br>
        <span style="font-size: 0.75rem; color: #64748B;">Multi-Tenant Commercial Event Management & Gate Control • <a href="/DEMO" style="color: #F5C542; text-decoration: none;">🧪 Evaluator Sandbox</a></span>
    </div>
    """, unsafe_allow_html=True)

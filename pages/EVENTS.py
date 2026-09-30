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
st.set_page_config(
    page_title="STRIDE™ | Event Registration & Ticketing",
    page_icon="🎟️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
# TOP GLOBAL NAVIGATION BAR
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# READ QUERY PARAMS (IF ACCESSED VIA DIRECT EVENT QR OR LINK)
# ------------------------------------------------------------------------------
param_event_id = st.query_params.get("event_id", "")

# ------------------------------------------------------------------------------
# MAIN PORTAL TABS
# ------------------------------------------------------------------------------
tab_reg, tab_wizard, tab_verify = st.tabs([
    "🎟️ Attendee Registration & Digital Pass",
    "🪄 Event Creator Wizard (Organizers)",
    "📷 Gate Usher Scanner & Accreditation Roster"
])

# ==============================================================================
# TAB 1: ATTENDEE REGISTRATION & M-PESA TICKETING
# ==============================================================================
with tab_reg:
    st.markdown("### 🎟️ Attendee Self-Registration & Dynamic QR Ticket Pass")
    st.caption("Register for upcoming corporate sports championships, AGMs, conferences, galas, or marathons. Pay via Safaricom M-Pesa STK Push and receive an encrypted digital pass instantly:")

    # Retrieve published events from SQLite
    all_events = backend.get_events(status="ACTIVE")
    if not all_events:
        st.warning("No active events currently published. Use the 'Event Creator Wizard' tab to create your first event!")
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
        
        # Preselect if event_id is in query params
        default_idx = 0
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

                    agm_acc_num = st.text_input(
                        "Shareholder / CDSC / Member Account Number:*",
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
                    chosen_amt = 5000.0  # Statutory AGM Accreditation fee fixed at KES 5,000

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

                att_name = st.text_input("Full Name (as per Official ID / National ID):*", placeholder="e.g. Wallace Mbugua")
                att_email = st.text_input("Email Address (for pass delivery):*", placeholder="e.g. wallace@enterprise.co.ke")
                att_org = st.text_input("Organization / Company / Sacco Branch:*", placeholder="e.g. Finance & Accounts / Equity Bank")
                att_phone = st.text_input("Safaricom M-Pesa Phone Number:*", placeholder="07XX XXX XXX", value="0722123456", help="Mobile number for STK Push prompt")

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
                        
                        # Set STK Pending Payload to trigger interactive handset simulator
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
                st.info("👈 Fill out the registration form on the left and tap **'Pay KES 5,000 via M-Pesa STK & Register'** to generate your official pass.")
                st.markdown("""
                <div style="background: rgba(8, 24, 48, 0.6); border: 2px dashed rgba(255,255,255,0.15); border-radius: 12px; padding: 40px 20px; text-align: center; color: #64748B;">
                    <div style="font-size: 3.5rem; margin-bottom: 10px;">🎟️</div>
                    <div style="font-weight: 700; color: #94A3B8; font-size: 1rem;">No Active Ticket Pass Generated Yet</div>
                    <div style="font-size: 0.8rem; margin-top: 6px;">Your encrypted dynamic QR ticket pass will render here immediately following payment verification.</div>
                </div>
                """, unsafe_allow_html=True)
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

                st.markdown(f"""
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
                """, unsafe_allow_html=True)

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

# ==============================================================================
# TAB 2: EVENT CREATOR WIZARD (FOR ORGANIZERS & CORPORATES)
# ==============================================================================
with tab_wizard:
    st.markdown("### 🪄 Universal Event & AGM Commercial Scoping Wizard")
    st.caption("Answer 4 quick scoping questions to determine your platform deployment scope, calculate your customized fee, and provision certified gate scanners instantly via M-Pesa:")

    wz_col1, wz_col2 = st.columns([1.35, 1])

    with wz_col1:
        # Category Selector outside form for reactive pricing
        wz_cat = st.selectbox(
            "Select Event Type / Assembly Category (Pull-Down):*",
            [
                "👔 Corporate AGM & Shareholder Assembly",
                "🏆 Sports Tournament & Derby",
                "🏃 Marathon, Fun Run & Athletics",
                "💡 Industry Conference & Tech Summit",
                "🎉 Corporate Gala Dinner & Awards",
                "🎓 School / University Sports Day",
                "💒 Private Reception / Social Gala"
            ],
            key="wz_event_category_selector"
        )
        is_wz_agm = ("AGM" in wz_cat or "Shareholder" in wz_cat)

        st.markdown("#### 1️⃣ Assembly Identity & Schedule")
        if is_wz_agm:
            e_title = st.text_input("Official AGM / Assembly Name:*", value="58th Annual General Meeting & Shareholder Elections", placeholder="e.g. 58th Annual General Meeting of Shareholders & Delegates", key="wz_e_title")
            e_host = st.text_input("Society / Convening Corporate Body:*", value="Apex Capital Holdings PLC Board & Secretariat", placeholder="e.g. Harambee Sacco Society Limited", key="wz_e_host")
            
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
                e_time = st.text_input("Assembly Call-to-Order Time:", value="09:00", key="wz_e_time")
            e_venue = st.text_input("Assembly Hall & Physical Address:*", value="Kenyatta International Convention Centre (KICC) / Grand Ballroom, Nairobi", key="wz_e_venue")

            if "Paid" in e_admit_mode:
                tc1, tc2 = st.columns(2)
                with tc1:
                    e_std_price = st.number_input("Shareholder Clearance Fee (KES):", min_value=0.0, value=5000.0, step=500.0, key="wz_std_price")
                with tc2:
                    e_vip_price = st.number_input("VIP / Board Delegate (KES):", min_value=0.0, value=5000.0, step=500.0, key="wz_vip_price")
                e_paid = True
                e_paybill = st.text_input("M-Pesa Paybill / Till Number for Settlements:", value="849200", key="wz_paybill")
            else:
                e_std_price = 0.0
                e_vip_price = 0.0
                e_paid = False
                e_paybill = "N/A (COMPLIMENTARY)"

            clean_gate_mode = "SINGLE_GATE"
            e_desc = st.text_area(
                "Statutory Notice & Agenda to Shareholders:*",
                value="Notice is hereby given that the Annual General Meeting will convene to: 1. Table the audited financial statements for FY2025. 2. Elect executive committee members. 3. Appoint external statutory auditors. 4. Transact any other ordinary business.",
                key="wz_agm_desc"
            )

        else:
            e_title = st.text_input("Official Event Name:*", placeholder="e.g. Kenya Airways Annual Sports Derby & Family Fun Day", key="wz_e_title")
            e_host = st.text_input("Host Company / Organizing Body:*", placeholder="e.g. KQ Sports Club Secretariat", key="wz_e_host")
            
            ec1, ec2 = st.columns(2)
            with ec1:
                e_date = st.date_input("Event Date:", value=now_dt.date() + datetime.timedelta(days=14), key="wz_e_date")
            with ec2:
                e_time = st.text_input("Start / Kick-off Time:", value="08:30", key="wz_e_time")
            e_venue = st.text_input("Venue & Physical Address:*", placeholder="e.g. Ngong Racecourse Grounds, Nairobi", key="wz_e_venue")

            tc1, tc2, tc3 = st.columns(3)
            with tc1:
                e_paid = st.checkbox("Paid Event (Collect via M-Pesa)", value=True, key="wz_paid_chk")
            with tc2:
                e_std_price = st.number_input("Standard Ticket (KES):", min_value=0.0, value=1000.0, step=100.0, key="wz_std_price")
            with tc3:
                e_vip_price = st.number_input("VIP / Delegate (KES):", min_value=0.0, value=3500.0, step=500.0, key="wz_vip_price")

            e_paybill = st.text_input("M-Pesa Paybill / Till Number for Settlements:", value="849200", key="wz_paybill")
            e_gate_mode = st.selectbox(
                "Gate Scanning Protocol:*",
                [
                    "DUAL_GATE (Arrival Scan + Departure Scan for Allowance Floor Verification)",
                    "SINGLE_GATE (Entry Scan Only for Galas, AGMs & Conferences)"
                ],
                key="wz_gate_mode"
            )
            clean_gate_mode = "DUAL_GATE" if "DUAL_GATE" in e_gate_mode else "SINGLE_GATE"
            e_desc = st.text_area("Event Description & Attendee Instructions:", placeholder="e.g. Official sports kit required. Breakfast and lunch provided at Pavilion A. Gate closes at 09:30.", key="wz_sports_desc")

        st.markdown("---")
        st.markdown("#### 2️⃣ Commercial Scope Questionnaire (Pricing Engine)")
        st.caption("Select your exact operational scale and compliance requirements. STRIDE™ recalculates your customized setup quote in real-time on the right:")

        if is_wz_agm:
            sc_scale = st.selectbox(
                "Q1: Expected Delegate / Shareholder Attendance (Pull-Down):*",
                [
                    "🐥 Tier 1: Small Society / Club AGM (Up to 100 Delegates) — KES 5,000",
                    "🏢 Tier 2: Mid-Sized Corporate / SACCO (101 – 500 Delegates) — KES 35,000",
                    "🏛️ Tier 3: Large Listed PLC / Tier-1 SACCO (501 – 2,500 Delegates) — KES 75,000",
                    "🌐 Tier 4: Mega National Assembly (2,500+ Delegates) — KES 150,000"
                ],
                key="sc_scale_agm"
            )
            sc_voting = st.selectbox(
                "Q2: Voting Resolution & Committee Election Engine (Pull-Down):*",
                [
                    "✋ Voice Vote & Statutory Quorum Floor Tracking — Included (KES 0)",
                    "⚖️ Weighted Voting Engine (Shares / Capital Bracket Weighting) — +KES 15,000",
                    "🗳️ Digital Secret Ballot & Committee Elections with Real-Time Tally Screen — +KES 25,000",
                    "📱 SMS OTP Multi-Factor Verification for Proxies & Remote Voting — +KES 20,000"
                ],
                key="sc_voting_agm"
            )
            sc_hw = st.selectbox(
                "Q3: Gate Usher Hardware & Access Station Mode (Pull-Down):*",
                [
                    "📲 Mobile BYOD Usher Mode (Ushers scan using any smartphone/tablet - Included) — KES 0",
                    "📟 STRIDE™ Rugged Barcode Gate Station Terminals (Pair Rental) — +KES 20,000",
                    "🖨️ Rapid Thermal Badge & Lanyard Printing Station — +KES 30,000"
                ],
                key="sc_hw_agm"
            )
            sc_audit = st.selectbox(
                "Q4: Statutory Compliance & Scrutineer Auditing (Pull-Down):*",
                [
                    "📄 Standard CSV Scrutineer & Company Secretary Export — Included (KES 0)",
                    "🔒 Certified Tamper-Evident SHA-256 Audit Pack (CMA / SASRA Regulatory Dossier) — +KES 15,000",
                    "👨‍💼 Dedicated On-Site STRIDE™ Certified Technical Marshal (1 Day Deployment) — +KES 25,000"
                ],
                key="sc_audit_agm"
            )

            # Calculation
            base_fee = 5000.0 if "Tier 1" in sc_scale else (35000.0 if "Tier 2" in sc_scale else (75000.0 if "Tier 3" in sc_scale else 150000.0))
            scale_tag = sc_scale.split("—")[0].strip()

            voting_fee = 0.0
            if "Weighted" in sc_voting: voting_fee = 15000.0
            elif "Digital Secret Ballot" in sc_voting: voting_fee = 25000.0
            elif "SMS OTP" in sc_voting: voting_fee = 20000.0
            voting_tag = sc_voting.split("—")[0].strip()

            hw_fee = 0.0
            if "Rugged" in sc_hw: hw_fee = 20000.0
            elif "Thermal Badge" in sc_hw: hw_fee = 30000.0
            hw_tag = sc_hw.split("—")[0].strip()

            audit_fee = 0.0
            if "SHA-256" in sc_audit: audit_fee = 15000.0
            elif "Marshal" in sc_audit: audit_fee = 25000.0
            audit_tag = sc_audit.split("—")[0].strip()

        else:
            sc_scale = st.selectbox(
                "Q1: Expected Participant / Athlete Scale (Pull-Down):*",
                [
                    "🏅 Tier 1: Club / Department Tournament (Up to 150 Participants) — KES 15,000",
                    "🏆 Tier 2: Corporate Inter-Bank / Industry Championship (151 – 750 Participants) — KES 45,000",
                    "🏃 Tier 3: Regional Marathon / Major Summit (751 – 3,000 Attendees) — KES 95,000",
                    "🌍 Tier 4: National / International Sporting Event (3,000+ Attendees) — KES 180,000"
                ],
                key="sc_scale_other"
            )
            sc_telemetry = st.selectbox(
                "Q2: Telemetry, Allowance Rules & Leaderboards (Pull-Down):*",
                [
                    "⏱️ Standard Check-In Attendance Tracking — Included (KES 0)",
                    "⏱️ Dual-Gate Duration Enforcement (Pre-sport + Post-sport allowance floor) — +KES 15,000",
                    "📊 Live Public Scoreboard & Discipline Leaderboards — +KES 20,000",
                    "🏅 Automated Digital Finisher Certificate / QR Medal Pass — +KES 15,000"
                ],
                key="sc_telemetry_other"
            )
            sc_hw = st.selectbox(
                "Q3: Hardware & Registration Station Kit (Pull-Down):*",
                [
                    "📲 Mobile BYOD Gate Marshalling — Included (KES 0)",
                    "🖨️ Thermal Athlete Bib & RFID/QR Badge Station — +KES 25,000",
                    "👨‍💼 Dedicated STRIDE™ Timekeeper & Gate Marshal — +KES 25,000"
                ],
                key="sc_hw_other"
            )

            # Calculation
            base_fee = 15000.0 if "Tier 1" in sc_scale else (45000.0 if "Tier 2" in sc_scale else (95000.0 if "Tier 3" in sc_scale else 180000.0))
            scale_tag = sc_scale.split("—")[0].strip()

            voting_fee = 0.0
            if "Dual-Gate" in sc_telemetry: voting_fee = 15000.0
            elif "Scoreboard" in sc_telemetry: voting_fee = 20000.0
            elif "Finisher" in sc_telemetry: voting_fee = 15000.0
            voting_tag = sc_telemetry.split("—")[0].strip()

            hw_fee = 0.0
            if "Thermal Athlete" in sc_hw: hw_fee = 25000.0
            elif "Timekeeper" in sc_hw: hw_fee = 25000.0
            hw_tag = sc_hw.split("—")[0].strip()

            audit_fee = 0.0
            audit_tag = "Standard Telemetry Export"

        subtotal = base_fee + voting_fee + hw_fee + audit_fee
        vat_amt = subtotal * 0.16
        grand_total = subtotal + vat_amt

        st.markdown("---")
        st.markdown("#### 3️⃣ Organizer Billing & Instant M-Pesa Settlement")
        b_org = st.text_input("Billing Entity / Organization Name:*", value=e_host if e_host else "Corporate Client", key="wz_b_org")
        b_email = st.text_input("Billing Email Address (for Official Tax Invoice):*", placeholder="finance@organization.co.ke", key="wz_b_email")
        b_phone = st.text_input("Safaricom M-Pesa Mobile Number for STK Push:*", value="0722123456", help="STK Push prompt will be dispatched to this handset", key="wz_b_phone")

        btn_pay_provision = st.button(
            f"💳 Settle KES {grand_total:,.0f} via M-Pesa STK & Launch Gateways",
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
                
                scoping_meta = f"{e_desc.strip()} [STRIDE Scope: Tier={scale_tag}, Voting={voting_tag}, HW={hw_tag}, Fee=KES {grand_total:,.0f}, Inv={inv_ref}, M-Pesa={mpesa_ref}]"
                
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
        
        # Display Live Scope Quotation Card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(8, 28, 58, 0.95) 0%, rgba(4, 14, 30, 0.98) 100%); border: 2px solid #F5C542; border-radius: 14px; padding: 18px 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(245, 197, 66, 0.25); padding-bottom: 8px;">
                <span style="color: #F5C542; font-weight: 900; font-size: 0.82rem; letter-spacing: 1.2px; text-transform: uppercase;">
                    STRIDE™ SCOPE QUOTATION
                </span>
                <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #34D399; font-size: 0.72rem; padding: 2px 8px; border-radius: 4px; font-weight: 800;">
                    LIVE PRO-FORMA
                </span>
            </div>
            
            <div style="margin: 12px 0 6px 0; font-size: 0.8rem; color: #CBD5E1;">
                <table style="width: 100%; border-collapse: collapse; line-height: 1.8;">
                    <tr>
                        <td style="color: #94A3B8;">Base Scale License:</td>
                        <td style="text-align: right; font-weight: 700; color: #FFFFFF;">KES {base_fee:,.0f}</td>
                    </tr>
                    <tr>
                        <td style="color: #94A3B8;">Governance / Telemetry:</td>
                        <td style="text-align: right; font-weight: 700; color: #FFFFFF;">KES {voting_fee:,.0f}</td>
                    </tr>
                    <tr>
                        <td style="color: #94A3B8;">Gate Hardware & Access:</td>
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
        """, unsafe_allow_html=True)

        if cur_inv:
            st.markdown(f"""
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
            """, unsafe_allow_html=True)

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
2. Governance Engine ({cur_inv['voting_tag']}): KES {cur_inv['voting_fee']:,.2f}
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

        st.markdown(f"""
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
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("##### 📊 Live Published Events Directory")
        ev_list = backend.get_events(status="ALL")
        if ev_list:
            df_ev_display = pd.DataFrame(ev_list)[["event_id", "title", "category", "event_date", "venue", "standard_price", "status"]]
            st.dataframe(df_ev_display, use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 3: GATE USHER SCANNER & ACCREDITATION ROSTER
# ==============================================================================
with tab_verify:
    st.markdown("### 📷 Gate Usher Entrance Scanner & Live Roster")
    st.caption("Venue ushers, security coordinators, and AGM scrutinizers: enter an attendee's Ticket ID or simulate scanning their QR code to verify admission, validate proxies, and track statutory quorum:")

    v_col1, v_col2 = st.columns([1.1, 1.4])

    with v_col1:
        st.markdown("#### 🔍 Gate Scanner Simulator")
        test_tkt_id = st.text_input("Enter Ticket ID to Verify:*", value="TKT-849201-11", placeholder="e.g. TKT-849201-11", key="input_gate_verify_tkt")
        
        btn_admit_gate = st.button("✅ Admit Attendee / Delegate at Gate", type="primary", use_container_width=True)

        if btn_admit_gate:
            if not test_tkt_id.strip() or test_tkt_id.strip() == "TKT-":
                st.error("Please provide a valid Ticket ID.")
            else:
                ok_adm, msg_adm, adm_ticket = backend.verify_and_admit_ticket(test_tkt_id.strip())
                if ok_adm:
                    st.success(msg_adm)
                    st.balloons()
                else:
                    st.error(msg_adm)

        st.markdown("---")
        st.caption("💡 **Quick Test Tickets:** You can copy any Ticket ID from the accredited roster on the right and test admission.")

    with v_col2:
        st.markdown("#### 📋 Live Event Accredited Roster")
        v_evt_choice = st.selectbox(
            "Filter Roster by Event / Assembly (Pull-Down):",
            [e["event_id"] + " — " + e["title"] for e in all_events] if all_events else ["None"],
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

# ------------------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------------------
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 1.4rem; border-top: 1px solid rgba(245, 197, 66, 0.25); color: #94A3B8; font-size: 0.82rem; background: rgba(4, 16, 33, 0.6); border-radius: 12px;">
    <strong style="color: #F5C542;">STRIDE™</strong> • Enterprise Event Telemetry, Accreditation & M-Pesa Ticketing Platform<br>
    <span style="font-size: 0.75rem; color: #64748B;">Multi-Tenant Commercial Event Management & Gate Control • <a href="/DEMO" style="color: #F5C542; text-decoration: none;">🧪 Evaluator Sandbox</a></span>
</div>
""", unsafe_allow_html=True)

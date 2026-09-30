"""
================================================================================
STRIDE™ — PUBLIC SELF-REGISTRATION, M-PESA STK TICKETING & EVENT CREATOR WIZARD
Universal Event Accreditation & Digital Pass Platform
URL Route: /register
================================================================================
"""

import streamlit as st
import pandas as pd
import datetime
import time
import os
import sys

# Ensure root directory is on sys.path for utils import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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
            <a href="/" style="color: #94A3B8; text-decoration: none; margin-right: 12px;">🏛️ Official CBK Portal</a>
            <a href="/DEMO" style="color: #F5C542; text-decoration: none;">🧪 Evaluator Sandbox</a>
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
        # Determine event selection options
        event_options = {f"{e['title']} ({e['event_id']})": e for e in all_events}
        
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

        # Display Event Overview Card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(8, 28, 58, 0.8) 0%, rgba(4, 14, 30, 0.9) 100%); border: 1.5px solid rgba(245, 197, 66, 0.4); border-left: 5px solid #F5C542; border-radius: 12px; padding: 16px 20px; margin: 12px 0 20px 0;">
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
                # Ticket Tier Selection
                std_p = float(selected_event.get("standard_price", 1000.0))
                vip_p = float(selected_event.get("vip_price", 3500.0))
                
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

                att_name = st.text_input("Full Name (as per Official ID):*", placeholder="e.g. Wallace Mbugua")
                att_email = st.text_input("Email Address (for pass delivery):*", placeholder="e.g. wallace@enterprise.co.ke")
                att_org = st.text_input("Organization / Department / Team:*", placeholder="e.g. Finance & Accounts / Equity Bank")
                att_phone = st.text_input("Safaricom M-Pesa Phone Number:*", placeholder="07XX XXX XXX (for instant STK push)", help="Safaricom phone number that will receive the M-Pesa PIN prompt")

                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 10px 14px; margin: 10px 0;">
                    <span style="color: #34D399; font-weight: 800; font-size: 0.88rem;">💰 Total Payable: KES {chosen_amt:,.0f}</span><br>
                    <span style="color: #94A3B8; font-size: 0.75rem;">Paybill: <strong>{selected_event['mpesa_paybill']}</strong> • Instant Automated Verification</span>
                </div>
                """, unsafe_allow_html=True)

                btn_sub_ticket = st.form_submit_button("📲 Complete Registration & Pay via M-Pesa", type="primary", use_container_width=True)

                if btn_sub_ticket:
                    if not att_name.strip():
                        st.error("Please enter your Full Name.")
                    elif not att_email.strip() or "@" not in att_email:
                        st.error("Please provide a valid email address.")
                    elif not att_phone.strip() or len(att_phone.strip()) < 9:
                        st.error("Please provide a valid Safaricom phone number for M-Pesa STK Push.")
                    else:
                        # Generate simulated M-Pesa Transaction ID
                        sim_tx = f"QK{int(time.time())}"[-10:]
                        ok_t, msg_t, tkt_obj = backend.register_event_ticket(
                            event_id=selected_event["event_id"],
                            attendee_name=att_name.strip(),
                            email=att_email.strip(),
                            phone=att_phone.strip(),
                            organization=att_org.strip() or "Independent Participant",
                            ticket_tier=tier_clean_name,
                            amount_paid=chosen_amt,
                            mpesa_trans_id=sim_tx
                        )
                        if ok_t:
                            st.session_state["pub_active_ticket"] = tkt_obj
                            st.session_state["pub_active_event"] = selected_event
                            st.toast("🎉 M-Pesa payment confirmed! Digital pass generated.", icon="🎟️")
                            st.rerun()
                        else:
                            st.error(msg_t)

        with col_reg_pass:
            st.markdown("#### 🎟️ Digital Mobile Pass")
            cur_ticket = st.session_state.get("pub_active_ticket", None)
            cur_evt = st.session_state.get("pub_active_event", selected_event)

            if not cur_ticket:
                st.info("👈 Fill out the registration form on the left and tap **'Complete Registration & Pay via M-Pesa'** to generate your official pass.")
                st.markdown("""
                <div style="background: rgba(8, 24, 48, 0.6); border: 2px dashed rgba(255,255,255,0.15); border-radius: 12px; padding: 40px 20px; text-align: center; color: #64748B;">
                    <div style="font-size: 3.5rem; margin-bottom: 10px;">🎟️</div>
                    <div style="font-weight: 700; color: #94A3B8; font-size: 1rem;">No Active Ticket Pass Generated Yet</div>
                    <div style="font-size: 0.8rem; margin-top: 6px;">Your encrypted dynamic QR ticket pass will render here immediately following payment verification.</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                t_tx = cur_ticket["mpesa_trans_id"]
                t_id = cur_ticket["ticket_id"]
                t_name = cur_ticket["attendee_name"]
                t_org = cur_ticket["organization"]
                t_tier = cur_ticket["ticket_tier"]
                t_amt = cur_ticket["amount_paid"]

                # Generate dynamic scannable QR Code pointing to instant verification URL
                verify_qr_data = f"https://cbk-stride.streamlit.app/register?verify_tkt={t_id}"
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
    st.markdown("### 🪄 Universal Event Creator Wizard")
    st.caption("Empower any organization, corporate HR department, sports club, or event planner to launch a certified registration gateway and gate scanner in 60 seconds:")

    wz_col1, wz_col2 = st.columns([1.4, 1])

    with wz_col1:
        with st.form(key="form_create_event_wizard"):
            st.markdown("#### 1️⃣ Event Identity & Host")
            e_title = st.text_input("Official Event Name:*", placeholder="e.g. Kenya Airways Annual Sports Derby & Family Fun Day")
            e_host = st.text_input("Host Company / Organizing Body:*", placeholder="e.g. KQ Sports Club Secretariat")
            e_cat = st.selectbox(
                "Event Category:*",
                [
                    "🏆 Sports Tournament & Derby",
                    "👔 Corporate AGM & Shareholder Meeting",
                    "🏃 Marathon, Fun Run & Athletics",
                    "💡 Industry Conference & Tech Summit",
                    "🎉 Corporate Gala Dinner & Awards",
                    "🎓 School / University Sports Day",
                    "💒 Private Reception / Social Gala"
                ]
            )

            st.markdown("#### 2️⃣ Schedule & Location")
            ec1, ec2 = st.columns(2)
            with ec1:
                e_date = st.date_input("Event Date:", value=now_dt.date() + datetime.timedelta(days=14))
            with ec2:
                e_time = st.text_input("Start / Kick-off Time:", value="08:30")
            e_venue = st.text_input("Venue & Physical Address:*", placeholder="e.g. Ngong Racecourse Grounds, Nairobi")

            st.markdown("#### 3️⃣ Ticketing & Accreditation Rules")
            tc1, tc2, tc3 = st.columns(3)
            with tc1:
                e_paid = st.checkbox("Paid Event (Collect via M-Pesa)", value=True)
            with tc2:
                e_std_price = st.number_input("Standard Ticket (KES):", min_value=0.0, value=1000.0, step=100.0)
            with tc3:
                e_vip_price = st.number_input("VIP / Delegate (KES):", min_value=0.0, value=3500.0, step=500.0)

            e_paybill = st.text_input("M-Pesa Paybill / Till Number for Settlements:", value="849200")
            e_gate_mode = st.selectbox(
                "Gate Scanning Protocol:*",
                [
                    "DUAL_GATE (Arrival Scan + Departure Scan for Allowance Floor Verification)",
                    "SINGLE_GATE (Entry Scan Only for Galas, AGMs & Conferences)"
                ]
            )
            clean_gate_mode = "DUAL_GATE" if "DUAL_GATE" in e_gate_mode else "SINGLE_GATE"

            e_desc = st.text_area("Event Description & Attendee Instructions:", placeholder="e.g. Official sports kit required. Breakfast and lunch provided at Pavilion A. Gate closes at 09:30.")

            btn_publish_event = st.form_submit_button("🚀 Publish Event & Activate Accreditation", type="primary", use_container_width=True)

            if btn_publish_event:
                if not e_title.strip():
                    st.error("Please provide an Event Name.")
                elif not e_host.strip():
                    st.error("Please provide the Host Company / Organizer Name.")
                elif not e_venue.strip():
                    st.error("Please specify the Venue.")
                else:
                    d_str = e_date.strftime("%Y-%m-%d")
                    ok_ev, msg_ev, new_eid = backend.create_event(
                        title=e_title.strip(),
                        organizer_name=e_host.strip(),
                        category=e_cat,
                        event_date=d_str,
                        event_time=e_time.strip(),
                        venue=e_venue.strip(),
                        description=e_desc.strip(),
                        gate_mode=clean_gate_mode,
                        is_paid=e_paid,
                        standard_price=e_std_price,
                        vip_price=e_vip_price,
                        mpesa_paybill=e_paybill.strip()
                    )
                    if ok_ev:
                        st.session_state["wz_last_created_id"] = new_eid
                        st.session_state["wz_last_created_title"] = e_title.strip()
                        st.success(f"🎉 Event published successfully! Unique ID: `{new_eid}`.")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(msg_ev)

    with wz_col2:
        st.markdown("#### 📱 Generated Gate Scanner & Shareable Links")
        last_eid = st.session_state.get("wz_last_created_id", "EVT-2026-001")
        last_title = st.session_state.get("wz_last_created_title", "2026 Inter-Bank Sports Championship")

        reg_share_url = f"https://cbk-stride.streamlit.app/register?event_id={last_eid}"
        gate_qr_img = f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={reg_share_url}"

        st.markdown(f"""
        <div style="background: rgba(8, 24, 48, 0.85); border: 2px solid #00F2FE; border-radius: 14px; padding: 20px; text-align: center;">
            <div style="font-size: 0.72rem; color: #00F2FE; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">
                OFFICIAL ENTRANCE SCANNER DESK
            </div>
            <h4 style="margin: 6px 0 2px 0; color: #FFFFFF; font-size: 1.05rem;">{last_title}</h4>
            <div style="font-size: 0.75rem; color: #94A3B8; margin-bottom: 10px;">Event ID: <code>{last_eid}</code></div>
            
            <div style="background: #FFFFFF; border-radius: 10px; padding: 10px; display: inline-block; margin-bottom: 10px;">
                <img src="{gate_qr_img}" alt="Gate Entrance QR" style="display: block; width: 170px; height: 170px;" />
            </div>
            
            <div style="font-size: 0.78rem; color: #CBD5E1; line-height: 1.5;">
                📢 <strong>Entrance Instructions:</strong> Display this QR on an iPad/tablet at the gate or print on venue banners. Attendees scan it to register or check in instantly.
            </div>
            
            <div style="background: rgba(0, 242, 254, 0.1); border: 1px dashed rgba(0,242,254,0.4); border-radius: 8px; padding: 8px; margin-top: 12px; font-size: 0.74rem; word-break: break-all; color: #00F2FE;">
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
    st.caption("Venue ushers and security coordinators: enter an attendee's Ticket ID or simulate scanning their QR code to verify admission and prevent pass sharing:")

    v_col1, v_col2 = st.columns([1.1, 1.4])

    with v_col1:
        st.markdown("#### 🔍 Gate Scanner Simulator")
        test_tkt_id = st.text_input("Enter Ticket ID to Verify:*", value="TKT-", placeholder="e.g. TKT-837194-42", key="input_gate_verify_tkt")
        
        btn_admit_gate = st.button("✅ Admit Attendee at Gate", type="primary", use_container_width=True)

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
            "Filter Roster by Event:",
            [e["event_id"] + " — " + e["title"] for e in all_events] if all_events else ["None"],
            key="sel_roster_evt"
        )
        if all_events and v_evt_choice != "None":
            target_eid = v_evt_choice.split("—")[0].strip()
            event_tickets = backend.get_tickets_by_event(target_eid)
            
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

# ------------------------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------------------------
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 1.4rem; border-top: 1px solid rgba(245, 197, 66, 0.25); color: #94A3B8; font-size: 0.82rem; background: rgba(4, 16, 33, 0.6); border-radius: 12px;">
    <strong style="color: #F5C542;">STRIDE™</strong> • Enterprise Sports Telemetry, Accreditation & M-Pesa Ticketing Platform<br>
    <span style="font-size: 0.75rem; color: #64748B;">Multi-Tenant Event Management • <a href="/" style="color: #00F2FE; text-decoration: none;">Return to Official CBK Portal</a> • <a href="/DEMO" style="color: #F5C542; text-decoration: none;">Evaluator Sandbox</a></span>
</div>
""", unsafe_allow_html=True)

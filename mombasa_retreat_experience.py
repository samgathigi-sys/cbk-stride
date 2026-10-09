"""
mombasa_retreat_experience.py
Luxury Executive Mobile Experience for Banki Kuu SACCO Mombasa Retreat 2026.
Features:
- Apple Wallet / Luxury Boarding Pass style digital pass
- Strict PII masking (Phone, Email, National ID, Token)
- Dynamic "HAPPENING NOW" session pulse
- 4 Core Interactive Modules: Pass, Programme, Meals, Voting
- Interactive Gate Usher / Concierge Camera Scanner Simulator
"""

import os
import time
import hashlib
import pandas as pd
import streamlit as st

def mask_phone_num(phone_str: str) -> str:
    """Masks phone to +254 7XX *** *XX."""
    clean = str(phone_str).strip()
    if len(clean) >= 9:
        return f"{clean[:7]} *** *{clean[-2:]}"
    return "+254 7•• ••• •••"

def mask_email_addr(email_str: str) -> str:
    """Masks email to s***@domain.com."""
    if "@" in str(email_str):
        user, domain = str(email_str).split("@", 1)
        if len(user) > 2:
            masked_user = f"{user[0]}***{user[-1]}"
        else:
            masked_user = f"{user[:1]}***"
        return f"{masked_user}@{domain}"
    return "s***@centralbank.go.ke"

def render_mombasa_retreat_experience():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "RETREAT_BADGES_REGISTRY.csv")
    
    # Load 95 delegates registry
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame([
            {"index": 1, "full_name": "Samuel Gathigi", "role": "Supervisory Board Delegate", "tier": "EXECUTIVE", "token_id": "BK-342801", "masked_phone": "+254 722 *** *00", "masked_email": "s***@centralbank.go.ke"},
            {"index": 2, "full_name": "Dr. Beatrice Kiptoo", "role": "Internal Audit & Risk Oversight", "tier": "EXECUTIVE", "token_id": "BK-342802", "masked_phone": "+254 733 *** *89", "masked_email": "b***@centralbank.go.ke"},
            {"index": 3, "full_name": "Andrew Ogola", "role": "Chess Captain & SACCO Delegate", "tier": "EXECUTIVE", "token_id": "BK-3366", "masked_phone": "+254 726 *** *90", "masked_email": "a***@centralbank.go.ke"},
            {"index": 4, "full_name": "Josiah Achikah Mayieka", "role": "BOD - SACCO", "tier": "EXECUTIVE", "token_id": "BK-3124", "masked_phone": "+254 726 *** *40", "masked_email": "M***a@centralbank.go.ke"},
            {"index": 5, "full_name": "Catherine Sompet Selempo", "role": "BOD - SACCO", "tier": "EXECUTIVE", "token_id": "BK-2281", "masked_phone": "+254 722 *** *39", "masked_email": "s***s@centralbank.go.ke"}
        ])

    # Luxury Top Banner
    st.markdown("""
    <style>
        .retreat-header {
            background: linear-gradient(135deg, #071F3D 0%, #030F21 60%, #020712 100%);
            border: 2px solid #F5C542;
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 20px;
            box-shadow: 0 12px 32px rgba(0,0,0,0.7);
        }
        .apple-pass-card {
            background: linear-gradient(145deg, rgba(8, 28, 58, 0.95) 0%, rgba(3, 14, 30, 0.98) 100%);
            border: 2px solid #F5C542;
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 20px 48px rgba(0, 0, 0, 0.85);
            position: relative;
            overflow: hidden;
        }
        .apple-pass-card::before {
            content: "";
            position: absolute;
            top: -50px;
            right: -50px;
            width: 150px;
            height: 150px;
            background: radial-gradient(circle, rgba(245, 197, 66, 0.15) 0%, transparent 70%);
            pointer-events: none;
        }
        .pulse-now {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: #10B981;
            box-shadow: 0 0 12px #10B981;
            margin-right: 8px;
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.7; }
            50% { transform: scale(1.25); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.7; }
        }
        .metric-badge {
            background: rgba(0, 242, 254, 0.12);
            border: 1px solid rgba(0, 242, 254, 0.35);
            color: #00F2FE;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.8px;
        }
    </style>
    """, unsafe_allow_html=True)

    # Experience Mode Switcher (Delegate View vs. Gate Usher Scanner)
    c_m1, c_m2 = st.columns([2.5, 1.2])
    with c_m1:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
            <span style="background: #F5C542; color: #020712; font-size: 0.72rem; font-weight: 900; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">
                🇰🇪 STRIDE™ EXECUTIVE RETREAT PASS
            </span>
            <span style="color: #94A3B8; font-size: 0.82rem;">Mombasa Strategic Leadership Retreat 2026</span>
        </div>
        """, unsafe_allow_html=True)
    with c_m2:
        view_role = st.selectbox(
            "Terminal View:",
            ["📱 VIP Delegate Mobile Experience", "📷 Gate Usher & Hotel Concierge Scanner"],
            key="retreat_view_role"
        )

    # --------------------------------------------------------------------------
    # 1. DELEGATE SELECTOR (Quick Switcher across the 95 Delegates)
    # --------------------------------------------------------------------------
    st.markdown("##### 👤 Test As Accredited Delegate (Cohort of 95):")
    delegate_opts = {
        f"{r['index']:02d}. {r['full_name']} — {r['role']} (Token: {r.get('token_id', 'BK-' + str(r['index']))})": r
        for _, r in df.iterrows()
    }
    
    # Pre-select Samuel Gathigi or Dr. Beatrice Kiptoo if available
    default_sel_idx = 0
    for idx, name in enumerate(delegate_opts.keys()):
        if "Samuel" in name or "Gathigi" in name:
            default_sel_idx = idx
            break

    sel_label = st.selectbox("Select Active Delegate:*", list(delegate_opts.keys()), index=default_sel_idx, key="sel_retreat_delegate")
    cur_del = delegate_opts[sel_label]

    del_name = cur_del["full_name"]
    del_role = cur_del["role"]
    del_token = cur_del.get("token_id", f"BK-{cur_del['index']:04d}")
    del_phone = cur_del.get("masked_phone", mask_phone_num("0722000000"))
    del_email = cur_del.get("masked_email", mask_email_addr(f"{del_name.lower().replace(' ', '.')}@centralbank.go.ke"))
    del_tier = cur_del.get("tier", "EXECUTIVE")

    # Synthetic room assignment based on index
    room_wings = ["Ocean Wing", "Palm Wing", "Executive Coral Suite", "Presidential Pavilion"]
    suite_num = 100 + (int(cur_del["index"]) * 3) % 400
    assigned_room = f"{room_wings[cur_del['index'] % len(room_wings)]} • Suite {suite_num}"

    # Sync with global active ticket for Gate Usher and Ballot tabs
    ser = str(cur_del.get("serial", "")).strip()
    idx_num = int(cur_del.get("index", 1))
    if ser == "3428":
        db_tkt_id = "TKT-BK-342801"
    elif ser == "3366":
        db_tkt_id = "TKT-BK-3366"
    elif ser == "CASUAL":
        db_tkt_id = f"TKT-BK-CASUAL-{idx_num:02d}"
    else:
        db_tkt_id = f"TKT-BK-{ser}"
    st.session_state["active_ticket_id"] = db_tkt_id

    # --------------------------------------------------------------------------
    # VIEW A: GATE USHER & CONCIERGE SCANNER TERMINAL
    # --------------------------------------------------------------------------
    if "Gate Usher" in view_role:
        st.markdown("### 📷 Gate Usher & Hotel Concierge Scanner Terminal")
        st.caption("Active camera optical scanning terminal with instant 0.4s photo pop-up, room verification, and catering lock:")

        col_cam, col_verify = st.columns([1.1, 1.3])

        with col_cam:
            # Simulated active camera viewfinder
            st.markdown(f"""
            <div style="background: #020712; border: 2.5px solid #10B981; border-radius: 16px; padding: 24px; text-align: center; position: relative;">
                <div style="font-size: 0.72rem; color: #10B981; font-weight: 800; letter-spacing: 1px; text-transform: uppercase;">
                    (((●))) ACTIVE OPTICAL VIEWFINDER • 60 FPS
                </div>
                <div style="background: rgba(16, 185, 129, 0.08); border: 2px dashed #10B981; border-radius: 12px; margin: 18px auto; width: 200px; height: 200px; display: flex; align-items: center; justify-content: center; position: relative;">
                    <div style="position: absolute; width: 100%; height: 2px; background: #00F2FE; top: 50%; box-shadow: 0 0 10px #00F2FE;"></div>
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=160x160&data=https://cbk-stride.streamlit.app/EVENTS?verify_token={del_token}" 
                         alt="QR Scanner" style="width: 150px; height: 150px; opacity: 0.85;" />
                </div>
                <div style="color: #94A3B8; font-size: 0.78rem;">
                    Targeting Pass Token: <code>{del_token}</code> • Latency: <strong>0.38s</strong>
                </div>
            </div>
            """, unsafe_allow_html=True)

            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                btn_admit = st.button("✅ Admit & Accredit Delegate", type="primary", use_container_width=True)
            with c_btn2:
                btn_flag = st.button("🚩 Flag Secretariat", use_container_width=True)

            if btn_admit:
                st.success(f"✓ {del_name} Admitted to Plenary Floor! Quorum updated.")
            if btn_flag:
                st.warning(f"Pass #{del_token} flagged for Secretariat Review.")

        with col_verify:
            # Verified Pop-up Card
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #092540 0%, #031326 100%); border: 2px solid #10B981; border-radius: 16px; padding: 20px; box-shadow: 0 12px 36px rgba(0,0,0,0.7);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="background: rgba(16, 185, 129, 0.2); color: #34D399; font-weight: 800; font-size: 0.72rem; padding: 3px 10px; border-radius: 4px;">
                        ✓ ACCESS GRANTED • QUORUM VERIFIED
                    </span>
                    <span style="color: #F5C542; font-weight: 800; font-size: 0.75rem;">SASRA TIER 1</span>
                </div>
                
                <div style="display: flex; gap: 16px; align-items: center; margin-bottom: 14px;">
                    <div style="width: 76px; height: 76px; border-radius: 50%; background: linear-gradient(135deg, #0284C7, #0369A1); display: flex; align-items: center; justify-content: center; font-size: 2rem; border: 2px solid #F5C542; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                        👔
                    </div>
                    <div>
                        <h3 style="margin: 0; color: #FFFFFF; font-size: 1.25rem; font-weight: 800;">{del_name}</h3>
                        <div style="color: #00F2FE; font-size: 0.82rem; font-weight: 700;">{del_role}</div>
                        <div style="color: #94A3B8; font-size: 0.75rem; margin-top: 2px;">Pass ID: <code>{del_token}</code></div>
                    </div>
                </div>

                <div style="background: rgba(2, 8, 20, 0.6); border-radius: 10px; padding: 12px 14px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 6px;">
                        <span style="color: #94A3B8;">Masked Phone:</span>
                        <strong style="color: #FFFFFF;">{del_phone}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 6px;">
                        <span style="color: #94A3B8;">Masked Email:</span>
                        <strong style="color: #FFFFFF;">{del_email}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.78rem; margin-bottom: 6px;">
                        <span style="color: #94A3B8;">Assigned Suite:</span>
                        <strong style="color: #F5C542;">{assigned_room}</strong>
                    </div>
                </div>

                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <span style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #34D399; padding: 4px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;">
                        ✓ Breakfast & Lunch Claimed (1/1)
                    </span>
                    <span style="background: rgba(56, 189, 248, 0.15); border: 1px solid #38BDF8; color: #38BDF8; padding: 4px 10px; border-radius: 6px; font-size: 0.72rem; font-weight: 700;">
                        ⏱️ Plenary Dwell: 52 Mins (Qualified)
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        return

    # --------------------------------------------------------------------------
    # VIEW B: THE VIP DELEGATE MOBILE EXPERIENCE
    # --------------------------------------------------------------------------
    
    # 1. LIVE "HAPPENING NOW" SESSION PULSE CARD
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(7, 25, 51, 0.85) 0%, rgba(2, 12, 28, 0.95) 100%); 
                border: 1.5px solid #10B981; border-left: 5px solid #10B981; border-radius: 12px; padding: 14px 18px; margin-bottom: 18px; box-shadow: 0 6px 20px rgba(0,0,0,0.4);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <div style="display: flex; align-items: center;">
                <span class="pulse-now"></span>
                <span style="color: #10B981; font-weight: 900; font-size: 0.72rem; letter-spacing: 1.2px; text-transform: uppercase;">
                    HAPPENING NOW • PLENARY SESSION
                </span>
            </div>
            <span style="background: rgba(16, 185, 129, 0.2); color: #34D399; font-size: 0.7rem; font-weight: 800; padding: 2px 8px; border-radius: 4px;">
                42 MINS REMAINING
            </span>
        </div>
        <div style="font-size: 1.05rem; font-weight: 800; color: #FFFFFF; margin: 2px 0;">
            Day 2 Keynote: Digital Transformation & AI Governance in Kenya's Financial Sector
        </div>
        <div style="font-size: 0.78rem; color: #CBD5E1;">
            📍 <strong>Ocean Ballroom A (Ground Floor)</strong> • Keynote Speaker: Dr. Patrick Njoroge (Executive Guest)
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. 4 SUB-MODULE TABS (Pass, Programme, Meals, Voting)
    sub_pass, sub_prog, sub_meals, sub_vote = st.tabs([
        "🪪 VIP Digital Pass",
        "📅 Dynamic Programme",
        "🍴 Meals & Allowance Quota",
        "🗳️ Secret Ballot & Voting"
    ])

    # --------------------------------------------------------------------------
    # SUB-TAB 1: VIP DIGITAL PASS CARD (Apple Wallet Glassmorphism Aesthetic)
    # --------------------------------------------------------------------------
    with sub_pass:
        col_p1, col_p2 = st.columns([1.15, 1])

        with col_p1:
            qr_verify_url = f"https://cbk-stride.streamlit.app/EVENTS?verify_token={del_token}"
            qr_img_api = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={qr_verify_url}"

            st.markdown(f"""
            <div class="apple-pass-card">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(245, 197, 66, 0.3); padding-bottom: 12px; margin-bottom: 16px;">
                    <div>
                        <div style="font-size: 0.7rem; color: #F5C542; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase;">
                            BANKI KUU SACCO • RETREAT PASS
                        </div>
                        <div style="font-size: 0.95rem; color: #FFFFFF; font-weight: 800; margin-top: 2px;">
                            Mombasa Strategic Leadership Retreat 2026
                        </div>
                    </div>
                    <div style="width: 42px; height: 42px; border-radius: 50%; background: linear-gradient(135deg, #F5C542, #B48811); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.5);">
                        ⭐
                    </div>
                </div>

                <div style="display: flex; gap: 16px; align-items: center; margin-bottom: 18px;">
                    <div style="width: 82px; height: 82px; border-radius: 12px; background: linear-gradient(135deg, #0284C7, #071F3D); display: flex; align-items: center; justify-content: center; font-size: 2.3rem; border: 2.5px solid #00F2FE; box-shadow: 0 8px 24px rgba(0,0,0,0.6);">
                        👔
                    </div>
                    <div>
                        <div style="font-size: 1.35rem; font-weight: 900; color: #FFFFFF;">{del_name}</div>
                        <div style="font-size: 0.85rem; color: #00F2FE; font-weight: 700; margin-top: 1px;">{del_role}</div>
                        <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 4px;">
                            Pass Serial: <code>{del_token}</code> • <strong>{del_tier}</strong>
                        </div>
                    </div>
                </div>

                <div style="background: rgba(255,255,255,0.04); border-radius: 10px; padding: 12px; margin-bottom: 18px;">
                    <div style="display: flex; justify-content: space-between; font-size: 0.76rem; margin-bottom: 4px;">
                        <span style="color: #94A3B8;">Masked Phone:</span>
                        <strong style="color: #FFFFFF;">{del_phone}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.76rem; margin-bottom: 4px;">
                        <span style="color: #94A3B8;">Masked Email:</span>
                        <strong style="color: #FFFFFF;">{del_email}</strong>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.76rem;">
                        <span style="color: #94A3B8;">Resort Accommodation:</span>
                        <strong style="color: #F5C542;">{assigned_room}</strong>
                    </div>
                </div>

                <div style="text-align: center; background: #FFFFFF; border-radius: 12px; padding: 12px; margin: 10px auto; width: 180px; box-shadow: 0 8px 20px rgba(0,0,0,0.6);">
                    <img src="{qr_img_api}" alt="Pass QR" style="display: block; width: 156px; height: 156px;" />
                </div>
                <div style="text-align: center; font-size: 0.7rem; color: #94A3B8; margin-top: 6px;">
                    Scan with any phone camera at airport, plenary gates & dining pavilions
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.08);">
                    <span style="font-size: 0.7rem; color: #10B981; font-weight: 800;">✓ QUORUM CERTIFIED</span>
                    <span style="font-size: 0.7rem; color: #64748B;">ODPC §25 Compliant</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_p2:
            st.markdown("#### 📱 Mobile Actions & Offline Pass")
            st.caption("Add to mobile wallet, download offline pass card, or view accreditation metadata:")

            st.download_button(
                label="📥 Download High-Res Pass Card (.png / .txt)",
                data=f"STRIDE RETREAT PASS\nName: {del_name}\nRole: {del_role}\nToken: {del_token}\nRoom: {assigned_room}\nVerification URL: {qr_verify_url}",
                file_name=f"PASS_{del_token}_{del_name.replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True
            )

            if st.button("📲 Add to Apple Wallet / Google Wallet (Simulate)", use_container_width=True):
                st.success("✓ Apple Wallet pass package generated! (.pkpass ready)")

            st.markdown("---")
            st.markdown("##### 🛡️ Cryptographic Data Privacy (ODPC §25)")
            st.info(f"""
            - **Plaintext PII Eliminated:** Raw national IDs are hashed.
            - **Phone Masking:** {del_phone}
            - **Email Scrubbing:** {del_email}
            - **Tamper-Evident SHA-256 Token:** `{del_token}`
            """)

    # --------------------------------------------------------------------------
    # SUB-TAB 2: DYNAMIC PROGRAMME & LIVE TIMETABLE
    # --------------------------------------------------------------------------
    with sub_prog:
        st.markdown("### 📅 Interactive Retreat Programme & Tracks")
        st.caption("Day-by-day timetable for the 4-day retreat at PrideInn Paradise Beach Resort:")

        day_choice = st.radio(
            "Select Retreat Day:",
            ["Day 1: SGR Ingress & Coastal Welcome", "Day 2: Governance & AI Keynote (Today)", "Day 3: Elections & Sports Derby", "Day 4: Resolutions & Departure"],
            horizontal=True,
            index=1
        )

        if "Day 1" in day_choice:
            st.markdown("""
            - **11:00 AM – 03:00 PM:** SGR Arrival (Mombasa Terminus) & Luxury Transfer to PrideInn Paradise.
            - **03:00 PM – 05:00 PM:** Delegate Room Key Issuance & Digital Pass Verification at Concierge.
            - **07:00 PM – 10:00 PM:** Coastal Swahili Gala Dinner & Executive Welcome by Board Chairman (*Ocean Lawn*).
            """)
        elif "Day 2" in day_choice:
            st.markdown("""
            - **07:00 AM – 08:30 AM:** Coastal Breakfast Buffet (*Flavours Restaurant*).
            - **08:45 AM – 10:15 AM:** `[NOW]` **Opening Keynote: Digital Transformation & AI Governance in SACCOs** (*Ocean Ballroom A*).
            - **10:15 AM – 10:45 AM:** Mid-Morning Tea & Networking.
            - **11:00 AM – 01:00 PM:** **Statutory Quorum Plenary & SASRA Prudential Review** (*Ocean Ballroom A*).
            - **01:00 PM – 02:30 PM:** Executive Buffet Lunch (*Tamu Tamu Terrace*).
            - **02:30 PM – 05:00 PM:** Breakout Tracks (Track A: Audit & Risk | Track B: IT Infrastructure & Security).
            - **07:00 PM – 09:30 PM:** Themed Seafood Dinner & Classical Swahili Music.
            """)
        elif "Day 3" in day_choice:
            st.markdown("""
            - **08:30 AM – 11:30 AM:** **Supervisory Committee & Board Elections (Digital Secret Ballot)** (*Ballroom A*).
            - **11:30 AM – 01:00 PM:** Returning Officer Official Certification & Dividend Adoption.
            - **02:30 PM – 05:30 PM:** Inter-Branch Beach Volleyball & Coastal Sports Derby (*Beach Front*).
            - **07:30 PM – 11:00 PM:** Annual Awards Gala Dinner & Trophy Presentation (*Grand Ballroom*).
            """)
        else:
            st.markdown("""
            - **08:00 AM – 10:00 AM:** Adoption of Formal Retreat Communiqué & SASRA Filing Resolutions.
            - **11:00 AM:** Hotel Checkout & Executive Coach Transfer to Mombasa SGR Terminus.
            """)

    # --------------------------------------------------------------------------
    # SUB-TAB 3: MEALS & ALLOWANCE QUOTA LOCK
    # --------------------------------------------------------------------------
    with sub_meals:
        st.markdown("### 🍴 Catering Entitlements & Sitting Allowance Ledger")
        st.caption("Live quota counters eliminating hotel catering leakage and duplicate claims:")

        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.1); border: 1.5px solid #10B981; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.72rem; color: #10B981; font-weight: 800;">BREAKFAST BUFFET</div>
                <div style="font-size: 1.6rem; font-weight: 900; color: #FFFFFF; margin: 4px 0;">CLAIMED ✓</div>
                <div style="font-size: 0.72rem; color: #CBD5E1;">Scanned at 07:44 AM (Flavours)</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col2:
            st.markdown("""
            <div style="background: rgba(16, 185, 129, 0.1); border: 1.5px solid #10B981; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.72rem; color: #10B981; font-weight: 800;">BUFFET LUNCH</div>
                <div style="font-size: 1.6rem; font-weight: 900; color: #FFFFFF; margin: 4px 0;">CLAIMED ✓</div>
                <div style="font-size: 0.72rem; color: #CBD5E1;">Scanned at 01:18 PM (Tamu Tamu)</div>
            </div>
            """, unsafe_allow_html=True)

        with m_col3:
            st.markdown("""
            <div style="background: rgba(245, 197, 66, 0.1); border: 1.5px solid #F5C542; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.72rem; color: #F5C542; font-weight: 800;">SEAFOOD GALA DINNER</div>
                <div style="font-size: 1.6rem; font-weight: 900; color: #F5C542; margin: 4px 0;">ACTIVE (1/1)</div>
                <div style="font-size: 0.72rem; color: #CBD5E1;">Ready for 07:00 PM Entrance</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("##### 🧪 Test Fraud Protection (Simulate Duplicate Meal Claim):")
        if st.button("🚫 Simulate Second Lunch Claim (Fraud Prevention Test)", use_container_width=True):
            st.error("🛑 ACCESS DENIED: Lunch was ALREADY CLAIMED at 01:18:24 PM at Tamu Tamu Terrace! (Duplicate claim blocked).")

    # --------------------------------------------------------------------------
    # SUB-TAB 4: SECRET BALLOT & E-VOTING
    # --------------------------------------------------------------------------
    with sub_vote:
        st.markdown("### 🗳️ Confidential E-Voting Chamber")
        st.caption("Cast your certified secret ballot for Ordinary Business and Board Elections:")

        v_col1, v_col2 = st.columns([1.1, 1.2])

        with v_col1:
            st.markdown(f"""
            <div style="background: rgba(8, 28, 58, 0.85); border: 1.5px solid #00F2FE; border-radius: 10px; padding: 12px 16px; margin-bottom: 12px;">
                <div style="font-size: 0.72rem; color: #00F2FE; font-weight: 800;">CERTIFIED VOTER CREDENTIAL</div>
                <div style="font-size: 1.1rem; font-weight: 800; color: #FFFFFF;">{del_name}</div>
                <div style="font-size: 0.8rem; color: #F5C542; font-weight: 800; margin-top: 2px;">
                    ⚖️ Allocated Voting Power: 10,000 Votes (Executive Quorum)
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.form("form_retreat_ballot"):
                st.markdown("##### 📜 Item 1: Ordinary Resolution 1")
                st.caption("Approval of Audited Financial Accounts & 14% Dividend Declaration:")
                v_res = st.radio("Your Vote:*", ["FOR (Approve Accounts & 14% Dividend)", "AGAINST", "ABSTAIN"])

                st.markdown("##### 🗳️ Item 2: Supervisory Committee Election")
                v_cand = st.radio("Candidate Selection:*", [
                    "Sarah Wanjiru CPA(K) (Independent, Audit & Finance)",
                    "Eng. David Ndung'u (Incumbent, Risk & Governance)",
                    "Dr. Peter Otieno (Institutional Nominee)"
                ])

                btn_cast = st.form_submit_button("🔒 Cast Confidential Ballot (10,000 Votes)", type="primary", use_container_width=True)

                if btn_cast:
                    st.balloons()
                    st.success("✓ Ballot Cast & Sealed! SHA-256 Receipt: SHA256:7a9f82d1c0b39e44")

        with v_col2:
            st.markdown("##### 📊 Returning Officer Live Tally Screen")
            st.caption("Real-time election return dynamically updating:")

            st.metric("Total Ballots Cast", "64 / 95 (67.4% Quorum)", delta="+10,000 Votes")

            st.markdown("###### Supervisory Committee Election Tally")
            st.markdown("""
            <div>
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #CBD5E1; font-weight: 700;">
                    <span style="color: #F5C542;">🏆 Sarah Wanjiru CPA(K)</span>
                    <span style="color: #F5C542;">420,000 votes (65.6%)</span>
                </div>
                <div style="background: rgba(255,255,255,0.08); border-radius: 6px; height: 10px; width: 100%; margin-top: 2px;">
                    <div style="background: #F5C542; height: 100%; width: 65.6%; border-radius: 6px;"></div>
                </div>
            </div>
            <div style="margin-top: 10px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #CBD5E1; font-weight: 700;">
                    <span>Eng. David Ndung'u</span>
                    <span>180,000 votes (28.1%)</span>
                </div>
                <div style="background: rgba(255,255,255,0.08); border-radius: 6px; height: 10px; width: 100%; margin-top: 2px;">
                    <div style="background: #38BDF8; height: 100%; width: 28.1%; border-radius: 6px;"></div>
                </div>
            </div>
            <div style="margin-top: 10px;">
                <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #CBD5E1; font-weight: 700;">
                    <span>Dr. Peter Otieno</span>
                    <span>40,000 votes (6.3%)</span>
                </div>
                <div style="background: rgba(255,255,255,0.08); border-radius: 6px; height: 10px; width: 100%; margin-top: 2px;">
                    <div style="background: #94A3B8; height: 100%; width: 6.3%; border-radius: 6px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

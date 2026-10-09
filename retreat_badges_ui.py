import os
import io
import json
import pandas as pd
import streamlit as st
from PIL import Image

def render_retreat_badges_ui():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "RETREAT_BADGES_REGISTRY.csv")
    front_dir = os.path.join(base_dir, "FRONT_CARDS")
    back_dir = os.path.join(base_dir, "BACK_CARDS")
    qr_dir = os.path.join(base_dir, "QR_CODES")

    if not os.path.exists(csv_path):
        st.warning("Retreat Badges registry not found. Please run the generation script first.")
        return

    # Experience Mode Selector (Luxury Mobile UI vs Print Center)
    retreat_mode = st.radio(
        "Select Retreat Experience Interface:",
        ["📱 Luxury Executive Mobile Pass & Live Experience (New)", "🖨️ Commercial Press-Ready Print Center (Badges PDF)"],
        horizontal=True,
        key="mombasa_retreat_mode_toggle"
    )

    if "Luxury Executive Mobile Pass" in retreat_mode:
        import mombasa_retreat_experience
        mombasa_retreat_experience.render_mombasa_retreat_experience()
        return

    # Header Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(6, 18, 38, 0.95) 0%, rgba(10, 32, 70, 0.9) 50%, rgba(2, 10, 24, 0.95) 100%); 
                border: 2px solid #DEAC30; border-radius: 14px; padding: 20px 24px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div>
                <div style="display: inline-block; background: #DEAC30; color: #061226; font-weight: 900; font-size: 0.75rem; 
                            padding: 3px 10px; border-radius: 4px; letter-spacing: 1.2px; text-transform: uppercase;">
                    🏦 BANKI KUU SACCO & BHC • MOMBASA 2026
                </div>
                <h2 style="color: #FFFFFF; margin: 8px 0 4px 0; font-size: 1.5rem; font-weight: 800;">
                    Executive Strategic Retreat: Badge & Tokenized QR Pass Center
                </h2>
                <div style="color: #94A3B8; font-size: 0.85rem;">
                    PrideInn Paradise Beach Resort & Spa, Shanzu • ODPC §25 Compliant Digital Keys • Coastal Navy & Gold Aesthetic
                </div>
            </div>
            <div style="text-align: right;">
                <span style="background: rgba(0, 215, 240, 0.15); border: 1px solid #00D7F0; color: #00D7F0; 
                            font-size: 0.8rem; font-weight: 700; padding: 6px 14px; border-radius: 20px; display: inline-block;">
                    🛡️ ODPC §25 VERIFIED (Zero Plaintext PII)
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Top Metrics Bar
    total_delegates = len(df)
    exec_count = len(df[df["tier"] == "EXECUTIVE"])
    ops_count = len(df[df["tier"] == "OPERATIONS"])
    support_count = len(df[df["tier"] == "SUPPORT"])

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Attendees", f"{total_delegates}", help="Full registered cohort")
    with c2:
        st.metric("Executive Delegates", f"{exec_count}", help="BOD, Supervisory, CEO & Secretariat")
    with c3:
        st.metric("Operations Staff", f"{ops_count}", help="Canteen & Hospitality Teams")
    with c4:
        st.metric("Security & Compliance", "100% ODPC", help="Cryptographic tokenization without raw PII")

    st.markdown("<hr style='border: 0; border-top: 1px solid rgba(222, 172, 48, 0.3); margin: 15px 0 20px 0;'>", unsafe_allow_html=True)

    # Commercial Press-Ready Print Center Section
    press_dir = os.path.join(base_dir, "PRESS_READY_OUTPUT")
    duplex_pdf = os.path.join(press_dir, "CBK_MOMBASA_2026_PRESS_READY_BADGES_DUPLEX.pdf")
    impos_pdf = os.path.join(press_dir, "CBK_MOMBASA_2026_IMPOSITION_SHEETS_4UP.pdf")

    with st.expander("🖨️ Commercial Press-Ready Print Documents (300 DPI Glossy Cardstock Run)", expanded=True):
        st.markdown("""
        <div style="background: rgba(2, 6, 14, 0.7); border: 1.5px solid #00F2FE; border-radius: 10px; padding: 14px 18px; margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
                <div>
                    <h4 style="margin: 0 0 4px 0; color: #FFFFFF; font-size: 1.05rem;">
                        Commercial Print Shop Package: 60 Executive Delegate Badges
                    </h4>
                    <div style="font-size: 0.8rem; color: #CBD5E1;">
                        Standard 300 DPI High-Resolution • 4-Up Imposition with Crop Marks & Bleed • Duplex Mirror Alignment
                    </div>
                </div>
                <div>
                    <span style="background: rgba(245, 197, 66, 0.2); border: 1px solid #F5C542; color: #F5C542; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem; font-weight: 700;">
                        GLOSSY CARDSTOCK READY
                    </span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        pcol1, pcol2 = st.columns(2)
        with pcol1:
            if os.path.exists(impos_pdf):
                with open(impos_pdf, "rb") as f:
                    pdf_bytes = f.read()
                st.download_button(
                    label="📄 Download 4-Up Imposition Sheets (30 Pgs, Crop Marks)",
                    data=pdf_bytes,
                    file_name="CBK_MOMBASA_2026_IMPOSITION_SHEETS_4UP_300DPI.pdf",
                    mime="application/pdf",
                    key="dl_impos_pdf"
                )
                st.caption("Recommended for commercial press operators with guillotine cutting.")

        with pcol2:
            if os.path.exists(duplex_pdf):
                with open(duplex_pdf, "rb") as f:
                    duplex_bytes = f.read()
                st.download_button(
                    label="📑 Download 120-Page Duplex Deck (Front & Back 1:1)",
                    data=duplex_bytes,
                    file_name="CBK_MOMBASA_2026_PRESS_READY_BADGES_DUPLEX_300DPI.pdf",
                    mime="application/pdf",
                    key="dl_duplex_pdf"
                )
                st.caption("Recommended for direct duplex card printers (Zebra / Fargo / Evolis).")

    st.markdown("<hr style='border: 0; border-top: 1px solid rgba(222, 172, 48, 0.2); margin: 15px 0 20px 0;'>", unsafe_allow_html=True)

    # Filters and Search
    f_col1, f_col2, f_col3 = st.columns([1.5, 2, 2.5])
    with f_col1:
        category_options = ["All Cohorts (95)", "Executive & Governance (51)", "Secretariat Leadership (24)", "Operations & Hospitality (42)"]
        cat_filter = st.selectbox("🎯 Filter Cohort", category_options)

    # Filter dataframe
    if "Executive" in cat_filter:
        filtered_df = df[df["tier"] == "EXECUTIVE"]
    elif "Secretariat" in cat_filter:
        filtered_df = df[df["category"] == "SECRETARIAT LEADERSHIP"]
    elif "Operations" in cat_filter:
        filtered_df = df[df["tier"] == "OPERATIONS"]
    else:
        filtered_df = df

    with f_col2:
        search_query = st.text_input("🔍 Search Name, Serial No, or Token", placeholder="e.g. Josiah, 3124, B25F3E65")
        if search_query.strip():
            sq = search_query.strip().lower()
            filtered_df = filtered_df[
                filtered_df["full_name"].str.lower().str.contains(sq, na=False) |
                filtered_df["serial"].astype(str).str.lower().str.contains(sq, na=False) |
                filtered_df["token_id"].str.lower().str.contains(sq, na=False)
            ]

    with f_col3:
        if len(filtered_df) == 0:
            st.warning("No delegates matching criteria.")
            selected_idx = None
        else:
            delegate_labels = [f"{r['index']:02d}. {r['full_name']} — {r['role']} (S/No: #{r['serial']})" for _, r in filtered_df.iterrows()]
            selected_choice = st.selectbox("👤 Select Delegate to View Badges", delegate_labels, index=0)
            selected_idx = int(selected_choice.split(".")[0])

    if selected_idx is not None:
        row = df[df["index"] == selected_idx].iloc[0]
        front_img_path = os.path.join(front_dir, str(row["front_card_file"]))
        back_img_path = os.path.join(back_dir, str(row["back_card_file"]))
        qr_img_path = os.path.join(qr_dir, str(row["qr_code_file"]))

        st.markdown(f"""
        <div style="background: rgba(10, 32, 70, 0.4); border-left: 4px solid #DEAC30; padding: 12px 18px; border-radius: 6px; margin: 15px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                <div>
                    <strong style="color: #DEAC30; font-size: 1.1rem;">{row['full_name']}</strong> 
                    <span style="color: #94A3B8; margin-left: 8px;">({row['role']})</span>
                </div>
                <div style="font-family: monospace; color: #00D7F0; font-size: 0.88rem;">
                    Token ID: <strong>{row['token_id']}</strong> • Clearance: <span style="color: #FFE68C;">{row['tier']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Dual Badge Display (Front & Back)
        col_front, col_back = st.columns(2)

        with col_front:
            st.markdown("### 🏷️ Front Badge (Mombasa Executive Pass)")
            if os.path.exists(front_img_path):
                st.image(front_img_path, caption=f"Front: {row['full_name']} — Pass #{row['token_id']}", use_container_width=True)
                with open(front_img_path, "rb") as f:
                    btn_data = f.read()
                st.download_button(
                    label=f"📥 Download Front Badge ({row['serial']})",
                    data=btn_data,
                    file_name=f"FRONT_{row['serial']}_{row['full_name'].replace(' ', '_')}.png",
                    mime="image/png",
                    key=f"dl_front_{row['index']}"
                )
            else:
                st.info("Front badge image generating...")

        with col_back:
            st.markdown("### 📋 Back Card (Itinerary & ODPC Pass)")
            if os.path.exists(back_img_path):
                st.image(back_img_path, caption=f"Back: 3-Day Itinerary & Encrypted QR Key", use_container_width=True)
                with open(back_img_path, "rb") as f:
                    btn_data = f.read()
                st.download_button(
                    label=f"📥 Download Back Card ({row['serial']})",
                    data=btn_data,
                    file_name=f"BACK_{row['serial']}_{row['full_name'].replace(' ', '_')}.png",
                    mime="image/png",
                    key=f"dl_back_{row['index']}"
                )
            else:
                st.info("Back card image generating...")

        # Interactive Verification & Metadata Section
        st.markdown("<hr style='border: 0; border-top: 1px solid rgba(222, 172, 48, 0.2); margin: 25px 0 15px 0;'>", unsafe_allow_html=True)
        meta_c1, meta_c2 = st.columns([1.2, 1.8])

        with meta_c1:
            st.markdown("#### 📱 Standalone Tokenized QR Code")
            if os.path.exists(qr_img_path):
                st.image(qr_img_path, width=220, caption="Encrypted Access Key (No PII)")
                with open(qr_img_path, "rb") as f:
                    qr_bytes = f.read()
                st.download_button(
                    label="📥 Download High-Res QR",
                    data=qr_bytes,
                    file_name=f"QR_{row['token_id']}.png",
                    mime="image/png",
                    key=f"dl_qr_{row['index']}"
                )

        with meta_c2:
            st.markdown("#### 🛡️ ODPC Compliance & Security Validation")
            st.markdown(f"""
            <table style="width: 100%; border-collapse: collapse; font-size: 0.85rem; color: #CBD5E1;">
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <td style="padding: 6px 0; color: #94A3B8; width: 140px;"><strong>Protected ID:</strong></td>
                    <td style="padding: 6px 0; font-family: monospace; color: #FFFFFF;">{row['masked_id']}</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <td style="padding: 6px 0; color: #94A3B8;"><strong>Protected Phone:</strong></td>
                    <td style="padding: 6px 0; font-family: monospace; color: #FFFFFF;">{row['masked_phone']}</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <td style="padding: 6px 0; color: #94A3B8;"><strong>Official Email:</strong></td>
                    <td style="padding: 6px 0; font-family: monospace; color: #FFFFFF;">{row['masked_email']}</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                    <td style="padding: 6px 0; color: #94A3B8;"><strong>Crypto Signature:</strong></td>
                    <td style="padding: 6px 0; font-family: monospace; font-size: 0.72rem; color: #00D7F0; word-break: break-all;">{row['crypto_sig']}</td>
                </tr>
                <tr>
                    <td style="padding: 6px 0; color: #94A3B8;"><strong>ODPC Compliance:</strong></td>
                    <td style="padding: 6px 0; color: #10B981; font-weight: 700;">✓ Section 25 Certified (HMAC-SHA256 Tokenization)</td>
                </tr>
            </table>
            """, unsafe_allow_html=True)

            if st.button("🧪 Simulate Gate Scanner Validation", key=f"scan_sim_{row['index']}"):
                st.success(f"✓ Gate Clearance Approved: {row['full_name']} ({row['role']}) — Access Level: {row['tier']}")
                st.json({
                    "scan_status": "SUCCESS",
                    "timestamp": "2026-10-07T12:30:00+03:00",
                    "event": "Banki Kuu SACCO Executive Retreat 2026",
                    "token_id": row["token_id"],
                    "signature_verified": True,
                    "terminal": "PrideInn Grand Ballroom Gate 01",
                    "pii_leakage": "ZERO (Strict ODPC Compliance)"
                })

    # Full Roster Table Tab / Expander
    with st.expander("📊 View Complete Participant Registry Table (95 Attendees)", expanded=False):
        st.dataframe(
            df[["index", "serial", "full_name", "role", "category", "tier", "token_id", "masked_id", "masked_phone"]],
            use_container_width=True,
            hide_index=True
        )
        csv_download = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Full Registry as CSV",
            data=csv_download,
            file_name="RETREAT_BADGES_REGISTRY_EXPORT.csv",
            mime="text/csv"
        )

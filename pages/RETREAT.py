"""
================================================================================
BANKI KUU SACCO & BHC — EXECUTIVE RETREAT BADGES & DIGITAL PASSES
URL Route: /RETREAT (https://cbk-stride.streamlit.app/RETREAT)
================================================================================
"""

import os
import sys
import streamlit as st

# Ensure root directory is on sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    st.set_page_config(
        page_title="Banki Kuu SACCO | Executive Retreat Badges & Passes",
        page_icon="🏖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
except Exception:
    pass

import retreat_badges_ui
retreat_badges_ui.render_retreat_badges_ui()

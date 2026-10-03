"""
================================================================================
BANKI KUU SACCO — 58TH AGM & SHAREHOLDER ELECTIONS PORTAL
URL Route: /BKS (https://cbk-stride.streamlit.app/BKS)
================================================================================
"""

import streamlit as st
import os
import sys
import importlib

# Ensure root directory is on sys.path for utils import
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    st.set_page_config(
        page_title="Banki Kuu SACCO | 58th AGM & Board Elections",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
except Exception:
    pass

# Force query params for Banki Kuu SACCO preset
st.query_params["event_id"] = "EVT-BANKI-KUU-SACCO"
st.query_params["bks"] = "1"

# Import and reload EVENTS module so UI code executes on every page view
import pages.EVENTS
importlib.reload(pages.EVENTS)

"""
================================================================================
BANKI KUU SACCO — 58TH AGM & SHAREHOLDER ELECTIONS PORTAL
URL Route: /BKS (https://cbk-stride.streamlit.app/BKS)
================================================================================
"""

import streamlit as st
import os
import sys

# Ensure root directory is on sys.path for utils import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Force query param for Banki Kuu SACCO preset
st.query_params["event_id"] = "EVT-BANKI-KUU-SACCO"

# Import and render EVENTS module
from pages import EVENTS

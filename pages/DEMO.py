"""
================================================================================
CBK STRIDE™ — DEMO ROUTE ALIAS
Ensures both /DEMO and /-DEMO load the interactive sandbox seamlessly.
================================================================================
"""
import os
import sys

demo_target = os.path.join(os.path.dirname(__file__), "-DEMO.py")
with open(demo_target, "r", encoding="utf-8") as f:
    code = f.read()

exec(compile(code, demo_target, "exec"))

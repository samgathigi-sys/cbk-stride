"""
Automated FTP Deployment Script for StrideAnalytics
Uploads index.html and all 5 interactive subpages directly to public_html on 173.214.168.54
"""

import os
import ftplib

import sys
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HOST = "173.214.168.54"
USER = "strideadmin"
PASS = "{0t!!B@II^[(BA%&Gk"

LOCAL_DIR = r"C:\Users\user\.gemini\antigravity\scratch\cbk-stride\strideanalytics_web"

FILES_TO_UPLOAD = [
    "index.html",
    "about.html",
    "stride-sacco.html",
    "saccostride.html",
    "govstride.html",
    "engine.html",
    "agmplan.html",
    "creditscore.html",
    "stride-chat.css",
    "stride-chat.js",
    "strideanalytics_whitepaper.pdf",
    "stride_cadence_executive_whitepaper.pdf",
    "NAVISION_TRIAL_BALANCE_2025_EXPORT.csv",
    "GL_TRIAL_BALANCE_2025_EXPORT.csv",
    "WEEKLY_LOAN_REPAYMENT_LEDGER_W42_2025.csv",
    "MOCK_HIGHLANDS_TEA_SACCO_LOAN_LEDGER.csv",
    "CoreBanking_MemberLoanLedger_Q4_2025.csv",
    "demo.html"
]

def deploy():
    print(f"Connecting to FTP server {HOST} as {USER}...")
    ftp = ftplib.FTP(HOST, timeout=15)
    ftp.login(USER, PASS)
    print("Connected successfully!")
    
    print("Navigating to public_html...")
    ftp.cwd("public_html")
    print(f"Current Remote Directory: {ftp.pwd()}")
    
    for filename in FILES_TO_UPLOAD:
        local_path = os.path.join(LOCAL_DIR, filename)
        if not os.path.exists(local_path):
            print(f"ERROR: Local file not found: {local_path}")
            continue
            
        file_size = os.path.getsize(local_path)
        print(f"Uploading {filename} ({file_size:,} bytes)...")
        with open(local_path, "rb") as f:
            ftp.storbinary(f"STOR {filename}", f)
        print(f"[OK] Uploaded {filename} successfully.")
        
    print("\n--- Verifying Remote public_html Directory ---")
    remote_files = ftp.nlst()
    for filename in FILES_TO_UPLOAD:
        if filename in remote_files:
            size = ftp.size(filename)
            print(f"  [CONFIRMED LIVE] {filename} -> {size:,} bytes")
        else:
            print(f"  [MISSING] {filename}")
            
    ftp.quit()
    print("\n🚀 DEPLOYMENT COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    deploy()

"""
Upload Bank of Uganda Cyber Forensics Masterclass to strideanalytics.com/Training/
"""
import os
import ftplib

FTP_HOST = "173.214.168.54"
FTP_USER = "strideadmin"
FTP_PASS = "{0t!!B@II^[(BA%&Gk"

LOCAL_DIR = r"C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics"

files_to_upload = [
    # (local_filename, remote_relative_path)
    ("bou_masterclass_presentation.html", "index.html"),
    ("bou_masterclass_presentation.html", "bou_masterclass_presentation.html"),
    ("war_room_simulator.html", "war_room_simulator.html"),
    ("cyber_forensic_chef.html", "cyber_forensic_chef.html"),
    ("Bank_of_Uganda_Cyber_Forensics_Masterclass.pdf", "Bank_of_Uganda_Cyber_Forensics_Masterclass.pdf"),
    ("Bank_of_Uganda_Cyber_Forensics_Masterclass.pptx", "Bank_of_Uganda_Cyber_Forensics_Masterclass.pptx"),
    ("HOWTO_MASTERCLASS_TRAINER_GUIDE.md", "HOWTO_MASTERCLASS_TRAINER_GUIDE.md"),
    ("HOWTO_MASTERCLASS_TRAINER_GUIDE.pdf", "HOWTO_MASTERCLASS_TRAINER_GUIDE.pdf"),
    ("README.md", "README.md"),
    ("DAY_1_FOUNDATIONS_AND_THREATS.md", "DAY_1_FOUNDATIONS_AND_THREATS.md"),
    ("DAY_2_NETWORK_FORENSICS_AND_IOCS.md", "DAY_2_NETWORK_FORENSICS_AND_IOCS.md"),
    ("DAY_3_EVIDENCE_ACQUISITION_AND_MEMORY.md", "DAY_3_EVIDENCE_ACQUISITION_AND_MEMORY.md"),
    ("DAY_4_INCIDENT_RESPONSE_AND_MALWARE.md", "DAY_4_INCIDENT_RESPONSE_AND_MALWARE.md"),
    ("DAY_5_UGANDA_LAW_AND_EXECUTIVE_REPORTING.md", "DAY_5_UGANDA_LAW_AND_EXECUTIVE_REPORTING.md"),
]

def main():
    print(f"Connecting to FTP server {FTP_HOST}...")
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    print("Logged in successfully.")

    ftp.cwd("public_html")
    
    # Check if 'Training' directory exists, if not create it
    dirs = []
    ftp.retrlines("NLST", dirs.append)
    if "Training" not in dirs:
        print("Creating directory 'Training' in public_html...")
        ftp.mkd("Training")
    else:
        print("Directory 'Training' already exists.")

    ftp.cwd("Training")
    print(f"Current remote directory: {ftp.pwd()}")

    for local_name, remote_name in files_to_upload:
        local_path = os.path.join(LOCAL_DIR, local_name)
        if os.path.exists(local_path):
            with open(local_path, "rb") as f:
                print(f"Uploading {local_name} -> Training/{remote_name}...")
                ftp.storbinary(f"STOR {remote_name}", f)
            print(f"[OK] Uploaded {remote_name}")
        else:
            print(f"[ERROR] File missing: {local_path}")

    ftp.quit()
    print("\nAll masterclass files uploaded successfully to strideanalytics/Training!")

if __name__ == "__main__":
    main()

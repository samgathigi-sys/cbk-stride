# Bank of Uganda 5-Day Cyber Forensics Masterclass
## Comprehensive Trainer & Participant How-To Operating Manual
### *Advanced Digital Forensics, Financial Threat Triage & Cross-Border Sovereign AI*

---

## 🏛️ 1. Masterclass Executive Overview & Architecture
This manual provides the step-by-step facilitation walkthrough for the 5-day masterclass delivered for the **Bank of Uganda (BoU)** Information Security, IT Audit, Risk Management, and CSIRT engineering teams.

All live interactive simulation tools, slide decks, and participant lab environments are hosted at:  
👉 **[https://strideanalytics.co.ke/Training/](https://strideanalytics.co.ke/Training/)**

---

## 📅 2. Day-by-Day Instructional Facilitation Plan

### Day 1: Foundations of Central Bank Digital Forensics & Threat Modeling
- **Learning Objectives**: ISO/IEC 27037 standards, Order of Volatility (RFC 3227), digital evidence seizure, and Central Bank threat models (RTGS, SWIFT, Core Banking).
- **Core Hands-on Lab**: 
  - Execute `evidence_integrity_verifier.py`.
  - **Key Pedagogical Lesson**: Binary mode capture (`"wb"` / `"rb"`). Show participants how OS-level CRLF newline conversion on Windows alters SHA-256 hashes, risking court dismissal.
- **War Room Tool**: Open **Mod 1 & 4: Evidence & Law** tab in the War Room. Use the live cryptographic hashing tool and test the "Simulate 1-Byte Tamper" button to demonstrate hash mismatch in court.

### Day 2: Cyber Attack Vectors, IoCs & Network Forensics
- **Learning Objectives**: Financial APT attack taxonomy, Command & Control (C2) beaconing mechanics, packet analysis, and IoC extraction.
- **Core Hands-on Lab**:
  - Execute `network_pcap_analyzer.py`.
  - **Key Pedagogical Lesson**: Statistical Jitter ratio. Explain why automated bot implants have low variance (`jitter < 0.15`), whereas human web browsing has high dispersion (`jitter > 1.0`).
- **War Room Tool**: Open **Mod 2: Threats & IoCs** to inspect the live IoC matrix (IPs, hashes, domains, JA3 fingerprints).

### Day 3: Forensic Imaging, Volatile RAM & Artifact Analysis
- **Learning Objectives**: Hardware write-blockers, bitstream raw vs E01 imaging, Volatility 3 memory triage, and NTFS Master File Table ($MFT) analysis.
- **Core Hands-on Lab**:
  - Open **Mod 3: Tools & Workbench** in the War Room.
  - Step 1: In the **Volatility 3 Terminal**, execute `windows.pslist`, then run `windows.malfind` to isolate the injected dual-sign bypass hook at offset `0x7ff72a140010` in `bou_rtgs_service.exe` (PID 4128).
  - Step 2: In the **PCAP Dissector**, click Frame 104 and Frame 108 to inspect the hex payload and decoded RTGS RPC calls.
  - Step 3: In the **File System Carver**, demonstrate timestomping anti-forensics ($STANDARD_INFORMATION vs $FILE_NAME).

### Day 4: Incident Response Playbooks & Advanced Malware Triage
- **Learning Objectives**: NIST SP 800-61 / ISO 27035 containment lifecycles, active directory eviction, ransomware isolation without reboot, and custom YARA rule engineering.
- **Core Hands-on Lab**:
  - Open **Mod 6: Malware & Cloud/AI** in the War Room. Test the interactive YARA signature compiler against process memory dumps.
  - Open **Mod 5: Incident Playbooks (TTX)** and run the simulated crisis drills.

### Day 5: Uganda Cyber Laws, Evidence Admissibility & Executive Reporting
- **Learning Objectives**: Statutory compliance under the **Uganda Computer Misuse Act (2011 & 2022 Amendment)**, **Data Protection and Privacy Act 2019**, and **Electronic Signatures Act 2011**.
- **Core Hands-on Lab**:
  - Open **Mod 7: Executive Report** in the War Room. Review the formal investigation dossier for Case `BOU-CYBER-2026-001` and demonstrate the one-click print/PDF export for the Governor and Board of Directors.
  - Capstone Defense: Mock cross-examination on chain of custody (Ledger `BOU-CUSTODY-TAPE-084`).

---

## 🕹️ 3. How to Facilitate the War Room & Incident Tabletop Simulator (TTX)
The Tabletop Simulator features **8 randomized scenarios**:
1. Navigate to **Mod 5: Incident Playbooks (TTX)** on the portal.
2. Click **`🎲 Random Incident Drill`** to generate an unannounced crisis (e.g., SWIFT HSM Key Bypass, Cloud API Token Replay, AI Voice Deepfake Wire Fraud).
3. Have participant teams debate and select decisions under pressure.
4. Highlight how every incorrect operational choice (e.g., pulling server power cords, paying ransomware, accepting unhashed logs) triggers instant point deductions and court admissibility penalties.

---

## 🔪 4. How to Run the CyberForensic Chef & Sovereign PII Privacy Shield
The dedicated open-source investigation tool is live at:  
👉 **[https://strideanalytics.co.ke/Training/cyber_forensic_chef.html](https://strideanalytics.co.ke/Training/cyber_forensic_chef.html)**

### Workflow A: Investigating Obfuscated Banking Malware
1. Click **`Load Obfuscated Malware`** in the top bar.
2. Add the recipe operations: `From Base64` → `Extract IoCs` → `Shannon Entropy Analysis`.
3. Click **`⚡ Bake & Execute Recipe`**.
4. Show how the hidden PE header, extracted C2 IP (`194.26.29.11`), and high entropy score (`7.14/8.00`) definitively establish malicious intent.

### Workflow B: The Power of PII Privacy in Financial Forensics
1. Click **`Load Dirty Bank PII Log`**. Show raw citizen names, Ugandan National ID Numbers (NIN `CM88019234KL12`), account numbers, and phone numbers.
2. Add the privacy shield operations:
   - `Shield Uganda NIN & Kenya IDs`
   - `Mask Bank Account Numbers (IBAN/PAN)`
   - `Mask Mobile Money MSISDNs (+256/+254)`
   - `Cryptographic HMAC Tokenization`
   - `Differential Privacy (ε=0.5 Laplace Noise)`
3. Click **`⚡ Bake & Execute Recipe`**.
4. Point out the **Statutory Privacy Audit Scorecard**: The evidence changes from *Violation* to *100% PROTECTED (Clean)*, proving compliance with Section 10 & 14 of the **Uganda Data Protection and Privacy Act 2019**.

---

## 🤖 5. How to Demonstrate Cross-Border Federated Learning (BoU ↔ CBK)
1. Open the **`🇰🇪 ↔ 🇺🇬 Regional Intel & Federated AI`** tab in the War Room.
2. Review the 3 real-world case studies from Kenyan financial cyberspace (Apex SACCO B2C float heist, eCitizen/KEPSS DDoS smokescreen, and SIM-swap syndicate OTP interception).
3. Scroll to the **Sovereign Federated Learning Engine**:
   - Explain the core legal dilemma: Uganda and Kenya Data Protection Acts prevent exporting raw bank customer logs across borders.
   - Click **`🚀 Execute Cross-Border Federated Learning Round`**.
   - Watch the 4-phase progress bar compute local gradients, apply Differential Privacy ($\epsilon = 0.5$) and Paillier Homomorphic Encryption, synchronize across the Kampala ↔ Nairobi fiber bridge, and aggregate via FedAvg.
   - Point out the resulting **98.6% zero-day detection accuracy** achieved with **0.00 KB raw data transferred**!

---

## ⚡ 6. How to Facilitate the Autonomous SOAR Playbook Studio
The dedicated SOAR laboratory is live at:  
👉 **[https://strideanalytics.co.ke/Training/soar_playbook_simulator.html](https://strideanalytics.co.ke/Training/soar_playbook_simulator.html)**

### Key Pedagogical Lessons:
1. **The 3:00 AM Question:** Ask the delegates: *"Can human analysts sit up all night inspecting Base64 strings and memory dumps?"*
2. **Execute Full Auto (1.5s):** Select the **Zero-Day SQLi & Code Injection** scenario and click **`▶ Full Auto`**. Watch all 7 nodes light up in 1.34s (Ingest ➔ Enrich ➔ Decision ➔ Firewall Drop ➔ Identity Revocation ➔ Volatile RAM Snapshot ➔ Statutory Ticket).
3. **Walk Through Step-by-Step:** Advance node by node using **`⏯ Step-by-Step`** to explain how the SOAR calls REST APIs on OPNsense/BGP and triggers the CyberForensic Chef microservice automatically.
4. **Spotlight Open-Source SOAR Tools:** Introduce delegates to **Shuffle SOAR** (shuffler.io), **TheHive + Cortex**, and **Wazuh Active Response**.

---

## 🌐 7. How to Present the Sovereign Payment Systems & Open-Source Network Proposal
The interactive, colorful network proposal is live at:  
👉 **[https://strideanalytics.co.ke/Training/payment_systems_architecture.html](https://strideanalytics.co.ke/Training/payment_systems_architecture.html)**

### Network Defense-in-Depth Walkthrough:
1. **Zone 0 (External Ingestion):** Commercial banks, MTN MoMo, Airtel Money, and SWIFT connecting over mTLS / IPSec fiber leased lines.
2. **Zone 1 (Perimeter DMZ):** Free Coraza WAF ($0 OSS) and Suricata 10Gbps NIDS filtering SQLi and C2 beacons without adding latency to live transactions.
3. **Zone 2 (Core Payment Enclave):** BoU RTGS switch and PostgreSQL settlement database protected by in-guest Wazuh Agents (FIM + Malfind RWX memory probes).
4. **Zone 3 (Sovereign Open-Source SOC Enclave):** The central nervous system uniting Wazuh SIEM, Shuffle SOAR, CyberForensic Chef, TheHive, and MISP threat sharing with Kenya CBK.
5. **Interactive Node Inspector:** Click on any component badge (e.g. *PostgreSQL*, *Wazuh*, *Coraza*, *MTN MoMo*) to open the technical drawer displaying real-world configuration scripts and regulatory compliance notes.
6. **The Financial Case:** Review the Economic Analysis Table showing how Bank of Uganda saves **$460,000 / year** by replacing proprietary licensing with sovereign open-source engineering.

---

## 🔗 8. Masterclass Online Resource Directory
- **Interactive Presentation Deck (Slides)**: [https://strideanalytics.co.ke/Training/](https://strideanalytics.co.ke/Training/)
- **War Room & Tabletop Simulator**: [https://strideanalytics.co.ke/Training/war_room_simulator.html](https://strideanalytics.co.ke/Training/war_room_simulator.html)
- **Autonomous SOAR Playbook Studio**: [https://strideanalytics.co.ke/Training/soar_playbook_simulator.html](https://strideanalytics.co.ke/Training/soar_playbook_simulator.html)
- **Sovereign Payment Systems Network Proposal**: [https://strideanalytics.co.ke/Training/payment_systems_architecture.html](https://strideanalytics.co.ke/Training/payment_systems_architecture.html)
- **CyberForensic Chef & PII Shield**: [https://strideanalytics.co.ke/Training/cyber_forensic_chef.html](https://strideanalytics.co.ke/Training/cyber_forensic_chef.html)
- **PDF Slide Deck**: [https://strideanalytics.co.ke/Training/Bank_of_Uganda_Cyber_Forensics_Masterclass.pdf](https://strideanalytics.co.ke/Training/Bank_of_Uganda_Cyber_Forensics_Masterclass.pdf)
- **PowerPoint Slide Deck (.pptx)**: [https://strideanalytics.co.ke/Training/Bank_of_Uganda_Cyber_Forensics_Masterclass.pptx](https://strideanalytics.co.ke/Training/Bank_of_Uganda_Cyber_Forensics_Masterclass.pptx)

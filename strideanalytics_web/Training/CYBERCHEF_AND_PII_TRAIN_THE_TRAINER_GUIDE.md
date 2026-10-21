# Train-the-Trainer Guide: Mastering CyberChef & The Sovereign PII Privacy Shield
### *A 10-Minute Facilitator Primer for the Bank of Uganda Cyber Forensics Masterclass*

---

## 🧭 1. What Exactly is CyberChef? (The 60-Second Mental Model)

Think of CyberChef as an **assembly line for digital evidence**:
- If an adversary wants to sneak an attack through a bank's firewall or email filter, they don't send plain text. They scramble it using encodings (like Base64 or Hex) and simple math (like XOR).
- To a human eye (or a basic firewall), the payload looks like meaningless gibberish: `TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAA...`
- **CyberChef** lets you take that gibberish, pass it through a chain of simple translation steps (**The Recipe**), and unpack it until the hidden criminal code is revealed.

At the Bank of Uganda, you will teach this tool for **two distinct missions**:
1. **Malware Triage**: Unpacking scrambled attacker payloads.
2. **PII Data Privacy**: Sanitizing innocent bank customer records from evidence files so the Bank complies with the **Uganda Data Protection and Privacy Act 2019 (DPPA)**.

---

## 🔍 2. Core Concepts & Jargon Translated for Instructors

| Term | What It Means | Why Central Bank Investigators Care |
| :--- | :--- | :--- |
| **Base64** | A way of turning binary data (like files or programs) into readable ASCII letters (`A-Z, a-z, 0-9, +, /`). | Attackers use it to sneak executable code past email scanners and intrusion detection systems. |
| **Hex (Hexadecimal)** | Base-16 numbering (`0-9` and `A-F`) representing raw bytes (e.g., `4D 5A` = `MZ`). | Every file on a disk or in memory is made of hex bytes. |
| **XOR Encryption** | A simple mathematical bit-flip operation using a secret byte key. | The #1 technique malware authors use to hide IP addresses and passwords inside executable files. |
| **Shannon Entropy** | A mathematical score from **0.0 to 8.0** measuring how random data is. | Normal English text has an entropy of ~4.0. Encrypted or packed malware has an entropy of **> 7.0**. High entropy = **instant malware red flag**! |
| **Defanging** | Turning live malicious links into harmless text (e.g., `http://malware.com` → `hxxp://malware[.]com`). | Prevents someone from accidentally clicking a malicious link in an official forensic report. |
| **HMAC Tokenization** | Replacing a real customer's name with an irreversible cryptographic pseudonym. | Allows investigators to trace transaction flow between accounts in court without revealing the customer's real identity. |
| **Differential Privacy ($\epsilon$)** | Adding calibrated statistical noise (Laplace noise) to query results. | Allows auditors to verify total transaction sums without being able to reverse-engineer any individual citizen's balance. |

---

## 🎯 3. Live Walkthrough Exercise 1: Malware Deobfuscation (5 Minutes)

### The Classroom Narrative
> *"Class, our SOC detected a suspicious file staged in `C:\Windows\Temp` on the RTGS server. When we open it in Notepad, it looks like random gibberish. Let's use CyberForensic Chef to unmask what the attacker was trying to run."*

### Step-by-Step Instructor Script:
1. Open the tool: **[https://strideanalytics.co.ke/Training/cyber_forensic_chef.html](https://strideanalytics.co.ke/Training/cyber_forensic_chef.html)**
2. In the top right header, click the red button: **`Load Obfuscated Malware`**.
3. **Point out the Input Box**: Show the class the scrambled string starting with `TVqQAAMAAAAE...`.
4. **Explain the Recipe**:
   - Show how the recipe automatically added:
     - `From Base64`
     - `Extract IoCs`
     - `Shannon Entropy Analysis`
5. Click **`⚡ Bake & Execute Recipe`**.
6. **The "Aha!" Moment for the Room**:
   - Point out the output box!
   - Show them the two letters at the very start: **`MZ`** (or `This program cannot be run in DOS mode`). Explain to the class: *"Whenever you see 'MZ', that is the signature header of a Windows Executable (.exe or .dll)! We have just proven that this text string was actually a hidden executable payload!"*
   - Point out the **Shannon Entropy Score: 7.14 / 8.00**. Explain: *"Score above 7.0 means it is packed or encrypted—classic financial trojan behavior."*

---

## 🔒 4. Live Walkthrough Exercise 2: The Sovereign PII Privacy Shield (5 Minutes)

### The Classroom Narrative
> *"Now class, imagine CID detectives subpoena our transaction logs to prosecute the hacker. But the log contains thousands of innocent Ugandan citizens' National ID numbers, bank balances, and phone numbers. If we hand this over unredacted, Bank of Uganda violates Section 10 of the Data Protection and Privacy Act 2019. How do we protect citizen privacy while keeping the evidence valid for court?"*

### Step-by-Step Instructor Script:
1. In the top right header, click the cyan button: **`Load Dirty Bank PII Log`**.
2. **Point out the Input Box**:
   - Show the class real citizen identifiers in the log:
     - Name: `DR. KATO MUGISHA`
     - Ugandan National ID (NIN): `CM88019234KL12`
     - Phone: `+256772189421`
     - Account: `9912048124`
     - Suspicious C2 IP: `194.26.29.11`
3. Point out the bottom audit box: Notice it says **`VIOLATION (Unredacted Citizen Financial Data Present)`** and the badge at the top shows a red alert!
4. **Show the Recipe Steps**:
   - `Shield Uganda NIN & Kenya IDs`
   - `Mask Bank Account Numbers (IBAN/PAN)`
   - `Mask Mobile Money MSISDNs (+256/+254)`
   - `Cryptographic HMAC Tokenization`
5. Click **`⚡ Bake & Execute Recipe`**.
6. **The "Aha!" Moment for the Room**:
   - Point to the output box:
     - `CM88019234KL12` is now `[REDACTED-UG-NIN-***]`
     - `+256772189421` is now `+256-***-***XXX`
     - Account is masked: `ACCT_MASKED=****9912048124`
     - Real customer name is replaced by a verifiable HMAC token: `Identity_Hash: HMAC_SHA256_8a12f9b1c`
     - **CRITICAL FORENSIC POINT**: Notice that the criminal C2 IP (`194.26.29.11`) and the transaction batch number are **NOT masked**! Only innocent personal privacy data is shielded!
   - Point to the compliance badge at the top: It now turns bright green: **`100% PROTECTED ✓ (Clean for High Court Production)`**.

---

## 🎤 5. Master Facilitator Cheatsheet & Questions to Ask the Room

To keep the room highly engaged, ask these 3 questions during the lab:

1. **Question for the Room**: *"Why can't we just use Microsoft Word 'Find & Replace' to delete citizen names?"*
   - **Answer**: Word's find-and-replace doesn't maintain a verifiable cryptographic transformation, alters file timestamps, and leaves metadata traces that defense lawyers will exploit in court. CyberForensic Chef generates repeatable, audited recipes that meet ISO/IEC 27037 standards.

2. **Question for the Room**: *"If we hash the customer's name with HMAC-SHA256, how does that help the judge?"*
   - **Answer**: If the suspect transferred money to 5 different accomplices, the judge can see that Account A sent money to Account B and Account C through identical tokens, proving the money-laundering chain without exposing the innocent victims' real personal lives to public court records.

3. **Question for the Room**: *"What happens if our examiners don't mask PII before sharing logs with third-party incident responders?"*
   - **Answer**: Under the **Uganda Data Protection and Privacy Act 2019**, unauthorized disclosure of financial personal data carries heavy administrative penalties, potential civil litigation against the Bank, and exclusion of digital evidence under constitutional privacy protections.

---

## 🌐 Quick Access Summary for Instructors:
- **CyberForensic Chef Tool**: [https://strideanalytics.co.ke/Training/cyber_forensic_chef.html](https://strideanalytics.co.ke/Training/cyber_forensic_chef.html)
- **Full War Room & TTX**: [https://strideanalytics.co.ke/Training/war_room_simulator.html](https://strideanalytics.co.ke/Training/war_room_simulator.html)
- **Presentation Deck**: [https://strideanalytics.co.ke/Training/](https://strideanalytics.co.ke/Training/)

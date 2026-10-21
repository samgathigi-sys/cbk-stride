"""
Expand scenarios in war_room_simulator.html to 8 varied, randomized, central-bank-relevant scenarios
"""
import re

SRC_FILE = r"C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics\war_room_simulator.html"
with open(SRC_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 1. New HTML for Scenario Selector & Randomizer
new_scenario_ui = r'''
                <!-- Scenario Controls: Filter Pills & Randomizer Button -->
                <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                    <div class="flex items-center gap-2 flex-wrap text-xxs font-mono">
                        <span class="text-slate-400">Filter By Domain:</span>
                        <button onclick="filterScenarios('all')" class="scen-filter-btn active px-2.5 py-1 rounded bg-bou-gold text-bou-950 font-bold" data-filter="all">All (8)</button>
                        <button onclick="filterScenarios('rails')" class="scen-filter-btn px-2.5 py-1 rounded bg-bou-900 hover:bg-bou-850 text-slate-300" data-filter="rails">Payment Rails (RTGS/SWIFT)</button>
                        <button onclick="filterScenarios('cloud')" class="scen-filter-btn px-2.5 py-1 rounded bg-bou-900 hover:bg-bou-850 text-slate-300" data-filter="cloud">Cloud, APIs & Tokens</button>
                        <button onclick="filterScenarios('malware')" class="scen-filter-btn px-2.5 py-1 rounded bg-bou-900 hover:bg-bou-850 text-slate-300" data-filter="malware">Ransomware & Supply Chain</button>
                        <button onclick="filterScenarios('ai')" class="scen-filter-btn px-2.5 py-1 rounded bg-bou-900 hover:bg-bou-850 text-slate-300" data-filter="ai">AI & Insider Threats</button>
                    </div>

                    <button onclick="randomizeScenario()" class="px-4 py-2 rounded bg-gradient-to-r from-bou-crimson to-bou-amber text-white font-bold text-xs hover:brightness-110 transition shadow-lg flex items-center gap-2 font-mono animate-pulse">
                        <span>🎲 Random Incident Drill</span>
                    </button>
                </div>

                <!-- 8 Interactive Scenario Cards Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-6" id="scenarioGrid">
                    <!-- 0: RTGS -->
                    <button onclick="loadScenario(0)" id="scenBtn0" class="scen-card p-3 text-left rounded-lg bg-bou-950 border border-bou-gold text-white font-mono text-xs transition" data-category="rails">
                        <div class="flex justify-between items-center text-xxs">
                            <span class="text-bou-gold font-bold">SCENARIO A</span>
                            <span class="text-bou-crimson font-bold">CRITICAL</span>
                        </div>
                        <div class="font-bold mt-1 text-xs">RTGS In-Memory Wire</div>
                        <div class="text-slate-400 text-xxs mt-1">4.8B UGX Injection • PID 4128 Hook</div>
                    </button>

                    <!-- 1: Ransomware -->
                    <button onclick="loadScenario(1)" id="scenBtn1" class="scen-card p-3 text-left rounded-lg bg-bou-950 border border-slate-800 text-slate-400 hover:text-white font-mono text-xs transition" data-category="malware">
                        <div class="flex justify-between items-center text-xxs">
                            <span class="text-bou-crimson font-bold">SCENARIO B</span>
                            <span class="text-bou-crimson font-bold">CRITICAL</span>
                        </div>
                        <div class="font-bold mt-1 text-xs">Hypervisor Ransomware</div>
                        <div class="text-slate-400 text-xxs mt-1">ESXi & SAN Locked • Double Extortion</div>
                    </button>

                    <!-- 2: Insider -->
                    <button onclick="loadScenario(2)" id="scenBtn2" class="scen-card p-3 text-left rounded-lg bg-bou-950 border border-slate-800 text-slate-400 hover:text-white font-mono text-xs transition" data-category="ai">
                        <div class="flex justify-between items-center text-xxs">
                            <span class="text-bou-cyan font-bold">SCENARIO C</span>
                            <span class="text-bou-amber font-bold">HIGH</span>
                        </div>
                        <div class="font-bold mt-1 text-xs">Core Banking Insider</div>
                        <div class="text-slate-400 text-xxs mt-1">Ledger Update • Redo Log Fraud</div>
                    </button>

                    <!-- 3: SWIFT / HSM -->
                    <button onclick="loadScenario(3)" id="scenBtn3" class="scen-card p-3 text-left rounded-lg bg-bou-950 border border-slate-800 text-slate-400 hover:text-white font-mono text-xs transition" data-category="rails">
                        <div class="flex justify-between items-center text-xxs">
                            <span class="text-bou-gold font-bold">SCENARIO D</span>
                            <span class="text-bou-crimson font-bold">CRITICAL</span>
                        </div>
                        <div class="font-bold mt-1 text-xs">SWIFT Alliance Gateway</div>
                        <div class="text-slate-400 text-xxs mt-1">HSM Key Bypass • MT103 Forgery</div>
                    </button>

                    <!-- 4: Cloud API Token -->
                    <button onclick="loadScenario(4)" id="scenBtn4" class="scen-card p-3 text-left rounded-lg bg-bou-950 border border-slate-800 text-slate-400 hover:text-white font-mono text-xs transition" data-category="cloud">
                        <div class="flex justify-between items-center text-xxs">
                            <span class="text-bou-purple-400 font-bold">SCENARIO E</span>
                            <span class="text-bou-amber font-bold">HIGH</span>
                        </div>
                        <div class="font-bold mt-1 text-xs">Payment Switch Cloud API</div>
                        <div class="text-slate-400 text-xxs mt-1">OAuth Token Replay • AWS CloudTrail</div>
                    </button>

                    <!-- 5: AI Deepfake -->
                    <button onclick="loadScenario(5)" id="scenBtn5" class="scen-card p-3 text-left rounded-lg bg-bou-950 border border-slate-800 text-slate-400 hover:text-white font-mono text-xs transition" data-category="ai">
                        <div class="flex justify-between items-center text-xxs">
                            <span class="text-bou-emerald font-bold">SCENARIO F</span>
                            <span class="text-bou-amber font-bold">HIGH</span>
                        </div>
                        <div class="font-bold mt-1 text-xs">AI Voice Deepfake Fraud</div>
                        <div class="text-slate-400 text-xxs mt-1">Executive Audio Clone • Spectral Triage</div>
                    </button>

                    <!-- 6: Supply Chain -->
                    <button onclick="loadScenario(6)" id="scenBtn6" class="scen-card p-3 text-left rounded-lg bg-bou-950 border border-slate-800 text-slate-400 hover:text-white font-mono text-xs transition" data-category="malware">
                        <div class="flex justify-between items-center text-xxs">
                            <span class="text-bou-amber font-bold">SCENARIO G</span>
                            <span class="text-bou-crimson font-bold">CRITICAL</span>
                        </div>
                        <div class="font-bold mt-1 text-xs">ACH Clearing Supply Chain</div>
                        <div class="text-slate-400 text-xxs mt-1">Backdoored DLL • 14 Banks Contagion</div>
                    </button>

                    <!-- 7: Cross-Border EAPS -->
                    <button onclick="loadScenario(7)" id="scenBtn7" class="scen-card p-3 text-left rounded-lg bg-bou-950 border border-slate-800 text-slate-400 hover:text-white font-mono text-xs transition" data-category="rails">
                        <div class="flex justify-between items-center text-xxs">
                            <span class="text-bou-goldLight font-bold">SCENARIO H</span>
                            <span class="text-bou-crimson font-bold">CRITICAL</span>
                        </div>
                        <div class="font-bold mt-1 text-xs">EAPS Mobile Float Arbitrage</div>
                        <div class="text-slate-400 text-xxs mt-1">Kampala-Nairobi Corridor • Synthetic KES</div>
                    </button>
                </div>
'''

# Replace old scenario button grid
pattern_old_grid = re.compile(r'<!-- Scenario Selector for TTX -->.*?</div>\s+</div>', re.DOTALL)
if pattern_old_grid.search(content):
    content = pattern_old_grid.sub(new_scenario_ui.strip(), content)
    print("Replaced scenario button grid.")
else:
    print("Warning: old scenario grid pattern not matched directly.")

# 2. Comprehensive 8 Scenarios Data in JavaScript
new_js_scenarios = r'''
        // 8 Comprehensive Central Bank Cyber Forensics Scenarios
        const scenarios = [
            // 0: RTGS Wire Injection
            {
                name: "Scenario A: RTGS In-Memory Wire Injection",
                steps: [
                    {
                        phase: "PHASE 1: DETECTION & INITIAL TRIAGE",
                        title: "The 06:28 EAT RTGS Batch Alarm",
                        prompt: "At 06:28 EAT, an unauthorized wire transfer of <strong>UGX 4,800,000,000</strong> is queued on payment engine <code>BOU-RTGS-SRV01</code> destined for foreign account <code>CR-8831-EXT</code>. Telemetry shows the dual-signer signature service was memory-patched. What is your immediate containment action?",
                        choices: [
                            { text: "Pull the physical power cable from the server rack immediately.", correct: false, penalty: 30, feedback: "CRITICAL FORENSIC ERROR: Pulling power destroyed volatile RAM! The memory-injected hook and active C2 keys are lost forever." },
                            { text: "Isolate VLAN 40 & capture volatile RAM bitstream under hardware write-blocker.", correct: true, feedback: "EXEMPLARY FORENSIC ACTION: Halted transaction dispatch while safeguarding RAM evidence under RFC 3227 and ISO 27037 standards." },
                            { text: "Allow the transfer to proceed to trace external bank beneficiaries.", correct: false, penalty: 50, feedback: "FATAL BREACH: UGX 4.8B settled and was instantly split into cryptocurrency tumblers. Sovereign funds lost!" }
                        ]
                    },
                    {
                        phase: "PHASE 2: PRIVILEGE ESCALATION INVESTIGATION",
                        title: "Tracing the Intrusion Source",
                        prompt: "RAM analysis confirms process <code>bou_rtgs_service.exe</code> (PID 4128) was hooked. How did the threat actor obtain SYSTEM-level access?",
                        choices: [
                            { text: "Correlate Event ID 4624 & dump LSASS memory for NTLM hash theft artifacts.", correct: true, feedback: "EXACT FINDING: Identified pass-the-hash attack originating from unpatched vendor VPN host 10.12.4.15." },
                            { text: "Format the server drive and restore yesterday's backup.", correct: false, penalty: 40, feedback: "EVIDENCE DESTRUCTION: You destroyed the primary evidence needed for prosecution under the Uganda Computer Misuse Act." },
                            { text: "Reboot the server into Safe Mode.", correct: false, penalty: 20, feedback: "FLAWED PROCEDURE: Reboot wiped volatile RAM state and failed to address root cause." }
                        ]
                    },
                    {
                        phase: "PHASE 3: ENTERPRISE CONTAINMENT",
                        title: "Threat Actor Counter-Move",
                        prompt: "Realizing their settlement batch was frozen, the adversary attempts lateral spread via domain Kerberos tickets. How do you evict them?",
                        choices: [
                            { text: "Double-rotate Active Directory krbtgt password & push YARA rule across server VLANs.", correct: true, feedback: "MASTERCLASS CSIRT EXECUTION: Invalidated all forged Golden Tickets and stopped wiper spread." },
                            { text: "Block internet access only at the external firewall.", correct: false, penalty: 25, feedback: "CONTAINMENT FAILURE: Attacker was already inside internal financial subnets using lateral SMB." }
                        ]
                    },
                    {
                        phase: "PHASE 4: JUDICIAL DOSSIER",
                        title: "High Court of Uganda Testimony",
                        prompt: "At trial, the defense files a motion alleging the server logs are unauthenticated hearsay. How do you certify admissibility?",
                        choices: [
                            { text: "Present dual SHA-256 matches, hardware write-blocker logs & unbroken custody ledger.", correct: true, feedback: "JUDICIAL VICTORY: Electronic evidence admitted under Section 8 of the Electronic Signatures Act & Computer Misuse Act." },
                            { text: "Provide unhashed paper printouts of the server event logs.", correct: false, penalty: 35, feedback: "EVIDENCE EXCLUDED: Court rejected unauthenticated printouts as inadmissible hearsay." }
                        ]
                    }
                ]
            },

            // 1: Hypervisor Ransomware
            {
                name: "Scenario B: Hypervisor Ransomware Outbreak",
                steps: [
                    {
                        phase: "PHASE 1: RANSOMWARE DETECTION",
                        title: "ESXi Virtual Disk Encryption Probe",
                        prompt: "At 02:00 EAT, multiple core banking database VMDK volumes begin throwing I/O errors. An unknown process is executing <code>esxcli vm process kill</code> across the primary SAN cluster. What is your first containment step?",
                        choices: [
                            { text: "Disconnect ESXi management network vSwitch & preserve SAN snapshots in read-only mode.", correct: true, feedback: "PERFECT CONTAINMENT: Prevented encryption payload from accessing immutable storage snapshots." },
                            { text: "Restart the storage SAN array immediately.", correct: false, penalty: 40, feedback: "DATA CORRUPTION: Hard reboot during write operations permanently corrupted database headers." },
                            { text: "Contact the attackers on Tor to ask for decryption price.", correct: false, penalty: 50, feedback: "GOVERNANCE BREACH: Bank of Uganda policy strictly prohibits ransom negotiations." }
                        ]
                    },
                    {
                        phase: "PHASE 2: INCIDENT RECOVERY",
                        title: "Clean Room Reconstruction",
                        prompt: "SAN immutable snapshots are secured. What is the verified procedure before bringing the Core Banking database back online?",
                        choices: [
                            { text: "Restore onto isolated clean-room infrastructure & perform offline hash/IoC verification.", correct: true, feedback: "SECURE RESTORATION: Verified zero persistence mechanisms remained before routing live transactions." },
                            { text: "Restore directly back onto original ESXi hosts without re-imaging.", correct: false, penalty: 30, feedback: "RE-INFECTION: Attacker cronjob executed wiper 15 minutes after restoration." }
                        ]
                    }
                ]
            },

            // 2: Core Banking Insider
            {
                name: "Scenario C: Core Banking Insider Manipulation",
                steps: [
                    {
                        phase: "PHASE 1: FRAUDULENT RECONCILIATION",
                        title: "Ledger Discrepancy Alert",
                        prompt: "IT Audit detects an unexplained UGX 850,000,000 ledger balance discrepancy between core settlement and treasury GL accounts. An internal database administrator claims it was a database index corruption. How do you investigate?",
                        choices: [
                            { text: "Extract binary transaction logs & compare database redo logs with network packet captures.", correct: true, feedback: "FRAUD UNCOVERED: Redo logs revealed direct SQL `UPDATE` query executed from internal DBA console." },
                            { text: "Accept the DBA's explanation and run database repair script.", correct: false, penalty: 45, feedback: "AUDIT FAILURE: The DBA had secretly diverted funds to an offshore intermediary." }
                        ]
                    }
                ]
            },

            // 3: SWIFT Alliance Gateway & HSM
            {
                name: "Scenario D: SWIFT Alliance Gateway & HSM Compromise",
                steps: [
                    {
                        phase: "PHASE 1: SUSPICIOUS FINANCIAL MESSAGING",
                        title: "04:12 EAT — Anomalous MT103 Settlement Outflow",
                        prompt: "SWIFT Relationship Management Application (RMA) flags 6 uncharacteristic MT103 payment instructions for <strong>USD 14,200,000</strong> directed to an unfamiliar correspondent bank in Eastern Europe. The Hardware Security Module (HSM) shows normal signing events. What is your immediate diagnostic step?",
                        choices: [
                            { text: "Verify local Alliance Gateway operator session tokens & inspect SWIFT message PDF printer spoolers.", correct: true, feedback: "CRUCIAL DISCOVERY: You uncover malware mimicking the Bangladesh Bank attack (Hermes trojan), which manipulated local SWIFT database records and suppressed printed confirmation receipts." },
                            { text: "Revoke SWIFT network connection at the ISP border immediately.", correct: false, penalty: 30, feedback: "PREMATURE CUTOFF: Severed global interbank communications before extracting in-flight payment message hashes." },
                            { text: "Authorize the payments under assumption of treasury foreign exchange operations.", correct: false, penalty: 60, feedback: "DISASTER: USD 14.2M foreign reserves settled across correspondent banks and became unrecoverable." }
                        ]
                    },
                    {
                        phase: "PHASE 2: SWIFT ENVIRONMENT ISOLATION",
                        title: "Hardening the SWIFT Customer Security Programme (CSP)",
                        prompt: "Malware was confirmed on the local Alliance Access server. What architectural control prevents recurring tampering?",
                        choices: [
                            { text: "Enforce strict HSM dual-custody physical smartcards & isolate SWIFT messaging VLAN to dedicated jump-boxes.", correct: true, feedback: "EXEMPLARY COMPLIANCE: Aligned with mandatory SWIFT CSP controls 1.1 and 2.1, eliminating single-operator compromise." },
                            { text: "Allow remote RDP administration of SWIFT gateway over VPN.", correct: false, penalty: 35, feedback: "COMPLIANCE BREACH: Severe violation of SWIFT Customer Security Programme standards." }
                        ]
                    }
                ]
            },

            // 4: Payment Switch Cloud API & Token Replay
            {
                name: "Scenario E: Payment Switch Cloud API & Token Replay",
                steps: [
                    {
                        phase: "PHASE 1: API ABUSE ANOMALY",
                        title: "Spike in Unsigned Settlement Invocations",
                        prompt: "The Bank's hybrid cloud interbank settlement API (hosted on AWS/Azure) triggers an alarm: a single OAuth Bearer token is issuing 1,200 requests per minute from non-whitelisted IP addresses in South America. What is your first forensic action?",
                        choices: [
                            { text: "Immediately revoke the compromised OAuth client secret & examine CloudTrail for AssumeRoleWithWebIdentity calls.", correct: true, feedback: "THREAT CONTAINED: Stopped token replay attack and isolated leaked CI/CD pipeline environment variables." },
                            { text: "Increase API rate limiting threshold to prevent server crash.", correct: false, penalty: 40, feedback: "FRAUD EXPEDITION: Allowed the attacker to execute 8,000 unauthorized transaction validation queries." }
                        ]
                    }
                ]
            },

            // 5: AI Voice Deepfake
            {
                name: "Scenario F: AI Voice Deepfake Executive Impersonation",
                steps: [
                    {
                        phase: "PHASE 1: SOCIAL ENGINEERING INTERCEPTION",
                        title: "Urgent Voice Call to Treasury Operations",
                        prompt: "A commercial bank settlement officer receives an urgent WhatsApp audio call from someone with the exact voice, cadence, and breath patterns of the BoU Executive Director ordering an immediate emergency liquidity transfer of UGX 12 Billion. What protocol must be enforced?",
                        choices: [
                            { text: "Reject verbal authorization; enforce mandatory out-of-band PKI digital signature with hardware token.", correct: true, feedback: "ATTACK THWARTED: Spectral analysis proved audio was synthesized using an advanced RVC voice clone. PKI dual-signing blocked the fraud." },
                            { text: "Process transfer immediately due to the seniority of the caller.", correct: false, penalty: 60, feedback: "CATASTROPHIC FAILURE: Commercial bank fell victim to executive voice cloning; UGX 12 Billion disbursed unlawfully." }
                        ]
                    }
                ]
            },

            // 6: ACH Clearing Supply Chain
            {
                name: "Scenario G: ACH Clearing Supply Chain Backdoor",
                steps: [
                    {
                        phase: "PHASE 1: INTERBANK CONTAGION",
                        title: "Backdoored Automated Clearing House (ACH) Update",
                        prompt: "A trusted vendor of the interbank clearing system pushes an auto-update. Within 30 minutes, 14 commercial banks experience outbound C2 beaconing to a foreign domain. How does the Central Bank CSIRT respond?",
                        choices: [
                            { text: "Issue emergency EAPS/ACH operational suspension & distribute YARA signature to scan the backdoored DLL across all member banks.", correct: true, feedback: "SYSTEMIC DEFENSE: Successfully quarantined supply-chain payload before fraudulent overnight clearing batches settled." },
                            { text: "Blame member commercial banks and instruct them to handle it individually.", correct: false, penalty: 45, feedback: "SYSTEMIC RUNAWAY: 4 commercial banks suffered automated clearing batch manipulation overnight." }
                        ]
                    }
                ]
            },

            // 7: EAPS Cross-Border Mobile Float
            {
                name: "Scenario H: EAPS Cross-Border Mobile Float Arbitrage",
                steps: [
                    {
                        phase: "PHASE 1: REGIONAL SETTLEMENT FRAUD",
                        title: "Kampala ↔ Nairobi Currency Float Discrepancy",
                        prompt: "A telecom mobile money switch integration across the Uganda-Kenya border reports a phantom KES 250,000,000 credit injection without corresponding UGX debit at the Bank of Uganda settlement node. What cross-border forensic action is taken?",
                        choices: [
                            { text: "Invoke bilateral BoU-CBK emergency CSIRT bridge & freeze recipient escrow wallets under EAC Article 124 protocol.", correct: true, feedback: "COORDINATED TRIAGE: Both central banks synchronized telemetries, unmasking an API race-condition exploit and recovering 100% of the funds." },
                            { text: "Assume currency conversion rounding discrepancy and resolve at end of week.", correct: false, penalty: 50, feedback: "EXTREME NEGLIGENCE: Phantom credit was cashed out through multi-currency cross-border agent networks." }
                        ]
                    }
                ]
            }
        ];
'''

# Replace the scenarios array in JavaScript
pattern_old_scen_js = re.compile(r'let currentScenarioIdx = 0;\s+let currentStepIdx = 0;\s+const scenarios = \[.*?\];\s+function loadScenario', re.DOTALL)
replacement_js = r'''let currentScenarioIdx = 0;
        let currentStepIdx = 0;
''' + new_js_scenarios + r'''
        // Scenario Filter & Randomizer Functions
        function filterScenarios(domain) {
            playTone(600, 'sine', 0.04);
            document.querySelectorAll('.scen-filter-btn').forEach(b => {
                const isAct = b.getAttribute('data-filter') === domain;
                b.className = isAct 
                    ? 'scen-filter-btn active px-2.5 py-1 rounded bg-bou-gold text-bou-950 font-bold'
                    : 'scen-filter-btn px-2.5 py-1 rounded bg-bou-900 hover:bg-bou-850 text-slate-300';
            });

            document.querySelectorAll('.scen-card').forEach(card => {
                const cat = card.getAttribute('data-category');
                if (domain === 'all' || cat === domain) {
                    card.classList.remove('hidden');
                } else {
                    card.classList.add('hidden');
                }
            });
        }

        function randomizeScenario() {
            playTone(900, 'triangle', 0.1);
            setTimeout(() => playTone(1200, 'triangle', 0.15), 100);
            
            // Random index 0 to 7
            const randIdx = Math.floor(Math.random() * scenarios.length);
            loadScenario(randIdx);

            // Visual feedback flash
            const btn = document.getElementById('scenBtn' + randIdx);
            if (btn) {
                btn.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                btn.classList.add('animate-pulse-gold');
                setTimeout(() => btn.classList.remove('animate-pulse-gold'), 1500);
            }
        }

        function loadScenario'''

if pattern_old_scen_js.search(content):
    content = pattern_old_scen_js.sub(replacement_js, content)
    print("Replaced javascript scenarios array and added filter/randomizer functions.")
else:
    print("Warning: old js scenarios pattern not matched directly.")

# Update the loadScenario function loop to 8 items
content = content.replace("for (let i = 0; i < 3; i++) {", "for (let i = 0; i < scenarios.length; i++) {")

with open(SRC_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated {SRC_FILE} successfully with 8 scenarios! ({len(content)} bytes)")

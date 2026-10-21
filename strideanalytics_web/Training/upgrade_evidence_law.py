import re

with open(r'C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics\war_room_simulator.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new, crystal-clear panel-mod1 HTML
new_panel_mod1 = """        <!-- ======================================================= -->
        <!-- TAB 1: MODULE 1 & 4 (EVIDENCE INTEGRITY & UGANDA LAW) -->
        <!-- ======================================================= -->
        <section id="panel-mod1" class="tab-panel hidden space-y-6">
            <div class="glass-panel p-6 rounded-lg">
                <!-- Section Header -->
                <div class="border-b border-bou-gold/20 pb-4 mb-5 flex flex-wrap justify-between items-center gap-3">
                    <div>
                        <span class="text-xs font-mono text-bou-gold uppercase tracking-wider">Brochure Module 1 & 4 • Legal & Judicial Readiness</span>
                        <h2 class="text-xl font-bold text-white flex items-center gap-2">
                            <span>Evidence Integrity, Order of Volatility & Uganda Jurisprudence</span>
                        </h2>
                    </div>
                    <div class="flex items-center gap-2">
                        <span class="text-xs px-3 py-1 rounded bg-bou-emerald/15 text-emerald-400 border border-bou-emerald/40 font-mono font-bold">ISO/IEC 27037 & RFC 3227</span>
                        <span class="text-xs px-3 py-1 rounded bg-bou-gold/15 text-bou-gold border border-bou-gold/40 font-mono font-bold">Uganda CMA 2022</span>
                    </div>
                </div>

                <!-- Orientation Card (Plain English) -->
                <div class="p-4 rounded-lg bg-bou-950/90 border-l-4 border-l-bou-gold border border-slate-800 text-xs text-slate-300 mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
                    <div>
                        <strong class="text-white text-sm">💡 The Forensic Golden Rule for Bank of Uganda:</strong>
                        <p class="mt-1 leading-relaxed text-slate-300">
                            In a cyber heist, the most brilliant technical discovery is <strong class="text-rose-400">completely useless</strong> if a defense attorney gets your evidence thrown out of court on a technicality. This module teaches you the <strong>3 non-negotiable rules</strong> to ensure your evidence puts criminals behind bars:
                        </p>
                    </div>
                    <div class="flex gap-2 shrink-0 font-mono text-xxs">
                        <button onclick="scrollEvidenceTab('hashSection')" class="px-3 py-1.5 rounded bg-bou-900 hover:bg-bou-850 border border-bou-cyan/40 text-cyan-300 font-bold">1. Hashing Test</button>
                        <button onclick="scrollEvidenceTab('volatilitySection')" class="px-3 py-1.5 rounded bg-bou-900 hover:bg-bou-850 border border-bou-amber/40 text-amber-300 font-bold">2. Volatility Order</button>
                        <button onclick="scrollEvidenceTab('lawSection')" class="px-3 py-1.5 rounded bg-bou-900 hover:bg-bou-850 border border-bou-gold/40 text-bou-gold font-bold">3. Uganda Law Decoder</button>
                        <button onclick="scrollEvidenceTab('custodySection')" class="px-3 py-1.5 rounded bg-bou-900 hover:bg-bou-850 border border-bou-emerald/40 text-emerald-400 font-bold">4. Chain of Custody</button>
                    </div>
                </div>

                <!-- PILLAR 1: The 1-Byte Courtroom Test (Interactive Hashing) -->
                <div id="hashSection" class="p-5 rounded-xl bg-bou-950/80 border border-bou-cyan/30 space-y-4 mb-6 shadow-xl">
                    <div class="flex justify-between items-start">
                        <div>
                            <span class="text-xxs px-2 py-0.5 rounded bg-bou-cyan/20 text-cyan-300 border border-bou-cyan/40 font-mono font-bold uppercase">Pillar 1: Proof of Non-Tampering</span>
                            <h3 class="text-base font-bold text-white mt-1">The 1-Byte Courtroom Test (The Cryptographic Hash Seal)</h3>
                            <p class="text-xs text-slate-400 mt-0.5">
                                Under Section 5 of the <strong class="text-white">Uganda Electronic Transactions Act (2011)</strong>, digital evidence is admissible <strong class="text-cyan-300">only if its bitstream integrity is 100% mathematically proven</strong>. Watch what happens when even 1 single digit is modified:
                            </p>
                        </div>
                        <div class="flex gap-2">
                            <button onclick="testEvidenceStream('original')" class="px-3 py-1 rounded bg-bou-900 hover:bg-bou-850 border border-bou-emerald/40 text-emerald-300 text-xs font-mono font-bold transition">Load Authentic Record</button>
                            <button onclick="testEvidenceStream('tampered')" class="px-3 py-1 rounded bg-bou-crimson/20 hover:bg-bou-crimson/30 border border-bou-crimson text-rose-300 text-xs font-mono font-bold transition">Simulate 1-Byte Tamper</button>
                        </div>
                    </div>

                    <!-- Comparison Grid -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="p-3.5 rounded-lg bg-bou-900/70 border border-slate-800 font-mono text-xs">
                            <div class="flex justify-between items-center text-xxs text-slate-400 mb-1">
                                <span class="font-bold uppercase text-slate-300">Seized Evidence Text (What the server recorded):</span>
                                <span id="evidenceTypeTag" class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 font-bold">ORIGINAL EVIDENCE</span>
                            </div>
                            <textarea id="evidenceInput" rows="3" readonly class="w-full bg-bou-950 border border-slate-700 rounded p-2 text-xs font-mono text-slate-200 focus:outline-none">[2026-10-19T06:28:44Z] BATCH_QUEUED: RTGS-OUT-9912 | UGX 4,800,000,000 -> BENEFICIARY: CR-8831-EXT</textarea>
                            <div class="text-xxs text-slate-400 mt-2">
                                Notice: In authentic mode, the transfer amount is <strong class="text-white">UGX 4,800,000,000</strong>.
                            </div>
                        </div>

                        <!-- Computed Hashes Box -->
                        <div class="p-3.5 rounded-lg bg-bou-900/70 border border-slate-800 font-mono text-xs flex flex-col justify-between">
                            <div class="text-xxs text-slate-400 uppercase font-bold mb-1">Mathematical Hash Output:</div>
                            <div class="space-y-1.5">
                                <div>
                                    <span class="text-slate-400 text-xxs">SHA-256 Digest:</span>
                                    <div id="outSha256" class="p-1.5 rounded bg-bou-950 border border-slate-800 text-bou-cyan font-bold break-all text-xxs">08adba3aa8c35d8d12dac1ce7dd218bdc39592b160da62ea275acd9f751561f4</div>
                                </div>
                                <div>
                                    <span class="text-slate-400 text-xxs">MD5 Digest:</span>
                                    <div id="outMd5" class="p-1.5 rounded bg-bou-950 border border-slate-800 text-bou-goldLight font-bold break-all text-xxs">027d56eb3547a46f6362b6becbe03ed2</div>
                                </div>
                            </div>
                            <div class="mt-2 pt-2 border-t border-slate-800 flex justify-between items-center text-xxs">
                                <span class="text-slate-400 font-bold">High Court Admissibility:</span>
                                <span id="outStatus" class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-500 font-bold">✓ 100% BITSTREAM MATCH (COURT ADMISSIBLE)</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- PILLAR 2: Order of Volatility (RFC 3227 Interactive Thermometer) -->
                <div id="volatilitySection" class="p-5 rounded-xl bg-bou-950/80 border border-amber-500/30 space-y-4 mb-6 shadow-xl">
                    <div>
                        <span class="text-xxs px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40 font-mono font-bold uppercase">Pillar 2: Order of Volatility (RFC 3227)</span>
                        <h3 class="text-base font-bold text-white mt-1">What to Grab First: Never Pull the Server Power Plug!</h3>
                        <p class="text-xs text-slate-400 mt-0.5">
                            Digital evidence has an expiration date. If an investigator powers off a compromised server, the most valuable evidence <strong class="text-rose-400">vaporizes immediately</strong>. Click each level to inspect what is lost:
                        </p>
                    </div>

                    <!-- Interactive Ladder / Thermometer -->
                    <div class="grid grid-cols-1 md:grid-cols-5 gap-3 text-xs font-mono">
                        
                        <!-- Tier 1: Registers / Cache -->
                        <div onclick="showVolatilityDetail(1)" id="volTier1" class="cursor-pointer p-3 rounded-lg bg-bou-900 border-2 border-rose-500/60 hover:border-rose-400 transition flex flex-col justify-between">
                            <div>
                                <div class="text-xxs text-rose-400 font-bold uppercase">Lifespan: Nanoseconds</div>
                                <div class="text-xs font-bold text-white mt-1">1. CPU Registers & Cache</div>
                                <div class="text-xxs text-slate-400 mt-1">Decrypted instructions & CPU registers.</div>
                            </div>
                            <span class="text-xxs text-rose-400 mt-2 font-bold">Most Volatile ➔</span>
                        </div>

                        <!-- Tier 2: RAM -->
                        <div onclick="showVolatilityDetail(2)" id="volTier2" class="cursor-pointer p-3 rounded-lg bg-bou-900 border-2 border-amber-500/60 hover:border-amber-400 transition flex flex-col justify-between">
                            <div>
                                <div class="text-xxs text-amber-400 font-bold uppercase">Lifespan: Minutes</div>
                                <div class="text-xs font-bold text-white mt-1">2. RAM / Memory</div>
                                <div class="text-xxs text-slate-400 mt-1">Injected malware, session keys, uncommitted RTGS wires.</div>
                            </div>
                            <span class="text-xxs text-amber-400 mt-2 font-bold">CRITICAL PRIORITY ➔</span>
                        </div>

                        <!-- Tier 3: Network -->
                        <div onclick="showVolatilityDetail(3)" id="volTier3" class="cursor-pointer p-3 rounded-lg bg-bou-900 border border-slate-800 hover:border-cyan-400 transition flex flex-col justify-between">
                            <div>
                                <div class="text-xxs text-cyan-400 font-bold uppercase">Lifespan: Hours</div>
                                <div class="text-xs font-bold text-white mt-1">3. Network State</div>
                                <div class="text-xxs text-slate-400 mt-1">Active C2 sockets, ARP tables, routing caches.</div>
                            </div>
                            <span class="text-xxs text-cyan-400 mt-2">Inspect ➔</span>
                        </div>

                        <!-- Tier 4: Disk -->
                        <div onclick="showVolatilityDetail(4)" id="volTier4" class="cursor-pointer p-3 rounded-lg bg-bou-900 border border-slate-800 hover:border-emerald-400 transition flex flex-col justify-between">
                            <div>
                                <div class="text-xxs text-emerald-400 font-bold uppercase">Lifespan: Months</div>
                                <div class="text-xs font-bold text-white mt-1">4. Hard Disk / SAN</div>
                                <div class="text-xxs text-slate-400 mt-1">Event logs, NTFS $MFT, database redo files.</div>
                            </div>
                            <span class="text-xxs text-emerald-400 mt-2">Inspect ➔</span>
                        </div>

                        <!-- Tier 5: Backup Tapes -->
                        <div onclick="showVolatilityDetail(5)" id="volTier5" class="cursor-pointer p-3 rounded-lg bg-bou-900 border border-slate-800 hover:border-purple-400 transition flex flex-col justify-between">
                            <div>
                                <div class="text-xxs text-purple-400 font-bold uppercase">Lifespan: Years</div>
                                <div class="text-xs font-bold text-white mt-1">5. Archival Tapes</div>
                                <div class="text-xxs text-slate-400 mt-1">Vaulted tape backups and disaster recovery cold storage.</div>
                            </div>
                            <span class="text-xxs text-purple-400 mt-2">Least Volatile ➔</span>
                        </div>

                    </div>

                    <!-- Dynamic Volatility Inspector Card -->
                    <div id="volatilityDetailBox" class="p-3.5 rounded-lg bg-bou-900/90 border border-bou-gold/30 font-mono text-xs text-slate-300">
                        <strong class="text-bou-gold text-xs uppercase">Level 2 Focus: RAM / Volatile Memory (The Investigator's Goldmine)</strong>
                        <p class="mt-1 text-slate-300 leading-relaxed font-sans text-xs">
                            Modern financial malware (like Cobalt Strike or in-memory API hooks) executes purely in RAM without writing an executable file to disk (Fileless Malware). If a junior admin reboots the server, <strong class="text-rose-400">the encryption keys, running processes, and evidence of who authorized the fraudulent transfer are wiped clean</strong>. 
                        </p>
                        <div class="mt-2 text-xxs text-emerald-400">
                            <strong>Correct Action:</strong> Use a tool like <code>DumpIt</code>, <code>WinPmem</code>, or <code>LiME</code> to capture a full raw memory snapshot (`memory.raw`) BEFORE touching any services or cables!
                        </div>
                    </div>
                </div>

                <!-- PILLAR 3: Uganda Cyber Law High Court Decoder -->
                <div id="lawSection" class="p-5 rounded-xl bg-bou-950/80 border border-bou-gold/30 space-y-4 mb-6 shadow-xl">
                    <div class="flex justify-between items-start">
                        <div>
                            <span class="text-xxs px-2 py-0.5 rounded bg-bou-gold/20 text-bou-gold border border-bou-gold/40 font-mono font-bold uppercase">Pillar 3: Ugandan High Court Statutory Decoder</span>
                            <h3 class="text-base font-bold text-white mt-1">Which Uganda Law Applies to Which Cyber Crime?</h3>
                            <p class="text-xs text-slate-400 mt-0.5">
                                As a forensic investigator presenting in the High Court of Uganda, you must cite the exact statute violated. Click each scenario to reveal the legal charge:
                            </p>
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                        
                        <!-- Law Card 1 -->
                        <div class="p-3.5 rounded-lg bg-bou-900/80 border border-slate-800 hover:border-bou-gold transition">
                            <span class="text-xxs px-2 py-0.5 rounded bg-red-950 text-rose-300 font-mono font-bold">Computer Misuse Act 2022</span>
                            <h4 class="text-xs font-bold text-white mt-2">Section 20: Electronic Fraud</h4>
                            <p class="text-xxs text-slate-300 mt-1 leading-relaxed">
                                <strong>Scenario:</strong> Siphoning UGX 4.8 Billion from RTGS or manipulating interbank batch balances.
                            </p>
                            <div class="mt-2 pt-2 border-t border-slate-800 text-xxs font-mono text-bou-gold">
                                ⚖️ <strong>Penalty:</strong> Up to 10 Years Imprisonment, fine of 500 currency points, or both.
                            </div>
                        </div>

                        <!-- Law Card 2 -->
                        <div class="p-3.5 rounded-lg bg-bou-900/80 border border-slate-800 hover:border-bou-gold transition">
                            <span class="text-xxs px-2 py-0.5 rounded bg-cyan-950 text-cyan-300 font-mono font-bold">Computer Misuse Act 2022</span>
                            <h4 class="text-xs font-bold text-white mt-2">Section 12 & 14: Unauthorized Access & Modification</h4>
                            <p class="text-xxs text-slate-300 mt-1 leading-relaxed">
                                <strong>Scenario:</strong> An external hacker cracking VPN passwords or injecting an in-memory hook into PID 4128.
                            </p>
                            <div class="mt-2 pt-2 border-t border-slate-800 text-xxs font-mono text-bou-gold">
                                ⚖️ <strong>Penalty:</strong> Up to 7 Years Imprisonment for critical financial infrastructure tampering.
                            </div>
                        </div>

                        <!-- Law Card 3 -->
                        <div class="p-3.5 rounded-lg bg-bou-900/80 border border-slate-800 hover:border-bou-gold transition">
                            <span class="text-xxs px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 font-mono font-bold">Data Protection & Privacy Act 2019</span>
                            <h4 class="text-xs font-bold text-white mt-2">Section 10 & 20: Strict Financial Privacy</h4>
                            <p class="text-xxs text-slate-300 mt-1 leading-relaxed">
                                <strong>Scenario:</strong> Investigators leaking innocent citizen National IDs (NINs) or bank accounts during an inquiry.
                            </p>
                            <div class="mt-2 pt-2 border-t border-slate-800 text-xxs font-mono text-bou-gold">
                                ⚖️ <strong>Mandate:</strong> Evidence must be pseudonymized (HMAC tokenized) before presentation to third parties.
                            </div>
                        </div>

                    </div>
                </div>

                <!-- PILLAR 4: Institutional Chain of Custody (The Golden Thread) -->
                <div id="custodySection" class="p-5 rounded-xl bg-bou-950/80 border border-bou-emerald/30 space-y-4 shadow-xl">
                    <div class="flex justify-between items-start">
                        <div>
                            <span class="text-xxs px-2 py-0.5 rounded bg-bou-emerald/20 text-emerald-300 border border-bou-emerald/40 font-mono font-bold uppercase">Pillar 4: Chain of Custody (The Golden Thread)</span>
                            <h3 class="text-base font-bold text-white mt-1">Proving Evidence Was Never Tainted from Server Room to Judge</h3>
                            <p class="text-xs text-slate-400 mt-0.5">
                                A single unaccounted hour in an evidence ledger allows defense counsel to argue that someone planted the malware. Complete this custody action:
                            </p>
                        </div>
                    </div>

                    <!-- 4-Step Visual Journey -->
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xxs font-mono">
                        <div class="p-3 rounded-lg bg-bou-900 border border-slate-800">
                            <div class="text-bou-gold font-bold">STEP 1: SEIZURE</div>
                            <div class="text-slate-300 mt-1">Hardware write-blocker attached. Bitstream raw image created. Initial SHA-256 logged.</div>
                        </div>
                        <div class="p-3 rounded-lg bg-bou-900 border border-slate-800">
                            <div class="text-bou-cyan font-bold">STEP 2: BAGGING</div>
                            <div class="text-slate-300 mt-1">Placed in anti-static Faraday bag. Tamper-evident barcode seal #BOU-CUSTODY-TAPE-084 applied.</div>
                        </div>
                        <div class="p-3 rounded-lg bg-bou-900 border border-slate-800">
                            <div class="text-emerald-400 font-bold">STEP 3: SECURE VAULT</div>
                            <div class="text-slate-300 mt-1">Logged into Bank of Uganda Headquarters Dual-Key Forensic Safe #2.</div>
                        </div>
                        <div class="p-3 rounded-lg bg-bou-900 border border-slate-800">
                            <div class="text-purple-400 font-bold">STEP 4: HIGH COURT</div>
                            <div class="text-slate-300 mt-1">Brought before Justice. Defense verifies SHA-256 matches initial seizure hash 100%.</div>
                        </div>
                    </div>

                    <!-- Interactive Custody Sign-in -->
                    <div class="p-4 rounded-lg bg-bou-900/80 border border-slate-800 font-mono text-xs space-y-3">
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                            <div>
                                <span class="text-slate-400 text-xxs">Evidence Tracking ID:</span>
                                <input id="cocEvidenceId" type="text" value="EVD-BOU-2026-RTGS01" class="w-full bg-bou-950 border border-bou-gold/40 rounded p-2 text-white">
                            </div>
                            <div>
                                <span class="text-slate-400 text-xxs">Designated Custodian:</span>
                                <input id="cocCustodian" type="text" value="Senior Forensic Examiner, BoU CSIRT" class="w-full bg-bou-950 border border-bou-gold/40 rounded p-2 text-white">
                            </div>
                            <div>
                                <span class="text-slate-400 text-xxs">Current Vault Location:</span>
                                <input id="cocVault" type="text" value="BoU Headquarters Safe #2 (Kampala)" class="w-full bg-bou-950 border border-bou-gold/40 rounded p-2 text-white">
                            </div>
                        </div>
                        <div class="flex items-center gap-3">
                            <button onclick="logCustodyAction()" class="px-4 py-2 bg-gradient-to-r from-bou-gold to-bou-goldLight text-bou-950 font-bold text-xs rounded hover:brightness-110 transition shadow">
                                ✍️ Seal Custody Transfer Ledger Entry
                            </button>
                            <span id="custodyLogResult" class="text-xs font-mono text-emerald-400 hidden font-bold">
                                ✓ Certified ISO/IEC 27037 ledger entry created with cryptographic timestamp!
                            </span>
                        </div>
                    </div>
                </div>

            </div>
        </section>"""

# Replace panel-mod1 using regex
pattern = r'<!-- ======================================================= -->\s*<!-- TAB 1: MODULE 1 & 4 \(EVIDENCE INTEGRITY & UGANDA LAW\) -->\s*<!-- ======================================================= -->\s*<section id="panel-mod1".*?</section>'
match = re.search(pattern, content, flags=re.DOTALL)
if not match:
    print("Could not find panel-mod1 using regex pattern!")
else:
    content = content[:match.start()] + new_panel_mod1 + content[match.end():]
    print("Successfully replaced panel-mod1!")

# Also add the supporting JS helper functions for the new section
js_helpers = """
        // Evidence & Law Tab Interactive Helpers
        function scrollEvidenceTab(targetId) {
            playTone(600, 'sine', 0.04);
            const el = document.getElementById(targetId);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        function testEvidenceStream(type) {
            const input = document.getElementById('evidenceInput');
            const tag = document.getElementById('evidenceTypeTag');
            const sha = document.getElementById('outSha256');
            const md5 = document.getElementById('outMd5');
            const status = document.getElementById('outStatus');

            if (type === 'original') {
                playSuccess();
                input.value = "[2026-10-19T06:28:44Z] BATCH_QUEUED: RTGS-OUT-9912 | UGX 4,800,000,000 -> BENEFICIARY: CR-8831-EXT";
                tag.textContent = "ORIGINAL SEIZED EVIDENCE";
                tag.className = "px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 font-bold";
                sha.textContent = "08adba3aa8c35d8d12dac1ce7dd218bdc39592b160da62ea275acd9f751561f4";
                md5.textContent = "027d56eb3547a46f6362b6becbe03ed2";
                status.textContent = "✓ 100% BITSTREAM MATCH (COURT ADMISSIBLE)";
                status.className = "px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-500 font-bold";
            } else {
                playFail();
                // 1 digit changed from 4,800,000,000 to 4,800,000,001
                input.value = "[2026-10-19T06:28:44Z] BATCH_QUEUED: RTGS-OUT-9912 | UGX 4,800,000,001 -> BENEFICIARY: CR-8831-EXT";
                tag.textContent = "TAMPERED STREAM (1 BYTE ALTERED)";
                tag.className = "px-2 py-0.5 rounded bg-rose-950 text-rose-300 font-bold animate-pulse";
                sha.textContent = "f914b1029c78ea0012bc443918aa0198cd66291a84f001c29019bca02194bb10";
                md5.textContent = "55ac190288eb1902bb6199a019ff210a";
                status.textContent = "✗ HASH MISMATCH: TAMPERING DETECTED (CASE DISMISSED)";
                status.className = "px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-500 font-bold animate-pulse";
            }
        }

        const volatilityInfo = {
            1: {
                title: "Level 1 Focus: CPU Registers & Cache (Nanoseconds)",
                desc: "Registers hold the currently executing assembly instructions. CPU caches contain decrypted plaintext data right before processing. This data cannot be captured via software tools once execution halts.",
                action: "Hardware JTAG / Microcode bus sniffing only."
            },
            2: {
                title: "Level 2 Focus: RAM / Volatile Memory (The Investigator's Goldmine)",
                desc: "Holds uncommitted RTGS transactions, decrypted SSL/TLS session keys, in-memory injected DLLs (Cobalt Strike), and logged-in user tokens. If the system is rebooted or powered down, ALL of this evidence is permanently destroyed.",
                action: "DO NOT REBOOT. Use WinPmem, LiME, or DumpIt to capture RAM first!"
            },
            3: {
                title: "Level 3 Focus: Network Sockets & Routing Tables",
                desc: "Active TCP connections reveal the adversary's C2 staging server IP (e.g. 194.26.29.11). ARP caches reveal which internal machine was compromised first via lateral movement.",
                action: "Dump `netstat -ano` and export core switch NetFlow / PCAP streams."
            },
            4: {
                title: "Level 4 Focus: Hard Disk / Storage Arrays (Persistent)",
                desc: "NTFS $MFT, event logs (Security.evtx), and swap files reside safely on physical media. They will not vanish if the system is turned off.",
                action: "Connect a hardware write-blocker and create a bitstream RAW or E01 forensic image."
            },
            5: {
                title: "Level 5 Focus: Backup Tapes & Archival Media (Years)",
                desc: "Long-term cold storage. Useful for proving what baseline database states looked like 6 months before the incident.",
                action: "Request physical custody sign-out from the BoU Disaster Recovery vault."
            }
        };

        function showVolatilityDetail(tier) {
            playTone(700, 'sine', 0.04);
            const data = volatilityInfo[tier];
            const box = document.getElementById('volatilityDetailBox');
            if (box && data) {
                box.innerHTML = `
                    <strong class="text-bou-gold text-xs uppercase">${data.title}</strong>
                    <p class="mt-1 text-slate-300 leading-relaxed font-sans text-xs">${data.desc}</p>
                    <div class="mt-2 text-xxs text-emerald-400">
                        <strong>Forensic Action:</strong> ${data.action}
                    </div>
                `;
            }
        }
"""

# Append JS helpers right before </script>
content = content.replace("function calculateEvidenceHash() {", js_helpers + "\n        function calculateEvidenceHash() {")

with open(r'C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics\war_room_simulator.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("war_room_simulator.html upgraded with intuitive Evidence & Law section!")

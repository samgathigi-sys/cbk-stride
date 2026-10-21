"""
Add Kenya Cyberspace Case Studies & Federated Learning (BoU <-> CBK) to War Room Simulator
"""
import re

SRC_FILE = r"C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics\war_room_simulator.html"
with open(SRC_FILE, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Navigation Button
old_nav_anchor = '<span>📋 Mod 7: Executive Report</span>\n            </button>'
new_nav_btn = '''<span>📋 Mod 7: Executive Report</span>
            </button>
            <button onclick="switchTab('crossborder')" class="tab-btn px-4 py-3 text-xs md:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 transition" data-tab="crossborder">
                <span>🇰🇪 ↔ 🇺🇬 Regional Intel & Federated AI</span>
            </button>'''

if 'data-tab="crossborder"' not in content:
    content = content.replace(old_nav_anchor, new_nav_btn)
    print("Added crossborder nav button.")

# 2. Construct the Section HTML
crossborder_section = r'''
        <!-- ============================================================== -->
        <!-- TAB 7: REGIONAL INTEL & FEDERATED LEARNING (KENYA <-> UGANDA) -->
        <!-- ============================================================== -->
        <section id="panel-crossborder" class="tab-panel hidden space-y-6">
            <div class="glass-panel p-6 rounded-lg">
                <div class="border-b border-bou-gold/20 pb-4 mb-5 flex flex-col md:flex-row md:justify-between md:items-center gap-2">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="text-xs font-mono text-bou-gold uppercase tracking-wider">East African Sovereign Security Matrix</span>
                            <span class="text-xs px-2 py-0.5 rounded bg-bou-emerald/10 text-bou-emerald border border-bou-emerald/30 font-mono">CBK 🇰🇪 ↔ BoU 🇺🇬</span>
                        </div>
                        <h2 class="text-xl font-bold text-white mt-1">Cross-Border Cyberspace Parallels & Privacy-Preserving Federated AI</h2>
                    </div>
                    <span class="text-xs px-3 py-1 rounded bg-bou-cyan/10 text-bou-cyan border border-bou-cyan/30 font-mono">EAPS Payment Rails • Zero Data Leakage</span>
                </div>

                <!-- Strategic Introduction Banner -->
                <div class="p-4 rounded-lg bg-gradient-to-r from-bou-950 via-bou-900 to-bou-950 border border-bou-gold/30 text-xs text-slate-300 leading-relaxed mb-6">
                    <strong class="text-bou-goldLight text-sm font-bold block mb-1">🏛️ Strategic Context: Interconnected Financial Infrastructure in East Africa</strong>
                    Because the <strong class="text-white">East African Payment System (EAPS)</strong> and cross-border mobile money corridors connect the Bank of Uganda and the Central Bank of Kenya, an advanced threat syndicate targeting Nairobi or Kampala poses systemic risks to both sovereign economies. Below are real-world lessons from Kenyan cyberspace and an interactive blueprint for <strong class="text-bou-emerald">Federated Learning</strong> that enables collaborative threat detection without violating either nation's Data Protection Acts.
                </div>

                <!-- Section 1: Real-World Kenyan Cyberspace Incidents (Forensic Parallels) -->
                <div class="space-y-4 mb-8">
                    <h3 class="text-sm font-bold text-bou-gold uppercase font-mono tracking-wider flex items-center gap-2">
                        <span>🇰🇪 Case Studies from Kenyan Financial Cyberspace & Forensic Lessons</span>
                    </h3>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <!-- Case 1 -->
                        <div class="p-4 rounded-lg bg-bou-950 border border-slate-800 hover:border-bou-gold/50 transition flex flex-col justify-between">
                            <div>
                                <div class="flex justify-between items-center text-xs font-mono mb-2">
                                    <span class="text-bou-crimson font-bold uppercase">Incident 1</span>
                                    <span class="text-slate-500">SACCO & MFI Sector</span>
                                </div>
                                <h4 class="text-sm font-bold text-white mb-2">Core Banking Float & B2C Disbursement Hijack</h4>
                                <p class="text-xs text-slate-300 leading-relaxed">
                                    Adversaries compromised third-party IT maintenance accounts, altered internal SQL transaction tables on weekend evenings, and initiated unauthorized batch B2C disbursements to burner mobile lines.
                                </p>
                            </div>
                            <div class="mt-4 pt-3 border-t border-slate-800/80 text-xxs text-bou-goldLight font-mono">
                                <strong>BoU Forensic Parallel:</strong> Identical to the Operation Crested Crane RTGS vector. Demonstrates why DB transaction logs alone are insufficient—immutable binary redo logs and network taps are required.
                            </div>
                        </div>

                        <!-- Case 2 -->
                        <div class="p-4 rounded-lg bg-bou-950 border border-slate-800 hover:border-bou-gold/50 transition flex flex-col justify-between">
                            <div>
                                <div class="flex justify-between items-center text-xs font-mono mb-2">
                                    <span class="text-bou-amber font-bold uppercase">Incident 2</span>
                                    <span class="text-slate-500">National Infrastructure</span>
                                </div>
                                <h4 class="text-sm font-bold text-white mb-2">Sovereign Portal & KEPSS Smokescreen Attacks</h4>
                                <p class="text-xs text-slate-300 leading-relaxed">
                                    High-volume distributed denial-of-service (DDoS) barrages targeting national citizen and payment gateways were weaponized as tactical diversions while secondary threat actors probed interbank API endpoints.
                                </p>
                            </div>
                            <div class="mt-4 pt-3 border-t border-slate-800/80 text-xxs text-bou-amber font-mono">
                                <strong>BoU Forensic Parallel:</strong> CSIRT playbooks must enforce strict dual-track investigation: while network engineers mitigate perimeter volumetric floods, forensic analysts must guard payment gateways against concurrent zero-day intrusion.
                            </div>
                        </div>

                        <!-- Case 3 -->
                        <div class="p-4 rounded-lg bg-bou-950 border border-slate-800 hover:border-bou-gold/50 transition flex flex-col justify-between">
                            <div>
                                <div class="flex justify-between items-center text-xs font-mono mb-2">
                                    <span class="text-bou-cyan font-bold uppercase">Incident 3</span>
                                    <span class="text-slate-500">Telecom & Banking</span>
                                </div>
                                <h4 class="text-sm font-bold text-white mb-2">SIM-Swap Syndicates & Dual-Sign OTP Interception</h4>
                                <p class="text-xs text-slate-300 leading-relaxed">
                                    Compromised customer care agent credentials at telecom providers permitted unauthorized SIM re-registration of registered corporate signatories, intercepting SMS-based 2FA tokens for high-value wires.
                                </p>
                            </div>
                            <div class="mt-4 pt-3 border-t border-slate-800/80 text-xxs text-bou-cyan font-mono">
                                <strong>BoU Forensic Parallel:</strong> SMS OTP is legally non-defensible for central bank RTGS settlements. Proves the legal requirement for hardware-isolated FIDO2/PKI tokens under Uganda's Electronic Signatures Act 2011.
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Section 2: Sovereign Federated Learning Simulator (BoU <-> CBK) -->
                <div class="p-6 rounded-lg bg-bou-950 border border-bou-gold/40 space-y-5">
                    <div class="flex flex-col md:flex-row md:justify-between md:items-center gap-2 border-b border-slate-800 pb-3">
                        <div>
                            <span class="text-xs font-mono text-bou-emerald uppercase tracking-wider">Privacy-Preserving Cross-Border AI</span>
                            <h3 class="text-lg font-bold text-white">Sovereign Federated Learning Engine (FedAvg + Differential Privacy)</h3>
                        </div>
                        <span class="text-xs font-mono px-2.5 py-1 rounded bg-bou-emerald/15 text-emerald-300 border border-bou-emerald/30">
                            Zero Bank Customer Data Leaves Sovereignty
                        </span>
                    </div>

                    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
                        <!-- Node 1: Kampala (BoU) -->
                        <div class="p-4 rounded-lg bg-bou-900/60 border border-bou-gold/30 space-y-3 font-mono text-xs">
                            <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                                <span class="font-bold text-bou-goldLight flex items-center gap-1.5">
                                    <span>🇺🇬 Node 1: Bank of Uganda (Kampala)</span>
                                </span>
                                <span class="text-slate-400">RTGS & Payment Switch</span>
                            </div>
                            <div class="text-slate-300 space-y-1">
                                <div>• Local Model: <strong class="text-white">BoU-CyberNet-v1 (LSTM Autoencoder)</strong></div>
                                <div>• Private Training Data: <strong class="text-white">1,840,000 RTGS Telemetry Events</strong></div>
                                <div>• Local Zero-Day Detection Rate: <span id="bouAcc" class="text-bou-amber font-bold">74.2%</span></div>
                                <div>• Data Privacy Status: <span class="text-bou-emerald font-bold">Kept Strictly in BoU Vault</span></div>
                            </div>
                        </div>

                        <!-- Node 2: Nairobi (CBK) -->
                        <div class="p-4 rounded-lg bg-bou-900/60 border border-bou-cyan/30 space-y-3 font-mono text-xs">
                            <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                                <span class="font-bold text-bou-cyan flex items-center gap-1.5">
                                    <span>🇰🇪 Node 2: Central Bank of Kenya (Nairobi)</span>
                                </span>
                                <span class="text-slate-400">KEPSS & Interbank Rails</span>
                            </div>
                            <div class="text-slate-300 space-y-1">
                                <div>• Local Model: <strong class="text-white">CBK-SovereignGuard-v2</strong></div>
                                <div>• Private Training Data: <strong class="text-white">2,410,000 KEPSS Telemetry Events</strong></div>
                                <div>• Local Zero-Day Detection Rate: <span id="cbkAcc" class="text-bou-amber font-bold">76.8%</span></div>
                                <div>• Data Privacy Status: <span class="text-bou-emerald font-bold">Kept Strictly in CBK Vault</span></div>
                            </div>
                        </div>
                    </div>

                    <!-- Interactive Controls & Federated Round Simulator -->
                    <div class="p-4 rounded-lg bg-black/60 border border-slate-800 space-y-4">
                        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                            <div class="flex items-center gap-4 text-xs font-mono">
                                <div>
                                    <span class="text-slate-400">Privacy Budget (ε):</span>
                                    <span class="text-bou-gold font-bold ml-1">0.5 (High Privacy)</span>
                                </div>
                                <div>
                                    <span class="text-slate-400">Protocol:</span>
                                    <span class="text-bou-cyan font-bold ml-1">SecAgg + FedAvg</span>
                                </div>
                            </div>
                            <button id="btnRunFed" onclick="simulateFederatedLearning()" class="px-5 py-2.5 rounded bg-gradient-to-r from-bou-gold to-bou-goldLight text-bou-950 font-bold text-xs hover:brightness-110 transition shadow-lg flex items-center gap-2">
                                <span>🚀 Execute Cross-Border Federated Learning Round</span>
                            </button>
                        </div>

                        <!-- Interactive Progress Bar -->
                        <div id="fedProgressBlock" class="hidden space-y-2 font-mono text-xs">
                            <div class="flex justify-between text-slate-300">
                                <span id="fedPhaseLabel">Phase 1: Computing Local Gradients in Kampala & Nairobi...</span>
                                <span id="fedPercent" class="text-bou-gold font-bold">0%</span>
                            </div>
                            <div class="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                                <div id="fedProgressBar" class="bg-gradient-to-r from-bou-gold via-bou-emerald to-bou-cyan h-2 rounded-full transition-all duration-300" style="width: 0%;"></div>
                            </div>
                        </div>

                        <!-- Result Card -->
                        <div id="fedResultCard" class="hidden p-4 rounded-lg bg-bou-emerald/15 border border-bou-emerald space-y-2 text-xs font-mono">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-emerald-300 text-sm">🎉 CROSS-BORDER FEDERATED MODEL COMPILED SUCCESSFULLY!</span>
                                <span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-xxs">ISO 27037 & EAPS Compliant</span>
                            </div>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 text-slate-200">
                                <div class="p-2.5 rounded bg-black/40 border border-emerald-500/30">
                                    <div class="text-slate-400 text-xxs">COMBINED ACCURACY</div>
                                    <div class="text-lg font-black text-white mt-0.5">98.6%</div>
                                    <div class="text-xxs text-emerald-400 mt-1">+24.4% zero-day detection jump!</div>
                                </div>
                                <div class="p-2.5 rounded bg-black/40 border border-emerald-500/30">
                                    <div class="text-slate-400 text-xxs">RAW DATA TRANSFERRED</div>
                                    <div class="text-lg font-black text-emerald-300 mt-0.5">0.00 KB</div>
                                    <div class="text-xxs text-slate-400 mt-1">100% compliance with DPPA 2019</div>
                                </div>
                                <div class="p-2.5 rounded bg-black/40 border border-emerald-500/30">
                                    <div class="text-slate-400 text-xxs">HOMOMORPHIC GRADIENTS</div>
                                    <div class="text-lg font-black text-bou-cyan mt-0.5">48,210 Weights</div>
                                    <div class="text-xxs text-slate-400 mt-1">Encrypted via Paillier Scheme</div>
                                </div>
                            </div>
                            <p class="text-slate-300 text-xxs pt-1 leading-relaxed">
                                <strong>Operational Impact:</strong> Bank of Uganda instantly gains the ability to identify novel C2 beacon variants and financial trojan injection techniques previously seen only in Nairobi, and the Central Bank of Kenya instantly inoculates its KEPSS network against the RTGS dual-sign bypass hook uncovered in Kampala—all without either central bank sharing confidential customer data or transaction ledgers.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Section 3: Comparative Jurisprudence Matrix (Uganda vs. Kenya) -->
                <div class="p-5 rounded-lg bg-bou-950 border border-bou-gold/30 space-y-4">
                    <h3 class="text-sm font-bold text-bou-gold uppercase font-mono tracking-wider">
                        ⚖️ Comparative Legal Matrix: Uganda vs. Kenya Cyber Jurisprudence
                    </h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left font-mono text-xs border-collapse">
                            <thead>
                                <tr class="border-b border-bou-gold/30 text-bou-gold">
                                    <th class="py-2 px-3">Legal Dimension</th>
                                    <th class="py-2 px-3">Uganda Statutory Framework</th>
                                    <th class="py-2 px-3">Kenya Statutory Framework</th>
                                    <th class="py-2 px-3">Cross-Border Harmonization</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-800 text-slate-300">
                                <tr>
                                    <td class="py-2.5 px-3 font-bold text-white">Computer Crime Offenses</td>
                                    <td class="py-2.5 px-3">Computer Misuse Act 2011 & 2022 (Sec 12, 14, 15, 20)</td>
                                    <td class="py-2.5 px-3">Computer Misuse and Cybercrimes Act 2018 (Sec 14, 16, 17, 18)</td>
                                    <td class="py-2.5 px-3 text-emerald-400">Harmonized definitions of unauthorized access & system interference</td>
                                </tr>
                                <tr>
                                    <td class="py-2.5 px-3 font-bold text-white">Data Protection & Privacy</td>
                                    <td class="py-2.5 px-3">Data Protection and Privacy Act, 2019 (PDPO)</td>
                                    <td class="py-2.5 px-3">Data Protection Act, 2019 (ODPC)</td>
                                    <td class="py-2.5 px-3 text-bou-cyan">Both prohibit cross-border export of unconsented citizen telemetry</td>
                                </tr>
                                <tr>
                                    <td class="py-2.5 px-3 font-bold text-white">Electronic Evidence</td>
                                    <td class="py-2.5 px-3">Electronic Signatures Act 2011 & Evidence Act Cap 6</td>
                                    <td class="py-2.5 px-3">Kenya Evidence Act (Sec 106B) & KICA 1998</td>
                                    <td class="py-2.5 px-3 text-emerald-400">Dual SHA-256 hash & certificate of electronic production mutually recognized</td>
                                </tr>
                                <tr>
                                    <td class="py-2.5 px-3 font-bold text-white">Regional Interpol Cooperation</td>
                                    <td class="py-2.5 px-3">CID Cybercrime Division / BoU CSIRT</td>
                                    <td class="py-2.5 px-3">DCI Cybercrime Unit / CBK Banking Fraud Unit</td>
                                    <td class="py-2.5 px-3 text-bou-goldLight">EAPCCO & EAC Article 124 Joint Mutual Legal Assistance Treaty (MLAT)</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>
'''

# Insert before </main>
if 'id="panel-crossborder"' not in content:
    content = content.replace('</main>', crossborder_section + '\n    </main>')
    print("Inserted panel-crossborder section before </main>.")

# 3. Add Javascript for Federated Learning Simulator
js_sim = r'''
        // Federated Learning Cross-Border Simulator (BoU <-> CBK)
        function simulateFederatedLearning() {
            playTone(850, 'sine', 0.08);
            const btn = document.getElementById('btnRunFed');
            const progressBlock = document.getElementById('fedProgressBlock');
            const bar = document.getElementById('fedProgressBar');
            const pct = document.getElementById('fedPercent');
            const label = document.getElementById('fedPhaseLabel');
            const card = document.getElementById('fedResultCard');

            btn.disabled = true;
            btn.classList.add('opacity-50', 'cursor-not-allowed');
            progressBlock.classList.remove('hidden');
            card.classList.add('hidden');

            let progress = 0;
            const steps = [
                { p: 25, text: "Phase 1: Local Model Training on BoU RTGS & CBK KEPSS Nodes..." },
                { p: 50, text: "Phase 2: Applying Differential Privacy (ε=0.5) & Paillier Homomorphic Encryption..." },
                { p: 75, text: "Phase 3: Secure Gradient Synchronization across Kampala ↔ Nairobi Fiber Bridge..." },
                { p: 100, text: "Phase 4: Global Weight Aggregation (FedAvg) Complete!" }
            ];
            let stepIdx = 0;

            const interval = setInterval(() => {
                progress += 5;
                if (progress > steps[stepIdx].p && stepIdx < steps.length - 1) {
                    stepIdx++;
                    label.textContent = steps[stepIdx].text;
                    playTone(600 + stepIdx * 100, 'sine', 0.04);
                }
                bar.style.width = progress + '%';
                pct.textContent = progress + '%';

                if (progress >= 100) {
                    clearInterval(interval);
                    playSuccess();
                    card.classList.remove('hidden');
                    btn.disabled = false;
                    btn.classList.remove('opacity-50', 'cursor-not-allowed');
                    btn.textContent = "🔄 Re-Train Cross-Border Federated Round";
                }
            }, 100);
        }
'''

if 'function simulateFederatedLearning()' not in content:
    content = content.replace('// Initialize First Scenario', js_sim + '\n        // Initialize First Scenario')
    print("Added simulateFederatedLearning JS function.")

with open(SRC_FILE, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated {SRC_FILE} successfully ({len(content)} bytes)")

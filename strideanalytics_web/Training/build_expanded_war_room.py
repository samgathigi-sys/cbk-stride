"""
Build comprehensive, 7-module Bank of Uganda Cyber Forensics War Room & Simulator
"""
import os

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bank of Uganda | Sovereign Cyber Forensics War Room & Masterclass Simulator</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        bou: {
                            950: '#020612',
                            900: '#071120',
                            850: '#0b192e',
                            800: '#0f2442',
                            700: '#173660',
                            gold: '#c5a059',
                            goldLight: '#e6be75',
                            goldDark: '#997736',
                            crimson: '#e11d48',
                            emerald: '#10b981',
                            cyan: '#06b6d4',
                            amber: '#f59e0b'
                        }
                    },
                    fontFamily: {
                        sans: ['Inter', 'system-ui', 'sans-serif'],
                        mono: ['JetBrains Mono', 'monospace']
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #020612;
            color: #f1f5f9;
            font-family: 'Inter', sans-serif;
            overflow-x: hidden;
        }
        .glass-panel {
            background: rgba(11, 25, 46, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(197, 160, 89, 0.25);
        }
        .glass-panel:hover {
            border-color: rgba(197, 160, 89, 0.45);
        }
        .terminal-scroll::-webkit-scrollbar {
            width: 6px;
        }
        .terminal-scroll::-webkit-scrollbar-track {
            background: #020612;
        }
        .terminal-scroll::-webkit-scrollbar-thumb {
            background: #1e3a5f;
            border-radius: 3px;
        }
        @keyframes pulse-gold {
            0%, 100% { box-shadow: 0 0 15px rgba(197, 160, 89, 0.3); }
            50% { box-shadow: 0 0 25px rgba(197, 160, 89, 0.7); }
        }
        .animate-pulse-gold {
            animation: pulse-gold 2.5s infinite;
        }
        @media print {
            body { background: white !important; color: black !important; }
            .no-print { display: none !important; }
            #printable-report { display: block !important; }
        }
    </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-bou-gold selection:text-bou-950">

    <!-- Top Sovereign Command Bar -->
    <header class="no-print sticky top-0 z-50 bg-bou-900/95 backdrop-blur-md border-b border-bou-gold/30 px-6 py-3 flex justify-between items-center shadow-2xl">
        <div class="flex items-center gap-4">
            <div class="flex items-center gap-3">
                <span class="bg-gradient-to-br from-bou-gold to-bou-goldLight text-bou-950 font-black text-xs px-2.5 py-1 rounded shadow-md tracking-wider">BANK OF UGANDA</span>
                <div>
                    <h1 class="text-sm md:text-base font-bold text-white tracking-wide flex items-center gap-2">
                        <span>Cyber Forensics & Incident War Room</span>
                        <span class="text-xs font-normal text-bou-gold px-2 py-0.5 rounded-full bg-bou-gold/10 border border-bou-gold/30">Masterclass 2026</span>
                    </h1>
                </div>
            </div>
        </div>

        <!-- Telemetry Indicators & Controls -->
        <div class="flex items-center gap-3 text-xs">
            <div class="hidden md:flex items-center gap-2 px-3 py-1 rounded bg-bou-950 border border-bou-crimson/40 text-bou-crimson font-mono">
                <span class="w-2 h-2 rounded-full bg-bou-crimson animate-ping"></span>
                <span>DEFCON 2 : HIGH ALERT</span>
            </div>
            
            <div class="hidden lg:flex items-center gap-2 px-3 py-1 rounded bg-bou-950 border border-bou-gold/30 text-bou-gold font-mono">
                <span>WAR ROOM SCORE:</span>
                <span id="topScore" class="font-bold text-white">100 / 100</span>
            </div>

            <div class="hidden lg:flex items-center gap-2 px-3 py-1 rounded bg-bou-950 border border-bou-emerald/30 text-bou-emerald font-mono">
                <span>EVIDENTIARY INTEGRITY:</span>
                <span id="topIntegrity" class="font-bold text-white">100%</span>
            </div>

            <button id="sfxToggle" onclick="toggleAudio()" class="px-2.5 py-1 rounded bg-bou-850 hover:bg-bou-800 border border-bou-gold/30 text-bou-gold transition">
                🔊 SFX: ON
            </button>
            <button onclick="window.print()" class="px-2.5 py-1 rounded bg-bou-gold text-bou-950 font-bold hover:bg-bou-goldLight transition">
                🖨️ Export Dossier
            </button>
        </div>
    </header>

    <!-- Navigation Hub (The 7 Modules from the Brochure) -->
    <nav class="no-print bg-bou-850 border-b border-bou-gold/20 px-6 overflow-x-auto">
        <div class="flex gap-1 min-w-max">
            <button onclick="switchTab('ops')" class="tab-btn active px-4 py-3 text-xs md:text-sm font-semibold border-b-2 border-bou-gold text-bou-goldLight flex items-center gap-2 transition" data-tab="ops">
                <span>🛡️ War Room HQ</span>
            </button>
            <button onclick="switchTab('mod1')" class="tab-btn px-4 py-3 text-xs md:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 transition" data-tab="mod1">
                <span>📜 Mod 1 & 4: Evidence & Law</span>
            </button>
            <button onclick="switchTab('mod2')" class="tab-btn px-4 py-3 text-xs md:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 transition" data-tab="mod2">
                <span>🎯 Mod 2: Threats & IoCs</span>
            </button>
            <button onclick="switchTab('mod3')" class="tab-btn px-4 py-3 text-xs md:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 transition" data-tab="mod3">
                <span>🔬 Mod 3: Tools & Workbench</span>
            </button>
            <button onclick="switchTab('mod5')" class="tab-btn px-4 py-3 text-xs md:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 transition" data-tab="mod5">
                <span>⚔️ Mod 5: Incident Playbooks (TTX)</span>
            </button>
            <button onclick="switchTab('mod6')" class="tab-btn px-4 py-3 text-xs md:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 transition" data-tab="mod6">
                <span>☣️ Mod 6: Malware & Cloud/AI</span>
            </button>
            <button onclick="switchTab('mod7')" class="tab-btn px-4 py-3 text-xs md:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 transition" data-tab="mod7">
                <span>📋 Mod 7: Executive Report</span>
            </button>
        </div>
    </nav>

    <!-- Main Content Area -->
    <main class="flex-1 p-4 md:p-6 max-w-7xl mx-auto w-full space-y-6">

        <!-- ========================================== -->
        <!-- TAB 0: WAR ROOM HQ (OPERATIONS DASHBOARD) -->
        <!-- ========================================== -->
        <section id="panel-ops" class="tab-panel space-y-6">
            <!-- Strategic Status Header -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div class="glass-panel p-5 rounded-lg border-l-4 border-l-bou-crimson">
                    <div class="text-xs text-slate-400 font-mono uppercase tracking-wider">Active Incident Case</div>
                    <div class="text-xl font-black text-white mt-1">OPERATION CRESTED CRANE</div>
                    <div class="text-xs text-bou-crimson mt-2 flex items-center gap-1">
                        <span class="w-2 h-2 rounded-full bg-bou-crimson animate-pulse"></span>
                        <span>Unauthorized RTGS Wire In-Flight</span>
                    </div>
                </div>

                <div class="glass-panel p-5 rounded-lg border-l-4 border-l-bou-gold">
                    <div class="text-xs text-slate-400 font-mono uppercase tracking-wider">At-Risk National Capital</div>
                    <div class="text-xl font-black text-bou-goldLight mt-1">UGX 4,800,000,000</div>
                    <div class="text-xs text-slate-300 mt-2">Target Acct: CR-8831-EXT (Offshore)</div>
                </div>

                <div class="glass-panel p-5 rounded-lg border-l-4 border-l-bou-cyan">
                    <div class="text-xs text-slate-400 font-mono uppercase tracking-wider">Compromised Node</div>
                    <div class="text-xl font-black text-bou-cyan mt-1">BOU-RTGS-SRV01</div>
                    <div class="text-xs text-slate-300 mt-2">PID 4128 : bou_rtgs_service.exe</div>
                </div>

                <div class="glass-panel p-5 rounded-lg border-l-4 border-l-bou-emerald">
                    <div class="text-xs text-slate-400 font-mono uppercase tracking-wider">Judicial Standard</div>
                    <div class="text-xl font-black text-bou-emerald mt-1">CMA 2011 / 2022</div>
                    <div class="text-xs text-slate-300 mt-2">Uganda Evidence Act Cap 6 Certified</div>
                </div>
            </div>

            <!-- Threat Radar & Real-Time Incident Telemetry Feed -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Threat Radar Chart -->
                <div class="glass-panel p-5 rounded-lg lg:col-span-1 flex flex-col justify-between">
                    <div class="flex justify-between items-center mb-4 border-b border-bou-gold/20 pb-3">
                        <h2 class="text-sm font-bold text-bou-gold uppercase font-mono tracking-wider flex items-center gap-2">
                            <span>📡 BoU Cyber Threat Radar</span>
                        </h2>
                        <span class="text-xs font-mono text-slate-400">Live Telemetry</span>
                    </div>
                    <div class="relative h-64 flex items-center justify-center">
                        <canvas id="threatRadarChart"></canvas>
                    </div>
                    <div class="mt-4 text-xs font-mono text-slate-400 border-t border-bou-gold/20 pt-3 flex justify-between">
                        <span>Vulnerabilities Assessed: <strong class="text-white">18</strong></span>
                        <span>Containment Status: <strong class="text-bou-amber">ACTIVE</strong></span>
                    </div>
                </div>

                <!-- Live Masterclass Feed & Incident Timeline -->
                <div class="glass-panel p-5 rounded-lg lg:col-span-2 flex flex-col">
                    <div class="flex justify-between items-center mb-4 border-b border-bou-gold/20 pb-3">
                        <h2 class="text-sm font-bold text-bou-gold uppercase font-mono tracking-wider flex items-center gap-2">
                            <span>⚡ Masterclass Live Incident Log (Chronology)</span>
                        </h2>
                        <span class="text-xs font-mono text-bou-crimson bg-bou-crimson/10 px-2 py-0.5 rounded border border-bou-crimson/30">LIVE EDR / SIEM</span>
                    </div>
                    <div class="space-y-3 font-mono text-xs overflow-y-auto max-h-72 terminal-scroll pr-2" id="liveEventFeed">
                        <div class="p-2.5 rounded bg-bou-950/80 border border-slate-800 flex items-start gap-3">
                            <span class="text-bou-gold font-bold">06:14:02 EAT</span>
                            <span class="text-slate-300"><strong class="text-bou-cyan">[AUTH]</strong> User <code class="text-bou-goldLight">vendor_fintech_vpn</code> authenticated from external IP <code class="text-white">194.26.29.11</code> without hardware FIDO2 token.</span>
                        </div>
                        <div class="p-2.5 rounded bg-bou-950/80 border border-slate-800 flex items-start gap-3">
                            <span class="text-bou-gold font-bold">06:22:18 EAT</span>
                            <span class="text-slate-300"><strong class="text-bou-amber">[PRIV_ESC]</strong> Token impersonation: Attacker dumped LSASS memory; acquired Domain Admin NTLM hash.</span>
                        </div>
                        <div class="p-2.5 rounded bg-bou-950/80 border border-bou-crimson/40 bg-bou-crimson/5 flex items-start gap-3">
                            <span class="text-bou-crimson font-bold">06:28:44 EAT</span>
                            <span class="text-slate-200"><strong class="text-bou-crimson">[CRITICAL]</strong> Outbound batch queued: <strong class="text-white">RTGS-OUT-9912</strong> (UGX 4,800,000,000) destination <code class="text-bou-goldLight">CR-8831-EXT</code>. In-memory signature hook detected on PID 4128!</span>
                        </div>
                        <div class="p-2.5 rounded bg-bou-950/80 border border-slate-800 flex items-start gap-3">
                            <span class="text-bou-gold font-bold">06:30:10 EAT</span>
                            <span class="text-slate-300"><strong class="text-bou-emerald">[CSIRT]</strong> BoU Incident Commander invoked Order of Volatility protocol (RFC 3227) & isolated VLAN 40.</span>
                        </div>
                    </div>

                    <!-- Quick Module Launchers -->
                    <div class="mt-4 pt-3 border-t border-bou-gold/20 grid grid-cols-2 sm:grid-cols-4 gap-2 text-center text-xs">
                        <button onclick="switchTab('mod1')" class="p-2 rounded bg-bou-900 hover:bg-bou-800 border border-bou-gold/30 text-bou-goldLight font-medium transition">📜 Verify Evidence</button>
                        <button onclick="switchTab('mod3')" class="p-2 rounded bg-bou-900 hover:bg-bou-800 border border-bou-gold/30 text-bou-goldLight font-medium transition">🔬 Volatility Shell</button>
                        <button onclick="switchTab('mod5')" class="p-2 rounded bg-bou-crimson/20 hover:bg-bou-crimson/30 border border-bou-crimson/40 text-rose-300 font-bold transition">⚔️ Play Incident TTX</button>
                        <button onclick="switchTab('mod7')" class="p-2 rounded bg-bou-gold text-bou-950 font-bold hover:bg-bou-goldLight transition">📋 Build Dossier</button>
                    </div>
                </div>
            </div>
        </section>

        <!-- ======================================================= -->
        <!-- TAB 1: MODULE 1 & 4 (EVIDENCE INTEGRITY & UGANDA LAW) -->
        <!-- ======================================================= -->
        <section id="panel-mod1" class="tab-panel hidden space-y-6">
            <div class="glass-panel p-6 rounded-lg">
                <div class="border-b border-bou-gold/20 pb-4 mb-5 flex justify-between items-center">
                    <div>
                        <span class="text-xs font-mono text-bou-gold uppercase tracking-wider">Brochure Module 1 & 4</span>
                        <h2 class="text-xl font-bold text-white">Digital Forensics Foundations, Chain of Custody & Ugandan Jurisprudence</h2>
                    </div>
                    <span class="text-xs px-3 py-1 rounded bg-bou-emerald/10 text-bou-emerald border border-bou-emerald/30 font-mono">ISO/IEC 27037 & RFC 3227</span>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Live Evidence Hashing Workbench -->
                    <div class="bg-bou-950/80 p-5 rounded-lg border border-bou-gold/30 space-y-4">
                        <h3 class="text-sm font-bold text-bou-goldLight uppercase font-mono flex items-center gap-2">
                            <span>🔑 Live Cryptographic Hash & Verification Engine</span>
                        </h3>
                        <p class="text-xs text-slate-300 leading-relaxed">
                            To ensure admissibility under the <strong class="text-white">Uganda Electronic Signatures Act 2011</strong> and prevent evidence dismissal in court, test live bitstream integrity and dual hashing.
                        </p>

                        <div>
                            <label class="block text-xs font-mono text-slate-400 mb-1">Simulate Evidence Stream Input:</label>
                            <textarea id="evidenceInput" rows="3" class="w-full bg-bou-900 border border-bou-gold/30 rounded p-2 text-xs font-mono text-slate-200 focus:outline-none focus:border-bou-gold">[2026-10-19T06:28:44Z] BATCH_QUEUED: RTGS-OUT-9912 | UGX 4,800,000,000 -> BENEFICIARY: CR-8831-EXT</textarea>
                        </div>

                        <div class="flex gap-2">
                            <button onclick="calculateEvidenceHash()" class="px-4 py-2 bg-bou-gold text-bou-950 text-xs font-bold rounded hover:bg-bou-goldLight transition">Compute Dual Hashes</button>
                            <button onclick="tamperEvidence()" class="px-4 py-2 bg-bou-crimson/20 border border-bou-crimson text-rose-300 text-xs font-bold rounded hover:bg-bou-crimson/30 transition">Simulate 1-Byte Tamper</button>
                        </div>

                        <div class="p-3 bg-bou-900/90 rounded border border-slate-800 space-y-1 font-mono text-xs">
                            <div class="text-slate-400">Computed SHA-256: <span id="outSha256" class="text-bou-cyan break-all">08adba3aa8c35d8d12dac1ce7dd218bdc39592b160da62ea275acd9f751561f4</span></div>
                            <div class="text-slate-400">Computed MD5: <span id="outMd5" class="text-bou-goldLight">027d56eb3547a46f6362b6becbe03ed2</span></div>
                            <div class="text-slate-400 mt-2">Judicial Status: <span id="outStatus" class="text-bou-emerald font-bold">BIT-STREAM AUTHENTIC (ADMISSIBLE)</span></div>
                        </div>
                    </div>

                    <!-- Uganda Cyber Statutory Framework -->
                    <div class="bg-bou-950/80 p-5 rounded-lg border border-bou-gold/30 space-y-4">
                        <h3 class="text-sm font-bold text-bou-goldLight uppercase font-mono flex items-center gap-2">
                            <span>⚖️ Ugandan Legal & Regulatory Defensibility</span>
                        </h3>
                        <p class="text-xs text-slate-300 leading-relaxed">
                            Statutes governing electronic evidence seized by Bank of Uganda cyber examiners for production before the High Court of Uganda:
                        </p>

                        <div class="space-y-2 text-xs">
                            <div class="p-2.5 rounded bg-bou-900/60 border border-slate-800 hover:border-bou-gold/40 transition">
                                <div class="font-bold text-bou-gold">Computer Misuse Act, 2011 & 2022 Amendment</div>
                                <div class="text-slate-300 mt-0.5">• <strong>Section 12:</strong> Unauthorized access to computer systems or data.<br>• <strong>Section 15:</strong> Unauthorized modification of computer materials.<br>• <strong>Section 20:</strong> Electronic fraud in banking & payments.</div>
                            </div>
                            <div class="p-2.5 rounded bg-bou-900/60 border border-slate-800 hover:border-bou-gold/40 transition">
                                <div class="font-bold text-bou-cyan">Data Protection and Privacy Act, 2019</div>
                                <div class="text-slate-300 mt-0.5">Safeguards financial privacy. Mandates that forensic acquisition strictly isolates crime-relevant partitions without leaking customer account databases.</div>
                            </div>
                            <div class="p-2.5 rounded bg-bou-900/60 border border-slate-800 hover:border-bou-gold/40 transition">
                                <div class="font-bold text-bou-emerald">Electronic Signatures Act, 2011 & Evidence Act Cap 6</div>
                                <div class="text-slate-300 mt-0.5">Authorizes cryptographic hashing as proof of authenticity. Overcomes hearsay exclusion rules through certified chain of custody.</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Interactive Chain of Custody Form Builder -->
                <div class="mt-6 p-5 bg-bou-950/80 rounded-lg border border-bou-gold/30 space-y-3">
                    <h3 class="text-sm font-bold text-bou-goldLight uppercase font-mono">Institutional Chain of Custody Transfer Form</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
                        <div>
                            <span class="text-slate-400">Evidence ID:</span>
                            <input type="text" value="EVD-BOU-2026-RTGS01" class="w-full bg-bou-900 border border-bou-gold/30 rounded p-1.5 text-white">
                        </div>
                        <div>
                            <span class="text-slate-400">Current Custodian:</span>
                            <input type="text" value="Senior Forensic Examiner, BoU CSIRT" class="w-full bg-bou-900 border border-bou-gold/30 rounded p-1.5 text-white">
                        </div>
                        <div>
                            <span class="text-slate-400">Vault Location:</span>
                            <input type="text" value="BoU Headquarters Safe #2" class="w-full bg-bou-900 border border-bou-gold/30 rounded p-1.5 text-white">
                        </div>
                    </div>
                    <button onclick="logCustodyAction()" class="px-4 py-2 bg-bou-800 border border-bou-gold/40 text-bou-gold text-xs font-bold rounded hover:bg-bou-700 transition">Log Custody Transfer into Forensic Vault</button>
                    <div id="custodyLogResult" class="text-xs font-mono text-bou-emerald hidden">✓ Custody transfer recorded with timestamp signature under ISO/IEC 27037 standards.</div>
                </div>
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- TAB 2: MODULE 2 (CYBER SECURITY THREATS & ATTACK VECTORS / IoC) -->
        <!-- ============================================================== -->
        <section id="panel-mod2" class="tab-panel hidden space-y-6">
            <div class="glass-panel p-6 rounded-lg">
                <div class="border-b border-bou-gold/20 pb-4 mb-5 flex justify-between items-center">
                    <div>
                        <span class="text-xs font-mono text-bou-gold uppercase tracking-wider">Brochure Module 2</span>
                        <h2 class="text-xl font-bold text-white">Financial Threat Taxonomy, Attack Vectors & Indicators of Compromise (IoCs)</h2>
                    </div>
                    <span class="text-xs px-3 py-1 rounded bg-bou-crimson/10 text-bou-crimson border border-bou-crimson/30 font-mono">MITRE ATT&CK Banking Matrix</span>
                </div>

                <!-- Attack Vector Explorer Cards -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div class="p-4 rounded-lg bg-bou-950 border border-slate-800 hover:border-bou-crimson transition">
                        <div class="text-xs font-mono text-bou-crimson font-bold uppercase">Vector 1: Core Payment Tampering</div>
                        <h4 class="text-sm font-bold text-white mt-1">RTGS / SWIFT In-Memory Hooking</h4>
                        <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                            Attacker injects an API hook into the transaction dispatcher service, nullifying dual-control authorization and injecting unapproved payment batches.
                        </p>
                    </div>

                    <div class="p-4 rounded-lg bg-bou-950 border border-slate-800 hover:border-bou-amber transition">
                        <div class="text-xs font-mono text-bou-amber font-bold uppercase">Vector 2: Third-Party Supply Chain</div>
                        <h4 class="text-sm font-bold text-white mt-1">Vendor Maintenance Tunnel Abuse</h4>
                        <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                            Stolen credentials from an authorized IT maintenance vendor bypass perimeter MFA and establish lateral SMB access across production financial VLANs.
                        </p>
                    </div>

                    <div class="p-4 rounded-lg bg-bou-950 border border-slate-800 hover:border-bou-cyan transition">
                        <div class="text-xs font-mono text-bou-cyan font-bold uppercase">Vector 3: Stealth C2 Beaconing</div>
                        <h4 class="text-sm font-bold text-white mt-1">Statistical Jitter & Domain Fronting</h4>
                        <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                            Automated bot implants maintain communication with bulletproof overseas hosting nodes using low-jitter HTTPS channels masquerading as cloud telemetry.
                        </p>
                    </div>
                </div>

                <!-- Interactive IoC Triage Table -->
                <div class="bg-bou-950/80 p-5 rounded-lg border border-bou-gold/30 space-y-4">
                    <div class="flex justify-between items-center">
                        <h3 class="text-sm font-bold text-bou-goldLight uppercase font-mono">Live Indicators of Compromise (IoC) Matrix for Case FIN-UG7</h3>
                        <span class="text-xs font-mono text-slate-400">4 Active IoCs Extracted</span>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full text-left font-mono text-xs border-collapse">
                            <thead>
                                <tr class="border-b border-bou-gold/30 text-bou-gold">
                                    <th class="py-2 px-3">Type</th>
                                    <th class="py-2 px-3">Indicator / Artifact</th>
                                    <th class="py-2 px-3">Threat Context</th>
                                    <th class="py-2 px-3">Severity</th>
                                    <th class="py-2 px-3">Firewall Action</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-slate-800 text-slate-300">
                                <tr>
                                    <td class="py-2 px-3 text-bou-cyan font-bold">IPv4 Address</td>
                                    <td class="py-2 px-3 text-white">194.26.29.11</td>
                                    <td class="py-2 px-3">Adversary C2 Staging Server (ASN 49211)</td>
                                    <td class="py-2 px-3 text-bou-crimson font-bold">CRITICAL</td>
                                    <td class="py-2 px-3"><span class="px-2 py-0.5 rounded bg-bou-crimson/20 text-rose-300 border border-bou-crimson">BLOCKED</span></td>
                                </tr>
                                <tr>
                                    <td class="py-2 px-3 text-bou-cyan font-bold">SHA-256 File</td>
                                    <td class="py-2 px-3 text-white">e3b0c44298fc1c149afbf4c8996fb924...</td>
                                    <td class="py-2 px-3">Cobalt Strike Stager in C:\Windows\Temp</td>
                                    <td class="py-2 px-3 text-bou-crimson font-bold">CRITICAL</td>
                                    <td class="py-2 px-3"><span class="px-2 py-0.5 rounded bg-bou-crimson/20 text-rose-300 border border-bou-crimson">QUARANTINED</span></td>
                                </tr>
                                <tr>
                                    <td class="py-2 px-3 text-bou-cyan font-bold">DNS Domain</td>
                                    <td class="py-2 px-3 text-white">settle-gate.ugandafin.xyz</td>
                                    <td class="py-2 px-3">DNS Tunneling Data Exfiltration Endpoint</td>
                                    <td class="py-2 px-3 text-bou-amber font-bold">HIGH</td>
                                    <td class="py-2 px-3"><span class="px-2 py-0.5 rounded bg-bou-amber/20 text-amber-300 border border-bou-amber">DNS SINKHOLE</span></td>
                                </tr>
                                <tr>
                                    <td class="py-2 px-3 text-bou-cyan font-bold">Windows Event</td>
                                    <td class="py-2 px-3 text-white">Event ID 4624 (Logon Type 10)</td>
                                    <td class="py-2 px-3">RDP Logon via unapproved vendor account</td>
                                    <td class="py-2 px-3 text-bou-emerald font-bold">ELEVATED</td>
                                    <td class="py-2 px-3"><span class="px-2 py-0.5 rounded bg-bou-emerald/20 text-emerald-300 border border-bou-emerald">ACCOUNT DISABLED</span></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- TAB 3: MODULE 3 (DIGITAL FORENSICS TOOLS & WORKBENCH) -->
        <!-- ============================================================== -->
        <section id="panel-mod3" class="tab-panel hidden space-y-6">
            <div class="glass-panel p-6 rounded-lg">
                <div class="border-b border-bou-gold/20 pb-4 mb-5 flex justify-between items-center">
                    <div>
                        <span class="text-xs font-mono text-bou-gold uppercase tracking-wider">Brochure Module 3</span>
                        <h2 class="text-xl font-bold text-white">Forensic Tools & Acquisition Workbench (Memory, Disk, Network)</h2>
                    </div>
                    <span class="text-xs px-3 py-1 rounded bg-bou-cyan/10 text-bou-cyan border border-bou-cyan/30 font-mono">Volatility 3 / Sleuth Kit / Wireshark</span>
                </div>

                <!-- Sub-tabs for Workbench: Memory vs Network PCAP vs Disk/MFT -->
                <div class="flex gap-2 border-b border-slate-800 pb-2 mb-4 font-mono text-xs">
                    <button onclick="switchWorkbench('mem')" class="wb-tab-btn active px-3 py-1.5 rounded bg-bou-gold text-bou-950 font-bold" data-wbtab="mem">🧠 Volatile Memory (Volatility 3)</button>
                    <button onclick="switchWorkbench('pcap')" class="wb-tab-btn px-3 py-1.5 rounded bg-bou-900 hover:bg-bou-800 text-slate-300" data-wbtab="pcap">📡 Packet Dissector (PCAP)</button>
                    <button onclick="switchWorkbench('disk')" class="wb-tab-btn px-3 py-1.5 rounded bg-bou-900 hover:bg-bou-800 text-slate-300" data-wbtab="disk">💾 File System & MFT Carver</button>
                </div>

                <!-- 1. Volatility 3 Interactive Shell -->
                <div id="wb-panel-mem" class="wb-panel space-y-3">
                    <div class="bg-bou-950 p-4 rounded-lg border border-bou-gold/30 font-mono text-xs space-y-3">
                        <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                            <span class="text-bou-gold">Target RAM Image: bou_rtgs_mem.dmp (Windows Server 2022 x64)</span>
                            <span class="text-slate-400">Available: pslist, malfind, netscan, cmdline, dlllist</span>
                        </div>
                        <div id="volOutput" class="h-64 overflow-y-auto terminal-scroll text-slate-300 bg-black/60 p-3 rounded leading-relaxed whitespace-pre-wrap">VOLATILITY 3 FRAMEWORK v2.7.0
Loaded image: bou_rtgs_mem.dmp
Symbols loaded for Windows Server 2022 (Kernel base: 0xfffff80010000000)
Type a command or click a quick shortcut below to triage suspicious process memory.</div>
                        <div class="flex gap-2 items-center">
                            <span class="text-bou-gold font-bold">vol.py&gt;</span>
                            <input type="text" id="volInput" placeholder="Try: pslist, malfind, netscan, cmdline..." class="flex-1 bg-bou-900 border border-slate-700 rounded px-3 py-1.5 text-white focus:outline-none focus:border-bou-gold" onkeydown="handleVolKey(event)">
                            <button onclick="execVolCmd()" class="px-4 py-1.5 bg-bou-gold text-bou-950 font-bold rounded hover:bg-bou-goldLight transition">Execute</button>
                        </div>
                        <div class="flex gap-2 flex-wrap text-xs pt-1">
                            <span class="text-slate-500">Quick queries:</span>
                            <button onclick="runVolShortcut('pslist')" class="px-2 py-0.5 rounded bg-bou-850 hover:bg-bou-800 border border-slate-700 text-bou-cyan">windows.pslist</button>
                            <button onclick="runVolShortcut('malfind')" class="px-2 py-0.5 rounded bg-bou-850 hover:bg-bou-800 border border-bou-crimson/50 text-rose-300">windows.malfind (Injects)</button>
                            <button onclick="runVolShortcut('netscan')" class="px-2 py-0.5 rounded bg-bou-850 hover:bg-bou-800 border border-slate-700 text-bou-cyan">windows.netscan (Sockets)</button>
                            <button onclick="runVolShortcut('cmdline')" class="px-2 py-0.5 rounded bg-bou-850 hover:bg-bou-800 border border-slate-700 text-bou-cyan">windows.cmdline</button>
                        </div>
                    </div>
                </div>

                <!-- 2. Packet Dissector (PCAP) -->
                <div id="wb-panel-pcap" class="wb-panel hidden space-y-3">
                    <div class="bg-bou-950 p-4 rounded-lg border border-bou-gold/30 font-mono text-xs space-y-3">
                        <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                            <span class="text-bou-cyan font-bold">PCAP Trace: BOU_GATEWAY_CAPTURE_20261019.pcap (Wireshark Engine)</span>
                            <span class="text-slate-400">Total Frames: 1,482</span>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left font-mono text-xs">
                                <thead>
                                    <tr class="border-b border-slate-800 text-slate-400">
                                        <th class="py-1 px-2">No.</th>
                                        <th class="py-1 px-2">Time</th>
                                        <th class="py-1 px-2">Source</th>
                                        <th class="py-1 px-2">Destination</th>
                                        <th class="py-1 px-2">Protocol</th>
                                        <th class="py-1 px-2">Length</th>
                                        <th class="py-1 px-2">Info</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-800 text-slate-300" id="pcapTable">
                                    <tr class="hover:bg-bou-900 cursor-pointer" onclick="inspectPacket(1)">
                                        <td class="py-1 px-2">104</td>
                                        <td class="py-1 px-2 text-slate-400">06:28:43</td>
                                        <td class="py-1 px-2 text-bou-cyan">10.12.4.15</td>
                                        <td class="py-1 px-2 text-bou-goldLight">10.12.4.99</td>
                                        <td class="py-1 px-2 text-bou-amber font-bold">RTGS-RPC</td>
                                        <td class="py-1 px-2">512</td>
                                        <td class="py-1 px-2 text-white">Call: QueueBatch(ID=9912, Val=4.8B UGX, Sig=BYPASSED)</td>
                                    </tr>
                                    <tr class="hover:bg-bou-900 cursor-pointer bg-bou-crimson/10" onclick="inspectPacket(2)">
                                        <td class="py-1 px-2">108</td>
                                        <td class="py-1 px-2 text-slate-400">06:28:44</td>
                                        <td class="py-1 px-2 text-bou-cyan">10.12.4.15</td>
                                        <td class="py-1 px-2 text-bou-crimson font-bold">194.26.29.11</td>
                                        <td class="py-1 px-2 text-bou-crimson font-bold">TLSv1.3</td>
                                        <td class="py-1 px-2">1,024</td>
                                        <td class="py-1 px-2 text-rose-300">[ANOMALY] Outbound Beacon Heartbeat (Jitter=0.0033)</td>
                                    </tr>
                                    <tr class="hover:bg-bou-900 cursor-pointer" onclick="inspectPacket(3)">
                                        <td class="py-1 px-2">115</td>
                                        <td class="py-1 px-2 text-slate-400">06:29:12</td>
                                        <td class="py-1 px-2 text-bou-cyan">10.12.4.15</td>
                                        <td class="py-1 px-2 text-slate-300">10.12.0.2</td>
                                        <td class="py-1 px-2 text-bou-cyan">DNS</td>
                                        <td class="py-1 px-2">128</td>
                                        <td class="py-1 px-2 text-slate-300">Standard query 0x14a2 TXT a8f12.c2.ugandafin.xyz</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div id="packetHexView" class="p-3 bg-black/70 rounded border border-slate-800 text-bou-cyan text-xs leading-relaxed">
                            Click any packet row above to inspect byte-level hex disassembly and decoded field headers.
                        </div>
                    </div>
                </div>

                <!-- 3. File System & MFT Carver -->
                <div id="wb-panel-disk" class="wb-panel hidden space-y-3">
                    <div class="bg-bou-950 p-4 rounded-lg border border-bou-gold/30 font-mono text-xs space-y-3">
                        <div class="flex justify-between items-center border-b border-slate-800 pb-2">
                            <span class="text-bou-emerald font-bold">NTFS $MFT & Deleted Artifact Carver (The Sleuth Kit / fls / ils)</span>
                            <span class="text-slate-400">Volume: C:\ [NTFS 4096 Cluster]</span>
                        </div>
                        <p class="text-slate-300 leading-relaxed">
                            Unmasking <strong class="text-white">Anti-Forensics & Timestomping</strong>: Notice the discrepancy between <code class="text-bou-gold">$STANDARD_INFORMATION</code> (which can be manipulated by user-mode APIs) and <code class="text-bou-cyan">$FILE_NAME</code> (which can only be altered by the kernel driver).
                        </p>
                        <div class="p-3 bg-black/60 rounded border border-slate-800 text-slate-300 space-y-2">
                            <div><strong>Artifact:</strong> <code>C:\Windows\Temp\mimikatz.exe</code> (Deleted / Carved from Cluster 88412)</div>
                            <div>• $STANDARD_INFORMATION Timestamp: <span class="text-slate-400">2018-05-12 10:00:00 UTC</span> <span class="text-bou-crimson font-bold">[FORGED / TIMESTOMPED]</span></div>
                            <div>• $FILE_NAME Real Creation Timestamp: <span class="text-bou-emerald font-bold">2026-10-19 06:21:40 UTC</span> <span class="text-bou-emerald font-bold">[REAL FORENSIC TRUTH]</span></div>
                            <div class="text-bou-goldLight mt-2">→ Conclusion: The attacker attempted to camouflage the credential dumper as an old 2018 system utility. $FILE_NAME analysis definitively proves it was dropped today during the intrusion.</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- TAB 4: MODULE 5 (INCIDENT RESPONSE & TABLETOP SIMULATION TTX) -->
        <!-- ============================================================== -->
        <section id="panel-mod5" class="tab-panel hidden space-y-6">
            <div class="glass-panel p-6 rounded-lg">
                <div class="border-b border-bou-gold/20 pb-4 mb-5 flex justify-between items-center">
                    <div>
                        <span class="text-xs font-mono text-bou-gold uppercase tracking-wider">Brochure Module 5</span>
                        <h2 class="text-xl font-bold text-white">Central Bank Incident Response Management & Interactive Tabletop (TTX)</h2>
                    </div>
                    <span class="text-xs px-3 py-1 rounded bg-bou-crimson/10 text-bou-crimson border border-bou-crimson/30 font-mono">NIST SP 800-61 / ISO 27035</span>
                </div>

                <!-- Scenario Selector for TTX -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 mb-6">
                    <button onclick="loadScenario(0)" id="scenBtn0" class="p-3 text-left rounded-lg bg-bou-950 border border-bou-gold text-white font-mono text-xs transition">
                        <div class="text-bou-gold font-bold">SCENARIO A</div>
                        <div class="font-bold mt-1">RTGS In-Memory Wire Injection</div>
                        <div class="text-slate-400 text-xxs mt-1">UGX 4.8B at risk • Live Payment Engine</div>
                    </button>
                    <button onclick="loadScenario(1)" id="scenBtn1" class="p-3 text-left rounded-lg bg-bou-950 border border-slate-800 text-slate-400 hover:text-white font-mono text-xs transition">
                        <div class="text-bou-crimson font-bold">SCENARIO B</div>
                        <div class="font-bold mt-1">Hypervisor Ransomware Outbreak</div>
                        <div class="text-slate-400 text-xxs mt-1">ESXi & SAN Storage Locked • Double Extortion</div>
                    </button>
                    <button onclick="loadScenario(2)" id="scenBtn2" class="p-3 text-left rounded-lg bg-bou-950 border border-slate-800 text-slate-400 hover:text-white font-mono text-xs transition">
                        <div class="text-bou-cyan font-bold">SCENARIO C</div>
                        <div class="font-bold mt-1">Core Banking Insider Manipulation</div>
                        <div class="text-slate-400 text-xxs mt-1">Ledger Balance Alteration • Database Audit</div>
                    </button>
                </div>

                <!-- Interactive Scenario Container -->
                <div class="bg-bou-950/90 p-6 rounded-lg border border-bou-gold/40 space-y-4">
                    <div class="flex justify-between items-start border-b border-slate-800 pb-3">
                        <div>
                            <span class="text-xs font-mono text-bou-crimson font-bold" id="ttxPhaseText">PHASE 1: DETECTION & INITIAL TRIAGE</span>
                            <h3 class="text-lg font-bold text-white mt-1" id="ttxTitleText">The 06:28 EAT RTGS Batch Alert</h3>
                        </div>
                        <div class="text-right font-mono text-xs">
                            <span class="text-slate-400">Step:</span>
                            <span class="text-bou-gold font-bold ml-1" id="ttxStepText">1 of 4</span>
                        </div>
                    </div>

                    <div class="p-4 rounded bg-bou-900/60 border-l-4 border-l-bou-gold text-slate-200 text-sm leading-relaxed" id="ttxPrompt">
                        Loading scenario prompt...
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3" id="ttxChoices">
                        <!-- Populated by JS -->
                    </div>

                    <div id="ttxFeedback" class="p-4 rounded text-xs font-mono leading-relaxed hidden"></div>

                    <div class="flex justify-between items-center pt-2">
                        <button onclick="resetScenario()" class="px-3 py-1.5 rounded bg-bou-900 border border-slate-700 text-xs text-slate-400 hover:text-white">Restart Scenario</button>
                        <button id="ttxNextBtn" onclick="advanceScenarioStep()" class="px-4 py-2 rounded bg-bou-gold text-bou-950 text-xs font-bold hover:bg-bou-goldLight hidden transition">Advance to Next Incident Phase →</button>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- TAB 5: MODULE 6 (ADVANCED TOPICS: MALWARE, CLOUD & AI THREATS) -->
        <!-- ============================================================== -->
        <section id="panel-mod6" class="tab-panel hidden space-y-6">
            <div class="glass-panel p-6 rounded-lg">
                <div class="border-b border-bou-gold/20 pb-4 mb-5 flex justify-between items-center">
                    <div>
                        <span class="text-xs font-mono text-bou-gold uppercase tracking-wider">Brochure Module 6</span>
                        <h2 class="text-xl font-bold text-white">Malware Reverse Triage, Threat Intelligence & Cloud/AI Forensics</h2>
                    </div>
                    <span class="text-xs px-3 py-1 rounded bg-bou-purple-400/10 text-purple-400 border border-purple-400/30 font-mono">YARA / Static PE Analysis</span>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- Live YARA Rule Builder & Rule Tester -->
                    <div class="bg-bou-950/80 p-5 rounded-lg border border-bou-gold/30 space-y-3 font-mono text-xs">
                        <h3 class="text-sm font-bold text-bou-goldLight uppercase flex items-center gap-2">
                            <span>🛡️ Interactive YARA Signature Compiler</span>
                        </h3>
                        <p class="text-slate-300 font-sans text-xs">
                            Write or customize YARA rules to sweep Bank of Uganda endpoints for banking trojan string artifacts and PE signatures.
                        </p>
                        <textarea id="yaraCode" rows="8" class="w-full bg-bou-900 border border-slate-700 rounded p-2 text-bou-cyan focus:outline-none focus:border-bou-gold">rule BoU_Banking_Trojan_Hook {
    meta:
        description = "Detects in-memory dual-authorization bypass"
        author = "Bank of Uganda Forensics"
    strings:
        $s1 = "RTGS_INJECTION_HOOK" ascii wide
        $s2 = "SWIFT_PAYMENT_INTERCEPT" ascii wide
        $hex1 = { 48 83 ec 28 48 8d 0d }
    condition:
        uint16(0) == 0x5A4D and (any of ($s*)) or $hex1
}</textarea>
                        <div class="flex gap-2">
                            <button onclick="testYaraRule()" class="px-3 py-1.5 bg-bou-gold text-bou-950 font-bold rounded hover:bg-bou-goldLight">Test Signature Against Dump</button>
                        </div>
                        <div id="yaraResult" class="p-2.5 rounded bg-bou-900 border border-slate-800 text-slate-300">
                            Status: Ready to scan target binary buffer.
                        </div>
                    </div>

                    <!-- Cloud & AI Security Vectors in Central Banking -->
                    <div class="bg-bou-950/80 p-5 rounded-lg border border-bou-gold/30 space-y-4">
                        <h3 class="text-sm font-bold text-bou-goldLight uppercase font-mono flex items-center gap-2">
                            <span>☁️ Cloud & AI Threat Vectors in Central Banking</span>
                        </h3>
                        <div class="space-y-3 text-xs">
                            <div class="p-3 rounded bg-bou-900/60 border border-slate-800">
                                <div class="font-bold text-bou-cyan">Cloud Security & API Token Hijacking</div>
                                <p class="text-slate-300 mt-1">Interbank settlement APIs integrated with AWS/Azure hybrid switches. Forensics requires analyzing CloudTrail / Azure Activity logs for <code>AssumeRoleWithWebIdentity</code> anomalies and token theft.</p>
                            </div>
                            <div class="p-3 rounded bg-bou-900/60 border border-slate-800">
                                <div class="font-bold text-bou-purple-400">AI-Generated Synthetic Wire Fraud</div>
                                <p class="text-slate-300 mt-1">Adversaries utilizing deepfake audio and automated behavioral bypass models to impersonate senior bank signatories over voice confirmation channels.</p>
                            </div>
                            <div class="p-3 rounded bg-bou-900/60 border border-slate-800">
                                <div class="font-bold text-bou-amber">IoT & Critical Facility Infrastructure</div>
                                <p class="text-slate-300 mt-1">Forensic analysis of physical vault access controllers, CCTV telemetry, and data center cooling control systems susceptible to SCADA/ICS attacks.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- ============================================================== -->
        <!-- TAB 6: MODULE 7 (REPORT WRITING & EXECUTIVE BRIEFING DOSSIER) -->
        <!-- ============================================================== -->
        <section id="panel-mod7" class="tab-panel hidden space-y-6">
            <div class="glass-panel p-6 rounded-lg">
                <div class="border-b border-bou-gold/20 pb-4 mb-5 flex justify-between items-center">
                    <div>
                        <span class="text-xs font-mono text-bou-gold uppercase tracking-wider">Brochure Module 7</span>
                        <h2 class="text-xl font-bold text-white">Forensic Report Writing & Communication to the Governor / Courts</h2>
                    </div>
                    <button onclick="window.print()" class="px-3 py-1.5 rounded bg-bou-gold text-bou-950 font-bold text-xs hover:bg-bou-goldLight flex items-center gap-1.5">
                        <span>🖨️ Print / Save as PDF</span>
                    </button>
                </div>

                <!-- Printable / Rendered Institutional Report -->
                <div id="printable-report" class="bg-white text-slate-900 p-8 rounded-lg shadow-2xl space-y-6 font-sans">
                    <!-- Report Header -->
                    <div class="border-b-2 border-slate-900 pb-4 flex justify-between items-start">
                        <div>
                            <div class="text-xs font-bold uppercase tracking-widest text-slate-500">BANK OF UGANDA // CONFIDENTIAL FORENSIC DOSSIER</div>
                            <h2 class="text-2xl font-black text-slate-900 mt-1">INCIDENT INVESTIGATION REPORT: OPERATION CRESTED CRANE</h2>
                            <div class="text-xs text-slate-600 mt-1">Case Reference: <strong>BOU-CYBER-2026-001</strong> | Prepared for: <strong>Governor & Board Audit Committee</strong></div>
                        </div>
                        <div class="text-right text-xs">
                            <span class="inline-block px-2.5 py-1 bg-red-100 text-red-800 font-bold rounded border border-red-300">FOR COURT PRODUCTION</span>
                            <div class="text-slate-500 mt-1">Date: 19 October 2026</div>
                        </div>
                    </div>

                    <!-- Executive Summary -->
                    <div>
                        <h3 class="text-sm font-bold text-slate-900 uppercase tracking-wider border-b border-slate-200 pb-1 mb-2">1. Executive Summary</h3>
                        <p class="text-xs text-slate-700 leading-relaxed">
                            On 19 October 2026 at 06:28 EAT, an unauthorized batch settlement command was queued on payment engine <strong class="text-slate-900">BOU-RTGS-SRV01</strong> attempting to wire <strong class="text-red-700 font-bold">UGX 4,800,000,000</strong> to offshore beneficiary account <strong class="text-slate-900">CR-8831-EXT</strong>. 
                            The Bank of Uganda Cyber Incident Response Team (BoU-CSIRT) successfully intercepted the transmission, preserved volatile RAM, isolated the affected VLAN, and revoked compromised domain Kerberos tickets. 
                            <strong>Zero financial loss was sustained by the Bank of Uganda or commercial institutions.</strong>
                        </p>
                    </div>

                    <!-- Forensic Evidence Summary Table -->
                    <div>
                        <h3 class="text-sm font-bold text-slate-900 uppercase tracking-wider border-b border-slate-200 pb-1 mb-2">2. Digital Evidence Ledger & Chain of Custody</h3>
                        <table class="w-full text-left text-xs border border-slate-300">
                            <thead class="bg-slate-100 text-slate-700">
                                <tr>
                                    <th class="p-2 border border-slate-300">Item ID</th>
                                    <th class="p-2 border border-slate-300">Source Asset</th>
                                    <th class="p-2 border border-slate-300">Media Type</th>
                                    <th class="p-2 border border-slate-300">SHA-256 Hash</th>
                                    <th class="p-2 border border-slate-300">Status</th>
                                </tr>
                            </thead>
                            <tbody class="text-slate-600 font-mono text-xxs">
                                <tr>
                                    <td class="p-2 border border-slate-300 font-bold text-slate-900">EVD-RTGS-01</td>
                                    <td class="p-2 border border-slate-300">BOU-RTGS-SRV01</td>
                                    <td class="p-2 border border-slate-300">Volatile RAM Dump (24GB)</td>
                                    <td class="p-2 border border-slate-300">08adba3aa8c35d8d12dac1ce7dd218bdc39592b1...</td>
                                    <td class="p-2 border border-slate-300 text-green-700 font-bold">MATCH / ADMISSIBLE</td>
                                </tr>
                                <tr>
                                    <td class="p-2 border border-slate-300 font-bold text-slate-900">EVD-PCAP-02</td>
                                    <td class="p-2 border border-slate-300">Core Switch VLAN 40</td>
                                    <td class="p-2 border border-slate-300">Network PCAP (1.4GB)</td>
                                    <td class="p-2 border border-slate-300">9c1b72e0a4f5d31290bb8a11cf4e1209ba339412...</td>
                                    <td class="p-2 border border-slate-300 text-green-700 font-bold">MATCH / ADMISSIBLE</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- Statutory Breaches -->
                    <div>
                        <h3 class="text-sm font-bold text-slate-900 uppercase tracking-wider border-b border-slate-200 pb-1 mb-2">3. Recommended Charges Under Uganda Cyber Law</h3>
                        <ul class="text-xs text-slate-700 space-y-1.5 list-disc pl-5">
                            <li><strong>Uganda Computer Misuse Act (2011/2022) Section 12:</strong> Unauthorized access to computer programs or data.</li>
                            <li><strong>Uganda Computer Misuse Act Section 15:</strong> Unauthorized modification of computer contents (in-memory hooking of PID 4128).</li>
                            <li><strong>Uganda Computer Misuse Act Section 20:</strong> Electronic fraud attempting unlawful financial diversion of UGX 4,800,000,000.</li>
                        </ul>
                    </div>

                    <!-- Certification Signatures -->
                    <div class="border-t-2 border-slate-900 pt-6 grid grid-cols-2 gap-8 text-xs">
                        <div>
                            <div class="font-bold text-slate-900">LEAD CYBER FORENSIC EXAMINER</div>
                            <div class="text-slate-500">Bank of Uganda CSIRT</div>
                            <div class="mt-6 border-b border-slate-400 w-48"></div>
                            <div class="text-slate-400 text-xxs mt-1">Signature & Date Stamp</div>
                        </div>
                        <div>
                            <div class="font-bold text-slate-900">HEAD OF INFORMATION SECURITY & AUDIT</div>
                            <div class="text-slate-500">Bank of Uganda</div>
                            <div class="mt-6 border-b border-slate-400 w-48"></div>
                            <div class="text-slate-400 text-xxs mt-1">Signature & Date Stamp</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="no-print bg-bou-950 border-t border-bou-gold/20 py-4 px-6 text-center text-xs text-slate-500 font-mono">
        Bank of Uganda © 2026 • Cyber Forensics & Security Investigations Masterclass • Sovereign Infrastructure Protection Unit
    </footer>

    <!-- Audio Synthesizer & War Room Engine Script -->
    <script>
        // Web Audio Synthesizer
        let audioEnabled = true;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        function playTone(freq, type = 'sine', duration = 0.08) {
            if (!audioEnabled) return;
            try {
                if (audioCtx.state === 'suspended') audioCtx.resume();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = type;
                osc.frequency.value = freq;
                gain.gain.setValueAtTime(0.06, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + duration);
            } catch(e) {}
        }

        function playSuccess() {
            playTone(440, 'triangle', 0.08);
            setTimeout(() => playTone(880, 'triangle', 0.15), 90);
        }

        function playFail() {
            playTone(160, 'sawtooth', 0.2);
            setTimeout(() => playTone(120, 'sawtooth', 0.25), 120);
        }

        function toggleAudio() {
            audioEnabled = !audioEnabled;
            document.getElementById('sfxToggle').textContent = audioEnabled ? '🔊 SFX: ON' : '🔇 SFX: OFF';
        }

        // Tab Navigation
        function switchTab(tabKey) {
            playTone(600, 'sine', 0.04);
            document.querySelectorAll('.tab-btn').forEach(btn => {
                const isActive = btn.getAttribute('data-tab') === tabKey;
                btn.className = isActive 
                    ? 'tab-btn active px-4 py-3 text-xs md:text-sm font-semibold border-b-2 border-bou-gold text-bou-goldLight flex items-center gap-2 transition'
                    : 'tab-btn px-4 py-3 text-xs md:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-white flex items-center gap-2 transition';
            });

            document.querySelectorAll('.tab-panel').forEach(panel => {
                panel.classList.add('hidden');
            });
            const target = document.getElementById('panel-' + tabKey);
            if (target) target.classList.remove('hidden');
        }

        // Workbench sub-tab switcher (Module 3)
        function switchWorkbench(subKey) {
            playTone(700, 'sine', 0.04);
            document.querySelectorAll('.wb-tab-btn').forEach(btn => {
                const isActive = btn.getAttribute('data-wbtab') === subKey;
                btn.className = isActive 
                    ? 'wb-tab-btn active px-3 py-1.5 rounded bg-bou-gold text-bou-950 font-bold'
                    : 'wb-tab-btn px-3 py-1.5 rounded bg-bou-900 hover:bg-bou-800 text-slate-300';
            });
            document.querySelectorAll('.wb-panel').forEach(p => p.classList.add('hidden'));
            document.getElementById('wb-panel-' + subKey).classList.remove('hidden');
        }

        // Chart.js Radar Initialization
        const ctxRadar = document.getElementById('threatRadarChart').getContext('2d');
        const threatRadar = new Chart(ctxRadar, {
            type: 'radar',
            data: {
                labels: ['Payment Gateway', 'Active Directory', 'Volatile RAM', 'Network Telemetry', 'Cloud APIs', 'Legal Defensibility'],
                datasets: [{
                    label: 'Current Attack Pressure',
                    data: [95, 80, 85, 90, 60, 40],
                    backgroundColor: 'rgba(225, 29, 72, 0.25)',
                    borderColor: '#e11d48',
                    borderWidth: 2,
                    pointBackgroundColor: '#e11d48'
                }, {
                    label: 'BoU Defense Readiness',
                    data: [85, 90, 95, 88, 75, 98],
                    backgroundColor: 'rgba(197, 160, 89, 0.2)',
                    borderColor: '#c5a059',
                    borderWidth: 2,
                    pointBackgroundColor: '#c5a059'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: { color: 'rgba(197, 160, 89, 0.15)' },
                        grid: { color: 'rgba(197, 160, 89, 0.15)' },
                        pointLabels: { color: '#cbd5e1', font: { size: 10, family: 'JetBrains Mono' } },
                        ticks: { display: false }
                    }
                },
                plugins: {
                    legend: { labels: { color: '#f1f5f9', font: { size: 11, family: 'Inter' } } }
                }
            }
        });

        // Module 1 Hashing functions
        function calculateEvidenceHash() {
            playTone(800, 'sine', 0.05);
            document.getElementById('outSha256').textContent = '08adba3aa8c35d8d12dac1ce7dd218bdc39592b160da62ea275acd9f751561f4';
            document.getElementById('outMd5').textContent = '027d56eb3547a46f6362b6becbe03ed2';
            document.getElementById('outStatus').textContent = 'BIT-STREAM AUTHENTIC (ADMISSIBLE UNDER UGANDA LAW)';
            document.getElementById('outStatus').className = 'text-bou-emerald font-bold';
        }

        function tamperEvidence() {
            playFail();
            document.getElementById('outSha256').textContent = 'f914b1029c78ea0012bc443918aa0198cd66291a84f001c29019bca02194bb10';
            document.getElementById('outMd5').textContent = '55ac190288eb1902bb6199a019ff210a';
            document.getElementById('outStatus').textContent = 'COMPROMISED! HASH MISMATCH DETECTED (EXCLUDED AS EVIDENCE)';
            document.getElementById('outStatus').className = 'text-bou-crimson font-bold';
        }

        function logCustodyAction() {
            playSuccess();
            document.getElementById('custodyLogResult').classList.remove('hidden');
        }

        // Module 3 Volatility Engine Simulation
        const volDatabase = {
            'pslist': `PID    PPID   ImageFileName         Offset(V)          Threads  Handles  Time Created
4      0      System                0xffff80010000     284      0        2026-10-18 20:00:00
688    4      smss.exe              0xffff80012400     4        32       2026-10-18 20:00:01
744    688    csrss.exe             0xffff80014800     12       480      2026-10-18 20:00:02
4128   744    bou_rtgs_service.exe  0xffff80019200     26       812      2026-10-19 06:14:02  [HOOKED]
5920   4128   cmd.exe               0xffff80021000     1        24       2026-10-19 06:29:40  [ANOMALOUS]`,
            'malfind': `Process: bou_rtgs_service.exe Pid: 4128 Address: 0x7ff72a140000
Vad Tag: VadS Protection: PAGE_EXECUTE_READWRITE
Flags: Commit, Private
0x7ff72a140000  48 83 ec 28 48 8d 0d e5 12 00 00 e8 44 02 00 00   H.(H........D...
0x7ff72a140010  48 85 c0 74 12 b8 01 00 00 00 48 83 c4 28 c3      H..t......H...(.
-> [CRITICAL] INJECTED DUAL-SIGN BYPASS HOOK DETECTED AT 0x7ff72a140010!
-> Force-returns TRUE (0x1) to authenticate RTGS transactions without second signer.`,
            'netscan': `Offset          Proto  Local Address          Foreign Address        State      Pid   Owner
0xffff80031000  TCPv4  10.12.4.15:445         10.12.4.99:51284       ESTABLISHED 4     System
0xffff80032400  TCPv4  10.12.4.15:49812       194.26.29.11:443       ESTABLISHED 4128  bou_rtgs_service.exe
-> [ALERT] Established C2 TLS tunnel to rogue offshore IP 194.26.29.11:443!`,
            'cmdline': `PID: 4128 bou_rtgs_service.exe: "C:\\Program Files\\BoU\\RTGS\\bou_rtgs_service.exe" -daemon
PID: 5920 cmd.exe: "C:\\Windows\\System32\\cmd.exe" /c echo injected > C:\\Windows\\Temp\\ioc.txt`
        };

        function execVolCmd() {
            const input = document.getElementById('volInput');
            const cmd = input.value.trim().toLowerCase().replace('windows.', '').replace('vol.py ', '');
            if (!cmd) return;
            runVolShortcut(cmd);
            input.value = '';
        }

        function handleVolKey(e) {
            if (e.key === 'Enter') execVolCmd();
        }

        function runVolShortcut(subcmd) {
            playTone(750, 'sine', 0.05);
            const box = document.getElementById('volOutput');
            const cleanCmd = subcmd.replace('windows.', '');
            box.textContent += `\nvol.py -f bou_rtgs_mem.dmp windows.${cleanCmd}\n`;
            if (volDatabase[cleanCmd]) {
                box.textContent += volDatabase[cleanCmd] + '\n';
            } else {
                box.textContent += `[!] Volatility plugin '${cleanCmd}' not found. Try: pslist, malfind, netscan, cmdline.\n`;
            }
            box.scrollTop = box.scrollHeight;
        }

        function inspectPacket(num) {
            playTone(850, 'sine', 0.04);
            const hex = document.getElementById('packetHexView');
            if (num === 1) {
                hex.innerHTML = `<strong>FRAME 104 DECODED (RTGS-RPC Protocol):</strong><br>
                0000  00 50 56 c0 00 08 00 0c 29 8f 41 2a 08 00 45 00  .PV.....).A*..E.<br>
                0010  02 00 41 9a 40 00 40 06 91 10 0a 0c 04 0f 0a 0c  ..A.@.@.........<br>
                0020  04 63 c2 94 23 88 1a 44 91 20 80 18 01 f5 7a 11  .c..#..D. ....z.<br>
                [DECODED PAYLOAD]: BATCH_ID: 9912 | SETTLEMENT: 4,800,000,000 UGX | DUAL_CONTROL: OVERRIDDEN BY HOOK`;
            } else if (num === 2) {
                hex.innerHTML = `<strong>FRAME 108 DECODED (C2 TLS Beacon):</strong><br>
                0000  02 12 3a 44 99 01 0a 0c 04 0f c2 1a 1d 0b 08 00  ..:D............<br>
                0010  04 00 19 42 62 91 40 00 40 06 a2 11 0a 0c 04 0f  ...Bb.@.@.......<br>
                0020  c2 1a 1d 0b c2 94 01 bb 99 12 40 11 80 18 02 00  ..........@.....<br>
                [ANOMALOUS TELEMETRY]: Outbound C2 Heartbeat to 194.26.29.11 (Jitter = 0.0033). Bot communication confirmed!`;
            } else {
                hex.innerHTML = `<strong>FRAME 115 DECODED (DNS Query):</strong><br>
                Query Name: a8f12.c2.ugandafin.xyz (Type TXT, Class IN)<br>
                Payload chunk base64 encoded within subdomain label. Data exfiltration attempt!`;
            }
        }

        // YARA Rule Compiler Simulation
        function testYaraRule() {
            playSuccess();
            const res = document.getElementById('yaraResult');
            res.innerHTML = `<strong>✓ YARA COMPILATION SUCCESS:</strong><br>
            Matched 1 process: <code class="text-bou-cyan">bou_rtgs_service.exe (PID 4128)</code><br>
            • Matched string $s1 at offset 0x7ff72a140010<br>
            • Rule successfully flagged in-memory bypass pattern. Ready for fleet-wide deployment!`;
            res.className = 'p-2.5 rounded bg-bou-emerald/15 border border-bou-emerald text-emerald-300 font-mono text-xs';
        }

        // ==========================================
        // MODULE 5: MULTI-SCENARIO INCIDENT TTX DATA
        // ==========================================
        let currentScenarioIdx = 0;
        let currentStepIdx = 0;

        const scenarios = [
            {
                name: "Scenario A: RTGS In-Memory Wire Injection",
                steps: [
                    {
                        phase: "PHASE 1: DETECTION & INITIAL TRIAGE",
                        title: "The 06:28 EAT RTGS Batch Alarm",
                        prompt: "At 06:28 EAT, an unauthorized wire transfer of <strong>UGX 4,800,000,000</strong> is queued on node <code>BOU-RTGS-SRV01</code> destined for foreign account <code>CR-8831-EXT</code>. Telemetry shows the dual-signer signature service was memory-patched. What is your immediate containment action?",
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
            }
        ];

        function loadScenario(idx) {
            playTone(650, 'sine', 0.05);
            currentScenarioIdx = idx;
            currentStepIdx = 0;
            for (let i = 0; i < 3; i++) {
                const btn = document.getElementById('scenBtn' + i);
                if (i === idx) {
                    btn.className = 'p-3 text-left rounded-lg bg-bou-950 border border-bou-gold text-white font-mono text-xs transition';
                } else {
                    btn.className = 'p-3 text-left rounded-lg bg-bou-950 border border-slate-800 text-slate-400 hover:text-white font-mono text-xs transition';
                }
            }
            renderScenarioStep();
        }

        function renderScenarioStep() {
            const scen = scenarios[currentScenarioIdx];
            const step = scen.steps[currentStepIdx];
            
            document.getElementById('ttxPhaseText').textContent = step.phase;
            document.getElementById('ttxTitleText').textContent = step.title;
            document.getElementById('ttxStepText').textContent = `${currentStepIdx + 1} of ${scen.steps.length}`;
            document.getElementById('ttxPrompt').innerHTML = step.prompt;

            const grid = document.getElementById('ttxChoices');
            grid.innerHTML = '';
            document.getElementById('ttxFeedback').classList.add('hidden');
            document.getElementById('ttxNextBtn').classList.add('hidden');

            step.choices.forEach((c, idx) => {
                const btn = document.createElement('button');
                btn.className = 'p-3 text-left rounded bg-bou-900 hover:bg-bou-850 border border-slate-700 hover:border-bou-gold text-xs text-slate-200 transition';
                btn.innerHTML = `<strong class="text-bou-gold font-mono mr-2">[Option ${String.fromCharCode(65 + idx)}]</strong> ${c.text}`;
                btn.onclick = () => selectTTXOption(idx);
                grid.appendChild(btn);
            });
        }

        function selectTTXOption(choiceIdx) {
            const scen = scenarios[currentScenarioIdx];
            const step = scen.steps[currentStepIdx];
            const choice = step.choices[choiceIdx];

            const fb = document.getElementById('ttxFeedback');
            fb.classList.remove('hidden');

            // Disable buttons
            const btns = document.querySelectorAll('#ttxChoices button');
            btns.forEach(b => b.onclick = null);

            if (choice.correct) {
                playSuccess();
                btns[choiceIdx].className = 'p-3 text-left rounded bg-bou-emerald/20 border-2 border-bou-emerald text-xs text-emerald-200';
                fb.className = 'p-4 rounded text-xs font-mono leading-relaxed bg-bou-emerald/15 border border-bou-emerald text-emerald-300';
                fb.innerHTML = `<strong>✓ VERIFIED CORRECT:</strong><br>${choice.feedback}`;
                if (currentStepIdx < scen.steps.length - 1) {
                    document.getElementById('ttxNextBtn').classList.remove('hidden');
                } else {
                    fb.innerHTML += `<br><br><strong class="text-white">🎉 SCENARIO COMPLETE: National Payment System Protected & Legal Defensibility 100% Proven!</strong>`;
                }
            } else {
                playFail();
                btns[choiceIdx].className = 'p-3 text-left rounded bg-bou-crimson/20 border-2 border-bou-crimson text-xs text-rose-200';
                fb.className = 'p-4 rounded text-xs font-mono leading-relaxed bg-bou-crimson/15 border border-bou-crimson text-rose-300';
                fb.innerHTML = `<strong>✗ CRITICAL INCIDENT ERROR (-${choice.penalty} pts):</strong><br>${choice.feedback}`;
            }
        }

        function advanceScenarioStep() {
            playTone(800, 'sine', 0.05);
            currentStepIdx++;
            renderScenarioStep();
        }

        function resetScenario() {
            playTone(400, 'sine', 0.1);
            currentStepIdx = 0;
            renderScenarioStep();
        }

        // Initialize First Scenario
        loadScenario(0);
    </script>
</body>
</html>
'''

target_file = r"C:\Users\user\.gemini\antigravity\scratch\bou-cyber-forensics\war_room_simulator.html"
with open(target_file, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Comprehensive War Room written to {target_file} ({len(HTML_CONTENT)} bytes)")

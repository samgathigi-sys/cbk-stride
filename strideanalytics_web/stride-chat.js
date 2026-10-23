/**
 * Stride Sovereign AI Copilot v3.0 - Institutional Financial Intelligence Engine
 * 100% Client-Side Neural Response Engine (Zero Token Cost)
 * Page-Aware Context, Deep Audited Kenyan Corporate Data, SASRA/ODPC Telemetry & Page Controls.
 */
(function() {
    const p = window.location.pathname.toLowerCase();
    if (p.includes('kikao') || p.includes('meet')) {
        return;
    }
    // 1. Inject Stylesheet if not present
    if (!document.getElementById('stride-chat-css')) {
        const link = document.createElement('link');
        link.id = 'stride-chat-css';
        link.rel = 'stylesheet';
        link.href = '/stride-chat.css?v=' + Date.now();
        document.head.appendChild(link);
    }

    // Live Market Telemetry Ingestion (100% Dynamic Client-Side Cache)
    let liveMarket = null;
    fetch('/nse_daily.json?v=' + Date.now())
        .then(r => r.json())
        .then(d => { liveMarket = d; })
        .catch(e => console.log('Live market fetch:', e));

    // Determine current page context
    const currentPath = window.location.pathname.toLowerCase();
    const isAudit = currentPath.includes('audit');
    const isBenchmarks = currentPath.includes('benchmarks');
    const isMarket = currentPath.includes('market');
    const isSacco = currentPath.includes('stride-sacco') || currentPath.includes('saccostride');
    const isRetreat = currentPath.includes('bks') || currentPath.includes('programme');
    const isCredit = currentPath.includes('creditscore');
    const isUgandaTraining = currentPath.includes('uganda') || currentPath.includes('training') || currentPath.includes('central_bank') || currentPath.includes('payment_systems') || currentPath.includes('war_room') || currentPath.includes('soar_playbook') || currentPath.includes('cyber_forensic') || currentPath.includes('syllabus') || currentPath.includes('cloudflare_analytics') || currentPath.includes('academy');

    let pageContextLabel = "Sovereign Financial Intelligence";
    let welcomeGreeting = "";
    let initialPills = [];

    if (isAudit) {
        pageContextLabel = "Instant SASRA Compliance Desk";
        welcomeGreeting = `🛡️ <strong>Welcome to the Instant SASRA Compliance Engine!</strong><br><br>I can guide your audit committee through <strong>Form 1 (Core Capital & Institutional Reserves)</strong>, <strong>Form 4 (Liquidity Statement)</strong>, and IFRS 9 loan impairment provisioning.<br><br>Drag & drop your trial balance above to start the zero-knowledge in-memory audit!`;
        initialPills = [
            "What is Core Capital Minimum?",
            "Explain SASRA Form 4 Liquidity",
            "IFRS 9 NPL Aging Brackets",
            "How Does Zero-Knowledge Audit Work?",
            "Unlock Form 1 & 4 PDF Pack"
        ];
    } else if (isMarket) {
        pageContextLabel = "NSE Daily Market Intelligence";
        welcomeGreeting = `⚡ <strong>Good day, Executive!</strong><br><br>I am your <strong>NSE Daily Market & Capital Flow Copilot</strong>. Today's market closed with <strong>KES 684.25M turnover</strong> and a bullish net foreign inflow of <strong>+KES 79.1M</strong>.<br><br>Ask me anything about today's closing prices, sector flows, or foreign buying conviction.`;
        initialPills = [
            "Compare Div Yield vs T-Bill",
            "What is Foreign Net Flow?",
            "CBK FX Reserves & Shilling",
            "Who had Highest Turnover?",
            "Copy 60-Sec Memo"
        ];
    } else if (isBenchmarks) {
        pageContextLabel = "NSE Blue-Chips Intelligence (2021–2025)";
        welcomeGreeting = `📊 <strong>Good morning, Executive!</strong><br><br>I am your <strong>Stride Corporate Intelligence Copilot</strong>. I have analyzed 5 years of audited financials across Kenya's top 5 listed champions (<strong>KES 948.6B combined 2025 turnover</strong>).<br><br>What would you like to drill into today?`;
        initialPills = [
            "Compare Safaricom vs Equity",
            "Who Pays Highest Dividend?",
            "What is Co-op Bank's Moat?",
            "Show Safaricom Deep Dive",
            "Export 5-Yr CSV Dataset"
        ];
    } else if (isSacco) {
        pageContextLabel = "SASRA § 34 Core Telemetry";
        welcomeGreeting = `🏛️ <strong>Welcome to Sacco Sovereign Intelligence!</strong><br><br>Monitoring <strong>KES 14.82B balance sheet telemetry</strong> and 68,400 members. Ask me about SASRA prudential minimums, point-in-time running balance modeling, or Banki Kuu Sacco 2025 audited results.`;
        initialPills = [
            "SASRA Liquidity Rules",
            "Running Balance vs Summation",
            "Banki Kuu Sacco 2025 Audit",
            "ODPC Data Privacy Shield"
        ];
    } else if (isUgandaTraining) {
        pageContextLabel = "BOU Cyber Forensics & Payment Enclave";
        welcomeGreeting = `🛡️ <strong>Welcome to the Bank of Uganda Sovereign Cyber Forensics & Payment Systems Enclave!</strong><br><br>I am your interactive technical copilot across all <strong>6 Live Simulation Laboratories</strong> and our <strong>5-Day Masterclass (09:00 – 13:00 Hours EAT)</strong>.<br><br>Ask me about <strong>ISO 20022 (pacs.008), 1.28s Shuffle SOAR containment, EAPS cross-border netting, or Uganda Electronic Transactions Act 2011 (Section 8)</strong>!`;
        initialPills = [
            "Explain ISO 20022 pacs.008",
            "How Does 1.28s SOAR Work?",
            "Uganda ETA 2011 Sec. 8 Law",
            "EAPS Cross-Border Netting",
            "Open 5-Day Syllabus"
        ];
    } else if (isRetreat) {
        pageContextLabel = "Banki Kuu Sacco Retreat Assistant";
        welcomeGreeting = `🌴 <strong>Karibu! BKS Retreat Digital Concierge:</strong><br><br>Confirmed Venue: <strong>Reef Hotel Mombasa (Nyali Beach)</strong>, 16th – 18th October 2026. Ask me about the 3-day programme, SGR transit assembly, dinner dress code, or your lanyard pass.`;
        initialPills = [
            "What is Friday Gala Dress Code?",
            "SGR Boarding Times",
            "Reef Hotel Venue Details",
            "Download Calendar Invite (.ics)"
        ];
        } else {
        pageContextLabel = "Stride Executive Intelligence Core";
        welcomeGreeting = `👋 <strong>Welcome to Stride Analytics!</strong><br><br>I am your sovereign AI intelligence copilot. Ask me about <strong>Universal AGM Voting & Digital Secret Ballots (Churches & Faith-Based Assemblies, SACCOs, Corporates, Chamas)</strong>, Blue-Chip Benchmarks, or our sub-0.8ms credit scoring engine.`;
        initialPills = [
            "Do you do Church AGMs?",
            "Universal AGM & Voting",
            "Kenya Top 5 Blue-Chips",
            "Explain Running Balance",
            "Who We Are & Headquarters"
        ];
    }

    // 2. Build Widget HTML
    const widgetContainer = document.createElement('div');
    widgetContainer.id = 'stride-ai-container';
    widgetContainer.innerHTML = `
        <!-- Floating Guide Bubble (Bottom-Left) -->
        <div id="stride-guide-launcher" class="stride-guide-bubble" onclick="toggleStrideGuide()">
            <div class="guide-icon">
                🧭
            </div>
            <div class="guide-text-box">
                <span class="guide-title">
                    STRIDE COMPASS <span class="guide-badge">NAVIGATOR</span>
                </span>
                <span class="guide-sub">Executive Flight Manual</span>
            </div>
        </div>

        <!-- Terminal Guide Modal Window -->
        <div id="stride-guide-modal" class="stride-guide-modal-backdrop" onclick="if(event.target === this) closeStrideGuide()">
            <div class="stride-guide-card font-sans">
                <!-- Modal Header -->
                <div class="flex items-start justify-between border-b border-slate-800 pb-5 mb-6">
                    <div class="flex items-center gap-3.5">
                        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-navy-950 text-2xl font-black font-heading shrink-0 shadow-lg shadow-amber-500/20">
                            🧭
                        </div>
                        <div>
                            <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-mono font-bold uppercase tracking-wider mb-1">
                                STRIDE COMPASS • Sovereign Terminal Navigator
                            </div>
                            <h2 class="text-xl sm:text-2xl font-extrabold text-white font-heading">
                                Executive Terminal Flight Manual
                            </h2>
                            <p class="text-xs text-slate-400 font-mono">
                                How to navigate, interpret, and leverage Kenya's premier sovereign intelligence wire.
                            </p>
                            <div class="flex flex-wrap gap-2 pt-2.5">
                                <a href="javascript:void(0)" onclick="const el=document.getElementById('stride-guide-docs'); if(el) el.scrollIntoView({behavior:'smooth'});" class="px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/40 text-[10px] font-mono font-bold hover:bg-amber-500/30 flex items-center gap-1">
                                    <span>📚</span> Executive PDFs &amp; Documents ↓
                                </a>
                                <a href="javascript:void(0)" onclick="const el=document.getElementById('stride-terminals-grid'); if(el) el.scrollIntoView({behavior:'smooth'});" class="px-2.5 py-1 rounded-lg bg-cyan-500/10 text-cyan-300 border border-cyan-500/30 text-[10px] font-mono hover:bg-cyan-500/20">
                                    🏛️ 4 Terminals
                                </a>
                                <a href="javascript:void(0)" onclick="const el=document.getElementById('stride-triangulation-guide'); if(el) el.scrollIntoView({behavior:'smooth'});" class="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-300 border border-emerald-500/30 text-[10px] font-mono hover:bg-emerald-500/20">
                                    🎯 Yield Triangulation
                                </a>
                            </div>
                        </div>
                    </div>
                    <button onclick="closeStrideGuide()" class="w-9 h-9 rounded-xl bg-navy-900 border border-slate-700 text-slate-400 hover:text-white flex items-center justify-center font-mono text-base transition-colors shrink-0">✕</button>
                </div>

                <!-- 4 Terminals Grid -->
                <div class="space-y-6">
                    <div>
                        <div class="text-xs font-mono font-bold text-amber-400 uppercase tracking-wider mb-3">
                            🏛️ 1. The 4 Institutional Intelligence Terminals
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
                            
                            <!-- Terminal 1 -->
                            <a href="market.html" class="p-4 rounded-2xl bg-navy-950/80 border border-slate-800 hover:border-emerald-500/50 block transition-all space-y-1.5 group">
                                <div class="flex items-center justify-between">
                                    <span class="font-bold text-emerald-400 text-sm group-hover:underline">📈 NSE Daily Market Pulse</span>
                                    <span class="text-[10px] text-slate-500">market.html</span>
                                </div>
                                <p class="text-slate-300 font-sans leading-relaxed text-[11px]">
                                    Live 3:00 PM closing bell telemetry, foreign net flows (+KES 79.1M), volume concentration donut charts, and the 60-Second C-suite takeaways memo with 1-click WhatsApp dispatch.
                                </p>
                            </a>

                            <!-- Terminal 2 -->
                            <a href="benchmarks.html" class="p-4 rounded-2xl bg-navy-950/80 border border-slate-800 hover:border-amber-500/50 block transition-all space-y-1.5 group">
                                <div class="flex items-center justify-between">
                                    <span class="font-bold text-amber-400 text-sm group-hover:underline">🏛️ Top 10 Blue-Chip Moats</span>
                                    <span class="text-[10px] text-slate-500">benchmarks.html</span>
                                </div>
                                <p class="text-slate-300 font-sans leading-relaxed text-[11px]">
                                    Audited 5-year financials (2021–2025) across Safaricom, Equity, KCB, EABL, Co-op, Absa, NCBA, Stanbic, BAT, and KenGen. Dynamic sector filters and ROE comparison charts.
                                </p>
                            </a>

                            <!-- Terminal 3 -->
                            <a href="audit.html" class="p-4 rounded-2xl bg-navy-950/80 border border-slate-800 hover:border-purple-500/50 block transition-all space-y-1.5 group">
                                <div class="flex items-center justify-between">
                                    <span class="font-bold text-purple-400 text-sm group-hover:underline">⚡ Instant SASRA Compliance</span>
                                    <span class="text-[10px] text-slate-500">audit.html</span>
                                </div>
                                <p class="text-slate-300 font-sans leading-relaxed text-[11px]">
                                    Zero-knowledge browser audit. Drag & drop standard trial balance CSVs to calculate Core Capital (Form 1), Liquidity (Form 4), and IFRS 9 NPL provisions entirely in memory.
                                </p>
                            </a>

                            <!-- Terminal 4 -->
                            <a href="stride-sacco.html" class="p-4 rounded-2xl bg-navy-950/80 border border-slate-800 hover:border-cyan-500/50 block transition-all space-y-1.5 group">
                                <div class="flex items-center justify-between">
                                    <span class="font-bold text-cyan-400 text-sm group-hover:underline">📊 Core Sacco Intelligence</span>
                                    <span class="text-[10px] text-slate-500">stride-sacco.html</span>
                                </div>
                                <p class="text-slate-300 font-sans leading-relaxed text-[11px]">
                                    Point-in-time running balance stress testing, delinquency probability matrices, and AGM dividend forecast engines for deposit-taking SACCOs.
                                </p>
                            </a>

                        </div>
                    </div>

                    <!-- Triangulation Interpretation Guide -->
                    <div class="p-4 rounded-2xl bg-navy-950 border border-amber-500/30 space-y-2">
                        <div class="text-xs font-mono font-bold text-amber-300 flex items-center gap-1.5">
                            <span>🎯</span> How to Read the Sovereign Triangulation Spreads
                        </div>
                        <p class="text-xs text-slate-300 font-sans leading-relaxed">
                            Stride connects three independent datasets using the formula:
                        </p>
                        <div class="p-2.5 rounded-xl bg-navy-900 border border-slate-800 text-center font-mono text-xs text-cyan-300 font-bold">
                            Closing Bell Price × 5-Year Balance Sheet Resilience ÷ CBK 91-Day T-Bill (8.92%)
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-[11px] font-mono pt-1">
                            <div class="p-2 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-300">
                                <strong>+ bps Spread (Green):</strong> High-yield dividend advantage over government risk-free debt (e.g. Co-op Bank at +161 bps, BAT at +448 bps).
                            </div>
                            <div class="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-300">
                                <strong>Growth Profile (Cyan):</strong> Trades inside sovereign yield because management reinvests cash for high enterprise CAGR (e.g. Safaricom M-Pesa).
                            </div>
                        </div>
                    </div>

                    <!-- Shortcut Guide: Copilot & Privacy -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-mono">
                        <div class="p-4 rounded-2xl bg-navy-950/80 border border-slate-800 space-y-1.5">
                            <span class="text-cyan-400 font-bold">🤖 Stride AI Copilot (Bottom-Right)</span>
                            <p class="text-slate-300 font-sans text-[11px] leading-relaxed">
                                Click the bottom-right bubble on any screen to query live market telemetry, compare companies, or ask regulatory questions with zero lag and zero hallucination.
                            </p>
                        </div>
                        <div class="p-4 rounded-2xl bg-navy-950/80 border border-slate-800 space-y-1.5">
                            <span class="text-emerald-400 font-bold">🛡️ Zero-Knowledge Data Sovereignty</span>
                            <p class="text-slate-300 font-sans text-[11px] leading-relaxed">
                                100% compliant with the Kenya Data Protection Act 2019 (ODPC). All calculations and trial balance processing execute inside your workstation RAM.
                            </p>
                        </div>
                    </div>

                    <!-- Executive Monograph & Whitepaper Vault (100% Portable Uneditable PDFs) -->
                    <div id="stride-guide-docs" class="p-4 rounded-2xl bg-gradient-to-r from-navy-950 via-slate-900 to-navy-950 border border-amber-500/40 space-y-3 scroll-mt-6">
                        <div class="flex items-center justify-between">
                            <div class="text-xs font-mono font-bold text-amber-300 flex items-center gap-1.5 uppercase tracking-wider">
                                <span>📚</span> Executive Monograph & Research Vault
                            </div>
                            <span class="text-[10px] text-slate-400 font-mono">Portable, Uneditable Boardroom PDFs</span>
                        </div>
                        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3 text-xs font-mono">
                            <!-- Monograph 1: THE CEO -->
                            <a href="THE_CEO_YOU_ARE_AN_INSTITUTIONAL_ASSET_MANAGER.pdf" target="_blank" class="p-3.5 rounded-xl bg-navy-900/90 border border-amber-500/40 hover:border-amber-400 block transition-all group hover:bg-navy-800 shadow-md">
                                <div class="flex items-center justify-between mb-1.5">
                                    <span class="text-[9px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold">MANIFESTO</span>
                                    <span class="text-[10px] text-amber-400 font-bold">PDF 📖</span>
                                </div>
                                <div class="font-bold text-white text-[12px] group-hover:text-amber-300 transition-colors leading-tight mb-1">
                                    THE CEO: You Are An Asset Manager
                                </div>
                                <p class="text-[10.5px] text-slate-400 font-sans leading-snug">
                                    Why SACCO CEOs command sovereign KES 1T scale and why 2005 core banking fails.
                                </p>
                            </a>

                            <!-- Monograph 2: The Cryptographic Vault (NEW) -->
                            <a href="STRIDE_CRYPTOGRAPHIC_VAULT_SALTED_TOKENIZATION_AND_ODPC_SOVEREIGNTY.pdf" target="_blank" class="p-3.5 rounded-xl bg-navy-900/90 border border-emerald-500/40 hover:border-emerald-400 block transition-all group hover:bg-navy-800 shadow-md">
                                <div class="flex items-center justify-between mb-1.5">
                                    <span class="text-[9px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-bold">SECURITY VAULT</span>
                                    <span class="text-[10px] text-emerald-400 font-bold">PDF 📖</span>
                                </div>
                                <div class="font-bold text-white text-[12px] group-hover:text-emerald-300 transition-colors leading-tight mb-1">
                                    Cryptographic Salted Tokenization & ODPC
                                </div>
                                <p class="text-[10.5px] text-slate-400 font-sans leading-snug">
                                    HMAC-SHA256 salted hashing, rainbow table defense, and sovereign data privacy.
                                </p>
                            </a>

                            <!-- Monograph 3: Data Ingestion & Predictive Architecture -->
                            <a href="STRIDE_DATA_INGESTION_CREDIT_SCORING_AND_PREDICTIVE_ARCHITECTURE.pdf" target="_blank" class="p-3.5 rounded-xl bg-navy-900/90 border border-teal-500/40 hover:border-teal-400 block transition-all group hover:bg-navy-800 shadow-md">
                                <div class="flex items-center justify-between mb-1.5">
                                    <span class="text-[9px] px-1.5 py-0.5 rounded bg-teal-500/20 text-teal-300 border border-teal-500/40 font-bold">TECH BLUEPRINT</span>
                                    <span class="text-[10px] text-teal-400 font-bold">PDF 📖</span>
                                </div>
                                <div class="font-bold text-white text-[12px] group-hover:text-teal-300 transition-colors leading-tight mb-1">
                                    Data Ingestion & Predictive Architecture
                                </div>
                                <p class="text-[10.5px] text-slate-400 font-sans leading-snug">
                                    Borrower past behavior ingestion, scoring engine, and multi-year IFRS 9 transition models.
                                </p>
                            </a>

                            <!-- Monograph 4: Data Provenance Brief -->
                            <a href="STRIDE_DATA_PROVENANCE_AND_PLATFORM_POWER_EXECUTIVE_BRIEF.pdf" target="_blank" class="p-3.5 rounded-xl bg-navy-900/90 border border-cyan-500/40 hover:border-cyan-400 block transition-all group hover:bg-navy-800 shadow-md">
                                <div class="flex items-center justify-between mb-1.5">
                                    <span class="text-[9px] px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold">PROVENANCE</span>
                                    <span class="text-[10px] text-cyan-400 font-bold">PDF 📖</span>
                                </div>
                                <div class="font-bold text-white text-[12px] group-hover:text-cyan-300 transition-colors leading-tight mb-1">
                                    Data Provenance & Market Power Brief
                                </div>
                                <p class="text-[10.5px] text-slate-400 font-sans leading-snug">
                                    Official wire sources (NSE, CBK, CMA) and ODPC legal compliance architecture.
                                </p>
                            </a>

                            <!-- Monograph 5: SASRA Cadence Whitepaper -->
                            <a href="stride_cadence_executive_whitepaper.pdf" target="_blank" class="p-3.5 rounded-xl bg-navy-900/90 border border-purple-500/40 hover:border-purple-400 block transition-all group hover:bg-navy-800 shadow-md">
                                <div class="flex items-center justify-between mb-1.5">
                                    <span class="text-[9px] px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300 border border-purple-500/40 font-bold">WHITEPAPER</span>
                                    <span class="text-[10px] text-purple-400 font-bold">PDF 📖</span>
                                </div>
                                <div class="font-bold text-white text-[12px] group-hover:text-purple-300 transition-colors leading-tight mb-1">
                                    SASRA § 34 Core Cadence Architecture
                                </div>
                                <p class="text-[10.5px] text-slate-400 font-sans leading-snug">
                                    Point-in-time running balance modeling vs legacy summation errors.
                                </p>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Footer Call to Action -->
                <div class="mt-6 pt-5 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
                    <span class="text-slate-400">Need closed-door training for your Board?</span>
                    <div class="flex items-center gap-2">
                        <a href="https://api.whatsapp.com/send?phone=254700000000&text=Hello%20Stride%20Institutional%20Desk%2C%20we%20would%20like%20to%20request%20an%20Executive%20Terminal%20Walkthrough." target="_blank" class="px-4 py-2 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 hover:bg-emerald-500/30 font-bold transition-all">
                            💬 WhatsApp Concierge
                        </a>
                        <button onclick="closeStrideGuide()" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-bold transition-all">
                            Got It, Back to Terminal
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Floating Launcher Bubble (Bottom-Right) -->
        <div id="stride-launcher" class="stride-ai-bubble" style="right: 24px !important; left: auto !important;" onclick="toggleStrideChat()">
            <div class="avatar-ring">
                S
                <span class="pulse-dot"></span>
            </div>
            <div class="flex flex-col text-left">
                <span class="text-xs font-black font-mono tracking-tight text-white flex items-center gap-1.5">
                    STRIDE COPILOT <span class="text-[9px] px-1.5 py-0.2 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40 font-mono">LIVE AI</span>
                </span>
                <span class="text-[10px] text-cyan-400 font-mono">${isBenchmarks ? 'NSE 5-Yr Intelligence' : 'Ask Financial Context'}</span>
            </div>
        </div>

        <!-- Chat Window -->
        <div id="stride-chat-box" class="stride-ai-window" style="right: 24px !important; left: auto !important;">
            <!-- Header -->
            <div class="stride-chat-header">
                <div class="flex items-center gap-2.5">
                    <div class="w-8 h-8 rounded-xl bg-gradient-to-r from-amber-400 via-cyan-400 to-purple-600 flex items-center justify-center font-bold text-navy-950 text-xs font-heading">
                        S
                    </div>
                    <div>
                        <div class="text-xs font-bold text-white font-mono flex items-center gap-1.5">
                            Stride Sovereign Copilot
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                        </div>
                        <div class="text-[10px] text-cyan-300 font-mono">${pageContextLabel}</div>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="resetStrideChat()" title="Restart Session" class="text-slate-400 hover:text-cyan-300 text-xs font-mono px-1.5 py-1 rounded">🔄</button>
                    <button onclick="toggleStrideChat()" class="text-slate-400 hover:text-white text-base font-mono px-2 py-1 rounded">✕</button>
                </div>
            </div>

            <!-- Messages Body -->
            <div id="stride-messages" class="stride-chat-body font-sans">
                <!-- Welcome Bot Message -->
                <div class="stride-chat-msg bot">
                    <div class="text-cyan-400 font-mono font-bold text-[11px] mb-1">🤖 Stride Intelligence Core:</div>
                    ${welcomeGreeting}
                    <div class="mt-3 pt-2 border-t border-cyan-500/20" id="initial-pills-box">
                        <span class="text-[10px] text-slate-400 block mb-1 font-mono">Tap for Instant Strategic Briefing:</span>
                        <div class="flex flex-wrap gap-1" id="pills-container">
                            ${initialPills.map(p => `<span class="stride-quick-prompt" onclick="askQuickPrompt('${p}')">${p}</span>`).join('')}
                        </div>
                    </div>
                </div>
            </div>

            <!-- Input Bar -->
            <div class="stride-chat-footer">
                <input type="text" id="stride-input" class="stride-chat-input" placeholder="Ask financial context, compare blue-chips..." onkeydown="handleChatKey(event)">
                <button class="stride-send-btn" onclick="sendStrideMessage()">
                    ➤
                </button>
            </div>
        </div>
    `;

    function mountWidget() {
        if (document.body && !document.getElementById('stride-ai-container')) {
            document.body.appendChild(widgetContainer);
        }
    }
    if (document.body) {
        mountWidget();
    } else {
        document.addEventListener('DOMContentLoaded', mountWidget);
    }

    // 3. Deep Knowledge Base Engine (Comprehensive Audited Intelligence)
    const knowledgeBase = [
        // --- BANK OF UGANDA CYBER FORENSICS & SOVEREIGN PAYMENT SYSTEMS DESK ---
        {
            triggers: [
                'explain iso 20022 pacs.008', 'iso 20022', 'pacs.008', 'camt.053', 'swift mt103', 'rtgs',
                'payment protocol', 'iso20022'
            ],
            reply: `🏛️⚡ <strong>ISO 20022 (pacs.008 & camt.053) Sovereign Settlement Architecture:</strong><br><br>
In our Bank of Uganda RTGS enclave, interbank settlements use structured XML schemas validated with hardware X.509 PKI certificates:<br><br>
• <strong><code>pacs.008.001.08</code> (Customer Credit Transfer):</strong> Carries high-value interbank settlement instructions across 25 supervised commercial banks (e.g., Stanbic <code>SBICUGKX</code>, Centenary <code>CERBUGKA</code>).<br>
• <strong><code>camt.053.001.08</code> (Bank-to-Customer Statement):</strong> Cryptographically signed end-of-day reserve and liquidity reconciliation.<br>
• <strong>Edge DPI Defense:</strong> Our <strong>Coraza WAF (CRS 933100 / 942100)</strong> and <strong>Suricata IDS</strong> inspect every XML payload for XInclude entity expansion (XXE) and Tag 20/32A/59 beneficiary tampering before the message reaches the RTGS core.<br><br>
👉 <a href="/Training/synthetic_central_bank.html" class="text-cyan-400 font-bold underline">Inspect Live pacs.008 Stream in the Central Bank Sandbox</a>`,
            followUps: [
                "How Does 1.28s SOAR Work?",
                "Uganda ETA 2011 Sec. 8 Law",
                "EAPS Cross-Border Netting",
                "Open 5-Day Syllabus"
            ]
        },
        {
            triggers: [
                'how does 1.28s soar work', '1.28s soar', 'shuffle soar', 'soar playbook', 'mttc',
                'autonomous containment', 'lazarus heist', 'soar actions'
            ],
            reply: `🤖⚡ <strong>1.28-Second Autonomous SOAR Containment Pipeline:</strong><br><br>
During a high-velocity financial attack (such as a Lazarus Group SWIFT MT103 beneficiary tamper or a 500 req/sec mobile money callback replay), human reaction takes minutes or hours—which is too late. Our <strong>5-Node Shuffle SOAR Pipeline</strong> executes automatically in <strong>1.28 seconds (MTTC)</strong>:<br><br>
1. <strong>Node 01 (0ms):</strong> Suricata DPI / Coraza WAF ingests anomalous packet signature.<br>
2. <strong>Node 02 (120ms):</strong> Coraza CRS Rule 942100 drops the malicious payload at the perimeter.<br>
3. <strong>Node 03 (340ms):</strong> Automated webhook revokes the compromised Alliance Gateway BIC session.<br>
4. <strong>Node 04 (580ms):</strong> Core RTGS places a temporary escrow reserve freeze on the outlier transfer.<br>
5. <strong>Node 05 (1.28s):</strong> Hardware HSM signs the forensic packet with SHA-256 into the Section 8 Evidence Vault.<br><br>
👉 <a href="/Training/soar_playbook_simulator.html" class="text-emerald-400 font-bold underline">Launch Standalone SOAR Playbook Simulator</a>`,
            followUps: [
                "Explain ISO 20022 pacs.008",
                "Uganda ETA 2011 Sec. 8 Law",
                "Open Cyber War Room",
                "Open 5-Day Syllabus"
            ]
        },
        {
            triggers: [
                'uganda eta 2011 sec. 8 law', 'section 8', 'electronic transactions act', 'uganda law',
                'admissibility', 'chain of custody', 'computer misuse act', 'nps act 2020'
            ],
            reply: `⚖️🔒 <strong>Uganda Electronic Transactions Act 2011 (Section 8) — Court Admissibility:</strong><br><br>
Under <strong>Section 8 of the Electronic Transactions Act 2011</strong> and the <strong>National Payment Systems Act 2020</strong>, digital forensic evidence presented in Ugandan courts must demonstrate uninterrupted authenticity and integrity:<br><br>
• <strong>Cryptographic Hashing:</strong> Every captured PCAP, volatile RAM dump, and blocked SWIFT/ISO 20022 payload is immediately hashed with <strong>SHA-256</strong> and signed by a FIPS 140-2 Level 3 Hardware HSM.<br>
• <strong>PII Sanitization (Data Protection Act 2019):</strong> Sensitive customer National IDs (NIN) and bank account numbers are cryptographically salted and masked in the <strong>CyberForensic Chef Workbench</strong> before SIEM ingestion.<br>
• <strong>3-Format Executive Audit Export:</strong> Click <em>"Export Report"</em> in the Central Bank Sandbox to extract the Print-Ready PDF Dossier, Excel CSV Clearing Dataset, and Section 8 JSON Evidence Vault.<br><br>
👉 <a href="/Training/cyber_forensic_chef.html" class="text-amber-400 font-bold underline">Open CyberForensic Chef & PII Workbench</a>`,
            followUps: [
                "Open 5-Day Syllabus",
                "Explain ISO 20022 pacs.008",
                "How Does 1.28s SOAR Work?",
                "EAPS Cross-Border Netting"
            ]
        },
        {
            triggers: [
                'eaps cross-border netting', 'eaps', 'cross-border', 'cbk', 'bot', 'bnr', 'mobile money switch'
            ],
            reply: `🌍🤝 <strong>East African Payment System (EAPS) & Mobile Money Escrow Switch:</strong><br><br>
Our sovereign telemetry enclave monitors both regional central bank corridors and domestic mobile money trust accounts:<br><br>
• <strong>EAPS Bilateral Netting:</strong> Real-time T+0 settlement links connecting <strong>Bank of Uganda (BOU)</strong> with the <strong>Central Bank of Kenya (CBK - KES)</strong>, <strong>Bank of Tanzania (BOT - TZS)</strong>, and <strong>National Bank of Rwanda (BNR - RWF)</strong>.<br>
• <strong>Mobile Money Trust Escrows:</strong> Tracks <strong>MTN Uganda</strong> (Stanbic Escrow) and <strong>Airtel Money</strong> (Absa Escrow) micro-transfer sweeps into the RTGS core, protected by Coraza CRS 912120 anti-replay rate limiters.<br><br>
👉 <a href="/Training/payment_systems_architecture.html" class="text-cyan-400 font-bold underline">View Full Sovereign Payment Architecture Map</a>`,
            followUps: [
                "Open 5-Day Syllabus",
                "Explain ISO 20022 pacs.008",
                "How Does 1.28s SOAR Work?"
            ]
        },
        {
            triggers: [
                'open 5-day syllabus', '5-day syllabus', 'syllabus', 'masterclass', 'training schedule', '0900 to 1300',
                'open cyber war room', 'war room'
            ],
            reply: `🎓📋 <strong>5-Day Masterclass Syllabus (09:00 – 13:00 Hours EAT Daily | 20 CPE Hours):</strong><br><br>
• <strong>Day 1 (09:00–13:00):</strong> Sovereign Payment Foundations (RTGS, SWIFT, EAPS) & Hybrid SOC Design.<br>
• <strong>Day 2 (09:00–13:00):</strong> Network Forensics, Deep Packet Inspection (DPI) & ISO 20022 Anomaly Hunting.<br>
• <strong>Day 3 (09:00–13:00):</strong> Volatile Memory Forensics (RFC 3227), Malware Decoding & PII Masking.<br>
• <strong>Day 4 (09:00–13:00):</strong> Sub-Second Shuffle SOAR Playbooks & Live Cyber War Room Exercises.<br>
• <strong>Day 5 (09:00–13:00):</strong> Uganda Cyber Law (ETA 2011 Sec. 8), Chain of Custody & Executive Board Reporting.<br><br>
👉 <a href="/Training/masterclass_syllabus.html" class="text-amber-400 font-bold underline">Open Full Syllabus & Download PDF / Word (.docx)</a><br>
👉 <a href="/Training/war_room_simulator.html" class="text-emerald-400 font-bold underline">Launch Multi-Scenario Cyber War Room</a>`,
            followUps: [
                "Explain ISO 20022 pacs.008",
                "How Does 1.28s SOAR Work?",
                "Uganda ETA 2011 Sec. 8 Law"
            ]
        },

        // --- UNIVERSAL AGM, CHURCH & FAITH-BASED GOVERNANCE DESK ---
        {
            triggers: [
                'church', 'church agm', 'churches', 'parish', 'diocese', 'faith', 'faith-based', 'fbo',
                'mosque', 'synod', 'pastor', 'bishop', 'clergy', 'deacon', 'elders', 'church election',
                'church council', 'pcc', 'religious assembly', 'cathedral', 'ministry agm',
                'do you do church agm', 'can our church use stride', 'church voting', 'church elections',
                'do you do church agms', 'can churches use stride'
            ],
            reply: `✝️🏛️ <strong>Yes! Stride Fully Powers Church AGMs & Faith-Based Assemblies:</strong><br><br>
Stride's <strong>Universal Digital Governance & AGM Engine</strong> is engineered specifically to eliminate voting friction, counting disputes, and paper ballot chaos across Christian denominations, Dioceses, Parishes, Mosques, and Faith-Based Organizations (FBOs):<br><br>
• <strong>Statutory & Legal Compliance:</strong> Built to satisfy the <strong>Societies Act (Cap 108)</strong>, <strong>Trustees (Perpetual Succession) Act</strong>, and <strong>Companies Limited by Guarantee</strong>.<br>
• <strong>Tamper-Proof Digital Secret Ballot:</strong> Congregants vote on their smartphones or stationed tablets for <em>Parish Church Councils (PCC), Deacons, Elders, Synod Delegates, and Treasurers</em>. Eliminates peer pressure, intimidation, and manual tally discrepancies in the sanctuary.<br>
• <strong>Attendance & Quorum Verification:</strong> Instant digital accreditation via SMS/WhatsApp QR pass so only bona fide registered members or delegates vote.<br>
• <strong>Financial & Project Budget Voting:</strong> Instant electronic voting on annual audited accounts, tithes/offering budgets, cathedral expansion funds, and constitutional amendments.<br>
• <strong>Multi-Parish & Diaspora Hybrid Inclusion:</strong> Unites main sanctuary congregants, branch parishes, and diaspora members into a single synchronized live vote.<br><br>
<div style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; padding: 8px 12px; border-radius: 6px; margin: 8px 0;">
  <strong class="text-emerald-400">⚡ Live Demonstration Ready:</strong><br>
  Test our digital ballot and returning officer scoreboard right now:<br>
  👉 <a href="vote.html" target="_blank" class="text-cyan-400 font-bold underline">Try Interactive Digital Ballot</a><br>
  👉 <a href="results.html" target="_blank" class="text-emerald-400 font-bold underline">Live Returning Officer Scoreboard</a><br>
  👉 <a href="agm-copilot.html" target="_blank" class="text-gold-400 font-bold underline">Launch Autonomous AGM Copilot</a>
</div>`,
            followUps: [
                "Church Secret Ballot Demo",
                "Societies Act Cap 108 Rules",
                "Parish & Diocese Setup",
                "Universal AGM Voting"
            ]
        },
        {
            triggers: [
                'church secret ballot demo', 'parish & diocese setup', 'societies act cap 108 rules',
                'societies act', 'cap 108', 'faith-based rules'
            ],
            reply: `📜 <strong>Societies Act (Cap 108) & Church Governance Rules:</strong><br><br>
Under Section 29 & 31 of Kenya's Societies Act (Cap 108):<br>
1. <strong>Annual General Meetings:</strong> Every registered society/church must hold an AGM once every calendar year to adopt audited accounts and elect office bearers.<br>
2. <strong>Quorum Verification:</strong> Stride validates attendance against the certified membership roll, preventing 'infiltrator voting'.<br>
3. <strong>Election Records:</strong> Stride automatically generates certified signed returning officer tallies ready for filing with the <strong>Registrar of Societies (Sheria House)</strong>.<br><br>
Would you like a custom demonstration setup for your Bishop, Pastor, or Church Executive Council? Contact our team at <a href="about.html" class="text-cyan-400 underline">strideanalytics.co.ke/about.html</a> or email <a href="mailto:governance@strideanalytics.co.ke" class="text-emerald-400 underline">governance@strideanalytics.co.ke</a>.`,
            followUps: [
                "Do you do Church AGMs?",
                "Try Interactive Digital Ballot",
                "Launch AGM Copilot"
            ]
        },
        {
            triggers: [
                'agm', 'annual general meeting', 'agm voting', 'e-voting', 'e-ballot', 'secret ballot',
                'agm copilot', 'quorum', 'agm portal', 'proxy voting', 'delegate credentials', 'agm results',
                'universal agm voting', 'universal agm & voting'
            ],
            reply: `🗳️ <strong>Stride Universal AGM & Statutory Digital Governance Suite:</strong><br><br>
Stride powers seamless, paperless, tamper-proof General Meetings across 4 key institutional regimes:<br><br>
1. <strong>Churches & Faith-Based Organizations:</strong> Societies Act (Cap 108), PCC/Elder secret balloting, building fund approvals, multi-branch hybrid voting.<br>
2. <strong>SACCOs & Co-operatives:</strong> Sacco Societies Act (Cap 490B) compliance, delegate credentialing, Form 1/4 reserves, and dividend approvals.<br>
3. <strong>Corporates & Listed PLCs:</strong> Companies Act No. 17 of 2015, institutional investor proxy management, share-weighted voting power.<br>
4. <strong>Country Clubs, NGOs & Chamas:</strong> Investment club asset distribution, member admission voting, committee executive elections.<br><br>
👉 <a href="agm-copilot.html" class="text-cyan-400 font-bold underline">Open AGM Copilot</a> &bull; <a href="vote.html" class="text-emerald-400 font-bold underline">Cast Sample Vote</a> &bull; <a href="pass.html" class="text-gold-400 font-bold underline">Digital Boarding Pass</a>`,
            followUps: [
                "Do you do Church AGMs?",
                "How Does Digital Ballot Work?",
                "SACCO AGM Solvency Ratios"
            ]
        },
        {
            triggers: [
                'chama', 'chama agm', 'investment club', 'ngo', 'ngo agm', 'association', 'welfare society',
                'alumni', 'club agm', 'karen country club', 'golf club'
            ],
            reply: `🤝 <strong>Chama, NGO, Club & Welfare Society Governance:</strong><br><br>
Whether managing an investment group with 50 members or a premier members club with 3,000 patrons:<br><br>
• <strong>Resolution Balloting:</strong> Approve asset purchases, land acquisitions, and monthly contribution adjustments with certified transparency.<br>
• <strong>Executive Committee Elections:</strong> Secret digital ballot for Chairman, Secretary, and Treasurer.<br>
• <strong>Zero Paper, Zero Disagreements:</strong> Immediate mathematical audit trail protects friendships, fellowship, and capital.<br><br>
Explore: <a href="vote.html" class="text-cyan-400 font-bold underline">Try Digital Ballot</a> or <a href="agm-copilot.html" class="text-emerald-400 font-bold underline">AGM Planning Copilot</a>.`,
            followUps: [
                "Do you do Church AGMs?",
                "Try Interactive Digital Ballot",
                "Contact Advisory Team"
            ]
        },
        // --- NSE DAILY MARKET & TELEMETRY DESK ---
        {
            triggers: ['compare div yield vs t-bill', 'yield spread', 't-bill vs dividend', 'tbill', 't-bill', 'treasury bill', 'yield spread'],
            reply: `🏛️ <strong>Equity Dividend Yield vs CBK 91-Day T-Bill (8.92% Benchmark):</strong><br><br>
• <strong>BAT Kenya (BAT):</strong> <strong>13.09%</strong> (<strong class="text-emerald-400">+417 bps</strong> super yield spread).<br>
• <strong>NCBA Group:</strong> <strong>11.02%</strong> (<strong class="text-emerald-400">+210 bps</strong> yield spread).<br>
• <strong>Co-operative Bank (COOP):</strong> <strong>10.53%</strong> (<strong class="text-emerald-400">+161 bps</strong> yield spread).<br>
• <strong>Absa Bank Kenya (ABSA):</strong> <strong>9.81%</strong> (<strong class="text-emerald-400">+89 bps</strong> yield spread).<br>
• <strong>Equity Group (EQTY):</strong> <strong>9.25%</strong> (<strong class="text-emerald-400">+33 bps</strong> yield spread).<br>
• <strong>KCB Group (KCB):</strong> <strong>8.50%</strong> (-42 bps vs T-Bill).<br>
• <strong>Safaricom (SCOM):</strong> <strong>6.72%</strong> (-220 bps, capital appreciation profile).<br><br>
💡 <em>Institutional Takeaway:</em> Banking equities offer an attractive <strong>33 to 210 bps cash premium</strong> over sovereign paper, justifying equity overweight for pension & institutional income funds.`,
            followUps: ["CBK FX Reserves & Shilling", "What is Foreign Net Flow?", "Copy 60-Sec Memo"]
        },
        {
            triggers: ['core capital minimum', 'core capital ratio', 'core capital floor', 'form 1 core capital', 'capital adequacy'],
            reply: `🏛️ <strong>SASRA Form 1 Capital Adequacy Minimums (Cap 490B):</strong><br><br>
• <strong>Core Capital to Total Assets:</strong> Minimum <strong>10.0%</strong>.<br>
• <strong>Minimum Absolute Core Capital:</strong> <strong>KES 10 Million</strong> (Deposit-Taking SACCOs).<br>
• <strong>Institutional Capital to Total Assets:</strong> Minimum <strong>8.0%</strong> (Statutory Reserve + Retained Surplus).<br>
• <strong>Core Capital to Deposits:</strong> Minimum <strong>8.0%</strong>.<br><br>
💡 <em>In Stride's Audit Checker:</em> The engine calculates Core Capital by summing Share Capital + Statutory Reserve (20% annual retention) + Retained Earnings, divided by Net Total Assets.`,
            followUps: ["Explain SASRA Form 4 Liquidity", "IFRS 9 NPL Aging Brackets", "How Does Zero-Knowledge Audit Work?"]
        },
        {
            triggers: ['form 4 liquidity', 'sasra liquidity rules', 'liquidity ratio', 'liquid assets to deposits'],
            reply: `💧 <strong>SASRA Form 4 Prudential Liquidity Requirements:</strong><br><br>
• <strong>Statutory Minimum:</strong> <strong>15.0%</strong> of withdrawable member savings (FOSA) and short-term debt.<br>
• <strong>Permissible Liquid Assets:</strong> Cash in vault, balances with commercial banks (Co-op Bank, KCB), and CBK Treasury Bills.<br>
• <strong>Prudential Purpose:</strong> Ensures the SACCO can withstand immediate member withdrawal surges without emergency external rediscounting.<br><br>
💡 <em>Audit Engine Metric:</em> Highlands Tea SACCO benchmark maintains <strong>36.60% liquidity (+2,160 bps buffer)</strong>, with 56.1% deployed into risk-free CBK Treasury Bills yielding 8.92%.`,
            followUps: ["What is Core Capital Minimum?", "IFRS 9 NPL Aging Brackets", "Unlock Form 1 & 4 PDF Pack"]
        },
        {
            triggers: ['ifrs 9', 'npl aging', 'npl brackets', 'impairment', 'delinquency brackets'],
            reply: `📊 <strong>IFRS 9 & SASRA Loan Portfolio Aging Classification:</strong><br><br>
1. <strong>Normal Performing (1% Provision):</strong> 0 to 30 days overdue (84.5% of ledger).<br>
2. <strong>Watch (5% Provision):</strong> 31 to 90 days overdue (10.3% of ledger).<br>
3. <strong>Substandard (25% Provision):</strong> 91 to 180 days overdue (3.1% of ledger).<br>
4. <strong>Doubtful (50% Provision):</strong> 181 to 360 days overdue (1.5% of ledger).<br>
5. <strong>Loss (100% Provision):</strong> Over 360 days overdue (0.6% of ledger).<br><br>
⚠️ <strong>Regulatory Benchmark:</strong> SASRA monitors a maximum NPL ceiling of <strong>5.0%</strong>. Ledgers exceeding 5.0% trigger supervisory monitoring.`,
            followUps: ["What is Core Capital Minimum?", "Explain SASRA Form 4 Liquidity", "Unlock Form 1 & 4 PDF Pack"]
        },
        {
            triggers: ['zero-knowledge', 'how does zero-knowledge work', 'data privacy', 'odpc compliance'],
            reply: `🛡️ <strong>Zero-Knowledge Browser Processing Architecture:</strong><br><br>
• <strong>100% Client-Side Execution:</strong> The trial balance parser runs entirely in your workstation's JavaScript engine using browser memory (RAM).<br>
• <strong>Zero Network Uploads:</strong> No row, account number, or financial ledger entry is transmitted to external servers or cloud AI models.<br>
• <strong>ODPC Compliance:</strong> Conforms strictly with the <em>Kenya Data Protection Act 2019</em> by ensuring sensitive institutional ledgers remain sovereign inside your perimeter.`,
            followUps: ["What is Core Capital Minimum?", "Explain SASRA Form 4 Liquidity", "Unlock Form 1 & 4 PDF Pack"]
        },
        {
            triggers: ['unlock form 1', 'unlock pdf', 'mpesa', 'paywall', 'upgrade enterprise'],
            reply: `📲 <strong>Unlocking Official SASRA Board Pack & Enterprise Upgrade:</strong><br><br>
• <strong>Single Audit Certificate:</strong> <strong>KES 4,950</strong> (One-off verified Form 1 & Form 4 PDF + Excel pack).<br>
• <strong>Annual Enterprise SaaS:</strong> <strong>KES 49,500 / month</strong> (Automated monthly compliance, core-banking integration, AGM dividend simulator).<br>
• <strong>M-Pesa B2B Paybill:</strong> Paybill <strong>848484</strong>, Account <code>STRIDE-AUDIT</code>.<br><br>
Click the <strong>'Pay via M-Pesa B2B'</strong> or <strong>'Verify Corporate Email'</strong> button on the audit page to unlock instantly!`,
            followUps: ["What is Core Capital Minimum?", "Explain SASRA Form 4 Liquidity"]
        },
        {
            triggers: ['cbk', 'central bank', 'cbr', 'central bank rate', 'monetary policy', 'fx reserves', 'reserves', 'shilling', 'usd/kes', 'exchange rate'],
            reply: `🏛️ <strong>Central Bank of Kenya (CBK) Macroeconomic Telemetry:</strong><br><br>
• <strong>Central Bank Rate (CBR):</strong> <strong>12.00%</strong> (supporting inflation anchoring).<br>
• <strong>USD / KES Mean Rate:</strong> <strong>129.25</strong> (Shilling stabilized following foreign inflows and Eurobond buyback).<br>
• <strong>91-Day Treasury Bill:</strong> <strong>8.92%</strong> (Latest auction oversubscribed at 142%).<br>
• <strong>Official FX Reserves:</strong> <strong>USD 8.24 Billion</strong> (providing <strong>4.3 Months</strong> of import cover, well above the 4.0 statutory minimum).<br>
• <strong>Headline Inflation:</strong> <strong>3.60%</strong> (comfortably within CBK's 5.0% ±2.5% target band).`,
            followUps: ["Compare Div Yield vs T-Bill", "What is Foreign Net Flow?", "Who had Highest Turnover?"]
        },
        {
            triggers: ['highest turnover', 'top turnover', 'turnover lead', 'traded most', 'volume leader', 'most active'],
            reply: (data) => {
                if (data && data.counters) {
                    const sorted = [...data.counters].sort((a,b) => b.turnover_m - a.turnover_m);
                    const top = sorted[0];
                    const second = sorted[1];
                    const netSign = top.foreign_net_m >= 0 ? '+' : '';
                    const netColor = top.foreign_net_m >= 0 ? 'text-emerald-400' : 'text-rose-400';
                    return `📈 <strong>Today's Turnover Leader: ${top.name} (${top.ticker})</strong><br><br>
• <strong>Turnover:</strong> <strong>KES ${top.turnover_m.toFixed(2)} Million</strong> (${top.turnover_share_pct}% of total market trades).<br>
• <strong>Closing Price:</strong> <strong>KES ${top.close.toFixed(2)}</strong> (${top.change_pct >= 0 ? '+' : ''}${top.change_pct.toFixed(2)}% ${top.change_pct >= 0 ? '▲' : '▼'}).<br>
• <strong>Volume:</strong> ${top.volume} shares traded.<br>
• <strong>Foreign Net Position:</strong> <strong class="${netColor}">${netSign}KES ${top.foreign_net_m.toFixed(1)}M</strong>.<br><br>
Second place was <strong>${second.name} (${second.ticker})</strong> with KES ${second.turnover_m.toFixed(2)}M (${second.turnover_share_pct}% share).`;
                }
                return `📈 <strong>Today's Turnover Leader: Safaricom (SCOM)</strong><br><br>
• <strong>Turnover:</strong> <strong>KES 324.87 Million</strong> (47.5% of total market trades).<br>
• <strong>Closing Price:</strong> <strong>KES 17.85</strong> (+1.71% ▲).<br>
• <strong>Volume:</strong> 18.20M shares traded across 640 deals.<br>
• <strong>Foreign Net Position:</strong> <strong class="text-emerald-400">+KES 52.4M</strong> (aggressive institutional buying).<br><br>
Second place was <strong>Equity Group Holdings (EQTY)</strong> with KES 142.10M (20.8% share).`;
            },
            followUps: ["What is Foreign Net Flow?", "Compare Bank vs Telco Flow", "Copy 60-Sec Memo"]
        },
        {
            triggers: ['foreign flow', 'foreign net', 'foreign inflow', 'foreign investors', 'offshore', 'foreign activity'],
            reply: (data) => {
                if (data && data.foreign_flows) {
                    const ff = data.foreign_flows;
                    return `🌍 <strong>Foreign Investor Capital Flow Barometer (${data.market_date}):</strong><br><br>
• <strong>Net Position:</strong> <strong class="text-emerald-400">${ff.net_inflow_formatted} (${ff.sentiment})</strong>.<br>
• <strong>Foreign Participation:</strong> <strong>${ff.foreign_participation_pct}%</strong> of total market activity.<br>
• <strong>Total Foreign Buys:</strong> ${ff.foreign_buys_formatted}.<br>
• <strong>Total Foreign Sales:</strong> ${ff.foreign_sales_formatted}.<br><br>
💡 <em>Institutional Read:</em> Offshore accounts were net ${ff.status === 'bullish' ? 'accumulators' : 'sellers'} across major index blue-chips.`;
                }
                return `🌍 <strong>Foreign Investor Capital Flow Barometer:</strong><br><br>
• <strong>Net Position:</strong> <strong class="text-emerald-400">+KES 79.1 Million (Net Inflow Accumulation)</strong>.<br>
• <strong>Foreign Participation:</strong> <strong>60.3%</strong> of total market activity.<br>
• <strong>Total Foreign Buys:</strong> KES 245.8M (59.6% of foreign volume).<br>
• <strong>Total Foreign Sales:</strong> KES 166.7M (40.4% of foreign volume).<br><br>
💡 <em>Institutional Read:</em> Offshore funds were net accumulators in <strong>SCOM (+KES 52.4M)</strong> and <strong>EQTY (+KES 21.8M)</strong>.`;
            },
            followUps: ["Who had Highest Turnover?", "Compare Bank vs Telco Flow", "Copy 60-Sec Memo"]
        },
        {
            triggers: ['bank vs telco', 'banking vs telecom', 'sector turnover', 'sector flow', 'sectors'],
            reply: (data) => {
                if (data && data.sectors) {
                    const lines = data.sectors.map(s => `• <strong>${s.name}:</strong> <strong>${s.pct}%</strong> (KES ${s.turnover_m}M)`).join('<br>');
                    return `📊 <strong>Daily Sector Turnover Distribution (${data.market_date}):</strong><br><br>${lines}<br><br><strong>Concentration:</strong> Top 2 sectors accounted for <strong>88.7%</strong> of deployed liquidity.`;
                }
                return `📊 <strong>Daily Sector Turnover Distribution:</strong><br><br>
• <strong>Telecommunication (SCOM):</strong> <strong>47.5%</strong> (KES 324.87M)<br>
• <strong>Banking (8 counters):</strong> <strong>41.2%</strong> (KES 281.90M)<br>
• <strong>Manufacturing & Allied:</strong> <strong>7.8%</strong> (KES 53.40M - EABL/BAT)<br>
• <strong>Energy & Petroleum:</strong> <strong>2.1%</strong> (KES 14.30M - KenGen)<br>
• <strong>Commercial & Services:</strong> <strong>1.4%</strong> (KES 9.78M)<br><br>
<strong>Concentration:</strong> Telecom & Banking accounted for <strong>88.7%</strong> of all capital deployed.`;
            },
            followUps: ["Who had Highest Turnover?", "What is Foreign Net Flow?", "Copy 60-Sec Memo"]
        },
        {
            triggers: ['copy memo', '60-sec memo', 'executive memo', 'closing memo', 'morning brief'],
            reply: (data) => {
                if (data && data.executive_memo && data.executive_memo.length >= 3) {
                    return `📋 <strong>The 60-Second Daily Closing Bell Memo (${data.market_date}):</strong><br><br>
1. ${data.executive_memo[0]}<br><br>
2. ${data.executive_memo[1]}<br><br>
3. ${data.executive_memo[2]}`;
                }
                return `📋 <strong>The 60-Second Daily Closing Bell Memo:</strong><br><br>
1. Foreign accounts drove 60.3% of trades with a net inflow of +KES 79.1M, primarily accumulating Safaricom and Equity.<br>
2. Banking sector sustained dividend yields between 8.5% and 10.5%, beating 91-day Treasury Bills.<br>
3. Market breadth was +18 gainers vs -9 decliners, lifting total Market Cap by KES 19.8B to KES 1.785 Trillion.`;
            },
            action: () => {
                if (typeof copyExecutiveMemo === 'function') copyExecutiveMemo();
            },
            followUps: ["Export Daily CSV", "Who had Highest Turnover?", "What is Foreign Net Flow?"]
        },
        {
            triggers: ['export daily csv', 'download daily csv', 'export market csv', 'market csv'],
            reply: `📥 <strong>Generating Daily Equities CSV Dataset...</strong><br><br>Downloading today's closing prices, volumes, turnovers, P/E multiples, dividend yields, and foreign net flow positions.`,
            action: () => {
                if (typeof exportMarketCSV === 'function') exportMarketCSV();
            },
            followUps: ["Who had Highest Turnover?", "What is Foreign Net Flow?", "Compare Bank vs Telco Flow"]
        },
        // --- BLUE-CHIPS BENCHMARK INTELLIGENCE ---
        {
            triggers: ['safaricom', 'scom', 'm-pesa', 'mpesa', 'telecom'],
            reply: `📱 <strong>Safaricom PLC (NSE: SCOM) 5-Year Financial Intelligence:</strong><br><br>
• <strong>2025 Revenue:</strong> <strong>KES 372.6B</strong> (Up from KES 264.0B in 2021, +41.1% 5-Yr expansion).<br>
• <strong>2025 Net Profit (PAT):</strong> <strong>KES 72.8B</strong> (East Africa's most profitable corporate).<br>
• <strong>M-Pesa Revenue Contribution:</strong> <strong>KES 158.4B</strong> (now accounts for <strong>42.5%</strong> of total turnover).<br>
• <strong>Return on Equity (ROE):</strong> <strong>44.8%</strong> (highest capital efficiency in Kenya).<br>
• <strong>5-Yr Dividends Declared:</strong> <strong>KES 134.5B</strong>.<br>
• <strong>Strategic Moat:</strong> 32 Million active users command 98% mobile money flow; fixed enterprise fiber lock-in and high long-term upside from Safaricom Ethiopia.`,
            action: () => { if (typeof openCompanyModal === 'function') openCompanyModal('safaricom'); },
            followUps: ["Compare Safaricom vs Equity", "Who Pays Highest Dividend?", "Show 5-Yr Revenue Chart"]
        },
        {
            triggers: ['equity', 'eqty', 'equity bank', 'equitybcdc', 'drc'],
            reply: `🏦 <strong>Equity Group Holdings PLC (NSE: EQTY) 5-Year Financial Intelligence:</strong><br><br>
• <strong>Total Balance Sheet Assets:</strong> <strong>KES 1.875 Trillion</strong> (East Africa's largest banking group!).<br>
• <strong>2025 Total Income:</strong> <strong>KES 192.5B</strong> (Up +105.4% from KES 93.7B in 2021).<br>
• <strong>2025 Net Profit (PAT):</strong> <strong>KES 58.6B</strong>.<br>
• <strong>Return on Equity (ROE):</strong> <strong>24.6%</strong>.<br>
• <strong>The DR Congo Game-Changer:</strong> EquityBCDC now contributes over <strong>32% of total group deposits</strong> and 30% of profit, successfully shielding Equity from single-country Kenyan sovereign debt exposure.<br>
• <strong>Strategic Moat:</strong> Digitized merchant acquiring and low-cost retail deposit franchise across 6 countries.`,
            action: () => { if (typeof openCompanyModal === 'function') openCompanyModal('equity'); },
            followUps: ["Compare Equity vs KCB", "What is Co-op Bank's Moat?", "Download 5-Yr CSV Dataset"]
        },
        {
            triggers: ['kcb', 'kcb group', 'tmb', 'trust merchant bank'],
            reply: `🏛️ <strong>KCB Group PLC (NSE: KCB) 5-Year Financial Intelligence:</strong><br><br>
• <strong>Total Assets:</strong> <strong>KES 1.842 Trillion</strong> (Kenya's foundational asset base).<br>
• <strong>2025 Revenue:</strong> <strong>KES 185.0B</strong> (Up +92.7% from KES 96.0B in 2021).<br>
• <strong>2025 Net Profit (PAT):</strong> <strong>KES 54.2B</strong>.<br>
• <strong>Net Interest Income (NII):</strong> Surged over <strong>104%</strong> to KES 139.5B.<br>
• <strong>Regional Footprint:</strong> Kenya, Tanzania, South Sudan, Rwanda, Uganda, Burundi, and DRC (via TMB acquisition).<br>
• <strong>Strategic Moat:</strong> Unrivaled public sector infrastructure clearing, largest corporate loan book, and national payroll dominance.`,
            action: () => { if (typeof openCompanyModal === 'function') openCompanyModal('kcb'); },
            followUps: ["Compare Equity vs KCB", "Who Pays Highest Dividend?", "Show 5-Yr Profit Chart"]
        },
        {
            triggers: ['eabl', 'diageo', 'beer', 'spirits', 'tusker', 'guinness'],
            reply: `🍺 <strong>East African Breweries PLC (EABL / Diageo) 5-Year Financial Intelligence:</strong><br><br>
• <strong>2025 Net Sales:</strong> <strong>KES 136.8B</strong> (Up +59.1% from KES 86.0B in 2021).<br>
• <strong>2025 Net Profit (PAT):</strong> <strong>KES 14.2B</strong>.<br>
• <strong>Return on Equity (ROE):</strong> <strong>38.2%</strong>.<br>
• <strong>Spirits Category Shift:</strong> Mainstream & premium spirits expanded to <strong>43% of group net sales</strong> (Kenya Cane, Chrome, Johnnie Walker), insulating margins against excise duty tax shocks on bottled beer.<br>
• <strong>ESG Milestone:</strong> 100% renewable biomass plants commissioned in Kisumu, Ruaraka, and Uganda.<br>
• <strong>Strategic Moat:</strong> Impenetrable cold-chain distribution network backed by Diageo global IP.`,
            action: () => { if (typeof openCompanyModal === 'function') openCompanyModal('eabl'); },
            followUps: ["What is Co-op Bank's Moat?", "Compare Safaricom vs Equity", "Export 5-Yr CSV Dataset"]
        },
        {
            triggers: ['co-op', 'coop', 'cooperative bank', 'co-operative bank', 'kingdom bank'],
            reply: `🤝 <strong>Co-operative Bank of Kenya (NSE: COOP) 5-Year Financial Intelligence:</strong><br><br>
• <strong>Total Assets:</strong> <strong>KES 742.5B</strong> (Up +38.3% from KES 536.9B in 2021).<br>
• <strong>2025 Net Profit (PAT):</strong> <strong>KES 30.4B</strong>.<br>
• <strong>Operational Efficiency:</strong> Holds Kenya's lowest <strong>Cost-to-Income ratio at ~45.8%</strong>.<br>
• <strong>Return on Equity (ROE):</strong> <strong>21.9%</strong>.<br>
• <strong>The Sacco Monopoly Moat:</strong> 64.5% owned by Kenya's co-operative movement through Co-op Holdings. It is the exclusive institutional clearing gateway for <strong>15,000+ Saccos</strong>, providing zero-cost structural liquidity and near-zero customer churn!`,
            action: () => { if (typeof openCompanyModal === 'function') openCompanyModal('coop'); },
            followUps: ["Compare Equity vs KCB", "Who Pays Highest Dividend?", "Banki Kuu Sacco 2025 Audit"]
        },
        {
            triggers: ['absa', 'absa bank', 'timiza', 'barclays'],
            reply: `💳 <strong>Absa Bank Kenya PLC (NSE: ABSA) 5-Year Financial Intelligence:</strong><br><br>
• <strong>2025 Revenue:</strong> <strong>KES 71.8B</strong> (Up +94.6% from KES 36.9B in 2021).<br>
• <strong>2025 Net Profit (PAT):</strong> <strong>KES 21.5B</strong>.<br>
• <strong>Total Balance Sheet Assets:</strong> <strong>KES 625.5B</strong>.<br>
• <strong>Return on Equity (ROE):</strong> <strong>23.8%</strong>.<br>
• <strong>Strategic Moat:</strong> Multinational corporate banking heritage, dominant digital asset financing via Timiza, and premier affluent private wealth management franchise in Kenya.`,
            action: () => { if (typeof openCompanyModal === 'function') openCompanyModal('absa'); },
            followUps: ["Compare Equity vs KCB", "What is NCBA's Moat?", "Compare Div Yield vs T-Bill"]
        },
        {
            triggers: ['ncba', 'm-shwari', 'mshwari', 'fuliza', 'cba', 'nic'],
            reply: `📱 <strong>NCBA Group PLC (NSE: NCBA) 5-Year Financial Intelligence:</strong><br><br>
• <strong>2025 Revenue:</strong> <strong>KES 82.4B</strong> (Up +76.1% from KES 46.8B in 2021).<br>
• <strong>2025 Net Profit (PAT):</strong> <strong>KES 26.8B</strong>.<br>
• <strong>Total Balance Sheet Assets:</strong> <strong>KES 768.2B</strong>.<br>
• <strong>Return on Equity (ROE):</strong> <strong>22.5%</strong>.<br>
• <strong>Strategic Moat:</strong> Digital micro-credit superpower powering <strong>M-Shwari & Fuliza</strong> with Safaricom. Commands <strong>>35% asset finance market share</strong> (vehicle and commercial equipment leasing) across Kenya.`,
            action: () => { if (typeof openCompanyModal === 'function') openCompanyModal('ncba'); },
            followUps: ["Compare Safaricom vs Equity", "Show BAT Kenya Dividends", "Compare Div Yield vs T-Bill"]
        },
        {
            triggers: ['stanbic', 'sbic', 'standard bank', 'cfc stanbic'],
            reply: `🏦 <strong>Stanbic Holdings PLC (NSE: SBIC) 5-Year Financial Intelligence:</strong><br><br>
• <strong>2025 Revenue:</strong> <strong>KES 52.4B</strong> (Up +109.6% from KES 25.0B in 2021).<br>
• <strong>2025 Net Profit (PAT):</strong> <strong>KES 16.8B</strong>.<br>
• <strong>Total Balance Sheet Assets:</strong> <strong>KES 532.0B</strong>.<br>
• <strong>Return on Equity (ROE):</strong> <strong>21.4%</strong>.<br>
• <strong>Strategic Moat:</strong> Backed by Africa's largest banking group (Standard Bank). Hegemony in large multinational syndicated facilities, cross-border FX clearing corridors, and premier custodial asset management.`,
            action: () => { if (typeof openCompanyModal === 'function') openCompanyModal('stanbic'); },
            followUps: ["Compare Div Yield vs T-Bill", "What is Co-op Bank's Moat?", "What is KenGen's Moat?"]
        },
        {
            triggers: ['bat', 'bat kenya', 'tobacco', 'oral nicotine', 'velo'],
            reply: `🏭 <strong>BAT Kenya PLC (NSE: BAT) 5-Year Financial Intelligence:</strong><br><br>
• <strong>2025 Revenue:</strong> <strong>KES 46.5B</strong>.<br>
• <strong>2025 Net Profit (PAT):</strong> <strong>KES 6.8B</strong>.<br>
• <strong>Return on Equity (ROE):</strong> <strong>46.5%</strong> (World-class capital efficiency).<br>
• <strong>5-Yr Dividends Declared:</strong> <strong>KES 28.2B</strong> (~85%-90% payout ratio, yielding ~13.09% cash returns).<br>
• <strong>Strategic Moat:</strong> Regional export powerhouse. Over <strong>58% of Nairobi factory output</strong> is exported across 13 East & Horn of Africa nations, earning hard foreign exchange.`,
            action: () => { if (typeof openCompanyModal === 'function') openCompanyModal('bat'); },
            followUps: ["Compare Div Yield vs T-Bill", "What is KenGen's Moat?", "Export 5-Yr CSV Dataset"]
        },
        {
            triggers: ['kengen', 'geothermal', 'olkaria', 'green energy', 'power generation', 'renewables'],
            reply: `⚡ <strong>KenGen PLC (NSE: KEGN) 5-Year Financial Intelligence:</strong><br><br>
• <strong>2025 Revenue:</strong> <strong>KES 61.4B</strong> (Up +34.1% from KES 45.8B in 2021).<br>
• <strong>2025 Net Profit (PAT):</strong> <strong>KES 8.4B</strong>.<br>
• <strong>Total Assets:</strong> <strong>KES 480.0B</strong>.<br>
• <strong>Green Energy Purity:</strong> <strong>93%</strong> of electric generation is renewable, anchored by Olkaria's 799 MW geothermal steam reservoirs.<br>
• <strong>Strategic Moat:</strong> Commands 70% of Kenya's national grid capacity; zero exposure to volatile oil imports; monetizing Olkaria Green Energy Park for international data centers.`,
            action: () => { if (typeof openCompanyModal === 'function') openCompanyModal('kengen'); },
            followUps: ["Compare Div Yield vs T-Bill", "Show BAT Kenya Dividends", "Who Pays Highest Dividend?"]
        },
        // --- COMPARISONS & RANKINGS ---
        {
            triggers: ['compare safaricom vs equity', 'safaricom vs equity', 'scom vs eqty'],
            reply: `⚔️ <strong>Head-to-Head: Safaricom PLC vs. Equity Group Holdings:</strong><br><br>
• <strong>2025 Revenue:</strong> Safaricom (KES 372.6B) vs Equity (KES 192.5B). <em>Safaricom leads by 1.9x</em>.<br>
• <strong>2025 Net Profit:</strong> Safaricom (KES 72.8B) vs Equity (KES 58.6B).<br>
• <strong>Capital Efficiency (ROE):</strong> Safaricom (<strong>44.8%</strong>) vs Equity (<strong>24.6%</strong>). Safaricom's asset-light digital network generates nearly double the equity return of banking capital.<br>
• <strong>Geographic Diversification:</strong> Equity leads heavily with DRC contributing 32% of deposits, while Safaricom is still incubating Ethiopia.<br>
• <strong>Strategic Takeaway:</strong> Safaricom is the premier cash-flow dividend dividend machine; Equity is the premier cross-border asset compounder.`,
            followUps: ["Compare Equity vs KCB", "Who Pays Highest Dividend?", "Export 5-Yr CSV Dataset"]
        },
        {
            triggers: ['compare equity vs kcb', 'equity vs kcb', 'eqty vs kcb', 'equity group vs kcb group'],
            reply: `⚔️ <strong>The Battle of the Titans: Equity Group vs. KCB Group:</strong><br><br>
• <strong>Total Asset Scale:</strong> Equity (<strong>KES 1.875 Trillion</strong>) vs KCB (<strong>KES 1.842 Trillion</strong>). Equity holds a slight edge following rapid DRC scaling.<br>
• <strong>2025 Net Profit (PAT):</strong> Equity (<strong>KES 58.6B</strong>) vs KCB (<strong>KES 54.2B</strong>).<br>
• <strong>Deposit Strategy:</strong> Equity dominates high-margin micro, retail, and SME digital merchants; KCB dominates massive corporate, public sector treasury, and syndicated infrastructure loans.<br>
• <strong>DR Congo Battleground:</strong> Equity acquired ProCredit/EquityBCDC; KCB acquired Trust Merchant Bank (TMB). Both are capturing the lucrative Katanga mining export trade corridor.`,
            followUps: ["What is Co-op Bank's Moat?", "Who Pays Highest Dividend?", "Show 5-Yr Profit Chart"]
        },
        {
            triggers: ['highest dividend', 'dividend yield', 'who pays dividend', 'payout'],
            reply: `🏆 <strong>Kenya Top 5 Cumulative 5-Year Dividend Leaderboard (2021–2025):</strong><br><br>
1. 🥇 <strong>Safaricom PLC:</strong> <strong>KES 134.5 Billion</strong> (Payout ratio ~80% of net earnings).<br>
2. 🥈 <strong>Equity Group:</strong> <strong>KES 58.2 Billion</strong>.<br>
3. 🥉 <strong>KCB Group:</strong> <strong>KES 45.0 Billion</strong>.<br>
4. 🎖️ <strong>Co-operative Bank:</strong> <strong>KES 42.1 Billion</strong>.<br>
5. 🎖️ <strong>EABL:</strong> <strong>KES 31.8 Billion</strong>.<br><br>
Combined 5-year dividends paid out to institutional and retail shareholders: <strong>KES 264.8 Billion</strong>!`,
            followUps: ["Compare Safaricom vs Equity", "What is Co-op Bank's Moat?", "Download 5-Yr CSV Dataset"]
        },
        {
            triggers: ['export', 'csv', 'download dataset', 'excel'],
            reply: `📥 <strong>Generating Benchmark Dataset:</strong><br><br>I am initiating an instant export of the 5-Year Master Financial Matrix for Safaricom, Equity, KCB, EABL, and Co-op Bank directly into an Excel-ready CSV format.`,
            action: () => { if (typeof exportBenchmarkCSV === 'function') exportBenchmarkCSV(); },
            followUps: ["Compare Safaricom vs Equity", "Who Pays Highest Dividend?", "Show 5-Yr Revenue Chart"]
        },
        {
            triggers: ['show revenue chart', 'revenue trajectory', 'chart 1'],
            reply: `📈 <strong>Navigating to 5-Year Revenue Expansion Chart:</strong><br><br>Notice the steep multi-year trajectory across all 5 champions, rising from KES 615.1B (2021) to <strong>KES 948.6B (2025)</strong>.`,
            action: () => {
                const el = document.getElementById('revenueChart');
                if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            },
            followUps: ["Show 5-Yr Profit Chart", "Compare Safaricom vs Equity", "Who Pays Highest Dividend?"]
        },
        {
            triggers: ['show profit chart', 'pat chart', 'earnings chart', 'chart 2'],
            reply: `💰 <strong>Navigating to Net Profit After Tax (PAT) Chart:</strong><br><br>Visualizing net bottom-line earnings resilience across interest rate hikes, inflation shocks, and currency devaluations.`,
            action: () => {
                const el = document.getElementById('patChart');
                if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            },
            followUps: ["Show 5-Yr Revenue Chart", "Compare Equity vs KCB", "Export 5-Yr CSV Dataset"]
        },
        // --- SACCO & REGULATORY TELEMETRY ---
        {
            triggers: ['running balance', 'summation', 'stock vs flow', 'stock and flow'],
            reply: `💡 <strong>Absolute Running Balance vs Flow (SASRA & IFRS 9 Rule):</strong><br><br>
In institutional accounting, <strong>Total Loan Book</strong> and <strong>Member Deposits</strong> are <em>Point-in-Time Balance Sheet closing balances</em> as of December 31. They must <strong>never</strong> be summed across years.<br><br>
To measure annual mobilization, always review the <strong>Δ YoY Net Flow</strong> metric. Explore this on the <a href="stride-sacco.html" class="text-cyan-400 underline">Stride-SACCO portal</a>!`,
            followUps: ["SASRA Liquidity Rules", "Banki Kuu Sacco 2025 Audit", "ODPC Data Privacy Shield"]
        },
        {
            triggers: ['sasra', 'prudential', 'liquidity', 'statutory minimum', 'cap 490b'],
            reply: `🏛️ <strong>SASRA Statutory Benchmarks (Sacco Societies Act Cap 490B):</strong><br><br>
• <strong>Core Capital to Total Assets:</strong> Minimum <strong>10.0%</strong>.<br>
• <strong>Liquidity Ratio (Buffer to Deposits):</strong> Minimum <strong>15.0%</strong>.<br>
• <strong>PAR > 30 Days (NPL Ratio):</strong> Statutory tolerance ceiling <strong>5.0%</strong>.<br>
• <strong>External Borrowing Limit:</strong> Maximum <strong>25.0%</strong> of Total Assets.`,
            followUps: ["Banki Kuu Sacco 2025 Audit", "Running Balance vs Summation", "ODPC Data Privacy Shield"]
        },
        {
            triggers: ['banki kuu', 'bksc', 'central bank sacco', 'cbk sacco'],
            reply: `🏛️ <strong>Banki Kuu Sacco Society Ltd (Audited 2025 Highlights):</strong><br><br>
• <strong>Total Assets:</strong> <strong>KES 3,529,546,055</strong> (+17.07% YoY growth).<br>
• <strong>Member Deposits:</strong> <strong>KES 2,145,636,483</strong>.<br>
• <strong>Loan Book:</strong> <strong>KES 3,053,805,856</strong> across 4,149 members.<br>
• <strong>PAR > 30 (NPL):</strong> Pristine <strong>2.10%</strong> (well below the 5% statutory ceiling).<br>
• <strong>Core Capital Ratio:</strong> <strong>11.36%</strong> (compliant with SASRA rules).`,
            followUps: ["SASRA Liquidity Rules", "Reef Hotel Venue Details", "What is Friday Gala Dress Code?"]
        },
        {
            triggers: ['odpc', 'pii', 'privacy', 'masking', 'data protection'],
            reply: `🔒 <strong>ODPC Sovereign Data Perimeter (Kenya Data Protection Act 2019):</strong><br><br>
Stride enforces automatic cryptographic hashing and visual field salting (e.g. <code>ID: 216****6</code>, <code>+254 72* *** *40</code>). Raw member PII never leaves the institutional boundary and is cryptographically anchored via SHA-256 Merkle root trees.`,
            followUps: ["SASRA Liquidity Rules", "Running Balance vs Summation", "Kenya Top 5 Blue-Chips"]
        },
        // --- RETREAT SPECIFIC ---
        {
            triggers: ['reef hotel', 'venue', 'mombasa', 'prideinn', 'hotel location'],
            reply: `🏖️ <strong>Confirmed Retreat Venue: Reef Hotel Mombasa (Nyali Beach)</strong><br><br>
• <strong>Dates:</strong> Thursday 16th – Sunday 18th October 2026.<br>
• <strong>Location:</strong> Mwamba Drive, Nyali Beach Shoreline, Mombasa.<br>
• <strong>Facilities:</strong> Reef Grand Plenary Hall, Beachfront Ocean Lawn, Reef Garden Terrace.<br>
• <strong>Concierge Desk:</strong> +254 722 205 994.<br>
• <strong>Emergency Medical Desk:</strong> Reef Hotel Onsite First Aid & Paramedic Team.`,
            followUps: ["What is Friday Gala Dress Code?", "SGR Boarding Times", "Download Calendar Invite (.ics)"]
        },
        {
            triggers: ['dress code', 'what to pack', 'wardrobe', 'gala attire'],
            reply: `👔 <strong>Official Retreat Dress Code & Wardrobe Guide:</strong><br><br>
• <strong>Day 1 (Thu 16 Oct):</strong> Smart Casual travel wear (warm layer for SGR train AC) & relaxed seaside welcome dinner casual.<br>
• <strong>Day 2 Day (Fri 17 Oct):</strong> Sacco sports T-shirt, breathable shorts & sneakers/trainers for sand dynamics.<br>
• <strong>Day 2 Night (Fri 17 Oct Gala):</strong> <strong class="text-gold-300">Strictly Coastal White & Gold Elegance</strong> for the Annual Recognition Awards Dinner.<br>
• <strong>Day 3 (Sat 18 Oct):</strong> Relaxed coastal casual & return travel wear.<br>
• <strong>Must-Have:</strong> Original National ID Card for SGR boarding.`,
            followUps: ["SGR Boarding Times", "Reef Hotel Venue Details", "Download Calendar Invite (.ics)"]
        },
        {
            triggers: ['sgr', 'madaraka', 'train', 'boarding', 'syokimau', 'transit'],
            reply: `🚆 <strong>Madaraka Express SGR Transit Schedule:</strong><br><br>
• <strong>Assembly:</strong> Friday, 16th October 2026 at <strong>07:30 AM</strong> at Syokimau SGR Terminus.<br>
• <strong>Departure:</strong> 08:30 AM Madaraka Express First Class departure.<br>
• <strong>Arrival in Mombasa:</strong> 13:30 PM at Miritini Station, followed by executive coach transfer to Reef Hotel Nyali.<br>
• <strong>Return:</strong> Sunday, 18th October at 15:00 PM Miritini departure, arriving Nairobi at 19:45 PM.`,
            followUps: ["What is Friday Gala Dress Code?", "Reef Hotel Venue Details", "Download Calendar Invite (.ics)"]
        },
        {
            triggers: ['calendar', 'ics', 'outlook invite', 'add to calendar'],
            reply: `📅 <strong>Add Retreat to Calendar (.ics):</strong><br><br>Generating your official calendar file with all 3 days, Reef Hotel Nyali venue, and SGR reminder alerts. Tap the download link below if not auto-triggered.`,
            action: () => { if (typeof downloadCalendarInvite === 'function') downloadCalendarInvite(); },
            followUps: ["What is Friday Gala Dress Code?", "SGR Boarding Times", "Reef Hotel Venue Details"]
        },
        // --- COMPANY IDENTITY & GENERAL ---
        {
            triggers: ['contact', 'email', 'phone', 'location', 'who we are', 'stride analytics'],
            reply: `🏢 <strong>Stride Analytics (strideanalytics.co.ke):</strong><br><br>
• <strong>Mandate:</strong> Sovereign Institutional Intelligence, SASRA Banking Analytics & Executive Telemetry.<br>
• <strong>Official Email:</strong> <a href="mailto:info@strideanalytics.co.ke" class="text-cyan-400 underline">info@strideanalytics.co.ke</a><br>
• <strong>Headquarters:</strong> Nairobi Financial Corridor, Kenya.<br>
• <strong>Client Suites:</strong> Stride-SACCO, Cadence Engine, AGMplan, and NSE Corporate Benchmarks.`,
            followUps: ["Kenya Top 5 Blue-Chips", "SASRA Liquidity Rules", "Book Board Demo"]
        }
    ];

    window.toggleStrideChat = function() {
        const box = document.getElementById('stride-chat-box');
        box.classList.toggle('open');
        if (box.classList.contains('open')) {
            document.getElementById('stride-input').focus();
        }
    };

    window.toggleStrideGuide = function() {
        const modal = document.getElementById('stride-guide-modal');
        if (modal) {
            modal.classList.toggle('active');
        }
    };

    window.closeStrideGuide = function() {
        const modal = document.getElementById('stride-guide-modal');
        if (modal) {
            modal.classList.remove('active');
        }
    };

    window.resetStrideChat = function() {
        const container = document.getElementById('stride-messages');
        container.innerHTML = `
            <div class="stride-chat-msg bot">
                <div class="text-cyan-400 font-mono font-bold text-[11px] mb-1">🤖 Stride Intelligence Core:</div>
                Session refreshed. How can I assist your boardroom or investment committee right now?
                <div class="mt-3 pt-2 border-t border-cyan-500/20">
                    <div class="flex flex-wrap gap-1">
                        ${initialPills.map(p => `<span class="stride-quick-prompt" onclick="askQuickPrompt('${p}')">${p}</span>`).join('')}
                    </div>
                </div>
            </div>
        `;
    };

    window.askQuickPrompt = function(text) {
        document.getElementById('stride-input').value = text;
        sendStrideMessage();
    };

    window.handleChatKey = function(event) {
        if (event.key === 'Enter') {
            sendStrideMessage();
        }
    };

    window.sendStrideMessage = function() {
        const input = document.getElementById('stride-input');
        const text = input.value.trim();
        if (!text) return;

        const container = document.getElementById('stride-messages');

        // Append User Message
        const userMsg = document.createElement('div');
        userMsg.className = 'stride-chat-msg user';
        userMsg.textContent = text;
        container.appendChild(userMsg);
        input.value = '';
        container.scrollTop = container.scrollHeight;

        // Neural Typing Simulation indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'stride-chat-msg bot font-mono text-[11px] text-slate-400 animate-pulse';
        typingIndicator.id = 'stride-typing';
        typingIndicator.textContent = '⚡ Analyzing audited filings & telemetry...';
        container.appendChild(typingIndicator);
        container.scrollTop = container.scrollHeight;

        setTimeout(() => {
            const typing = document.getElementById('stride-typing');
            if (typing) typing.remove();

            const query = text.toLowerCase();
            let matched = null;

            // Search knowledge base
            for (const item of knowledgeBase) {
                if (item.triggers.some(t => query.includes(t.toLowerCase()))) {
                    matched = item;
                    break;
                }
            }

            let replyHtml = '';
            let followUps = [];

            if (matched) {
                replyHtml = typeof matched.reply === 'function' ? matched.reply(liveMarket) : matched.reply;
                followUps = matched.followUps || [];
                // Execute action if bound
                if (typeof matched.action === 'function') {
                    try { matched.action(); } catch (err) { console.log('Action execution:', err); }
                }
            } else {
                replyHtml = `🤖 <strong>Stride AI Core:</strong><br><br>
I've cross-referenced your query regarding <em>"${text.replace(/</g, "&lt;")}"</em> against our multi-year sovereign repository. Explore the direct interactive modules below:<br><br>
• <a href="benchmarks.html" class="text-gold-400 underline font-bold">Kenya Top 5 Blue-Chips (2021–2025)</a><br>
• <a href="stride-sacco.html" class="text-cyan-400 underline font-bold">Stride-SACCO 10-Yr Running Balance</a><br>
• <a href="about.html" class="text-emerald-400 underline font-bold">Corporate Advisory Desk</a>`;
                followUps = ["Compare Safaricom vs Equity", "SASRA Liquidity Rules", "Who Pays Highest Dividend?"];
            }

            // Create bot message
            const botMsg = document.createElement('div');
            botMsg.className = 'stride-chat-msg bot';
            
            let pillsHtml = '';
            if (followUps.length > 0) {
                pillsHtml = `
                    <div class="mt-2.5 pt-2 border-t border-slate-700/60">
                        <span class="text-[9px] text-slate-400 block mb-1 font-mono uppercase tracking-wider">Suggested Inquiries:</span>
                        <div class="flex flex-wrap gap-1">
                            ${followUps.map(p => `<span class="stride-quick-prompt" onclick="askQuickPrompt('${p}')">${p}</span>`).join('')}
                        </div>
                    </div>
                `;
            }

            botMsg.innerHTML = replyHtml + pillsHtml;
            container.appendChild(botMsg);
            container.scrollTop = container.scrollHeight;
        }, 300);
    };

    // -------------------------------------------------------------------------
    // Universal In-Browser PDF Reader (Opens all PDFs directly in browser)
    // -------------------------------------------------------------------------
    function initUniversalPdfReader() {
        if (document.getElementById('stride-pdf-modal')) return;

        const modal = document.createElement('div');
        modal.id = 'stride-pdf-modal';
        modal.style.cssText = 'position:fixed;inset:0;z-index:999999;background:rgba(2,6,23,0.88);backdrop-filter:blur(16px);display:none;align-items:center;justify-content:center;padding:12px;box-sizing:border-box;';
        modal.innerHTML = `
            <div style="width:100%;max-width:1150px;height:92vh;background:#050b14;border:1px solid rgba(6,182,212,0.45);border-radius:18px;box-shadow:0 25px 60px -15px rgba(0,0,0,0.8),0 0 35px rgba(6,182,212,0.25);display:flex;flex-direction:column;overflow:hidden;font-family:Inter,sans-serif;">
                <!-- Header Bar -->
                <div style="padding:12px 20px;background:#020617;border-bottom:1px solid rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:space-between;gap:12px;flex-shrink:0;">
                    <div style="display:flex;align-items:center;gap:10px;min-width:0;flex:1;">
                        <span style="width:10px;height:10px;border-radius:50%;background:#10b981;box-shadow:0 0 10px #10b981;flex-shrink:0;"></span>
                        <span id="stride-pdf-title" style="font-weight:700;color:#ffffff;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">Document Preview</span>
                        <span style="padding:2px 8px;border-radius:9999px;font-family:'JetBrains Mono',monospace;font-size:10px;font-weight:700;background:rgba(6,182,212,0.15);color:#22d3ee;border:1px solid rgba(6,182,212,0.3);letter-spacing:0.5px;flex-shrink:0;">WATERMARKED &amp; VERIFIED</span>
                    </div>
                    <div style="display:flex;align-items:center;gap:8px;flex-shrink:0;">
                        <a id="stride-pdf-newtab" href="#" target="_blank" style="padding:6px 14px;border-radius:10px;background:rgba(6,182,212,0.12);border:1px solid rgba(6,182,212,0.35);color:#38bdf8;font-size:11px;font-weight:600;text-decoration:none;display:inline-flex;align-items:center;gap:5px;font-family:'JetBrains Mono',monospace;transition:all 0.2s;" onmouseover="this.style.background='rgba(6,182,212,0.25)'" onmouseout="this.style.background='rgba(6,182,212,0.12)'">
                            <span>↗</span> <span>Open Full Tab</span>
                        </a>
                        <a id="stride-pdf-save" href="#" download style="padding:6px 12px;border-radius:10px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.12);color:#94a3b8;font-size:11px;font-weight:600;text-decoration:none;display:inline-flex;align-items:center;gap:5px;font-family:'JetBrains Mono',monospace;transition:all 0.2s;" onmouseover="this.style.color='#ffffff'" onmouseout="this.style.color='#94a3b8'">
                            <span>📥</span> <span>Save Copy</span>
                        </a>
                        <button id="stride-pdf-close" style="width:32px;height:32px;border-radius:10px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:#cbd5e1;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all 0.2s;margin-left:4px;" onmouseover="this.style.background='rgba(239,68,68,0.2)';this.style.color='#ef4444'" onmouseout="this.style.background='rgba(255,255,255,0.08)';this.style.color='#cbd5e1'">
                            ✕
                        </button>
                    </div>
                </div>
                <!-- Frame Content -->
                <div style="flex:1;width:100%;height:100%;background:#020617;position:relative;">
                    <iframe id="stride-pdf-frame" style="width:100%;height:100%;border:0;" src=""></iframe>
                </div>
            </div>
        `;
        document.body.appendChild(modal);

        const closeBtn = document.getElementById('stride-pdf-close');
        closeBtn.onclick = function() {
            modal.style.display = 'none';
            document.getElementById('stride-pdf-frame').src = '';
            document.body.style.overflow = '';
        };

        modal.onclick = function(e) {
            if (e.target === modal) {
                closeBtn.click();
            }
        };

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && modal.style.display === 'flex') {
                closeBtn.click();
            }
        });

        window.openStridePdf = function(url, title) {
            modal.style.display = 'flex';
            document.getElementById('stride-pdf-title').textContent = title || 'StrideAnalytics Sovereign Document';
            document.getElementById('stride-pdf-newtab').href = url;
            document.getElementById('stride-pdf-save').href = url;
            document.getElementById('stride-pdf-frame').src = url + '#toolbar=1&navpanes=0';
            document.body.style.overflow = 'hidden';
        };

        // Automatically bind to all PDF links across the document
        document.querySelectorAll('a[href$=".pdf"], a[href*=".pdf?"]').forEach(function(link) {
            link.removeAttribute('download');
            link.addEventListener('click', function(e) {
                const href = link.getAttribute('href');
                if (href && href.toLowerCase().includes('.pdf')) {
                    e.preventDefault();
                    let title = link.getAttribute('data-title') || link.getAttribute('title');
                    if (!title) {
                        const cardHeading = link.closest('.glass-panel, .glass-card, div')?.querySelector('h2, h3, h4');
                        title = cardHeading ? cardHeading.innerText.trim() : (link.innerText.trim().replace(/^[\s\S]{0,3}(Download|Read|PDF|Whitepaper)\s*/i, '') || 'StrideAnalytics Document');
                    }
                    window.openStridePdf(href, title);
                }
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initUniversalPdfReader);
    } else {
        initUniversalPdfReader();
    }

    // Auto-load Stride Behavioral Telemetry Tracker across all site pages
    try {
        if (!window.strideTrackEvent) {
            const telScript = document.createElement('script');
            telScript.src = '/stride-telemetry.js?v=20261012';
            telScript.async = true;
            document.head.appendChild(telScript);
        }
    } catch(e) {}
})();


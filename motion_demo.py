"""
Interactive Motion Demo Video HTML Generator for Banki Kuu SACCO
Returns full self-contained HTML for embedding directly into Streamlit Cloud.
"""

def get_bks_motion_html() -> str:
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Banki Kuu SACCO - SaaS Delegate Journey Motion Simulation</title>
    <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
    <style>
        @keyframes laserScan {
            0% { top: 0%; opacity: 0.8; }
            50% { top: 90%; opacity: 1; }
            100% { top: 0%; opacity: 0.8; }
        }
        .laser-line {
            position: absolute;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, #00F2FE, #F5C542, #00F2FE, transparent);
            box-shadow: 0 0 15px #00F2FE, 0 0 25px #F5C542;
            animation: laserScan 2s ease-in-out infinite;
        }
        @keyframes pulseGlow {
            0%, 100% { box-shadow: 0 0 15px rgba(245, 197, 66, 0.4), 0 0 30px rgba(0, 242, 254, 0.2); }
            50% { box-shadow: 0 0 30px rgba(245, 197, 66, 0.8), 0 0 50px rgba(0, 242, 254, 0.5); }
        }
        .glow-card {
            animation: pulseGlow 4s infinite ease-in-out;
        }
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        .typewriter {
            overflow: hidden;
            white-space: nowrap;
            animation: typing 2.5s steps(40, end);
        }
    </style>
</head>
<body class="bg-slate-950 text-white antialiased p-3 sm:p-5">

<div class="bg-slate-900 text-white border border-slate-700 rounded-2xl p-5 shadow-2xl max-w-4xl mx-auto space-y-5">
    
    <!-- Top Header Banner -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b border-slate-800 pb-4">
        <div>
            <div class="inline-flex items-center gap-2 bg-gradient-to-r from-amber-500/20 to-blue-500/20 border border-amber-400/40 text-amber-300 text-xs font-extrabold px-3 py-1 rounded-full uppercase tracking-widest">
                <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
                SaaS Boardroom Presentation Simulation
            </div>
            <h2 class="text-xl sm:text-2xl font-black tracking-tight text-white mt-1.5 flex items-center gap-2">
                🏦 Banki Kuu SACCO — End-to-End AGM Journey
            </h2>
            <p class="text-xs sm:text-sm text-slate-400">
                Interactive video-style flow simulation for Board of Directors & Scrutineers approval
            </p>
        </div>
        
        <!-- Video Player Control Panel -->
        <div class="flex items-center gap-2 bg-slate-950 p-1.5 rounded-xl border border-slate-800 self-stretch sm:self-auto justify-center">
            <button id="btnPrev" onclick="stepPrev()" class="p-2 rounded-lg bg-slate-900 hover:bg-amber-500/20 text-xs font-bold text-white transition-all border border-slate-700">
                ⏮️ Prev
            </button>
            <button id="btnPlay" onclick="togglePlay()" class="px-4 py-2 rounded-lg bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 text-xs font-black uppercase tracking-wider transition-all shadow-lg flex items-center gap-1.5">
                <span id="playIcon">▶️</span> <span id="playText">PLAY VIDEO</span>
            </button>
            <button id="btnNext" onclick="stepNext()" class="p-2 rounded-lg bg-slate-900 hover:bg-amber-500/20 text-xs font-bold text-white transition-all border border-slate-700">
                Next ⏭️
            </button>
        </div>
    </div>

    <!-- Timeline Stepper Bar -->
    <div class="grid grid-cols-5 gap-1.5 sm:gap-2">
        <button onclick="goToStage(0)" id="stepTab-0" class="step-tab p-2 rounded-xl border text-center transition-all bg-amber-500/20 border-amber-400 text-white font-bold text-xs">
            <div class="text-base sm:text-lg mb-0.5">📱</div>
            <div class="truncate text-[11px] sm:text-xs">1. Dispatch</div>
        </button>
        <button onclick="goToStage(1)" id="stepTab-1" class="step-tab p-2 rounded-xl border text-center transition-all bg-slate-950 border-slate-800 text-slate-400 text-xs">
            <div class="text-base sm:text-lg mb-0.5">🎟️</div>
            <div class="truncate text-[11px] sm:text-xs">2. Dynamic Pass</div>
        </button>
        <button onclick="goToStage(2)" id="stepTab-2" class="step-tab p-2 rounded-xl border text-center transition-all bg-slate-950 border-slate-800 text-slate-400 text-xs">
            <div class="text-base sm:text-lg mb-0.5">📷</div>
            <div class="truncate text-[11px] sm:text-xs">3. Gate Scan</div>
        </button>
        <button onclick="goToStage(3)" id="stepTab-3" class="step-tab p-2 rounded-xl border text-center transition-all bg-slate-950 border-slate-800 text-slate-400 text-xs">
            <div class="text-base sm:text-lg mb-0.5">📊</div>
            <div class="truncate text-[11px] sm:text-xs">4. Quorum Meter</div>
        </button>
        <button onclick="goToStage(4)" id="stepTab-4" class="step-tab p-2 rounded-xl border text-center transition-all bg-slate-950 border-slate-800 text-slate-400 text-xs">
            <div class="text-base sm:text-lg mb-0.5">🗳️</div>
            <div class="truncate text-[11px] sm:text-xs">5. E-Voting</div>
        </button>
    </div>

    <!-- Main Motion Screen (Video Stage Canvas) -->
    <div class="relative bg-gradient-to-b from-slate-950 via-slate-900 to-slate-950 border-2 border-amber-400/50 rounded-2xl p-4 sm:p-6 min-h-[310px] flex flex-col justify-between overflow-hidden shadow-inner glow-card">
        
        <!-- Live Scene Indicator -->
        <div class="flex justify-between items-center text-xs font-bold text-amber-300 uppercase tracking-widest border-b border-white/10 pb-2 mb-3">
            <span id="sceneTitle" class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
                STAGE 1: PRE-AGM BULK DISPATCH (SMS / WHATSAPP / EMAIL)
            </span>
            <span id="sceneCounter" class="bg-amber-400/20 px-2 py-0.5 rounded text-amber-300 text-[11px]">SCENE 1 / 5</span>
        </div>

        <!-- Dynamic Content Canvas -->
        <div id="stageCanvas" class="my-auto py-2">
            <!-- Injected dynamically via JS -->
        </div>

        <!-- Stage Explainer & SaaS Benefit Bar -->
        <div class="mt-4 pt-3 border-t border-white/10 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 text-xs">
            <div id="stageNarrative" class="text-slate-300 font-medium leading-relaxed">
                Automated dispatch pushes personalized confirmation links to all 500+ registered members via SMS/WhatsApp/Email.
            </div>
            <div id="stageSaaSImpact" class="bg-blue-500/20 border border-cyan-400/40 text-cyan-300 font-bold px-3 py-1 rounded-lg shrink-0">
                💡 Eliminates manual phone calling & physical mailer expenses
            </div>
        </div>
    </div>

    <!-- Bottom SaaS Value Grid for SACCO Board -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
        <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-center">
            <div class="text-amber-400 font-black text-base sm:text-lg">95%+</div>
            <div class="text-slate-400 font-semibold mt-0.5">AGM Cost Savings</div>
        </div>
        <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-center">
            <div class="text-emerald-400 font-black text-base sm:text-lg">&lt; 2 Secs</div>
            <div class="text-slate-400 font-semibold mt-0.5">Gate Clearance Speed</div>
        </div>
        <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-center">
            <div class="text-cyan-400 font-black text-base sm:text-lg">100%</div>
            <div class="text-slate-400 font-semibold mt-0.5">SASRA Quorum Audited</div>
        </div>
        <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-center">
            <div class="text-purple-400 font-black text-base sm:text-lg">SHA-256</div>
            <div class="text-slate-400 font-semibold mt-0.5">Encrypted Ballot Hash</div>
        </div>
    </div>

</div>

<script>
const STAGES = [
    {
        title: "STAGE 1: PRE-AGM BULK DISPATCH (SMS / WHATSAPP / EMAIL)",
        counter: "SCENE 1 / 5",
        narrative: "Automated bulk engine dispatches encrypted invitations to 500+ member phones with zero manual effort.",
        saasImpact: "⚡ Saves KES 350,000+ in printing & postage",
        render: () => `
            <div class="max-w-md mx-auto bg-slate-900 border border-slate-700 rounded-2xl p-4 shadow-xl text-left">
                <div class="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-2 mb-3">
                    <span class="font-bold text-amber-400">💬 SMS Dispatch Engine</span>
                    <span>Just Now</span>
                </div>
                <div class="bg-blue-950/80 border border-blue-500/40 rounded-xl p-3 text-xs text-slate-200 leading-relaxed font-sans">
                    <div class="font-bold text-amber-300 mb-1">Banki Kuu Staff SACCO 58th AGM</div>
                    Dear <span class="text-cyan-300 font-bold">Samuel Gathigi</span> (Member #342801), click your confidential link to confirm attendance & get your dynamic pass:
                    <div class="mt-2 text-cyan-400 underline font-mono text-[11px] bg-slate-900 p-1.5 rounded">
                        https://cbk-stride.streamlit.app/BKS?confirm=TKT-BK-342801
                    </div>
                </div>
                <div class="mt-2 text-right text-[11px] text-emerald-400 font-bold flex items-center justify-end gap-1">
                    <span>✓ Delivered via Safaricom STK Pipeline</span>
                </div>
            </div>
        `
    },
    {
        title: "STAGE 2: 1-CLICK CONFIRMATION & DYNAMIC QR PASS",
        counter: "SCENE 2 / 5",
        narrative: "Member taps link, confirming attendance instantly and generating a dynamic anti-counterfeit QR pass.",
        saasImpact: "🎟️ Zero Paper Tickets • 100% Mobile Ready",
        render: () => `
            <div class="max-w-sm mx-auto bg-gradient-to-b from-blue-950 to-slate-950 border-2 border-amber-400 rounded-2xl p-4 text-center shadow-2xl">
                <div class="text-[11px] font-black tracking-widest text-amber-300 uppercase">BANKI KUU STAFF SACCO LTD</div>
                <div class="text-sm font-bold text-white mt-0.5">58th AGM Shareholder Pass</div>
                <div class="my-3 bg-white p-3 rounded-xl inline-block shadow-lg border border-amber-400">
                    <img src="https://api.qrserver.com/v1/create-qr-code/?size=130x130&data=TKT-BK-342801" class="w-28 h-28 mx-auto" alt="QR Pass" />
                </div>
                <div class="text-xs text-cyan-300 font-bold">Samuel Gathigi</div>
                <div class="text-[11px] text-slate-400 font-mono">ID: SACCO-3428 • Serial: TKT-BK-342801</div>
                <div class="mt-2 inline-block bg-emerald-500/20 text-emerald-400 text-[11px] font-bold px-3 py-0.5 rounded-full border border-emerald-400/30">
                    ● CONFIRMED & READY FOR ENTRANCE
                </div>
            </div>
        `
    },
    {
        title: "STAGE 3: 2-SECOND FAST-TRACK GATE USHER SCAN",
        counter: "SCENE 3 / 5",
        narrative: "Venue ushers scan the QR pass with any smartphone. Ticket is authenticated in under 2 seconds.",
        saasImpact: "🚀 Eliminates 2-Hour Hall Entry Congestion",
        render: () => `
            <div class="max-w-md mx-auto bg-slate-900 border border-cyan-500/50 rounded-2xl p-4 text-center relative overflow-hidden shadow-2xl">
                <div class="laser-line"></div>
                <div class="text-xs text-slate-400 uppercase font-bold tracking-wider mb-2">📷 Gate Scanner Mobile Terminal</div>
                <div class="bg-slate-950 p-4 rounded-xl border border-slate-800">
                    <div class="text-3xl mb-1">📱 ↔️ 🎟️</div>
                    <div class="text-emerald-400 font-black text-base uppercase tracking-wider">✓ ADMITTED & ACCREDITED</div>
                    <div class="text-xs text-white font-bold mt-1">Delegate: Samuel Gathigi</div>
                    <div class="text-[11px] text-slate-400">Timestamp: 08:34:12 EAT • Gate 1 Usher Terminal</div>
                </div>
            </div>
        `
    },
    {
        title: "STAGE 4: REAL-TIME SASRA STATUTORY QUORUM METER",
        counter: "SCENE 4 / 5",
        narrative: "Accreditation automatically updates the SASRA Quorum Meter live on the main hall LED screen.",
        saasImpact: "📊 100% Regulatory SASRA Compliance Audited",
        render: () => `
            <div class="max-w-md mx-auto bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 border border-amber-400/60 rounded-2xl p-4 text-center shadow-xl">
                <div class="text-xs font-bold text-amber-300 uppercase tracking-widest mb-1">🏛️ SASRA STATUTORY QUORUM MONITOR</div>
                <div class="text-3xl font-black text-emerald-400 my-1">50 / 50 DELEGATES</div>
                <div class="w-full bg-slate-800 rounded-full h-3 border border-slate-700 overflow-hidden my-2">
                    <div class="bg-gradient-to-r from-amber-400 to-emerald-400 h-3 rounded-full w-full transition-all duration-1000"></div>
                </div>
                <div class="text-xs font-bold text-emerald-300 bg-emerald-500/20 py-1 px-3 rounded-lg border border-emerald-400/40 inline-block">
                    ✓ STATUTORY QUORUM ATTAINED — ASSEMBLY COMMENCED
                </div>
            </div>
        `
    },
    {
        title: "STAGE 5: ENCRYPTED E-VOTING & CRYPTOGRAPHIC RECEIPT",
        counter: "SCENE 5 / 5",
        narrative: "Member casts vote on their smartphone. System generates a tamper-evident SHA-256 receipt.",
        saasImpact: "🔒 Bulletproof Electoral Integrity & Zero Double-Voting",
        render: () => `
            <div class="max-w-md mx-auto bg-slate-900 border-2 border-emerald-400 rounded-2xl p-4 text-center shadow-2xl">
                <div class="text-2xl mb-1">🗳️ 🔒</div>
                <div class="text-emerald-400 font-black text-sm uppercase tracking-wider">✓ BALLOT CAST & CERTIFIED</div>
                <div class="text-xs text-white font-bold mt-1">Resolution: 2026 Dividend Distribution (12.5%)</div>
                <div class="mt-2 bg-slate-950 p-2.5 rounded-xl border border-slate-800 text-[11px] font-mono text-cyan-300 text-left">
                    <div class="text-slate-500 text-[10px] uppercase font-sans">SHA-256 Cryptographic Hash Receipt:</div>
                    0x7f8a9b3c4d5e6f1a2b3c4d5e6f7a8b9c0d1e2f3a
                </div>
                <div class="mt-2 text-[11px] text-amber-300 font-bold">● Double-Voting Lock Active</div>
            </div>
        `
    }
];

let currentStage = 0;
let isPlaying = false;
let playInterval = null;

function renderStage(idx) {
    const stage = STAGES[idx];
    document.getElementById("sceneTitle").innerHTML = `<span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span> ${stage.title}`;
    document.getElementById("sceneCounter").innerText = stage.counter;
    document.getElementById("stageCanvas").innerHTML = stage.render();
    document.getElementById("stageNarrative").innerText = stage.narrative;
    document.getElementById("stageSaaSImpact").innerText = stage.saasImpact;

    STAGES.forEach((_, i) => {
        const tab = document.getElementById(`stepTab-${i}`);
        if (i === idx) {
            tab.className = "step-tab p-2 rounded-xl border text-center transition-all bg-amber-500/20 border-amber-400 text-white font-bold text-xs shadow-lg";
        } else {
            tab.className = "step-tab p-2 rounded-xl border text-center transition-all bg-slate-950 border-slate-800 text-slate-400 text-xs";
        }
    });
}

function goToStage(idx) {
    currentStage = idx;
    renderStage(currentStage);
}

function stepNext() {
    currentStage = (currentStage + 1) % STAGES.length;
    renderStage(currentStage);
}

function stepPrev() {
    currentStage = (currentStage - 1 + STAGES.length) % STAGES.length;
    renderStage(currentStage);
}

function togglePlay() {
    isPlaying = !isPlaying;
    const playIcon = document.getElementById("playIcon");
    const playText = document.getElementById("playText");
    const btnPlay = document.getElementById("btnPlay");

    if (isPlaying) {
        playIcon.innerText = "⏸️";
        playText.innerText = "PAUSE";
        btnPlay.className = "px-4 py-2 rounded-lg bg-gradient-to-r from-red-500 to-amber-500 text-white text-xs font-black uppercase tracking-wider transition-all shadow-lg flex items-center gap-1.5";
        playInterval = setInterval(() => {
            stepNext();
        }, 3500);
    } else {
        playIcon.innerText = "▶️";
        playText.innerText = "PLAY VIDEO";
        btnPlay.className = "px-4 py-2 rounded-lg bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 text-xs font-black uppercase tracking-wider transition-all shadow-lg flex items-center gap-1.5";
        clearInterval(playInterval);
    }
}

renderStage(0);
</script>

</body>
</html>"""

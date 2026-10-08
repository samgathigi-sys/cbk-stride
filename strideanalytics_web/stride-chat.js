/**
 * Stride AI Sovereign Copilot - Embedded Client Assistant
 * Provides interactive instant telemetry explanations, SASRA regulations,
 * ODPC privacy compliance, and multi-tenant guidance.
 */
(function() {
    // 1. Inject Stylesheet if not present with cache busting
    if (!document.getElementById('stride-chat-css')) {
        const link = document.createElement('link');
        link.id = 'stride-chat-css';
        link.rel = 'stylesheet';
        link.href = 'stride-chat.css?v=' + Date.now();
        document.head.appendChild(link);
    }

    // 2. Build Widget HTML with inline right-side positioning to bypass any cached CSS
    const widgetContainer = document.createElement('div');
    widgetContainer.id = 'stride-ai-container';
    widgetContainer.innerHTML = `
        <!-- Floating Launcher Bubble (Bottom-Right) -->
        <div id="stride-launcher" class="stride-ai-bubble" style="right: 24px !important; left: auto !important;" onclick="toggleStrideChat()">
            <div class="avatar-ring">
                S
                <span class="pulse-dot"></span>
            </div>
            <div class="flex flex-col text-left">
                <span class="text-xs font-black font-mono tracking-tight text-white flex items-center gap-1.5">
                    STRIDE AI <span class="text-[9px] px-1.5 py-0.2 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-mono">COPILOT</span>
                </span>
                <span class="text-[10px] text-cyan-400 font-mono">Ask Telemetry & SASRA</span>
            </div>
        </div>

        <!-- Chat Window -->
        <div id="stride-chat-box" class="stride-ai-window" style="right: 24px !important; left: auto !important;">
            <!-- Header -->
            <div class="stride-chat-header">
                <div class="flex items-center gap-2.5">
                    <div class="w-7 h-7 rounded-lg bg-gradient-to-r from-cyan-400 to-purple-600 flex items-center justify-center font-bold text-navy-950 text-xs font-heading">
                        S
                    </div>
                    <div>
                        <div class="text-xs font-bold text-white font-mono flex items-center gap-1.5">
                            Stride Sovereign Copilot
                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                        </div>
                        <div class="text-[10px] text-cyan-400 font-mono">ODPC v2.4 • SASRA Cap 490B AI Core</div>
                    </div>
                </div>
                <button onclick="toggleStrideChat()" class="text-slate-400 hover:text-white text-base font-mono px-2 py-1 rounded">✕</button>
            </div>

            <!-- Messages Body -->
            <div id="stride-messages" class="stride-chat-body font-sans">
                <!-- Welcome Bot Message -->
                <div class="stride-chat-msg bot">
                    <div class="text-cyan-400 font-mono font-bold text-[11px] mb-1">🤖 Stride Intelligence Core:</div>
                    Hello! I am your <strong>Stride Sovereign AI Assistant</strong>. Ask me anything about SACCO liquidity ratios, SASRA supervisory rules, the 10-year running balance model, or ODPC data privacy.
                    <div class="mt-2.5 pt-2 border-t border-cyan-500/20">
                        <span class="text-[10px] text-slate-400 block mb-1 font-mono">Quick Inquiries:</span>
                        <div class="flex flex-wrap gap-1">
                            <span class="stride-quick-prompt" onclick="askQuickPrompt('Explain running balance vs summation')">Running Balance vs Flow</span>
                            <span class="stride-quick-prompt" onclick="askQuickPrompt('What are SASRA liquidity minimums?')">SASRA Liquidity Rules</span>
                            <span class="stride-quick-prompt" onclick="askQuickPrompt('How does Stride protect member PII?')">ODPC Privacy Masking</span>
                            <span class="stride-quick-prompt" onclick="askQuickPrompt('Tell me about Stride-SACCO dummy tenant')">Stride-SACCO 10-Yr</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Input Bar -->
            <div class="stride-chat-footer">
                <input type="text" id="stride-input" class="stride-chat-input" placeholder="Type a financial or regulatory question..." onkeydown="handleChatKey(event)">
                <button class="stride-send-btn" onclick="sendStrideMessage()">
                    ➤
                </button>
            </div>
        </div>
    `;
    document.body.appendChild(widgetContainer);

    // 3. Knowledge Base & Response Engine
    const responses = [
        {
            keywords: ['running balance', 'summation', 'stock', 'flow', 'ceo', 'prudential accounting'],
            reply: `💡 <strong>Absolute Running Balance vs Flow:</strong><br><br>
In institutional accounting (governed by SASRA & IFRS 9 standards), <strong>Total Loan Book</strong> and <strong>Member Deposits</strong> are <em>Balance Sheet closing balances</em> as of December 31. They must <strong>never</strong> be summed across years.<br><br>
To see annual movement, toggle the <strong>Net Annual Mobilization (Δ YoY Flow)</strong> chart on the <a href="stride-sacco.html" class="text-cyan-400 underline">Stride-SACCO portal</a>.`
        },
        {
            keywords: ['sasra', 'prudential', 'liquidity', 'ratio', 'statutory', 'limit'],
            reply: `🏛️ <strong>SASRA Statutory Benchmarks (Sacco Societies Act Cap 490B):</strong><br><br>
• <strong>Core Capital to Total Assets:</strong> Minimum <strong>10.0%</strong> (Stride-SACCO operates at 14.6%).<br>
• <strong>Liquidity Ratio:</strong> Minimum <strong>15.0%</strong> (Stride-SACCO operates at 34.2%).<br>
• <strong>PAR > 30 Days (NPL):</strong> Recommended below <strong>5.0%</strong> (Stride-SACCO operates at 3.85%).<br>
• <strong>External Borrowing:</strong> Maximum <strong>25.0%</strong> of Total Assets.`
        },
        {
            keywords: ['odpc', 'pii', 'privacy', 'anonymize', 'token', 'mask'],
            reply: `🔒 <strong>ODPC Sovereign Data Shield:</strong><br><br>
In compliance with Kenya's Data Protection Act (2019), Stride automatically salts and dynamically masks member identifiers (e.g. <code>MBR-**8492-KE</code>). Raw PII never leaves the local jurisdictional perimeter and is cryptographically anchored via SHA-256 Merkle root trees.`
        },
        {
            keywords: ['stride-sacco', '10 year', 'longitudinal', 'dummy'],
            reply: `📊 <strong>Stride-SACCO 10-Year Simulation:</strong><br><br>
Tracks balance sheet growth from KES 3.10B (2015) to <strong>KES 14.82B (2025)</strong> across 68,400 active members. Includes COVID-19 resilience benchmarks, macro rate shock simulations, and direct SASRA Form 1 & 4 filing exports. Explore it at <a href="stride-sacco.html" class="text-cyan-400 underline">strideanalytics.co.ke/stride-sacco.html</a>!`
        },
        {
            keywords: ['credit', 'score', 'underwriting', 'loan', 'pd'],
            reply: `⚡ <strong>CreditScore Predictive Engine:</strong><br><br>
Uses machine learning probability of default (PD) modeling calibrated to Kenyan cash flow cycles. Evaluates debt-service coverage, member savings velocity, and guarantor networks in under 14 milliseconds. Try the simulator on <a href="creditscore.html" class="text-cyan-400 underline">creditscore.html</a>.`
        },
        {
            keywords: ['contact', 'email', 'phone', 'location', 'who we are'],
            reply: `✉️ <strong>Stride Analytics Contact Desk:</strong><br><br>
• <strong>Email:</strong> <a href="mailto:info@strideanalytics.co.ke" class="text-cyan-400 underline">info@strideanalytics.co.ke</a><br>
• <strong>Headquarters:</strong> Nairobi Financial Corridor, Kenya.<br>
• <strong>Portal:</strong> Scan our interactive vCard QR on the <a href="about.html" class="text-cyan-400 underline">Who We Are</a> page!`
        }
    ];

    window.toggleStrideChat = function() {
        const box = document.getElementById('stride-chat-box');
        box.classList.toggle('open');
        if (box.classList.contains('open')) {
            document.getElementById('stride-input').focus();
        }
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

        // Simulate Neural Thinking
        setTimeout(() => {
            const query = text.toLowerCase();
            let matchedReply = null;

            for (const item of responses) {
                if (item.keywords.some(k => query.includes(k))) {
                    matchedReply = item.reply;
                    break;
                }
            }

            if (!matchedReply) {
                matchedReply = `🤖 <strong>Stride AI Core:</strong><br><br>
I've analyzed your query regarding <em>"${text.replace(/</g, "&lt;")}"</em> against our sovereign data architecture. You can review detailed interactive telemetry in our dedicated enterprise modules:<br>
• <a href="saccostride.html" class="text-cyan-400 underline">SaccoStride</a> for liquidity & stress-tests.<br>
• <a href="stride-sacco.html" class="text-purple-400 underline">Stride-SACCO</a> for 10-year running balance models.<br>
• <a href="about.html" class="text-emerald-400 underline">Contacts &amp; Who We Are</a> to speak with an engineering liaison.`;
            }

            const botMsg = document.createElement('div');
            botMsg.className = 'stride-chat-msg bot';
            botMsg.innerHTML = matchedReply;
            container.appendChild(botMsg);
            container.scrollTop = container.scrollHeight;
        }, 350);
    };
})();

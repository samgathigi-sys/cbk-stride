import os
import sys
import matplotlib
matplotlib.use('Agg') # non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("commercial_assets", exist_ok=True)

# Set global aesthetic style
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# VISUAL 1: DUAL OPERATING COMMERCIAL MODELS
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5.5), dpi=300)
fig.patch.set_facecolor('#081830')
ax.set_facecolor('#081830')
ax.axis('off')

# Titles
ax.text(0.5, 0.95, "STRIDE™ DUAL-OPERATING COMMERCIAL MODEL", color="#F5C542", fontsize=16, fontweight='bold', ha='center', va='top')
ax.text(0.5, 0.88, "How Clients Self-Provision vs. How You Deliver Turnkey Managed Services", color="#CBD5E1", fontsize=10, ha='center', va='top')

# Card 1: Self-Service SaaS ("They Make It")
rect1 = plt.Rectangle((0.05, 0.12), 0.42, 0.70, transform=ax.transAxes, facecolor='#0D2240', edgecolor='#00F2FE', linewidth=2, linestyle='-', zorder=1)
ax.add_patch(rect1)
ax.text(0.26, 0.76, "MODEL A: SELF-SERVICE SaaS", color="#00F2FE", fontsize=12, fontweight='bold', ha='center', va='center')
ax.text(0.26, 0.71, "('THEY MAKE IT')", color="#FFE58F", fontsize=10, fontweight='bold', ha='center', va='center')

bullets_a = [
    "• Target: Event planners, SACCO secretaries, club captains",
    "• Flow: Client visits cbk-stride.streamlit.app/EVENTS",
    "• Step 1: Answers 4 scoping questions in Wizard",
    "• Step 2: Instant M-Pesa STK Push payment",
    "• Output: System auto-spins Event ID (EVT-2026-XXX)",
    "• Handover: Automated Gate QR + instant URL link",
    "• Pricing: KES 15,000 – KES 75,000 / event",
    "• Your Effort: ZERO (100% automated passive cashflow)"
]
for idx, b in enumerate(bullets_a):
    ax.text(0.08, 0.63 - idx * 0.065, b, color="#E2E8F0", fontsize=8.2, va='center')

# Card 2: Turnkey Concierge Agency ("You Make It & Give The Link")
rect2 = plt.Rectangle((0.53, 0.12), 0.42, 0.70, transform=ax.transAxes, facecolor='#0D2240', edgecolor='#F5C542', linewidth=2, linestyle='-', zorder=1)
ax.add_patch(rect2)
ax.text(0.74, 0.76, "MODEL B: TURNKEY CONCIERGE", color="#F5C542", fontsize=12, fontweight='bold', ha='center', va='center')
ax.text(0.74, 0.71, "('YOU MAKE IT & GIVE THE LINK')", color="#34D399", fontsize=10, fontweight='bold', ha='center', va='center')

bullets_b = [
    "• Target: Tier-1 Banks, Blue-Chip SACCOs, State Galas",
    "• Flow: High-ticket executive pitch to Board / Secretariat",
    "• Step 1: You configure bespoke meeting parameters in Wizard",
    "• Step 2: You provision corporate invoice & Paybill routing",
    "• Output: You print roll-up QR entrance banners for venue",
    "• Handover: Hand over configured iPads + gate usher links",
    "• Pricing: KES 85,000 – KES 250,000+ / engagement",
    "• Your Effort: 2-3 hours setup + high-margin consultation"
]
for idx, b in enumerate(bullets_b):
    ax.text(0.56, 0.63 - idx * 0.065, b, color="#E2E8F0", fontsize=8.2, va='center')

# Bottom Banner
ax.text(0.5, 0.05, "★ Both models share the EXACT SAME underlying architecture, database, and anti-counterfeit QR engine.", color="#38BDF8", fontsize=9, fontstyle='italic', ha='center', va='center')

plt.tight_layout()
plt.savefig("commercial_assets/visual_operating_models.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved visual_operating_models.png")

# ==============================================================================
# VISUAL 2: MODULAR PRICING WATERFALL & SETUP REVENUE
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
fig.patch.set_facecolor('#081830')
ax.set_facecolor('#0B1E38')

categories = ['Base Scale\nLicense', 'Specialized\nModule (AGM/Sports)', 'Gate Hardware\n& Ushers', 'Auditing &\nCompliance', 'Statutory VAT\n(16%)', 'TOTAL TYPICAL\nREVENUE']
values = [45000, 25000, 20000, 15000, 16800, 121800]
colors = ['#00F2FE', '#38BDF8', '#818CF8', '#A78BFA', '#F59E0B', '#10B981']

bars = ax.bar(categories, values, color=colors, width=0.55, edgecolor='#FFFFFF', linewidth=0.7)

for bar in bars:
    height = bar.get_height()
    ax.annotate(f'KES {height:,.0f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6),
                textcoords="offset points",
                ha='center', va='bottom',
                color='#FFFFFF', fontweight='bold', fontsize=9.5)

ax.set_title("STRIDE™ MODULAR PRICING ENGINE (TYPICAL TIER-1 SACCO AGM QUOTE)", color='#F5C542', fontsize=14, fontweight='bold', pad=18)
ax.set_ylabel("Platform Fee (KES)", color='#CBD5E1', fontsize=10)
ax.tick_params(colors='#CBD5E1', labelsize=8.8)
ax.grid(axis='y', linestyle='--', alpha=0.15, color='#FFFFFF')
ax.set_ylim(0, 140000)

plt.tight_layout()
plt.savefig("commercial_assets/visual_pricing_waterfall.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved visual_pricing_waterfall.png")

# ==============================================================================
# VISUAL 3: MONTHLY REVENUE PROJECTIONS ACROSS 4 CLUSTERS
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
fig.patch.set_facecolor('#081830')
ax.set_facecolor('#0B1E38')

clusters = ['Tier-1 SACCO\n& Corporate AGMs', 'Inter-Bank & Corporate\nSports Tournaments', 'Professional\nConferences & Seminars', 'High-End Galas\n& Corporate Dinners']
events_per_month = [3, 2, 2, 1]
avg_fee_per_event = [115000, 85000, 65000, 45000]
monthly_rev = [e * f for e, f in zip(events_per_month, avg_fee_per_event)]

y_pos = np.arange(len(clusters))
bars = ax.barh(y_pos, monthly_rev, color=['#10B981', '#00F2FE', '#F5C542', '#EC4899'], edgecolor='#FFFFFF', linewidth=0.8, height=0.55)

for bar, ev_count, fee in zip(bars, events_per_month, avg_fee_per_event):
    width = bar.get_width()
    ax.text(width + 8000, bar.get_y() + bar.get_height()/2,
            f"KES {width:,.0f}/mo ({ev_count} events @ KES {fee:,.0f})",
            va='center', color='#FFFFFF', fontweight='bold', fontsize=9)

ax.set_yticks(y_pos)
ax.set_yticklabels(clusters, color='#CBD5E1', fontsize=9.5, fontweight='bold')
ax.set_xlabel("Projected Monthly Revenue (KES)", color='#CBD5E1', fontsize=10)
ax.set_title("PROJECTED MONTHLY REVENUE BY MARKET CLUSTER (CONSERVATIVE 8 EVENTS/MO)", color='#F5C542', fontsize=13, fontweight='bold', pad=18)
ax.set_xlim(0, 450000)
ax.tick_params(colors='#CBD5E1')
ax.grid(axis='x', linestyle='--', alpha=0.15, color='#FFFFFF')

plt.tight_layout()
plt.savefig("commercial_assets/visual_market_projections.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved visual_market_projections.png")

# ==============================================================================
# VISUAL 4: END-TO-END EVENT LIFECYCLE FLOW
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 4.8), dpi=300)
fig.patch.set_facecolor('#081830')
ax.set_facecolor('#081830')
ax.axis('off')

ax.text(0.5, 0.93, "STRIDE™ END-TO-END EVENT PROVISIONING & ACCREDITATION LIFECYCLE", color="#F5C542", fontsize=13, fontweight='bold', ha='center')

steps = [
    ("1. SCOPING WIZARD", "Select category & answer\n4 modular questions\n(Scale, HW, Audits)", "#00F2FE"),
    ("2. M-PESA STK SETTLE", "Instant STK push triggers\nKES fee payment &\ngenerates official tax invoice", "#38BDF8"),
    ("3. EVENT PROVISION", "System registers isolated\nEvent ID (EVT-2026-XXX)\nin SQLite database", "#F5C542"),
    ("4. GATE QR HANDOVER", "Download entrance QR &\nURL link for iPad desk\n& roll-up venue banners", "#10B981"),
    ("5. PASSENGER CHECK-IN", "Attendees scan, register,\nreceive anti-counterfeit QR\npass, & cast ballots", "#A78BFA")
]

box_width = 0.16
box_height = 0.52
spacing = 0.035
start_x = 0.035
y_pos = 0.22

for idx, (title, desc, border_col) in enumerate(steps):
    x = start_x + idx * (box_width + spacing)
    rect = plt.Rectangle((x, y_pos), box_width, box_height, transform=ax.transAxes,
                         facecolor='#0D2240', edgecolor=border_col, linewidth=2)
    ax.add_patch(rect)
    ax.text(x + box_width/2, y_pos + box_height - 0.08, title, color=border_col,
            fontsize=8.5, fontweight='bold', ha='center', va='center')
    ax.text(x + box_width/2, y_pos + box_height/2 - 0.06, desc, color='#E2E8F0',
            fontsize=7.2, ha='center', va='center', multialignment='center')
    
    # Arrow
    if idx < len(steps) - 1:
        ax.annotate('', xy=(x + box_width + spacing * 0.9, y_pos + box_height/2),
                    xytext=(x + box_width + spacing * 0.1, y_pos + box_height/2),
                    arrowprops=dict(arrowstyle="->", color="#F5C542", lw=2))

ax.text(0.5, 0.08, "Outcome: Complete zero-friction event execution from ticket issuance to statutory quorum auditing.",
        color="#34D399", fontsize=9, fontweight='bold', ha='center')

plt.tight_layout()
plt.savefig("commercial_assets/visual_portal_lifecycle.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved visual_portal_lifecycle.png")

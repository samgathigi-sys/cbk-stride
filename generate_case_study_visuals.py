import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("commercial_assets", exist_ok=True)

plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# VISUAL 1: CASE STUDY ROI WATERFALL (KES SAVINGS & FRAUD PREVENTION)
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
fig.patch.set_facecolor('#081830')
ax.set_facecolor('#0B1E38')

categories = [
    'STRIDE™ Fee\n(Investment)',
    'Prevented Phantom\nPer-Diems',
    'Avoided Venue\nOvertime Fines',
    'Prevented Proxy\nLegal Disputes',
    'NET FINANCIAL\nVALUE GAINED'
]
amounts = [-115000, 1820000, 450000, 400000, 2555000]
colors = ['#EF4444', '#10B981', '#00F2FE', '#38BDF8', '#F5C542']

bars = ax.bar(categories, amounts, color=colors, width=0.52, edgecolor='#FFFFFF', linewidth=0.8)

for bar, amt in zip(bars, amounts):
    height = bar.get_height()
    va = 'bottom' if height >= 0 else 'top'
    y_pos = height + (35000 if height >= 0 else -65000)
    sign = "+" if amt > 0 else ""
    ax.annotate(f'{sign}KES {amt:,.0f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 6 if height >= 0 else -14),
                textcoords="offset points",
                ha='center', va=va,
                color='#FFFFFF', fontweight='bold', fontsize=9.2)

ax.set_title("CASE STUDY FINANCIAL ROI: HOW A KES 115K STRIDE DEPLOYMENT CREATES KES 2.55M VALUE",
             color='#F5C542', fontsize=12.5, fontweight='bold', pad=18)
ax.set_ylabel("Financial Impact (KES)", color='#CBD5E1', fontsize=10)
ax.tick_params(colors='#CBD5E1', labelsize=8.5)
ax.grid(axis='y', linestyle='--', alpha=0.15, color='#FFFFFF')
ax.axhline(0, color='#94A3B8', linewidth=1)
ax.set_ylim(-300000, 3000000)

plt.tight_layout()
plt.savefig("commercial_assets/case_study_roi_waterfall.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved case_study_roi_waterfall.png")

# ==============================================================================
# VISUAL 2: BEFORE VS AFTER OPERATIONAL METRICS (THE STRIDE IMPACT)
# ==============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), dpi=300)
fig.patch.set_facecolor('#081830')

# Subplot 1: Accreditation Time (Minutes)
ax1.set_facecolor('#0B1E38')
metrics_time = ['Delegate Queue Time', 'Quorum Tally Time']
legacy_time = [180, 150] # minutes
stride_time = [14, 0.2]  # minutes

x = np.arange(len(metrics_time))
width = 0.35

ax1.bar(x - width/2, legacy_time, width, label='Legacy Paper / Manual', color='#EF4444', edgecolor='#FFFFFF', linewidth=0.7)
ax1.bar(x + width/2, stride_time, width, label='STRIDE™ Digital Gate', color='#10B981', edgecolor='#FFFFFF', linewidth=0.7)

ax1.set_title("Operational Speed (Minutes)", color='#F5C542', fontsize=11, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(metrics_time, color='#CBD5E1', fontsize=9, fontweight='bold')
ax1.set_ylabel("Minutes", color='#CBD5E1', fontsize=9)
ax1.tick_params(colors='#CBD5E1')
ax1.legend(facecolor='#081830', edgecolor='#475569', labelcolor='#FFFFFF', fontsize=8)
ax1.grid(axis='y', linestyle='--', alpha=0.15, color='#FFFFFF')

for i in x:
    ax1.text(i - width/2, legacy_time[i] + 4, f"{legacy_time[i]}m", ha='center', color='#FFFFFF', fontweight='bold', fontsize=8.5)
    ax1.text(i + width/2, stride_time[i] + 4, f"{stride_time[i]}m", ha='center', color='#34D399', fontweight='bold', fontsize=8.5)

# Subplot 2: Integrity & Compliance Rates (%)
ax2.set_facecolor('#0B1E38')
metrics_rate = ['Fraud / Ghost Claims', 'Statutory Audit Rating']
legacy_rate = [24, 52] # %
stride_rate = [0, 100] # %

ax2.bar(x - width/2, legacy_rate, width, label='Legacy Manual', color='#EF4444', edgecolor='#FFFFFF', linewidth=0.7)
ax2.bar(x + width/2, stride_rate, width, label='STRIDE™ Cryptographic', color='#00F2FE', edgecolor='#FFFFFF', linewidth=0.7)

ax2.set_title("Security & Compliance Rates (%)", color='#F5C542', fontsize=11, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(metrics_rate, color='#CBD5E1', fontsize=9, fontweight='bold')
ax2.set_ylabel("Percentage (%)", color='#CBD5E1', fontsize=9)
ax2.tick_params(colors='#CBD5E1')
ax2.legend(facecolor='#081830', edgecolor='#475569', labelcolor='#FFFFFF', fontsize=8)
ax2.grid(axis='y', linestyle='--', alpha=0.15, color='#FFFFFF')

for i in x:
    ax2.text(i - width/2, legacy_rate[i] + 2, f"{legacy_rate[i]}%", ha='center', color='#FFFFFF', fontweight='bold', fontsize=8.5)
    ax2.text(i + width/2, stride_rate[i] + 2, f"{stride_rate[i]}%", ha='center', color='#38BDF8', fontweight='bold', fontsize=8.5)

fig.suptitle("STRIDE™ BEFORE VS. AFTER BENCHMARK: 92% TIME SAVED, ZERO FRAUD",
             color='#FFFFFF', fontsize=12.5, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig("commercial_assets/case_study_operational_metrics.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved case_study_operational_metrics.png")

# ==============================================================================
# VISUAL 3: 6 SECTOR BLUEPRINT MAP
# ==============================================================================
fig, ax = plt.subplots(figsize=(10, 5.0), dpi=300)
fig.patch.set_facecolor('#081830')
ax.set_facecolor('#081830')
ax.axis('off')

ax.text(0.5, 0.94, "STRIDE™ MULTI-SECTOR COMMERCIAL BLUEPRINT ACROSS EAST AFRICA",
        color="#F5C542", fontsize=13, fontweight='bold', ha='center')

sectors = [
    ("1. TIER-1 SACCOs & AGMs", "1,500+ Delegates\nStatutory Quorum\nElectronic Ballots", "#00F2FE", 0.05, 0.50),
    ("2. TRADE UNIONS & DELEGATES", "2,500 Delegates\nPer-Diem Fraud Shield\nDual-Gate Floor", "#38BDF8", 0.36, 0.50),
    ("3. REGULATORY BODIES & CPD", "1,200 Professionals\nAnti-Pass Sharing\nDigital Certificates", "#10B981", 0.68, 0.50),
    ("4. INTER-BANK SPORTS", "679 Bank Athletes\n18 Sporting Venues\nCertified Units Payout", "#F5C542", 0.05, 0.10),
    ("5. COUNTY PUBLIC HEARINGS", "Constitutional Art 201\nCitizen Identity Verification\nAirtight Budget Dockets", "#A78BFA", 0.36, 0.10),
    ("6. VIP GOLF & CHARITY GALAS", "High-Net-Worth Guests\nInstant Revocation Passes\nZero Gatecrashing", "#EC4899", 0.68, 0.10)
]

for title, desc, col, x, y in sectors:
    rect = plt.Rectangle((x, y), 0.28, 0.35, transform=ax.transAxes,
                         facecolor='#0D2240', edgecolor=col, linewidth=1.8)
    ax.add_patch(rect)
    ax.text(x + 0.14, y + 0.28, title, color=col, fontsize=8.8, fontweight='bold', ha='center')
    ax.text(x + 0.14, y + 0.14, desc, color='#E2E8F0', fontsize=7.8, ha='center', multialignment='center')

plt.tight_layout()
plt.savefig("commercial_assets/case_study_sector_breakdown.png", dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
plt.close()
print("Saved case_study_sector_breakdown.png")

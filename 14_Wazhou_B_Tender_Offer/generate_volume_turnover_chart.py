#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wazhou B Trading Volume and Turnover Analysis
瓦轴B成交量和换手率分析
"""

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Configure font to support Chinese characters
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# Data
dates = [
    '2026-01-20',
    '2026-01-21',
]

# Trading volume (in lots, 1 lot = 100 shares)
volume_lots = [
    5796,   # 2026-01-20
    3994,   # 2026-01-21
]

# Trading volume (in shares)
volume_shares = [v * 100 for v in volume_lots]

# Trading amount (in 10,000 HKD)
trading_amount = [
    161.460,  # 2026-01-20 (万港元)
    111.467,  # 2026-01-21 (万港元)
]

# Turnover rate (%)
turnover_rate = [
    0.37,  # 2026-01-20
    0.25,  # 2026-01-21
]

# Price change (%)
price_change = [
    0.00,   # 2026-01-20
    -0.36,  # 2026-01-21
]

# Closing prices
closing_prices = [
    2.790,  # 2026-01-20
    2.780,  # 2026-01-21
]

# Convert date format
date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]

# Create figure with multiple subplots
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# ===== Subplot 1: Trading Volume (Shares) =====
ax1 = fig.add_subplot(gs[0, :])
bars1 = ax1.bar(date_objects, volume_shares, width=0.6, color='steelblue', alpha=0.7, label='成交量 (股)')

# Add value labels on bars
for i, (date, vol) in enumerate(zip(date_objects, volume_shares)):
    ax1.text(date, vol + 10000, f'{vol:,}股\n({volume_lots[i]:,}手)',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

ax1.set_ylabel('成交量 (股)', fontsize=12, fontweight='bold')
ax1.set_title('瓦轴B (200706) 每日成交量', fontsize=14, fontweight='bold', pad=15)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
ax1.legend(loc='upper right', fontsize=10)

# ===== Subplot 2: Trading Amount =====
ax2 = fig.add_subplot(gs[1, 0])
bars2 = ax2.bar(date_objects, trading_amount, width=0.6, color='orange', alpha=0.7, label='成交金额 (万港元)')

# Add value labels on bars
for i, (date, amount) in enumerate(zip(date_objects, trading_amount)):
    ax2.text(date, amount + 5, f'{amount:.2f}万\n港元',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

ax2.set_ylabel('成交金额 (万港元)', fontsize=12, fontweight='bold')
ax2.set_title('每日成交金额', fontsize=14, fontweight='bold', pad=15)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
ax2.legend(loc='upper right', fontsize=10)

# ===== Subplot 3: Turnover Rate =====
ax3 = fig.add_subplot(gs[1, 1])
bars3 = ax3.bar(date_objects, turnover_rate, width=0.6, color='green', alpha=0.7, label='换手率 (%)')

# Add value labels on bars
for i, (date, rate) in enumerate(zip(date_objects, turnover_rate)):
    ax3.text(date, rate + 0.01, f'{rate:.2f}%',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

ax3.set_ylabel('换手率 (%)', fontsize=12, fontweight='bold')
ax3.set_title('每日换手率', fontsize=14, fontweight='bold', pad=15)
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax3.grid(True, alpha=0.3, axis='y', linestyle='--')
ax3.legend(loc='upper right', fontsize=10)

# ===== Subplot 4: Price Change and Volume Correlation =====
ax4 = fig.add_subplot(gs[2, :])
ax4_twin = ax4.twinx()

# Bar chart for volume
bars4 = ax4.bar(date_objects, volume_lots, width=0.6, color='skyblue', alpha=0.6, label='成交量 (手)')

# Line chart for price change
line4 = ax4_twin.plot(date_objects, price_change, color='red', linewidth=3,
                      marker='o', markersize=10, label='涨跌幅 (%)')
ax4_twin.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# Add value labels
for i, (date, vol, change) in enumerate(zip(date_objects, volume_lots, price_change)):
    # Volume label
    ax4.text(date, vol + 100, f'{vol:,}',
             ha='center', va='bottom', fontsize=9, color='blue')
    # Price change label
    color = 'red' if change < 0 else 'green' if change > 0 else 'gray'
    ax4_twin.text(date, change + 0.05, f'{change:+.2f}%',
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color=color,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax4.set_xlabel('日期', fontsize=12, fontweight='bold')
ax4.set_ylabel('成交量 (手)', fontsize=12, fontweight='bold', color='blue')
ax4_twin.set_ylabel('涨跌幅 (%)', fontsize=12, fontweight='bold', color='red')
ax4.tick_params(axis='y', labelcolor='blue')
ax4_twin.tick_params(axis='y', labelcolor='red')

ax4.set_title('成交量与价格涨跌幅关联分析', fontsize=14, fontweight='bold', pad=15)
ax4.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax4.grid(True, alpha=0.3, axis='y', linestyle='--')

# Merge legends
lines, labels = ax4.get_legend_handles_labels()
lines2, labels2 = ax4_twin.get_legend_handles_labels()
ax4.legend(lines + lines2, labels + labels2, loc='upper right', fontsize=10)

# Add overall statistics text box
total_volume = sum(volume_shares)
total_amount = sum(trading_amount)
avg_turnover = np.mean(turnover_rate)
avg_price = np.mean(closing_prices)

stats_text = f'''统计区间: {dates[0]} 至 {dates[-1]}
累计成交量: {total_volume:,} 股 ({sum(volume_lots):,} 手)
累计成交额: {total_amount:.2f} 万港元
平均换手率: {avg_turnover:.2f}%
平均价格: {avg_price:.3f} 港元
总体趋势: 成交清淡，市场观望'''

props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, edgecolor='orange', linewidth=2)
fig.text(0.5, 0.95, stats_text, transform=fig.transFigure,
         fontsize=11, verticalalignment='top', horizontalalignment='center',
         bbox=props, family='monospace')

# Overall title
fig.suptitle('瓦轴B (200706) 交易活跃度分析\n2026年1月20-21日',
             fontsize=18, fontweight='bold', y=0.99)

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.93])

# Save figure
plt.savefig('reports/volume_turnover_chart.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("图表已保存: reports/volume_turnover_chart.png")
plt.close()

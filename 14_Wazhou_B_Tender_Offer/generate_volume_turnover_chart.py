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
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'DejaVu Sans', 'sans-serif']
plt.rcParams['font.monospace'] = ['WenQuanYi Zen Hei Mono', 'WenQuanYi Zen Hei', 'DejaVu Sans Mono']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 10

# Data
dates = [
    '2026-01-20', '2026-01-21', '2026-01-22', '2026-01-23',
    '2026-01-26', '2026-01-27', '2026-01-28', '2026-01-29',
    '2026-01-30', '2026-02-02', '2026-02-03', '2026-02-04',
    '2026-02-05', '2026-02-06', '2026-02-09', '2026-02-10',
    '2026-02-11', '2026-02-12', '2026-02-13', '2026-02-24',
    '2026-02-25', '2026-02-26', '2026-02-27',
]

# Trading volume (in lots, 1 lot = 100 shares)
volume_lots = [
    5796,   # 2026-01-20
    3994,   # 2026-01-21
    5994,   # 2026-01-22
    4042,   # 2026-01-23
    9914,   # 2026-01-26 (首次大幅放量)
    7208,   # 2026-01-27
    749,    # 2026-01-28 (历史最低!)
    7101,   # 2026-01-29
    4902,   # 2026-01-30
    6438,   # 2026-02-02
    3558,   # 2026-02-03
    3386,   # 2026-02-04
    2028,   # 2026-02-05
    7930,   # 2026-02-06 (二次大幅放量!)
    3213,   # 2026-02-09
    5631,   # 2026-02-10
    6072,   # 2026-02-11
    5576,   # 2026-02-12
    7447,   # 2026-02-13 (股价上涨，成交再度活跃!)
    6586,   # 2026-02-24
    5623,   # 2026-02-25 (价格回调，成交减少)
    9960,   # 2026-02-26 (成交量大幅激增!)
    15071,  # 2026-02-27 (成交量创新高!要约成功确认!)
]

# Trading volume (in shares)
volume_shares = [v * 100 for v in volume_lots]

# Trading amount (in 10,000 HKD)
trading_amount = [
    161.460,  # 2026-01-20
    111.467,  # 2026-01-21
    166.704,  # 2026-01-22
    112.436,  # 2026-01-23
    274.607,  # 2026-01-26 - 首次放量高峰
    199.703,  # 2026-01-27
    20.833,   # 2026-01-28 - 历史最低
    197.186,  # 2026-01-29
    135.862,  # 2026-01-30
    178.739,  # 2026-02-02
    99.074,   # 2026-02-03
    93.978,   # 2026-02-04
    56.247,   # 2026-02-05
    220.181,  # 2026-02-06 - 二次放量高峰
    89.200,   # 2026-02-09
    155.946,  # 2026-02-10
    168.163,  # 2026-02-11
    155.238,  # 2026-02-12
    208.182,  # 2026-02-13
    184.477,  # 2026-02-24
    156.286,  # 2026-02-25
    276.686,  # 2026-02-26 - 三次放量高峰!
    424.912,  # 2026-02-27 - 四次放量创新高!
]

# Turnover rate (%)
turnover_rate = [
    0.37,  # 2026-01-20
    0.25,  # 2026-01-21
    0.38,  # 2026-01-22
    0.25,  # 2026-01-23
    0.63,  # 2026-01-26
    0.45,  # 2026-01-27
    0.05,  # 2026-01-28 (历史最低)
    0.45,  # 2026-01-29
    0.31,  # 2026-01-30
    0.41,  # 2026-02-02
    0.22,  # 2026-02-03
    0.21,  # 2026-02-04
    0.13,  # 2026-02-05
    0.50,  # 2026-02-06 (二次高峰)
    0.20,  # 2026-02-09
    0.36,  # 2026-02-10
    0.38,  # 2026-02-11
    0.35,  # 2026-02-12
    0.47,  # 2026-02-13
    0.42,  # 2026-02-24
    0.36,  # 2026-02-25
    0.63,  # 2026-02-26 (三次高峰!)
    0.95,  # 2026-02-27 (四次高峰创新高!)
]

# Price change (%)
price_change = [
    0.00,   # 2026-01-20
    -0.36,  # 2026-01-21
    0.36,   # 2026-01-22
    0.00,   # 2026-01-23
    -0.72,  # 2026-01-26 (最大跌幅)
    0.36,   # 2026-01-27
    0.36,   # 2026-01-28
    -0.36,  # 2026-01-29
    -0.36,  # 2026-01-30
    0.00,   # 2026-02-02
    0.36,   # 2026-02-03
    -0.36,  # 2026-02-04
    0.36,   # 2026-02-05
    0.00,   # 2026-02-06
    -0.36,  # 2026-02-09
    0.00,   # 2026-02-10
    0.36,   # 2026-02-11
    0.36,   # 2026-02-12
    0.72,   # 2026-02-13 (最大涨幅!)
    0.00,   # 2026-02-24
    -2.14,  # 2026-02-25 (最大跌幅!)
    1.09,   # 2026-02-26 (反弹)
    0.72,   # 2026-02-27 (继续上涨)
]

# Closing prices
closing_prices = [
    2.790,  # 2026-01-20
    2.780,  # 2026-01-21
    2.790,  # 2026-01-22
    2.790,  # 2026-01-23
    2.770,  # 2026-01-26
    2.780,  # 2026-01-27
    2.790,  # 2026-01-28
    2.780,  # 2026-01-29
    2.770,  # 2026-01-30
    2.770,  # 2026-02-02
    2.780,  # 2026-02-03
    2.770,  # 2026-02-04
    2.780,  # 2026-02-05
    2.780,  # 2026-02-06
    2.770,  # 2026-02-09
    2.770,  # 2026-02-10
    2.780,  # 2026-02-11
    2.790,  # 2026-02-12
    2.810,  # 2026-02-13 (新高！)
    2.810,  # 2026-02-24
    2.750,  # 2026-02-25 (回调)
    2.780,  # 2026-02-26 (反弹)
    2.800,  # 2026-02-27 (继续上涨)
]

# Convert date format for labels
date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
date_labels = [d.strftime('%m/%d') for d in date_objects]

# Use integer indices for x-axis
x_indices = list(range(len(dates)))

# Create figure with multiple subplots
fig = plt.figure(figsize=(16, 12))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# ===== Subplot 1: Trading Volume (Shares) =====
ax1 = fig.add_subplot(gs[0, :])
bars1 = ax1.bar(x_indices, volume_shares, width=0.8, color='steelblue', alpha=0.7, label='成交量 (股)')

# Add value labels on bars
for i, vol in enumerate(volume_shares):
    ax1.text(i, vol + 10000, f'{vol:,}股\n({volume_lots[i]:,}手)',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

ax1.set_ylabel('成交量 (股)', fontsize=12, fontweight='bold')
ax1.set_title('瓦轴B (200706) 每日成交量', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x_indices)
ax1.set_xticklabels(date_labels, rotation=45, ha='right')
ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
ax1.legend(loc='upper right', fontsize=10)

# ===== Subplot 2: Trading Amount =====
ax2 = fig.add_subplot(gs[1, 0])
bars2 = ax2.bar(x_indices, trading_amount, width=0.8, color='orange', alpha=0.7, label='成交金额 (万港元)')

# Add value labels on bars
for i, amount in enumerate(trading_amount):
    ax2.text(i, amount + 5, f'{amount:.2f}万\n港元',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

ax2.set_ylabel('成交金额 (万港元)', fontsize=12, fontweight='bold')
ax2.set_title('每日成交金额', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x_indices)
ax2.set_xticklabels(date_labels, rotation=45, ha='right')
ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
ax2.legend(loc='upper right', fontsize=10)

# ===== Subplot 3: Turnover Rate =====
ax3 = fig.add_subplot(gs[1, 1])
bars3 = ax3.bar(x_indices, turnover_rate, width=0.8, color='green', alpha=0.7, label='换手率 (%)')

# Add value labels on bars
for i, rate in enumerate(turnover_rate):
    ax3.text(i, rate + 0.01, f'{rate:.2f}%',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

ax3.set_ylabel('换手率 (%)', fontsize=12, fontweight='bold')
ax3.set_title('每日换手率', fontsize=14, fontweight='bold', pad=15)
ax3.set_xticks(x_indices)
ax3.set_xticklabels(date_labels, rotation=45, ha='right')
ax3.grid(True, alpha=0.3, axis='y', linestyle='--')
ax3.legend(loc='upper right', fontsize=10)

# ===== Subplot 4: Price Change and Volume Correlation =====
ax4 = fig.add_subplot(gs[2, :])
ax4_twin = ax4.twinx()

# Bar chart for volume
bars4 = ax4.bar(x_indices, volume_lots, width=0.8, color='skyblue', alpha=0.6, label='成交量 (手)')

# Line chart for price change
line4 = ax4_twin.plot(x_indices, price_change, color='red', linewidth=3,
                      marker='o', markersize=10, label='涨跌幅 (%)')
ax4_twin.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# Add value labels
for i, (vol, change) in enumerate(zip(volume_lots, price_change)):
    # Volume label
    ax4.text(i, vol + 100, f'{vol:,}',
             ha='center', va='bottom', fontsize=9, color='blue')
    # Price change label
    color = 'red' if change < 0 else 'green' if change > 0 else 'gray'
    ax4_twin.text(i, change + 0.05, f'{change:+.2f}%',
                 ha='center', va='bottom', fontsize=10, fontweight='bold', color=color,
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

ax4.set_xlabel('日期', fontsize=12, fontweight='bold')
ax4.set_ylabel('成交量 (手)', fontsize=12, fontweight='bold', color='blue')
ax4_twin.set_ylabel('涨跌幅 (%)', fontsize=12, fontweight='bold', color='red')
ax4.tick_params(axis='y', labelcolor='blue')
ax4_twin.tick_params(axis='y', labelcolor='red')

ax4.set_title('成交量与价格涨跌幅关联分析', fontsize=14, fontweight='bold', pad=15)
ax4.set_xticks(x_indices)
ax4.set_xticklabels(date_labels, rotation=45, ha='right')
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
fig.suptitle('瓦轴B (200706) 交易活跃度分析\n2026年1月20日-2月26日',
             fontsize=18, fontweight='bold', y=0.99)

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.93])

# Save figure
plt.savefig('reports/volume_turnover_chart.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("图表已保存: reports/volume_turnover_chart.png")
plt.close()

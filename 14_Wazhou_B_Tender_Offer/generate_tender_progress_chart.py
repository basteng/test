#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wazhou B Tender Offer Progress Visualization
瓦轴B要约收购进展可视化
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
    '2026-01-20',
    '2026-01-21',
    '2026-01-22',
    '2026-01-23',
    '2026-01-26',
    '2026-01-27',
    '2026-01-28',
    '2026-01-29',
    '2026-01-30',
    '2026-02-02',
    '2026-02-03',
    '2026-02-04',
    '2026-02-05',
    '2026-02-06',
    '2026-02-09',
]

# Cumulative net accepted shares (流通股)
cumulative_shares = [
    2092729,   # 2026-01-20
    2487296,   # 2026-01-21
    2886990,   # 2026-01-22
    3516667,   # 2026-01-23
    4611954,   # 2026-01-26 (首次突破100万单日增长)
    5224122,   # 2026-01-27
    5393909,   # 2026-01-28
    5667078,   # 2026-01-29
    5894954,   # 2026-01-30
    6402215,   # 2026-02-02 (突破4%)
    6694900,   # 2026-02-03
    8357146,   # 2026-02-04 (大幅跳升，突破5%!)
    9653603,   # 2026-02-05 (突破6%，突破960万!)
    10898425,  # 2026-02-06 (持续增长，接近1100万!)
    11699837,  # 2026-02-09 (突破7%，接近1170万!)
]

# Completion ratio
completion_ratio = [
    1.32,      # 2026-01-20
    1.568,     # 2026-01-21
    1.82,      # 2026-01-22
    2.217,     # 2026-01-23
    2.908,     # 2026-01-26
    3.294,     # 2026-01-27
    3.401,     # 2026-01-28
    3.573,     # 2026-01-29
    3.717,     # 2026-01-30
    4.037,     # 2026-02-02 (突破4%)
    4.221,     # 2026-02-03
    5.269,     # 2026-02-04 (突破5%)
    6.087,     # 2026-02-05 (突破6%!)
    6.872,     # 2026-02-06 (接近7%)
    7.377,     # 2026-02-09 (突破7%!)
]

# Number of shareholders
shareholders = [
    33,        # 2026-01-20
    59,        # 2026-01-21
    74,        # 2026-01-22
    96,        # 2026-01-23
    142,       # 2026-01-26
    172,       # 2026-01-27
    189,       # 2026-01-28
    199,       # 2026-01-29
    223,       # 2026-01-30
    247,       # 2026-02-02
    266,       # 2026-02-03
    289,       # 2026-02-04
    313,       # 2026-02-05
    343,       # 2026-02-06
    424,       # 2026-02-09
]

# Convert date format
date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]

# Target shares (预定收购股份数)
target_shares = 158600000

# Create figure with two subplots
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.3)

# ===== Subplot 1: Cumulative Shares and Completion Ratio =====
ax1 = fig.add_subplot(gs[0])
ax1_right = ax1.twinx()

# Set colors
color_shares = '#1f77b4'
color_ratio = '#ff7f0e'
color_target = '#d62728'

# Left axis - Shares
ax1.set_ylabel('累计预受股份数', color=color_shares, fontsize=12, fontweight='bold')
line1 = ax1.plot(date_objects, cumulative_shares, color=color_shares,
                 linewidth=3, marker='o', markersize=10,
                 label='累计预受股份', zorder=3)
ax1.tick_params(axis='y', labelcolor=color_shares)
ax1.grid(True, alpha=0.3, linestyle='--')

# Add target line
line_target = ax1.axhline(y=target_shares, color=color_target,
                          linestyle='--', linewidth=2,
                          label=f'预定收购目标 ({target_shares:,}股)', zorder=2)

# Fill area - Completed portion
ax1.fill_between(date_objects, 0, cumulative_shares,
                 alpha=0.2, color=color_shares, label='已完成区域')

# Right axis - Completion ratio
ax1_right.set_ylabel('完成比例 (%)', color=color_ratio, fontsize=12, fontweight='bold')
line2 = ax1_right.plot(date_objects, completion_ratio, color=color_ratio,
                       linewidth=3, marker='s', markersize=10,
                       label='完成百分比', linestyle='--', zorder=3)
ax1_right.tick_params(axis='y', labelcolor=color_ratio)

# Set y-axis range
ax1.set_ylim([0, target_shares * 1.1])
ax1_right.set_ylim([0, 100])

# Format left axis tick labels
def shares_formatter(x, pos):
    if x >= 1000000:
        return f'{x/1000000:.1f}M'
    elif x >= 1000:
        return f'{x/1000:.0f}K'
    else:
        return f'{x:.0f}'
ax1.yaxis.set_major_formatter(plt.FuncFormatter(shares_formatter))

# Add data labels
for i, (date, shares, ratio) in enumerate(zip(date_objects, cumulative_shares, completion_ratio)):
    # Shares label
    ax1.annotate(f'{shares:,}股\n({ratio}%)',
                xy=(date, shares),
                xytext=(0, 15),
                textcoords='offset points',
                ha='center',
                fontsize=10,
                fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))

# Format x-axis dates
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax1.set_xlabel('日期', fontsize=12, fontweight='bold')

# Title
ax1.set_title('瓦轴B (200706) 要约收购进展\n2026年1月20日-2月9日',
              fontsize=16, fontweight='bold', pad=20)

# Merge legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax1_right.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2,
          loc='upper left', fontsize=10, framealpha=0.9)

# ===== Subplot 2: Number of Shareholders =====
ax2 = fig.add_subplot(gs[1])

# Bar chart for shareholders
bars = ax2.bar(date_objects, shareholders, width=0.5, color='#2ca02c', alpha=0.7, label='预受股东户数')

# Add value labels on bars
for i, (date, count) in enumerate(zip(date_objects, shareholders)):
    ax2.text(date, count + 1, f'{count}户', ha='center', va='bottom', fontsize=11, fontweight='bold')

# Format axes
ax2.set_ylabel('股东户数', fontsize=12, fontweight='bold')
ax2.set_xlabel('日期', fontsize=12, fontweight='bold')
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
ax2.legend(loc='upper left', fontsize=10)

# Set title
ax2.set_title('预受要约股东户数变化', fontsize=14, fontweight='bold', pad=15)

# Add statistics text box
stats_text = f'''最新数据 ({dates[-1]}):
预受股份: {cumulative_shares[-1]:,} 股
完成比例: {completion_ratio[-1]}%
参与股东: {shareholders[-1]} 户
距离目标: {target_shares - cumulative_shares[-1]:,} 股
还需完成: {100 - completion_ratio[-1]:.2f}%
⚠️ 2月4-5日加速！单日新增超130万股'''

props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
ax1.text(0.98, 0.02, stats_text, transform=ax1.transAxes,
         fontsize=11, verticalalignment='bottom', horizontalalignment='right',
         bbox=props, family='monospace')

# Adjust layout
plt.tight_layout()

# Save chart
plt.savefig('reports/tender_offer_progress_chart.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("图表已保存: reports/tender_offer_progress_chart.png")
plt.close()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wazhou B Stock Price vs Tender Offer Shares
瓦轴B股价与要约收购股份对比
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

# Data - trading days
dates = [
    '2026-01-20', '2026-01-21', '2026-01-22', '2026-01-23',
    '2026-01-26', '2026-01-27', '2026-01-28', '2026-01-29',
    '2026-01-30', '2026-02-02', '2026-02-03', '2026-02-04',
    '2026-02-05', '2026-02-06', '2026-02-09', '2026-02-10',
    '2026-02-11', '2026-02-12', '2026-02-13', '2026-02-24',
    '2026-02-25', '2026-02-26', '2026-02-27',
]

# Closing prices (HKD)
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
    2.810,  # 2026-02-13 (新高！接近要约价)
    2.810,  # 2026-02-24 (维持高位)
    2.750,  # 2026-02-25 (回调-2.14%，但要约进展大幅突破！)
    2.780,  # 2026-02-26 (反弹+1.09%)
    2.800,  # 2026-02-27 (继续上涨+0.72%，要约成功确认！)
]

# Opening prices (HKD)
opening_prices = [
    2.790,  # 2026-01-20
    2.790,  # 2026-01-21
    2.790,  # 2026-01-22
    2.780,  # 2026-01-23
    2.780,  # 2026-01-26
    2.760,  # 2026-01-27
    2.770,  # 2026-01-28
    2.780,  # 2026-01-29
    2.780,  # 2026-01-30
    2.770,  # 2026-02-02
    2.780,  # 2026-02-03
    2.780,  # 2026-02-04
    2.770,  # 2026-02-05
    2.770,  # 2026-02-06 (修正)
    2.780,  # 2026-02-09
    2.780,  # 2026-02-10
    2.760,  # 2026-02-11
    2.780,  # 2026-02-12
    2.780,  # 2026-02-13
    2.800,  # 2026-02-24
    2.800,  # 2026-02-25
    2.750,  # 2026-02-26
    2.780,  # 2026-02-27
]

# Highest prices (HKD)
high_prices = [
    2.790,  # 2026-01-20
    2.800,  # 2026-01-21
    2.790,  # 2026-01-22
    2.790,  # 2026-01-23
    2.780,  # 2026-01-26
    2.780,  # 2026-01-27
    2.790,  # 2026-01-28
    2.790,  # 2026-01-29
    2.780,  # 2026-01-30
    2.790,  # 2026-02-02
    2.790,  # 2026-02-03
    2.790,  # 2026-02-04
    2.780,  # 2026-02-05
    2.790,  # 2026-02-06 (修正)
    2.790,  # 2026-02-09
    2.780,  # 2026-02-10
    2.780,  # 2026-02-11
    2.790,  # 2026-02-12
    2.810,  # 2026-02-13
    2.820,  # 2026-02-24
    2.800,  # 2026-02-25
    2.790,  # 2026-02-26
    2.800,  # 2026-02-27
]

# Lowest prices (HKD)
low_prices = [
    2.780,  # 2026-01-20
    2.780,  # 2026-01-21
    2.770,  # 2026-01-22
    2.780,  # 2026-01-23
    2.760,  # 2026-01-26
    2.760,  # 2026-01-27
    2.770,  # 2026-01-28
    2.780,  # 2026-01-29
    2.760,  # 2026-01-30
    2.770,  # 2026-02-02
    2.780,  # 2026-02-03
    2.770,  # 2026-02-04
    2.770,  # 2026-02-05
    2.760,  # 2026-02-06 (修正)
    2.770,  # 2026-02-09
    2.760,  # 2026-02-10
    2.760,  # 2026-02-11
    2.780,  # 2026-02-12
    2.780,  # 2026-02-13
    2.800,  # 2026-02-24
    2.750,  # 2026-02-25
    2.750,  # 2026-02-26
    2.780,  # 2026-02-27
]

# Completion ratio (from tender offer data)
completion_ratio = [
    1.32,    # 2026-01-20
    1.568,   # 2026-01-21
    1.82,    # 2026-01-22
    2.217,   # 2026-01-23
    2.908,   # 2026-01-26
    3.294,   # 2026-01-27
    3.401,   # 2026-01-28
    3.573,   # 2026-01-29
    3.717,   # 2026-01-30
    4.037,   # 2026-02-02
    4.221,   # 2026-02-03
    5.269,   # 2026-02-04
    6.087,   # 2026-02-05
    6.872,   # 2026-02-06
    7.377,   # 2026-02-09
    8.022,   # 2026-02-10
    9.477,   # 2026-02-11
    11.274,  # 2026-02-12
    11.402,  # 2026-02-13
    13.669,  # 2026-02-24 (使用前一日数据)
    20.595,  # 2026-02-25 (历史性突破!)
    31.156,  # 2026-02-26 (再创新高!超过最低门槛!)
    34.379,  # 2026-02-27 (确认成功!完成最低门槛139.6%!)
]

# Cumulative accepted shares
cumulative_shares = [
    2092729,   # 2026-01-20
    2487296,   # 2026-01-21
    2886990,   # 2026-01-22
    3516667,   # 2026-01-23
    4611954,   # 2026-01-26
    5224122,   # 2026-01-27
    5393909,   # 2026-01-28
    5667078,   # 2026-01-29
    5894954,   # 2026-01-30
    6402215,   # 2026-02-02
    6694900,   # 2026-02-03
    8357146,   # 2026-02-04
    9653603,   # 2026-02-05
    10898425,  # 2026-02-06
    11699837,  # 2026-02-09
    12723122,  # 2026-02-10
    15030921,  # 2026-02-11
    17880621,  # 2026-02-12
    18083941,  # 2026-02-13
    21679119,  # 2026-02-24 (使用前一日数据)
    32663634,  # 2026-02-25 (历史性突破!)
    49413439,  # 2026-02-26 (再创新高!单日+1675万!)
    54524555,  # 2026-02-27 (确认成功!累计5452万股!)
]

# Tender offer price reference line
tender_offer_price = 2.86

# Convert date format
date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]

# Create figure and axes
fig, ax1 = plt.subplots(figsize=(16, 9))
ax2 = ax1.twinx()

# Plot stock closing price on left axis
line1 = ax1.plot(date_objects, closing_prices, 'b-', linewidth=3, marker='o',
                 markersize=10, label='收盘价')
# Plot high and low prices
ax1.fill_between(date_objects, low_prices, high_prices, alpha=0.2, color='blue', label='价格区间 (最高-最低)')

# Add tender offer price reference line
line_tender = ax1.axhline(y=tender_offer_price, color='r', linestyle='--',
                          linewidth=2.5, alpha=0.8, label=f'要约收购价 ({tender_offer_price} 港元)')

# Plot completion ratio on right axis
line2 = ax2.plot(date_objects, completion_ratio, 'g-', linewidth=3, marker='s',
                 markersize=10, label='完成比例')

# Add data labels for stock price
for i in range(len(date_objects)):
    # Closing price label
    ax1.annotate(f'{closing_prices[i]:.3f} 港元',
                xy=(date_objects[i], closing_prices[i]),
                xytext=(0, -25),
                textcoords='offset points',
                ha='center',
                fontsize=10,
                fontweight='bold',
                color='blue',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='lightblue', alpha=0.8, edgecolor='blue'))

# Add data labels for completion ratio
for i in range(len(date_objects)):
    ax2.annotate(f'{completion_ratio[i]:.2f}%\n{cumulative_shares[i]:,}股',
                xy=(date_objects[i], completion_ratio[i]),
                xytext=(0, 15),
                textcoords='offset points',
                ha='center',
                fontsize=10,
                fontweight='bold',
                color='green',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen', alpha=0.8, edgecolor='green'))

# Set labels
ax1.set_xlabel('日期', fontsize=12, fontweight='bold')
ax1.set_ylabel('股价 (港元)', fontsize=12, fontweight='bold', color='b')
ax2.set_ylabel('完成比例 (%)', fontsize=12, fontweight='bold', color='g')

# Color the tick labels
ax1.tick_params(axis='y', labelcolor='b')
ax2.tick_params(axis='y', labelcolor='g')

# Set y-axis limits
ax1.set_ylim([2.70, 2.90])
ax2.set_ylim([0, 25])

# Format y-axis for percentage
def percentage_formatter(x, pos):
    return f'{x:.1f}%'
ax2.yaxis.set_major_formatter(plt.FuncFormatter(percentage_formatter))

# Format x-axis dates
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=0, ha='center')

# Add annotation for price discount to tender offer price
latest_price = closing_prices[-1]
discount = (tender_offer_price - latest_price) / tender_offer_price * 100
ax1.annotate(f'较要约价折价: {discount:.2f}%',
             xy=(date_objects[-1], latest_price),
             xytext=(date_objects[-1], 2.82),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.9),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2',
                           color='red', lw=2),
             fontsize=11, fontweight='bold', ha='center')

# Title
plt.title('瓦轴B (200706) 股价走势与要约收购进展对比\n2026年1月20日-2月26日',
          fontsize=16, fontweight='bold', pad=20)

# Merge legends
lines = line1 + [line_tender] + line2
labels = [l.get_label() for l in lines]
# Also add fill_between to legend
from matplotlib.patches import Patch
lines.append(Patch(facecolor='blue', alpha=0.2))
labels.append('价格区间 (最高-最低)')
ax1.legend(lines, labels, loc='upper left', fontsize=10, framealpha=0.9)

# Add grid
ax1.grid(True, alpha=0.3)

# Add statistics text box
premium = ((tender_offer_price - latest_price) / latest_price * 100)
stats_text = f'''最新数据 ({dates[-1]}):
收盘价: {latest_price:.3f} 港元
要约价: {tender_offer_price} 港元
溢价空间: {premium:.2f}%
完成比例: {completion_ratio[-1]:.2f}%
预受股份: {cumulative_shares[-1]:,} 股'''

props = dict(boxstyle='round', facecolor='wheat', alpha=0.9)
ax1.text(0.98, 0.02, stats_text, transform=ax1.transAxes,
         fontsize=11, verticalalignment='bottom', horizontalalignment='right',
         bbox=props, family='monospace')

# Adjust layout
plt.tight_layout()

# Save figure
plt.savefig('reports/stock_price_vs_shares_chart.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("图表已保存: reports/stock_price_vs_shares_chart.png")
plt.close()

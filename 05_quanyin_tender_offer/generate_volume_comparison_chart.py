#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quanyin High-Tech Daily Trading Volume vs Tender Offer Net Increase
"""

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Data - only trading days
dates = [
    '2025-12-08',
    '2025-12-09',
    '2025-12-10',
    '2025-12-11',
    '2025-12-12',
    '2025-12-15',
    '2025-12-16',
    '2025-12-17',
    '2025-12-18',
    '2025-12-19',
    '2025-12-22',
    '2025-12-23',
    '2025-12-24',
    '2025-12-25',
    '2025-12-26',
    '2025-12-29',
    '2025-12-30',
    '2025-12-31',
    '2026-01-05'
]

# Daily trading volume in shares (1手 = 100股)
# Actual data from market screenshots
daily_trading_volume = [
    3334000,   # 12-08 actual (33.34万手)
    2776000,   # 12-09 actual (27.76万手)
    2754000,   # 12-10 interpolated
    2733000,   # 12-11 actual (27.33万手)
    2600000,   # 12-12 interpolated
    2450000,   # 12-15 interpolated
    2320000,   # 12-16 interpolated
    2188000,   # 12-17 actual (21.88万手)
    2250000,   # 12-18 interpolated
    2300000,   # 12-19 interpolated
    2382000,   # 12-22 actual (23.82万手)
    2400000,   # 12-23 interpolated
    2450000,   # 12-24 interpolated
    2500000,   # 12-25 interpolated
    2397000,   # 12-26 actual (23.97万手)
    2450000,   # 12-29 estimated
    3989770,   # 12-30 actual (39.8977万手)
    5135110,   # 12-31 actual (51.3511万手)
    6379720    # 01-05 actual (63.7972万手) FINAL
]

# Daily net increase in tender offer shares
# Calculated from the tender offer tracking data
daily_tender_net_increase = [
    3270280,    # 12-08: +3,270,280
    393570,     # 12-09: +393,570
    541083,     # 12-10: +541,083
    290758,     # 12-11: +290,758
    810460,     # 12-12: +810,460
    1550830,    # 12-15: +1,550,830
    1986848,    # 12-16: +1,986,848
    2782160,    # 12-17: +2,782,160
    -1903100,   # 12-18: -1,903,100 (withdrawal)
    347208,     # 12-19: +347,208
    1617426,    # 12-22: +1,617,426
    145360,     # 12-23: +145,360
    411000,     # 12-24: +411,000
    4020160,    # 12-25: +4,020,160
    78900,      # 12-26: +78,900
    4817382,    # 12-29: +4,817,382
    10714412,   # 12-30: +10,714,412
    12629572,   # 12-31: +12,629,572
    172484564   # 01-05: +172,484,564 (FINAL! UNPRECEDENTED! 13.66x prev record!)
]

# Closing prices - all actual data from market
# Source: Stock exchange data screenshot
closing_prices = [
    11.50,  # 12-08
    11.46,  # 12-09
    11.51,  # 12-10
    11.44,  # 12-11
    11.37,  # 12-12
    11.34,  # 12-15
    11.31,  # 12-16
    11.31,  # 12-17
    11.36,  # 12-18
    11.41,  # 12-19
    11.45,  # 12-22
    11.47,  # 12-23
    11.58,  # 12-24
    11.57,  # 12-25
    11.53,  # 12-26
    11.62,  # 12-29
    11.54,  # 12-30
    11.68,  # 12-31
    11.69   # 01-05 (FINAL)
]

# Convert date format
date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]

# Create figure with larger size
fig, ax1 = plt.subplots(figsize=(16, 9))
ax2 = ax1.twinx()
ax3 = ax1.twinx()  # Third axis for stock price

# Offset the right spine of ax3
ax3.spines['right'].set_position(('outward', 60))

# Create bar chart for daily trading volume on left axis
bar_width = 0.4
positions = np.arange(len(date_objects))
bars1 = ax1.bar(positions - bar_width/2, daily_trading_volume, bar_width,
                label='Daily Trading Volume', color='steelblue', alpha=0.7)

# Create bar chart for tender offer net increase on right axis
bars2 = ax2.bar(positions + bar_width/2, daily_tender_net_increase, bar_width,
                label='Tender Offer Net Increase', color='coral', alpha=0.7)

# Add stock price line on third axis
line3 = ax3.plot(positions, closing_prices, 'purple', linewidth=3, marker='D',
                 markersize=7, label='Stock Price', zorder=5)

# Set labels
ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
ax1.set_ylabel('Daily Trading Volume (shares)', fontsize=12, fontweight='bold', color='steelblue')
ax2.set_ylabel('Tender Offer Net Increase (shares)', fontsize=12, fontweight='bold', color='coral')
ax3.set_ylabel('Stock Price (CNY)', fontsize=12, fontweight='bold', color='purple')

# Color the tick labels
ax1.tick_params(axis='y', labelcolor='steelblue')
ax2.tick_params(axis='y', labelcolor='coral')
ax3.tick_params(axis='y', labelcolor='purple')

# Format y-axis for millions
def millions_formatter(x, pos):
    return f'{x/1000000:.1f}M'
ax1.yaxis.set_major_formatter(plt.FuncFormatter(millions_formatter))
ax2.yaxis.set_major_formatter(plt.FuncFormatter(millions_formatter))

# Set y-axis limits
ax1.set_ylim([0, 7000000])  # Increased to accommodate 01-05's trading volume 6.38M
ax2.set_ylim([-2500000, 180000000])  # Increased to accommodate 01-05's UNPRECEDENTED 172.48M!
ax3.set_ylim([11.0, 12.0])

# Add zero line for right axis
ax2.axhline(y=0, color='gray', linestyle='-', linewidth=1, alpha=0.5)

# Add tender offer price reference line on stock price axis
ax3.axhline(y=11.85, color='red', linestyle='--', linewidth=2, alpha=0.5,
            label='Tender Price (11.85)', zorder=4)

# Format x-axis
ax1.set_xticks(positions)
ax1.set_xticklabels([d.strftime('%m-%d') for d in date_objects], rotation=45, ha='right')

# Add data labels on bars and stock price
for i, (v1, v2, price) in enumerate(zip(daily_trading_volume, daily_tender_net_increase, closing_prices)):
    # Trading volume labels (in millions) - show every other
    if i % 2 == 0:
        ax1.text(i - bar_width/2, v1 + 100000, f'{v1/1000000:.2f}M',
                ha='center', va='bottom', fontsize=7, color='steelblue', rotation=0)

    # Tender offer labels (in millions) - show every other
    if i % 2 == 1:
        if v2 >= 0:
            ax2.text(i + bar_width/2, v2 + 100000, f'+{v2/1000000:.2f}M',
                    ha='center', va='bottom', fontsize=7, color='coral', rotation=0)
        else:
            ax2.text(i + bar_width/2, v2 - 100000, f'{v2/1000000:.2f}M',
                    ha='center', va='top', fontsize=7, color='red', rotation=0)

    # Stock price labels - show every other
    if i % 2 == 0:
        ax3.annotate(f'{price:.2f}',
                    xy=(i, price),
                    xytext=(0, 8),
                    textcoords='offset points',
                    ha='center',
                    fontsize=7,
                    color='purple',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7, edgecolor='purple'))

# Highlight special events
# FINAL UNPRECEDENTED explosion on 01-05
final_idx = 18
ax2.annotate('FINAL! UNPRECEDENTED!\n+172.48M shares\n13.66x prev record!\n(01-05)',
             xy=(final_idx + bar_width/2, daily_tender_net_increase[final_idx]),
             xytext=(final_idx-1, 160000000),  # Upper right
             bbox=dict(boxstyle='round,pad=0.5', facecolor='gold', alpha=0.98),
             arrowprops=dict(arrowstyle='->', color='red', lw=3),
             fontsize=12, fontweight='bold', ha='center')

# Previous record on 12-31
prev_record_idx = 17
ax2.annotate('Prev Record\n+12.63M\n(12-31)',
             xy=(prev_record_idx + bar_width/2, daily_tender_net_increase[prev_record_idx]),
             xytext=(prev_record_idx-1.5, 20000000),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8),
             arrowprops=dict(arrowstyle='->', color='orange', lw=1.5),
             fontsize=9, ha='center')

# Sharp drop on 12-18
drop_idx = 8
ax2.annotate('Withdrawal\n-1.90M shares',
             xy=(drop_idx + bar_width/2, daily_tender_net_increase[drop_idx]),
             xytext=(drop_idx, -2200000),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral', alpha=0.9),
             arrowprops=dict(arrowstyle='->', color='red', lw=2),
             fontsize=9, ha='center')

# Title
plt.title('Quanyin High-Tech (300087) Trading Volume, Tender Offer & Stock Price\nDecember 8, 2025 - January 5, 2026',
          fontsize=16, fontweight='bold', pad=20)

# Merge legends from all three axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax1.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3,
          loc='upper left', fontsize=10, framealpha=0.9)

# Add grid for better readability
ax1.grid(True, alpha=0.3, axis='y')

# Add statistics text box
avg_volume = np.mean(daily_trading_volume)
avg_tender = np.mean([x for x in daily_tender_net_increase if x > 0])  # Average of positive values
total_tender = sum(daily_tender_net_increase)
avg_price = np.mean(closing_prices)
price_change = closing_prices[-1] - closing_prices[0]

stats_text = f'''FINAL Summary (Dec 8 - Jan 5):
Avg Trading: {avg_volume/1000000:.2f}M shares/day
Avg Tender+: {avg_tender/1000000:.2f}M shares/day
Total Net+: {total_tender/1000000:.2f}M shares
Tender/Trade: {(avg_tender/avg_volume*100):.1f}%
Avg Price: {avg_price:.2f} CNY
Price Change: {price_change:+.2f} CNY
01-05 FINAL: +172.48M shares!'''

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax1.text(0.50, 0.95, stats_text, transform=ax1.transAxes,  # Upper middle (higher)
         fontsize=10, verticalalignment='top', horizontalalignment='center',
         bbox=props, family='monospace')

# Adjust layout
plt.tight_layout()

# Save figure
plt.savefig('reports/volume_comparison_chart.png',
            dpi=300, bbox_inches='tight')
print("Chart saved: reports/volume_comparison_chart.png")

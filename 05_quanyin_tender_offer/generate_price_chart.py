#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quanyin High-Tech Stock Price vs Tender Offer Shares
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
    '2025-12-26'
]

# Closing prices (actual + interpolated for missing dates)
# Actual prices: 12-08: 11.50, 12-09: 11.46, 12-17: 11.31, 12-19: 11.41, 12-22: 11.45, 12-26: 11.53
# Interpolated for: 12-10, 12-11, 12-12, 12-15, 12-16, 12-18, 12-23, 12-24, 12-25
closing_prices = [
    11.50,  # 12-08 actual
    11.46,  # 12-09 actual
    11.42,  # 12-10 interpolated
    11.38,  # 12-11 interpolated
    11.35,  # 12-12 interpolated
    11.33,  # 12-15 interpolated
    11.32,  # 12-16 interpolated
    11.31,  # 12-17 actual
    11.36,  # 12-18 interpolated
    11.41,  # 12-19 actual
    11.45,  # 12-22 actual
    11.47,  # 12-23 interpolated
    11.49,  # 12-24 interpolated
    11.51,  # 12-25 interpolated
    11.53   # 12-26 actual
]

# Cumulative net accepted shares (from tender offer data)
cumulative_shares = [
    84069050,
    84462620,
    85003703,
    85294461,
    86104921,
    87655751,
    89642599,
    92424759,
    90521659,
    90868867,
    92486293,
    92631653,
    93042653,
    97062813,
    97141713
]

# Tender offer price reference line
tender_offer_price = 11.85

# Convert date format
date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]

# Create figure and axes
fig, ax1 = plt.subplots(figsize=(14, 8))
ax2 = ax1.twinx()

# Plot stock closing price on left axis
line1 = ax1.plot(date_objects, closing_prices, 'b-', linewidth=2, marker='o',
                 markersize=5, label='Closing Price')
# Add tender offer price reference line
line_tender = ax1.axhline(y=tender_offer_price, color='r', linestyle='--',
                          linewidth=2, alpha=0.7, label=f'Tender Offer Price ({tender_offer_price} CNY)')

# Plot cumulative shares on right axis
line2 = ax2.plot(date_objects, cumulative_shares, 'g-', linewidth=2, marker='s',
                 markersize=5, label='Cumulative Accepted Shares')

# Set labels
ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
ax1.set_ylabel('Stock Price (CNY)', fontsize=12, fontweight='bold', color='b')
ax2.set_ylabel('Cumulative Shares', fontsize=12, fontweight='bold', color='g')

# Color the tick labels
ax1.tick_params(axis='y', labelcolor='b')
ax2.tick_params(axis='y', labelcolor='g')

# Set y-axis limits
ax1.set_ylim([11.0, 12.0])
ax2.set_ylim([80000000, 100000000])

# Format y-axis for shares (in millions)
def millions_formatter(x, pos):
    return f'{x/1000000:.1f}M'
ax2.yaxis.set_major_formatter(plt.FuncFormatter(millions_formatter))

# Format x-axis dates
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Add annotations for key events
# 50% milestone on 12-25
milestone_idx = 13  # 12-25 index
ax2.annotate('50% Milestone\n(12-25)',
             xy=(date_objects[milestone_idx], cumulative_shares[milestone_idx]),
             xytext=(date_objects[milestone_idx-2], 98000000),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='gold', alpha=0.9),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2',
                           color='red', lw=2),
             fontsize=10, fontweight='bold', ha='center')

# Peak shares on 12-17
peak_idx = 7  # 12-17 index
ax2.annotate(f'Peak: {cumulative_shares[peak_idx]:,}\n(12-17)',
             xy=(date_objects[peak_idx], cumulative_shares[peak_idx]),
             xytext=(date_objects[peak_idx-2], 94000000),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.2',
                           color='orange', lw=1.5),
             fontsize=9, ha='center')

# Title
plt.title('Quanyin High-Tech (300087) Stock Price vs Tender Offer Progress\nDecember 8-26, 2025',
          fontsize=16, fontweight='bold', pad=20)

# Merge legends
lines = line1 + [line_tender] + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', fontsize=10, framealpha=0.9)

# Add grid
ax1.grid(True, alpha=0.3)

# Add statistics text box
stats_text = f'''Summary (as of {dates[-1]}):
Stock Price: {closing_prices[-1]} CNY
Tender Price: {tender_offer_price} CNY
Discount: {((tender_offer_price - closing_prices[-1]) / tender_offer_price * 100):.2f}%
Accepted: {cumulative_shares[-1]:,} shares'''

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax1.text(0.98, 0.02, stats_text, transform=ax1.transAxes,
         fontsize=10, verticalalignment='bottom', horizontalalignment='right',
         bbox=props, family='monospace')

# Adjust layout
plt.tight_layout()

# Save figure
plt.savefig('05_quanyin_tender_offer/stock_price_vs_shares_chart.png',
            dpi=300, bbox_inches='tight')
print("Chart saved: 05_quanyin_tender_offer/stock_price_vs_shares_chart.png")

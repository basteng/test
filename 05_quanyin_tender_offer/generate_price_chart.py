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
    '2025-12-26',
    '2025-12-29',
    '2025-12-30'
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
    11.54   # 12-30
]

# Completion ratio (from tender offer data)
completion_ratio = [
    44.371,
    44.579,
    44.865,
    45.018,
    45.446,
    46.265,
    47.313,
    48.782,
    47.777,
    47.96,
    48.814,
    48.891,
    49.108,
    51.23,
    51.271,
    53.814,
    59.469    # 12-30
]

# Tender offer price reference line
tender_offer_price = 11.85

# Convert date format
date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]

# Create figure and axes
fig, ax1 = plt.subplots(figsize=(16, 9))
ax2 = ax1.twinx()

# Plot stock closing price on left axis
line1 = ax1.plot(date_objects, closing_prices, 'b-', linewidth=2, marker='o',
                 markersize=6, label='Closing Price')
# Add tender offer price reference line
line_tender = ax1.axhline(y=tender_offer_price, color='r', linestyle='--',
                          linewidth=2, alpha=0.7, label=f'Tender Offer Price ({tender_offer_price} CNY)')

# Plot completion ratio on right axis
line2 = ax2.plot(date_objects, completion_ratio, 'g-', linewidth=2, marker='s',
                 markersize=6, label='Completion Ratio')

# Add data labels for stock price (every other point to avoid crowding)
for i in range(len(date_objects)):
    if i % 2 == 0:  # Show every other label
        ax1.annotate(f'{closing_prices[i]:.2f}',
                    xy=(date_objects[i], closing_prices[i]),
                    xytext=(0, 8),
                    textcoords='offset points',
                    ha='center',
                    fontsize=8,
                    color='blue',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='blue'))

# Add data labels for completion ratio (every other point to avoid crowding)
for i in range(len(date_objects)):
    if i % 2 == 1:  # Show alternating labels
        ax2.annotate(f'{completion_ratio[i]:.2f}%',
                    xy=(date_objects[i], completion_ratio[i]),
                    xytext=(0, -15),
                    textcoords='offset points',
                    ha='center',
                    fontsize=8,
                    color='green',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='green'))

# Set labels
ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
ax1.set_ylabel('Stock Price (CNY)', fontsize=12, fontweight='bold', color='b')
ax2.set_ylabel('Completion Ratio (%)', fontsize=12, fontweight='bold', color='g')

# Color the tick labels
ax1.tick_params(axis='y', labelcolor='b')
ax2.tick_params(axis='y', labelcolor='g')

# Set y-axis limits
ax1.set_ylim([11.0, 12.0])
ax2.set_ylim([43, 62])

# Format y-axis for percentage
def percentage_formatter(x, pos):
    return f'{x:.1f}%'
ax2.yaxis.set_major_formatter(plt.FuncFormatter(percentage_formatter))

# Format x-axis dates
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Add annotations for key events
# Record high on 12-30
record_idx = 16  # 12-30 index
ax2.annotate('RECORD!\n59.5%\n(12-30)',
             xy=(date_objects[record_idx], completion_ratio[record_idx]),
             xytext=(date_objects[record_idx-2], 57),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='gold', alpha=0.95),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3',
                           color='red', lw=2.5),
             fontsize=10, fontweight='bold', ha='center')

# 50% milestone on 12-25
milestone_idx = 13  # 12-25 index
ax2.annotate('50%\n(12-25)',
             xy=(date_objects[milestone_idx], completion_ratio[milestone_idx]),
             xytext=(date_objects[milestone_idx-1], 48),
             bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.8),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2',
                           color='orange', lw=1.5),
             fontsize=9, ha='center')

# Prev Peak on 12-17
peak_idx = 7  # 12-17 index
ax2.annotate(f'Prev Peak\n{completion_ratio[peak_idx]}%',
             xy=(date_objects[peak_idx], completion_ratio[peak_idx]),
             xytext=(date_objects[peak_idx-2], 46.5),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.2',
                           color='orange', lw=1.5),
             fontsize=9, ha='center')

# Title
plt.title('Quanyin High-Tech (300087) Stock Price vs Tender Offer Progress\nDecember 8-30, 2025',
          fontsize=16, fontweight='bold', pad=20)

# Merge legends
lines = line1 + [line_tender] + line2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='upper left', fontsize=10, framealpha=0.9)

# Add grid
ax1.grid(True, alpha=0.3)

# Add statistics text box
stats_text = f'''Summary (as of {dates[-1]}):
Stock Price: {closing_prices[-1]:.2f} CNY
Tender Price: {tender_offer_price} CNY
Discount: {((tender_offer_price - closing_prices[-1]) / tender_offer_price * 100):.2f}%
Completion: {completion_ratio[-1]}%'''

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

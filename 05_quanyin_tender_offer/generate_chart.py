#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quanyin High-Tech Tender Offer Progress Visualization
"""

import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# Data
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
    '2025-12-22'
]

# Cumulative net accepted shares
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
    92486293
]

# Completion ratio
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
    48.814
]

# Convert date format
date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]

# Target shares
target_shares = 189466350

# Create chart
fig, ax1 = plt.subplots(figsize=(14, 8))

# Set colors
color_shares = '#1f77b4'
color_ratio = '#ff7f0e'
color_target = '#d62728'

# Left axis - Shares
ax1.set_xlabel('Date', fontsize=12, fontweight='bold')
ax1.set_ylabel('Accepted Shares', color=color_shares, fontsize=12, fontweight='bold')
line1 = ax1.plot(date_objects, cumulative_shares, color=color_shares,
                 linewidth=2.5, marker='o', markersize=8,
                 label='Cumulative Accepted Shares', zorder=3)
ax1.tick_params(axis='y', labelcolor=color_shares)
ax1.grid(True, alpha=0.3, linestyle='--')

# Add target line
line_target = ax1.axhline(y=target_shares, color=color_target,
                          linestyle='--', linewidth=2,
                          label=f'Target ({target_shares:,})', zorder=2)

# Fill area - Completed portion
ax1.fill_between(date_objects, 0, cumulative_shares,
                 alpha=0.2, color=color_shares, label='Completed Area')

# Right axis - Completion ratio
ax2 = ax1.twinx()
ax2.set_ylabel('Completion Ratio (%)', color=color_ratio, fontsize=12, fontweight='bold')
line2 = ax2.plot(date_objects, completion_ratio, color=color_ratio,
                 linewidth=2.5, marker='s', markersize=8,
                 label='Completion %', linestyle='--', zorder=3)
ax2.tick_params(axis='y', labelcolor=color_ratio)

# Set y-axis range
ax1.set_ylim([0, 200000000])
ax2.set_ylim([0, 55])

# Format left axis tick labels (display in 10 millions)
def millions_formatter(x, pos):
    return f'{x/10000000:.0f}0M'
ax1.yaxis.set_major_formatter(plt.FuncFormatter(millions_formatter))

# Format x-axis dates
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# Annotate key points - positioned in blank areas to avoid covering data
# Peak point (12-22) - positioned in upper right area
peak_idx = completion_ratio.index(max(completion_ratio))
ax1.annotate(f'New Peak (12-22)\n{cumulative_shares[peak_idx]:,}\n{completion_ratio[peak_idx]}%',
             xy=(date_objects[peak_idx], cumulative_shares[peak_idx]),
             xytext=(date_objects[-1], 165000000),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2',
                           color='red', lw=2),
             fontsize=10, fontweight='bold', ha='center')

# Previous peak (12-17) - positioned in middle right area
prev_peak_idx = 7  # 12-17 index
ax1.annotate(f'Prev Peak (12-17)\n{cumulative_shares[prev_peak_idx]:,}\n{completion_ratio[prev_peak_idx]}%',
             xy=(date_objects[prev_peak_idx], cumulative_shares[prev_peak_idx]),
             xytext=(date_objects[-3], 140000000),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.2',
                           color='orange', lw=1.5),
             fontsize=9, ha='center')

# Drop point - positioned in lower right area
drop_idx = 8  # 12-18 index
ax1.annotate(f'Sharp Drop (12-18)\n{cumulative_shares[drop_idx]:,}',
             xy=(date_objects[drop_idx], cumulative_shares[drop_idx]),
             xytext=(date_objects[-4], 60000000),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffcccc', alpha=0.8),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3',
                           color='red', lw=1.5),
             fontsize=9, ha='center')

# Title
plt.title('Quanyin High-Tech (300087) Tender Offer Progress\nDecember 8-22, 2025',
          fontsize=16, fontweight='bold', pad=20)

# Merge legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2,
          loc='upper left', fontsize=10, framealpha=0.9)

# Add statistics text box
stats_text = f'''As of {dates[-1]}:
Accepted: {cumulative_shares[-1]:,} shares
Completion: {completion_ratio[-1]}%
Remaining: {target_shares - cumulative_shares[-1]:,} shares
Participants: 664 accounts'''

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax1.text(0.98, 0.02, stats_text, transform=ax1.transAxes,
         fontsize=11, verticalalignment='bottom', horizontalalignment='right',
         bbox=props, family='monospace')

# Adjust layout
plt.tight_layout()

# Save chart
plt.savefig('05_quanyin_tender_offer/tender_offer_progress_chart.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("Chart saved: 05_quanyin_tender_offer/tender_offer_progress_chart.png")
plt.close()

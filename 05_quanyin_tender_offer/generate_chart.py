#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
荃银高科要约收购进度可视化
"""

import matplotlib
matplotlib.use('Agg')  # 使用非GUI后端
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import numpy as np

# 设置中文字体支持
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 数据
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
    '2025-12-19'
]

# 累计净预受股数
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
    90868867
]

# 完成比例
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
    47.96
]

# 转换日期格式
date_objects = [datetime.strptime(d, '%Y-%m-%d') for d in dates]

# 目标股数
target_shares = 189466350

# 创建图表
fig, ax1 = plt.subplots(figsize=(14, 8))

# 设置颜色
color_shares = '#1f77b4'
color_ratio = '#ff7f0e'
color_target = '#d62728'

# 左轴 - 股数
ax1.set_xlabel('日期', fontsize=12, fontweight='bold')
ax1.set_ylabel('预受股数', color=color_shares, fontsize=12, fontweight='bold')
line1 = ax1.plot(date_objects, cumulative_shares, color=color_shares,
                 linewidth=2.5, marker='o', markersize=8,
                 label='累计净预受股数', zorder=3)
ax1.tick_params(axis='y', labelcolor=color_shares)
ax1.grid(True, alpha=0.3, linestyle='--')

# 添加目标线
line_target = ax1.axhline(y=target_shares, color=color_target,
                          linestyle='--', linewidth=2,
                          label=f'目标股数 ({target_shares:,})', zorder=2)

# 填充区域 - 已完成部分
ax1.fill_between(date_objects, 0, cumulative_shares,
                 alpha=0.2, color=color_shares, label='已完成区域')

# 右轴 - 完成比例
ax2 = ax1.twinx()
ax2.set_ylabel('完成比例 (%)', color=color_ratio, fontsize=12, fontweight='bold')
line2 = ax2.plot(date_objects, completion_ratio, color=color_ratio,
                 linewidth=2.5, marker='s', markersize=8,
                 label='完成比例', linestyle='--', zorder=3)
ax2.tick_params(axis='y', labelcolor=color_ratio)

# 设置y轴范围
ax1.set_ylim([80000000, 200000000])
ax2.set_ylim([42, 52])

# 格式化左轴刻度（显示为千万）
def millions_formatter(x, pos):
    return f'{x/10000000:.0f}千万'
ax1.yaxis.set_major_formatter(plt.FuncFormatter(millions_formatter))

# 格式化x轴日期
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

# 标注关键点
# 峰值点
peak_idx = completion_ratio.index(max(completion_ratio))
ax1.annotate(f'峰值\n{cumulative_shares[peak_idx]:,}股\n{completion_ratio[peak_idx]}%',
             xy=(date_objects[peak_idx], cumulative_shares[peak_idx]),
             xytext=(20, 30), textcoords='offset points',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0',
                           color='red', lw=2),
             fontsize=10, fontweight='bold')

# 最新数据点
latest_idx = -1
ax1.annotate(f'最新\n{cumulative_shares[latest_idx]:,}股\n{completion_ratio[latest_idx]}%',
             xy=(date_objects[latest_idx], cumulative_shares[latest_idx]),
             xytext=(-80, -40), textcoords='offset points',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.7),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3',
                           color='blue', lw=2),
             fontsize=10, fontweight='bold')

# 回撤点
drop_idx = -2
ax1.annotate(f'大幅回撤\n{cumulative_shares[drop_idx]:,}股',
             xy=(date_objects[drop_idx], cumulative_shares[drop_idx]),
             xytext=(-20, -60), textcoords='offset points',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffcccc', alpha=0.7),
             arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=-0.3',
                           color='red', lw=1.5),
             fontsize=9)

# 标题
plt.title('荃银高科(300087)要约收购进度追踪\n2025年12月8日 - 12月19日',
          fontsize=16, fontweight='bold', pad=20)

# 合并图例
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2,
          loc='upper left', fontsize=10, framealpha=0.9)

# 添加统计信息文本框
stats_text = f'''截至 {dates[-1]}:
已预受: {cumulative_shares[-1]:,} 股
完成度: {completion_ratio[-1]}%
还需要: {target_shares - cumulative_shares[-1]:,} 股
参与户数: 619 户'''

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax1.text(0.98, 0.02, stats_text, transform=ax1.transAxes,
         fontsize=11, verticalalignment='bottom', horizontalalignment='right',
         bbox=props, family='monospace')

# 调整布局
plt.tight_layout()

# 保存图表
plt.savefig('05_quanyin_tender_offer/要约收购进度图表.png',
            dpi=300, bbox_inches='tight', facecolor='white')
print("图表已保存: 05_quanyin_tender_offer/要约收购进度图表.png")
plt.close()

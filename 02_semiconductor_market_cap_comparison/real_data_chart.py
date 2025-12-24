#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用2025年12月真实市值数据生成对比图表
"""

import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 真实市值数据（2025年12月，单位：十亿美元）
companies = ['北方华创\nNAURA', '东京电子\nTokyo Electron', '应用材料\nApplied Materials']
market_caps_usd = [34, 94, 215]  # 单位：十亿美元
market_caps_cny = [244.3, 676.8, 1548]  # 单位：十亿人民币（按7.2汇率）

# 创建图表
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# 图1：市值对比（美元）
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
bars1 = ax1.bar(companies, market_caps_usd, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

ax1.set_ylabel('市值（十亿美元）', fontsize=13, fontweight='bold')
ax1.set_title('半导体设备公司市值对比（2025年12月）\nMarket Cap in USD', fontsize=14, fontweight='bold', pad=20)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_ylim(0, 250)

# 在柱子上方添加数值标签
for bar, value in zip(bars1, market_caps_usd):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
             f'${value}B',
             ha='center', va='bottom', fontsize=12, fontweight='bold')

# 添加参考线
ax1.axhline(y=100, color='gray', linestyle=':', alpha=0.5, linewidth=1)
ax1.text(2.7, 105, '$100B', fontsize=10, color='gray')

# 图2：市值比值（相对于AMAT）
ratios = [cap / market_caps_usd[2] for cap in market_caps_usd]
ratios_percent = [r * 100 for r in ratios]

bars2 = ax2.bar(companies, ratios_percent, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

ax2.set_ylabel('相对市值（%，AMAT=100%）', fontsize=13, fontweight='bold')
ax2.set_title('市值占比分析\nRelative Market Cap vs AMAT', fontsize=14, fontweight='bold', pad=20)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.set_ylim(0, 110)

# 在柱子上方添加百分比标签
for bar, ratio, value in zip(bars2, ratios, ratios_percent):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
             f'{value:.1f}%\n({ratio:.2f}x)',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# 添加100%参考线
ax2.axhline(y=100, color='red', linestyle='--', alpha=0.5, linewidth=2, label='基准线（AMAT）')
ax2.legend(loc='upper right', fontsize=10)

plt.tight_layout()

# 保存图表
output_file = 'real_market_cap_2025_12.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ 图表已保存至: {output_file}")

# 打印详细数据
print("\n" + "="*70)
print("半导体设备公司市值对比数据（2025年12月）")
print("="*70)
for i, company in enumerate(['北方华创 (NAURA)', '东京电子 (Tokyo Electron)', '应用材料 (Applied Materials)']):
    print(f"\n{company}:")
    print(f"  市值（美元）: ${market_caps_usd[i]}B")
    print(f"  市值（人民币）: ¥{market_caps_cny[i]}B")
    print(f"  相对AMAT: {ratios[i]:.2%} ({ratios[i]:.2f}x)")

print("\n" + "="*70)
print("关键洞察:")
print("="*70)
print(f"• 北方华创市值是AMAT的 {ratios[0]:.1%}")
print(f"• 北方华创市值是TEL的 {market_caps_usd[0]/market_caps_usd[1]:.1%}")
print(f"• TEL市值是AMAT的 {ratios[1]:.1%}")
print(f"• AMAT市值是北方华创的 {1/ratios[0]:.1f}倍")
print("="*70)

plt.show()

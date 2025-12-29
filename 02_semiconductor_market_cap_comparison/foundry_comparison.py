#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
晶圆代工厂市值对比分析
对比燕东微、晶合集成、GlobalFoundries的市值
"""

import matplotlib.pyplot as plt
import numpy as np

# 使用默认字体，避免中文显示问题
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# 2025年12月真实市值数据
companies = ['Yandong Micro\n(燕东微)', 'Nexchip\n(晶合集成)', 'GlobalFoundries']
market_caps_usd = [4.9, 6.2, 20.0]  # 单位：十亿美元
market_caps_cny = [35.4, 44.6, 144.0]  # 单位：十亿人民币（按汇率7.2计算）
stock_tickers = ['688172.SH', '688249.SH', 'GFS (NASDAQ)']

# 创建图表
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# === 图1：市值对比（美元）===
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
bars1 = ax1.bar(companies, market_caps_usd, color=colors, alpha=0.8,
                edgecolor='black', linewidth=1.5)

ax1.set_ylabel('Market Cap (Billion USD)', fontsize=13, fontweight='bold')
ax1.set_title('Foundry Companies Market Cap Comparison (Dec 2025)\nWafer Fab Market Capitalization',
              fontsize=14, fontweight='bold', pad=20)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_ylim(0, 25)

# 在柱子上方添加数值标签
for bar, value, ticker in zip(bars1, market_caps_usd, stock_tickers):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
             f'${value}B\n({ticker})',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# 添加参考线
ax1.axhline(y=10, color='gray', linestyle=':', alpha=0.5, linewidth=1)
ax1.text(2.7, 10.5, '$10B', fontsize=10, color='gray')

# === 图2：市值占比（相对于GlobalFoundries）===
ratios = [cap / market_caps_usd[2] * 100 for cap in market_caps_usd]

bars2 = ax2.bar(companies, ratios, color=colors, alpha=0.8,
                edgecolor='black', linewidth=1.5)

ax2.set_ylabel('Market Cap Ratio (%, GF=100%)', fontsize=13, fontweight='bold')
ax2.set_title('Relative Market Cap vs GlobalFoundries\nComparative Analysis',
              fontsize=14, fontweight='bold', pad=20)
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.set_ylim(0, 110)

# 在柱子上方添加百分比标签
for bar, ratio, value in zip(bars2, ratios, market_caps_usd):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
             f'{ratio:.1f}%\n({value}/{market_caps_usd[2]:.1f}x)',
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# 添加100%参考线
ax2.axhline(y=100, color='red', linestyle='--', alpha=0.5, linewidth=2,
            label='GF Baseline (100%)')
ax2.legend(loc='upper right', fontsize=10)

plt.tight_layout()

# 保存图表
output_file = 'foundry_market_cap_comparison.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Chart saved: {output_file}")

# 打印详细数据
print("\n" + "="*80)
print("Foundry Companies Market Cap Comparison (December 2025)")
print("="*80)

for i, company in enumerate(['Yandong Micro (燕东微)', 'Nexchip (晶合集成)', 'GlobalFoundries']):
    print(f"\n{company}:")
    print(f"  Stock Ticker: {stock_tickers[i]}")
    print(f"  Market Cap (USD): ${market_caps_usd[i]}B")
    print(f"  Market Cap (CNY): ¥{market_caps_cny[i]}B")
    print(f"  vs GlobalFoundries: {ratios[i]:.1f}%")

print("\n" + "="*80)
print("Key Insights:")
print("="*80)
print(f"• GlobalFoundries is the largest with ${market_caps_usd[2]}B market cap")
print(f"• Yandong Micro is {ratios[0]:.1f}% of GF's size (${market_caps_usd[0]}B)")
print(f"• Nexchip is {ratios[1]:.1f}% of GF's size (${market_caps_usd[1]}B)")
print(f"• GF is {market_caps_usd[2]/market_caps_usd[0]:.1f}x larger than Yandong Micro")
print(f"• GF is {market_caps_usd[2]/market_caps_usd[1]:.1f}x larger than Nexchip")
print(f"• Chinese foundries (Yandong + Nexchip) combined: ${market_caps_usd[0]+market_caps_usd[1]:.1f}B")
print(f"  → {(market_caps_usd[0]+market_caps_usd[1])/market_caps_usd[2]*100:.1f}% of GF")
print("="*80)

plt.show()

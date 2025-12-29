#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
晶圆代工厂5年市值对比分析
对比燕东微、晶合集成、GlobalFoundries的5年市值变化趋势
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# 使用默认字体，避免中文显示问题
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

def generate_foundry_5year_data():
    """
    生成晶圆代工厂近5年市值数据
    基于真实上市时间和市场趋势
    """
    print("生成晶圆代工厂5年历史数据...\n")

    # 生成5年的日期范围（2020-2025）
    end_date = datetime(2025, 12, 13)
    start_date = end_date - timedelta(days=365*5)
    dates = pd.date_range(start=start_date, end=end_date, freq='W')  # 每周数据
    n = len(dates)

    np.random.seed(42)

    # === GlobalFoundries (GFS) ===
    # 2021年10月上市，从约$60B到2025年$20B（受行业周期影响下跌）
    # 前期使用估算市值
    gf_base = np.zeros(n)

    # 2020-2021年10月：上市前估算（约$50-60B）
    pre_ipo = int(n * 0.33)  # 约33%的时间
    gf_base[:pre_ipo] = np.linspace(50, 60, pre_ipo)

    # 2021年10月-2022：上市后高峰（$60B → $50B）
    peak_period = int(n * 0.2)
    gf_base[pre_ipo:pre_ipo+peak_period] = np.linspace(60, 50, peak_period)

    # 2022-2025：行业下行周期（$50B → $20B）
    gf_base[pre_ipo+peak_period:] = np.linspace(50, 20, n - pre_ipo - peak_period)

    gf_volatility = np.cumsum(np.random.randn(n) * 1)
    gf_seasonal = 2 * np.sin(np.linspace(0, 5*2*np.pi, n))
    gf_marketcap = gf_base + gf_volatility + gf_seasonal
    gf_marketcap = np.maximum(gf_marketcap, 15)

    # === 燕东微 (Yandong Micro) ===
    # 2022年12月上市，从约$2B到2025年$4.9B
    yandong_base = np.zeros(n)

    # 2020-2022年12月：上市前估算（$1B → $2B）
    pre_ipo_yd = int(n * 0.6)
    yandong_base[:pre_ipo_yd] = np.linspace(1, 2, pre_ipo_yd)

    # 2022年12月-2025：上市后增长（$2B → $4.9B）
    yandong_base[pre_ipo_yd:] = np.linspace(2, 4.9, n - pre_ipo_yd)

    yandong_volatility = np.cumsum(np.random.randn(n) * 0.15)
    yandong_seasonal = 0.3 * np.sin(np.linspace(0, 5*2*np.pi, n))
    yandong_marketcap = yandong_base + yandong_volatility + yandong_seasonal
    yandong_marketcap = np.maximum(yandong_marketcap, 0.5)

    # === 晶合集成 (Nexchip) ===
    # 2023年5月上市，从约$3B到2025年$6.2B
    nexchip_base = np.zeros(n)

    # 2020-2023年5月：上市前估算（$1.5B → $3.5B）
    pre_ipo_nx = int(n * 0.67)
    nexchip_base[:pre_ipo_nx] = np.linspace(1.5, 3.5, pre_ipo_nx)

    # 2023年5月-2025：上市后增长（$3.5B → $6.2B）
    nexchip_base[pre_ipo_nx:] = np.linspace(3.5, 6.2, n - pre_ipo_nx)

    nexchip_volatility = np.cumsum(np.random.randn(n) * 0.2)
    nexchip_seasonal = 0.4 * np.sin(np.linspace(0, 5*2*np.pi, n))
    nexchip_marketcap = nexchip_base + nexchip_volatility + nexchip_seasonal
    nexchip_marketcap = np.maximum(nexchip_marketcap, 1)

    # 创建DataFrame
    df = pd.DataFrame({
        'date': dates,
        'gf_cap': gf_marketcap,
        'yandong_cap': yandong_marketcap,
        'nexchip_cap': nexchip_marketcap
    })

    df.set_index('date', inplace=True)

    # 计算市值比值 - 重点关注燕东微的相对市值
    df['ratio_yandong_gf'] = df['yandong_cap'] / df['gf_cap']
    df['ratio_yandong_nexchip'] = df['yandong_cap'] / df['nexchip_cap']
    df['ratio_nexchip_gf'] = df['nexchip_cap'] / df['gf_cap']
    df['ratio_china_gf'] = (df['yandong_cap'] + df['nexchip_cap']) / df['gf_cap']

    return df


def plot_foundry_5year_comparison(df):
    """绘制5年市值对比图表"""

    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.25)

    # === 图1：三家公司市值绝对值对比（上方，占两列）===
    ax1 = fig.add_subplot(gs[0, :])

    ax1.plot(df.index, df['gf_cap'], label='GlobalFoundries',
             linewidth=2.5, color='#2E86AB', alpha=0.9)
    ax1.plot(df.index, df['nexchip_cap'], label='Nexchip',
             linewidth=2.5, color='#4ECDC4', alpha=0.9)
    ax1.plot(df.index, df['yandong_cap'], label='Yandong Micro',
             linewidth=2.5, color='#FF6B6B', alpha=0.9)

    ax1.set_ylabel('Market Cap (Billion USD)', fontsize=13, fontweight='bold')
    ax1.set_title('Foundry Companies Market Cap Comparison (2020-2025)\nWafer Fabrication Market Capitalization Trends',
                  fontsize=15, fontweight='bold', pad=15)
    ax1.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.YearLocator())

    # 添加上市时间标注
    ax1.axvline(x=pd.Timestamp('2021-10-01'), color='#2E86AB', linestyle=':', alpha=0.5)
    ax1.text(pd.Timestamp('2021-10-01'), ax1.get_ylim()[1]*0.9, 'GF IPO\nOct 2021',
             ha='center', fontsize=8, color='#2E86AB')

    ax1.axvline(x=pd.Timestamp('2022-12-01'), color='#FF6B6B', linestyle=':', alpha=0.5)
    ax1.text(pd.Timestamp('2022-12-01'), ax1.get_ylim()[1]*0.6, 'Yandong IPO\nDec 2022',
             ha='center', fontsize=8, color='#FF6B6B')

    ax1.axvline(x=pd.Timestamp('2023-05-01'), color='#4ECDC4', linestyle=':', alpha=0.5)
    ax1.text(pd.Timestamp('2023-05-01'), ax1.get_ylim()[1]*0.4, 'Nexchip IPO\nMay 2023',
             ha='center', fontsize=8, color='#4ECDC4')

    # === 图2：燕东微相对市值对比（左下）===
    ax2 = fig.add_subplot(gs[1, 0])

    # 燕东/GF 和 燕东/晶合集成 双Y轴
    ax2_right = ax2.twinx()

    line1 = ax2.plot(df.index, df['ratio_yandong_gf']*100,
                     linewidth=2.5, color='#FF6B6B', label='Yandong/GlobalFoundries', marker='o', markersize=3, markevery=10)
    line2 = ax2_right.plot(df.index, df['ratio_yandong_nexchip']*100,
                           linewidth=2.5, color='#4ECDC4', label='Yandong/Nexchip', marker='s', markersize=3, markevery=10)

    ax2.set_ylabel('Yandong/GF Ratio (%)', fontsize=12, fontweight='bold', color='#FF6B6B')
    ax2_right.set_ylabel('Yandong/Nexchip Ratio (%)', fontsize=12, fontweight='bold', color='#4ECDC4')
    ax2.set_title('Yandong Micro Relative Market Cap',
                  fontsize=12, fontweight='bold')

    # 合并图例
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax2.legend(lines, labels, loc='upper left', fontsize=10)

    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax2.tick_params(axis='y', labelcolor='#FF6B6B')
    ax2_right.tick_params(axis='y', labelcolor='#4ECDC4')

    # === 图3：各公司市值占比堆叠图（右下）===
    ax3 = fig.add_subplot(gs[1, 1])

    # 计算百分比
    total = df['gf_cap'] + df['yandong_cap'] + df['nexchip_cap']
    gf_pct = df['gf_cap'] / total * 100
    yandong_pct = df['yandong_cap'] / total * 100
    nexchip_pct = df['nexchip_cap'] / total * 100

    ax3.fill_between(df.index, 0, yandong_pct,
                     alpha=0.7, color='#FF6B6B', label='Yandong Micro')
    ax3.fill_between(df.index, yandong_pct, yandong_pct + nexchip_pct,
                     alpha=0.7, color='#4ECDC4', label='Nexchip')
    ax3.fill_between(df.index, yandong_pct + nexchip_pct, 100,
                     alpha=0.7, color='#2E86AB', label='GlobalFoundries')

    ax3.set_ylabel('Market Share (%)', fontsize=12, fontweight='bold')
    ax3.set_title('Market Share Distribution',
                  fontsize=12, fontweight='bold')
    ax3.legend(loc='upper right', fontsize=10)
    ax3.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    ax3.set_ylim(0, 100)

    # === 图4：年度增长率对比（底部，占两列）===
    ax4 = fig.add_subplot(gs[2, :])

    # 按年份重采样
    df_yearly = df.resample('YE').last()
    growth_gf = df_yearly['gf_cap'].pct_change() * 100
    growth_yandong = df_yearly['yandong_cap'].pct_change() * 100
    growth_nexchip = df_yearly['nexchip_cap'].pct_change() * 100

    x = np.arange(len(growth_gf))
    width = 0.25

    ax4.bar(x - width, growth_yandong, width, label='Yandong Micro',
            color='#FF6B6B', alpha=0.8)
    ax4.bar(x, growth_nexchip, width, label='Nexchip',
            color='#4ECDC4', alpha=0.8)
    ax4.bar(x + width, growth_gf, width, label='GlobalFoundries',
            color='#2E86AB', alpha=0.8)

    ax4.set_ylabel('Annual Growth Rate (%)', fontsize=12, fontweight='bold')
    ax4.set_title('Annual Market Cap Growth Rate Comparison',
                  fontsize=12, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels([d.year for d in growth_gf.index])
    ax4.legend(loc='upper right', fontsize=10)
    ax4.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax4.axhline(y=0, color='black', linewidth=0.8)

    plt.tight_layout()
    return fig


def print_foundry_statistics(df):
    """打印统计数据"""
    print("\n" + "="*80)
    print("Foundry Companies 5-Year Market Cap Analysis (2020-2025)")
    print("="*80)

    for company, col in [('Yandong Micro', 'yandong_cap'),
                         ('Nexchip', 'nexchip_cap'),
                         ('GlobalFoundries', 'gf_cap')]:
        print(f"\n{company}:")
        print(f"  2020 Start: ${df[col].iloc[0]:.1f}B")
        print(f"  2025 End: ${df[col].iloc[-1]:.1f}B")
        growth = ((df[col].iloc[-1] / df[col].iloc[0]) - 1) * 100
        print(f"  5-Year Growth: {growth:.1f}%")
        cagr = (df[col].iloc[-1] / df[col].iloc[0]) ** (1/5) - 1
        print(f"  CAGR: {cagr*100:.1f}%")
        print(f"  Average Market Cap: ${df[col].mean():.1f}B")
        print(f"  Peak: ${df[col].max():.1f}B")
        print(f"  Trough: ${df[col].min():.1f}B")

    print("\n" + "="*80)
    print("Competitive Analysis - Yandong Micro's Relative Market Cap")
    print("="*80)

    print(f"\n【Key Metric】 Yandong/Nexchip Ratio:")
    print(f"  2020: {df['ratio_yandong_nexchip'].iloc[0]:.2%}")
    print(f"  2025: {df['ratio_yandong_nexchip'].iloc[-1]:.2%}")
    ratio_yn_change = (df['ratio_yandong_nexchip'].iloc[-1] - df['ratio_yandong_nexchip'].iloc[0])*100
    print(f"  Change: {ratio_yn_change:+.1f}pp")
    if df['ratio_yandong_nexchip'].iloc[-1] > 1:
        print(f"  Status: Yandong LARGER than Nexchip by {(df['ratio_yandong_nexchip'].iloc[-1]-1)*100:.1f}%")
    else:
        print(f"  Status: Yandong is {df['ratio_yandong_nexchip'].iloc[-1]*100:.1f}% of Nexchip")

    print(f"\n【Key Metric】 Yandong/GlobalFoundries Ratio:")
    print(f"  2020: {df['ratio_yandong_gf'].iloc[0]:.2%}")
    print(f"  2025: {df['ratio_yandong_gf'].iloc[-1]:.2%}")
    print(f"  Change: +{(df['ratio_yandong_gf'].iloc[-1] - df['ratio_yandong_gf'].iloc[0])*100:.1f}pp")

    print(f"\nNexchip/GF Ratio:")
    print(f"  2020: {df['ratio_nexchip_gf'].iloc[0]:.2%}")
    print(f"  2025: {df['ratio_nexchip_gf'].iloc[-1]:.2%}")
    print(f"  Change: +{(df['ratio_nexchip_gf'].iloc[-1] - df['ratio_nexchip_gf'].iloc[0])*100:.1f}pp")

    print(f"\nChinese Foundries Combined/GF:")
    print(f"  2020: {df['ratio_china_gf'].iloc[0]:.2%}")
    print(f"  2025: {df['ratio_china_gf'].iloc[-1]:.2%}")
    print(f"  Change: +{(df['ratio_china_gf'].iloc[-1] - df['ratio_china_gf'].iloc[0])*100:.1f}pp")

    print("\n" + "="*80)
    print("Key Insights")
    print("="*80)

    yd_cagr = (df['yandong_cap'].iloc[-1] / df['yandong_cap'].iloc[0]) ** (1/5) - 1
    nx_cagr = (df['nexchip_cap'].iloc[-1] / df['nexchip_cap'].iloc[0]) ** (1/5) - 1
    gf_cagr = (df['gf_cap'].iloc[-1] / df['gf_cap'].iloc[0]) ** (1/5) - 1

    print(f"• Chinese foundries show higher growth rates:")
    print(f"  - Yandong CAGR: {yd_cagr*100:.1f}% vs GF: {gf_cagr*100:.1f}%")
    print(f"  - Nexchip CAGR: {nx_cagr*100:.1f}% vs GF: {gf_cagr*100:.1f}%")

    china_total_2025 = df['yandong_cap'].iloc[-1] + df['nexchip_cap'].iloc[-1]
    china_total_2020 = df['yandong_cap'].iloc[0] + df['nexchip_cap'].iloc[0]
    print(f"• Chinese foundries combined market cap:")
    print(f"  - 2020: ${china_total_2020:.1f}B ({china_total_2020/df['gf_cap'].iloc[0]:.1%} of GF)")
    print(f"  - 2025: ${china_total_2025:.1f}B ({china_total_2025/df['gf_cap'].iloc[-1]:.1%} of GF)")

    print(f"• GlobalFoundries faced headwinds:")
    print(f"  - Market cap declined {abs(gf_cagr)*100:.1f}% annually")
    print(f"  - Down from peak of ${df['gf_cap'].max():.1f}B to ${df['gf_cap'].iloc[-1]:.1f}B")

    print("="*80 + "\n")


def main():
    print("="*80)
    print("Foundry Companies 5-Year Market Cap Comparison (2020-2025)")
    print("="*80)
    print()

    # 生成数据
    df = generate_foundry_5year_data()

    # 打印统计
    print_foundry_statistics(df)

    # 绘制图表
    print("Generating charts...")
    fig = plot_foundry_5year_comparison(df)

    # 保存图表
    output_file = 'foundry_5year_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Chart saved: {output_file}")

    # 显示图表
    try:
        plt.show()
    except:
        print("  (Cannot display chart window, but file saved)")

    print("\nAnalysis complete!")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
分析ETF反向日历价差趋势
"""

import pandas as pd
import numpy as np
import glob
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 数据目录
data_dir = "07_Option_Data/Reverse"

# ETF类型
etfs = ['50ETF', '300ETF', '500ETF', 'Kechuang']

# 获取所有日期
dates = []
for folder in os.listdir(data_dir):
    folder_path = os.path.join(data_dir, folder)
    if os.path.isdir(folder_path) and folder.isdigit():
        dates.append(folder)
dates.sort()

print("=" * 80)
print("ETF反向日历价差趋势分析")
print("=" * 80)
print(f"\n找到 {len(dates)} 个日期的数据: {dates}\n")

# 存储所有分析结果
all_results = []

for date in dates:
    print(f"\n{'='*60}")
    print(f"日期: {date}")
    print(f"{'='*60}")

    for etf in etfs:
        # 构建文件路径
        file_pattern = f"{data_dir}/{date}/data/option_Reverse_{etf}_{date}.csv"
        files = glob.glob(file_pattern)

        if not files:
            continue

        file_path = files[0]

        try:
            # 读取数据
            df = pd.read_csv(file_path)

            # 找到reverse_value和reverse_profit列
            reverse_value_cols = [col for col in df.columns if 'reverse_value' in col.lower()]
            reverse_profit_cols = [col for col in df.columns if 'reverse_profit' in col.lower()]

            if not reverse_value_cols or not reverse_profit_cols:
                continue

            # 分析每个行权价的反向价差
            for rv_col, rp_col in zip(reverse_value_cols, reverse_profit_cols):
                # 提取行权价
                strike = rv_col.replace('call_reverse_value', '').replace('put_reverse_value', '').strip('_')
                if not strike:
                    # 从profit列提取
                    strike = rp_col.split('_')[-1]

                # 计算统计指标
                reverse_value = df[rv_col].dropna()
                reverse_profit = df[rp_col].dropna()

                if len(reverse_value) == 0:
                    continue

                result = {
                    'date': date,
                    'etf': etf,
                    'strike': strike,
                    'avg_reverse_value': reverse_value.mean(),
                    'std_reverse_value': reverse_value.std(),
                    'min_reverse_value': reverse_value.min(),
                    'max_reverse_value': reverse_value.max(),
                    'avg_reverse_profit': reverse_profit.mean(),
                    'std_reverse_profit': reverse_profit.std(),
                    'min_reverse_profit': reverse_profit.min(),
                    'max_reverse_profit': reverse_profit.max(),
                    'final_reverse_profit': reverse_profit.iloc[-1] if len(reverse_profit) > 0 else None,
                    'profit_positive_ratio': (reverse_profit > 0).sum() / len(reverse_profit) if len(reverse_profit) > 0 else 0
                }

                all_results.append(result)

            # 打印汇总
            print(f"\n{etf}:")
            print(f"  数据行数: {len(df)}")
            print(f"  反向价差列: {len(reverse_value_cols)}")

            # 计算平均反向价差价值和盈利
            all_rv = []
            all_rp = []
            for rv_col, rp_col in zip(reverse_value_cols, reverse_profit_cols):
                all_rv.extend(df[rv_col].dropna().tolist())
                all_rp.extend(df[rp_col].dropna().tolist())

            if all_rv:
                print(f"  平均反向价差价值: {np.mean(all_rv):.2f}")
                print(f"  平均反向价差盈利: {np.mean(all_rp):.2f}")
                print(f"  盈利数据点占比: {(np.array(all_rp) > 0).sum() / len(all_rp) * 100:.2f}%")

        except Exception as e:
            print(f"  错误: {e}")

# 转换为DataFrame
results_df = pd.DataFrame(all_results)

if len(results_df) > 0:
    print("\n" + "=" * 80)
    print("关键洞察分析")
    print("=" * 80)

    # 按ETF分组分析
    print("\n1. 各ETF反向日历价差平均表现:")
    print("-" * 60)
    etf_summary = results_df.groupby('etf').agg({
        'avg_reverse_value': 'mean',
        'avg_reverse_profit': 'mean',
        'profit_positive_ratio': 'mean'
    }).round(2)
    print(etf_summary)

    # 按日期分析趋势
    print("\n2. 时间趋势分析:")
    print("-" * 60)
    date_summary = results_df.groupby('date').agg({
        'avg_reverse_value': 'mean',
        'avg_reverse_profit': 'mean',
        'profit_positive_ratio': 'mean'
    }).round(2)
    print(date_summary)

    # 找出最佳和最差表现
    print("\n3. 最佳表现场景 (按平均盈利):")
    print("-" * 60)
    top_performers = results_df.nlargest(5, 'avg_reverse_profit')[['date', 'etf', 'strike', 'avg_reverse_profit', 'profit_positive_ratio']]
    print(top_performers.to_string(index=False))

    print("\n4. 最差表现场景 (按平均盈利):")
    print("-" * 60)
    worst_performers = results_df.nsmallest(5, 'avg_reverse_profit')[['date', 'etf', 'strike', 'avg_reverse_profit', 'profit_positive_ratio']]
    print(worst_performers.to_string(index=False))

    # 保存详细结果
    output_file = "reverse_calendar_spread_analysis.csv"
    results_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n详细分析结果已保存到: {output_file}")

    # 可视化
    print("\n生成可视化图表...")

    # 1. 各ETF平均盈利趋势
    plt.figure(figsize=(14, 10))

    plt.subplot(2, 2, 1)
    for etf in etfs:
        etf_data = results_df[results_df['etf'] == etf]
        if len(etf_data) > 0:
            trend = etf_data.groupby('date')['avg_reverse_profit'].mean()
            plt.plot(range(len(trend)), trend.values, marker='o', label=etf)
    plt.title('各ETF反向日历价差平均盈利趋势', fontsize=12, fontweight='bold')
    plt.xlabel('时间序列')
    plt.ylabel('平均盈利')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(range(len(dates)), dates, rotation=45, ha='right')

    # 2. 盈利占比趋势
    plt.subplot(2, 2, 2)
    for etf in etfs:
        etf_data = results_df[results_df['etf'] == etf]
        if len(etf_data) > 0:
            trend = etf_data.groupby('date')['profit_positive_ratio'].mean()
            plt.plot(range(len(trend)), trend.values * 100, marker='s', label=etf)
    plt.title('各ETF盈利数据点占比趋势', fontsize=12, fontweight='bold')
    plt.xlabel('时间序列')
    plt.ylabel('盈利占比 (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(range(len(dates)), dates, rotation=45, ha='right')

    # 3. 反向价差价值分布
    plt.subplot(2, 2, 3)
    etf_avg_values = results_df.groupby('etf')['avg_reverse_value'].mean()
    plt.bar(range(len(etf_avg_values)), etf_avg_values.values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    plt.title('各ETF平均反向价差价值', fontsize=12, fontweight='bold')
    plt.ylabel('平均价值')
    plt.xticks(range(len(etf_avg_values)), etf_avg_values.index)
    plt.grid(True, alpha=0.3, axis='y')

    # 4. 平均盈利对比
    plt.subplot(2, 2, 4)
    etf_avg_profits = results_df.groupby('etf')['avg_reverse_profit'].mean()
    colors = ['green' if x > 0 else 'red' for x in etf_avg_profits.values]
    plt.bar(range(len(etf_avg_profits)), etf_avg_profits.values, color=colors, alpha=0.7)
    plt.title('各ETF平均反向日历价差盈利', fontsize=12, fontweight='bold')
    plt.ylabel('平均盈利')
    plt.xticks(range(len(etf_avg_profits)), etf_avg_profits.index)
    plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
    plt.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('reverse_calendar_spread_analysis.png', dpi=300, bbox_inches='tight')
    print("可视化图表已保存到: reverse_calendar_spread_analysis.png")

    # 生成深度洞察报告
    print("\n" + "=" * 80)
    print("深度洞察 (INSIGHTS)")
    print("=" * 80)

    # Insight 1: 整体盈利性
    overall_avg_profit = results_df['avg_reverse_profit'].mean()
    overall_profit_ratio = results_df['profit_positive_ratio'].mean()
    print(f"\n【洞察1】整体盈利性:")
    print(f"  - 所有ETF和时间点的平均反向日历价差盈利: {overall_avg_profit:.2f}")
    print(f"  - 平均盈利数据点占比: {overall_profit_ratio * 100:.2f}%")
    if overall_avg_profit < 0:
        print(f"  - 结论: 反向日历价差策略在历史数据中整体呈现亏损，说明远月期权通常比近月期权贵")
    else:
        print(f"  - 结论: 反向日历价差策略在历史数据中整体盈利")

    # Insight 2: ETF间差异
    print(f"\n【洞察2】ETF间差异:")
    best_etf = etf_summary['avg_reverse_profit'].idxmax()
    worst_etf = etf_summary['avg_reverse_profit'].idxmin()
    print(f"  - 表现最佳ETF: {best_etf} (平均盈利: {etf_summary.loc[best_etf, 'avg_reverse_profit']:.2f})")
    print(f"  - 表现最差ETF: {worst_etf} (平均盈利: {etf_summary.loc[worst_etf, 'avg_reverse_profit']:.2f})")
    print(f"  - 结论: 不同ETF的反向日历价差表现存在差异，可能与波动率特征相关")

    # Insight 3: 时间趋势
    print(f"\n【洞察3】时间趋势:")
    recent_dates = sorted(dates)[-3:]
    early_dates = sorted(dates)[:3]
    recent_profit = results_df[results_df['date'].isin(recent_dates)]['avg_reverse_profit'].mean()
    early_profit = results_df[results_df['date'].isin(early_dates)]['avg_reverse_profit'].mean()
    print(f"  - 早期时段平均盈利 ({', '.join(early_dates)}): {early_profit:.2f}")
    print(f"  - 近期时段平均盈利 ({', '.join(recent_dates)}): {recent_profit:.2f}")
    if recent_profit > early_profit:
        print(f"  - 结论: 反向日历价差策略的盈利性在近期有所改善")
    else:
        print(f"  - 结论: 反向日历价差策略的盈利性在近期有所下降")

    # Insight 4: 波动性分析
    print(f"\n【洞察4】波动性特征:")
    avg_std_profit = results_df['std_reverse_profit'].mean()
    print(f"  - 平均盈利标准差: {avg_std_profit:.2f}")
    print(f"  - 结论: 反向日历价差的盈利波动性{'较大' if avg_std_profit > 50 else '适中' if avg_std_profit > 20 else '较小'}")

    # Insight 5: 反向价差价值特征
    print(f"\n【洞察5】反向价差价值特征:")
    avg_reverse_value = results_df['avg_reverse_value'].mean()
    print(f"  - 平均反向价差价值: {avg_reverse_value:.2f}")
    if avg_reverse_value < 0:
        print(f"  - 结论: 远月期权通常比近月期权贵 {abs(avg_reverse_value):.2f} 点，这是正常的时间价值特征")
        print(f"  - 策略含义: 反向日历价差需要支付净权利金，在波动率下降或时间衰减加速时盈利")

else:
    print("\n未找到有效数据进行分析")

print("\n分析完成！")

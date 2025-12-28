#!/usr/bin/env python3
"""
分析50ETF反向日历价差的最佳卖出时间和特征
"""

import pandas as pd
import numpy as np
import glob
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# 数据目录
data_dir = "07_Option_Data/Reverse"

# 获取所有日期
dates = []
for folder in os.listdir(data_dir):
    folder_path = os.path.join(data_dir, folder)
    if os.path.isdir(folder_path) and folder.isdigit():
        dates.append(folder)
dates.sort()

print("=" * 80)
print("50ETF反向日历价差 - 最佳卖出时间分析")
print("=" * 80)
print(f"\n找到 {len(dates)} 个日期的数据: {dates}\n")

all_best_exits = []
all_timing_analysis = []

for date in dates:
    print(f"\n{'='*60}")
    print(f"日期: {date}")
    print(f"{'='*60}")

    # 构建文件路径
    file_pattern = f"{data_dir}/{date}/data/option_Reverse_50ETF_{date}.csv"
    files = glob.glob(file_pattern)

    if not files:
        print(f"未找到数据文件")
        continue

    file_path = files[0]

    try:
        # 读取数据
        df = pd.read_csv(file_path)

        # 找到profit列
        profit_cols = [col for col in df.columns if 'reverse_profit' in col.lower()]

        if not profit_cols:
            print(f"未找到profit列")
            continue

        profit_col = profit_cols[0]

        # 添加时间序列索引
        df['time_index'] = range(len(df))
        df['time_minutes'] = df['time_index'] * 1  # 假设每分钟一个数据点

        # 计算统计指标
        max_profit = df[profit_col].max()
        max_profit_idx = df[profit_col].idxmax()
        max_profit_time = df.loc[max_profit_idx, 'Now Time'] if 'Now Time' in df.columns else df.loc[max_profit_idx, 'time_index']

        min_profit = df[profit_col].min()
        min_profit_idx = df[profit_col].idxmin()

        avg_profit = df[profit_col].mean()
        final_profit = df[profit_col].iloc[-1]

        # 计算在不同持仓时间下的平均盈利
        # 分为早盘、午盘、尾盘
        total_points = len(df)
        early_session = df[df['time_index'] < total_points * 0.33]
        mid_session = df[(df['time_index'] >= total_points * 0.33) & (df['time_index'] < total_points * 0.67)]
        late_session = df[df['time_index'] >= total_points * 0.67]

        print(f"\n盈利统计:")
        print(f"  最大盈利: {max_profit:.2f} 点 (时间: {max_profit_time})")
        print(f"  最小盈利: {min_profit:.2f} 点")
        print(f"  平均盈利: {avg_profit:.2f} 点")
        print(f"  收盘盈利: {final_profit:.2f} 点")

        print(f"\n分时段统计:")
        print(f"  早盘平均盈利: {early_session[profit_col].mean():.2f} 点")
        print(f"  午盘平均盈利: {mid_session[profit_col].mean():.2f} 点")
        print(f"  尾盘平均盈利: {late_session[profit_col].mean():.2f} 点")

        # 找出盈利超过阈值的时间点
        thresholds = [10, 20, 50, 100, 200]
        print(f"\n达到盈利阈值的时间:")
        for threshold in thresholds:
            above_threshold = df[df[profit_col] >= threshold]
            if len(above_threshold) > 0:
                first_time = above_threshold.iloc[0]['Now Time'] if 'Now Time' in df.columns else above_threshold.iloc[0]['time_index']
                percent = len(above_threshold) / len(df) * 100
                print(f"  >={threshold}点: 首次达到 {first_time}, 持续 {percent:.1f}% 的时间")

        # 保存最佳卖出点
        all_best_exits.append({
            'date': date,
            'max_profit': max_profit,
            'max_profit_time': max_profit_time,
            'avg_profit': avg_profit,
            'final_profit': final_profit,
            'early_avg': early_session[profit_col].mean(),
            'mid_avg': mid_session[profit_col].mean(),
            'late_avg': late_session[profit_col].mean(),
            'data_points': len(df),
            'profit_positive_pct': (df[profit_col] > 0).sum() / len(df) * 100
        })

        # 分析持仓时间与盈利的关系
        # 每隔10%的时间点采样
        for pct in range(10, 101, 10):
            idx = int(len(df) * pct / 100) - 1
            if idx >= 0 and idx < len(df):
                timing_profit = df.iloc[idx][profit_col]
                all_timing_analysis.append({
                    'date': date,
                    'hold_pct': pct,
                    'profit': timing_profit
                })

    except Exception as e:
        print(f"  错误: {e}")

# 转换为DataFrame
exits_df = pd.DataFrame(all_best_exits)
timing_df = pd.DataFrame(all_timing_analysis)

if len(exits_df) > 0:
    print("\n" + "=" * 80)
    print("50ETF综合分析")
    print("=" * 80)

    print("\n各日期最佳卖出点汇总:")
    print("-" * 60)
    print(exits_df[['date', 'max_profit', 'avg_profit', 'final_profit', 'profit_positive_pct']].to_string(index=False))

    print(f"\n整体统计:")
    print(f"  平均最大盈利: {exits_df['max_profit'].mean():.2f} 点")
    print(f"  平均日均盈利: {exits_df['avg_profit'].mean():.2f} 点")
    print(f"  平均收盘盈利: {exits_df['final_profit'].mean():.2f} 点")
    print(f"  从最大盈利到收盘的平均回撤: {(exits_df['max_profit'] - exits_df['final_profit']).mean():.2f} 点")
    print(f"  平均盈利时间占比: {exits_df['profit_positive_pct'].mean():.2f}%")

    print(f"\n分时段平均盈利:")
    print(f"  早盘: {exits_df['early_avg'].mean():.2f} 点")
    print(f"  午盘: {exits_df['mid_avg'].mean():.2f} 点")
    print(f"  尾盘: {exits_df['late_avg'].mean():.2f} 点")

    # 找出最佳持仓时间比例
    if len(timing_df) > 0:
        print(f"\n持仓时间与盈利关系:")
        print("-" * 60)
        timing_summary = timing_df.groupby('hold_pct')['profit'].agg(['mean', 'std', 'max', 'min']).round(2)
        timing_summary.columns = ['平均盈利', '标准差', '最大盈利', '最小盈利']
        print(timing_summary)

        best_hold_pct = timing_summary['平均盈利'].idxmax()
        print(f"\n✅ 最佳持仓时间比例: {best_hold_pct}% (平均盈利: {timing_summary.loc[best_hold_pct, '平均盈利']:.2f} 点)")

    # 可视化
    print("\n生成可视化图表...")

    fig, axes = plt.subplots(2, 2, figsize=(15, 12))

    # 1. 各日期最大盈利 vs 收盘盈利
    ax1 = axes[0, 0]
    x = range(len(exits_df))
    ax1.plot(x, exits_df['max_profit'].values, marker='o', label='Max Profit', color='green', linewidth=2)
    ax1.plot(x, exits_df['final_profit'].values, marker='s', label='Final Profit', color='blue', linewidth=2)
    ax1.plot(x, exits_df['avg_profit'].values, marker='^', label='Avg Profit', color='orange', linewidth=2)
    ax1.set_title('50ETF: Max vs Final vs Avg Profit by Date', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Date Index')
    ax1.set_ylabel('Profit (points)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='red', linestyle='--', linewidth=1)
    ax1.set_xticks(x)
    ax1.set_xticklabels(exits_df['date'], rotation=45, ha='right')

    # 2. 分时段平均盈利对比
    ax2 = axes[0, 1]
    session_data = [
        exits_df['early_avg'].mean(),
        exits_df['mid_avg'].mean(),
        exits_df['late_avg'].mean()
    ]
    sessions = ['Early Session', 'Mid Session', 'Late Session']
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    bars = ax2.bar(sessions, session_data, color=colors, alpha=0.7)
    ax2.set_title('50ETF: Average Profit by Trading Session', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Average Profit (points)')
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)

    # 在柱子上标注数值
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom' if height > 0 else 'top')

    # 3. 持仓时间与盈利关系
    if len(timing_df) > 0:
        ax3 = axes[1, 0]
        timing_summary = timing_df.groupby('hold_pct')['profit'].mean()
        ax3.plot(timing_summary.index, timing_summary.values, marker='o', linewidth=2, markersize=8, color='purple')
        ax3.fill_between(timing_summary.index, 0, timing_summary.values, alpha=0.3, color='purple')
        ax3.set_title('50ETF: Profit by Holding Time %', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Holding Time (%)')
        ax3.set_ylabel('Average Profit (points)')
        ax3.grid(True, alpha=0.3)
        ax3.axhline(y=0, color='red', linestyle='--', linewidth=1)

        # 标注最佳点
        best_idx = timing_summary.idxmax()
        best_val = timing_summary.max()
        ax3.scatter([best_idx], [best_val], color='red', s=200, zorder=5, marker='*')
        ax3.annotate(f'Best: {best_idx}%\n{best_val:.1f} pts',
                    xy=(best_idx, best_val),
                    xytext=(best_idx + 10, best_val + 5),
                    fontsize=10,
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    # 4. 盈利时间占比
    ax4 = axes[1, 1]
    ax4.bar(range(len(exits_df)), exits_df['profit_positive_pct'].values,
            color=['green' if p > 50 else 'orange' if p > 30 else 'red' for p in exits_df['profit_positive_pct']],
            alpha=0.7)
    ax4.set_title('50ETF: Profitable Time Percentage', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Date Index')
    ax4.set_ylabel('Profitable Time (%)')
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.axhline(y=50, color='black', linestyle='--', linewidth=1, label='50% line')
    ax4.set_xticks(range(len(exits_df)))
    ax4.set_xticklabels(exits_df['date'], rotation=45, ha='right')
    ax4.legend()

    plt.tight_layout()
    output_file = '07_Option_Data/50etf_best_exit_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"图表已保存到: {output_file}")

    # 保存详细数据
    csv_file = '07_Option_Data/50etf_best_exit_data.csv'
    exits_df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"详细数据已保存到: {csv_file}")

    # 生成Markdown报告
    md_file = '07_Option_Data/50etf_best_exit_insights.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 50ETF反向日历价差 - 最佳卖出时间分析\n\n")
        f.write(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**数据时间范围**: {dates[0]} - {dates[-1]}  \n")
        f.write(f"**分析日期数**: {len(exits_df)}  \n\n")
        f.write("---\n\n")

        f.write("## 🎯 关键发现\n\n")

        avg_max = exits_df['max_profit'].mean()
        avg_daily = exits_df['avg_profit'].mean()
        avg_final = exits_df['final_profit'].mean()
        avg_drawdown = (exits_df['max_profit'] - exits_df['final_profit']).mean()
        avg_profit_time = exits_df['profit_positive_pct'].mean()

        f.write(f"### 盈利统计\n\n")
        f.write(f"- **平均最大盈利**: {avg_max:.2f} 点\n")
        f.write(f"- **平均日均盈利**: {avg_daily:.2f} 点\n")
        f.write(f"- **平均收盘盈利**: {avg_final:.2f} 点\n")
        f.write(f"- **平均回撤**: {avg_drawdown:.2f} 点\n")
        f.write(f"- **平均盈利时间占比**: {avg_profit_time:.2f}%\n\n")

        # 对比500ETF
        f.write(f"### 与500ETF对比\n\n")
        f.write(f"| 指标 | 50ETF | 500ETF |\n")
        f.write(f"|------|-------|--------|\n")
        f.write(f"| 平均日均盈利 | {avg_daily:.2f} | 177.88 |\n")
        f.write(f"| 平均收盘盈利 | {avg_final:.2f} | -46.00 |\n")
        f.write(f"| 盈利时间占比 | {avg_profit_time:.2f}% | 44.50% |\n\n")

        f.write(f"### 分时段表现\n\n")
        early_avg = exits_df['early_avg'].mean()
        mid_avg = exits_df['mid_avg'].mean()
        late_avg = exits_df['late_avg'].mean()

        sessions = [('早盘', early_avg), ('午盘', mid_avg), ('尾盘', late_avg)]
        sessions_sorted = sorted(sessions, key=lambda x: x[1], reverse=True)

        for i, (name, val) in enumerate(sessions_sorted):
            emoji = '🥇' if i == 0 else '🥈' if i == 1 else '🥉'
            f.write(f"- {emoji} **{name}**: {val:.2f} 点\n")
        f.write("\n")

        if len(timing_df) > 0:
            timing_summary = timing_df.groupby('hold_pct')['profit'].mean()
            best_hold_pct = timing_summary.idxmax()
            best_hold_profit = timing_summary.max()

            f.write(f"### 最佳持仓时间\n\n")
            f.write(f"- **最佳持仓比例**: {best_hold_pct}%\n")
            f.write(f"- **该时点平均盈利**: {best_hold_profit:.2f} 点\n\n")

        f.write("## 💡 50ETF独特特征\n\n")

        # 分析50ETF的特点
        if avg_profit_time > 50:
            f.write(f"1. ✅ **高胜率**: 盈利时间占比{avg_profit_time:.1f}%，表现稳定\n")
        else:
            f.write(f"1. ⚠️ **胜率较低**: 盈利时间占比{avg_profit_time:.1f}%，需谨慎\n")

        if abs(avg_final) < 50:
            f.write(f"2. ✅ **收盘表现好**: 平均收盘盈利{avg_final:.2f}点，持有到收盘损失小\n")
        else:
            f.write(f"2. ⚠️ **收盘回撤大**: 平均收盘盈利{avg_final:.2f}点，建议提前平仓\n")

        if avg_max < 500:
            f.write(f"3. 📊 **波动性较小**: 平均最大盈利{avg_max:.2f}点，适合稳健投资者\n")
        else:
            f.write(f"3. 📊 **波动性较大**: 平均最大盈利{avg_max:.2f}点，有机会也有风险\n")

        f.write("\n")

        f.write("## 📋 历史数据详情\n\n")
        f.write("| 日期 | 最大盈利 | 平均盈利 | 收盘盈利 | 盈利时间% |\n")
        f.write("|------|----------|----------|----------|----------|\n")

        for _, row in exits_df.iterrows():
            f.write(f"| {row['date']} | {row['max_profit']:.2f} | {row['avg_profit']:.2f} | {row['final_profit']:.2f} | {row['profit_positive_pct']:.1f}% |\n")

        f.write("\n")

    print(f"Markdown报告已保存到: {md_file}")

else:
    print("\n未找到有效数据进行分析")

print("\n分析完成！")

#!/usr/bin/env python3
"""
分析反向日历价差在距离到期日还剩多少天时卖出最合适
"""

import pandas as pd
import numpy as np
import glob
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
import re

# 数据目录
data_dir = "07_Option_Data/Reverse"

# 中国ETF期权到期日：每月第四个星期三
def get_fourth_wednesday(year, month):
    """获取指定年月的第四个星期三"""
    # 找到该月第一天
    first_day = datetime(year, month, 1)
    # 找到第一个星期三
    days_until_wednesday = (2 - first_day.weekday()) % 7
    first_wednesday = first_day + timedelta(days=days_until_wednesday)
    # 第四个星期三
    fourth_wednesday = first_wednesday + timedelta(weeks=3)
    return fourth_wednesday

# 获取所有日期
dates = []
for folder in os.listdir(data_dir):
    folder_path = os.path.join(data_dir, folder)
    if os.path.isdir(folder_path) and folder.isdigit():
        dates.append(folder)
dates.sort()

print("=" * 80)
print("反向日历价差 - 距离到期日最佳卖出时间分析")
print("=" * 80)

all_results = []

for date_str in dates:
    print(f"\n{'='*60}")
    print(f"数据日期: {date_str}")
    print(f"{'='*60}")

    # 解析数据日期
    data_date = datetime.strptime(date_str, '%Y%m%d')

    # 读取500ETF数据
    file_pattern = f"{data_dir}/{date_str}/data/option_Reverse_500ETF_{date_str}.csv"
    files = glob.glob(file_pattern)

    if not files:
        print(f"未找到数据文件")
        continue

    file_path = files[0]

    try:
        # 读取CSV头部，获取期权合约月份
        df = pd.read_csv(file_path, nrows=1)
        columns = df.columns.tolist()

        # 提取期权合约月份
        call_months = []
        for col in columns:
            match = re.search(r'call_(\d{6})_', col)
            if match:
                call_months.append(match.group(1))

        if len(call_months) < 2:
            print(f"未找到足够的期权合约信息")
            continue

        # 近月和远月
        near_month = call_months[0]  # 第一个是近月
        far_month = call_months[1]   # 第二个是远月

        # 解析到期月份
        near_year = int(near_month[:4])
        near_mon = int(near_month[4:6])
        far_year = int(far_month[:4])
        far_mon = int(far_month[4:6])

        # 计算到期日
        near_expiry = get_fourth_wednesday(near_year, near_mon)
        far_expiry = get_fourth_wednesday(far_year, far_mon)

        # 计算距离到期日的天数
        days_to_near_expiry = (near_expiry - data_date).days
        days_to_far_expiry = (far_expiry - data_date).days

        print(f"近月合约: {near_month} (到期日: {near_expiry.strftime('%Y-%m-%d')})")
        print(f"远月合约: {far_month} (到期日: {far_expiry.strftime('%Y-%m-%d')})")
        print(f"距近月到期: {days_to_near_expiry} 天")
        print(f"距远月到期: {days_to_far_expiry} 天")

        # 读取完整数据，分析盈利
        df_full = pd.read_csv(file_path)
        profit_cols = [col for col in df_full.columns if 'reverse_profit' in col.lower()]

        if not profit_cols:
            print(f"未找到profit列")
            continue

        profit_col = profit_cols[0]

        # 分析每一天的盈利情况
        # 解析时间列
        time_col = 'Now Time'
        if time_col not in df_full.columns:
            print(f"未找到时间列")
            continue

        df_full['datetime'] = pd.to_datetime(df_full[time_col], errors='coerce')
        df_full = df_full.dropna(subset=['datetime'])

        # 按日期分组，计算每日平均盈利和最大盈利
        df_full['date'] = df_full['datetime'].dt.date
        daily_stats = df_full.groupby('date')[profit_col].agg(['mean', 'max', 'min', 'last']).reset_index()

        # 计算每一天距离近月到期日的天数
        daily_stats['datetime'] = pd.to_datetime(daily_stats['date'])
        daily_stats['days_to_expiry'] = daily_stats['datetime'].apply(
            lambda x: (near_expiry - x).days
        )

        print(f"\n每日盈利统计 (前5天和后5天):")
        print(daily_stats[['date', 'days_to_expiry', 'mean', 'max', 'last']].head(5).to_string(index=False))
        print("...")
        print(daily_stats[['date', 'days_to_expiry', 'mean', 'max', 'last']].tail(5).to_string(index=False))

        # 找出最佳卖出日期（平均盈利最高的日期）
        best_day_idx = daily_stats['mean'].idxmax()
        best_day = daily_stats.loc[best_day_idx]

        print(f"\n最佳卖出日:")
        print(f"  日期: {best_day['date']}")
        print(f"  距近月到期: {best_day['days_to_expiry']} 天")
        print(f"  平均盈利: {best_day['mean']:.2f} 点")
        print(f"  最大盈利: {best_day['max']:.2f} 点")

        # 保存结果
        for _, row in daily_stats.iterrows():
            all_results.append({
                'data_date': date_str,
                'trade_date': row['date'],
                'days_to_expiry': row['days_to_expiry'],
                'avg_profit': row['mean'],
                'max_profit': row['max'],
                'final_profit': row['last'],
                'near_expiry': near_expiry.strftime('%Y-%m-%d'),
                'far_expiry': far_expiry.strftime('%Y-%m-%d')
            })

    except Exception as e:
        print(f"  错误: {e}")
        import traceback
        traceback.print_exc()

# 转换为DataFrame
results_df = pd.DataFrame(all_results)

if len(results_df) > 0:
    print("\n" + "=" * 80)
    print("综合分析 - 通用规律")
    print("=" * 80)

    # 按距离到期日天数分组，计算平均盈利
    days_summary = results_df.groupby('days_to_expiry')['avg_profit'].agg(['mean', 'std', 'count', 'max', 'min']).reset_index()
    days_summary = days_summary.sort_values('days_to_expiry', ascending=False)
    days_summary.columns = ['距到期天数', '平均盈利', '标准差', '样本数', '最大值', '最小值']

    print("\n按距到期天数统计 (样本数>=3的天数):")
    print("-" * 80)
    filtered_summary = days_summary[days_summary['样本数'] >= 3].round(2)
    print(filtered_summary.to_string(index=False))

    # 找出最佳卖出天数
    best_days = filtered_summary[filtered_summary['样本数'] >= 3].nlargest(5, '平均盈利')

    print(f"\n✅ Top 5 最佳卖出时间 (距近月到期日):")
    print("-" * 80)
    for idx, row in best_days.iterrows():
        print(f"  {int(row['距到期天数'])} 天前: 平均盈利 {row['平均盈利']:.2f} 点 (样本数: {int(row['样本数'])})")

    # 分析不同时间段的盈利特征
    print(f"\n📊 按时间段统计:")
    print("-" * 80)

    # 定义时间段
    segments = [
        ("超长期 (>60天)", results_df[results_df['days_to_expiry'] > 60]),
        ("长期 (40-60天)", results_df[(results_df['days_to_expiry'] >= 40) & (results_df['days_to_expiry'] <= 60)]),
        ("中期 (20-40天)", results_df[(results_df['days_to_expiry'] >= 20) & (results_df['days_to_expiry'] < 40)]),
        ("短期 (10-20天)", results_df[(results_df['days_to_expiry'] >= 10) & (results_df['days_to_expiry'] < 20)]),
        ("临期 (<10天)", results_df[results_df['days_to_expiry'] < 10])
    ]

    for name, segment_df in segments:
        if len(segment_df) > 0:
            avg = segment_df['avg_profit'].mean()
            std = segment_df['avg_profit'].std()
            count = len(segment_df)
            print(f"  {name}: 平均盈利 {avg:.2f} 点 (标准差: {std:.2f}, 样本数: {count})")

    # 可视化
    print("\n生成可视化图表...")

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # 1. 距到期天数 vs 平均盈利
    ax1 = axes[0, 0]
    filtered_for_plot = days_summary[days_summary['样本数'] >= 3]
    ax1.scatter(filtered_for_plot['距到期天数'], filtered_for_plot['平均盈利'],
                s=filtered_for_plot['样本数']*10, alpha=0.6, c=filtered_for_plot['平均盈利'],
                cmap='RdYlGn', edgecolors='black', linewidth=1)
    ax1.axhline(y=0, color='red', linestyle='--', linewidth=1)
    ax1.set_title('Avg Profit by Days to Expiry (Size=Sample Count)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Days to Near Month Expiry')
    ax1.set_ylabel('Average Profit (points)')
    ax1.grid(True, alpha=0.3)

    # 标注最佳点
    if len(best_days) > 0:
        best = best_days.iloc[0]
        ax1.scatter([best['距到期天数']], [best['平均盈利']],
                   s=500, marker='*', color='gold', edgecolors='red', linewidth=2, zorder=5)
        ax1.annotate(f"Best: {int(best['距到期天数'])} days\n{best['平均盈利']:.0f} pts",
                    xy=(best['距到期天数'], best['平均盈利']),
                    xytext=(best['距到期天数'] + 10, best['平均盈利'] + 200),
                    fontsize=10, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=2))

    # 2. 分时间段的盈利分布
    ax2 = axes[0, 1]
    segment_names = []
    segment_avgs = []
    segment_stds = []

    for name, segment_df in segments:
        if len(segment_df) > 0:
            segment_names.append(name.split('(')[0].strip())
            segment_avgs.append(segment_df['avg_profit'].mean())
            segment_stds.append(segment_df['avg_profit'].std())

    bars = ax2.bar(range(len(segment_names)), segment_avgs,
                   yerr=segment_stds, capsize=5, alpha=0.7,
                   color=['#FF6B6B', '#FFA07A', '#FFD700', '#90EE90', '#87CEEB'])
    ax2.set_xticks(range(len(segment_names)))
    ax2.set_xticklabels(segment_names, rotation=15, ha='right')
    ax2.set_title('Average Profit by Time Period', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Average Profit (points)')
    ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
    ax2.grid(True, alpha=0.3, axis='y')

    # 在柱子上标注数值
    for i, (bar, val) in enumerate(zip(bars, segment_avgs)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.0f}',
                ha='center', va='bottom' if height > 0 else 'top', fontsize=9)

    # 3. 每个数据集的最佳卖出时间
    ax3 = axes[1, 0]
    dataset_best = results_df.groupby('data_date').apply(
        lambda x: x.loc[x['avg_profit'].idxmax()]
    ).reset_index(drop=True)

    x_pos = range(len(dataset_best))
    colors = ['green' if d > 0 else 'red' for d in dataset_best['days_to_expiry']]
    bars = ax3.bar(x_pos, dataset_best['days_to_expiry'], color=colors, alpha=0.7)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(dataset_best['data_date'], rotation=45, ha='right')
    ax3.set_title('Best Exit Days for Each Dataset', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Days to Expiry')
    ax3.grid(True, alpha=0.3, axis='y')

    # 标注平均值
    avg_best_days = dataset_best['days_to_expiry'].mean()
    ax3.axhline(y=avg_best_days, color='orange', linestyle='--', linewidth=2,
                label=f'Avg: {avg_best_days:.1f} days')
    ax3.legend()

    # 4. 盈利趋势图（移动平均）
    ax4 = axes[1, 1]
    # 按距到期天数排序
    days_sorted = days_summary.sort_values('距到期天数', ascending=False)

    # 过滤样本数>=2的数据点
    days_filtered = days_sorted[days_sorted['样本数'] >= 2]

    ax4.plot(days_filtered['距到期天数'], days_filtered['平均盈利'],
            marker='o', linewidth=2, markersize=6, color='purple', alpha=0.7)
    ax4.fill_between(days_filtered['距到期天数'], 0, days_filtered['平均盈利'],
                     alpha=0.3, color='purple')
    ax4.axhline(y=0, color='red', linestyle='--', linewidth=1)
    ax4.set_title('Profit Trend by Days to Expiry', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Days to Near Month Expiry')
    ax4.set_ylabel('Average Profit (points)')
    ax4.grid(True, alpha=0.3)
    ax4.invert_xaxis()  # 反转x轴，使时间从右到左流动

    plt.tight_layout()
    output_file = '07_Option_Data/days_to_expiry_analysis.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"图表已保存到: {output_file}")

    # 保存详细数据
    csv_file = '07_Option_Data/days_to_expiry_data.csv'
    results_df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    print(f"详细数据已保存到: {csv_file}")

    # 保存汇总数据
    summary_csv = '07_Option_Data/days_to_expiry_summary.csv'
    days_summary.to_csv(summary_csv, index=False, encoding='utf-8-sig')
    print(f"汇总数据已保存到: {summary_csv}")

    # 生成Markdown报告
    md_file = '07_Option_Data/days_to_expiry_insights.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# 反向日历价差 - 距到期日最佳卖出时间分析\n\n")
        f.write(f"**分析时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
        f.write(f"**数据集数量**: {results_df['data_date'].nunique()}  \n")
        f.write(f"**总样本数**: {len(results_df)}  \n\n")
        f.write("---\n\n")

        f.write("## 🎯 核心发现：最佳卖出时间\n\n")

        if len(best_days) > 0:
            f.write("### Top 5 最佳卖出时机（距近月到期日）\n\n")
            for i, (idx, row) in enumerate(best_days.iterrows()):
                emoji = '🥇' if i == 0 else '🥈' if i == 1 else '🥉' if i == 2 else '📌'
                f.write(f"{i+1}. {emoji} **{int(row['距到期天数'])} 天前**: ")
                f.write(f"平均盈利 **{row['平均盈利']:.2f}** 点 ")
                f.write(f"(样本数: {int(row['样本数'])}, 标准差: {row['标准差']:.2f})\n")
            f.write("\n")

        f.write("## 📊 按时间段统计\n\n")
        f.write("| 时间段 | 平均盈利 | 标准差 | 样本数 |\n")
        f.write("|--------|----------|--------|--------|\n")

        for name, segment_df in segments:
            if len(segment_df) > 0:
                avg = segment_df['avg_profit'].mean()
                std = segment_df['avg_profit'].std()
                count = len(segment_df)
                f.write(f"| {name} | {avg:.2f} | {std:.2f} | {count} |\n")
        f.write("\n")

        f.write("## 💡 策略建议\n\n")

        if len(best_days) > 0:
            best = best_days.iloc[0]
            f.write(f"1. **最优卖出时机**: 距近月到期 **{int(best['距到期天数'])}** 天时平仓\n")
            f.write(f"   - 该时点平均盈利: **{best['平均盈利']:.2f}** 点\n")
            f.write(f"   - 统计可靠性: {int(best['样本数'])} 个样本\n\n")

        # 分析每个数据集的最佳卖出时间
        avg_best_days = dataset_best['days_to_expiry'].mean()
        median_best_days = dataset_best['days_to_expiry'].median()

        f.write(f"2. **各数据集最佳卖出日统计**:\n")
        f.write(f"   - 平均最佳卖出时间: 距到期 **{avg_best_days:.1f}** 天\n")
        f.write(f"   - 中位数: 距到期 **{median_best_days:.0f}** 天\n\n")

        f.write("3. **时间段建议**:\n")
        best_segment = max(segments, key=lambda x: x[1]['avg_profit'].mean() if len(x[1]) > 0 else -float('inf'))
        f.write(f"   - 表现最佳时间段: **{best_segment[0]}**\n")
        f.write(f"   - 平均盈利: {best_segment[1]['avg_profit'].mean():.2f} 点\n\n")

        # 风险提示
        f.write("## ⚠️ 风险提示\n\n")

        # 计算波动性
        high_volatility_days = days_summary[days_summary['标准差'] > 500]
        if len(high_volatility_days) > 0:
            f.write("**高波动性时段** (标准差>500):\n\n")
            for _, row in high_volatility_days.head(5).iterrows():
                f.write(f"- 距到期 {int(row['距到期天数'])} 天: 标准差 {row['标准差']:.2f} 点\n")
            f.write("\n")

        f.write("## 📋 各数据集详情\n\n")
        f.write("| 数据日期 | 最佳卖出日 | 距到期天数 | 盈利 |\n")
        f.write("|----------|------------|------------|------|\n")

        for _, row in dataset_best.iterrows():
            f.write(f"| {row['data_date']} | {row['trade_date']} | {int(row['days_to_expiry'])} 天 | {row['avg_profit']:.2f} 点 |\n")

        f.write("\n")

    print(f"Markdown报告已保存到: {md_file}")

else:
    print("\n未找到有效数据进行分析")

print("\n分析完成！")

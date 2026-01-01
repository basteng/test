#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金业绩分析报告
分析基金的操作水平和改进建议
"""

import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
rcParams['axes.unicode_minus'] = False

# 基金数据
data = {
    '日期': ['2025/4/21', '2025/4/25', '2025/4/28', '2025/5/6', '2025/5/29',
            '2025/8/24', '2025/11/2', '2025/12/17', '2025/12/26', '2025/12/31'],
    '净值': [1, 0.9996, 0.9991, 0.9983, 0.9961, 1.058, 1.0929, 1.1156, 1.1221, 1.1272],
    '年化': [0.00, -3.44, -4.59, -4.01, -3.64, 20.37, 19.51, 19.17, 19.51, 20.17],
    '上证指数': [3276.73, 3297.29, 3288.41, 3316.11, 3363.45, 3825.76, 3958.38, 3870.8, 3963.68, 3968.84],
    '美国十年期国债': [4.4341, 4.315, 4.269, 4.367, 4.519, 4.258, 4.099, 4.167, 4.153, 4.119],
    '上证50': [2657.64, 2655.36, 2651.23, 2647.72, 2690.89, 2928.61, 3005.41, 2993.13, 3045.4, 3031.13],
    '沪深300': [3772.52, 3784.36, 3781.62, 3808.54, 3858.7, 4378, 4622.67, 4579.72, 4657.24, 4629.94],
    '中国十年期国债': [1.65, 1.667, 1.656, 1.632, 1.724, 1.789, 1.746, 1.844, 1.833, 1.848],
    '美元汇率': [7.3195, 7.3088, 7.3144, 7.2045, 7.2061, 7.1567, 7.1047, 7.0387, 6.9957, 6.982]
}

df = pd.DataFrame(data)
df['日期'] = pd.to_datetime(df['日期'])

# 计算关键指标
def analyze_fund_performance(df):
    """分析基金业绩表现"""

    print("=" * 80)
    print("基金业绩分析报告")
    print("=" * 80)
    print()

    # 1. 基本收益指标
    print("【一、收益表现分析】")
    print("-" * 80)

    total_return = (df['净值'].iloc[-1] / df['净值'].iloc[0] - 1) * 100
    days = (df['日期'].iloc[-1] - df['日期'].iloc[0]).days
    annualized_return = df['年化'].iloc[-1]

    print(f"统计区间: {df['日期'].iloc[0].strftime('%Y-%m-%d')} 至 {df['日期'].iloc[-1].strftime('%Y-%m-%d')}")
    print(f"统计天数: {days} 天")
    print(f"累计收益率: {total_return:.2f}%")
    print(f"年化收益率: {annualized_return:.2f}%")
    print()

    # 最大回撤
    df['累计最大净值'] = df['净值'].cummax()
    df['回撤'] = (df['净值'] / df['累计最大净值'] - 1) * 100
    max_drawdown = df['回撤'].min()
    max_dd_date = df.loc[df['回撤'].idxmin(), '日期']

    print(f"最大回撤: {max_drawdown:.2f}%")
    print(f"最大回撤日期: {max_dd_date.strftime('%Y-%m-%d')}")
    print()

    # 2. 与市场指数对比
    print("【二、相对市场表现】")
    print("-" * 80)

    # 计算各指数涨幅
    sz_return = (df['上证指数'].iloc[-1] / df['上证指数'].iloc[0] - 1) * 100
    sz50_return = (df['上证50'].iloc[-1] / df['上证50'].iloc[0] - 1) * 100
    hs300_return = (df['沪深300'].iloc[-1] / df['沪深300'].iloc[0] - 1) * 100

    print(f"基金收益率:    {total_return:>8.2f}%")
    print(f"上证指数涨幅:  {sz_return:>8.2f}%  (超额收益: {total_return - sz_return:>6.2f}%)")
    print(f"上证50涨幅:    {sz50_return:>8.2f}%  (超额收益: {total_return - sz50_return:>6.2f}%)")
    print(f"沪深300涨幅:   {hs300_return:>8.2f}%  (超额收益: {total_return - hs300_return:>6.2f}%)")
    print()

    # 3. 波动性分析
    print("【三、风险与波动性分析】")
    print("-" * 80)

    # 计算净值变化率
    df['净值变化率'] = df['净值'].pct_change() * 100
    volatility = df['净值变化率'].std()

    print(f"净值波动率(标准差): {volatility:.2f}%")
    print(f"最大单期涨幅: {df['净值变化率'].max():.2f}%")
    print(f"最大单期跌幅: {df['净值变化率'].min():.2f}%")
    print()

    # 夏普比率估算 (假设无风险利率为3%)
    risk_free_rate = 3.0
    excess_return = annualized_return - risk_free_rate
    annualized_vol = volatility * np.sqrt(252/days)  # 年化波动率
    sharpe_ratio = excess_return / annualized_vol if annualized_vol > 0 else 0

    print(f"年化波动率: {annualized_vol:.2f}%")
    print(f"夏普比率(估算): {sharpe_ratio:.2f}")
    print()

    # 4. 阶段表现分析
    print("【四、阶段表现分析】")
    print("-" * 80)

    # 找出关键转折点
    min_value = df['净值'].min()
    min_date = df.loc[df['净值'].idxmin(), '日期']

    print(f"最低点净值: {min_value:.4f} (日期: {min_date.strftime('%Y-%m-%d')})")

    # 计算恢复阶段
    recovery_data = df[df['日期'] >= min_date]
    if len(recovery_data) > 1:
        recovery_return = (recovery_data['净值'].iloc[-1] / recovery_data['净值'].iloc[0] - 1) * 100
        recovery_days = (recovery_data['日期'].iloc[-1] - recovery_data['日期'].iloc[0]).days
        print(f"从最低点反弹: {recovery_return:.2f}% (用时{recovery_days}天)")
    print()

    # 5. 操作水平评估
    print("【五、操作水平评估】")
    print("-" * 80)

    evaluation = []

    # 评估标准
    if total_return > 10:
        evaluation.append("✓ 绝对收益表现良好 (>10%)")
    else:
        evaluation.append("△ 绝对收益有待提升")

    if total_return > sz_return and total_return > hs300_return:
        evaluation.append("✓ 成功跑赢主要市场指数")
    else:
        evaluation.append("△ 未能全面跑赢市场指数")

    if max_drawdown > -5:
        evaluation.append("✓ 风险控制较好 (最大回撤<5%)")
    elif max_drawdown > -10:
        evaluation.append("△ 风险控制一般 (最大回撤5-10%)")
    else:
        evaluation.append("✗ 风险控制需要加强 (最大回撤>10%)")

    if sharpe_ratio > 1.5:
        evaluation.append("✓ 风险调整后收益优秀 (夏普比率>1.5)")
    elif sharpe_ratio > 1.0:
        evaluation.append("△ 风险调整后收益良好 (夏普比率>1.0)")
    else:
        evaluation.append("△ 风险调整后收益有待提升")

    for item in evaluation:
        print(item)
    print()

    # 6. 改进建议
    print("【六、改进建议】")
    print("-" * 80)

    suggestions = []

    # 根据数据特征提供建议
    if max_drawdown < -2:
        suggestions.append("""
1. 加强风险管理
   - 在4-5月期间出现了回撤,建议设置更严格的止损机制
   - 考虑使用动态仓位管理,在市场不确定时降低仓位
   - 建立明确的风险预算和回撤控制目标""")

    # 检查是否抓住了市场上涨
    market_rally = df[df['日期'] >= pd.to_datetime('2025-08-24')]
    if len(market_rally) > 0:
        fund_rally = (market_rally['净值'].iloc[-1] / market_rally['净值'].iloc[0] - 1) * 100
        market_index_rally = (market_rally['上证指数'].iloc[-1] / market_rally['上证指数'].iloc[0] - 1) * 100

        suggestions.append(f"""
2. 把握市场节奏
   - 8月24日后市场出现明显上涨,基金涨幅{fund_rally:.2f}%,市场涨幅{market_index_rally:.2f}%
   - {"成功抓住了这轮上涨" if fund_rally > market_index_rally * 0.9 else "建议提高对市场拐点的判断能力"}
   - 建立系统化的仓位调整策略,在市场转暖时及时加仓""")

    suggestions.append("""
3. 优化选股策略
   - 分析持仓结构,评估是否过度集中或过度分散
   - 加强基本面研究,选择高质量、高成长性标的
   - 建立动态的股票池管理机制,及时调整不符合预期的持仓""")

    suggestions.append("""
4. 提升交易纪律
   - 建立明确的买卖决策流程和标准
   - 避免情绪化交易,坚持策略执行
   - 定期复盘交易记录,总结经验教训""")

    # 根据波动性提供建议
    if volatility > 3:
        suggestions.append("""
5. 平滑净值波动
   - 当前净值波动较大,建议增加持仓分散度
   - 考虑配置一定比例的低波动资产
   - 使用期权等衍生品工具进行对冲""")

    suggestions.append("""
6. 宏观对冲策略
   - 关注美元汇率走势(期间贬值约4.6%),考虑汇率对冲
   - 监控中美利率走势,调整股债配置比例
   - 建立宏观指标监控体系,提前应对市场环境变化""")

    for suggestion in suggestions:
        print(suggestion)

    print()
    print("=" * 80)

    return df

# 运行分析
df = analyze_fund_performance(df)

# 生成可视化图表
def create_performance_charts(df):
    """创建业绩分析图表"""

    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('基金业绩分析图表', fontsize=16, fontweight='bold')

    # 1. 净值走势图
    ax1 = axes[0, 0]
    ax1.plot(df['日期'], df['净值'], marker='o', linewidth=2, markersize=6, color='#1f77b4', label='基金净值')
    ax1.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='初始净值')
    ax1.fill_between(df['日期'], 1.0, df['净值'], where=(df['净值'] >= 1.0), alpha=0.3, color='green', label='盈利区域')
    ax1.fill_between(df['日期'], 1.0, df['净值'], where=(df['净值'] < 1.0), alpha=0.3, color='red', label='亏损区域')
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel('净值', fontsize=12)
    ax1.set_title('基金净值走势', fontsize=14, fontweight='bold')
    ax1.legend(loc='best')
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # 2. 回撤分析
    ax2 = axes[0, 1]
    ax2.fill_between(df['日期'], 0, df['回撤'], color='red', alpha=0.5, label='回撤幅度')
    ax2.plot(df['日期'], df['回撤'], color='darkred', linewidth=2, marker='o', markersize=6)
    ax2.set_xlabel('日期', fontsize=12)
    ax2.set_ylabel('回撤 (%)', fontsize=12)
    ax2.set_title('回撤分析', fontsize=14, fontweight='bold')
    ax2.legend(loc='best')
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # 3. 与市场指数对比
    ax3 = axes[1, 0]
    # 归一化处理
    df['基金归一化'] = df['净值'] / df['净值'].iloc[0] * 100
    df['上证归一化'] = df['上证指数'] / df['上证指数'].iloc[0] * 100
    df['上证50归一化'] = df['上证50'] / df['上证50'].iloc[0] * 100
    df['沪深300归一化'] = df['沪深300'] / df['沪深300'].iloc[0] * 100

    ax3.plot(df['日期'], df['基金归一化'], marker='o', linewidth=2.5, markersize=6, label='基金', color='#1f77b4')
    ax3.plot(df['日期'], df['上证归一化'], marker='s', linewidth=1.5, markersize=4, label='上证指数', color='#ff7f0e', alpha=0.7)
    ax3.plot(df['日期'], df['上证50归一化'], marker='^', linewidth=1.5, markersize=4, label='上证50', color='#2ca02c', alpha=0.7)
    ax3.plot(df['日期'], df['沪深300归一化'], marker='d', linewidth=1.5, markersize=4, label='沪深300', color='#d62728', alpha=0.7)
    ax3.axhline(y=100, color='gray', linestyle='--', alpha=0.5)
    ax3.set_xlabel('日期', fontsize=12)
    ax3.set_ylabel('相对表现 (基期=100)', fontsize=12)
    ax3.set_title('基金 vs 市场指数对比', fontsize=14, fontweight='bold')
    ax3.legend(loc='best')
    ax3.grid(True, alpha=0.3)
    ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # 4. 年化收益率变化
    ax4 = axes[1, 1]
    colors = ['green' if x >= 0 else 'red' for x in df['年化']]
    ax4.bar(df['日期'], df['年化'], color=colors, alpha=0.6, edgecolor='black')
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax4.set_xlabel('日期', fontsize=12)
    ax4.set_ylabel('年化收益率 (%)', fontsize=12)
    ax4.set_title('年化收益率变化', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig('/home/user/test/fund_performance_analysis.png', dpi=300, bbox_inches='tight')
    print("\n图表已保存至: /home/user/test/fund_performance_analysis.png")

    return fig

# 生成图表
try:
    create_performance_charts(df)
    print("\n分析完成!")
except Exception as e:
    print(f"\n生成图表时出错: {e}")
    print("文字分析报告已完成,图表生成失败可能是由于缺少matplotlib库")

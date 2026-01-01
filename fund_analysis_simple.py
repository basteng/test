#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金业绩分析报告
分析基金的操作水平和改进建议
"""

from datetime import datetime
import math

# 基金数据
data = [
    {'日期': '2025/4/21', '净值': 1, '年化': 0.00, '上证指数': 3276.73, '美国十年期国债': 4.4341, '上证50': 2657.64, '沪深300': 3772.52, '中国十年期国债': 1.65, '美元汇率': 7.3195},
    {'日期': '2025/4/25', '净值': 0.9996, '年化': -3.44, '上证指数': 3297.29, '美国十年期国债': 4.315, '上证50': 2655.36, '沪深300': 3784.36, '中国十年期国债': 1.667, '美元汇率': 7.3088},
    {'日期': '2025/4/28', '净值': 0.9991, '年化': -4.59, '上证指数': 3288.41, '美国十年期国债': 4.269, '上证50': 2651.23, '沪深300': 3781.62, '中国十年期国债': 1.656, '美元汇率': 7.3144},
    {'日期': '2025/5/6', '净值': 0.9983, '年化': -4.01, '上证指数': 3316.11, '美国十年期国债': 4.367, '上证50': 2647.72, '沪深300': 3808.54, '中国十年期国债': 1.632, '美元汇率': 7.2045},
    {'日期': '2025/5/29', '净值': 0.9961, '年化': -3.64, '上证指数': 3363.45, '美国十年期国债': 4.519, '上证50': 2690.89, '沪深300': 3858.7, '中国十年期国债': 1.724, '美元汇率': 7.2061},
    {'日期': '2025/8/24', '净值': 1.058, '年化': 20.37, '上证指数': 3825.76, '美国十年期国债': 4.258, '上证50': 2928.61, '沪深300': 4378, '中国十年期国债': 1.789, '美元汇率': 7.1567},
    {'日期': '2025/11/2', '净值': 1.0929, '年化': 19.51, '上证指数': 3958.38, '美国十年期国债': 4.099, '上证50': 3005.41, '沪深300': 4622.67, '中国十年期国债': 1.746, '美元汇率': 7.1047},
    {'日期': '2025/12/17', '净值': 1.1156, '年化': 19.17, '上证指数': 3870.8, '美国十年期国债': 4.167, '上证50': 2993.13, '沪深300': 4579.72, '中国十年期国债': 1.844, '美元汇率': 7.0387},
    {'日期': '2025/12/26', '净值': 1.1221, '年化': 19.51, '上证指数': 3963.68, '美国十年期国债': 4.153, '上证50': 3045.4, '沪深300': 4657.24, '中国十年期国债': 1.833, '美元汇率': 6.9957},
    {'日期': '2025/12/31', '净值': 1.1272, '年化': 20.17, '上证指数': 3968.84, '美国十年期国债': 4.119, '上证50': 3031.13, '沪深300': 4629.94, '中国十年期国债': 1.848, '美元汇率': 6.982}
]

def analyze_fund_performance(data):
    """分析基金业绩表现"""

    print("=" * 80)
    print("基金业绩分析报告")
    print("=" * 80)
    print()

    # 转换日期
    for item in data:
        item['日期对象'] = datetime.strptime(item['日期'], '%Y/%m/%d')

    # 1. 基本收益指标
    print("【一、收益表现分析】")
    print("-" * 80)

    first = data[0]
    last = data[-1]
    total_return = (last['净值'] / first['净值'] - 1) * 100
    days = (last['日期对象'] - first['日期对象']).days
    annualized_return = last['年化']

    print(f"统计区间: {first['日期']} 至 {last['日期']}")
    print(f"统计天数: {days} 天 (约{days/30:.1f}个月)")
    print(f"累计收益率: {total_return:.2f}%")
    print(f"年化收益率: {annualized_return:.2f}%")
    print()

    # 计算最大回撤
    max_value = first['净值']
    max_drawdown = 0
    max_dd_date = first['日期']

    for item in data:
        if item['净值'] > max_value:
            max_value = item['净值']
        drawdown = (item['净值'] / max_value - 1) * 100
        if drawdown < max_drawdown:
            max_drawdown = drawdown
            max_dd_date = item['日期']

    print(f"最大回撤: {max_drawdown:.2f}%")
    print(f"最大回撤日期: {max_dd_date}")
    print()

    # 2. 与市场指数对比
    print("【二、相对市场表现】")
    print("-" * 80)

    # 计算各指数涨幅
    sz_return = (last['上证指数'] / first['上证指数'] - 1) * 100
    sz50_return = (last['上证50'] / first['上证50'] - 1) * 100
    hs300_return = (last['沪深300'] / first['沪深300'] - 1) * 100

    print(f"基金收益率:    {total_return:>8.2f}%")
    print(f"上证指数涨幅:  {sz_return:>8.2f}%  (超额收益: {total_return - sz_return:>6.2f}%)")
    print(f"上证50涨幅:    {sz50_return:>8.2f}%  (超额收益: {total_return - sz50_return:>6.2f}%)")
    print(f"沪深300涨幅:   {hs300_return:>8.2f}%  (超额收益: {total_return - hs300_return:>6.2f}%)")
    print()

    # 对比分析
    if total_return > sz_return and total_return > hs300_return:
        print("✓ 基金成功跑赢了主要市场指数,展现了良好的主动管理能力")
    elif total_return > sz_return or total_return > hs300_return:
        print("△ 基金跑赢了部分市场指数,但未能全面跑赢市场")
    else:
        print("✗ 基金未能跑赢主要市场指数,需要反思投资策略")
    print()

    # 3. 波动性分析
    print("【三、风险与波动性分析】")
    print("-" * 80)

    # 计算净值变化
    changes = []
    for i in range(1, len(data)):
        change = (data[i]['净值'] / data[i-1]['净值'] - 1) * 100
        changes.append(change)

    # 计算标准差
    mean_change = sum(changes) / len(changes)
    variance = sum((x - mean_change) ** 2 for x in changes) / len(changes)
    std_dev = math.sqrt(variance)

    max_gain = max(changes)
    max_loss = min(changes)

    print(f"净值波动率(标准差): {std_dev:.2f}%")
    print(f"最大单期涨幅: {max_gain:.2f}%")
    print(f"最大单期跌幅: {max_loss:.2f}%")
    print()

    # 夏普比率估算
    risk_free_rate = 3.0
    excess_return = annualized_return - risk_free_rate
    annualized_vol = std_dev * math.sqrt(252/days) if days > 0 else 0
    sharpe_ratio = excess_return / annualized_vol if annualized_vol > 0 else 0

    print(f"年化波动率(估算): {annualized_vol:.2f}%")
    print(f"夏普比率(估算): {sharpe_ratio:.2f}")
    print()

    # 4. 阶段表现分析
    print("【四、阶段表现分析】")
    print("-" * 80)

    # 找出最低点
    min_nav = min(data, key=lambda x: x['净值'])
    min_index = data.index(min_nav)

    print(f"最低点净值: {min_nav['净值']:.4f} (日期: {min_nav['日期']})")
    print(f"从起点到最低点: {(min_nav['净值'] / first['净值'] - 1) * 100:.2f}%")

    # 恢复阶段
    if min_index < len(data) - 1:
        recovery = (last['净值'] / min_nav['净值'] - 1) * 100
        recovery_days = (last['日期对象'] - min_nav['日期对象']).days
        print(f"从最低点反弹: {recovery:.2f}% (用时{recovery_days}天)")
    print()

    # 关键时间段分析
    print("关键时间段表现:")
    print(f"  4-5月(调整期): {(data[4]['净值'] / data[0]['净值'] - 1) * 100:.2f}%")
    if len(data) > 5:
        print(f"  8月(转折期):   {(data[5]['净值'] / data[4]['净值'] - 1) * 100:.2f}%")
        print(f"  11-12月(上涨期): {(data[-1]['净值'] / data[6]['净值'] - 1) * 100:.2f}%")
    print()

    # 5. 操作水平评估
    print("【五、操作水平评估】")
    print("-" * 80)

    score = 0
    total_score = 0
    评估项目 = []

    # 绝对收益
    total_score += 25
    if total_return > 15:
        score += 25
        评估项目.append("✓ [25/25分] 绝对收益优秀 (>15%)")
    elif total_return > 10:
        score += 20
        评估项目.append("✓ [20/25分] 绝对收益良好 (10-15%)")
    elif total_return > 5:
        score += 15
        评估项目.append("△ [15/25分] 绝对收益一般 (5-10%)")
    else:
        score += 10
        评估项目.append("△ [10/25分] 绝对收益有待提升 (<5%)")

    # 相对收益
    total_score += 25
    if total_return > sz_return + 5 and total_return > hs300_return + 5:
        score += 25
        评估项目.append("✓ [25/25分] 大幅跑赢市场 (超额>5%)")
    elif total_return > sz_return and total_return > hs300_return:
        score += 20
        评估项目.append("✓ [20/25分] 成功跑赢市场")
    elif total_return > sz_return or total_return > hs300_return:
        score += 15
        评估项目.append("△ [15/25分] 部分跑赢市场")
    else:
        score += 10
        评估项目.append("✗ [10/25分] 未能跑赢市场")

    # 风险控制
    total_score += 25
    if max_drawdown > -3:
        score += 25
        评估项目.append("✓ [25/25分] 风险控制优秀 (回撤<3%)")
    elif max_drawdown > -5:
        score += 20
        评估项目.append("✓ [20/25分] 风险控制良好 (回撤3-5%)")
    elif max_drawdown > -10:
        score += 15
        评估项目.append("△ [15/25分] 风险控制一般 (回撤5-10%)")
    else:
        score += 10
        评估项目.append("✗ [10/25分] 风险控制需加强 (回撤>10%)")

    # 风险调整收益
    total_score += 25
    if sharpe_ratio > 2.0:
        score += 25
        评估项目.append("✓ [25/25分] 风险调整收益优秀 (夏普>2.0)")
    elif sharpe_ratio > 1.5:
        score += 20
        评估项目.append("✓ [20/25分] 风险调整收益良好 (夏普>1.5)")
    elif sharpe_ratio > 1.0:
        score += 15
        评估项目.append("△ [15/25分] 风险调整收益一般 (夏普>1.0)")
    else:
        score += 10
        评估项目.append("△ [10/25分] 风险调整收益有待提升")

    for item in 评估项目:
        print(item)

    print()
    print(f"综合评分: {score}/{total_score}分 ({score/total_score*100:.1f}%)")

    if score >= 90:
        print("总体评价: 优秀 - 基金操作水平出色")
    elif score >= 80:
        print("总体评价: 良好 - 基金操作水平较好,有一定提升空间")
    elif score >= 70:
        print("总体评价: 中等 - 基金操作水平一般,需要改进")
    else:
        print("总体评价: 需改进 - 基金操作水平有待大幅提升")
    print()

    # 6. 改进建议
    print("【六、改进建议】")
    print("-" * 80)
    print()

    print("1. 风险管理优化")
    print("-" * 40)
    if max_drawdown < -2:
        print("   • 4-5月期间出现了回撤,暴露了风险控制的不足")
        print("   • 建议设置更严格的止损机制,如单只股票-8%止损,组合-5%减仓")
        print("   • 考虑使用动态仓位管理,市场不确定时降低至60-70%仓位")
        print("   • 建立风险预算体系,明确各类资产的风险敞口上限")
    else:
        print("   • 当前风险控制表现良好,建议继续保持")
        print("   • 可以适当放宽止损线,给予优质股票更多表现空间")
    print()

    print("2. 择时能力提升")
    print("-" * 40)
    # 分析8月份后的表现
    aug_index = 5  # 8月24日数据索引
    if aug_index < len(data):
        pre_aug = data[aug_index - 1]
        post_aug = data[aug_index]
        aug_fund_gain = (post_aug['净值'] / pre_aug['净值'] - 1) * 100
        aug_market_gain = (post_aug['上证指数'] / pre_aug['上证指数'] - 1) * 100

        print(f"   • 8月市场出现明显拐点,上证指数涨{aug_market_gain:.2f}%,基金涨{aug_fund_gain:.2f}%")
        if aug_fund_gain > aug_market_gain:
            print("   • 成功抓住了这轮上涨,说明择时判断较准确")
            print("   • 建议总结此次成功经验,形成可复制的择时模型")
        else:
            print("   • 未能充分把握这轮上涨,说明仓位管理偏保守")
            print("   • 建议建立市场情绪监控体系,在拐点出现时敢于加仓")

        print("   • 关注技术面和资金面信号:成交量放大、北向资金流入等")
        print("   • 结合宏观政策,如货币政策宽松、产业政策支持等")
    print()

    print("3. 选股策略优化")
    print("-" * 40)
    print("   • 加强行业轮动研究,把握不同阶段的主线板块")
    print("   • 优化持仓结构:")
    print("     - 核心仓位(40-50%): 长期看好的优质龙头")
    print("     - 卫星仓位(30-40%): 主题投资、高成长股")
    print("     - 灵活仓位(10-20%): 短期交易、事件驱动")
    print("   • 建立个股筛选标准:")
    print("     - 基本面: ROE>15%,营收增长>20%,负债率<60%")
    print("     - 估值: PE<行业平均*1.5,PEG<1")
    print("     - 技术面: 突破关键阻力位,量价配合")
    print()

    print("4. 交易纪律强化")
    print("-" * 40)
    print("   • 建立标准化交易流程:")
    print("     ① 研究分析 → ② 风险评估 → ③ 仓位决策 → ④ 执行交易 → ⑤ 跟踪复盘")
    print("   • 设定明确的买入标准:")
    print("     - 逻辑清晰:有明确的投资逻辑和催化剂")
    print("     - 时机合适:技术形态良好,趋势向上")
    print("     - 风险可控:有明确的止损位和预期收益空间")
    print("   • 设定卖出纪律:")
    print("     - 止损:跌破关键支撑或基本面恶化")
    print("     - 止盈:达到目标价位或估值明显偏高")
    print("     - 止平:逻辑不再成立或有更好标的")
    print()

    print("5. 宏观对冲策略")
    print("-" * 40)
    usd_change = (last['美元汇率'] / first['美元汇率'] - 1) * 100
    chn_bond_change = (last['中国十年期国债'] - first['中国十年期国债'])
    us_bond_change = (last['美国十年期国债'] - first['美国十年期国债'])

    print(f"   • 美元汇率变化: {usd_change:.2f}% (人民币{'升值' if usd_change < 0 else '贬值'})")
    print(f"   • 中国十年期国债收益率变化: {chn_bond_change:+.2f}个BP")
    print(f"   • 美国十年期国债收益率变化: {us_bond_change:+.2f}个BP")
    print()
    print("   建议:")
    if abs(usd_change) > 3:
        print(f"   • 汇率波动较大,如持有港股或美股,需考虑汇率对冲")
    print("   • 关注中美利差变化,影响跨境资金流动")
    print("   • 利率下行时,成长股更占优;利率上行时,价值股更占优")
    print("   • 可配置5-10%的债券资产,起到组合压舱石作用")
    print()

    print("6. 业绩持续性建设")
    print("-" * 40)
    print("   • 建立投资复盘机制:")
    print("     - 每周复盘持仓变化和市场热点")
    print("     - 每月总结投资收益和失误教训")
    print("     - 每季度回顾策略有效性并调整")
    print("   • 强化研究体系:")
    print("     - 建立行业研究框架,深入3-5个重点行业")
    print("     - 跟踪50-100只核心股票池")
    print("     - 定期调研上市公司,获取一手信息")
    print("   • 持续学习提升:")
    print("     - 研究优秀基金经理的投资方法")
    print("     - 学习行为金融学,避免认知偏差")
    print("     - 关注海外市场经验,拓宽投资视野")
    print()

    print("7. 具体行动计划")
    print("-" * 40)
    print("   短期(1-3个月):")
    print("   • 梳理当前持仓,淘汰逻辑不清晰的个股")
    print("   • 建立风险监控表格,每日更新组合风险指标")
    print("   • 设置交易日志,记录每笔买卖的理由和结果")
    print()
    print("   中期(3-6个月):")
    print("   • 完善投资决策流程,形成标准化操作手册")
    print("   • 建立宏观经济监控指标体系")
    print("   • 开发量化辅助工具,提升决策效率")
    print()
    print("   长期(6-12个月):")
    print("   • 形成自己的投资风格和核心能力圈")
    print("   • 建立稳定的超额收益来源")
    print("   • 打造可复制、可持续的投资体系")
    print()

    print("=" * 80)
    print("分析完成!")
    print("=" * 80)

# 运行分析
analyze_fund_performance(data)

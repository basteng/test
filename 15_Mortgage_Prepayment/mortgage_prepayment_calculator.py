#!/usr/bin/env python3
"""
房贷提前还款计算器
Mortgage Prepayment Calculator

场景：324万贷款，3.05%利率，30年(360月)，已还13月，手头30万现金
比较：马上提前还款 vs 一年后提前还款
还款方式：等额本息
"""

# ============================================================
# 基本参数
# ============================================================
LOAN_AMOUNT = 3_240_000          # 贷款总额（元）
ANNUAL_RATE = 0.0305             # 年利率 3.05%
TOTAL_MONTHS = 360               # 贷款总期数（30年）
MONTHS_PAID = 13                 # 已还期数
PREPAY_AMOUNT = 300_000          # 提前还款金额（元）
CASH_ANNUAL_RETURN = 0.02        # 现金理财年化收益率（假设2%，可调整）

MONTHLY_RATE = ANNUAL_RATE / 12  # 月利率


def monthly_payment(principal, monthly_rate, n_months):
    """计算等额本息月供"""
    if monthly_rate == 0:
        return principal / n_months
    r = monthly_rate
    factor = (1 + r) ** n_months
    return principal * r * factor / (factor - 1)


def remaining_principal(original_principal, monthly_rate, n_months, months_paid):
    """计算已还 months_paid 期后的剩余本金"""
    r = monthly_rate
    mp = monthly_payment(original_principal, r, n_months)
    factor = (1 + r) ** months_paid
    return original_principal * factor - mp * (factor - 1) / r


def total_interest(principal, monthly_rate, n_months):
    """计算总利息"""
    mp = monthly_payment(principal, monthly_rate, n_months)
    return mp * n_months - principal


def amortization_schedule(principal, monthly_rate, n_months):
    """生成完整的还款计划表，返回每期(本金, 利息, 剩余本金)"""
    mp = monthly_payment(principal, monthly_rate, n_months)
    balance = principal
    schedule = []
    for i in range(1, n_months + 1):
        interest_part = balance * monthly_rate
        principal_part = mp - interest_part
        balance -= principal_part
        if balance < 0:
            balance = 0
        schedule.append({
            'month': i,
            'payment': mp,
            'principal': principal_part,
            'interest': interest_part,
            'balance': balance
        })
    return schedule


def scenario_no_prepay():
    """场景0：不提前还款，按原计划还完"""
    mp = monthly_payment(LOAN_AMOUNT, MONTHLY_RATE, TOTAL_MONTHS)
    total_paid = mp * TOTAL_MONTHS
    total_int = total_paid - LOAN_AMOUNT
    remaining_months = TOTAL_MONTHS - MONTHS_PAID

    # 已还的利息
    schedule = amortization_schedule(LOAN_AMOUNT, MONTHLY_RATE, TOTAL_MONTHS)
    interest_paid = sum(s['interest'] for s in schedule[:MONTHS_PAID])
    interest_remaining = total_int - interest_paid

    return {
        'name': '不提前还款（原计划）',
        'monthly_payment': mp,
        'remaining_months': remaining_months,
        'total_interest': total_int,
        'interest_paid': interest_paid,
        'interest_remaining': interest_remaining,
        'total_paid': total_paid,
    }


def scenario_prepay_now(reduce_term=True):
    """
    场景1：第13期还完后立即提前还30万
    reduce_term=True: 缩短期限，月供不变
    reduce_term=False: 减少月供，期限不变
    """
    # 第13期还完后的剩余本金
    bal = remaining_principal(LOAN_AMOUNT, MONTHLY_RATE, TOTAL_MONTHS, MONTHS_PAID)
    new_balance = bal - PREPAY_AMOUNT
    original_remaining = TOTAL_MONTHS - MONTHS_PAID  # 347个月

    # 已还的利息
    schedule_orig = amortization_schedule(LOAN_AMOUNT, MONTHLY_RATE, TOTAL_MONTHS)
    interest_already_paid = sum(s['interest'] for s in schedule_orig[:MONTHS_PAID])

    if reduce_term:
        # 月供不变，计算新的还款期数
        mp = monthly_payment(LOAN_AMOUNT, MONTHLY_RATE, TOTAL_MONTHS)
        # 月供 = new_balance * r * (1+r)^n / ((1+r)^n - 1)
        # 解 n: n = -log(1 - new_balance*r/mp) / log(1+r)
        import math
        r = MONTHLY_RATE
        if mp <= new_balance * r:
            new_months = original_remaining  # 月供不够覆盖利息，不缩短
        else:
            new_months = math.ceil(-math.log(1 - new_balance * r / mp) / math.log(1 + r))

        # 新的还款计划
        new_schedule = amortization_schedule(new_balance, MONTHLY_RATE, new_months)
        # 最后一期可能月供不同
        actual_last_payment = new_schedule[-1]['payment'] if new_schedule else 0

        interest_after_prepay = sum(s['interest'] for s in new_schedule)
        total_interest_life = interest_already_paid + interest_after_prepay
        months_saved = original_remaining - new_months

        return {
            'name': '马上还30万（缩短期限）',
            'prepay_month': MONTHS_PAID,
            'balance_before_prepay': bal,
            'new_balance': new_balance,
            'monthly_payment': mp,
            'new_remaining_months': new_months,
            'months_saved': months_saved,
            'years_saved': months_saved / 12,
            'interest_already_paid': interest_already_paid,
            'interest_after_prepay': interest_after_prepay,
            'total_interest_life': total_interest_life,
        }
    else:
        # 期限不变，计算新的月供
        new_mp = monthly_payment(new_balance, MONTHLY_RATE, original_remaining)
        old_mp = monthly_payment(LOAN_AMOUNT, MONTHLY_RATE, TOTAL_MONTHS)

        new_schedule = amortization_schedule(new_balance, MONTHLY_RATE, original_remaining)
        interest_after_prepay = sum(s['interest'] for s in new_schedule)
        total_interest_life = interest_already_paid + interest_after_prepay

        return {
            'name': '马上还30万（减少月供）',
            'prepay_month': MONTHS_PAID,
            'balance_before_prepay': bal,
            'new_balance': new_balance,
            'monthly_payment_old': old_mp,
            'monthly_payment_new': new_mp,
            'monthly_saving': old_mp - new_mp,
            'remaining_months': original_remaining,
            'interest_already_paid': interest_already_paid,
            'interest_after_prepay': interest_after_prepay,
            'total_interest_life': total_interest_life,
        }


def scenario_prepay_later(reduce_term=True):
    """
    场景2：一年后（第25期还完后）提前还30万
    """
    prepay_at = MONTHS_PAID + 12  # 第25期

    # 第25期还完后的剩余本金
    bal = remaining_principal(LOAN_AMOUNT, MONTHLY_RATE, TOTAL_MONTHS, prepay_at)
    new_balance = bal - PREPAY_AMOUNT
    original_remaining_from_25 = TOTAL_MONTHS - prepay_at  # 335个月

    # 已还的利息（前25期）
    schedule_orig = amortization_schedule(LOAN_AMOUNT, MONTHLY_RATE, TOTAL_MONTHS)
    interest_paid_25 = sum(s['interest'] for s in schedule_orig[:prepay_at])

    # 30万在这一年的理财收益
    cash_return = PREPAY_AMOUNT * CASH_ANNUAL_RETURN

    if reduce_term:
        mp = monthly_payment(LOAN_AMOUNT, MONTHLY_RATE, TOTAL_MONTHS)
        import math
        r = MONTHLY_RATE
        if mp <= new_balance * r:
            new_months = original_remaining_from_25
        else:
            new_months = math.ceil(-math.log(1 - new_balance * r / mp) / math.log(1 + r))

        new_schedule = amortization_schedule(new_balance, MONTHLY_RATE, new_months)
        interest_after_prepay = sum(s['interest'] for s in new_schedule)
        total_interest_life = interest_paid_25 + interest_after_prepay
        months_saved = original_remaining_from_25 - new_months

        return {
            'name': '一年后还30万（缩短期限）',
            'prepay_month': prepay_at,
            'balance_before_prepay': bal,
            'new_balance': new_balance,
            'monthly_payment': mp,
            'new_remaining_months': new_months,
            'months_saved_from_prepay': months_saved,
            'total_remaining_after_prepay': new_months,
            'total_months_from_now': 12 + new_months,
            'interest_paid_25': interest_paid_25,
            'interest_after_prepay': interest_after_prepay,
            'total_interest_life': total_interest_life,
            'cash_return': cash_return,
        }
    else:
        new_mp = monthly_payment(new_balance, MONTHLY_RATE, original_remaining_from_25)
        old_mp = monthly_payment(LOAN_AMOUNT, MONTHLY_RATE, TOTAL_MONTHS)

        new_schedule = amortization_schedule(new_balance, MONTHLY_RATE, original_remaining_from_25)
        interest_after_prepay = sum(s['interest'] for s in new_schedule)
        total_interest_life = interest_paid_25 + interest_after_prepay

        return {
            'name': '一年后还30万（减少月供）',
            'prepay_month': prepay_at,
            'balance_before_prepay': bal,
            'new_balance': new_balance,
            'monthly_payment_old': old_mp,
            'monthly_payment_new': new_mp,
            'monthly_saving': old_mp - new_mp,
            'remaining_months': original_remaining_from_25,
            'interest_paid_25': interest_paid_25,
            'interest_after_prepay': interest_after_prepay,
            'total_interest_life': total_interest_life,
            'cash_return': cash_return,
        }


def fmt(amount):
    """格式化金额为万元"""
    return f"{amount / 10000:.2f}万"


def fmt_yuan(amount):
    """格式化金额为元"""
    return f"{amount:,.2f}元"


def main():
    print("=" * 70)
    print("房贷提前还款分析报告")
    print("=" * 70)
    print(f"\n贷款总额：{fmt(LOAN_AMOUNT)}    年利率：{ANNUAL_RATE*100:.2f}%")
    print(f"贷款期限：{TOTAL_MONTHS}个月（{TOTAL_MONTHS//12}年）")
    print(f"已还期数：{MONTHS_PAID}个月")
    print(f"提前还款金额：{fmt(PREPAY_AMOUNT)}")
    print(f"现金理财假设年化收益：{CASH_ANNUAL_RETURN*100:.1f}%\n")

    # ============================================================
    # 基准：不提前还款
    # ============================================================
    base = scenario_no_prepay()
    print("-" * 70)
    print(f"【基准】{base['name']}")
    print("-" * 70)
    print(f"  月供：{fmt_yuan(base['monthly_payment'])}")
    print(f"  剩余期数：{base['remaining_months']}个月（{base['remaining_months']/12:.1f}年）")
    print(f"  贷款总利息：{fmt(base['total_interest'])}")
    print(f"  已付利息：{fmt(base['interest_paid'])}")
    print(f"  剩余应付利息：{fmt(base['interest_remaining'])}")

    # ============================================================
    # 场景1A：马上还，缩短期限
    # ============================================================
    s1a = scenario_prepay_now(reduce_term=True)
    print(f"\n{'='*70}")
    print(f"【方案A】{s1a['name']}")
    print("=" * 70)
    print(f"  提前还款时间：第{s1a['prepay_month']}期后")
    print(f"  还款前剩余本金：{fmt(s1a['balance_before_prepay'])}")
    print(f"  还30万后剩余本金：{fmt(s1a['new_balance'])}")
    print(f"  月供不变：{fmt_yuan(s1a['monthly_payment'])}")
    print(f"  新剩余期数：{s1a['new_remaining_months']}个月（{s1a['new_remaining_months']/12:.1f}年）")
    print(f"  缩短期限：{s1a['months_saved']}个月（{s1a['years_saved']:.1f}年）")
    print(f"  提前还款后总利息：{fmt(s1a['interest_after_prepay'])}")
    print(f"  贷款生命周期总利息：{fmt(s1a['total_interest_life'])}")
    interest_saved_1a = base['total_interest'] - s1a['total_interest_life']
    print(f"  >>> 比不还节省利息：{fmt(interest_saved_1a)}")

    # ============================================================
    # 场景1B：马上还，减少月供
    # ============================================================
    s1b = scenario_prepay_now(reduce_term=False)
    print(f"\n{'='*70}")
    print(f"【方案B】{s1b['name']}")
    print("=" * 70)
    print(f"  提前还款时间：第{s1b['prepay_month']}期后")
    print(f"  还款前剩余本金：{fmt(s1b['balance_before_prepay'])}")
    print(f"  还30万后剩余本金：{fmt(s1b['new_balance'])}")
    print(f"  原月供：{fmt_yuan(s1b['monthly_payment_old'])}")
    print(f"  新月供：{fmt_yuan(s1b['monthly_payment_new'])}")
    print(f"  每月减少：{fmt_yuan(s1b['monthly_saving'])}")
    print(f"  剩余期数不变：{s1b['remaining_months']}个月")
    print(f"  贷款生命周期总利息：{fmt(s1b['total_interest_life'])}")
    interest_saved_1b = base['total_interest'] - s1b['total_interest_life']
    print(f"  >>> 比不还节省利息：{fmt(interest_saved_1b)}")

    # ============================================================
    # 场景2A：一年后还，缩短期限
    # ============================================================
    s2a = scenario_prepay_later(reduce_term=True)
    print(f"\n{'='*70}")
    print(f"【方案C】{s2a['name']}")
    print("=" * 70)
    print(f"  提前还款时间：第{s2a['prepay_month']}期后")
    print(f"  还款前剩余本金：{fmt(s2a['balance_before_prepay'])}")
    print(f"  还30万后剩余本金：{fmt(s2a['new_balance'])}")
    print(f"  月供不变：{fmt_yuan(s2a['monthly_payment'])}")
    print(f"  新剩余期数：{s2a['new_remaining_months']}个月（{s2a['new_remaining_months']/12:.1f}年）")
    print(f"  从现在算起总剩余：12 + {s2a['new_remaining_months']} = {s2a['total_months_from_now']}个月")
    print(f"  贷款生命周期总利息：{fmt(s2a['total_interest_life'])}")
    interest_saved_2a = base['total_interest'] - s2a['total_interest_life']
    print(f"  >>> 比不还节省利息：{fmt(interest_saved_2a)}")
    print(f"  30万一年理财收益（{CASH_ANNUAL_RETURN*100:.1f}%）：{fmt_yuan(s2a['cash_return'])}")
    net_saved_2a = interest_saved_2a + s2a['cash_return']
    print(f"  >>> 净节省（含理财）：{fmt(net_saved_2a)}")

    # ============================================================
    # 场景2B：一年后还，减少月供
    # ============================================================
    s2b = scenario_prepay_later(reduce_term=False)
    print(f"\n{'='*70}")
    print(f"【方案D】{s2b['name']}")
    print("=" * 70)
    print(f"  提前还款时间：第{s2b['prepay_month']}期后")
    print(f"  还款前剩余本金：{fmt(s2b['balance_before_prepay'])}")
    print(f"  还30万后剩余本金：{fmt(s2b['new_balance'])}")
    print(f"  原月供：{fmt_yuan(s2b['monthly_payment_old'])}")
    print(f"  新月供：{fmt_yuan(s2b['monthly_payment_new'])}")
    print(f"  每月减少：{fmt_yuan(s2b['monthly_saving'])}")
    print(f"  剩余期数不变：{s2b['remaining_months']}个月")
    print(f"  贷款生命周期总利息：{fmt(s2b['total_interest_life'])}")
    interest_saved_2b = base['total_interest'] - s2b['total_interest_life']
    print(f"  >>> 比不还节省利息：{fmt(interest_saved_2b)}")
    print(f"  30万一年理财收益（{CASH_ANNUAL_RETURN*100:.1f}%）：{fmt_yuan(s2b['cash_return'])}")
    net_saved_2b = interest_saved_2b + s2b['cash_return']
    print(f"  >>> 净节省（含理财）：{fmt(net_saved_2b)}")

    # ============================================================
    # 对比总结
    # ============================================================
    print(f"\n{'='*70}")
    print("对比总结")
    print("=" * 70)

    print(f"\n{'方案':<25} {'节省利息':<15} {'理财收益':<12} {'净节省':<15}")
    print("-" * 70)
    print(f"{'A.马上还-缩短期限':<20} {fmt(interest_saved_1a):<15} {'—':<12} {fmt(interest_saved_1a):<15}")
    print(f"{'B.马上还-减少月供':<20} {fmt(interest_saved_1b):<15} {'—':<12} {fmt(interest_saved_1b):<15}")
    print(f"{'C.一年后还-缩短期限':<19} {fmt(interest_saved_2a):<15} {fmt_yuan(s2a['cash_return']):<12} {fmt(net_saved_2a):<15}")
    print(f"{'D.一年后还-减少月供':<19} {fmt(interest_saved_2b):<15} {fmt_yuan(s2b['cash_return']):<12} {fmt(net_saved_2b):<15}")

    diff_ab = interest_saved_1a - interest_saved_1b
    diff_ac = interest_saved_1a - net_saved_2a
    diff_interest_now_vs_later = interest_saved_1a - interest_saved_2a

    print(f"\n关键对比：")
    print(f"  马上还（缩短期限 vs 减少月供）差额：{fmt(diff_ab)}")
    print(f"  马上还 vs 一年后还（均缩短期限）：")
    print(f"    纯利息差额：{fmt(diff_interest_now_vs_later)}（马上还多省这么多利息）")
    print(f"    考虑理财收益后净差额：{fmt(diff_ac)}")
    print(f"    即：晚还一年多付约 {fmt(diff_interest_now_vs_later)} 利息，")
    print(f"         但30万理财一年约赚 {fmt_yuan(s2a['cash_return'])}")

    # ============================================================
    # 决策建议
    # ============================================================
    print(f"\n{'='*70}")
    print("决策分析")
    print("=" * 70)

    print("""
1. 【缩短期限 vs 减少月供】
   缩短期限永远比减少月供省更多利息。
   除非你现金流紧张需要降低月供压力，否则优先选缩短期限。

2. 【马上还 vs 一年后还】
   核心问题：30万放一年的收益 能否 覆盖 多付的利息？
""")

    breakeven_rate = diff_interest_now_vs_later / PREPAY_AMOUNT * 100
    print(f"   盈亏平衡理财收益率 = {breakeven_rate:.2f}%")
    print(f"   （即30万一年收益需达到 {fmt(diff_interest_now_vs_later)} 才能打平）")
    print()

    if CASH_ANNUAL_RETURN * 100 >= breakeven_rate:
        print(f"   当前假设理财收益率 {CASH_ANNUAL_RETURN*100:.1f}% >= 盈亏平衡点 {breakeven_rate:.2f}%")
        print(f"   → 可以考虑一年后再还，理财收益能覆盖多付的利息")
    else:
        print(f"   当前假设理财收益率 {CASH_ANNUAL_RETURN*100:.1f}% < 盈亏平衡点 {breakeven_rate:.2f}%")
        print(f"   → 建议马上提前还款，省下的利息比理财收益多")

    print(f"""
3. 【其他重要考量】
   - 应急资金：还完30万后，手头是否还有3-6个月的应急储备？
     如果没有，留部分现金更安全。
   - 违约金：部分银行对提前还款有违约金（通常前1-3年），
     需确认你的合同条款。一般违约金为提前还款金额的1%左右。
     如果有1%违约金 = {fmt_yuan(PREPAY_AMOUNT * 0.01)}，
     一年后如果没有违约金，可能等一年更划算。
   - 投资机会：如果有确定性较高的投资渠道收益率>{breakeven_rate:.2f}%，
     可以不急着还。
   - 通胀因素：3.05%的利率已经很低，长期通胀约2-3%，
     实际利率接近0-1%，不提前还也可以。
   - 税务/公积金：如果贷款是公积金贷款或组合贷，
     公积金部分利率更低，优先还商贷部分。

4. 【总结建议】
   3.05%利率在历史上属于较低水平。
   如果没有违约金 + 应急资金充足 → 马上还，选缩短期限（方案A）
   如果有违约金或需要资金灵活性 → 可以等一年
   如果有稳定>{breakeven_rate:.1f}%的投资渠道 → 不急着还
""")


if __name__ == '__main__':
    main()

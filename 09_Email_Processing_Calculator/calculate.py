#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

print("=" * 80)
print("Email处理进度计算器")
print("=" * 80)

# 基本信息
total_emails = 2173

print(f"\n总email数量: {total_emails}")
print("\n" + "=" * 80)
print("请根据表格统计数据填写:")
print("=" * 80)

# 这里填写从截图中统计的数据
# ======================================
# 请修改下面的数值！
# ======================================

sent_count = 0          # 已发出（打√）的数量
checked_not_send = 0    # 已查但不发（中文）的数量
unprocessed = 2173      # 未处理（空白）的数量

# ======================================

print(f"\n当前统计:")
print(f"  ✓ 已发出（打√）: {sent_count}")
print(f"  ✗ 已查但不发（中文）: {checked_not_send}")
print(f"  ○ 未处理（空白）: {unprocessed}")
print(f"  {'─' * 40}")
print(f"  合计: {sent_count + checked_not_send + unprocessed}")

# 验证数据
if sent_count + checked_not_send + unprocessed != total_emails:
    print(f"\n⚠️  警告：统计数据不匹配！")
    print(f"  合计 {sent_count + checked_not_send + unprocessed} ≠ 总数 {total_emails}")
    print(f"  请检查数据！")

print("\n" + "=" * 80)
print("时间计算")
print("=" * 80)

# 日期
start_date = datetime(2026, 1, 7)
end_date = datetime(2026, 10, 6)
days_available = (end_date - start_date).days + 1

print(f"\n开始日期: {start_date.strftime('%Y年%m月%d日')} (今天)")
print(f"结束日期: {end_date.strftime('%Y年%m月%d日')}")
print(f"可用天数: {days_available} 天")
print(f"可用月数: 约 {days_available / 30:.1f} 个月")

if unprocessed > 0:
    emails_per_day = unprocessed / days_available

    print("\n" + "=" * 80)
    print("核心数据")
    print("=" * 80)

    print(f"\n📊 需要处理的email数量: {unprocessed}")
    print(f"📈 每天最少需处理: {emails_per_day:.2f} 个")
    print(f"🎯 建议每天处理: {int(emails_per_day) + 1} 个")

    print("\n" + "=" * 80)
    print("不同处理速度的完成时间表")
    print("=" * 80)

    daily_targets = [3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30, 40, 50]

    print("\n  每天 | 需要天数 |  完成日期  | 缓冲天数 | 状态")
    print("  " + "─" * 65)

    for target in daily_targets:
        days_needed = (unprocessed + target - 1) // target
        completion_date = start_date + timedelta(days=days_needed - 1)
        buffer_days = (end_date - completion_date).days

        if completion_date <= end_date:
            status = "✓"
            status_text = "按时"
        else:
            status = "✗"
            status_text = f"超时{-buffer_days}天"
            buffer_days = 0

        print(f"  {status} {target:2d}个 | {days_needed:4d} 天 | {completion_date.strftime('%Y-%m-%d')} | {buffer_days:4d} 天 | {status_text}")

    # 推荐方案
    print("\n" + "=" * 80)
    print("📋 推荐方案")
    print("=" * 80)

    recommended_daily = int(emails_per_day) + 1
    recommended_days = (unprocessed + recommended_daily - 1) // recommended_daily
    recommended_completion = start_date + timedelta(days=recommended_days - 1)
    buffer = (end_date - recommended_completion).days

    print(f"\n✨ 方案A: 稳健方案")
    print(f"   每天处理 {recommended_daily} 个email")
    print(f"   需要 {recommended_days} 天")
    print(f"   完成日期: {recommended_completion.strftime('%Y年%m月%d日')}")
    print(f"   缓冲时间: {buffer} 天")

    # 保险方案
    safe_daily = recommended_daily + 2
    safe_days = (unprocessed + safe_daily - 1) // safe_daily
    safe_completion = start_date + timedelta(days=safe_days - 1)
    safe_buffer = (end_date - safe_completion).days

    print(f"\n🛡️  方案B: 保险方案（留更多余地）")
    print(f"   每天处理 {safe_daily} 个email")
    print(f"   需要 {safe_days} 天")
    print(f"   完成日期: {safe_completion.strftime('%Y年%m月%d日')}")
    print(f"   缓冲时间: {safe_buffer} 天")

    # 快速方案
    fast_daily = safe_daily + 3
    fast_days = (unprocessed + fast_daily - 1) // fast_daily
    fast_completion = start_date + timedelta(days=fast_days - 1)
    fast_buffer = (end_date - fast_completion).days

    print(f"\n🚀 方案C: 快速方案（快速完成）")
    print(f"   每天处理 {fast_daily} 个email")
    print(f"   需要 {fast_days} 天")
    print(f"   完成日期: {fast_completion.strftime('%Y年%m月%d日')}")
    print(f"   缓冲时间: {fast_buffer} 天")

    # 工作日方案（假设一周工作5天）
    workday_daily = int(unprocessed / (days_available * 5 / 7)) + 1
    workdays_needed = (unprocessed + workday_daily - 1) // workday_daily
    workday_completion = start_date + timedelta(days=int(workdays_needed * 7 / 5))
    workday_buffer = (end_date - workday_completion).days

    print(f"\n💼 方案D: 工作日方案（仅工作日处理，周末休息）")
    print(f"   每个工作日处理 {workday_daily} 个email")
    print(f"   需要约 {workdays_needed} 个工作日 (约 {int(workdays_needed / 5)} 周)")
    print(f"   预计完成日期: {workday_completion.strftime('%Y年%m月%d日')}")
    print(f"   缓冲时间: 约 {workday_buffer} 天")

    # 进度追踪建议
    print("\n" + "=" * 80)
    print("📈 进度追踪建议")
    print("=" * 80)

    print(f"\n每周检查点目标 (按方案A计算):")
    week_target = recommended_daily * 7
    for week in range(1, min(13, days_available // 7 + 2)):
        week_end = start_date + timedelta(days=week * 7 - 1)
        if week_end > end_date:
            break
        cumulative = week * week_target
        if cumulative > unprocessed:
            cumulative = unprocessed
        percentage = (cumulative / unprocessed) * 100
        print(f"  第{week:2d}周 ({week_end.strftime('%m-%d')}): 累计处理 {cumulative:4d} 个 ({percentage:5.1f}%)")

else:
    print("\n🎉 恭喜！所有email已处理完成！")

print("\n" + "=" * 80)
print("注意事项:")
print("=" * 80)
print("""
1. 以上计算假设每天都能处理，如遇特殊情况请提前增加处理量
2. 建议使用方案B（保险方案）确保有足够缓冲时间
3. 如果只在工作日处理，建议使用方案D
4. 定期检查进度，如发现落后及时调整处理速度
5. 记得保存处理记录，避免重复处理
""")

print("=" * 80)

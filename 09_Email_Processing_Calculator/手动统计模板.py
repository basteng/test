#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

print("=" * 80)
print("Email处理进度计算器 - 手动输入版")
print("=" * 80)

# 基本信息
total_emails = 2173
print(f"\n总email数量: {total_emails}")

# 手动输入统计数据
print("\n请根据表格截图统计以下数据：")
print("-" * 80)

# 这里需要手动填写从截图中统计的数据
# 请替换下面的数值
sent_count = 0  # 已发出（打√）的数量 - 请手动填写
checked_not_send = 0  # 已查但不发（中文）的数量 - 请手动填写
unprocessed = 2173  # 未处理（空白）的数量 - 请手动填写

print(f"已发出（打√）: {sent_count}")
print(f"已查但不发（中文）: {checked_not_send}")
print(f"未处理（空白）: {unprocessed}")
print(f"合计: {sent_count + checked_not_send + unprocessed}")

# 验证
if sent_count + checked_not_send + unprocessed != total_emails:
    print(f"\n⚠️  警告：合计数量 ({sent_count + checked_not_send + unprocessed}) 与总数 ({total_emails}) 不符！")

print("\n" + "=" * 80)
print("时间计算")
print("=" * 80)

# 日期计算
start_date = datetime(2026, 1, 7)
end_date = datetime(2026, 10, 6)
days_available = (end_date - start_date).days + 1

print(f"\n开始日期: {start_date.strftime('%Y年%m月%d日')} (今天)")
print(f"结束日期: {end_date.strftime('%Y年%m月%d日')}")
print(f"可用天数: {days_available} 天")

# 计算每天需要处理的数量
if unprocessed > 0:
    emails_per_day = unprocessed / days_available

    print("\n" + "=" * 80)
    print("处理计划")
    print("=" * 80)

    print(f"\n需要处理的email数量: {unprocessed}")
    print(f"每天需要处理: {emails_per_day:.2f} 个")
    print(f"建议每天处理: {int(emails_per_day) + 1} 个 (向上取整)")

    # 不同处理速度的完成时间
    print("\n" + "=" * 80)
    print("不同处理速度的完成时间表")
    print("=" * 80)

    daily_targets = [3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]

    print("\n每天处理 | 需要天数 | 完成日期   | 能否按时完成")
    print("-" * 60)

    for target in daily_targets:
        days_needed = (unprocessed + target - 1) // target
        completion_date = start_date + timedelta(days=days_needed - 1)
        on_time = "✓ 可以" if completion_date <= end_date else "✗ 超时"
        print(f"  {target:2d} 个    | {days_needed:4d} 天  | {completion_date.strftime('%Y-%m-%d')} | {on_time}")

    # 推荐方案
    print("\n" + "=" * 80)
    print("推荐方案")
    print("=" * 80)

    recommended_daily = int(emails_per_day) + 1
    recommended_days = (unprocessed + recommended_daily - 1) // recommended_daily
    recommended_completion = start_date + timedelta(days=recommended_days - 1)

    print(f"\n✨ 推荐每天处理 {recommended_daily} 个email")
    print(f"   - 需要 {recommended_days} 天")
    print(f"   - 预计完成日期: {recommended_completion.strftime('%Y年%m月%d日')}")
    print(f"   - 留有缓冲时间: {(end_date - recommended_completion).days} 天")

    # 保险方案
    safe_daily = recommended_daily + 2
    safe_days = (unprocessed + safe_daily - 1) // safe_daily
    safe_completion = start_date + timedelta(days=safe_days - 1)

    print(f"\n🛡️  保险方案（每天多处理2个）")
    print(f"   - 每天处理 {safe_daily} 个email")
    print(f"   - 需要 {safe_days} 天")
    print(f"   - 预计完成日期: {safe_completion.strftime('%Y年%m月%d日')}")
    print(f"   - 留有缓冲时间: {(end_date - safe_completion).days} 天")

else:
    print("\n所有email已处理完成！🎉")

print("\n" + "=" * 80)

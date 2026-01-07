#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

print("=" * 80)
print("Email处理进度计算器")
print("=" * 80)

# 基本信息（基于用户提供的截图信息）
total_emails = 2173
print(f"\n总email数量: {total_emails}")

# 从用户那里获取已处理的数量（我们需要手动统计图片）
# 这里我们需要用户确认具体数字
print("\n请根据表格统计以下信息:")
print("- 已发出（打√）的数量")
print("- 已查但不发（中文）的数量")
print("- 未处理（空白）的数量")

# 先用估算的方式计算
print("\n" + "=" * 80)
print("假设场景分析:")
print("=" * 80)

# 日期计算
start_date = datetime(2026, 1, 7)
end_date = datetime(2026, 10, 6)
days_available = (end_date - start_date).days + 1

print(f"\n开始日期: {start_date.strftime('%Y年%m月%d日')}")
print(f"结束日期: {end_date.strftime('%Y年%m月%d日')}")
print(f"可用天数: {days_available} 天")

# 不同的未处理数量场景
scenarios = [
    ("假设已处理20%", int(total_emails * 0.8)),
    ("假设已处理30%", int(total_emails * 0.7)),
    ("假设已处理40%", int(total_emails * 0.6)),
    ("假设已处理50%", int(total_emails * 0.5)),
    ("假设已处理10%", int(total_emails * 0.9)),
    ("全部未处理", total_emails),
]

for scenario_name, unprocessed in scenarios:
    print(f"\n{scenario_name}:")
    print(f"  未处理数量: {unprocessed}")
    emails_per_day = unprocessed / days_available
    print(f"  每天需要处理: {emails_per_day:.2f} 个")
    print(f"  建议每天处理: {int(emails_per_day) + 1} 个 (向上取整)")

# 提供不同处理速度的完成时间表
print("\n" + "=" * 80)
print("不同处理速度完成时间对照表 (假设50%未处理):")
print("=" * 80)

unprocessed = int(total_emails * 0.5)
daily_targets = [5, 8, 10, 15, 20, 25, 30, 40, 50]

for target in daily_targets:
    days_needed = (unprocessed + target - 1) // target
    completion_date = start_date + timedelta(days=days_needed - 1)
    status = "✓" if completion_date <= end_date else "✗"
    print(f"{status} 每天处理 {target:2d} 个: 需要 {days_needed:3d} 天, 完成于 {completion_date.strftime('%Y-%m-%d')} ({completion_date.strftime('%m月%d日')})")

print("\n" + "=" * 80)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复总表中所有数据的 Annual Return 计算错误
只修改 Annual Return 列，其他列保持不变
"""

import csv
import shutil
from datetime import datetime
from collections import defaultdict

# 配置
CSV_START_DATE = "20250530"
MASTER_CSV = "option_trading_20250530.csv"

def backup_file():
    """备份总表文件"""
    print("=" * 60)
    print("步骤 1: 备份总表文件")
    print("=" * 60)

    backup_filename = f"{MASTER_CSV}.backup_full"
    shutil.copy2(MASTER_CSV, backup_filename)
    print(f"✓ 已备份总表: {backup_filename}")
    print()

def fix_master_annual_return():
    """修复总表所有数据的 Annual Return"""
    print("=" * 60)
    print("步骤 2: 修复总表 Annual Return")
    print("=" * 60)

    csv_start = datetime.strptime(CSV_START_DATE, "%Y%m%d").date()

    rows = []
    fixed_count = 0
    month_stats = defaultdict(int)  # 按月统计修复数量
    month_examples = defaultdict(list)  # 按月保存示例

    # 读取所有行
    with open(MASTER_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # 跳过表头
        rows.append(header)

        for row in reader:
            if len(row) < 12:
                rows.append(row)
                continue

            date_str = row[0]  # 日期列

            try:
                # 解析数据
                row_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                total_cost = float(row[9])  # Total Cost
                total_return = float(row[10])  # Total Return
                month = row[12] if len(row) > 12 else ""  # Month

                # 计算从CSV开始日期到该行日期的实际天数
                days = (row_date - csv_start).days + 1

                # 重新计算年化收益率
                if total_cost > 0 and days > 0:
                    annual_return = ((total_return / total_cost - 1) / days * 365) * 100
                    old_value = row[11]
                    new_value = f"{annual_return:.4f}%"

                    # 只修改 Annual Return 列
                    row[11] = new_value

                    # 统计
                    month_key = month if month else "未知"
                    month_stats[month_key] += 1
                    fixed_count += 1

                    # 保存每个月的前2个示例
                    if len(month_examples[month_key]) < 2:
                        month_examples[month_key].append({
                            'date': date_str,
                            'days': days,
                            'cost': total_cost,
                            'return': total_return,
                            'old': old_value,
                            'new': new_value
                        })

            except Exception as e:
                print(f"⚠ 处理行出错: {date_str}, 错误: {e}")

            rows.append(row)

    # 写回文件
    with open(MASTER_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✓ 总共修复了 {fixed_count} 行数据\n")

    # 按月份显示统计
    print("各月份修复统计:")
    sorted_months = sorted(month_stats.keys())
    for month in sorted_months:
        count = month_stats[month]
        print(f"  {month}: {count} 行")

    # 显示每个月的示例
    print("\n" + "=" * 60)
    print("各月份修复示例")
    print("=" * 60)

    for month in sorted_months:
        if month in month_examples:
            print(f"\n📅 {month} 月:")
            for i, ex in enumerate(month_examples[month], 1):
                print(f"\n  示例 {i}:")
                print(f"    日期: {ex['date']}")
                print(f"    运行天数: {ex['days']}天（从{CSV_START_DATE}开始）")
                print(f"    成本: {ex['cost']:.0f}, 收益: {ex['return']:.0f}")
                print(f"    修复前: {ex['old']}")
                print(f"    修复后: {ex['new']}")

def verify_fix():
    """验证修复结果"""
    print("\n" + "=" * 60)
    print("步骤 3: 验证修复结果")
    print("=" * 60)

    csv_start = datetime.strptime(CSV_START_DATE, "%Y%m%d").date()

    # 随机抽取几行验证
    verification_dates = [
        "2025-06-06 09:41:02",
        "2025-11-10 09:40:33",
        "2025-12-05 09:40:05"
    ]

    with open(MASTER_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # 跳过表头

        for row in reader:
            if len(row) < 12:
                continue

            date_str = row[0]
            if date_str in verification_dates:
                row_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                total_cost = float(row[9])
                total_return = float(row[10])
                annual_return = row[11]

                days = (row_date - csv_start).days + 1
                expected = ((total_return / total_cost - 1) / days * 365) * 100

                print(f"\n✓ {date_str}")
                print(f"  天数: {days}, 成本: {total_cost:.0f}, 收益: {total_return:.0f}")
                print(f"  CSV中的值: {annual_return}")
                print(f"  计算验证: {expected:.4f}%")
                print(f"  状态: {'✓ 正确' if abs(float(annual_return.rstrip('%')) - expected) < 0.01 else '✗ 错误'}")

def main():
    print("\n开始修复总表所有 Annual Return 数据\n")

    try:
        # 1. 备份文件
        backup_file()

        # 2. 修复数据
        fix_master_annual_return()

        # 3. 验证结果
        verify_fix()

        print("\n" + "=" * 60)
        print("✅ 修复完成！")
        print("=" * 60)
        print(f"\n备份文件: {MASTER_CSV}.backup_full")
        print("如有问题，可使用备份文件恢复")

    except Exception as e:
        print(f"\n❌ 修复过程出错: {e}")
        import traceback
        traceback.print_exc()
        print("\n请检查备份文件并手动恢复")

if __name__ == "__main__":
    main()

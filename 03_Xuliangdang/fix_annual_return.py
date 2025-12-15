#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复总表和月度分表中的 Annual Return 计算错误
"""

import csv
import shutil
from datetime import datetime

# 配置
CSV_START_DATE = "20250530"
MASTER_CSV = "option_trading_20250530.csv"
MONTHLY_CSV = "option_trading_202512.csv"
MONTH_START_DATE = "2025-12-05"  # 从状态文件获取

def backup_files():
    """备份原文件"""
    print("=" * 60)
    print("步骤 1: 备份原文件")
    print("=" * 60)

    # 备份总表
    master_backup = f"{MASTER_CSV}.backup"
    shutil.copy2(MASTER_CSV, master_backup)
    print(f"✓ 已备份总表: {master_backup}")

    # 备份月度分表
    monthly_backup = f"{MONTHLY_CSV}.backup"
    shutil.copy2(MONTHLY_CSV, monthly_backup)
    print(f"✓ 已备份月度分表: {monthly_backup}")
    print()

def fix_master_csv():
    """修复总表中12月份的 Annual Return"""
    print("=" * 60)
    print("步骤 2: 修复总表 (option_trading_20250530.csv)")
    print("=" * 60)

    csv_start = datetime.strptime(CSV_START_DATE, "%Y%m%d").date()

    rows = []
    fixed_count = 0
    examples = []

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

            # 只修复12月的数据
            if date_str.startswith("2025-12-"):
                try:
                    # 解析数据
                    row_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                    total_cost = float(row[9])  # Total Cost
                    total_return = float(row[10])  # Total Return

                    # 计算天数
                    days = (row_date - csv_start).days + 1

                    # 重新计算年化收益率
                    if total_cost > 0 and days > 0:
                        annual_return = ((total_return / total_cost - 1) / days * 365) * 100
                        old_value = row[11]
                        new_value = f"{annual_return:.4f}%"
                        row[11] = new_value

                        # 记录前3个修复示例
                        if fixed_count < 3:
                            examples.append({
                                'date': date_str,
                                'days': days,
                                'cost': total_cost,
                                'return': total_return,
                                'old': old_value,
                                'new': new_value
                            })

                        fixed_count += 1
                except Exception as e:
                    print(f"⚠ 处理行出错: {date_str}, 错误: {e}")

            rows.append(row)

    # 写回文件
    with open(MASTER_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✓ 修复了 {fixed_count} 行12月数据")

    if examples:
        print("\n修复示例（前3行）:")
        for i, ex in enumerate(examples, 1):
            print(f"\n  示例 {i}:")
            print(f"    日期: {ex['date']}")
            print(f"    天数: {ex['days']}天")
            print(f"    成本: {ex['cost']}, 收益: {ex['return']}")
            print(f"    修复前: {ex['old']}")
            print(f"    修复后: {ex['new']}")
    print()

def fix_monthly_csv():
    """修复12月月度分表的年化收益率"""
    print("=" * 60)
    print("步骤 3: 修复月度分表 (option_trading_202512.csv)")
    print("=" * 60)

    month_start = datetime.strptime(MONTH_START_DATE, "%Y-%m-%d").date()

    rows = []
    fixed_count = 0
    examples = []

    # 读取所有行（注意：没有表头）
    with open(MONTHLY_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)

        for row in reader:
            if len(row) < 12:
                rows.append(row)
                continue

            date_str = row[0]  # 日期列

            try:
                # 解析数据
                row_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                total_cost = float(row[9])  # 总成本（当月固定1000）
                total_return = float(row[10])  # 总收益

                # 计算当月天数
                days = (row_date - month_start).days + 1

                # 重新计算年化收益率
                if total_cost > 0 and days > 0:
                    annual_return = ((total_return / total_cost - 1) / days * 365) * 100
                    old_value = row[11]
                    new_value = f"{annual_return:.4f}%"
                    row[11] = new_value

                    # 记录前3个修复示例
                    if fixed_count < 3:
                        examples.append({
                            'date': date_str,
                            'days': days,
                            'cost': total_cost,
                            'return': total_return,
                            'old': old_value,
                            'new': new_value
                        })

                    fixed_count += 1
            except Exception as e:
                print(f"⚠ 处理行出错: {date_str}, 错误: {e}")

            rows.append(row)

    # 写回文件
    with open(MONTHLY_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✓ 修复了 {fixed_count} 行数据")

    if examples:
        print("\n修复示例（前3行）:")
        for i, ex in enumerate(examples, 1):
            print(f"\n  示例 {i}:")
            print(f"    日期: {ex['date']}")
            print(f"    天数: {ex['days']}天（从{MONTH_START_DATE}开始）")
            print(f"    成本: {ex['cost']}, 收益: {ex['return']}")
            print(f"    修复前: {ex['old']}")
            print(f"    修复后: {ex['new']}")
    print()

def main():
    print("\n开始修复 Annual Return 计算错误\n")

    try:
        # 1. 备份文件
        backup_files()

        # 2. 修复总表
        fix_master_csv()

        # 3. 修复月度分表
        fix_monthly_csv()

        print("=" * 60)
        print("✅ 修复完成！")
        print("=" * 60)
        print("\n备份文件:")
        print(f"  - {MASTER_CSV}.backup")
        print(f"  - {MONTHLY_CSV}.backup")
        print("\n如有问题，可使用备份文件恢复")

    except Exception as e:
        print(f"\n❌ 修复过程出错: {e}")
        print("请检查备份文件并手动恢复")

if __name__ == "__main__":
    main()

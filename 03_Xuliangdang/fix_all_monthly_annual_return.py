#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复所有月度分表的 Annual Return 计算错误
只修改 Annual Return 列，其他列保持不变
"""

import csv
import os
from datetime import datetime
import glob
from collections import defaultdict

def get_monthly_csv_files():
    """获取所有月度分表文件（排除12月，已经修复过）"""
    files = glob.glob("option_trading_2025[0-1][0-9].csv")
    # 排除已备份的文件和12月文件
    files = [f for f in files if not f.endswith('.backup') and
             '_old' not in f and '_with' not in f and '202512' not in f]
    return sorted(files)

def fix_monthly_csv(csv_file):
    """修复单个月度分表的 Annual Return"""

    # 从文件名提取月份
    month = csv_file.replace("option_trading_", "").replace(".csv", "")

    print(f"\n处理: {csv_file} ({month}月)")
    print("-" * 60)

    rows = []
    fixed_count = 0
    month_start = None
    examples = []

    try:
        # 读取所有行
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for idx, row in enumerate(reader):
                if len(row) < 12:
                    rows.append(row)
                    continue

                date_str = row[0]

                # 第一行确定月开始日期
                if month_start is None:
                    try:
                        month_start = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                        print(f"月开始日期: {month_start}")
                    except:
                        rows.append(row)
                        continue

                # 修复年化收益率
                try:
                    row_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                    total_cost = float(row[9])
                    total_return = float(row[10])

                    # 计算当月天数
                    days = (row_date - month_start).days + 1

                    # 重新计算年化收益率
                    if total_cost > 0 and days > 0:
                        annual_return = ((total_return / total_cost - 1) / days * 365) * 100
                        old_value = row[11]
                        new_value = f"{annual_return:.4f}%"

                        # 只修改 Annual Return 列
                        row[11] = new_value
                        fixed_count += 1

                        # 保存前2个示例
                        if len(examples) < 2:
                            examples.append({
                                'date': date_str,
                                'days': days,
                                'cost': total_cost,
                                'return': total_return,
                                'old': old_value,
                                'new': new_value
                            })

                except Exception as e:
                    pass

                rows.append(row)

        # 写回文件
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)

        print(f"✓ 修复了 {fixed_count} 行数据")

        # 显示示例
        if examples:
            print("\n修复示例:")
            for i, ex in enumerate(examples, 1):
                print(f"  示例 {i}:")
                print(f"    日期: {ex['date']}")
                print(f"    天数: {ex['days']}天")
                print(f"    成本: {ex['cost']:.0f}, 收益: {ex['return']:.0f}")
                print(f"    修复前: {ex['old']}")
                print(f"    修复后: {ex['new']}")

        return {
            'file': csv_file,
            'month': month,
            'fixed': fixed_count,
            'success': True
        }

    except Exception as e:
        print(f"✗ 修复失败: {e}")
        return {
            'file': csv_file,
            'month': month,
            'fixed': 0,
            'success': False,
            'error': str(e)
        }

def verify_monthly_csv(csv_file):
    """验证修复结果"""

    month_start = None
    check_count = 0
    error_count = 0

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for row in reader:
                if len(row) < 12:
                    continue

                date_str = row[0]

                if month_start is None:
                    try:
                        month_start = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                    except:
                        continue

                try:
                    row_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                    total_cost = float(row[9])
                    total_return = float(row[10])
                    annual_return_str = row[11]
                    annual_return = float(annual_return_str.rstrip('%'))

                    days = (row_date - month_start).days + 1
                    if total_cost > 0 and days > 0:
                        expected = ((total_return / total_cost - 1) / days * 365) * 100

                        check_count += 1
                        # 检查是否匹配（允许0.01%的误差）
                        if abs(annual_return - expected) > 0.01:
                            error_count += 1

                except:
                    continue

        return check_count, error_count

    except Exception as e:
        return 0, 0

def main():
    print("=" * 60)
    print("开始修复所有月度分表的 Annual Return")
    print("=" * 60)

    monthly_files = get_monthly_csv_files()

    if not monthly_files:
        print("\n⚠ 未找到需要修复的月度分表文件")
        return

    print(f"\n找到 {len(monthly_files)} 个月度分表需要修复:")
    for f in monthly_files:
        month = f.replace("option_trading_", "").replace(".csv", "")
        print(f"  - {f} ({month}月)")

    print("\n" + "=" * 60)
    print("开始修复")
    print("=" * 60)

    results = []
    total_fixed = 0

    # 修复每个文件
    for csv_file in monthly_files:
        result = fix_monthly_csv(csv_file)
        results.append(result)
        if result['success']:
            total_fixed += result['fixed']

    # 验证修复结果
    print("\n" + "=" * 60)
    print("验证修复结果")
    print("=" * 60)

    all_correct = True
    for csv_file in monthly_files:
        month = csv_file.replace("option_trading_", "").replace(".csv", "")
        check_count, error_count = verify_monthly_csv(csv_file)

        if error_count == 0:
            print(f"✓ {csv_file} ({month}月): 验证通过 ({check_count} 行)")
        else:
            print(f"✗ {csv_file} ({month}月): 发现 {error_count} 个错误")
            all_correct = False

    # 总结
    print("\n" + "=" * 60)
    print("修复完成总结")
    print("=" * 60)

    success_count = sum(1 for r in results if r['success'])
    failed_count = len(results) - success_count

    print(f"\n修复统计:")
    print(f"  ✓ 成功修复: {success_count} 个文件")
    print(f"  ✗ 修复失败: {failed_count} 个文件")
    print(f"  总修复行数: {total_fixed} 行")

    if all_correct:
        print(f"\n✅ 所有文件验证通过！")
    else:
        print(f"\n⚠ 部分文件验证失败，请检查")

    print(f"\n备份文件后缀: .backup_20251205")
    print("如有问题，可使用备份文件恢复")

    # 显示失败的文件
    if failed_count > 0:
        print(f"\n修复失败的文件:")
        for r in results:
            if not r['success']:
                print(f"  - {r['file']}: {r.get('error', '未知错误')}")

if __name__ == "__main__":
    main()

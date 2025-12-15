#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
备份所有月度分表并检查 Annual Return 是否需要修复
"""

import csv
import shutil
import os
from datetime import datetime
import glob

# 获取今天日期作为备份后缀
BACKUP_SUFFIX = datetime.now().strftime("%Y%m%d")

def get_monthly_csv_files():
    """获取所有月度分表文件"""
    # 匹配 option_trading_YYYYMM.csv 格式
    files = glob.glob("option_trading_2025[0-1][0-9].csv")
    # 排除已备份的文件
    files = [f for f in files if not f.endswith('.backup') and '_old' not in f and '_with' not in f]
    return sorted(files)

def backup_monthly_files():
    """备份所有月度分表文件"""
    print("=" * 60)
    print("步骤 1: 备份所有月度分表文件")
    print("=" * 60)

    monthly_files = get_monthly_csv_files()

    if not monthly_files:
        print("⚠ 未找到月度分表文件")
        return []

    backed_up = []
    for csv_file in monthly_files:
        backup_name = f"{csv_file}.backup_{BACKUP_SUFFIX}"

        # 检查文件是否存在
        if not os.path.exists(csv_file):
            print(f"⚠ 文件不存在: {csv_file}")
            continue

        try:
            shutil.copy2(csv_file, backup_name)
            print(f"✓ 已备份: {csv_file} → {backup_name}")
            backed_up.append(csv_file)
        except Exception as e:
            print(f"✗ 备份失败: {csv_file}, 错误: {e}")

    print(f"\n总共备份了 {len(backed_up)} 个文件")
    print()
    return backed_up

def check_monthly_annual_return(csv_file):
    """检查单个月度分表的 Annual Return 是否正确"""

    # 从文件名提取月份 (YYYYMM)
    month = csv_file.replace("option_trading_", "").replace(".csv", "")

    # 假设月度分表第一行数据的日期就是当月开始日期
    month_start = None
    issues = []
    total_rows = 0

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            for idx, row in enumerate(reader):
                if len(row) < 12:
                    continue

                total_rows += 1
                date_str = row[0]

                # 第一行确定月开始日期
                if month_start is None:
                    try:
                        month_start = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                    except:
                        continue

                # 检查年化收益率计算
                try:
                    row_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S").date()
                    total_cost = float(row[9])
                    total_return = float(row[10])
                    annual_return_str = row[11]

                    # 去掉百分号
                    annual_return = float(annual_return_str.rstrip('%'))

                    # 计算应该的值
                    days = (row_date - month_start).days + 1
                    if total_cost > 0 and days > 0:
                        expected = ((total_return / total_cost - 1) / days * 365) * 100

                        # 检查是否匹配（允许0.01%的误差）
                        if abs(annual_return - expected) > 0.01:
                            if len(issues) < 3:  # 只记录前3个问题示例
                                issues.append({
                                    'row': idx + 1,
                                    'date': date_str,
                                    'days': days,
                                    'cost': total_cost,
                                    'return': total_return,
                                    'current': annual_return_str,
                                    'expected': f"{expected:.4f}%"
                                })
                except Exception as e:
                    continue

        return {
            'file': csv_file,
            'month': month,
            'month_start': month_start,
            'total_rows': total_rows,
            'issues': issues,
            'needs_fix': len(issues) > 0
        }

    except Exception as e:
        print(f"✗ 检查文件失败: {csv_file}, 错误: {e}")
        return None

def check_all_monthly_files():
    """检查所有月度分表文件"""
    print("=" * 60)
    print("步骤 2: 检查所有月度分表的 Annual Return")
    print("=" * 60)

    monthly_files = get_monthly_csv_files()

    if not monthly_files:
        print("⚠ 未找到月度分表文件")
        return

    needs_fix_list = []
    ok_list = []

    for csv_file in monthly_files:
        result = check_monthly_annual_return(csv_file)

        if result is None:
            continue

        if result['needs_fix']:
            needs_fix_list.append(result)
        else:
            ok_list.append(result)

    # 显示检查结果
    print(f"\n检查完成:")
    print(f"  ✓ 正确的文件: {len(ok_list)} 个")
    print(f"  ✗ 需要修复的文件: {len(needs_fix_list)} 个")

    if ok_list:
        print(f"\n✓ 以下文件的 Annual Return 计算正确:")
        for result in ok_list:
            print(f"  - {result['file']} ({result['month']}, {result['total_rows']} 行)")

    if needs_fix_list:
        print(f"\n✗ 以下文件需要修复:")
        for result in needs_fix_list:
            print(f"\n  📁 {result['file']} ({result['month']})")
            print(f"     月开始日期: {result['month_start']}")
            print(f"     总行数: {result['total_rows']}")
            print(f"     发现 {len(result['issues'])} 个错误（显示前3个）:")

            for issue in result['issues']:
                print(f"\n     问题行 #{issue['row']}:")
                print(f"       日期: {issue['date']}")
                print(f"       天数: {issue['days']}天")
                print(f"       成本: {issue['cost']}, 收益: {issue['return']}")
                print(f"       当前值: {issue['current']}")
                print(f"       应该是: {issue['expected']}")

    print("\n" + "=" * 60)

    return needs_fix_list

def main():
    print(f"\n开始备份和检查所有月度分表文件")
    print(f"备份后缀: {BACKUP_SUFFIX}\n")

    try:
        # 1. 备份所有月度分表
        backed_up = backup_monthly_files()

        if not backed_up:
            print("没有文件被备份，退出")
            return

        # 2. 检查所有月度分表
        needs_fix = check_all_monthly_files()

        print("✅ 检查完成！")
        print(f"\n备份文件使用后缀: .backup_{BACKUP_SUFFIX}")

        if needs_fix:
            print(f"\n⚠ 发现 {len(needs_fix)} 个文件需要修复 Annual Return")
            print("建议运行修复脚本进行修复")
        else:
            print("\n✓ 所有月度分表的 Annual Return 都是正确的")

    except Exception as e:
        print(f"\n❌ 处理过程出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

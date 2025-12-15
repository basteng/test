#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正12月CSV数据中的错误基础值
- 余数成本：66 → 33
- 总表Total Cost：6000 → 7000
- 重新计算Total Return
"""

import csv
import shutil
from datetime import datetime

# 备份文件
def backup_file(filepath):
    backup_path = f"{filepath}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(filepath, backup_path)
    print(f"✅ 已备份: {backup_path}")
    return backup_path

# 修正月度CSV
def fix_monthly_csv():
    csv_file = "option_trading_202512.csv"
    print(f"\n📝 修正月度CSV: {csv_file}")

    backup_file(csv_file)

    rows = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)

        count = 0
        for row in reader:
            # 列索引: 8=余数成本, 9=总成本, 10=总收益
            # 修正余数成本
            old_remainder = int(row[8])
            if old_remainder == 66:
                row[8] = '33'  # 新余数成本

                # 重新计算总收益
                call_contracts = int(row[6])
                put_contracts = int(row[7])
                call_price = float(row[4])
                put_price = float(row[5])

                current_option_value = int(call_contracts * call_price * 10000 + put_contracts * put_price * 10000)
                new_total_return = current_option_value + 33
                row[10] = str(new_total_return)

                count += 1

            rows.append(row)

    # 写回文件
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ 已修正 {count} 条记录")

# 修正总表CSV
def fix_master_csv():
    csv_file = "option_trading_20250530.csv"
    print(f"\n📝 修正总表CSV: {csv_file}")

    backup_file(csv_file)

    rows = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)

        count = 0
        for row in reader:
            # 只处理12月的数据
            if row[12] == '202512':
                # 列索引: 8=Remainder Cost, 9=Total Cost, 10=Total Return
                old_remainder = int(row[8])
                if old_remainder == 66:
                    row[8] = '33'  # 新余数成本
                    row[9] = '7000'  # 新Total Cost

                    # 重新计算Total Return
                    call_contracts = int(row[6])
                    put_contracts = int(row[7])
                    call_price = float(row[4])
                    put_price = float(row[5])

                    current_option_value = int(call_contracts * call_price * 10000 + put_contracts * put_price * 10000)
                    new_total_return = current_option_value + 33 + 5607  # 加上11月的最终收益
                    row[10] = str(new_total_return)

                    count += 1

            rows.append(row)

    # 写回文件
    with open(csv_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ 已修正 {count} 条记录")

if __name__ == "__main__":
    print("=" * 60)
    print("开始修正12月CSV数据")
    print("=" * 60)

    try:
        fix_monthly_csv()
        fix_master_csv()

        print("\n" + "=" * 60)
        print("✅ 所有CSV数据修正完成！")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ 修正失败: {str(e)}")
        import traceback
        traceback.print_exc()

"""
这个脚本用于直接测试向总表和月度分表同时写入数据
"""

import os
import csv
import datetime
from XuTwo import get_csv_filename, CSV_START_DATE

def display_csv_content(filename, max_rows=5):
    """显示CSV文件的内容"""
    print(f"\n文件：{filename}")
    
    if not os.path.exists(filename):
        print(f"文件不存在: {filename}")
        return False
        
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i < max_rows:
                    print(row)
                else:
                    print("...")
                    break
        return True
    except Exception as e:
        print(f"读取文件出错: {e}")
        return False

def write_test_data():
    """测试向总表和月度分表同时写入数据"""
    # 使用当前日期创建文件名
    current_month = datetime.datetime.now().strftime("%Y%m")
    
    # 获取总表文件名
    master_csv = get_csv_filename()
    # 获取月度分表文件名
    monthly_csv = f"option_trading_{current_month}.csv"
    
    # 准备测试数据
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    etf_price = 3.25
    call_strike = 3.35
    put_strike = 3.15
    call_price = 0.0095
    put_price = 0.0102
    call_qty = 526
    put_qty = 490
    remainder_cost = 11
    total_cost = 1000
    total_return = 1020
    annual_return = "4.5%"
    
    print(f"测试写入总表: {master_csv}")
    try:
        # 1. 写入总表
        with open(master_csv, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                current_datetime,
                etf_price,
                call_strike,
                put_strike,
                call_price,
                put_price,
                call_qty,
                put_qty,
                remainder_cost,
                total_cost,
                total_return,
                annual_return,
                current_month
            ])
            file.flush()
        print(f"✅ 成功写入总表数据")
    except Exception as e:
        print(f"❌ 写入总表数据失败: {e}")
        return False
        
    print(f"测试写入月度分表: {monthly_csv}")
    try:
        # 2. 写入月度分表
        with open(monthly_csv, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                current_datetime,
                etf_price,
                call_strike,
                put_strike,
                call_price,
                put_price,
                call_qty,
                put_qty,
                remainder_cost,
                total_cost,
                total_return,
                annual_return
            ])
            file.flush()
        print(f"✅ 成功写入月度分表数据")
        return True
    except Exception as e:
        print(f"❌ 写入月度分表数据失败: {e}")
        return False

if __name__ == "__main__":
    print(f"当前的CSV开始日期: {CSV_START_DATE}")
    master_csv = get_csv_filename()
    current_month = datetime.datetime.now().strftime("%Y%m")
    monthly_csv = f"option_trading_{current_month}.csv"
    
    print(f"当前使用的总表文件: {master_csv}")
    print(f"当前使用的月度分表文件: {monthly_csv}")
    
    # 显示文件内容（写入前）
    print("\n写入前文件内容:")
    display_csv_content(master_csv)
    display_csv_content(monthly_csv)
    
    # 测试写入数据
    if write_test_data():
        print("\n写入数据后文件内容:")
        display_csv_content(master_csv)
        display_csv_content(monthly_csv)
    else:
        print("\n写入测试数据失败")

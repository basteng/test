"""
这个脚本用于测试XuTwo.py程序中的双重CSV文件写入功能
它将检查总表和月度分表是否都正常工作
"""

import os
import csv
import datetime
import time
from XuTwo import get_csv_filename, start_new_record_cycle, CSV_START_DATE, create_csv_file

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
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    current_month = datetime.datetime.now().strftime("%Y%m")
    
    # 获取总表文件名
    master_csv = get_csv_filename()
    # 获取月度分表文件名
    monthly_csv = f"option_trading_{current_month}.csv"
    
    # 确保文件存在
    create_csv_file(current_month)
    
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

def main():
    """主函数"""
    # 显示当前配置
    print(f"当前的CSV开始日期: {CSV_START_DATE}")
    master_csv = get_csv_filename()
    current_month = datetime.datetime.now().strftime("%Y%m")
    monthly_csv = f"option_trading_{current_month}.csv"
    
    print(f"当前使用的总表文件: {master_csv}")
    print(f"当前使用的月度分表文件: {monthly_csv}")
    
    # 显示总表内容
    if os.path.exists(master_csv):
        display_csv_content(master_csv)
    else:
        print(f"总表文件不存在: {master_csv}")
    
    # 显示月度分表内容
    if os.path.exists(monthly_csv):
        display_csv_content(monthly_csv)
    else:
        print(f"月度分表文件不存在: {monthly_csv}")
    
    # 询问是否测试写入
    print("\n请选择操作:")
    print("1. 测试向总表和月度分表写入数据")
    print("2. 创建新的CSV记录周期")
    print("3. 退出")
    
    choice = input("请输入选项 (1-3): ")
    
    if choice == '1':
        # 测试写入数据
        if write_test_data():
            print("\n写入数据后文件内容:")
            display_csv_content(master_csv)
            display_csv_content(monthly_csv)
            return True
        return False
        
    elif choice == '2':
        # 创建新的CSV记录周期
        date_str = input("请输入日期 (格式: YYYYMMDD，如20250603，留空则使用当前日期): ")
        if date_str and len(date_str) != 8:
            print("日期格式错误，应为YYYYMMDD (例如: 20250603)")
            return False
        
        # 调用函数创建新周期
        if date_str:
            new_csv = start_new_record_cycle(date_str)
        else:
            new_csv = start_new_record_cycle()
        print(f"已创建新的CSV文件: {new_csv}")
        
        # 创建或确保月度文件存在
        current_month = datetime.datetime.now().strftime("%Y%m")
        create_csv_file(current_month)
        
        # 显示新文件内容
        print("\n新总表文件内容:")
        display_csv_content(new_csv)
        
        monthly_csv = f"option_trading_{current_month}.csv"
        print("\n月度分表文件内容:")
        display_csv_content(monthly_csv)
        return True
        
    else:
        print("已取消操作")
        return True

if __name__ == "__main__":
    main()

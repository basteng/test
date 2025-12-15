"""
这个脚本用于测试XuTwo.py程序中的新CSV记录周期功能
它将创建一个新的CSV文件用于记录交易数据
"""

import os
import csv
import datetime
from XuTwo import get_csv_filename, start_new_record_cycle, CSV_START_DATE

def main():
    # 显示当前配置
    print(f"当前的CSV开始日期: {CSV_START_DATE}")
    current_csv = get_csv_filename()
    print(f"当前使用的CSV文件: {current_csv}")
    
    if os.path.exists(current_csv):
        print(f"文件已存在，显示前5行内容:")
        try:
            with open(current_csv, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if i < 5:
                        print(row)
                    else:
                        break
        except Exception as e:
            print(f"读取文件时出错: {e}")
    else:
        print(f"文件不存在: {current_csv}")
    
    # 询问用户是否创建新的CSV文件
    print("\n选项:")
    print("1. 使用当前日期创建新的CSV文件")
    print("2. 手动输入日期创建新的CSV文件")
    print("3. 退出")
    
    choice = input("请输入选项 (1-3): ")
    
    if choice == '1':
        # 使用当前日期
        new_csv = start_new_record_cycle()
        print(f"已创建新的CSV文件: {new_csv}")
    elif choice == '2':
        # 手动输入日期
        date_str = input("请输入日期 (格式: YYYYMMDD): ")
        if len(date_str) != 8 or not date_str.isdigit():
            print("日期格式错误，应为YYYYMMDD (例如: 20250603)")
            return
        
        new_csv = start_new_record_cycle(date_str)
        print(f"已创建新的CSV文件: {new_csv}")
    else:
        print("已取消操作")

if __name__ == "__main__":
    main()

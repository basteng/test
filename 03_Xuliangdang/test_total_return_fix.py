"""
测试Total Return跨月计算修复
"""
import os
import sys
import csv
import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from XuTwo import get_previous_month_final_return, get_csv_filename

def test_previous_month_final_return():
    """测试get_previous_month_final_return函数"""
    print("测试get_previous_month_final_return函数")
    
    # 测试当前CSV文件
    csv_filename = get_csv_filename()
    print(f"总表CSV文件: {csv_filename}")
    
    if not os.path.exists(csv_filename):
        print("总表CSV文件不存在")
        return
    
    # 读取CSV文件查看数据
    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    print(f"总表中共有 {len(rows)} 条记录")
    
    # 显示最后几条记录
    print("\n最后5条记录:")
    for row in rows[-5:]:
        print(f"日期: {row['Date']}, 月份: {row['Month']}, Total Return: {row['Total Return']}")
    
    # 测试函数
    previous_month_return = get_previous_month_final_return()
    print(f"\n通过函数获取的上月最终Total Return: {previous_month_return}")
    
    # 手动验证：查找上个月的最后一条记录
    current_month = datetime.datetime.now().strftime("%Y%m")
    current_year = int(current_month[:4])
    current_month_num = int(current_month[4:])
    
    if current_month_num == 1:
        previous_month = f"{current_year - 1}12"
    else:
        previous_month = f"{current_year}{current_month_num - 1:02d}"
    
    print(f"\n当前月份: {current_month}, 上个月: {previous_month}")
    
    # 找到上个月的记录
    previous_month_records = []
    current_month_records = []
    
    for row in rows:
        if row['Month'] == previous_month:
            previous_month_records.append(row)
        elif row['Month'] == current_month:
            current_month_records.append(row)
    
    print(f"\n上月记录数: {len(previous_month_records)}")
    print(f"当月记录数: {len(current_month_records)}")
    
    if previous_month_records:
        last_previous_record = previous_month_records[-1]
        print(f"上月最后一条记录: 日期={last_previous_record['Date']}, Total Return={last_previous_record['Total Return']}")
    
    if current_month_records:
        first_current_record = current_month_records[0]
        print(f"当月第一条记录: 日期={first_current_record['Date']}, Total Return={first_current_record['Total Return']}")
        
        # 分析跨月计算逻辑
        print(f"\n分析跨月计算:")
        print(f"上月最终Total Return: {previous_month_return}")
        print(f"当月第一条Total Return: {first_current_record['Total Return']}")
        print(f"当月Total Cost: {first_current_record['Total Cost']}")
        
        if int(first_current_record['Total Cost']) > 1000:
            print("✅ 检测到跨月情况（Total Cost > 1000）")
            expected_logic = f"应该是: 上月最终Total Return({previous_month_return}) + 当月期权价值 + 当月余数成本"
            print(f"期望的计算逻辑: {expected_logic}")
        else:
            print("❌ 未检测到跨月情况")

if __name__ == "__main__":
    test_previous_month_final_return()
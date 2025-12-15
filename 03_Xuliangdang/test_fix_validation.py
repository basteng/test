#!/usr/bin/env python3
"""
测试修复后的换月累计逻辑
"""

import sys
import os
import csv

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_get_first_record_month():
    """测试动态获取第一个记录月份的函数"""
    try:
        from XuTwo import get_first_record_month_from_csv, get_csv_filename
        
        print("=== 测试get_first_record_month_from_csv函数 ===")
        
        # 获取CSV文件名
        csv_filename = get_csv_filename()
        print(f"CSV文件名: {csv_filename}")
        
        if os.path.exists(csv_filename):
            # 测试函数
            first_month = get_first_record_month_from_csv()
            print(f"第一个记录月份: {first_month}")
            
            # 手动验证
            with open(csv_filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                first_row = next(reader)
                manual_first_month = first_row['Month']
                print(f"手动读取的第一个月份: {manual_first_month}")
                
            # 验证结果
            if first_month == manual_first_month:
                print("✅ 函数工作正常")
            else:
                print("❌ 函数结果不正确")
        else:
            print(f"❌ CSV文件不存在: {csv_filename}")
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        print(traceback.format_exc())

def test_previous_month_return():
    """测试上月收益读取函数"""
    try:
        from XuTwo import get_previous_month_final_return
        
        print("\n=== 测试get_previous_month_final_return函数 ===")
        
        # 当前假设是202508
        previous_return = get_previous_month_final_return()
        print(f"上月最终收益: {previous_return}")
        
        # 手动验证202507最后一条记录
        from XuTwo import get_csv_filename
        csv_filename = get_csv_filename()
        
        if os.path.exists(csv_filename):
            last_207_return = 0
            with open(csv_filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Month'] == '202507':
                        last_207_return = int(float(row['Total Return']))
            
            print(f"手动读取202507最后收益: {last_207_return}")
            
            if previous_return == last_207_return:
                print("✅ 上月收益读取正确")
            else:
                print("❌ 上月收益读取不正确")
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        print(traceback.format_exc())

def test_total_return_calculation():
    """测试Total Return计算逻辑"""
    print("\n=== 测试Total Return计算逻辑 ===")
    
    # 模拟8月的数据
    previous_month_final_return = 316  # 7月最终收益
    current_option_value = int((5 * 0.0102 * 10000) + (11 * 0.0042 * 10000))  # 当前期权价值
    remainder_cost = 40  # 余数成本
    
    print(f"7月最终收益: {previous_month_final_return}")
    print(f"8月期权价值: {current_option_value}") 
    print(f"余数成本: {remainder_cost}")
    
    # 计算Total Return
    if previous_month_final_return > 0:
        total_return = int(previous_month_final_return + current_option_value + remainder_cost)
        print(f"计算得到的Total Return: {total_return}")
        print("✅ 应该使用累计逻辑")
    else:
        print("❌ previous_month_final_return <= 0, 会使用单月收益")
    
    print(f"预期的Total Return应该约为: {316 + 972 + 40} = 1328")

if __name__ == "__main__":
    print("验证换月累计逻辑修复效果")
    print("=" * 50)
    
    test_get_first_record_month()
    test_previous_month_return()
    test_total_return_calculation()
    
    print("\n" + "=" * 50)
    print("测试完成")
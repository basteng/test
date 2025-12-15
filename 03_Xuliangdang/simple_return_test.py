"""
简单的Total Return计算测试
"""
import csv
import datetime

def test_total_return_calculation():
    """测试Total Return计算逻辑"""
    csv_filename = "option_trading_20250530.csv"
    
    # 读取CSV文件
    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"总表中共有 {len(rows)} 条记录")
    
    # 分析6月和7月的数据
    june_records = []
    july_records = []
    
    for row in rows:
        if row['Month'] == '202506':
            june_records.append(row)
        elif row['Month'] == '202507':
            july_records.append(row)
    
    print(f"\n6月记录数: {len(june_records)}")
    print(f"7月记录数: {len(july_records)}")
    
    if june_records:
        print(f"\n6月最后一条记录:")
        last_june = june_records[-1]
        print(f"日期: {last_june['Date']}")
        print(f"Total Cost: {last_june['Total Cost']}")
        print(f"Total Return: {last_june['Total Return']}")
        
    if july_records:
        print(f"\n7月第一条记录:")
        first_july = july_records[0]
        print(f"日期: {first_july['Date']}")
        print(f"Total Cost: {first_july['Total Cost']}")
        print(f"Total Return: {first_july['Total Return']}")
        
        print(f"\n问题分析:")
        print(f"6月最终Total Return: {last_june['Total Return']}")
        print(f"7月第一条Total Return: {first_july['Total Return']}")
        print(f"7月Total Cost: {first_july['Total Cost']}")
        
        # 计算期望的7月Total Return
        june_final_return = int(float(last_june['Total Return']))
        july_call_value = int(float(first_july['Call Price']) * float(first_july['Call Qty']) * 10000)
        july_put_value = int(float(first_july['Put Price']) * float(first_july['Put Qty']) * 10000)
        july_remainder = int(float(first_july['Remainder Cost']))
        
        expected_july_return = june_final_return + july_call_value + july_put_value + july_remainder
        actual_july_return = int(float(first_july['Total Return']))
        
        print(f"\n期望的7月Total Return计算:")
        print(f"6月最终Total Return: {june_final_return}")
        print(f"7月Call期权价值: {july_call_value}")
        print(f"7月Put期权价值: {july_put_value}")
        print(f"7月余数成本: {july_remainder}")
        print(f"期望Total Return: {expected_july_return}")
        print(f"实际Total Return: {actual_july_return}")
        print(f"差异: {expected_july_return - actual_july_return}")

if __name__ == "__main__":
    test_total_return_calculation()
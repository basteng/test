"""
分析总表和当月表中的错误数据
"""
import csv
import datetime

def analyze_error_data():
    """分析错误数据的特征"""
    
    # 分析总表数据
    print("=== 分析总表数据 ===")
    master_csv = "option_trading_20250530.csv"
    
    with open(master_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"总表总记录数: {len(rows)}")
    
    # 分析6月和7月数据
    june_records = [row for row in rows if row['Month'] == '202506']
    july_records = [row for row in rows if row['Month'] == '202507']
    
    print(f"6月记录数: {len(june_records)}")
    print(f"7月记录数: {len(july_records)}")
    
    if june_records:
        june_last = june_records[-1]
        print(f"\n6月最后记录:")
        print(f"日期: {june_last['Date']}")
        print(f"Total Cost: {june_last['Total Cost']}")
        print(f"Total Return: {june_last['Total Return']}")
        
    if july_records:
        july_first = july_records[0]
        print(f"\n7月第一条记录:")
        print(f"日期: {july_first['Date']}")
        print(f"Total Cost: {july_first['Total Cost']}")
        print(f"Total Return: {july_first['Total Return']}")
        
        # 分析7月数据的问题
        print(f"\n7月数据问题分析:")
        expected_total_return = int(june_last['Total Return']) + int(july_first['Total Return']) - 1000
        print(f"6月最终Total Return: {june_last['Total Return']}")
        print(f"7月当前Total Return: {july_first['Total Return']}")
        print(f"期望的7月Total Return应该是: {expected_total_return}")
        
        # 检查哪些7月记录的Total Return是错误的
        error_count = 0
        for record in july_records:
            if int(record['Total Cost']) == 2000 and int(record['Total Return']) < 1050:
                error_count += 1
        
        print(f"7月错误记录数量（Total Cost=2000但Total Return<1050）: {error_count}")
    
    # 分析当月表数据
    print(f"\n=== 分析当月表数据 ===")
    monthly_csv = "option_trading_202507.csv"
    
    try:
        with open(monthly_csv, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            monthly_rows = list(reader)
        
        print(f"当月表总记录数: {len(monthly_rows)}")
        
        if monthly_rows:
            first_record = monthly_rows[0]
            print(f"\n当月表第一条记录:")
            print(f"日期: {first_record['日期']}")
            print(f"总成本: {first_record['总成本']}")
            print(f"总收益: {first_record['总收益']}")
            print(f"年化收益率: {first_record['年化收益率']}")
            
            # 检查年化收益率问题
            total_cost = float(first_record['总成本'])
            total_return = float(first_record['总收益'])
            annual_return = float(first_record['年化收益率'].replace('%', ''))
            
            print(f"\n年化收益率问题分析:")
            print(f"总成本: {total_cost}")
            print(f"总收益: {total_return}")
            print(f"当前年化收益率: {annual_return}%")
            
            # 正确的当月年化收益率应该是0%（因为总收益=总成本）
            expected_monthly_return = (total_return / total_cost - 1) * 100
            print(f"期望的当月收益率: {expected_monthly_return}%")
            
            # 如果按3天计算年化
            expected_annual = expected_monthly_return / 3 * 365
            print(f"期望的当月年化收益率（按3天计算）: {expected_annual}%")
    
    except FileNotFoundError:
        print("当月表文件不存在")
    
    return {
        'june_final_return': int(june_last['Total Return']) if june_records else 0,
        'july_records_count': len(july_records),
        'monthly_records_count': len(monthly_rows) if 'monthly_rows' in locals() else 0
    }

if __name__ == "__main__":
    analyze_error_data()
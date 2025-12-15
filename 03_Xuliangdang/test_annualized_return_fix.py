"""
测试年化收益率计算修复
"""
import csv
import datetime

def test_annualized_return():
    """测试年化收益率计算"""
    print("测试年化收益率计算修复")
    
    # 读取总表和当月CSV
    master_csv = "option_trading_20250530.csv"
    monthly_csv = "option_trading_202507.csv"
    
    print(f"\n分析文件: {master_csv} 和 {monthly_csv}")
    
    # 读取总表数据
    with open(master_csv, 'r', encoding='utf-8') as f:
        master_reader = csv.DictReader(f)
        master_rows = list(master_reader)
    
    # 读取当月数据
    with open(monthly_csv, 'r', encoding='utf-8') as f:
        monthly_reader = csv.DictReader(f)
        monthly_rows = list(monthly_reader)
    
    # 分析7月的数据
    july_master_records = [row for row in master_rows if row['Month'] == '202507']
    
    print(f"\n总表中7月记录数: {len(july_master_records)}")
    print(f"月表中7月记录数: {len(monthly_rows)}")
    
    if july_master_records and monthly_rows:
        # 取第一条记录进行对比
        master_first = july_master_records[0]
        monthly_first = monthly_rows[0]
        
        print(f"\n总表第一条7月记录:")
        print(f"日期: {master_first['Date']}")
        print(f"Total Cost: {master_first['Total Cost']}")
        print(f"Total Return: {master_first['Total Return']}")
        print(f"Annual Return: {master_first['Annual Return']}")
        
        print(f"\n月表第一条记录:")
        print(f"日期: {monthly_first['日期']}")
        print(f"总成本: {monthly_first['总成本']}")
        print(f"总收益: {monthly_first['总收益']}")
        print(f"年化收益率: {monthly_first['年化收益率']}")
        
        # 计算期望的年化收益率
        print(f"\n年化收益率分析:")
        
        # 总表年化收益率计算（假设运行了45天）
        total_cost = float(master_first['Total Cost'])
        total_return = float(master_first['Total Return'])
        days_running = 45  # 假设的总运行天数
        
        expected_master_annual = ((total_return / total_cost - 1) / days_running * 365) * 100
        print(f"总表期望年化收益率: {expected_master_annual:.4f}%")
        print(f"总表实际年化收益率: {master_first['Annual Return']}")
        
        # 月表年化收益率计算（假设当月运行了3天）
        monthly_cost = float(monthly_first['总成本'])
        monthly_return = float(monthly_first['总收益'])
        monthly_days = 3  # 假设的当月运行天数
        
        expected_monthly_annual = ((monthly_return / monthly_cost - 1) / monthly_days * 365) * 100
        print(f"月表期望年化收益率: {expected_monthly_annual:.4f}%")
        print(f"月表实际年化收益率: {monthly_first['年化收益率']}")
        
        # 验证修复
        master_annual = float(master_first['Annual Return'].replace('%', ''))
        monthly_annual = float(monthly_first['年化收益率'].replace('%', ''))
        
        print(f"\n修复验证:")
        print(f"总表和月表年化收益率是否相同: {'是' if abs(master_annual - monthly_annual) < 0.01 else '否'}")
        print(f"相同说明没有修复，不同说明已经分别计算")

if __name__ == "__main__":
    test_annualized_return()
"""
清理所有7月的错误数据
"""
import csv
import os

def clean_all_july_data():
    """清理所有7月的错误数据"""
    print("=== 清理所有7月错误数据 ===")
    
    master_csv = "option_trading_20250530.csv"
    temp_csv = "option_trading_20250530_temp.csv"
    
    # 读取所有数据
    with open(master_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"原始总记录数: {len(rows)}")
    
    # 统计各月数据
    june_count = len([row for row in rows if row['Month'] == '202506'])
    july_count = len([row for row in rows if row['Month'] == '202507'])
    other_count = len([row for row in rows if row['Month'] not in ['202506', '202507']])
    
    print(f"6月记录数: {june_count}")
    print(f"7月记录数: {july_count}")
    print(f"其他月份记录数: {other_count}")
    
    # 只保留非7月的数据
    clean_rows = [row for row in rows if row['Month'] != '202507']
    
    print(f"清理后记录数: {len(clean_rows)}")
    print(f"移除7月记录数: {july_count}")
    
    # 写入清理后的数据
    with open(temp_csv, 'w', newline='', encoding='utf-8') as f:
        if clean_rows:
            fieldnames = clean_rows[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(clean_rows)
    
    # 替换原文件
    os.replace(temp_csv, master_csv)
    print(f"总表清理完成，所有7月数据已移除")
    
    # 显示6月最后的记录
    june_records = [row for row in clean_rows if row['Month'] == '202506']
    if june_records:
        june_last = june_records[-1]
        print(f"\n6月最后记录:")
        print(f"日期: {june_last['Date']}")
        print(f"Total Cost: {june_last['Total Cost']}")
        print(f"Total Return: {june_last['Total Return']}")
    
    return len(clean_rows), july_count

def verify_cleanup():
    """验证清理结果"""
    print(f"\n=== 验证清理结果 ===")
    
    master_csv = "option_trading_20250530.csv"
    with open(master_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    june_count = len([row for row in rows if row['Month'] == '202506'])
    july_count = len([row for row in rows if row['Month'] == '202507'])
    
    print(f"验证结果:")
    print(f"  总记录数: {len(rows)}")
    print(f"  6月记录数: {june_count}")
    print(f"  7月记录数: {july_count}")
    
    if july_count == 0:
        print("✅ 所有7月错误数据已清理完成")
    else:
        print("❌ 仍有7月数据残留")
    
    # 检查当月表
    monthly_csv = "option_trading_202507.csv"
    with open(monthly_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        monthly_rows = list(reader)
    
    print(f"  当月表记录数: {len(monthly_rows)}")
    
    if len(monthly_rows) == 0:
        print("✅ 当月表已清空")
    else:
        print("❌ 当月表仍有数据")

def main():
    print("开始清理所有7月错误数据...")
    
    # 清理所有7月数据
    clean_count, removed_count = clean_all_july_data()
    
    # 验证清理结果
    verify_cleanup()
    
    print(f"\n=== 清理总结 ===")
    print(f"保留记录数: {clean_count}")
    print(f"移除7月记录数: {removed_count}")
    print(f"数据清理完成！程序重新运行时将生成正确的7月数据。")

if __name__ == "__main__":
    main()
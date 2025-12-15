"""
清理总表和当月表中的错误数据
"""
import csv
import datetime
import os

def clean_master_csv():
    """清理总表中的错误数据"""
    print("=== 清理总表错误数据 ===")
    
    master_csv = "option_trading_20250530.csv"
    temp_csv = "option_trading_20250530_temp.csv"
    
    # 读取所有数据
    with open(master_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"原始总记录数: {len(rows)}")
    
    # 分析6月最后的Total Return
    june_records = [row for row in rows if row['Month'] == '202506']
    june_final_return = 93  # 从分析中得知
    
    print(f"6月最终Total Return: {june_final_return}")
    
    # 过滤掉错误的7月数据
    clean_rows = []
    removed_count = 0
    
    for row in rows:
        # 保留6月的所有数据
        if row['Month'] == '202506':
            clean_rows.append(row)
        # 7月数据需要检查
        elif row['Month'] == '202507':
            total_cost = int(float(row['Total Cost']))
            total_return = int(float(row['Total Return']))
            
            # 错误数据特征：Total Cost=2000但Total Return没有正确累加6月收益
            if total_cost == 2000 and total_return < (june_final_return + 900):
                removed_count += 1
                print(f"移除错误记录: 日期={row['Date']}, Total Return={total_return}")
            else:
                clean_rows.append(row)
        else:
            # 其他月份保留
            clean_rows.append(row)
    
    print(f"移除错误记录数: {removed_count}")
    print(f"清理后记录数: {len(clean_rows)}")
    
    # 写入清理后的数据
    with open(temp_csv, 'w', newline='', encoding='utf-8') as f:
        if clean_rows:
            fieldnames = clean_rows[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(clean_rows)
    
    # 替换原文件
    os.replace(temp_csv, master_csv)
    print(f"总表清理完成，保存到 {master_csv}")
    
    return len(clean_rows), removed_count

def clean_monthly_csv():
    """清理当月表中的错误数据"""
    print(f"\n=== 清理当月表错误数据 ===")
    
    monthly_csv = "option_trading_202507.csv"
    temp_csv = "option_trading_202507_temp.csv"
    
    if not os.path.exists(monthly_csv):
        print("当月表文件不存在")
        return 0, 0
    
    # 读取所有数据
    with open(monthly_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"原始记录数: {len(rows)}")
    
    # 清理策略：删除所有记录，因为年化收益率计算错误
    # 当程序重新运行时会生成正确的数据
    clean_rows = []
    removed_count = len(rows)
    
    print(f"移除所有错误记录: {removed_count}")
    
    # 写入空的CSV文件（只保留表头）
    with open(temp_csv, 'w', newline='', encoding='utf-8') as f:
        if rows:  # 如果有数据，保留表头结构
            fieldnames = rows[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            # 不写入任何数据行
    
    # 替换原文件
    os.replace(temp_csv, monthly_csv)
    print(f"当月表清理完成，保存到 {monthly_csv}")
    
    return 0, removed_count

def verify_cleaned_data():
    """验证清理后的数据"""
    print(f"\n=== 验证清理结果 ===")
    
    # 验证总表
    master_csv = "option_trading_20250530.csv"
    with open(master_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    june_records = [row for row in rows if row['Month'] == '202506']
    july_records = [row for row in rows if row['Month'] == '202507']
    
    print(f"总表验证:")
    print(f"  6月记录数: {len(june_records)}")
    print(f"  7月记录数: {len(july_records)}")
    
    if june_records:
        june_last = june_records[-1]
        print(f"  6月最后记录Total Return: {june_last['Total Return']}")
    
    if july_records:
        july_first = july_records[0]
        print(f"  7月第一条记录Total Return: {july_first['Total Return']}")
    else:
        print(f"  7月记录已全部清除")
    
    # 验证当月表
    monthly_csv = "option_trading_202507.csv"
    with open(monthly_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        monthly_rows = list(reader)
    
    print(f"\n当月表验证:")
    print(f"  记录数: {len(monthly_rows)}")

def main():
    """主函数"""
    print("开始清理错误数据...")
    
    # 清理总表
    master_clean_count, master_removed_count = clean_master_csv()
    
    # 清理当月表
    monthly_clean_count, monthly_removed_count = clean_monthly_csv()
    
    # 验证结果
    verify_cleaned_data()
    
    print(f"\n=== 清理总结 ===")
    print(f"总表: 保留 {master_clean_count} 条记录, 移除 {master_removed_count} 条错误记录")
    print(f"当月表: 保留 {monthly_clean_count} 条记录, 移除 {monthly_removed_count} 条错误记录")
    print(f"数据清理完成！")

if __name__ == "__main__":
    main()
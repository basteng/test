#!/usr/bin/env python3
"""
修复option_trading_20250530.csv中8月份的错误Total Return数据
将8月份的Total Return从错误的单月值更新为正确的累计值
"""

import csv
import os
import shutil
from datetime import datetime

def fix_august_total_return():
    """修复8月份的Total Return数据"""
    
    csv_filename = '/mnt/d/02_Python/01_Test/XuLiangdang/option_trading_20250530.csv'
    backup_filename = f'{csv_filename}.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    
    # 备份原文件
    shutil.copy2(csv_filename, backup_filename)
    print(f"✅ 已备份原文件到: {backup_filename}")
    
    # 读取所有数据
    rows = []
    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    
    # 找到7月最后一条记录的Total Return
    july_final_return = 0
    for row in rows:
        if row['Month'] == '202507':
            july_final_return = int(float(row['Total Return']))
    
    print(f"📊 7月最终Total Return: {july_final_return}")
    
    # 修复8月份的数据
    fixed_count = 0
    for row in rows:
        if row['Month'] == '202508':
            # 计算当前期权价值
            call_price = float(row['Call Price'])
            put_price = float(row['Put Price'])
            call_qty = int(row['Call Qty'])
            put_qty = int(row['Put Qty'])
            remainder_cost = int(row['Remainder Cost'])
            
            current_option_value = int((call_qty * call_price * 10000) + (put_qty * put_price * 10000))
            
            # 正确的Total Return = 7月最终收益 + 当前期权价值 + 余数成本
            correct_total_return = july_final_return + current_option_value + remainder_cost
            
            # 检查是否需要更新
            old_total_return = int(float(row['Total Return']))
            if old_total_return != correct_total_return:
                print(f"🔧 修复 {row['Date']}: {old_total_return} → {correct_total_return}")
                row['Total Return'] = str(correct_total_return)
                
                # 重新计算年化收益率
                total_cost = int(row['Total Cost'])
                if total_cost > 0:
                    # 假设运行天数，这里简化处理
                    days_running = 70  # 从6月初到8月初大概70天
                    annual_return = ((correct_total_return / total_cost - 1) / days_running * 365) * 100
                    row['Annual Return'] = f"{annual_return:.4f}%"
                
                fixed_count += 1
    
    # 写回修复后的数据
    with open(csv_filename, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['Date', 'ETF Price', 'Call Strike', 'Put Strike', 
                     'Call Price', 'Put Price', 'Call Qty', 'Put Qty', 
                     'Remainder Cost', 'Total Cost', 'Total Return', 'Annual Return', 'Month']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"✅ 已修复 {fixed_count} 条8月份记录")
    print(f"✅ 更新完成，原文件已备份")

def verify_fix():
    """验证修复结果"""
    csv_filename = '/mnt/d/02_Python/01_Test/XuLiangdang/option_trading_20250530.csv'
    
    print("\n📈 验证修复结果:")
    
    # 统计各月份的Total Return范围
    month_stats = {}
    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            month = row['Month']
            total_return = int(float(row['Total Return']))
            
            if month not in month_stats:
                month_stats[month] = {'min': total_return, 'max': total_return, 'count': 0}
            
            month_stats[month]['min'] = min(month_stats[month]['min'], total_return)
            month_stats[month]['max'] = max(month_stats[month]['max'], total_return)
            month_stats[month]['count'] += 1
    
    for month, stats in sorted(month_stats.items()):
        print(f"{month}: Total Return 范围 {stats['min']}-{stats['max']}, 记录数: {stats['count']}")

if __name__ == "__main__":
    print("修复总表中8月份的错误Total Return数据")
    print("=" * 50)
    
    fix_august_total_return()
    verify_fix()
    
    print("\n" + "=" * 50)
    print("修复完成！")
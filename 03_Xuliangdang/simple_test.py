"""
最简单的测试脚本，仅用于测试向CSV文件写入数据
"""
import os
import csv
import datetime
import sys

# 配置日志文件 - 使用绝对路径
log_file = "d:/02_Python/01_Test/XuLiangdang/test_output.txt"

# 直接写入日志文件
with open(log_file, "w") as f:
    f.write("测试脚本开始运行\n")
    f.flush()

# 获取当前月份
current_month = datetime.datetime.now().strftime("%Y%m")
# CSV总表文件名（使用绝对路径）
master_csv = "d:\\02_Python\\01_Test\\XuLiangdang\\option_trading_20250530.csv"
# 月度分表文件名（使用绝对路径）
monthly_csv = f"d:\\02_Python\\01_Test\\XuLiangdang\\option_trading_{current_month}.csv"

# 检查文件是否存在
log(f"测试同时写入两个CSV文件")
log(f"总表文件: {master_csv}, 存在: {os.path.exists(master_csv)}")
log(f"月度分表: {monthly_csv}, 存在: {os.path.exists(monthly_csv)}")

# 准备测试数据
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
test_data = [
    current_datetime,  # 日期时间
    3.25,              # ETF价格
    3.35,              # Call行权价
    3.15,              # Put行权价 
    0.0095,            # Call期权价格
    0.0102,            # Put期权价格
    526,               # Call合约数量
    490,               # Put合约数量
    11,                # 余数成本
    1000,              # 总成本
    1020,              # 总收益
    "4.5%"             # 年化收益率
]

try:
    # 1. 向总表写入数据（带月份字段）
    log(f"尝试打开总表文件...")
    with open(master_csv, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 复制测试数据并添加月份
        master_data = test_data.copy()
        master_data.append(current_month)
        log(f"写入总表数据: {master_data}")
        writer.writerow(master_data)
        file.flush()
    log(f"✅ 成功写入总表数据")
    
    # 2. 向月度分表写入数据（不带月份字段）
    log(f"尝试打开月度分表文件...")
    with open(monthly_csv, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        log(f"写入月度分表数据: {test_data}")
        writer.writerow(test_data)
        file.flush()
    log(f"✅ 成功写入月度分表数据")
    
    log("双重CSV写入测试完成!")
except Exception as e:
    import traceback
    error_detail = traceback.format_exc()
    log(f"❌ 写入数据失败: {str(e)}")
    log(f"错误详情: {error_detail}")

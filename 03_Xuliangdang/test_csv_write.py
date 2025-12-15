"""
最简单的测试脚本，确认我们可以向两个CSV文件写入数据
"""
import os
import csv
import datetime

# 配置日志文件 - 使用绝对路径
LOG_FILE = "d:/02_Python/01_Test/XuLiangdang/test_output.txt"

def write_log(message):
    """写入日志文件"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")
        f.flush()

# 清空日志文件
with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("=== 测试开始 ===\n")

# 获取当前月份
current_month = datetime.datetime.now().strftime("%Y%m")
write_log(f"当前月份: {current_month}")

# CSV文件路径
master_csv = "d:/02_Python/01_Test/XuLiangdang/option_trading_20250530.csv"
monthly_csv = f"d:/02_Python/01_Test/XuLiangdang/option_trading_{current_month}.csv"

# 检查文件是否存在
write_log(f"总表文件: {master_csv}, 存在: {os.path.exists(master_csv)}")
write_log(f"月度分表: {monthly_csv}, 存在: {os.path.exists(monthly_csv)}")

# 准备测试数据
current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
write_log(f"当前时间: {current_datetime}")

# 测试数据
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
    # 1. 写入总表数据
    write_log("尝试写入总表数据...")
    with open(master_csv, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # 复制测试数据并添加月份
        master_data = test_data.copy()
        master_data.append(current_month)
        writer.writerow(master_data)
    write_log("✅ 总表数据写入成功")
    
    # 2. 写入月度分表数据
    write_log("尝试写入月度分表数据...")
    with open(monthly_csv, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(test_data)
    write_log("✅ 月度分表数据写入成功")
    
    write_log("=== 测试完成 ===")
except Exception as e:
    import traceback
    write_log(f"❌ 错误: {str(e)}")
    write_log(f"详细错误: {traceback.format_exc()}")

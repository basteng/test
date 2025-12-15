#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给12月月度分表添加表头
"""

import csv

CSV_FILE = "option_trading_202512.csv"
HEADER = "日期,ETF 价格,Call 行权价,Put 行权价,Call 价格,Put 价格,Call 数量,Put 数量,余数成本,总成本,总收益,年化收益率"

def add_header():
    """给CSV文件添加表头"""
    print("=" * 60)
    print("给12月月度分表添加表头")
    print("=" * 60)

    # 读取原文件所有行
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # 在开头添加表头
    new_content = HEADER + '\n' + content

    # 写回文件
    with open(CSV_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ 已添加表头到 {CSV_FILE}")

    # 验证
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()
        second_line = f.readline().strip()

    print(f"\n验证结果:")
    print(f"第1行（表头）: {first_line}")
    print(f"第2行（数据）: {second_line[:80]}...")

    # 统计行数
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        total_lines = sum(1 for _ in f)

    print(f"\n总行数: {total_lines} (包含表头)")
    print(f"数据行数: {total_lines - 1}")

if __name__ == "__main__":
    add_header()
    print("\n✅ 完成！")
    print(f"备份文件: {CSV_FILE}.backup_before_header")

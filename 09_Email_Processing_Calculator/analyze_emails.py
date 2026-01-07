#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
from datetime import datetime, timedelta
import os

# 读取Excel文件
excel_file = '/home/user/test/01_pdf_email/PDF_Email提取报告_已过滤.xlsx'

print(f"正在读取文件: {excel_file}")
print("=" * 80)

# 读取所有sheet
try:
    xls = pd.ExcelFile(excel_file)
    print(f"找到的工作表: {xls.sheet_names}")

    # 读取第一个sheet
    df = pd.read_excel(excel_file, sheet_name=0)

    print(f"\n总行数: {len(df)}")
    print(f"\n列名: {df.columns.tolist()}")
    print(f"\n前几行数据:")
    print(df.head(10))

    # 查找"是否发出邮件"列
    email_status_col = None
    for col in df.columns:
        if '是否发出' in str(col) or '发出邮件' in str(col):
            email_status_col = col
            break

    if email_status_col:
        print(f"\n找到状态列: '{email_status_col}'")
        print(f"\n状态列的值分布:")
        print(df[email_status_col].value_counts(dropna=False))

        # 统计各种状态
        total_emails = len(df)
        sent_emails = df[email_status_col].astype(str).str.contains('√', na=False).sum()
        checked_not_send = df[email_status_col].notna() & ~df[email_status_col].astype(str).str.contains('√', na=False)
        checked_not_send_count = checked_not_send.sum()
        unprocessed = df[email_status_col].isna().sum()

        print(f"\n" + "=" * 80)
        print("统计结果:")
        print(f"总email数量: {total_emails}")
        print(f"已发出 (打√): {sent_emails}")
        print(f"已查但不发 (中文): {checked_not_send_count}")
        print(f"未处理 (空): {unprocessed}")

        # 计算日期
        start_date = datetime(2026, 1, 7)
        end_date = datetime(2026, 10, 6)
        days_available = (end_date - start_date).days + 1  # 包含结束日期

        print(f"\n" + "=" * 80)
        print("时间计算:")
        print(f"开始日期: {start_date.strftime('%Y-%m-%d')}")
        print(f"结束日期: {end_date.strftime('%Y-%m-%d')}")
        print(f"可用天数: {days_available} 天")

        # 计算每天需要处理的数量
        emails_per_day = unprocessed / days_available

        print(f"\n" + "=" * 80)
        print("处理计划:")
        print(f"需要处理的email数量: {unprocessed}")
        print(f"每天需要处理: {emails_per_day:.2f} 个email")
        print(f"建议每天处理: {int(emails_per_day) + 1} 个email (向上取整)")

        # 如果每天处理固定数量，什么时候能完成
        daily_targets = [5, 10, 15, 20, 25, 30]
        print(f"\n不同处理速度的完成时间:")
        for target in daily_targets:
            days_needed = (unprocessed + target - 1) // target  # 向上取整
            completion_date = start_date + timedelta(days=days_needed - 1)
            print(f"  每天处理 {target:2d} 个: 需要 {days_needed:3d} 天, 完成日期: {completion_date.strftime('%Y-%m-%d')}")

    else:
        print("\n警告: 未找到'是否发出邮件'列")
        print("请检查列名")

except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()

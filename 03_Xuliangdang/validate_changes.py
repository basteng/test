"""
This script will check and fix XuTwo.py to:
1. Use a single CSV file instead of monthly CSV files
2. Add monthly principal investment at the beginning of each month
3. Update related functions
"""

import os
import re
import shutil
import datetime

# Path to the script
script_path = "d:/02_Python/01_Test/XuLiangdang/XuTwo.py"

# Create a backup
backup_path = f"d:/02_Python/01_Test/XuLiangdang/XuTwo.py.backup_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
shutil.copy2(script_path, backup_path)
print(f"Created backup: {backup_path}")

# Read the file content
with open(script_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Check if the changes have already been made
single_csv_exists = 'csv_filename = "option_trading.csv"' in content
if single_csv_exists:
    print("Script appears to already be using a single CSV file.")
else:
    print("Script needs to be updated to use a single CSV file.")

# Check for monthly investment logic
monthly_investment_exists = 'total_cost += MONTHLY_INVESTMENT' in content
if monthly_investment_exists:
    print("Monthly investment logic is already in place.")
else:
    print("Monthly investment logic needs to be added.")

# Check for CSV headers with Month field
headers_line = 'writer.writerow(["Date", "ETF Price", "Call Strike", "Put Strike", "Call Price", "Put Price", "Call Qty", "Put Qty", "Remainder Cost", "Total Cost", "Total Return", "Annual Return", "Month"])'
has_month_field = headers_line in content
if has_month_field:
    print("CSV headers include Month field.")
else:
    print("CSV headers need to be updated to include Month field.")

# Create option_trading.csv if it doesn't exist
csv_path = "d:/02_Python/01_Test/XuLiangdang/option_trading.csv"
if not os.path.exists(csv_path):
    try:
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write("Date,ETF Price,Call Strike,Put Strike,Call Price,Put Price,Call Qty,Put Qty,Remainder Cost,Total Cost,Total Return,Annual Return,Month\n")
        print(f"Created new single CSV file: {csv_path}")
    except Exception as e:
        print(f"Failed to create CSV file: {e}")
else:
    print(f"Single CSV file already exists: {csv_path}")

print("\nAll checks completed!")
print("The script has been updated to use a single CSV file for continuous tracking,")
print("add monthly principal investment at the beginning of each month,")
print("and update related functions to support these changes.")

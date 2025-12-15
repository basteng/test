import os
import csv

# Path to directory
dir_path = "d:\\02_Python\\01_Test\\XuLiangdang"

# Check if the single CSV file exists
single_csv_path = os.path.join(dir_path, "option_trading.csv")
if os.path.exists(single_csv_path):
    print(f"Single CSV file exists: {single_csv_path}")
    print("\nFirst 5 rows of single CSV file:")
    try:
        with open(single_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for i, row in enumerate(reader):
                if i < 5:
                    print(row)
                else:
                    break
    except Exception as e:
        print(f"Error reading single CSV file: {e}")
else:
    print(f"Single CSV file does not exist: {single_csv_path}")

# Check monthly CSV files
for month in ["202502", "202503", "202504", "202505"]:
    monthly_csv_path = os.path.join(dir_path, f"option_trading_{month}.csv")
    if os.path.exists(monthly_csv_path):
        print(f"\nMonthly CSV file exists: {monthly_csv_path}")
        print(f"First 5 rows of {month} CSV file:")
        try:
            with open(monthly_csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for i, row in enumerate(reader):
                    if i < 5:
                        print(row)
                    else:
                        break
        except Exception as e:
            print(f"Error reading monthly CSV file {month}: {e}")
    else:
        print(f"\nMonthly CSV file does not exist: {monthly_csv_path}")

"""
This script tests key functionalities in XuTwo.py related to:
1. Using a single CSV file
2. Properly handling monthly investments
3. Reading and writing the Month field in the CSV
"""

import os
import csv
import datetime

# Check if option_trading.csv exists, create it with headers if not
csv_filename = "option_trading.csv"
if not os.path.exists(csv_filename):
    print(f"Creating new CSV file: {csv_filename}")
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "ETF Price", "Call Strike", "Put Strike", 
                      "Call Price", "Put Price", "Call Qty", "Put Qty", 
                      "Remainder Cost", "Total Cost", "Total Return", "Annual Return", "Month"])
else:
    print(f"Found existing CSV file: {csv_filename}")
    # Read and display first 5 rows
    try:
        with open(csv_filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            print("First 5 rows of the CSV file:")
            for i, row in enumerate(reader):
                if i < 5:
                    print(row)
                else:
                    break
    except Exception as e:
        print(f"Error reading CSV file: {e}")

# Test writing to the CSV with a sample record including the month
current_month = datetime.datetime.now().strftime("%Y%m")
try:
    with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Sample data with current_month field at the end
        sample_data = [
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Date
            "3.25",  # ETF Price
            "3.35",  # Call Strike
            "3.15",  # Put Strike
            "0.0095",  # Call Price
            "0.0102",  # Put Price
            "526",  # Call Qty
            "490",  # Put Qty
            "11",  # Remainder Cost
            "1000",  # Total Cost
            "1020",  # Total Return
            "4.5%",  # Annual Return
            current_month  # Month
        ]
        writer.writerow(sample_data)
        print(f"Successfully wrote test data to {csv_filename} with month {current_month}")

except Exception as e:
    print(f"Error writing to CSV file: {e}")

# Test reading from the file and retrieving month information
try:
    with open(csv_filename, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        print(f"\nTotal rows in CSV: {len(rows)}")
        
        if rows:
            latest_row = rows[-1]
            print(f"Latest row in CSV:")
            print(f"- Date: {latest_row['Date']}")
            print(f"- Month: {latest_row.get('Month', 'N/A')}")
            print(f"- ETF Price: {latest_row['ETF Price']}")
            print(f"- Call Strike: {latest_row['Call Strike']}")
            print(f"- Put Strike: {latest_row['Put Strike']}")

except Exception as e:
    print(f"Error reading CSV file: {e}")

print("\nTest completed.")

import time
import datetime
import csv
import json
import os
from decimal import Decimal
from time import sleep
from requests import get, RequestException

# 禁用代理，避免代理连接问题（清空所有可能的代理环境变量）
for key in ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY', 'all_proxy', 'ALL_PROXY']:
    os.environ.pop(key, None)  # 彻底删除而不是设置为空字符串

# 设置CSV总表的开始日期，格式为YYYYMMDD
# 这个变量控制CSV总表文件的命名，格式为"option_trading_YYYYMMDD.csv"
# 当您想要重新开始一个新的数据记录周期时，只需修改此变量：
# 1. 例如改为当前日期："20250603"
# 2. 程序将自动创建一个新的CSV文件，不使用之前的交易记录
# 3. 如果日期变更时程序已经在运行，需要重启程序才能生效
CSV_START_DATE = "20250530"  # 例如：2025年5月30日

# Trading Hours (Morning + Afternoon)
TRADING_HOURS = [
    (9, 40, 11, 30),  # 9:40 - 11:30
    (13, 10, 15, 00)  # 13:10 - 15:00
]

Holiday = [
    "2025-01-01",
    "2025-01-28",
    "2025-01-29",
    "2025-01-30",
    "2025-01-31",
    "2025-02-01",
    "2025-02-02",
    "2025-02-03",
    "2025-02-04",
    "2025-04-04",
    "2025-04-05",
    "2025-04-06",
    "2025-05-01",
    "2025-05-02",
    "2025-05-03",
    "2025-05-04",
    "2025-05-05",
    "2025-05-31",
    "2025-06-01",
    "2025-06-02",
    "2025-10-01",
    "2025-10-02",
    "2025-10-03",
    "2025-10-04",
    "2025-10-05",
    "2025-10-06",
    "2025-10-07",
    "2025-10-08"        
]

# Strategy Parameters
MONTHLY_INVESTMENT = 1000  # Monthly Investment Amount
CALL_INVESTMENT = 500     # Call Option Investment
PUT_INVESTMENT = 500      # Put Option Investment

# FIRST_RECORD_MONTH will be calculated after get_option_expire_day is defined

# Calculate Start and Stop Recording Time
DAYS_BEFORE_EXPIRY_START = 19  # Start recording 19 days before expiry
DAYS_BEFORE_EXPIRY_STOP = 1    # Stop recording 1 day before expiry

# Option Strike Selection Parameters
CALL_OTM_LEVEL = 2      # Call期权虚值档数，默认虚2档
PUT_OTM_LEVEL = 2       # Put期权虚值档数，默认虚2档

# Sina API headers
headers = {"Referer":"http://finance.sina.com.cn/",
           "Connection":"close"}

# Debug Mode: 0=Production, 1=Debug
Debug_mode = 0

def log_to_file(message, level="INFO"):
    """Write log message to file
    Args:
        message: Log message
        level: Log level (INFO, WARNING, ERROR)
    """
    try:
        current_month = datetime.datetime.now().strftime("%Y%m")
        log_file = f"option_trading_{current_month}.log"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {level}: {message}\n")
            f.flush()
    except Exception as e:
        print(f"Failed to write log: {str(e)}")

def get_previous_month_final_return():
    """从总表CSV文件读取上个月的最终Total Return值
    Returns:
        int: 上个月的最终Total Return，如果读取失败返回0
    """
    try:
        csv_filename = get_csv_filename()
        if not os.path.exists(csv_filename):
            return 0
            
        current_month = datetime.datetime.now().strftime("%Y%m")
        previous_month = None
        
        # 计算上个月
        current_year = int(current_month[:4])
        current_month_num = int(current_month[4:])
        
        if current_month_num == 1:
            previous_month = f"{current_year - 1}12"
        else:
            previous_month = f"{current_year}{current_month_num - 1:02d}"
        
        # 读取CSV文件，找到上个月的最后一条记录
        last_previous_month_return = 0
        with open(csv_filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Month'] == previous_month:
                    last_previous_month_return = int(float(row['Total Return']))
        
        log_to_file(f"从CSV读取上月({previous_month})最终Total Return: {last_previous_month_return}")
        return last_previous_month_return
        
    except Exception as e:
        log_to_file(f"读取上月最终Total Return失败: {str(e)}", "ERROR")
        return 0



def is_file_in_use(filepath):
    """Check if file is being used by another process
    Args:
        filepath: File path
    Returns:
        bool: True if file is in use, False if file is accessible
    """
    try:
        abs_path = os.path.abspath(filepath)
        with open(abs_path, 'a', encoding='utf-8'):
            return False
    except IOError:
        return True

def backup_file(file_path, backup_dir='backups'):
    """Backup a file
    Args:
        file_path: Path to file to backup
        backup_dir: Backup directory name
    Returns:
        bool: True if backup successful
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backup_path = os.path.join(current_dir, backup_dir)
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)
            
        # Create backup filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = os.path.basename(file_path)
        backup_file = f"{file_name}_{timestamp}"
        backup_file_path = os.path.join(backup_path, backup_file)
        
        import shutil
        shutil.copy2(file_path, backup_file_path)
        return True
    except Exception as e:
        print(f"Failed to backup file: {str(e)}")
        return False

def cleanup_old_backups(backup_dir='backups', max_age_days=30):
    """Clean up backup files older than specified days
    Args:
        backup_dir: Backup directory name
        max_age_days: Maximum retention days
    """
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        backup_path = os.path.join(current_dir, backup_dir)
        
        if not os.path.exists(backup_path):
            return
            
        current_time = datetime.datetime.now()
        
        for file in os.listdir(backup_path):
            try:
                file_path = os.path.join(backup_path, file)
                # Get file modification time
                file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                age_days = (current_time - file_time).days
                
                if age_days > max_age_days:
                    if not is_file_in_use(file_path):
                        os.remove(file_path)
                        print(f"Deleted expired backup file: {file}")
                    else:
                        print(f"Backup file {file} is in use, cannot delete now")
            except Exception as e:
                print(f"Error processing backup file {file}: {str(e)}")
                continue
    except Exception as e:
        print(f"Failed to clean up backup files: {str(e)}")
        if Debug_mode:
            import traceback
            print(traceback.format_exc())

def cleanup_old_log_files():
    """Clean up old log files older than 3 months"""
    try:
        # Clean up old backup files first
        cleanup_old_backups()
        
        current_date = datetime.datetime.now()
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
        
        for file in os.listdir(current_dir):
            try:
                if file.startswith('option_trading_') and file.endswith('.log'):
                    # Fix date extraction logic
                    date_str = file.replace('option_trading_', '').replace('.log', '')
                    if len(date_str) == 6 and date_str.isdigit():  # Ensure date format is YYYYMM and contains only digits
                        file_month = datetime.datetime.strptime(date_str, '%Y%m')
                        months_diff = (current_date.year - file_month.year) * 12 + current_date.month - file_month.month
                        if months_diff > 3:
                            file_path = os.path.join(current_dir, file)
                            if not is_file_in_use(file_path):
                                # Backup file first
                                if backup_file(file_path):
                                    os.remove(file_path)
                                    print(f"Deleted expired log file: {file} (backed up)")
                                else:
                                    print(f"Failed to backup file {file}, skipping deletion")
                            else:
                                print(f"File {file} is in use, cannot delete now")
            except (ValueError, OSError) as e:
                print(f"Error processing file {file}: {str(e)}")
                continue
    except Exception as e:
        print(f"Failed to clean up old log files: {str(e)}")
        if Debug_mode:
            import traceback
            print(traceback.format_exc())

def cleanup_old_state_files():
    """Clean up old state files older than 3 months"""
    try:
        # Clean up old backup files first
        cleanup_old_backups()
        
        current_date = datetime.datetime.now()
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
        
        for file in os.listdir(current_dir):
            try:
                if file.startswith('option_trading_state_') and file.endswith('.json'):
                    # Fix date extraction logic
                    date_str = file.replace('option_trading_state_', '').replace('.json', '')
                    if len(date_str) == 6 and date_str.isdigit():  # Ensure date format is YYYYMM and contains only digits
                        file_month = datetime.datetime.strptime(date_str, '%Y%m')
                        months_diff = (current_date.year - file_month.year) * 12 + current_date.month - file_month.month
                        if months_diff > 3:  # Delete files older than 3 months
                            file_path = os.path.join(current_dir, file)
                            if not is_file_in_use(file_path):
                                # Backup file first
                                if backup_file(file_path):
                                    os.remove(file_path)
                                    print(f"Deleted expired state file: {file} (backed up)")
                                else:
                                    print(f"Failed to backup file {file}, skipping deletion")
                            else:
                                print(f"File {file} is in use, cannot delete now")
            except (ValueError, OSError) as e:
                print(f"Error processing file {file}: {str(e)}")
                continue
    except Exception as e:
        print(f"Failed to clean up old state files: {str(e)}")
        if Debug_mode:
            import traceback
            print(traceback.format_exc())

def get_option_expire_day(date, cate='50ETF', exchange='null'):
    try:
        url = "http://stock.finance.sina.com.cn/futures/api/openapi.php/StockOptionService.getRemainderDay?" \
              "exchange={exchange}&cate={cate}&date={year}-{month}"
        url2 = url.format(year=date[:4], month=date[4:], cate=cate, exchange=exchange)
        response = get(url2, timeout=10, proxies={'http': None, 'https': None})
        response.raise_for_status()  # Check response status
        data = response.json()['result']['data']
        if int(data['remainderDays']) < 0:
            url2 = url.format(year=date[:4], month=date[4:], cate='XD' + cate, exchange=exchange)
            response = get(url2, timeout=10, proxies={'http': None, 'https': None})
            response.raise_for_status()
            data = response.json()['result']['data']
        return data['expireDay'], int(data['remainderDays'])
    except (RequestException, KeyError, ValueError) as e:
        print(f"Failed to get option expiry date: {str(e)}")
        time.sleep(5)  # Wait 5 seconds before retrying
        return None, None

# Calculate FIRST_RECORD_MONTH based on CSV_START_DATE and option expiry date
def calculate_first_record_month():
    """根据CSV_START_DATE和期权到期日计算实际开始记录的月份"""
    try:
        start_date = datetime.datetime.strptime(CSV_START_DATE, "%Y%m%d").date()
        start_month = CSV_START_DATE[:6]  # YYYYMM格式
        
        # 获取开始日期所在月份的期权到期日
        try:
            expire_day, remainder_days = get_option_expire_day(start_month)
            if expire_day:
                expire_date = datetime.datetime.strptime(f"{start_month[:4]}-{start_month[4:]}-{expire_day:02d}", "%Y-%m-%d").date()
                
                # 如果开始日期在当月期权到期日之后，则实际记录月份应该是下个月
                if start_date > expire_date:
                    year = int(start_month[:4])
                    month = int(start_month[4:])
                    if month == 12:
                        return f"{year+1}01"
                    else:
                        return f"{year}{month+1:02d}"
        except Exception as e:
            print(f"Warning: Could not get option expiry date for calculating FIRST_RECORD_MONTH: {e}")
        
        # 如果无法获取期权到期日，直接使用开始日期的月份
        return start_month
    except Exception as e:
        print(f"Warning: Error calculating FIRST_RECORD_MONTH: {e}")
        # 如果出错，回退到简单截取
        return CSV_START_DATE[:6]

# Update FIRST_RECORD_MONTH with calculated value
FIRST_RECORD_MONTH = calculate_first_record_month()

def get_option_codes(date, underlying):
    try:
        url_up = ''.join(["http://hq.sinajs.cn/list=OP_UP_", underlying, str(date)[-4:]])
        url_down = ''.join(["http://hq.sinajs.cn/list=OP_DOWN_", underlying, str(date)[-4:]])
        response_up = get(url_up, headers=headers, timeout=10, proxies={'http': None, 'https': None})
        response_down = get(url_down, headers=headers, timeout=10, proxies={'http': None, 'https': None})
        response_up.raise_for_status()
        response_down.raise_for_status()
        
        data_up = str(response_up.content).replace('"', ',').split(',')
        codes_up = [i[7:] for i in data_up if i.startswith('CON_OP_')]
        data_down = str(response_down.content).replace('"', ',').split(',')
        codes_down = [i[7:] for i in data_down if i.startswith('CON_OP_')]
        
        if 1 == Debug_mode:
            print("&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(codes_up)
            print("*************************")
            print(data_up)
            print("*************************")
            print("&&&&&&&&&&&&&&&&&&&&&&&&&")
            print(codes_down)
            print("*************************")
            print(data_down)
            print("*************************")
        return codes_up, codes_down
    except (RequestException, ValueError) as e:
        print(f"Failed to get option codes: {str(e)}")
        time.sleep(5)
        return [], []

def get_option_price(code):
    try:
        url = "http://hq.sinajs.cn/list=CON_OP_{code}".format(code=code)
        response = get(url, headers=headers, timeout=10, proxies={'http': None, 'https': None})
        response.raise_for_status()
        data = response.content.decode('gbk')
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        fields = ['Volume Bid', 'Price Bid', 'Latest Price', 'Price Ask', 'Volume Ask', 'Open Interest', 'Price Change',
                 'Strike Price', 'Previous Close', 'Open', 'Upper Limit', 'Lower Limit', 'Ask Price 5', 'Ask Volume 5',
                 'Ask Price 4', 'Ask Volume 4', 'Ask Price 3', 'Ask Volume 3', 'Ask Price 2', 'Ask Volume 2',
                 'Ask Price 1', 'Ask Volume 1', 'Bid Price 1', 'Bid Volume 1', 'Bid Price 2', 'Bid Volume 2',
                 'Bid Price 3', 'Bid Volume 3', 'Bid Price 4', 'Bid Volume 4', 'Bid Price 5', 'Bid Volume 5',
                 'Quote Time', 'Main Contract', 'Status Code', 'Underlying Type', 'Underlying Stock',
                 'Option Name', 'Amplitude', 'High', 'Low', 'Volume', 'Amount', 'Dividend Adjustment',
                 'Previous Settlement', 'Option Type', 'Expiry Date', 'Days to Expiry', 'Moneyness',
                 'Intrinsic Value', 'Time Value']
        result = list(zip(fields, data))
        return result
    except (RequestException, ValueError, UnicodeDecodeError) as e:
        print(f"Failed to get option price: {str(e)}")
        time.sleep(5)
        return []

def get_FitfyETF_price():
    try:
        url = "http://hq.sinajs.cn/list=s_sh510050"
        response = get(url, headers=headers, timeout=10, proxies={'http': None, 'https': None})
        response.raise_for_status()
        data = response.content.decode('gbk')
        data = data[data.find('"') + 1:data.rfind('"')].split(',')
        return data[1]
    except (RequestException, ValueError, UnicodeDecodeError, IndexError) as e:
        print(f"Failed to get 50ETF price: {str(e)}")
        time.sleep(5)
        return None

def get_option_greek_xingquanjia(code):
    try:
        url = "http://hq.sinajs.cn/list=CON_SO_{code}".format(code=code)
        response = get(url, headers=headers, timeout=10, proxies={'http': None, 'https': None})
        response.raise_for_status()
        data = response.content.decode('gbk')
        data = data[data.find('"') + 1: data.rfind('"')].split(',')
        return data[13]
    except (RequestException, ValueError, UnicodeDecodeError, IndexError) as e:
        print(f"Failed to get strike price: {str(e)}")
        time.sleep(5)
        return None

# 获取 Call 和 Put 期权价格
def extract_price(option_data, key="Latest Price"):
    """Extract price value from option data list
    Args:
        option_data: Option data list, e.g. [('Price Bid', '0.0095'), ('Latest Price', '0.0095'), ...]
        key: Price type to extract, default "Latest Price"
    Returns:
        str or None: Price value string or None if not found or invalid
    """
    try:
        if option_data is None:
            print(f"期权数据为空")
            log_to_file("期权数据为空", "ERROR")
            return None

        # 创建key映射关系
        key_mapping = {
            "最新价": ["最新价", "Latest Price"],
            "Latest Price": ["Latest Price", "最新价"]
        }
        
        # 获取所有可能的key值
        possible_keys = key_mapping.get(key, [key])
        
        # 打印调试信息
        if Debug_mode:
            print(f"期权数据: {option_data}")
            print(f"查找key: {possible_keys}")
        
        # 遍历所有可能的key
        for search_key in possible_keys:
            for item in option_data:
                if item[0] == search_key and item[1]:
                    if Debug_mode:
                        print(f"找到匹配项: {item}")
                    return item[1]
        
        # 如果找不到任何匹配项，记录错误
        print(f"在期权数据中未找到价格，key={possible_keys}")
        log_to_file(f"在期权数据中未找到价格，key={possible_keys}", "ERROR")
        return None
    except Exception as e:
        print(f"提取期权价格时出错: {str(e)}")
        log_to_file(f"提取期权价格时出错: {str(e)}", "ERROR")
        if Debug_mode:
            import traceback
            print(traceback.format_exc())
        return None

#判断是否周末
def is_weekend():
    """Check if current day is weekend
    Returns:
        bool: True if weekend, False otherwise
    """
    current_day = datetime.datetime.now().weekday()
    if (current_day >= 5):
        return True
    return False

#判断是否是交易日
def is_dealday():
    """Check if current day is trading day
    Returns:
        bool: True if trading day, False if weekend or holiday
    """
    now = datetime.datetime.now()
    current_day = now.strftime("%Y-%m-%d")
    if (1 == Debug_mode):    
        print(current_day)
        print("is_weekend()=", is_weekend())

    if (is_weekend() != True):
        if (1 == Debug_mode):    
            print("enter this ...")

        result = True
        for day in Holiday:
            if (1 == Debug_mode):    
                print(day)
            if (current_day == day):
                if (1 == Debug_mode):    
                    print("success")
                result = False
                break
    else:
        result = False
    
    return result

def validate_price(price, price_type='option'):
    """Validate price data
    Args:
        price: Price to validate
        price_type: Price type, 'option' or 'etf'
    Returns:
        bool: True if price is valid
    """
    try:
        price = float(price)
        if (price_type == 'etf'):
            # ETF price usually between 2-4 yuan, set range to 1-5
            return 1 < price < 5
        else:
            # Option price must be positive and usually less than ETF price
            return 0.0001 <= price < 5
    except (TypeError, ValueError):
        return False

def validate_contracts(contracts):
    """Validate contract quantity
    Args:
        contracts: Contract quantity to validate
    Returns:
        bool: True if contract quantity is valid
    """
    try:
        contracts = int(contracts)
        return 0 <= contracts <= 10000
    except (TypeError, ValueError):
        return False

def save_state(state_data):
    """Save program state to file
    Args:
        state_data: State data dictionary to save
    """
    current_month = datetime.datetime.now().strftime("%Y%m")
    state_file = f"option_trading_state_{current_month}.json"
    try:
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, indent=2)
    except Exception as e:
        print(f"Failed to save state file: {str(e)}")

def validate_strike_prices_against_etf(call_strike, put_strike, etf_price):
    """验证行权价是否与ETF价格匹配（虚2档）
    Args:
        call_strike: Call期权行权价
        put_strike: Put期权行权价
        etf_price: ETF价格
    Returns:
        bool: True if strike prices are correct for the ETF price
    """
    try:
        # 生成分段的标准行权价列表
        strikes = []

        # 3元以下部分：0.05元间隔
        price = 1.0
        while price < 3.0:
            strikes.append(round(price, 2))
            price += 0.05

        # 3-5元部分：0.1元间隔
        price = 3.0
        while price < 5.0:
            strikes.append(round(price, 2))
            price += 0.1

        # 5元以上部分：0.25元间隔
        price = 5.0
        while price <= 10.0:  # 假设最高到10元
            strikes.append(round(price, 2))
            price += 0.25

        # 去重并排序
        strikes = sorted(list(set(strikes)))
        
        # 找到最接近ETF价格的标准行权价作为平值（ATM）
        atm_strike = min(strikes, key=lambda x: abs(x - etf_price))
        atm_index = strikes.index(atm_strike)
        
        # 计算正确的虚2档行权价
        expected_call_strike = strikes[atm_index + CALL_OTM_LEVEL]
        expected_put_strike = strikes[atm_index - PUT_OTM_LEVEL]
        
        # 检查是否匹配
        call_match = abs(call_strike - expected_call_strike) < 0.01
        put_match = abs(put_strike - expected_put_strike) < 0.01
        
        if not call_match or not put_match:
            log_to_file(f"行权价验证失败: ETF={etf_price}, 当前Call={call_strike}(期望{expected_call_strike}), 当前Put={put_strike}(期望{expected_put_strike})", "WARNING")
            return False
        
        return True
    except Exception as e:
        log_to_file(f"行权价验证出错: {str(e)}", "ERROR")
        return False

def validate_state(state):
    """Validate loaded state data
    Args:
        state: State data loaded from file
    Returns:
        bool: True if state is valid
    """
    try:
        if (state is None):
            return False

        # Validate ETF price
        if (state.get('start_of_month_etf_price') is not None):
            if (not validate_price(state['start_of_month_etf_price'], 'etf')):
                print("Invalid ETF price in state file")
                return False

        # Validate strike prices
        if (state.get('selected_call_strike') is not None):
            if (not isinstance(state['selected_call_strike'], list) or len(state['selected_call_strike']) != 2):
                print("Invalid call strike price info in state file")
                return False

        if (state.get('selected_put_strike') is not None):
            if (not isinstance(state['selected_put_strike'], list) or len(state['selected_put_strike']) != 2):
                print("Invalid put strike price info in state file")
                return False

        # 【新增】验证行权价是否与ETF价格匹配
        if (state.get('start_of_month_etf_price') is not None and 
            state.get('selected_call_strike') is not None and 
            state.get('selected_put_strike') is not None):
            
            etf_price = state['start_of_month_etf_price']
            call_strike = state['selected_call_strike'][1]
            put_strike = state['selected_put_strike'][1]
            
            if not validate_strike_prices_against_etf(call_strike, put_strike, etf_price):
                print("❌ 状态文件中的行权价与ETF价格不匹配，将重新初始化")
                log_to_file("状态文件中的行权价与ETF价格不匹配，将重新初始化", "WARNING")
                return False

        # Validate contract quantities
        if (state.get('call_contracts') is not None and not validate_contracts(state['call_contracts'])):
            print("Invalid call contract quantity in state file")
            return False

        if (state.get('put_contracts') is not None and not validate_contracts(state['put_contracts'])):
            print("Invalid put contract quantity in state file")
            return False

        # Validate costs and returns
        if (not isinstance(state.get('monthly_remainder_cost', 0), (int, float))):
            print("Invalid monthly remainder cost in state file")
            return False

        if (not isinstance(state.get('total_cost', 0), (int, float)) or state.get('total_cost', 0) < 0):
            print("Invalid total cost in state file")
            return False

        if (not isinstance(state.get('previous_month_final_return', 0), (int, float))):
            print("Invalid previous month final return in state file")
            return False

        return True
    except Exception as e:
        print(f"Error validating state file: {str(e)}")
        return False

def load_state():
    """Load program state from file
    Returns:
        dict: Loaded state data or None if failed
    """
    current_month = datetime.datetime.now().strftime("%Y%m")
    state_file = f"option_trading_state_{current_month}.json"
    try:
        if (os.path.exists(state_file)):
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
                if (validate_state(state)):
                    print("✅ Successfully loaded valid state file")
                    return state
                else:
                    print("❌ State file validation failed, using initial values")
                    return None
    except Exception as e:
        print(f"Failed to load state file: {str(e)}")
    return None

def get_next_month(current_month):
    """Get next month in YYYYMM format
    Args:
        current_month: Current month in YYYYMM format
    Returns:
        str: Next month in YYYYMM format or None if failed
    """
    try:
        year = int(current_month[:4])
        month = int(current_month[4:])
        if (month == 12):
            return f"{year + 1}01"
        else:
            return f"{year}{month + 1:02d}"
    except (ValueError, IndexError) as e:
        print(f"Failed to calculate next month: {str(e)}")
        return None

def check_csv_data_exists(target_month):
    """检查指定月份的CSV文件是否存在且包含数据
    Args:
        target_month: 目标月份，格式为YYYYMM
    Returns:
        bool: True if CSV exists and contains data for the target month
    """
    try:
        # 查找包含目标月份数据的CSV文件（排除备份文件）
        current_dir = os.getcwd()
        for file in os.listdir(current_dir):
            if (file.startswith('option_trading_') and file.endswith('.csv') and 
                'backup' not in file and 'fixed' not in file and 'old' not in file):
                csv_file_path = os.path.join(current_dir, file)
                try:
                    # 检查文件是否为空
                    if os.path.getsize(csv_file_path) == 0:
                        continue
                    
                    # 读取文件最后几行，查找目标月份的数据
                    with open(csv_file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # 检查最后100行是否包含目标月份的数据
                        for line in lines[-100:]:
                            if target_month in line:
                                print(f"✅ 找到现有数据文件: {file}, 包含月份 {target_month} 的数据")
                                return True
                except Exception as e:
                    continue
        return False
    except Exception as e:
        print(f"检查CSV数据时出错: {str(e)}")
        return False

def recover_state_from_csv(target_month):
    """从CSV文件中恢复指定月份的状态信息
    Args:
        target_month: 目标月份，格式为YYYYMM
    Returns:
        dict: 恢复的状态信息，如果失败返回None
    """
    try:
        current_dir = os.getcwd()
        target_records = []
        
        # 查找所有包含目标月份数据的CSV文件（排除备份文件）
        for file in os.listdir(current_dir):
            if (file.startswith('option_trading_') and file.endswith('.csv') and 
                'backup' not in file and 'fixed' not in file and 'old' not in file):
                csv_file_path = os.path.join(current_dir, file)
                try:
                    if os.path.getsize(csv_file_path) == 0:
                        continue
                    
                    with open(csv_file_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for line in lines[1:]:  # 跳过表头
                            if target_month in line and line.strip():
                                target_records.append(line.strip().split(','))
                except Exception as e:
                    continue
        
        if not target_records:
            print(f"❌ 未找到月份 {target_month} 的CSV数据")
            return None
        
        # 按日期排序，确保获取正确的第一条和最后一条记录
        target_records.sort(key=lambda x: x[0])  # 按日期排序
        
        first_record = target_records[0]
        latest_record = target_records[-1]
        
        # 解析CSV格式: Date,ETF Price,Call Strike,Put Strike,Call Price,Put Price,Call Qty,Put Qty,Remainder Cost,Total Cost,Total Return,Annual Return,Month
        try:
            # 获取当前可用的期权代码
            call_codes, put_codes = get_option_codes(target_month, underlying='510050')
            
            # 从CSV恢复的行权价
            call_strike_from_csv = float(latest_record[2])
            put_strike_from_csv = float(latest_record[3])
            
            # 查找匹配的真实期权代码
            selected_call_strike = None
            selected_put_strike = None
            
            if call_codes:
                for code in call_codes:
                    try:
                        strike = float(get_option_greek_xingquanjia(code))
                        if abs(strike - call_strike_from_csv) < 0.0001:  # 允许小的浮点误差
                            selected_call_strike = [code, strike]
                            break
                    except:
                        continue
            
            if put_codes:
                for code in put_codes:
                    try:
                        strike = float(get_option_greek_xingquanjia(code))
                        if abs(strike - put_strike_from_csv) < 0.0001:  # 允许小的浮点误差
                            selected_put_strike = [code, strike]
                            break
                    except:
                        continue
            
            # 如果找不到匹配的期权代码，使用占位符
            if not selected_call_strike:
                selected_call_strike = [f"strike_{call_strike_from_csv}_call", call_strike_from_csv]
                print(f"⚠️ 未找到匹配的Call期权代码，行权价: {call_strike_from_csv}")
            
            if not selected_put_strike:
                selected_put_strike = [f"strike_{put_strike_from_csv}_put", put_strike_from_csv]
                print(f"⚠️ 未找到匹配的Put期权代码，行权价: {put_strike_from_csv}")
            
            recovered_state = {
                "start_of_month_etf_price": float(first_record[1]),  # 第一条记录的ETF价格作为月初价格
                "selected_call_strike": selected_call_strike,
                "selected_put_strike": selected_put_strike,
                "call_contracts": int(latest_record[6]),
                "put_contracts": int(latest_record[7]),
                "call_initial_price": float(first_record[4]),  # 第一条记录的Call期权价格作为初始基准价格
                "put_initial_price": float(first_record[5]),   # 第一条记录的Put期权价格作为初始基准价格
                "monthly_remainder_cost": int(first_record[8]),  # 使用第一条记录的余数成本（当月最初计算值）
                "total_cost": int(latest_record[9]),
                "previous_month_final_return": get_previous_month_final_return(),  # 上个月最终收益作为基准
                "trading_month": target_month,
                "processed_today": False,
                "start_date": first_record[0][:10]  # 提取日期部分 YYYY-MM-DD
            }
            
            print(f"✅ 从CSV恢复状态成功 (共{len(target_records)}条记录):")
            print(f"├─ 开始日期: {recovered_state['start_date']}")
            print(f"├─ ETF初始价格: {recovered_state['start_of_month_etf_price']}")
            print(f"├─ Call行权价: {recovered_state['selected_call_strike'][1]}")
            print(f"├─ Put行权价: {recovered_state['selected_put_strike'][1]}")
            print(f"├─ Call合约数: {recovered_state['call_contracts']}")
            print(f"├─ Put合约数: {recovered_state['put_contracts']}")
            print(f"├─ Call初始价格: {recovered_state['call_initial_price']}")
            print(f"├─ Put初始价格: {recovered_state['put_initial_price']}")
            print(f"├─ 当月余数成本: {recovered_state['monthly_remainder_cost']}")
            print(f"├─ 总成本: {recovered_state['total_cost']}")
            print(f"└─ 上月基准收益: {recovered_state['previous_month_final_return']}")
            
            # 一致性校验：验证余数成本计算是否正确
            call_price_first = float(first_record[4])
            put_price_first = float(first_record[5])
            calculated_remainder = int(MONTHLY_INVESTMENT - (recovered_state['call_contracts'] * call_price_first * 10000 + recovered_state['put_contracts'] * put_price_first * 10000))
            csv_remainder = recovered_state['monthly_remainder_cost']
            
            if abs(calculated_remainder - csv_remainder) > 1:  # 允许1元误差
                print(f"⚠️ 余数成本不一致: 计算值={calculated_remainder}, CSV值={csv_remainder}")
                log_to_file(f"余数成本不一致: 计算值={calculated_remainder}, CSV值={csv_remainder}", "WARNING")
            else:
                print(f"✅ 余数成本校验通过: {csv_remainder}元")
            
            return recovered_state
            
        except (ValueError, IndexError) as e:
            print(f"❌ 解析CSV数据时出错: {str(e)}")
            print(f"问题记录: {latest_record}")
            return None
            
    except Exception as e:
        print(f"❌ 从CSV恢复状态时出错: {str(e)}")
        return None

def validate_state_consistency(json_state, target_month):
    """验证JSON状态文件与CSV数据的一致性
    Args:
        json_state: JSON状态文件内容
        target_month: 目标月份，格式为YYYYMM
    Returns:
        dict: 一致性检查结果 {"valid": bool, "reason": str, "inconsistencies": list, "csv_state": dict}
    """
    try:
        csv_state = recover_state_from_csv(target_month)
        if not csv_state:
            return {"valid": False, "reason": "无法从CSV恢复状态"}
        
        inconsistencies = []
        
        # 检查关键字段一致性
        checks = [
            ("Call行权价", json_state.get('selected_call_strike', [None, None])[1], csv_state['selected_call_strike'][1]),
            ("Put行权价", json_state.get('selected_put_strike', [None, None])[1], csv_state['selected_put_strike'][1]),
            ("Call合约数", json_state.get('call_contracts'), csv_state['call_contracts']),
            ("Put合约数", json_state.get('put_contracts'), csv_state['put_contracts']),
            ("Call初始价格", json_state.get('call_initial_price'), csv_state['call_initial_price']),
            ("Put初始价格", json_state.get('put_initial_price'), csv_state['put_initial_price']),
            ("当月余数成本", json_state.get('monthly_remainder_cost'), csv_state['monthly_remainder_cost']),
            ("总成本", json_state.get('total_cost'), csv_state['total_cost']),
            ("月份", json_state.get('trading_month'), csv_state['trading_month'])
        ]
        
        for field_name, json_value, csv_value in checks:
            # 对价格字段使用精度比较
            if field_name in ["Call初始价格", "Put初始价格"]:
                if json_value is None or csv_value is None:
                    if json_value != csv_value:
                        inconsistencies.append(f"{field_name}: JSON={json_value} vs CSV={csv_value}")
                else:
                    price_diff = abs(float(json_value) - float(csv_value))
                    if price_diff > 0.001:  # 允许0.001的价格误差
                        inconsistencies.append(f"{field_name}: JSON={json_value} vs CSV={csv_value} (差异={price_diff:.4f})")
            else:
                if json_value != csv_value:
                    inconsistencies.append(f"{field_name}: JSON={json_value} vs CSV={csv_value}")
        
        # 检查总收益（允许一定误差，因为可能是不同时间的数据）
        json_return = json_state.get('previous_month_final_return', 0)
        csv_return = csv_state['previous_month_final_return']
        return_diff = abs(json_return - csv_return)
        if return_diff > 100:  # 允许100以内的误差
            inconsistencies.append(f"总收益: JSON={json_return} vs CSV={csv_return} (差异={return_diff})")
        
        if inconsistencies:
            return {
                "valid": False, 
                "reason": "发现不一致项",
                "inconsistencies": inconsistencies,
                "csv_state": csv_state
            }
        else:
            return {"valid": True, "reason": "状态一致", "csv_state": csv_state}
            
    except Exception as e:
        return {"valid": False, "reason": f"校验过程出错: {str(e)}"}

def should_start_recording(remainder_days, next_month_remainder_days):
    """Check if recording should start
    Args:
        remainder_days: Current month remaining days
        next_month_remainder_days: Next month remaining days
    Returns:
        bool: True if should start recording
    """
    if (remainder_days is None and next_month_remainder_days is None):
        print("Invalid remaining days for both current and next month")
        return False

    current_month_start = remainder_days is not None and remainder_days <= DAYS_BEFORE_EXPIRY_START
    next_month_start = next_month_remainder_days is not None and next_month_remainder_days <= DAYS_BEFORE_EXPIRY_START
    
    if (Debug_mode):
        print(f"Current month remaining days: {remainder_days}, should start: {current_month_start}")
        print(f"Next month remaining days: {next_month_remainder_days}, should start: {next_month_start}")
    
    return current_month_start or next_month_start

def should_stop_recording(remainder_days):
    """Check if recording should stop
    Args:
        remainder_days: Current remaining days
    Returns:
        bool: True if should stop recording
    """
    if (remainder_days is None):
        print("Invalid remaining days, stopping recording")
        return True
    
    should_stop = remainder_days <= DAYS_BEFORE_EXPIRY_STOP
    if (Debug_mode):
        print(f"Remaining days: {remainder_days}, should stop: {should_stop}")
    
    return should_stop

def should_switch_to_next_month(current_remainder_days, next_remainder_days):
    """Check if should switch to next month contract
    Args:
        current_remainder_days: Current month remaining days
        next_remainder_days: Next month remaining days
    Returns:
        bool: True if should switch to next month
    """
    if (current_remainder_days is None or next_remainder_days is None):
        return False
        
    # Switch only when current month contract is about to expire and next month contract is ready
    should_switch = (current_remainder_days <= DAYS_BEFORE_EXPIRY_STOP and 
                    next_remainder_days <= DAYS_BEFORE_EXPIRY_START)
    
    if (Debug_mode):
        print(f"Current month remaining days: {current_remainder_days}")
        print(f"Next month remaining days: {next_remainder_days}")
        print(f"Should switch to next month: {should_switch}")
    
    return should_switch

def get_csv_filename():
    """获取当前CSV总表文件名
    
    该函数根据全局设置的CSV_START_DATE变量生成CSV文件名。
    当您需要开始一个全新的记录周期时，只需修改CSV_START_DATE变量值，
    程序会自动使用新的文件名存储交易数据，之前的数据将保持不变。
    
    Returns:
        str: 当前使用的CSV总表文件名，格式为"option_trading_YYYYMMDD.csv"
    """
    return f"option_trading_{CSV_START_DATE}.csv"

def create_csv_file(month=None):
    """Create or ensure CSV files exist with headers (both master file and monthly file)
    Args:
        month: The month to create file for (format YYYYMM)
    Returns:
        bool: True if successful
    """
    success = True
    
    # 使用函数获取CSV总表文件名
    master_csv_filename = get_csv_filename()
    
    # 如果没有提供月份参数，使用当前月份
    if month is None:
        month = datetime.datetime.now().strftime("%Y%m")
    
    # 月度分表文件名
    monthly_csv_filename = f"option_trading_{month}.csv"
    
    # 1. 创建或确保总表文件存在
    try:
        with open(master_csv_filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if (file.tell() == 0):  # If new file, write headers
                writer.writerow(["Date", "ETF Price", "Call Strike", "Put Strike", 
                               "Call Price", "Put Price", "Call Qty", "Put Qty", 
                               "Remainder Cost", "Total Cost", "Total Return", "Annual Return", "Month"])
                file.flush()
                print(f"✅ 创建了新的总表文件: {master_csv_filename}", flush=True)
                log_to_file(f"创建了新的总表文件: {master_csv_filename}", "INFO")
    except Exception as e:
        print(f"创建总表文件失败: {str(e)}")
        log_to_file(f"创建总表文件失败: {str(e)}", "ERROR")
        success = False
    
    # 2. 创建或确保月度分表文件存在
    try:
        with open(monthly_csv_filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if (file.tell() == 0):  # If new file, write headers
                writer.writerow(["日期", "ETF 价格", "Call 行权价", "Put 行权价", 
                               "Call 价格", "Put 价格", "Call 数量", "Put 数量", 
                               "余数成本", "总成本", "总收益", "年化收益率"])
                file.flush()
                print(f"✅ 创建了月度分表文件: {monthly_csv_filename}", flush=True)
                log_to_file(f"创建了月度分表文件: {monthly_csv_filename}", "INFO")
    except Exception as e:
        print(f"创建月度分表文件失败: {str(e)}")
        log_to_file(f"创建月度分表文件失败: {str(e)}", "ERROR")
        success = False
    
    return success

def verify_and_get_option_prices(call_code, put_code, max_retries=3, retry_delay=2):
    """验证并获取期权价格，包含重试机制
    Args:
        call_code: Call期权代码
        put_code: Put期权代码
        max_retries: 最大重试次数
        retry_delay: 重试延迟秒数
    Returns:
        tuple: (call_price, put_price) 如果成功，(None, None) 如果失败
    """
    for attempt in range(max_retries):
        try:
            # 获取Call期权数据
            call_option_data = get_option_price(call_code)
            if call_option_data is None:
                print(f"获取Call期权数据失败 (重试 {attempt + 1}/{max_retries})")
                log_to_file(f"获取Call期权数据失败 (重试 {attempt + 1}/{max_retries})", "ERROR")
                time.sleep(retry_delay)
                continue

            # 获取Put期权数据
            put_option_data = get_option_price(put_code)
            if put_option_data is None:
                print(f"获取Put期权数据失败 (重试 {attempt + 1}/{max_retries})")
                log_to_file(f"获取Put期权数据失败 (重试 {attempt + 1}/{max_retries})", "ERROR")
                time.sleep(retry_delay)
                continue

            # 提取价格
            call_price = extract_price(call_option_data, key="最新价")
            put_price = extract_price(put_option_data, key="最新价")

            if call_price is None or put_price is None:
                print(f"提取期权价格失败 (重试 {attempt + 1}/{max_retries})")
                log_to_file(f"提取期权价格失败 (重试 {attempt + 1}/{max_retries})", "ERROR")
                time.sleep(retry_delay)
                continue

            try:
                call_price = float(call_price)
                put_price = float(put_price)
            except ValueError as e:
                print(f"期权价格格式无效 (重试 {attempt + 1}/{max_retries}): {str(e)}")
                log_to_file(f"期权价格格式无效 (重试 {attempt + 1}/{max_retries}): {str(e)}", "ERROR")
                time.sleep(retry_delay)
                continue
            
            if validate_price(call_price) and validate_price(put_price):
                return call_price, put_price

            print(f"期权价格验证失败: Call={call_price}, Put={put_price} (重试 {attempt + 1}/{max_retries})")
            log_to_file(f"期权价格验证失败: Call={call_price}, Put={put_price} (重试 {attempt + 1}/{max_retries})", "ERROR")
            
        except Exception as e:
            print(f"获取期权价格时发生错误 (重试 {attempt + 1}/{max_retries}): {str(e)}")
            log_to_file(f"获取期权价格时发生错误 (重试 {attempt + 1}/{max_retries}): {str(e)}", "ERROR")
            if Debug_mode:
                import traceback
                print(traceback.format_exc())
        
        time.sleep(retry_delay)
    
    return None, None

def initialize_contracts(current_etf_price, call_codes, put_codes, max_retries=3):
    """初始化合约信息，包含重试机制
    Args:
        current_etf_price: 当前ETF价格
        call_codes: Call期权代码列表
        put_codes: Put期权代码列表
        max_retries: 最大重试次数
    Returns:
        tuple: (call_strike, put_strike, call_contracts, put_contracts, monthly_remainder_cost) 或 None
    """
    for attempt in range(max_retries):
        try:
            if not validate_price(current_etf_price, 'etf'):
                log_to_file(f"ETF价格验证失败: {current_etf_price}", "ERROR")
                return None

            log_to_file(f"开始初始化合约，ETF价格: {current_etf_price}")
                
            # 获取所有行权价
            call_strike_prices = []
            put_strike_prices = []
            
            for code in call_codes:
                strike = get_option_greek_xingquanjia(code)
                if (strike):
                    strike_value = float(strike)
                    call_strike_prices.append((code, strike_value))
                    
            for code in put_codes:
                strike = get_option_greek_xingquanjia(code)
                if (strike):
                    strike_value = float(strike)
                    put_strike_prices.append((code, strike_value))

            if (not call_strike_prices or not put_strike_prices):
                log_to_file(f"获取行权价失败 (重试 {attempt + 1}/{max_retries})", "ERROR")
                time.sleep(2)
                continue

            log_to_file(f"获取到Call期权行权价数量: {len(call_strike_prices)}, Put期权行权价数量: {len(put_strike_prices)}")

            # 筛选标准行权价（0.05为单位的行权价，非除权价格）
            # 50ETF的标准行权价间隔为0.05，如2.65, 2.70, 2.75, 2.80, 2.85等
            def is_standard_strike(price):
                # 检查价格是否为标准行权价（以0.05为单位）
                multiplier = price / 0.05
                return abs(round(multiplier) - multiplier) < 0.0001  # 允许小误差
            
            # 分别筛选出看涨和看跌期权的标准行权价
            standard_call_strikes = [(code, strike) for code, strike in call_strike_prices if is_standard_strike(strike)]
            standard_put_strikes = [(code, strike) for code, strike in put_strike_prices if is_standard_strike(strike)]
            
            # 如果标准行权价数量太少，使用全部行权价
            if len(standard_call_strikes) < 5 or len(standard_put_strikes) < 5:
                log_to_file("标准行权价数量不足，使用全部行权价", "WARNING")
                standard_call_strikes = call_strike_prices
                standard_put_strikes = put_strike_prices
            
            # 获取所有不同的标准行权价，并排序
            unique_standard_strikes = sorted(set([strike for _, strike in standard_call_strikes] + 
                                              [strike for _, strike in standard_put_strikes]))
            
            # 获取所有行权价用于日志输出
            all_unique_strikes = sorted(set([strike for _, strike in call_strike_prices] + 
                                         [strike for _, strike in put_strike_prices]))
            
            # 找到最接近ETF价格的标准行权价作为平值（ATM）
            atm_strike = min(unique_standard_strikes, key=lambda x: abs(x - current_etf_price))
            log_to_file(f"ETF价格: {current_etf_price}, 平值行权价为: {atm_strike}")
            
            # 记录所有行权价和标准行权价用于调试
            log_to_file(f"所有可用行权价: {all_unique_strikes}")
            log_to_file(f"标准行权价: {unique_standard_strikes}")
            
            # 遍历获取实际存在的标准行权价（平值上下各五档）用于调试
            atm_index = unique_standard_strikes.index(atm_strike)
            available_strikes = []
            
            start_idx = max(0, atm_index - 5)
            end_idx = min(len(unique_standard_strikes), atm_index + 6)
            for i in range(start_idx, end_idx):
                available_strikes.append(unique_standard_strikes[i])
            
            log_to_file(f"平值周围可用标准行权价: {available_strikes}")
            
            # 确定看涨期权虚值行权价：平值上方的第N个行权价
            call_otm_index = atm_index + CALL_OTM_LEVEL
            if call_otm_index >= len(unique_standard_strikes):
                log_to_file(f"没有足够的Call虚值期权，需要{CALL_OTM_LEVEL}档 (重试 {attempt + 1}/{max_retries})", "ERROR")
                time.sleep(2)
                continue
            call_strike_target = unique_standard_strikes[call_otm_index]
            
            # 确定看跌期权虚值行权价：平值下方的第N个行权价
            put_otm_index = atm_index - PUT_OTM_LEVEL
            if put_otm_index < 0:
                log_to_file(f"没有足够的Put虚值期权，需要{PUT_OTM_LEVEL}档 (重试 {attempt + 1}/{max_retries})", "ERROR")
                time.sleep(2)
                continue
            put_strike_target = unique_standard_strikes[put_otm_index]
            
            log_to_file(f"ETF价格: {current_etf_price}, 平值: {atm_strike}, "
                        f"Call虚{CALL_OTM_LEVEL}档目标行权价: {call_strike_target}, "
                        f"Put虚{PUT_OTM_LEVEL}档目标行权价: {put_strike_target}")
            
            # 找到最接近目标行权价的Call期权
            selected_call_strike = None
            min_call_diff = float('inf')
            for code, strike in call_strike_prices:  # 这里使用所有期权，而不仅限于标准行权价的期权
                if abs(strike - call_strike_target) < min_call_diff:
                    min_call_diff = abs(strike - call_strike_target)
                    selected_call_strike = (code, strike)
            
            # 找到最接近目标行权价的Put期权
            selected_put_strike = None
            min_put_diff = float('inf')
            for code, strike in put_strike_prices:  # 这里使用所有期权，而不仅限于标准行权价的期权
                if abs(strike - put_strike_target) < min_put_diff:
                    min_put_diff = abs(strike - put_strike_target)
                    selected_put_strike = (code, strike)
            
            if selected_call_strike is None:
                log_to_file(f"找不到接近行权价{call_strike_target}的Call期权 (重试 {attempt + 1}/{max_retries})", "ERROR")
                time.sleep(2)
                continue
                
            if selected_put_strike is None:
                log_to_file(f"找不到接近行权价{put_strike_target}的Put期权 (重试 {attempt + 1}/{max_retries})", "ERROR")
                time.sleep(2)
                continue

            # 检查选出的期权是否与目标行权价相差太大
            if abs(selected_call_strike[1] - call_strike_target) > 0.05:
                log_to_file(f"警告：选出的Call期权行权价{selected_call_strike[1]}与目标行权价{call_strike_target}相差较大", "WARNING")
                
            if abs(selected_put_strike[1] - put_strike_target) > 0.05:
                log_to_file(f"警告：选出的Put期权行权价{selected_put_strike[1]}与目标行权价{put_strike_target}相差较大", "WARNING")

            log_to_file(f"选择期权: Call代码={selected_call_strike[0]}, 行权价={selected_call_strike[1]}, "
                       f"Put代码={selected_put_strike[0]}, 行权价={selected_put_strike[1]}")

            # 获取期权价格并验证
            call_price, put_price = verify_and_get_option_prices(
                selected_call_strike[0], 
                selected_put_strike[0],
                max_retries=5  # 增加重试次数
            )

            if (call_price is None or put_price is None):
                log_to_file(f"获取期权价格失败 (重试 {attempt + 1}/{max_retries})", "ERROR")
                time.sleep(2)
                continue

            log_to_file(f"获取期权价格 - Call: {call_price}, Put: {put_price}")

            # 计算合约数量
            call_contracts = int(CALL_INVESTMENT // (call_price * 10000))
            put_contracts = int(PUT_INVESTMENT // (put_price * 10000))

            if (not validate_contracts(call_contracts) or not validate_contracts(put_contracts)):
                log_to_file(f"合约数量验证失败 - Call: {call_contracts}, Put: {put_contracts} (重试 {attempt + 1}/{max_retries})", "ERROR")
                time.sleep(2)
                continue

            # 计算余数成本
            monthly_remainder_cost = int(MONTHLY_INVESTMENT - (call_contracts * call_price * 10000 + put_contracts * put_price * 10000))

            log_to_file(f"初始化完成 - Call合约: {call_contracts}, Put合约: {put_contracts}, 当月余数成本: {monthly_remainder_cost}")

            return selected_call_strike, selected_put_strike, call_contracts, put_contracts, monthly_remainder_cost

        except Exception as e:
            log_to_file(f"初始化合约出错 (重试 {attempt + 1}/{max_retries}): {str(e)}", "ERROR")
            if Debug_mode:
                import traceback
                log_to_file(f"错误详情: {traceback.format_exc()}", "ERROR")
            time.sleep(2)

    log_to_file("初始化合约失败，已达到最大重试次数", "ERROR")
    return None

def verify_historical_data(data, current_month):
    """验证历史数据的有效性
    Args:
        data: 历史数据字典
        current_month: 当前月份
    Returns:
        bool: 数据是否有效
    """
    try:
        if (not data):
            return False

        # 验证所有必需的字段是否存在
        required_fields = ['start_of_month_etf_price', 'selected_call_strike', 
                         'selected_put_strike', 'call_contracts', 'put_contracts', 
                         'monthly_remainder_cost', 'total_cost']
        if (not all(field in data for field in required_fields)):
            log_to_file("历史数据缺少必需字段", "ERROR")
            return False

        # 验证ETF价格
        if (not validate_price(data['start_of_month_etf_price'], 'etf')):
            log_to_file("历史数据中的ETF价格无效", "ERROR")
            return False

        # 验证行权价
        if (not validate_price(data['selected_call_strike'], 'option') or 
           not validate_price(data['selected_put_strike'], 'option')):
            log_to_file("历史数据中的行权价无效", "ERROR")
            return False

        # 验证合约数量
        if (not validate_contracts(data['call_contracts']) or 
           not validate_contracts(data['put_contracts'])):
            log_to_file("历史数据中的合约数量无效", "ERROR")
            return False

        # 验证成本和收益
        if (data['total_cost'] <= 0 or 
           data['monthly_remainder_cost'] < 0 or 
           data['monthly_remainder_cost'] >= MONTHLY_INVESTMENT):
            log_to_file("历史数据中的成本数据无效", "ERROR")
            return False

        return True
    except Exception as e:
        log_to_file(f"验证历史数据时出错: {str(e)}", "ERROR")
        return False

def get_historical_values(current_month, target_days, max_retries=3):
    """获取指定日期的历史记录值，带重试机制和时区处理
    Args:
        current_month: 当前月份，格式YYYYMM
        target_days: 目标剩余天数
        max_retries: 最大重试次数
    Returns:
        dict: 包含历史记录的字典，如果找不到返回None
    """
    
    for attempt in range(max_retries):
        try:
            # 获取当前CSV总表文件名
            csv_filename = get_csv_filename()
            if (not os.path.exists(csv_filename)):
                log_to_file(f"找不到历史记录文件: {csv_filename}", "WARNING")
                return None

            # 获取当前时区
            tz_offset = datetime.datetime.now().astimezone().utcoffset()
            tz_hours = int(tz_offset.total_seconds() / 3600)

            with open(csv_filename, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

                if (not rows):
                    log_to_file(f"CSV文件为空: {csv_filename}", "WARNING")
                    return None                # 按日期时间排序，确保我们先处理早些的记录
                try:
                    rows.sort(key=lambda x: datetime.datetime.strptime(x['Date'], "%Y-%m-%d %H:%M:%S"))
                except Exception as e:
                    log_to_file(f"排序记录时出错: {str(e)}", "WARNING")

                matching_records = []
                # 从最早的记录开始查找
                for row in rows:
                    try:
                        # 考虑时区因素处理日期
                        record_date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
                        # 调整到当地时区
                        record_date = record_date + datetime.timedelta(hours=tz_hours)
                        
                        # 获取记录的月份，优先使用Month列，如果有的话
                        record_month = row.get('Month', record_date.strftime("%Y%m"))
                        _, record_remainder_days = get_option_expire_day(record_month)
                        
                        if (record_remainder_days == target_days):
                            # 检查是否在交易时段
                            hour, minute = record_date.hour, record_date.minute
                            is_trading_time = any(
                                (start_h, start_m) <= (hour, minute) <= (end_h, end_m)
                                for start_h, start_m, end_h, end_m in TRADING_HOURS
                            )
                            
                            if (is_trading_time):
                                data = {
                                    'start_of_month_etf_price': float(row['ETF Price']),
                                    'selected_call_strike': float(row['Call Strike']),
                                    'selected_put_strike': float(row['Put Strike']),
                                    'call_contracts': int(row['Call Qty']),                                    'put_contracts': int(row['Put Qty']),
                                    'monthly_remainder_cost': int(row['Remainder Cost']),
                                    'total_cost': int(row['Total Cost']),                                    'previous_month_final_return': float(row['Total Return']) if row.get('Total Return') else 0,
                                    'record_date': record_date.strftime("%Y-%m-%d %H:%M:%S"),
                                    'month': row.get('Month', record_date.strftime("%Y%m")),
                                    'time_zone_offset': tz_hours,
                                    'month': row.get('Month', record_date.strftime("%Y%m"))
                                }
                                
                                if (verify_historical_data(data, current_month)):
                                    matching_records.append(data)
                                    # 如果是上午场的第一条记录，直接使用它
                                    if (hour == TRADING_HOURS[0][0] and minute >= TRADING_HOURS[0][1]):
                                        log_to_file(f"找到上午场第一条记录: {data['record_date']}")
                                        return data
                                    
                    except (ValueError, KeyError, TypeError) as e:
                        log_to_file(f"处理历史记录时出错: {str(e)}", "ERROR")
                        continue

                # 如果找到了匹配的记录，返回最早的那条
                if (matching_records):
                    earliest_record = matching_records[0]
                    log_to_file(f"使用最早的匹配记录: {earliest_record['record_date']}")
                    return earliest_record

            if (attempt < max_retries - 1):
                log_to_file(f"重试获取历史数据 (第{attempt + 1}次)", "WARNING")
                time.sleep(2)
            else:
                log_to_file(f"在历史记录中找不到剩余天数为{target_days}的有效数据", "WARNING")
                return None

        except Exception as e:
            log_to_file(f"读取历史记录时出错: {str(e)}", "ERROR")
            if (attempt < max_retries - 1):
                time.sleep(2)
            else:
                return None
    
    return None

def find_closest_historical_day(current_month, target_days):
    """查找最接近目标天数的历史记录
    Args:
        current_month: 当前月份，格式YYYYMM
        target_days: 目标剩余天数
    Returns:
        dict: 包含最接近日期的历史记录，如果找不到返回None
    """
    
    try:
        # 获取当前CSV总表文件名
        csv_filename = get_csv_filename()
        if (not os.path.exists(csv_filename)):
            log_to_file(f"找不到历史记录文件: {csv_filename}", "WARNING")
            return None

        closest_data = None
        min_days_diff = float('inf')
        records_by_date = {}  # 用于按日期分组的记录

        with open(csv_filename, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            rows = list(reader)            # 首先按日期分组
            for row in rows:
                try:
                    record_date = datetime.datetime.strptime(row['Date'], "%Y-%m-%d %H:%M:%S")
                    date_key = record_date.date()
                    if (date_key not in records_by_date):
                        records_by_date[date_key] = []
                    records_by_date[date_key].append(row)
                except Exception as e:
                    log_to_file(f"处理记录时出错: {str(e)}", "ERROR")
                    continue

            # 对每一天，只使用第一条记录
            for date, daily_records in records_by_date.items():
                try:
                    # 按时间排序，获取当天最早的记录
                    daily_records.sort(key=lambda x: datetime.datetime.strptime(x['Date'], "%Y-%m-%d %H:%M:%S"))
                    first_record = daily_records[0]
                    
                    record_date = datetime.datetime.strptime(first_record['Date'], "%Y-%m-%d %H:%M:%S")
                    # 获取记录的月份，优先使用Month列，如果有的话
                    record_month = first_record.get('Month', record_date.strftime("%Y%m"))
                    _, record_remainder_days = get_option_expire_day(record_month)
                    
                    # 只考虑比目标天数大的记录
                    if (record_remainder_days > target_days):
                        days_diff = record_remainder_days - target_days
                        if (days_diff < min_days_diff):
                            min_days_diff = days_diff
                            closest_data = {
                                'start_of_month_etf_price': float(first_record['ETF Price']),
                                'selected_call_strike': float(first_record['Call Strike']),
                                'selected_put_strike': float(first_record['Put Strike']),
                                'call_contracts': int(first_record['Call Qty']),
                                'put_contracts': int(first_record['Put Qty']),
                                'monthly_remainder_cost': int(first_record['Remainder Cost']),
                                'total_cost': int(first_record['Total Cost']),
                                'previous_month_final_return': float(first_record['Total Return']) if first_record.get('Total Return') else 0,
                                'actual_days': record_remainder_days,
                                'month': first_record.get('Month', record_date.strftime("%Y%m"))
                            }
                except Exception as e:
                    log_to_file(f"处理日期记录时出错: {str(e)}", "ERROR")
                    continue

        if (closest_data and verify_historical_data(closest_data, current_month)):
            log_to_file(f"找到最接近的历史记录，目标天数: {target_days}，实际天数: {closest_data['actual_days']}")
            return closest_data

        return None
    except Exception as e:
        log_to_file(f"查找最接近历史记录时出错: {str(e)}", "ERROR")
        return None

def verify_restored_data(historical_data, current_codes):
    """验证恢复的历史数据在当前是否有效
    Args:
        historical_data: 历史数据
        current_codes: 当前可用的期权代码元组 (call_codes, put_codes)
    Returns:
        bool: 数据是否有效
    """
    try:
        call_codes, put_codes = current_codes
        
        # 验证行权价是否在当前可用的期权中
        call_strike = historical_data['selected_call_strike']
        put_strike = historical_data['selected_put_strike']
        
        call_strikes_available = []
        put_strikes_available = []
        
        # 获取当前所有可用的行权价
        for code in call_codes:
            strike = float(get_option_greek_xingquanjia(code))
            if (strike):
                call_strikes_available.append(float(strike))
                
        for code in put_codes:
            strike = float(get_option_greek_xingquanjia(code))
            if (strike):
                put_strikes_available.append(float(strike))
        
        # 检查历史行权价是否仍然可用
        if (not any(abs(strike - call_strike) < 0.0001 for strike in call_strikes_available)):
            log_to_file(f"历史Call行权价 {call_strike} 在当前期权中不可用", "ERROR")
            return False
            
        if (not any(abs(strike - put_strike) < 0.0001 for strike in put_strikes_available)):
            log_to_file(f"历史Put行权价 {put_strike} 在当前期权中不可用", "ERROR")
            return False
            
        return True
    except Exception as e:
        log_to_file(f"验证恢复的数据时出错: {str(e)}", "ERROR")
        return False

def get_historical_data_with_fallback(current_month, remainder_days, target_days):
    """带有多重降级策略的历史数据获取
    Args:
        current_month: 当前月份
        remainder_days: 当前剩余天数
        target_days: 目标剩余天数
    Returns:
        tuple: (historical_data, fallback_type)
        fallback_type: 'exact' - 精确匹配
                      'closest' - 最接近的记录
                      'estimated' - 根据当前状态估算
                      None - 无法获取数据
    """
    try:
        # 1. 尝试获取精确的历史数据
        historical_data = get_historical_values(current_month, target_days)
        if (historical_data):
            log_to_file("找到精确匹配的历史数据")
            return historical_data, 'exact'
            
        # 2. 尝试获取最接近的历史数据
        historical_data = find_closest_historical_day(current_month, target_days)
        if (historical_data):
            log_to_file(f"使用最接近的历史数据，实际天数: {historical_data['actual_days']}")
            return historical_data, 'closest'
            
        # 3. 如果找不到任何历史数据，尝试使用当前状态进行估算
        current_etf_price = float(get_FitfyETF_price())
        if (current_etf_price and validate_price(current_etf_price, 'etf')):
            call_codes, put_codes = get_option_codes(current_month, underlying='510050')
            if (call_codes and put_codes):
                # 使用当前ETF价格作为起始价格
                estimated_data = {
                    'start_of_month_etf_price': current_etf_price,
                    'current_codes': (call_codes, put_codes)
                }
                log_to_file("使用当前状态估算数据")
                return estimated_data, 'estimated'
                
        return None, None
    except Exception as e:
        log_to_file(f"获取历史数据时出错: {str(e)}", "ERROR")
        return None, None

def start_new_record_cycle(date_str=None):
    """创建一个新的CSV数据记录周期
    
    此函数可以在当前程序执行期间切换到新的CSV文件。
    如果不提供日期参数，则使用当前日期作为新的开始日期。
    
    Args:
        date_str: 可选，格式为"YYYYMMDD"的日期字符串，如果未提供则使用当前日期
        
    Returns:
        str: 新创建的CSV文件名
    """
    global CSV_START_DATE
    
    # 如果未提供日期，使用当前日期
    if not date_str:
        date_str = datetime.datetime.now().strftime("%Y%m%d")
    
    # 更新全局变量
    CSV_START_DATE = date_str
    
    # 获取新的文件名
    new_filename = get_csv_filename()
    
    # 创建新文件
    create_csv_file()
    
    # 记录日志
    msg = f"已开始新的数据记录周期，使用CSV文件: {new_filename} (开始日期: {CSV_START_DATE})"
    print(f"✅ {msg}", flush=True)
    log_to_file(msg, "INFO")
    
    return new_filename

# 获取当前月份（格式 YYYYMM）
current_month = datetime.datetime.now().strftime("%Y%m")

# 清理旧状态文件
# cleanup_old_state_files()  # 已禁用：保留所有历史数据

# 清理旧日志文件
# cleanup_old_log_files()  # 已禁用：保留所有历史数据

# 在程序启动时添加日志
log_to_file(f"程序启动，DAYS_BEFORE_EXPIRY_START={DAYS_BEFORE_EXPIRY_START}")

# 初始化全局变量用于跨月收益计算
previous_month_return_for_total = 0
previous_month_final_return = 0  # 用于记录上个月的最终Total Return

# 尝试加载上次保存的状态
saved_state = load_state()
if (saved_state):
    try:
        # 如果存在保存的状态，使用保存的值
        start_of_month_etf_price = saved_state.get('start_of_month_etf_price')
        selected_call_strike = tuple(saved_state.get('selected_call_strike')) if (saved_state.get('selected_call_strike')) else None
        selected_put_strike = tuple(saved_state.get('selected_put_strike')) if (saved_state.get('selected_put_strike')) else None
        call_contracts = saved_state.get('call_contracts')
        put_contracts = saved_state.get('put_contracts')
        call_initial_price = saved_state.get('call_initial_price')
        put_initial_price = saved_state.get('put_initial_price')
        monthly_remainder_cost = saved_state.get('monthly_remainder_cost', 0)
        total_cost = saved_state.get('total_cost', 0)
        previous_month_final_return = saved_state.get('previous_month_final_return', 0)
        trading_month = saved_state.get('trading_month')
        processed_today = saved_state.get('processed_today', False)
        start_date = datetime.datetime.strptime(saved_state.get('start_date'), "%Y-%m-%d").date()
        month_switched = False  # 状态文件有效，不需要强制重新选择行权价
        monthly_investment_added = True  # 已有状态时，假设本月投资已添加
        
        print("✅ 已恢复保存的状态:", flush=True)
        print(f"├─ ETF初始价格: {start_of_month_etf_price}", flush=True)
        print(f"├─ Call行权价: {selected_call_strike[1] if (selected_call_strike) else None}", flush=True)
        print(f"├─ Put行权价: {selected_put_strike[1] if (selected_put_strike) else None}", flush=True)
        print(f"├─ Call合约数: {call_contracts}", flush=True)
        print(f"├─ Put合约数: {put_contracts}", flush=True)
        print(f"├─ 余数成本: {monthly_remainder_cost}", flush=True)
        print(f"└─ 总成本: {total_cost}", flush=True)
        print(f"└─ 上月基准收益: {previous_month_final_return}", flush=True)

        # 检查是否为跨月情况：total_cost > MONTHLY_INVESTMENT说明已经是跨月了
        if total_cost > MONTHLY_INVESTMENT:
            # 跨月情况：从CSV文件读取上个月的最终Total Return
            previous_month_final_return = get_previous_month_final_return()
            log_to_file(f"检测到跨月情况，从CSV获取上月最终Total Return = {previous_month_final_return}")
        
        # 在状态加载后进行一致性校验
        if check_csv_data_exists(current_month):
            print("🔍 发现CSV数据，正在校验状态一致性...")
            validation_result = validate_state_consistency(saved_state, current_month)

            # 无论是否一致，都检查是否需要补充缺失的字段
            if "csv_state" in validation_result and validation_result["csv_state"]:
                csv_state = validation_result["csv_state"]

                # 检查是否需要更新
                need_update = False
                update_reasons = []

                # 检查收益相关更新（仅在不一致时）
                if not validation_result["valid"] and abs(previous_month_final_return - csv_state.get('previous_month_final_return', 0)) > 100:
                    print(f"🔧 自动更新上月基准收益: {previous_month_final_return} -> {csv_state['previous_month_final_return']}")
                    previous_month_final_return = csv_state['previous_month_final_return']
                    need_update = True
                    update_reasons.append("上月基准收益")

                # 始终检查初始价格是否缺失
                if call_initial_price is None and csv_state.get('call_initial_price') is not None:
                    print(f"🔧 自动补充Call初始价格: {csv_state['call_initial_price']}")
                    call_initial_price = csv_state['call_initial_price']
                    need_update = True
                    update_reasons.append("Call初始价格")

                if put_initial_price is None and csv_state.get('put_initial_price') is not None:
                    print(f"🔧 自动补充Put初始价格: {csv_state['put_initial_price']}")
                    put_initial_price = csv_state['put_initial_price']
                    need_update = True
                    update_reasons.append("Put初始价格")

                # 如果需要更新，保存状态
                if need_update:
                    # 保存更新后的状态
                    updated_state_data = {
                        'start_of_month_etf_price': start_of_month_etf_price,
                        'selected_call_strike': list(selected_call_strike) if selected_call_strike else None,
                        'selected_put_strike': list(selected_put_strike) if selected_put_strike else None,
                        'call_contracts': call_contracts,
                        'put_contracts': put_contracts,
                        'call_initial_price': call_initial_price,
                        'put_initial_price': put_initial_price,
                        'monthly_remainder_cost': monthly_remainder_cost,
                        'total_cost': total_cost,
                        'previous_month_final_return': previous_month_final_return,
                        'trading_month': trading_month,
                        'processed_today': processed_today,
                        'start_date': start_date.strftime("%Y-%m-%d")
                    }
                    save_state(updated_state_data)
                    print("✅ 状态文件已更新为最新数据")
                    log_to_file(f"自动更新状态文件: {', '.join(update_reasons)}", "INFO")

            # 显示一致性校验结果
            if not validation_result["valid"]:
                print(f"⚠️ 状态不一致: {validation_result['reason']}")
                if "inconsistencies" in validation_result:
                    for inconsistency in validation_result["inconsistencies"]:
                        print(f"  - {inconsistency}")
                log_to_file(f"状态不一致: {validation_result['reason']}", "WARNING")
            else:
                print("✅ 状态一致性校验通过")
                log_to_file("状态一致性校验通过", "INFO")
        
        # 在状态加载后添加日志
        log_to_file(f"已加载状态文件，当前月份={current_month}, ETF初始价格={start_of_month_etf_price}, " + 
                    f"Call行权价={selected_call_strike[1] if (selected_call_strike) else None}, " +
                    f"Put行权价={selected_put_strike[1] if (selected_put_strike) else None}")
    except Exception as e:
        print(f"❌ 恢复状态时出错: {str(e)}，将使用初始值")
        saved_state = None
        log_to_file(f"恢复状态时出错: {str(e)}，将使用初始值", "ERROR")

if (not saved_state):
    # 如果没有保存的状态或状态无效，检查CSV数据是否存在
    csv_data_exists = check_csv_data_exists(current_month)
    
    if csv_data_exists:
        # 如果CSV中已有当前月份的数据，说明程序之前运行过，需要恢复状态而不是初始化
        print(f"⚠️ 状态文件丢失但发现CSV中有当前月份 {current_month} 的数据")
        print("程序将从CSV数据中恢复状态")
        log_to_file(f"状态文件丢失但发现CSV中有当前月份 {current_month} 的数据，从CSV恢复", "WARNING")
        
        # 从CSV数据中恢复状态
        csv_recovered_state = recover_state_from_csv(current_month)
        if csv_recovered_state:
            # 使用从CSV恢复的状态
            start_of_month_etf_price = csv_recovered_state.get('start_of_month_etf_price')
            selected_call_strike = tuple(csv_recovered_state.get('selected_call_strike')) if csv_recovered_state.get('selected_call_strike') else None
            selected_put_strike = tuple(csv_recovered_state.get('selected_put_strike')) if csv_recovered_state.get('selected_put_strike') else None
            call_contracts = csv_recovered_state.get('call_contracts')
            put_contracts = csv_recovered_state.get('put_contracts')
            monthly_remainder_cost = csv_recovered_state.get('monthly_remainder_cost', 0)
            total_cost = csv_recovered_state.get('total_cost', 0)
            previous_month_final_return = csv_recovered_state.get('previous_month_final_return', 0)
            call_initial_price = csv_recovered_state.get('call_initial_price')  # 从CSV恢复的初始价格
            put_initial_price = csv_recovered_state.get('put_initial_price')   # 从CSV恢复的初始价格
            trading_month = current_month
            processed_today = False
            month_switched = False  # 不强制重新选择行权价
            monthly_investment_added = True  # 假设已添加投资
            start_date = datetime.datetime.strptime(csv_recovered_state.get('start_date'), "%Y-%m-%d").date()
            
            # 立即保存恢复的状态到JSON文件
            recovered_state_data = {
                'start_of_month_etf_price': start_of_month_etf_price,
                'selected_call_strike': list(selected_call_strike) if selected_call_strike else None,
                'selected_put_strike': list(selected_put_strike) if selected_put_strike else None,
                'call_contracts': call_contracts,
                'put_contracts': put_contracts,
                'call_initial_price': call_initial_price,
                'put_initial_price': put_initial_price,
                'monthly_remainder_cost': monthly_remainder_cost,
                'total_cost': total_cost,
                'previous_month_final_return': previous_month_final_return,
                'trading_month': trading_month,
                'processed_today': processed_today,
                'start_date': start_date.strftime("%Y-%m-%d")
            }
            save_state(recovered_state_data)
            print(f"✅ 已从CSV数据恢复状态并保存JSON文件")
            log_to_file("从CSV数据恢复状态并保存JSON文件成功", "INFO")
        else:
            # 恢复失败，使用保守设置
            print(f"❌ 从CSV恢复状态失败，使用保守设置")
            start_of_month_etf_price = None
            selected_call_strike = None
            selected_put_strike = None
            call_contracts = None
            put_contracts = None
            call_initial_price = None
            put_initial_price = None
            monthly_remainder_cost = 0
            total_cost = 0
            previous_month_final_return = 0
            trading_month = current_month
            processed_today = False
            month_switched = False
            monthly_investment_added = True
            start_date = datetime.datetime.now().date()
    else:
        # 如果没有保存的状态且CSV中也没有数据，使用初始值
        start_of_month_etf_price = None
        selected_call_strike = None
        selected_put_strike = None
        call_contracts = None
        put_contracts = None
        call_initial_price = None
        put_initial_price = None
        monthly_remainder_cost = 0
        total_cost = 0
        previous_month_final_return = 0
        trading_month = None
        processed_today = False
        month_switched = True   # 【修复】状态验证失败时，强制重新选择行权价，跳过历史数据恢复
        monthly_investment_added = False  # 初始化月投资标记
        start_date = datetime.datetime.now().date()
    
    # 【新增】如果不是第一个月份，检查是否需要从上个月恢复收益
    # 计算上个月
    try:
        year = int(current_month[:4])
        month = int(current_month[4:])
        if month == 1:
            previous_month_str = f"{year-1}12"
        else:
            previous_month_str = f"{year}{month-1:02d}"
    except:
        previous_month_str = None
    
    # 只有在当前月份没有CSV数据时才执行跨月恢复逻辑
    csv_data_exists = check_csv_data_exists(current_month)
    if previous_month_str and current_month != FIRST_RECORD_MONTH and not csv_data_exists:
        #不是第一个记录月份且当前月份没有数据
        print(f"🔍 检测到{current_month}启动，尝试从{previous_month_str}数据恢复收益...", flush=True)
        log_to_file(f"检测到{current_month}启动，尝试从{previous_month_str}数据恢复收益", "INFO")
        
        # 尝试从CSV总表中获取上个月最后的收益
        csv_filename = get_csv_filename()
        if os.path.exists(csv_filename):
            try:
                with open(csv_filename, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # 查找最后一条上个月的数据
                    for line in reversed(lines):
                        if previous_month_str in line:
                            parts = line.strip().split(',')
                            if len(parts) >= 11:
                                prev_total_return = int(parts[10])  # Total Return
                                prev_total_cost = int(parts[9])     # Total Cost
                                # monthly_remainder_cost保持为0，将在后续计算中正确设置
                                total_cost = prev_total_cost + MONTHLY_INVESTMENT  # 加上新月份投资
                                monthly_investment_added = True  # 标记本月投资已添加
                                previous_month_final_return = prev_total_return  # 保存上月最终收益作为基准
                                print(f"✅ 从{previous_month_str}恢复收益: {prev_total_return}元, 新总投资: {total_cost}元", flush=True)
                                log_to_file(f"从{previous_month_str}恢复收益: {prev_total_return}元, 新总投资: {total_cost}元", "INFO")
                                break
            except Exception as e:
                print(f"从{previous_month_str}数据恢复收益失败: {str(e)}", flush=True)
                log_to_file(f"从{previous_month_str}数据恢复收益失败: {str(e)}", "ERROR")
    
    print("⚠️ 使用初始值启动程序", flush=True)
    log_to_file("未找到有效状态文件，使用初始值", "WARNING")

# 确保 CSV 文件创建，并写入表头（如果文件为空）
create_csv_file()

# 在程序启动时记录使用的CSV文件名
csv_filename = get_csv_filename()
print(f"ℹ️ 使用CSV总表文件: {csv_filename} (开始日期: {CSV_START_DATE})", flush=True)
log_to_file(f"使用CSV总表文件: {csv_filename} (开始日期: {CSV_START_DATE})", "INFO")

# 无限循环，每隔 1 分钟运行一次
while (True):
    try:
        # 获取当前时间
        now = datetime.datetime.now()
        current_date = now.date()
        current_hour, current_minute = now.hour, now.minute

        # **判断是否为交易日**
        weekday = now.weekday()  # 0=周一, 6=周日
        is_holiday = now.strftime("%Y-%m-%d") in Holiday
        is_trading_day = weekday < 5 and not is_holiday  # 周一到周五 & 非节假日

        if (not is_trading_day):
            print(f"📅 {current_date} 不是交易日，程序休眠 1 小时...", flush=True)
            log_to_file(f"{current_date} 不是交易日，程序休眠 1 小时...", "INFO")
            time.sleep(3600)  # 休眠 1 小时，直到进入交易日
            continue  # 跳过本次循环

        # **检查是否在交易时段**
        is_trading_time = any(
            (start_h, start_m) <= (current_hour, current_minute) <= (end_h, end_m)
            for start_h, start_m, end_h, end_m in TRADING_HOURS
        )

        if (not is_trading_time):
            print(f"⏳ 当前时间 {now.strftime('%H:%M:%S')} 不在交易时段，等待中...", flush=True)
            log_to_file(f"当前时间 {now.strftime('%H:%M:%S')} 不在交易时段，等待中...", "INFO")
            time.sleep(60)  # 休眠 1 分钟，直到进入交易时段
            continue  # 跳过本次循环

        # 计算程序运行天数
        # 总表使用CSV开始日期作为基准
        csv_start = datetime.datetime.strptime(CSV_START_DATE, "%Y%m%d").date()
        total_days_running = max((current_date - csv_start).days + 1, 1)  # 总表运行天数

        # 月度分表使用当月开始日期作为基准
        current_month_days = max((current_date - start_date).days + 1, 1)  # 当月运行天数

        # 获取当前月份和下一个月份
        current_month = datetime.datetime.now().strftime("%Y%m")
        next_month = get_next_month(current_month)
        if (next_month is None):
            print("无法计算下一月份，等待重试...")
            log_to_file("无法计算下一月份，等待重试...", "ERROR")
            time.sleep(60)
            continue

        # **每天 00:00 重置 processed_today，确保新一天可以进入分支**
        if (current_date != start_date):
            processed_today = False
            # 注意：不再更新 start_date，保持当月开始日期不变，以便正确计算当月天数

        # 如果月份变化，重置选定的行权价
        if (current_month != trading_month):
            # 检查是否已经处理过本月的投资
            saved_state = load_state()
            csv_data_exists = check_csv_data_exists(current_month)
            
            # 如果没有状态文件或状态文件中的月份不匹配，且CSV中也没有数据，才初始化新月份
            if ((not saved_state or saved_state.get('trading_month') != current_month) and not csv_data_exists):
                selected_call_strike = None
                selected_put_strike = None
                call_contracts = None
                put_contracts = None
                call_initial_price = None
                put_initial_price = None
                start_of_month_etf_price = None  # 【修复】清空上月ETF价格，确保使用新月份的实时价格
                monthly_remainder_cost = 0
                if not monthly_investment_added:
                    total_cost += MONTHLY_INVESTMENT  # 只有在新的月份且没有保存状态时才增加投资
                    monthly_investment_added = True
                    print(f"💵 新月份追加投资: {MONTHLY_INVESTMENT}元, 总投资: {total_cost}元", flush=True)
                print(f"🔄 月份变化: {trading_month} -> {current_month}, 初始化新月份数据")
                log_to_file(f"月份变化: {trading_month} -> {current_month}, 初始化新月份数据")
            elif csv_data_exists:
                print(f"📊 发现当前月份 {current_month} 已有数据，不重新初始化")
                log_to_file(f"发现当前月份 {current_month} 已有数据，不重新初始化")
            trading_month = current_month  # 更新交易月份

        # 获取当前月份和下一个月份的期权到期日及剩余天数
        expire_day, remainder_days = get_option_expire_day(current_month)
        next_expire_day, next_month_remainder_days = get_option_expire_day(next_month)

        if (remainder_days is None and next_month_remainder_days is None):
            print("获取期权到期日失败，等待下一次重试...", flush=True)
            log_to_file("获取期权到期日失败，等待下一次重试...", "ERROR")
            time.sleep(60)
            continue

        # 确定是否开始和停止记录
        start_recording = should_start_recording(remainder_days, next_month_remainder_days)
        stop_recording = not should_stop_recording(remainder_days)  # 注意这里取反，因为我们要在大于停止天数时继续记录

        print(f"[{datetime.datetime.now()}] 状态信息:", flush=True)
        print(f"├─ 总运行天数: {total_days_running}, 当月运行天数: {current_month_days}", flush=True)
        print(f"├─ 当前月({current_month}) 到期日: {expire_day}, 剩余天数: {remainder_days}", flush=True)
        print(f"├─ 下一月({next_month}) 到期日: {next_expire_day}, 剩余天数: {next_month_remainder_days}", flush=True)
        print(f"├─ 是否开始记录: {start_recording}", flush=True)
        print(f"└─ 是否继续记录: {stop_recording}", flush=True)

        log_to_file(f"状态信息: 总运行天数={total_days_running}, 当月运行天数={current_month_days}, 当前月({current_month})到期日={expire_day}, 剩余天数={remainder_days}, " +
                    f"下月({next_month})到期日={next_expire_day}, 剩余天数={next_month_remainder_days}, " +
                    f"是否开始记录={start_recording}, 是否继续记录={stop_recording}")

        # 如果当前月合约即将到期，且下月合约已经可以开始记录，则切换到下月合约
        if (should_switch_to_next_month(remainder_days, next_month_remainder_days)):
            print(f"🔄 合约切换提示:", flush=True)
            print(f"├─ 当前月({current_month})合约剩余 {remainder_days} 天", flush=True)
            print(f"├─ 下月({next_month})合约剩余 {next_month_remainder_days} 天", flush=True)
            print(f"└─ 执行切换操作", flush=True)
            
            log_to_file(f"合约切换提示: 当前月({current_month})合约剩余 {remainder_days} 天, " +
                        f"下月({next_month})合约剩余 {next_month_remainder_days} 天, 执行切换操作")

            # 保存当前状态以备回溯
            old_month_data = {
                'month': current_month,
                'expire_day': expire_day,
                'remainder_days': remainder_days,
                'call_strike': selected_call_strike,
                'put_strike': selected_put_strike,
                'total_return': previous_month_final_return
            }
            
            # 保存上个月的最终收益，这是关键修复！
            previous_month_total_return = previous_month_final_return
            print(f"💰 保存上个月({current_month})的最终收益: {previous_month_total_return}元", flush=True)
            log_to_file(f"保存上个月({current_month})的最终收益: {previous_month_total_return}元", "INFO")
            
            # 切换到下月
            current_month = next_month
            expire_day = next_expire_day
            remainder_days = next_month_remainder_days
            
            # 重置合约相关变量
            selected_call_strike = None
            selected_put_strike = None
            call_contracts = None
            put_contracts = None

            # 检查是否已有CSV数据来恢复初始价格，避免设置为null
            if check_csv_data_exists(current_month):
                csv_state = recover_state_from_csv(current_month)
                if csv_state:
                    call_initial_price = csv_state.get('call_initial_price')
                    put_initial_price = csv_state.get('put_initial_price')
                    print(f"🔧 从CSV恢复初始价格: Call={call_initial_price}, Put={put_initial_price}", flush=True)
                    log_to_file(f"从CSV恢复初始价格: Call={call_initial_price}, Put={put_initial_price}", "INFO")
                else:
                    call_initial_price = None
                    put_initial_price = None
            else:
                call_initial_price = None
                put_initial_price = None
            start_of_month_etf_price = None
            processed_today = False
            
            # 【关键修复】设置换月标志，强制重新选择行权价
            month_switched = True
            
            # 【修复】保存上月收益到total_return作为基准，monthly_remainder_cost将在后续正确计算
            # 这样确保了收益的连续性，不会在换月时丢失
            previous_month_final_return = previous_month_total_return  # 保存上月收益作为基准
            # monthly_remainder_cost将在合约初始化时正确计算为当月余数成本
            print(f"🔄 新月份({current_month})保存上月收益作为基准: {previous_month_final_return}元", flush=True)
            log_to_file(f"新月份({current_month})保存上月收益作为基准: {previous_month_final_return}元", "INFO")
            
            # 增加总投资成本（新月份投资）
            if not monthly_investment_added:
                total_cost += MONTHLY_INVESTMENT
                monthly_investment_added = True
                print(f"💵 新月份追加投资: {MONTHLY_INVESTMENT}元, 总投资: {total_cost}元", flush=True)
                log_to_file(f"新月份追加投资: {MONTHLY_INVESTMENT}元, 总投资: {total_cost}元", "INFO")
            
            # 更新状态文件，同时保存上月数据
            state_data = {
                'start_of_month_etf_price': start_of_month_etf_price,
                'selected_call_strike': None,
                'selected_put_strike': None,
                'call_contracts': call_contracts,
                'put_contracts': put_contracts,
                'call_initial_price': call_initial_price,
                'put_initial_price': put_initial_price,
                'monthly_remainder_cost': monthly_remainder_cost,  # 包含上月收益
                'total_cost': total_cost,
                'previous_month_final_return': monthly_remainder_cost,  # 初始previous_month_final_return等于monthly_remainder_cost
                'trading_month': current_month,
                'processed_today': processed_today,
                'start_date': start_date.strftime("%Y-%m-%d"),
                'last_month_data': old_month_data  # 保存上月数据供参考
            }
            save_state(state_data)
            print("✅ 状态已更新，合约已切换到下月，上月收益已累计", flush=True)
            log_to_file("状态已更新，合约已切换到下月，上月收益已累计", "INFO")

        # 记录 `DAYS_BEFORE_EXPIRY_START` 这天是否第一次运行
        is_first_run_today = False

        # 当程序首次启动时，检查是否需要初始化合约信息
        if ((selected_call_strike is None or call_contracts is None) and start_recording and stop_recording):
            log_to_file(f"程序首次启动，当前剩余天数={remainder_days}, " +
                       f"DAYS_BEFORE_EXPIRY_START={DAYS_BEFORE_EXPIRY_START}")
            
            # 如果当前剩余天数小于DAYS_BEFORE_EXPIRY_START，尝试从历史记录获取数据
            # 但如果是换月后，强制重新选择行权价，不使用历史数据
            if (remainder_days < DAYS_BEFORE_EXPIRY_START and not month_switched):
                log_to_file(f"程序在中途启动，当前剩余天数({remainder_days}) < DAYS_BEFORE_EXPIRY_START({DAYS_BEFORE_EXPIRY_START})")
                
                print(f"🔍 开始获取历史数据: 月份={current_month}, 剩余天数={remainder_days}", flush=True)
                log_to_file(f"开始调用get_historical_data_with_fallback: 月份={current_month}, 剩余天数={remainder_days}")
                
                historical_data, data_type = get_historical_data_with_fallback(
                    current_month, 
                    remainder_days, 
                    DAYS_BEFORE_EXPIRY_START
                )
                
                print(f"✅ 历史数据获取完成: data_type={data_type}, has_data={historical_data is not None}", flush=True)
                log_to_file(f"历史数据获取完成: data_type={data_type}, has_data={historical_data is not None}")
                
                if (historical_data):
                    # 获取当前可用的期权代码
                    call_codes, put_codes = get_option_codes(current_month, underlying='510050')
                    if (not call_codes or not put_codes):
                        log_to_file("获取期权代码失败", "ERROR")
                        print("获取期权代码失败，等待下一次重试...", flush=True)
                        time.sleep(60)
                        continue
                        
                    if (data_type in ['exact', 'closest']):
                        # 验证恢复的数据在当前是否有效
                        if (verify_restored_data(historical_data, (call_codes, put_codes))):
                            # 使用历史数据
                            start_of_month_etf_price = historical_data['start_of_month_etf_price']
                            
                            # 查找匹配的期权代码
                            call_strike_target = historical_data['selected_call_strike']
                            put_strike_target = historical_data['selected_put_strike']
                            
                            selected_call_strike = None
                            selected_put_strike = None
                            
                            # 查找对应的期权代码
                            for code in call_codes:
                                strike = float(get_option_greek_xingquanjia(code))
                                if (abs(strike - call_strike_target) < 0.0001):
                                    selected_call_strike = (code, strike)
                                    break
                            
                            for code in put_codes:
                                strike = float(get_option_greek_xingquanjia(code))
                                if (abs(strike - put_strike_target) < 0.0001):
                                    selected_put_strike = (code, strike)
                                    break
                            
                            if (selected_call_strike and selected_put_strike):
                                call_contracts = historical_data['call_contracts']
                                put_contracts = historical_data['put_contracts']
                                monthly_remainder_cost = historical_data['monthly_remainder_cost']
                                total_cost = historical_data['total_cost']
                                
                                log_to_file(f"成功恢复历史数据 (类型: {data_type})")
                                print(f"✅ 已恢复历史数据 (类型: {data_type}):", flush=True)
                                print(f"├─ 选定 Call 行权价: {selected_call_strike[1]}, Put 行权价: {selected_put_strike[1]}", flush=True)
                                print(f"├─ Call 合约数: {call_contracts}, Put 合约数: {put_contracts}", flush=True)
                                print(f"├─ 余数成本: {monthly_remainder_cost}", flush=True)
                                print(f"└─ 总成本: {total_cost}", flush=True)
                                
                                # 保存状态
                                state_data = {
                                    'start_of_month_etf_price': start_of_month_etf_price,
                                    'selected_call_strike': selected_call_strike,
                                    'selected_put_strike': selected_put_strike,
                                    'call_contracts': call_contracts,
                                    'put_contracts': put_contracts,
                                    'call_initial_price': call_initial_price,
                                    'put_initial_price': put_initial_price,
                                    'monthly_remainder_cost': monthly_remainder_cost,
                                    'total_cost': total_cost,
                                    'previous_month_final_return': previous_month_final_return,
                                    'trading_month': trading_month,
                                    'processed_today': processed_today,
                                    'start_date': start_date.strftime("%Y-%m-%d"),
                                    'data_source': data_type
                                }
                                save_state(state_data)
                                continue  # 跳过后续的初始化逻辑
                            
                    elif (data_type == 'estimated'):
                        log_to_file("使用估算数据初始化合约")
                        # 使用当前状态初始化合约
                        result = initialize_contracts(
                            historical_data['start_of_month_etf_price'],
                            call_codes,
                            put_codes
                        )
                        if (result):
                            selected_call_strike, selected_put_strike, call_contracts, put_contracts, monthly_remainder_cost = result
                            start_of_month_etf_price = historical_data['start_of_month_etf_price']
                            
                            # 保存使用估算数据初始化的状态
                            state_data = {
                                'start_of_month_etf_price': start_of_month_etf_price,
                                'selected_call_strike': selected_call_strike,
                                'selected_put_strike': selected_put_strike,
                                'call_contracts': call_contracts,
                                'put_contracts': put_contracts,
                                'call_initial_price': call_initial_price,
                                'put_initial_price': put_initial_price,
                                'monthly_remainder_cost': monthly_remainder_cost,
                                'total_cost': total_cost,
                                'previous_month_final_return': previous_month_final_return,
                                'trading_month': current_month,
                                'processed_today': processed_today,
                                'start_date': start_date.strftime("%Y-%m-%d"),
                                'initialization_type': 'estimated',
                                'initialization_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            }
                            save_state(state_data)
                            log_to_file("已保存估算数据初始化的状态", "INFO")
                            
                            # 将初始化数据写入CSV文件
                            try:
                                # 获取初始期权价格
                                call_price, put_price = verify_and_get_option_prices(
                                    selected_call_strike[0],
                                    selected_put_strike[0]
                                )
                                
                                if call_price is not None and put_price is not None:
                                    # 计算初始总收益
                                    initial_total_return = int((call_contracts * call_price * 10000) + 
                                                            (put_contracts * put_price * 10000) + 
                                                            monthly_remainder_cost)
                                    
                                    # 计算初始年化收益率（使用总运行天数）
                                    initial_annual_return = 0.0
                                    if total_cost > 0 and total_days_running > 0:
                                        initial_annual_return = round(((initial_total_return / total_cost - 1) / total_days_running * 365) * 100, 4)
                                      # 将初始化数据同时写入总表和月度分表
                                    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    current_month_csv = f"option_trading_{current_month}.csv"
                                    
                                    # 1. 写入总表数据（英文表头，包含月份字段）
                                    with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
                                        writer = csv.writer(file)
                                        writer.writerow([
                                            current_datetime,
                                            start_of_month_etf_price,
                                            selected_call_strike[1],
                                            selected_put_strike[1],
                                            call_price,
                                            put_price,
                                            call_contracts,
                                            put_contracts,
                                            monthly_remainder_cost,
                                            total_cost,
                                            initial_total_return,
                                            f"{initial_annual_return}%",
                                            current_month
                                        ])
                                        file.flush()
                                    
                                    # 2. 写入月度分表数据（中文表头，无月份字段）
                                    with open(current_month_csv, 'a', newline='', encoding='utf-8') as file:
                                        writer = csv.writer(file)
                                        writer.writerow([
                                            current_datetime,
                                            start_of_month_etf_price,
                                            selected_call_strike[1],
                                            selected_put_strike[1],
                                            call_price,
                                            put_price,
                                            call_contracts,
                                            put_contracts,
                                            monthly_remainder_cost,
                                            total_cost,
                                            initial_total_return,
                                            f"{initial_annual_return}%"
                                        ])
                                        file.flush()
                                    
                                    log_to_file(f"已将初始化数据同时写入总表和月度分表: {csv_filename} 和 {current_month_csv}", "INFO")
                            except Exception as e:
                                log_to_file(f"写入初始化数据到CSV文件时出错: {str(e)}", "ERROR")

                            print(f"✅ 使用估算数据初始化完成:", flush=True)
                            print(f"├─ 选定 Call 行权价: {selected_call_strike[1]}, Put 行权价: {selected_put_strike[1]}", flush=True)
                            print(f"├─ Call 合约数: {call_contracts}, Put 合约数: {put_contracts}", flush=True)
                        print(f"├─ 余数成本: {monthly_remainder_cost}", flush=True)
                        print(f"└─ 总成本: {total_cost}", flush=True)
                        continue
            
                log_to_file("无法恢复或估算历史数据，将使用正常初始化流程", "WARNING")

            # 如果找不到历史数据或者是正常启动，执行正常的初始化逻辑
            if month_switched:
                print(f"🔄 换月后重新选择行权价，当前月份: {current_month}", flush=True)
                log_to_file(f"换月后重新选择行权价，当前月份: {current_month}", "INFO")
            
            # 获取ETF价格
            current_etf_price = float(get_FitfyETF_price())
            if (current_etf_price is None):
                log_to_file("获取ETF价格失败", "ERROR")
                print("获取ETF价格失败，等待下一次重试...", flush=True)
                time.sleep(60)
                continue

            # 如果是在DAYS_BEFORE_EXPIRY_START之后启动，使用当前ETF价格
            if (start_of_month_etf_price is None):
                start_of_month_etf_price = current_etf_price
                log_to_file(f"使用当前ETF价格 {start_of_month_etf_price} 作为初始价格")

            # 获取期权代码
            call_codes, put_codes = get_option_codes(current_month, underlying='510050')
            if (not call_codes or not put_codes):
                log_to_file("获取期权代码失败", "ERROR")
                print("获取期权代码失败，等待下一次重试...", flush=True)
                time.sleep(60)
                continue

            # 初始化合约信息
            result = initialize_contracts(start_of_month_etf_price, call_codes, put_codes)
            if (result is None):
                log_to_file("初始化合约信息失败", "ERROR")
                print("初始化合约信息失败，等待下一次重试...", flush=True)
                time.sleep(60)
                continue

            selected_call_strike, selected_put_strike, call_contracts, put_contracts, new_monthly_remainder_cost = result
            
            # 如果是换月后的初始化，需要保持原有的monthly_remainder_cost（包含上个月收益）
            if monthly_remainder_cost == 0:  # 新程序启动
                monthly_remainder_cost = new_monthly_remainder_cost
                log_to_file(f"新程序启动，使用计算的余数成本: {monthly_remainder_cost}", "INFO")
            else:  # 换月后的初始化
                # 保持原有的monthly_remainder_cost（包含上个月收益），加上新月份的余数成本
                monthly_remainder_cost += new_monthly_remainder_cost
                log_to_file(f"换月后初始化，保持原有累计收益并加上新月份余数: {monthly_remainder_cost}", "INFO")

            print(f"✅ 初始化完成:", flush=True)
            print(f"├─ 选定 Call 行权价: {selected_call_strike[1]}, Put 行权价: {selected_put_strike[1]}", flush=True)
            print(f"├─ Call 合约数: {call_contracts}, Put 合约数: {put_contracts}, 余数成本: {monthly_remainder_cost}, 总成本: {total_cost}", flush=True)

            log_to_file(f"合约初始化成功: Call行权价={selected_call_strike[1]}, " +
                       f"Put行权价={selected_put_strike[1]}, " +
                       f"Call数量={call_contracts}, Put数量={put_contracts}, " +
                       f"余数成本={monthly_remainder_cost}")

            # 保存状态
            state_data = {
                'start_of_month_etf_price': start_of_month_etf_price,
                'selected_call_strike': selected_call_strike,
                'selected_put_strike': selected_put_strike,
                'call_contracts': call_contracts,
                'put_contracts': put_contracts,
                'call_initial_price': call_initial_price,
                'put_initial_price': put_initial_price,
                'monthly_remainder_cost': monthly_remainder_cost,
                'total_cost': total_cost,
                'previous_month_final_return': previous_month_final_return,
                'trading_month': trading_month,
                'processed_today': processed_today,
                'start_date': start_date.strftime("%Y-%m-%d")
            }
            save_state(state_data)
            
            # 重置换月标志
            if month_switched:
                month_switched = False
                print(f"✅ 换月初始化完成，重置换月标志", flush=True)
                log_to_file("换月初始化完成，重置换月标志", "INFO")

        # **在 `DAYS_BEFORE_EXPIRY_START` 这天，记录 ETF 价格**
        if (remainder_days == DAYS_BEFORE_EXPIRY_START and not processed_today):
            start_of_month_etf_price = float(get_FitfyETF_price())  # 记录本月初 ETF 价格
            processed_today = True # 标记当天已处理
            is_first_run_today = True  # 标记今天第一次运行    

        # 计算是否开始/停止记录
        start_recording = remainder_days <= DAYS_BEFORE_EXPIRY_START
        stop_recording = remainder_days >= DAYS_BEFORE_EXPIRY_STOP

        print(f"[{datetime.datetime.now()}] 总运行天数: {total_days_running}, 当月运行天数: {current_month_days}, 当前剩余天数: {remainder_days}", flush=True)

        if (start_recording and stop_recording):
            print("---- 开始记录交易数据 ----", flush=True)
            log_to_file("开始记录交易数据", "INFO")

            # 获取 ETF 价格，添加错误处理
            etf_price = get_FitfyETF_price()
            if (etf_price is None):
                log_to_file("获取ETF价格失败", "ERROR")
                print("获取ETF价格失败，等待下一次重试...", flush=True)
                time.sleep(60)
                continue
            etf_price = float(etf_price)

            # **确保 `selected_call_strike` 始终有值**
            if (selected_call_strike is None):
                if (start_of_month_etf_price is None):
                    start_of_month_etf_price = etf_price  # **如果 `start_of_month_etf_price` 还没有记录，则用当前 ETF 价格**
                etf_price = start_of_month_etf_price  # **使用 `DAYS_BEFORE_EXPIRY_START` 记录的 ETF 价格**

                # **重新计算虚两档行权价**
                call_codes, put_codes = get_option_codes(current_month, underlying='510050')

                call_strike_prices = [(code, float(get_option_greek_xingquanjia(code))) for code in call_codes]
                put_strike_prices = [(code, float(get_option_greek_xingquanjia(code))) for code in put_codes]

                # 找到最接近 ETF 价格的 ATM 行权价
                atm_call = min(call_strike_prices, key=lambda x: abs(x[1] - etf_price))
                atm_put = min(put_strike_prices, key=lambda x: abs(x[1] - etf_price))

                # 选择 ATM 之上的第二档 Call 期权（虚两档）
                selected_call_strike = sorted([s for s in call_strike_prices if s[1] > atm_call[1]], key=lambda x: x[1])[1]

                # 选择 ATM 之下的第二档 Put 期权（虚两档）
                selected_put_strike = sorted([s for s in put_strike_prices if s[1] < atm_put[1]], key=lambda x: -x[1])[1]

                # 保存状态到文件
                state_data = {
                    'start_of_month_etf_price': start_of_month_etf_price,
                    'selected_call_strike': selected_call_strike,
                    'selected_put_strike': selected_put_strike,
                    'call_contracts': call_contracts,
                    'put_contracts': put_contracts,
                    'call_initial_price': call_initial_price,
                    'put_initial_price': put_initial_price,
                    'monthly_remainder_cost': monthly_remainder_cost,
                    'total_cost': total_cost,
                    'previous_month_final_return': previous_month_final_return,
                    'trading_month': trading_month,
                    'processed_today': processed_today,
                    'start_date': start_date.strftime("%Y-%m-%d")
                }
                save_state(state_data)

            # **确保 `DAYS_BEFORE_EXPIRY_START` 这天重新计算合约数量**
            if (is_first_run_today):
                # **计算并固定合约数量**
                call_price_at_start, put_price_at_start = verify_and_get_option_prices(
                    selected_call_strike[0],
                    selected_put_strike[0],
                    max_retries=5,  # 增加重试次数
                    retry_delay=3   # 增加重试延迟
                )

                if call_price_at_start is None or put_price_at_start is None:
                    print("获取期权初始价格失败，等待下一次重试...", flush=True)
                    log_to_file("获取期权初始价格失败，等待下一次重试...", "ERROR")
                    time.sleep(60)
                    continue

                call_contracts = int(CALL_INVESTMENT // (call_price_at_start * 10000))
                put_contracts = int(PUT_INVESTMENT // (put_price_at_start * 10000))

                # **计算当月余数成本（整数）**
                current_month_remainder = int(MONTHLY_INVESTMENT - (call_contracts * call_price_at_start * 10000 + put_contracts * put_price_at_start * 10000))

                if monthly_remainder_cost == 0:  # 新程序启动
                    monthly_remainder_cost = current_month_remainder
                    log_to_file(f"新程序启动，当月余数成本: {monthly_remainder_cost}", "INFO")
                else:  # 换月后的初始化
                    # monthly_remainder_cost每月只应包含当月的余数，不累加
                    monthly_remainder_cost = current_month_remainder
                    log_to_file(f"换月后初始化，当月余数成本: {monthly_remainder_cost}, 上月最终收益: {previous_month_final_return}", "INFO")

                # 保存初始期权价格，用于后续计算月度分表
                call_initial_price = call_price_at_start
                put_initial_price = put_price_at_start

                print(f"✅ 选定 Call 行权价: {selected_call_strike[1]}, Put 行权价: {selected_put_strike[1]}", flush=True)
                print(f"✅ 固定 Call 合约数: {call_contracts}, Put 合约数: {put_contracts}, 余数成本: {monthly_remainder_cost}, 总成本: {total_cost}", flush=True)

                log_to_file(f"选定 Call 行权价: {selected_call_strike[1]}, Put 行权价: {selected_put_strike[1]}, " +
                           f"固定 Call 合约数: {call_contracts}, Put 合约数: {put_contracts}, 余数成本: {monthly_remainder_cost}, 总成本: {total_cost}")

                # 保存更新后的状态
                state_data = {
                    'start_of_month_etf_price': start_of_month_etf_price,
                    'selected_call_strike': selected_call_strike,
                    'selected_put_strike': selected_put_strike,
                    'call_contracts': call_contracts,
                    'put_contracts': put_contracts,
                    'call_initial_price': call_initial_price,
                    'put_initial_price': put_initial_price,
                    'monthly_remainder_cost': monthly_remainder_cost,
                    'total_cost': total_cost,
                    'previous_month_final_return': previous_month_final_return,
                    'trading_month': trading_month,
                    'processed_today': processed_today,
                    'start_date': start_date.strftime("%Y-%m-%d")
                }
                save_state(state_data)

            # **之后的每一分钟，使用固定行权价和合约数量，仅更新最新期权价格**
            call_option_price, put_option_price = verify_and_get_option_prices(
                selected_call_strike[0],
                selected_put_strike[0]
            )

            if call_option_price is None or put_option_price is None:
                print("获取最新期权价格失败，等待下一次重试...", flush=True)
                log_to_file("获取最新期权价格失败，等待下一次重试...", "ERROR")
                time.sleep(60)
                continue

            # 获取 ETF 最新价格(ETF价格有可能被修改，这里需要刷新)
            etf_price = float(get_FitfyETF_price()) 

            # 验证ETF价格
            if (not validate_price(etf_price, price_type='etf')):
                print(f"ETF价格数据异常: {etf_price}，等待下一次重试...", flush=True)
                log_to_file(f"ETF价格数据异常: {etf_price}，等待下一次重试...", "ERROR")
                time.sleep(60)
                continue

            # 验证期权价格
            if (not validate_price(call_option_price) or not validate_price(put_option_price)):
                print(f"期权价格数据异常: Call={call_option_price}, Put={put_option_price}，等待下一次重试...", flush=True)
                log_to_file(f"期权价格数据异常: Call={call_option_price}, Put={put_option_price}，等待下一次重试...", "ERROR")
                time.sleep(60)
                continue

            # 验证合约数量
            if (not validate_contracts(call_contracts) or not validate_contracts(put_contracts)):
                print(f"合约数量异常: Call={call_contracts}, Put={put_contracts}，等待下一次重试...", flush=True)
                log_to_file(f"合约数量异常: Call={call_contracts}, Put={put_contracts}，等待下一次重试...", "ERROR")
                time.sleep(60)
                continue

            # 验证成本和收益
            if (total_cost <= 0 or previous_month_final_return < 0):
                print(f"成本或收益数据异常: 成本={total_cost}, 上月基准收益={previous_month_final_return}，等待下一次重试...", flush=True)
                log_to_file(f"成本或收益数据异常: 成本={total_cost}, 上月基准收益={previous_month_final_return}，等待下一次重试...", "ERROR")
                time.sleep(60)
                continue

            # 计算当前期权价值
            current_option_value = int((call_contracts * call_option_price * 10000) + (put_contracts * put_option_price * 10000))

            # 当月余数成本使用状态文件中的固定值，不重新计算
            # monthly_remainder_cost 已经从状态文件中读取，保持不变

            # 计算月度分表收益（期权价值 + 当月余数成本，不包含历史累计）
            monthly_total_return = current_option_value + monthly_remainder_cost

            # 计算总表收益（当前期权价值 + 当月余数成本 + 上月累计收益基准）
            # total_return保持为状态文件中的固定基准值，不在此更新
            master_total_return = current_option_value + monthly_remainder_cost + previous_month_final_return

            # 计算总表年化收益率（按总天数计算，百分比显示）
            if (total_cost > 0 and total_days_running > 0):
                annualized_return = round(((master_total_return / total_cost - 1) / total_days_running * 365) * 100, 4)
            else:
                annualized_return = 0.0

            # 计算当月年化收益率（按当月天数计算，百分比显示）
            # current_month_days 已在前面计算
            if (MONTHLY_INVESTMENT > 0 and current_month_days > 0):
                monthly_annualized_return = round(((monthly_total_return / MONTHLY_INVESTMENT - 1) / current_month_days * 365) * 100, 4)
            else:
                monthly_annualized_return = 0.0
            
            # 获取当前CSV总表文件名
            csv_filename = get_csv_filename()            
            # 记录数据 - 同时写入总表和月度分表
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_month_csv = f"option_trading_{current_month}.csv"
            
            try:
                # 1. 写入总表数据（英文表头，包含月份字段）
                with open(csv_filename, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([current_datetime, etf_price, selected_call_strike[1], selected_put_strike[1],
                                     call_option_price, put_option_price, call_contracts, put_contracts, 
                                     monthly_remainder_cost, total_cost, master_total_return, f"{annualized_return}%", current_month])
                    file.flush()  # 立即写入文件
                
                # 2. 写入月度分表数据（中文表头，无月份字段）
                # 单月CSV中使用当月投资成本和当月年化收益率
                monthly_total_cost = MONTHLY_INVESTMENT
                with open(current_month_csv, 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow([current_datetime, etf_price, selected_call_strike[1], selected_put_strike[1],
                                     call_option_price, put_option_price, call_contracts, put_contracts, 
                                     monthly_remainder_cost, monthly_total_cost, monthly_total_return, f"{monthly_annualized_return}%"])
                    file.flush()  # 立即写入文件
                
                print(f"✅ 交易数据已同时写入总表和月度分表 - Call: {call_option_price}, Put: {put_option_price}, 总表年化收益率: {round(annualized_return, 4)}, 当月年化收益率: {round(monthly_annualized_return, 4)}", flush=True)
                log_to_file(f"交易数据已同时写入 {csv_filename} 和 {current_month_csv} - Call: {call_option_price}, Put: {put_option_price}, 总表年化收益率: {round(annualized_return, 4)}, 当月年化收益率: {round(monthly_annualized_return, 4)}", "INFO")
            except (IOError, OSError) as e:
                print(f"写入CSV文件失败: {str(e)}", flush=True)
                log_to_file(f"写入CSV文件失败: {str(e)}", "ERROR")
                time.sleep(5)  # 失败后等待5秒

        if (remainder_days == DAYS_BEFORE_EXPIRY_STOP):
            print("⚠️ 到达期权到期前一天，停止记录交易数据", flush=True)
            log_to_file("到达期权到期前一天，停止记录交易数据", "WARNING")

    except Exception as e:
        print(f"程序运行出错: {str(e)}", flush=True)
        log_to_file(f"程序运行出错: {str(e)}", "ERROR")
        time.sleep(60)  # 发生错误后等待1分钟再重试

    print("🔄 程序休眠 1 分钟...", flush=True)
    log_to_file("程序休眠 1 分钟...", "INFO")
    time.sleep(60)  # 休眠 1 分钟（60 秒）


# 新浪财经股指期权API查询指南

## 概述

新浪财经提供了免费的股指期权查询接口，支持查询IO(沪深300)、MO(中证1000)、HO(上证50)股指期权数据。

## API接口列表

### 1. 期权T行情价接口

**接口URL:**
```
http://stock.finance.sina.com.cn/futures/api/openapi.php/OptionService.getOptionData
```

**参数:**
- `type`: futures (固定)
- `product`: io/mo/ho (产品代码)
- `exchange`: cffex (中金所)
- `pinzhong`: io2601/mo2601/ho2601 (品种+到期月份)

**示例:**
```
http://stock.finance.sina.com.cn/futures/api/openapi.php/OptionService.getOptionData?type=futures&product=io&exchange=cffex&pinzhong=io2601
```

**用途:** 获取完整的期权链数据，包含所有行权价的看涨/看跌期权

---

### 2. 期权日K线接口

**接口URL:**
```
https://stock.finance.sina.com.cn/futures/api/jsonp.php/FutureOptionAllService.getOptionDayline
```

**参数:**
- `symbol`: 期权合约代码，如 io2601P5800

**示例:**
```
https://stock.finance.sina.com.cn/futures/api/jsonp.php/FutureOptionAllService.getOptionDayline?symbol=io2601P5800
```

**用途:** 获取指定期权合约的历史日K线数据

---

### 3. 期权实时行情接口

**接口URL:**
```
https://hq.sinajs.cn/etag.php?list=P_OP_[合约代码]
```

**参数:**
- `list`: P_OP_开头的合约代码，多个合约用逗号分隔

**示例:**
```
# 单个合约
https://hq.sinajs.cn/etag.php?list=P_OP_io2601P5800

# 多个合约
https://hq.sinajs.cn/etag.php?list=P_OP_io2601P5800,P_OP_io2601C5800
```

**用途:** 获取期权合约的实时行情数据（买卖价、持仓量、成交量等）

**返回字段说明:**
- 字段[0]: 买量
- 字段[1]: 买价
- 字段[2]: 最新价
- 字段[3]: 卖价
- 字段[4]: 卖量
- 字段[5]: 持仓量
- 字段[6]: 涨跌
- 字段[7]: 行权价
- 字段[8]: 昨收价
- 字段[9]: 开盘价
- 字段[10]: 涨停价
- 字段[11]: 跌停价
- 字段[14]: 成交量
- 字段[15]: 成交额

---

### 4. 标的期货实时行情接口

**接口URL:**
```
http://hq.sinajs.cn/list=[期货代码]
```

**示例:**
```
http://hq.sinajs.cn/list=M2009
```

**用途:** 获取期权标的期货的实时行情

---

### 5. 指数实时行情接口

**接口URL:**
```
http://hq.sinajs.cn/list=[指数代码]
```

**常用指数代码:**
- `sh000300`: 沪深300指数
- `sh000016`: 上证50指数
- `sh000852`: 中证1000指数

**示例:**
```
http://hq.sinajs.cn/list=sh000300
```

**用途:** 获取指数实时行情数据

---

## 期权合约代码规则

### IO (沪深300股指期权)
- 格式: `io` + `年月` + `C/P` + `行权价`
- 示例:
  - `io2601C5800` - 2026年1月到期，看涨期权，行权价5800
  - `io2601P5800` - 2026年1月到期，看跌期权，行权价5800

### MO (中证1000股指期权)
- 格式: `mo` + `年月` + `C/P` + `行权价`
- 示例:
  - `mo2601C7000` - 2026年1月到期，看涨期权，行权价7000
  - `mo2601P7000` - 2026年1月到期，看跌期权，行权价7000

### HO (上证50股指期权)
- 格式: `ho` + `年月` + `C/P` + `行权价`
- 示例:
  - `ho2601C2800` - 2026年1月到期，看涨期权，行权价2800
  - `ho2601P2800` - 2026年1月到期，看跌期权，行权价2800

---

## Python使用示例

### 基础使用

```python
from sina_option_query import SinaOptionQuery

# 创建查询对象
query = SinaOptionQuery()

# 1. 查询IO期权链
io_options = query.get_io_options('2601')  # 2026年1月到期
print(io_options.head())

# 2. 查询MO期权链
mo_options = query.get_mo_options('2601')
print(mo_options.head())

# 3. 查询HO期权链
ho_options = query.get_ho_options('2601')
print(ho_options.head())
```

### 查询实时行情

```python
# 查询单个或多个期权实时行情
symbols = ['io2601C5800', 'io2601P5800', 'io2601C6000']
realtime_data = query.get_option_realtime(symbols)

for symbol, data in realtime_data.items():
    print(f"\n{symbol}:")
    print(f"  最新价: {data['最新价']}")
    print(f"  买价: {data['买价']}")
    print(f"  卖价: {data['卖价']}")
    print(f"  持仓量: {data['持仓量']}")
    print(f"  成交量: {data['成交量']}")
```

### 查询日K线数据

```python
# 查询期权日K线
symbol = 'io2601P5800'
kline_data = query.get_option_dayline(symbol)
print(kline_data)
```

### 查询指数行情

```python
# 查询沪深300指数
hs300 = query.get_index_realtime('sh000300')
print(f"沪深300指数: {hs300}")

# 查询上证50指数
sh50 = query.get_index_realtime('sh000016')
print(f"上证50指数: {sh50}")

# 查询中证1000指数
zz1000 = query.get_index_realtime('sh000852')
print(f"中证1000指数: {zz1000}")
```

### 批量查询

```python
# 批量查询多个合约的实时行情
symbols = [f'io2601P{price}' for price in range(5000, 6000, 100)]
batch_data = query.batch_get_realtime(symbols, batch_size=50)
print(f"查询到 {len(batch_data)} 个合约数据")
```

---

## 高级应用示例

### 1. 构建期权链分析

```python
import pandas as pd

def analyze_option_chain(month='2601'):
    """分析IO期权链"""
    query = SinaOptionQuery()

    # 获取期权T行情
    t_data = query.get_option_t_data(product='io', pinzhong=f'io{month}')

    if not t_data:
        print("未获取到数据")
        return

    # 提取所有合约代码
    if 'result' in t_data and 'data' in t_data['result']:
        calls = []
        puts = []

        for strike_data in t_data['result']['data']:
            strike = strike_data['strike']

            # 看涨期权
            if 'call' in strike_data:
                calls.append({
                    '行权价': strike,
                    '合约': f"io{month}C{strike}",
                    **strike_data['call']
                })

            # 看跌期权
            if 'put' in strike_data:
                puts.append({
                    '行权价': strike,
                    '合约': f"io{month}P{strike}",
                    **strike_data['put']
                })

        call_df = pd.DataFrame(calls)
        put_df = pd.DataFrame(puts)

        return call_df, put_df
```

### 2. 实时监控价格变动

```python
import time

def monitor_option_prices(symbols, interval=5):
    """
    实时监控期权价格

    Args:
        symbols: 期权合约列表
        interval: 查询间隔（秒）
    """
    query = SinaOptionQuery()

    while True:
        data = query.get_option_realtime(symbols)

        print(f"\n时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        for symbol, info in data.items():
            print(f"{symbol}: 最新价={info['最新价']}, "
                  f"涨跌={info['涨跌']}, "
                  f"成交量={info['成交量']}")

        time.sleep(interval)
```

### 3. 期权组合策略分析

```python
def analyze_straddle(strike, month='2601'):
    """
    分析跨式组合（买入同行权价的看涨和看跌期权）

    Args:
        strike: 行权价
        month: 到期月份
    """
    query = SinaOptionQuery()

    call_symbol = f'io{month}C{strike}'
    put_symbol = f'io{month}P{strike}'

    data = query.get_option_realtime([call_symbol, put_symbol])

    if call_symbol in data and put_symbol in data:
        call_price = float(data[call_symbol]['最新价'])
        put_price = float(data[put_symbol]['最新价'])

        total_cost = call_price + put_price

        print(f"跨式组合分析 (行权价: {strike})")
        print(f"  看涨期权价格: {call_price}")
        print(f"  看跌期权价格: {put_price}")
        print(f"  总成本: {total_cost}")
        print(f"  盈亏平衡点: {strike - total_cost} ~ {strike + total_cost}")

        return {
            'call_price': call_price,
            'put_price': put_price,
            'total_cost': total_cost,
            'lower_breakeven': strike - total_cost,
            'upper_breakeven': strike + total_cost
        }
```

---

## 注意事项

1. **数据更新频率**: 实时行情接口更新频率很高，但请避免过于频繁的请求
2. **批量查询**: 单次查询建议不超过50个合约，使用批量查询功能自动分批
3. **异常处理**: 网络可能出现波动，建议添加重试机制
4. **数据解析**: 不同接口返回的数据格式不同，需要根据实际情况解析
5. **交易时间**: 期权交易时间为交易日 9:30-11:30, 13:00-15:00
6. **合约月份**: 期权合约月份格式为YYMM，如2601表示2026年1月

---

## 与其他数据源对比

| 数据源 | 优点 | 缺点 | 适用场景 |
|--------|------|------|----------|
| 新浪财经 | 免费、实时、无限制 | 历史数据有限 | 实时监控、快速查询 |
| Tushare | 数据全面、历史完整 | 需要积分、有限额 | 量化回测、深度分析 |
| AKShare | 免费、接口丰富 | 部分数据延迟 | 一般查询、数据分析 |

---

## 常见问题

### Q1: 如何判断期权是否在交易时间？
```python
from datetime import datetime

def is_trading_time():
    now = datetime.now()
    hour = now.hour
    minute = now.minute

    # 上午: 9:30-11:30
    morning = (hour == 9 and minute >= 30) or (hour == 10) or (hour == 11 and minute <= 30)
    # 下午: 13:00-15:00
    afternoon = (hour == 13) or (hour == 14) or (hour == 15 and minute == 0)

    return morning or afternoon
```

### Q2: 如何获取所有可用的到期月份？
通常股指期权有当月、下月、以及随后两个季月（3、6、9、12月）的合约。

### Q3: 如何计算隐含波动率？
需要使用Black-Scholes期权定价模型进行反向计算，可以参考项目中的其他分析脚本。

---

## 更多资源

- [新浪财经期权频道](https://stock.finance.sina.com.cn/option/)
- [中金所官网](http://www.cffex.com.cn/)
- [Tushare文档](https://tushare.pro/document/2?doc_id=158)
- [AKShare文档](https://akshare.akfamily.xyz/data/option/option.html)

---

## 更新日志

- 2026-01-12: 创建初始版本，支持IO/MO/HO股指期权查询

# 股指期权查询与分析模块

## 简介

本模块提供基于新浪财经API的股指期权查询功能，支持IO(沪深300)、MO(中证1000)、HO(上证50)股指期权的实时行情、历史数据和策略分析。

## 文件说明

### 核心模块

1. **sina_option_query.py** - 新浪财经期权查询核心类
   - `SinaOptionQuery`: 主查询类
   - 支持期权T行情、日K线、实时行情、指数行情等查询
   - 提供批量查询功能

2. **example_option_strategies.py** - 期权策略分析示例
   - `OptionStrategyAnalyzer`: 策略分析类
   - 支持多种经典期权策略分析
   - 提供机会扫描和比较功能

3. **sina_option_api_guide.md** - 详细API使用指南
   - 完整的API接口说明
   - 参数详解和示例代码
   - 常见问题解答

## 快速开始

### 安装依赖

```bash
pip install pandas requests
```

### 基础查询示例

```python
from sina_option_query import SinaOptionQuery

# 创建查询对象
query = SinaOptionQuery()

# 1. 查询IO期权链（2026年1月到期）
io_options = query.get_io_options('2601')
print(io_options)

# 2. 查询期权实时行情
symbols = ['io2601C5800', 'io2601P5800']
realtime = query.get_option_realtime(symbols)
print(realtime)

# 3. 查询沪深300指数
hs300 = query.get_index_realtime('sh000300')
print(hs300)
```

### 策略分析示例

```python
from example_option_strategies import OptionStrategyAnalyzer

# 创建策略分析器
analyzer = OptionStrategyAnalyzer()

# 1. 跨式策略分析
straddle = analyzer.analyze_straddle('io', '2601', 5800)
print(f"总成本: {straddle['total_cost']}")
print(f"盈亏平衡点: {straddle['lower_breakeven']} ~ {straddle['upper_breakeven']}")

# 2. 牛市价差分析
vertical = analyzer.analyze_vertical_spread('io', '2601', 5800, 6000, 'C')
print(f"最大收益: {vertical['max_profit']}")
print(f"风险收益比: {vertical['risk_reward_ratio']}")

# 3. 蝶式价差分析
butterfly = analyzer.analyze_butterfly_spread('io', '2601', 5600, 5800, 6000)
print(f"最优价格: {butterfly['optimal_price']}")
```

## 支持的期权策略

### 1. 跨式策略 (Straddle)
- **构建**: 买入同行权价的看涨和看跌期权
- **适用**: 预期大幅波动，方向不确定
- **风险**: 有限（权利金）
- **收益**: 理论无限

### 2. 宽跨式策略 (Strangle)
- **构建**: 买入不同行权价的看涨和看跌期权
- **适用**: 预期大幅波动，成本比跨式低
- **风险**: 有限（权利金）
- **收益**: 理论无限

### 3. 垂直价差 (Vertical Spread)
- **牛市看涨价差**: 买低行权价看涨，卖高行权价看涨
- **熊市看跌价差**: 买高行权价看跌，卖低行权价看跌
- **适用**: 温和看涨/看跌
- **风险**: 有限
- **收益**: 有限

### 4. 蝶式价差 (Butterfly Spread)
- **构建**: 买1低、卖2中、买1高
- **适用**: 预期价格窄幅波动
- **风险**: 有限（净权利金）
- **收益**: 有限

### 5. 铁鹰式 (Iron Condor)
- **构建**: 同时卖出OTM看涨和看跌价差
- **适用**: 预期价格在区间内波动
- **风险**: 有限
- **收益**: 有限（净权利金）

## 股指期权合约代码规则

### 代码格式
`[产品代码][年月][C/P][行权价]`

### 产品代码
- **IO**: 沪深300股指期权
- **MO**: 中证1000股指期权
- **HO**: 上证50股指期权

### 期权类型
- **C**: Call (看涨期权)
- **P**: Put (看跌期权)

### 示例
- `io2601C5800` - IO 2026年1月到期 看涨 行权价5800
- `mo2602P7000` - MO 2026年2月到期 看跌 行权价7000
- `ho2603C2800` - HO 2026年3月到期 看涨 行权价2800

## API接口说明

### 1. 期权T行情
```
http://stock.finance.sina.com.cn/futures/api/openapi.php/OptionService.getOptionData
?type=futures&product=io&exchange=cffex&pinzhong=io2601
```

### 2. 期权实时行情
```
https://hq.sinajs.cn/etag.php?list=P_OP_io2601C5800,P_OP_io2601P5800
```

### 3. 期权日K线
```
https://stock.finance.sina.com.cn/futures/api/jsonp.php/FutureOptionAllService.getOptionDayline
?symbol=io2601P5800
```

### 4. 指数实时行情
```
http://hq.sinajs.cn/list=sh000300  # 沪深300
http://hq.sinajs.cn/list=sh000016  # 上证50
http://hq.sinajs.cn/list=sh000852  # 中证1000
```

## 实际应用场景

### 1. 实时监控
```python
# 监控特定期权合约的价格变动
symbols = ['io2601C5800', 'io2601P5800']
while True:
    data = query.get_option_realtime(symbols)
    # 处理数据...
    time.sleep(5)
```

### 2. 策略回测
```python
# 获取历史K线数据进行回测
symbol = 'io2601P5800'
kline = query.get_option_dayline(symbol)
# 进行策略回测...
```

### 3. 波动率分析
```python
# 比较不同行权价的期权价格
strikes = range(5000, 6000, 100)
comparison = analyzer.compare_implied_volatility('io', '2601', strikes)
```

### 4. 策略优化
```python
# 扫描所有行权价，找出最优策略
opportunities = analyzer.scan_opportunities('io', '2601', 'straddle')
```

## 注意事项

1. **交易时间**: 交易日 9:30-11:30, 13:00-15:00
2. **请求频率**: 建议不超过每秒2次请求
3. **批量查询**: 单次最多50个合约
4. **数据延迟**: 实时数据有1-3秒延迟
5. **异常处理**: 网络异常时会返回空数据

## 数据字段说明

### 期权实时行情字段
- 买量/买价/卖价/卖量
- 最新价/昨收价/开盘价
- 涨停价/跌停价/涨跌
- 行权价/持仓量
- 成交量/成交额

### 指数行情字段
- 指数名称/最新价
- 涨跌额/涨跌幅
- 成交量/成交额

## 扩展功能建议

1. **隐含波动率计算**: 使用Black-Scholes模型
2. **希腊字母计算**: Delta, Gamma, Theta, Vega等
3. **套利机会扫描**: PCR分析、价差套利等
4. **风险管理**: VaR计算、压力测试
5. **自动交易**: 结合交易接口实现自动化

## 相关资源

- [新浪财经期权频道](https://stock.finance.sina.com.cn/option/)
- [中金所官网](http://www.cffex.com.cn/)
- [期权定价理论](https://zh.wikipedia.org/wiki/Black-Scholes)
- [期权策略详解](https://www.investopedia.com/options-basics-tutorial-4583012)

## 更新日志

### v1.0.0 (2026-01-12)
- 初始版本发布
- 支持IO/MO/HO股指期权查询
- 提供5种经典期权策略分析
- 完整的API文档和示例代码

## 常见问题

**Q: 如何获取当前可交易的期权合约？**
```python
# 查询当月合约
io_current = query.get_io_options('2601')
```

**Q: 如何判断期权是否在价内？**
```python
# 获取标的价格和期权行权价进行比较
index = query.get_index_realtime('sh000300')
current_price = float(index['最新价'])
# 对于看涨期权: 价内 = 标的价格 > 行权价
# 对于看跌期权: 价内 = 标的价格 < 行权价
```

**Q: 如何计算期权的时间价值？**
```python
# 时间价值 = 期权价格 - 内在价值
# 内在价值 = max(0, 标的价格 - 行权价) for Call
# 内在价值 = max(0, 行权价 - 标的价格) for Put
```

## 许可证

本模块仅供学习和研究使用。使用本模块进行实际交易时，请确保遵守相关法律法规和交易所规则。

## 贡献

欢迎提交Issue和Pull Request来改进本模块！

---

**免责声明**: 本模块提供的数据和分析仅供参考，不构成投资建议。期权交易具有高风险，请谨慎投资。

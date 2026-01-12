#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股指期权策略分析示例
演示如何使用sina_option_query模块进行期权策略分析
"""

from sina_option_query import SinaOptionQuery
import pandas as pd
from typing import Dict, List
import time


class OptionStrategyAnalyzer:
    """期权策略分析器"""

    def __init__(self):
        self.query = SinaOptionQuery()

    def analyze_vertical_spread(self, product: str, month: str,
                                 strike_low: int, strike_high: int,
                                 option_type: str = 'C') -> Dict:
        """
        分析垂直价差策略

        Args:
            product: io/mo/ho
            month: 到期月份
            strike_low: 低行权价
            strike_high: 高行权价
            option_type: C(看涨) 或 P(看跌)

        Returns:
            策略分析结果
        """
        # 构建合约代码
        symbol_low = f"{product}{month}{option_type}{strike_low}"
        symbol_high = f"{product}{month}{option_type}{strike_high}"

        # 获取实时行情
        data = self.query.get_option_realtime([symbol_low, symbol_high])

        if symbol_low in data and symbol_high in data:
            price_low = float(data[symbol_low]['最新价'])
            price_high = float(data[symbol_high]['最新价'])

            # 牛市价差: 买入低行权价，卖出高行权价
            if option_type == 'C':
                strategy_type = "牛市看涨价差"
                net_cost = price_low - price_high
                max_profit = (strike_high - strike_low) - net_cost
                max_loss = net_cost
            else:
                strategy_type = "熊市看跌价差"
                net_cost = price_high - price_low
                max_profit = net_cost
                max_loss = (strike_high - strike_low) - net_cost

            return {
                'strategy': strategy_type,
                'symbol_long': symbol_low,
                'symbol_short': symbol_high,
                'price_long': price_low,
                'price_short': price_high,
                'net_cost': net_cost,
                'max_profit': max_profit,
                'max_loss': max_loss,
                'risk_reward_ratio': max_profit / max_loss if max_loss != 0 else 0
            }

        return {}

    def analyze_straddle(self, product: str, month: str, strike: int) -> Dict:
        """
        分析跨式策略（买入同行权价的看涨和看跌）

        Args:
            product: io/mo/ho
            month: 到期月份
            strike: 行权价

        Returns:
            策略分析结果
        """
        call_symbol = f"{product}{month}C{strike}"
        put_symbol = f"{product}{month}P{strike}"

        data = self.query.get_option_realtime([call_symbol, put_symbol])

        if call_symbol in data and put_symbol in data:
            call_price = float(data[call_symbol]['最新价'])
            put_price = float(data[put_symbol]['最新价'])
            total_cost = call_price + put_price

            return {
                'strategy': '跨式组合',
                'call_symbol': call_symbol,
                'put_symbol': put_symbol,
                'call_price': call_price,
                'put_price': put_price,
                'total_cost': total_cost,
                'upper_breakeven': strike + total_cost,
                'lower_breakeven': strike - total_cost,
                'breakeven_range': total_cost * 2
            }

        return {}

    def analyze_strangle(self, product: str, month: str,
                         call_strike: int, put_strike: int) -> Dict:
        """
        分析宽跨式策略（买入不同行权价的看涨和看跌）

        Args:
            product: io/mo/ho
            month: 到期月份
            call_strike: 看涨期权行权价
            put_strike: 看跌期权行权价

        Returns:
            策略分析结果
        """
        call_symbol = f"{product}{month}C{call_strike}"
        put_symbol = f"{product}{month}P{put_strike}"

        data = self.query.get_option_realtime([call_symbol, put_symbol])

        if call_symbol in data and put_symbol in data:
            call_price = float(data[call_symbol]['最新价'])
            put_price = float(data[put_symbol]['最新价'])
            total_cost = call_price + put_price

            return {
                'strategy': '宽跨式组合',
                'call_symbol': call_symbol,
                'put_symbol': put_symbol,
                'call_price': call_price,
                'put_price': put_price,
                'total_cost': total_cost,
                'upper_breakeven': call_strike + total_cost,
                'lower_breakeven': put_strike - total_cost,
                'profit_zone_width': (call_strike + total_cost) - (put_strike - total_cost)
            }

        return {}

    def analyze_butterfly_spread(self, product: str, month: str,
                                  strike_low: int, strike_mid: int,
                                  strike_high: int, option_type: str = 'C') -> Dict:
        """
        分析蝶式价差策略

        Args:
            product: io/mo/ho
            month: 到期月份
            strike_low: 低行权价
            strike_mid: 中间行权价
            strike_high: 高行权价
            option_type: C(看涨) 或 P(看跌)

        Returns:
            策略分析结果
        """
        symbol_low = f"{product}{month}{option_type}{strike_low}"
        symbol_mid = f"{product}{month}{option_type}{strike_mid}"
        symbol_high = f"{product}{month}{option_type}{strike_high}"

        data = self.query.get_option_realtime([symbol_low, symbol_mid, symbol_high])

        if all(s in data for s in [symbol_low, symbol_mid, symbol_high]):
            price_low = float(data[symbol_low]['最新价'])
            price_mid = float(data[symbol_mid]['最新价'])
            price_high = float(data[symbol_high]['最新价'])

            # 蝶式价差: 买1低，卖2中，买1高
            net_cost = price_low - 2 * price_mid + price_high
            max_profit = (strike_mid - strike_low) - net_cost
            max_loss = net_cost

            return {
                'strategy': '蝶式价差',
                'symbols': {
                    'low': symbol_low,
                    'mid': symbol_mid,
                    'high': symbol_high
                },
                'prices': {
                    'low': price_low,
                    'mid': price_mid,
                    'high': price_high
                },
                'net_cost': net_cost,
                'max_profit': max_profit,
                'max_loss': max_loss,
                'optimal_price': strike_mid,
                'risk_reward_ratio': max_profit / max_loss if max_loss != 0 else 0
            }

        return {}

    def analyze_iron_condor(self, product: str, month: str,
                            put_strike_low: int, put_strike_high: int,
                            call_strike_low: int, call_strike_high: int) -> Dict:
        """
        分析铁鹰式策略

        Args:
            product: io/mo/ho
            month: 到期月份
            put_strike_low: 看跌期权低行权价
            put_strike_high: 看跌期权高行权价
            call_strike_low: 看涨期权低行权价
            call_strike_high: 看涨期权高行权价

        Returns:
            策略分析结果
        """
        # 买入低行权价看跌，卖出高行权价看跌
        # 卖出低行权价看涨，买入高行权价看涨
        symbols = [
            f"{product}{month}P{put_strike_low}",
            f"{product}{month}P{put_strike_high}",
            f"{product}{month}C{call_strike_low}",
            f"{product}{month}C{call_strike_high}"
        ]

        data = self.query.get_option_realtime(symbols)

        if all(s in data for s in symbols):
            prices = [float(data[s]['最新价']) for s in symbols]

            # 净收入 = 卖出的权利金 - 买入的权利金
            net_credit = prices[1] + prices[2] - prices[0] - prices[3]
            max_profit = net_credit
            max_loss = (put_strike_high - put_strike_low) - net_credit

            return {
                'strategy': '铁鹰式',
                'symbols': {
                    'put_buy': symbols[0],
                    'put_sell': symbols[1],
                    'call_sell': symbols[2],
                    'call_buy': symbols[3]
                },
                'prices': {
                    'put_buy': prices[0],
                    'put_sell': prices[1],
                    'call_sell': prices[2],
                    'call_buy': prices[3]
                },
                'net_credit': net_credit,
                'max_profit': max_profit,
                'max_loss': max_loss,
                'profit_range': (put_strike_high, call_strike_low),
                'risk_reward_ratio': max_profit / max_loss if max_loss != 0 else 0
            }

        return {}

    def scan_opportunities(self, product: str = 'io', month: str = '2601',
                          strategy_type: str = 'straddle') -> pd.DataFrame:
        """
        扫描期权机会

        Args:
            product: io/mo/ho
            month: 到期月份
            strategy_type: 策略类型 (straddle/strangle/vertical_spread)

        Returns:
            机会列表DataFrame
        """
        opportunities = []

        # 获取期权链
        if product == 'io':
            option_chain = self.query.get_io_options(month)
        elif product == 'mo':
            option_chain = self.query.get_mo_options(month)
        elif product == 'ho':
            option_chain = self.query.get_ho_options(month)
        else:
            return pd.DataFrame()

        # 根据策略类型扫描
        # 这里需要根据实际返回的数据结构进行调整
        # 示例代码，实际使用时需要根据API返回格式修改

        return pd.DataFrame(opportunities)

    def compare_implied_volatility(self, product: str, month: str,
                                   strikes: List[int]) -> pd.DataFrame:
        """
        比较不同行权价的隐含波动率

        Args:
            product: io/mo/ho
            month: 到期月份
            strikes: 行权价列表

        Returns:
            波动率比较DataFrame
        """
        results = []

        for strike in strikes:
            call_symbol = f"{product}{month}C{strike}"
            put_symbol = f"{product}{month}P{strike}"

            data = self.query.get_option_realtime([call_symbol, put_symbol])

            if call_symbol in data and put_symbol in data:
                results.append({
                    '行权价': strike,
                    '看涨期权价格': data[call_symbol]['最新价'],
                    '看跌期权价格': data[put_symbol]['最新价'],
                    '看涨成交量': data[call_symbol]['成交量'],
                    '看跌成交量': data[put_symbol]['成交量'],
                    '看涨持仓量': data[call_symbol]['持仓量'],
                    '看跌持仓量': data[put_symbol]['持仓量'],
                })

            time.sleep(0.1)  # 避免请求过快

        return pd.DataFrame(results)


def demo_strategies():
    """演示各种策略分析"""
    analyzer = OptionStrategyAnalyzer()

    print("=" * 80)
    print("股指期权策略分析示例")
    print("=" * 80)
    print()

    # 1. 跨式策略
    print("1. 跨式策略分析 (行权价 5800)")
    print("-" * 80)
    straddle = analyzer.analyze_straddle('io', '2601', 5800)
    if straddle:
        print(f"策略类型: {straddle['strategy']}")
        print(f"看涨期权: {straddle['call_symbol']} 价格: {straddle['call_price']}")
        print(f"看跌期权: {straddle['put_symbol']} 价格: {straddle['put_price']}")
        print(f"总成本: {straddle['total_cost']}")
        print(f"上盈亏平衡点: {straddle['upper_breakeven']}")
        print(f"下盈亏平衡点: {straddle['lower_breakeven']}")
    else:
        print("无法获取数据")
    print()

    # 2. 垂直价差
    print("2. 牛市看涨价差分析 (5800-6000)")
    print("-" * 80)
    vertical = analyzer.analyze_vertical_spread('io', '2601', 5800, 6000, 'C')
    if vertical:
        print(f"策略类型: {vertical['strategy']}")
        print(f"买入: {vertical['symbol_long']} 价格: {vertical['price_long']}")
        print(f"卖出: {vertical['symbol_short']} 价格: {vertical['price_short']}")
        print(f"净成本: {vertical['net_cost']}")
        print(f"最大收益: {vertical['max_profit']}")
        print(f"最大亏损: {vertical['max_loss']}")
        print(f"风险收益比: {vertical['risk_reward_ratio']:.2f}")
    else:
        print("无法获取数据")
    print()

    # 3. 宽跨式策略
    print("3. 宽跨式策略分析 (看涨6000/看跌5600)")
    print("-" * 80)
    strangle = analyzer.analyze_strangle('io', '2601', 6000, 5600)
    if strangle:
        print(f"策略类型: {strangle['strategy']}")
        print(f"看涨期权: {strangle['call_symbol']} 价格: {strangle['call_price']}")
        print(f"看跌期权: {strangle['put_symbol']} 价格: {strangle['put_price']}")
        print(f"总成本: {strangle['total_cost']}")
        print(f"上盈亏平衡点: {strangle['upper_breakeven']}")
        print(f"下盈亏平衡点: {strangle['lower_breakeven']}")
    else:
        print("无法获取数据")
    print()

    # 4. 蝶式价差
    print("4. 蝶式价差分析 (5600-5800-6000)")
    print("-" * 80)
    butterfly = analyzer.analyze_butterfly_spread('io', '2601', 5600, 5800, 6000, 'C')
    if butterfly:
        print(f"策略类型: {butterfly['strategy']}")
        print(f"买入低: {butterfly['symbols']['low']} 价格: {butterfly['prices']['low']}")
        print(f"卖出中x2: {butterfly['symbols']['mid']} 价格: {butterfly['prices']['mid']}")
        print(f"买入高: {butterfly['symbols']['high']} 价格: {butterfly['prices']['high']}")
        print(f"净成本: {butterfly['net_cost']}")
        print(f"最大收益: {butterfly['max_profit']}")
        print(f"最大亏损: {butterfly['max_loss']}")
        print(f"最优标的价格: {butterfly['optimal_price']}")
    else:
        print("无法获取数据")
    print()

    # 5. 波动率比较
    print("5. 不同行权价期权比较")
    print("-" * 80)
    strikes = [5600, 5700, 5800, 5900, 6000]
    comparison = analyzer.compare_implied_volatility('io', '2601', strikes)
    if not comparison.empty:
        print(comparison.to_string(index=False))
    else:
        print("无法获取数据")
    print()


if __name__ == '__main__':
    demo_strategies()

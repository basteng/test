#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新浪财经股指期权查询模块
支持查询IO(沪深300)、MO(中证1000)、HO(上证50)股指期权数据
"""

import requests
import json
import pandas as pd
from typing import List, Dict, Optional
import time


class SinaOptionQuery:
    """新浪财经期权数据查询类"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def get_option_t_data(self, product: str = 'io', exchange: str = 'cffex',
                          pinzhong: str = 'io2012') -> Dict:
        """
        获取期权T行情价

        Args:
            product: 产品代码 (io: 沪深300, mo: 中证1000, ho: 上证50)
            exchange: 交易所 (cffex: 中金所)
            pinzhong: 品种代码，如 io2012, mo2601 等

        Returns:
            期权T行情数据字典
        """
        url = (f"http://stock.finance.sina.com.cn/futures/api/openapi.php/"
               f"OptionService.getOptionData")
        params = {
            'type': 'futures',
            'product': product,
            'exchange': exchange,
            'pinzhong': pinzhong
        }

        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"获取期权T行情数据失败: {e}")
            return {}

    def get_option_dayline(self, symbol: str) -> Dict:
        """
        获取期权日K线数据

        Args:
            symbol: 期权合约代码，如 io2012P4000

        Returns:
            期权日K线数据字典
        """
        url = (f"https://stock.finance.sina.com.cn/futures/api/jsonp.php/"
               f"FutureOptionAllService.getOptionDayline")
        params = {'symbol': symbol}

        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            # 处理JSONP返回，去除函数包装
            text = response.text
            if '(' in text and ')' in text:
                text = text[text.find('(')+1:text.rfind(')')]
            return json.loads(text)
        except Exception as e:
            print(f"获取期权日K线数据失败: {e}")
            return {}

    def get_option_realtime(self, symbols: List[str]) -> Dict:
        """
        获取期权实时行情（支持多个合约）

        Args:
            symbols: 期权合约代码列表，如 ['io2012P4000', 'io2012P3900']

        Returns:
            期权实时行情数据字典
        """
        # 构建查询列表，添加P_OP_前缀
        symbol_list = ','.join([f'P_OP_{s}' for s in symbols])
        url = f"https://hq.sinajs.cn/etag.php?list={symbol_list}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return self._parse_realtime_data(response.text, symbols)
        except Exception as e:
            print(f"获取期权实时行情失败: {e}")
            return {}

    def get_underlying_realtime(self, symbol: str) -> Dict:
        """
        获取标的（期货）实时行情

        Args:
            symbol: 期货合约代码，如 M2009（对应IF2009等）

        Returns:
            期货实时行情数据字典
        """
        url = f"http://hq.sinajs.cn/list={symbol}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return self._parse_underlying_data(response.text, symbol)
        except Exception as e:
            print(f"获取标的实时行情失败: {e}")
            return {}

    def get_index_realtime(self, index_code: str = 'sh000300') -> Dict:
        """
        获取指数实时行情

        Args:
            index_code: 指数代码
                - sh000300: 沪深300指数
                - sh000016: 上证50指数
                - sh000852: 中证1000指数

        Returns:
            指数实时行情数据字典
        """
        url = f"http://hq.sinajs.cn/list={index_code}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return self._parse_index_data(response.text, index_code)
        except Exception as e:
            print(f"获取指数实时行情失败: {e}")
            return {}

    def _parse_realtime_data(self, text: str, symbols: List[str]) -> Dict:
        """解析期权实时行情数据"""
        result = {}
        lines = text.strip().split('\n')

        for i, line in enumerate(lines):
            if 'hq_str_P_OP_' in line:
                # 提取数据部分
                data_str = line.split('"')[1]
                fields = data_str.split(',')

                if len(fields) >= 40:  # 确保有足够的字段
                    symbol = symbols[i] if i < len(symbols) else 'unknown'
                    result[symbol] = {
                        '买量': fields[0],
                        '买价': fields[1],
                        '最新价': fields[2],
                        '卖价': fields[3],
                        '卖量': fields[4],
                        '持仓量': fields[5],
                        '涨跌': fields[6],
                        '行权价': fields[7],
                        '昨收价': fields[8],
                        '开盘价': fields[9],
                        '涨停价': fields[10],
                        '跌停价': fields[11],
                        '成交量': fields[14],
                        '成交额': fields[15],
                    }

        return result

    def _parse_underlying_data(self, text: str, symbol: str) -> Dict:
        """解析标的期货实时行情数据"""
        if 'hq_str_' not in text:
            return {}

        data_str = text.split('"')[1]
        fields = data_str.split(',')

        if len(fields) >= 8:
            return {
                'symbol': symbol,
                '最新价': fields[0],
                '昨收价': fields[1],
                '开盘价': fields[2],
                '最高价': fields[3],
                '最低价': fields[4],
                '成交量': fields[6],
                '成交额': fields[7],
            }
        return {}

    def _parse_index_data(self, text: str, index_code: str) -> Dict:
        """解析指数实时行情数据"""
        if 'hq_str_' not in text:
            return {}

        data_str = text.split('"')[1]
        fields = data_str.split(',')

        if len(fields) >= 6:
            return {
                'index_code': index_code,
                '指数名称': fields[0],
                '最新价': fields[1],
                '涨跌额': fields[2],
                '涨跌幅': fields[3],
                '成交量': fields[4],
                '成交额': fields[5],
            }
        return {}

    def get_io_options(self, month: str = '2601') -> pd.DataFrame:
        """
        获取IO(沪深300)股指期权链

        Args:
            month: 到期月份，如 '2601' 表示2026年1月

        Returns:
            期权链DataFrame
        """
        pinzhong = f'io{month}'
        data = self.get_option_t_data(product='io', pinzhong=pinzhong)

        if data and 'result' in data:
            return self._convert_to_dataframe(data['result'])
        return pd.DataFrame()

    def get_mo_options(self, month: str = '2601') -> pd.DataFrame:
        """
        获取MO(中证1000)股指期权链

        Args:
            month: 到期月份，如 '2601' 表示2026年1月

        Returns:
            期权链DataFrame
        """
        pinzhong = f'mo{month}'
        data = self.get_option_t_data(product='mo', pinzhong=pinzhong)

        if data and 'result' in data:
            return self._convert_to_dataframe(data['result'])
        return pd.DataFrame()

    def get_ho_options(self, month: str = '2601') -> pd.DataFrame:
        """
        获取HO(上证50)股指期权链

        Args:
            month: 到期月份，如 '2601' 表示2026年1月

        Returns:
            期权链DataFrame
        """
        pinzhong = f'ho{month}'
        data = self.get_option_t_data(product='ho', pinzhong=pinzhong)

        if data and 'result' in data:
            return self._convert_to_dataframe(data['result'])
        return pd.DataFrame()

    def _convert_to_dataframe(self, data: Dict) -> pd.DataFrame:
        """将期权数据转换为DataFrame"""
        if not data:
            return pd.DataFrame()

        # 这里需要根据实际返回的数据结构进行调整
        try:
            df = pd.DataFrame(data)
            return df
        except Exception as e:
            print(f"转换DataFrame失败: {e}")
            return pd.DataFrame()

    def batch_get_realtime(self, symbols: List[str], batch_size: int = 50) -> Dict:
        """
        批量获取期权实时行情（自动分批）

        Args:
            symbols: 期权合约代码列表
            batch_size: 每批查询的数量

        Returns:
            所有期权实时行情数据字典
        """
        result = {}

        for i in range(0, len(symbols), batch_size):
            batch = symbols[i:i+batch_size]
            batch_result = self.get_option_realtime(batch)
            result.update(batch_result)

            # 避免请求过快
            if i + batch_size < len(symbols):
                time.sleep(0.5)

        return result


def main():
    """示例用法"""
    query = SinaOptionQuery()

    print("=" * 80)
    print("1. 查询沪深300股指期权(IO)2601合约")
    print("=" * 80)
    io_data = query.get_io_options('2601')
    print(f"IO期权链数据: {len(io_data)} 条记录")
    if not io_data.empty:
        print(io_data.head())
    print()

    print("=" * 80)
    print("2. 查询期权实时行情")
    print("=" * 80)
    # 示例合约代码
    symbols = ['io2601C5800', 'io2601P5800']
    realtime_data = query.get_option_realtime(symbols)
    for symbol, data in realtime_data.items():
        print(f"\n{symbol}:")
        for key, value in data.items():
            print(f"  {key}: {value}")
    print()

    print("=" * 80)
    print("3. 查询沪深300指数实时行情")
    print("=" * 80)
    index_data = query.get_index_realtime('sh000300')
    print("沪深300指数:")
    for key, value in index_data.items():
        print(f"  {key}: {value}")
    print()

    print("=" * 80)
    print("4. 查询中证1000股指期权(MO)2601合约")
    print("=" * 80)
    mo_data = query.get_mo_options('2601')
    print(f"MO期权链数据: {len(mo_data)} 条记录")
    if not mo_data.empty:
        print(mo_data.head())
    print()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
半导体设备公司市值对比分析
对比北方华创、Applied Materials (AMAT)、Tokyo Electron (TEL) 的市值
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import os

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 股票代码
NAURA_TICKER = "002371.SZ"  # 北方华创
AMAT_TICKER = "AMAT"        # Applied Materials
TEL_TICKER = "8035.T"       # Tokyo Electron

# 汇率代码
USDCNY_TICKER = "USDCNY=X"  # 美元/人民币
USDJPY_TICKER = "JPY=X"     # 美元/日元

# 如果需要代理，取消注释并设置
# os.environ['HTTP_PROXY'] = 'http://your-proxy:port'
# os.environ['HTTPS_PROXY'] = 'http://your-proxy:port'


def fetch_stock_data(ticker, start_date, end_date, max_retries=3):
    """获取股票历史数据，带重试机制"""
    for attempt in range(max_retries):
        try:
            print(f"正在获取 {ticker} 的数据... (尝试 {attempt + 1}/{max_retries})")
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            if not df.empty:
                print(f"✓ 成功获取 {ticker} 的 {len(df)} 条数据")
                return df
            else:
                print(f"警告: {ticker} 返回空数据")
        except Exception as e:
            print(f"✗ 获取 {ticker} 失败: {e}")
            if attempt < max_retries - 1:
                print(f"  等待后重试...")
                import time
                time.sleep(2 ** attempt)  # 指数退避
    return pd.DataFrame()


def fetch_exchange_rate(ticker, start_date, end_date, max_retries=3):
    """获取汇率数据，带重试机制"""
    for attempt in range(max_retries):
        try:
            print(f"正在获取汇率数据 {ticker}... (尝试 {attempt + 1}/{max_retries})")
            rate = yf.Ticker(ticker)
            df = rate.history(start=start_date, end=end_date)
            if not df.empty:
                print(f"✓ 成功获取汇率数据")
                return df
        except Exception as e:
            print(f"✗ 获取汇率 {ticker} 失败: {e}")
            if attempt < max_retries - 1:
                print(f"  等待后重试...")
                import time
                time.sleep(2 ** attempt)
    return pd.DataFrame()


def get_market_cap_series(ticker, start_date, end_date):
    """获取市值时间序列（美元）"""
    stock = yf.Ticker(ticker)

    # 获取股价数据
    hist = stock.history(start=start_date, end=end_date)

    if hist.empty:
        print(f"警告: {ticker} 没有数据")
        return pd.Series(dtype=float)

    # 获取股本信息（总股本）
    try:
        shares = stock.info.get('sharesOutstanding', None)
        if shares is None:
            print(f"警告: 无法获取 {ticker} 的总股本，尝试使用市值数据")
            # 如果无法获取股本，尝试直接使用市值
            current_market_cap = stock.info.get('marketCap', None)
            if current_market_cap and not hist.empty:
                # 用当前市值和股价反推股本
                current_price = hist['Close'].iloc[-1]
                shares = current_market_cap / current_price
            else:
                return pd.Series(dtype=float)
    except Exception as e:
        print(f"获取 {ticker} 信息时出错: {e}")
        return pd.Series(dtype=float)

    # 计算市值（本币）
    market_cap_local = hist['Close'] * shares

    return market_cap_local, hist['Close']


def main():
    # 设置时间范围（最近2年）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)

    print(f"\n分析时间范围: {start_date.date()} 至 {end_date.date()}\n")
    print("=" * 60)

    # 获取汇率数据
    print("\n获取汇率数据...")
    usdcny = fetch_exchange_rate(USDCNY_TICKER, start_date, end_date)
    usdjpy = fetch_exchange_rate(USDJPY_TICKER, start_date, end_date)

    # 如果汇率数据获取失败，使用固定汇率
    use_fixed_rates = False
    if usdcny.empty or usdjpy.empty:
        print("\n警告: 汇率数据获取失败，使用固定汇率 (USD/CNY=7.2, JPY/USD=150)")
        use_fixed_rates = True
        fixed_usdcny = 7.2  # 美元兑人民币
        fixed_jpyusd = 150  # 日元兑美元

    # 获取股票数据和市值
    print("\n获取股票数据...")
    naura_data = get_market_cap_series(NAURA_TICKER, start_date, end_date)
    amat_data = get_market_cap_series(AMAT_TICKER, start_date, end_date)
    tel_data = get_market_cap_series(TEL_TICKER, start_date, end_date)

    # 检查数据有效性
    if isinstance(naura_data, tuple) and isinstance(amat_data, tuple) and isinstance(tel_data, tuple):
        naura_cap, naura_price = naura_data
        amat_cap, amat_price = amat_data
        tel_cap, tel_price = tel_data
    else:
        print("错误: 股票数据获取失败")
        return

    # 转换为DataFrame便于处理
    if use_fixed_rates:
        df = pd.DataFrame({
            'naura_price': naura_price,
            'naura_cap_cny': naura_cap,
            'amat_cap_usd': amat_cap,
            'tel_cap_jpy': tel_cap,
        })
        # 使用固定汇率
        df['naura_cap_usd'] = df['naura_cap_cny'] / fixed_usdcny
        df['tel_cap_usd'] = df['tel_cap_jpy'] / fixed_jpyusd
    else:
        df = pd.DataFrame({
            'naura_price': naura_price,
            'naura_cap_cny': naura_cap,
            'amat_cap_usd': amat_cap,
            'tel_cap_jpy': tel_cap,
            'usdcny': usdcny['Close'],
            'usdjpy': usdjpy['Close']
        })
        # 填充缺失值（使用前向填充）
        df = df.fillna(method='ffill').fillna(method='bfill')
        # 转换为美元市值
        df['naura_cap_usd'] = df['naura_cap_cny'] / df['usdcny']
        df['tel_cap_usd'] = df['tel_cap_jpy'] / df['usdjpy']

    # 计算比值
    df['ratio_naura_amat'] = df['naura_cap_usd'] / df['amat_cap_usd']
    df['ratio_naura_tel'] = df['naura_cap_usd'] / df['tel_cap_usd']

    # 删除包含NaN的行
    df = df.dropna()

    if df.empty:
        print("错误: 没有有效数据可以绘图")
        return

    print(f"\n有效数据点数: {len(df)}")
    print("\n最新数据:")
    print(f"北方华创股价: ¥{df['naura_price'].iloc[-1]:.2f}")
    print(f"北方华创市值: ${df['naura_cap_usd'].iloc[-1]/1e9:.2f}B")
    print(f"AMAT市值: ${df['amat_cap_usd'].iloc[-1]/1e9:.2f}B")
    print(f"TEL市值: ${df['tel_cap_usd'].iloc[-1]/1e9:.2f}B")
    print(f"市值比 (北方华创/AMAT): {df['ratio_naura_amat'].iloc[-1]:.3f}")
    print(f"市值比 (北方华创/TEL): {df['ratio_naura_tel'].iloc[-1]:.3f}")

    # 绘图
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # 左Y轴：北方华创股价
    color1 = 'tab:blue'
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel('北方华创股价 (¥)', color=color1, fontsize=12)
    line1 = ax1.plot(df.index, df['naura_price'], color=color1, linewidth=2, label='北方华创股价')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    # 右Y轴：市值比值
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    color3 = 'tab:orange'
    ax2.set_ylabel('市值比值', fontsize=12)
    line2 = ax2.plot(df.index, df['ratio_naura_amat'], color=color2, linewidth=2,
                     label='北方华创/AMAT', linestyle='-')
    line3 = ax2.plot(df.index, df['ratio_naura_tel'], color=color3, linewidth=2,
                     label='北方华创/TEL', linestyle='--')
    ax2.tick_params(axis='y')

    # 添加水平参考线
    ax2.axhline(y=1.0, color='gray', linestyle=':', alpha=0.5, label='市值相等线')

    # 图例
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=10)

    # 标题
    plt.title('半导体设备公司市值对比分析\n北方华创 vs AMAT vs TEL',
              fontsize=14, fontweight='bold', pad=20)

    # 格式化x轴日期
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)

    # 调整布局
    plt.tight_layout()

    # 保存图表
    output_file = 'market_cap_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n图表已保存至: {output_file}")

    # 显示图表
    plt.show()

    print("\n" + "=" * 60)
    print("分析完成！")


if __name__ == "__main__":
    main()

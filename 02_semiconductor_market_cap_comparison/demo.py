#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
半导体设备公司市值对比分析 - 示例数据演示版本
对比北方华创、Applied Materials (AMAT)、Tokyo Electron (TEL) 的市值
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def generate_sample_data():
    """生成示例数据用于演示"""
    print("使用示例数据进行演示...\n")

    # 生成最近2年的日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    # 生成示例股价数据（基于真实市场特征的模拟数据）
    np.random.seed(42)

    # 北方华创股价 (CNY) - 从200到350波动
    naura_base = 250
    naura_trend = np.linspace(0, 40, len(dates))  # 上升趋势
    naura_noise = np.cumsum(np.random.randn(len(dates)) * 3)
    naura_price = naura_base + naura_trend + naura_noise
    naura_price = np.maximum(naura_price, 180)  # 最低价

    # AMAT股价 (USD) - 从120到210波动
    amat_base = 150
    amat_trend = np.linspace(0, 30, len(dates))
    amat_noise = np.cumsum(np.random.randn(len(dates)) * 2)
    amat_price = amat_base + amat_trend + amat_noise

    # TEL股价 (JPY) - 从18000到28000波动
    tel_base = 22000
    tel_trend = np.linspace(0, 4000, len(dates))
    tel_noise = np.cumsum(np.random.randn(len(dates)) * 200)
    tel_price = tel_base + tel_trend + tel_noise

    # 汇率数据（加入一些波动）
    usdcny_base = 7.2
    usdcny = usdcny_base + np.sin(np.linspace(0, 4*np.pi, len(dates))) * 0.15

    jpyusd_base = 150
    jpyusd = jpyusd_base + np.sin(np.linspace(0, 4*np.pi, len(dates))) * 10

    # 总股本（单位：股）
    naura_shares = 1.8e9  # 18亿股
    amat_shares = 850e6   # 8.5亿股
    tel_shares = 300e6    # 3亿股

    # 计算市值（本币）
    naura_cap_cny = naura_price * naura_shares
    amat_cap_usd = amat_price * amat_shares
    tel_cap_jpy = tel_price * tel_shares

    # 创建DataFrame
    df = pd.DataFrame({
        'naura_price': naura_price,
        'naura_cap_cny': naura_cap_cny,
        'amat_cap_usd': amat_cap_usd,
        'tel_cap_jpy': tel_cap_jpy,
        'usdcny': usdcny,
        'jpyusd': jpyusd
    }, index=dates)

    # 转换为美元市值
    df['naura_cap_usd'] = df['naura_cap_cny'] / df['usdcny']
    df['tel_cap_usd'] = df['tel_cap_jpy'] / df['jpyusd']

    # 计算比值
    df['ratio_naura_amat'] = df['naura_cap_usd'] / df['amat_cap_usd']
    df['ratio_naura_tel'] = df['naura_cap_usd'] / df['tel_cap_usd']

    return df


def main():
    print("=" * 60)
    print("半导体设备公司市值对比分析 - 示例数据演示")
    print("=" * 60)
    print("\n注意: 这是使用模拟数据的演示版本")
    print("实际运行请使用 main.py 并确保网络连接\n")

    # 生成示例数据
    df = generate_sample_data()

    print(f"分析时间范围: {df.index[0].date()} 至 {df.index[-1].date()}")
    print(f"数据点数: {len(df)}\n")

    # 显示最新数据
    print("=" * 60)
    print("最新数据 (示例):")
    print("=" * 60)
    print(f"北方华创股价: ¥{df['naura_price'].iloc[-1]:.2f}")
    print(f"北方华创市值: ${df['naura_cap_usd'].iloc[-1]/1e9:.2f}B")
    print(f"AMAT市值: ${df['amat_cap_usd'].iloc[-1]/1e9:.2f}B")
    print(f"TEL市值: ${df['tel_cap_usd'].iloc[-1]/1e9:.2f}B")
    print(f"\n市值比 (北方华创/AMAT): {df['ratio_naura_amat'].iloc[-1]:.3f}")
    print(f"市值比 (北方华创/TEL): {df['ratio_naura_tel'].iloc[-1]:.3f}")

    # 统计信息
    print(f"\n市值比统计 (北方华创/AMAT):")
    print(f"  平均值: {df['ratio_naura_amat'].mean():.3f}")
    print(f"  最小值: {df['ratio_naura_amat'].min():.3f}")
    print(f"  最大值: {df['ratio_naura_amat'].max():.3f}")

    print(f"\n市值比统计 (北方华创/TEL):")
    print(f"  平均值: {df['ratio_naura_tel'].mean():.3f}")
    print(f"  最小值: {df['ratio_naura_tel'].min():.3f}")
    print(f"  最大值: {df['ratio_naura_tel'].max():.3f}")

    # 绘图
    print("\n正在生成图表...")
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # 左Y轴：北方华创股价
    color1 = 'tab:blue'
    ax1.set_xlabel('日期', fontsize=12)
    ax1.set_ylabel('北方华创股价 (¥)', color=color1, fontsize=12)
    line1 = ax1.plot(df.index, df['naura_price'], color=color1, linewidth=2,
                     label='北方华创股价', alpha=0.8)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3, linestyle='--')

    # 右Y轴：市值比值
    ax2 = ax1.twinx()
    color2 = 'tab:red'
    color3 = 'tab:orange'
    ax2.set_ylabel('市值比值', fontsize=12)
    line2 = ax2.plot(df.index, df['ratio_naura_amat'], color=color2, linewidth=2.5,
                     label='北方华创/AMAT', linestyle='-', alpha=0.9)
    line3 = ax2.plot(df.index, df['ratio_naura_tel'], color=color3, linewidth=2.5,
                     label='北方华创/TEL', linestyle='--', alpha=0.9)
    ax2.tick_params(axis='y')

    # 添加水平参考线
    ax2.axhline(y=1.0, color='gray', linestyle=':', linewidth=2, alpha=0.6, label='市值相等线')

    # 图例
    lines = line1 + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', fontsize=11, framealpha=0.9)

    # 标题
    plt.title('半导体设备公司市值对比分析\n北方华创 vs AMAT vs TEL\n(示例数据演示)',
              fontsize=14, fontweight='bold', pad=20)

    # 格式化x轴日期
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    plt.xticks(rotation=45)

    # 调整布局
    plt.tight_layout()

    # 保存图表
    output_file = 'market_cap_comparison_demo.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ 图表已保存至: {output_file}")

    # 尝试显示图表
    try:
        plt.show()
    except:
        print("  (无法显示图表窗口，但文件已保存)")

    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print("\n说明:")
    print("- 此演示使用模拟数据展示程序功能")
    print("- 图表显示了北方华创股价（左轴）和相对两家国际巨头的市值比值（右轴）")
    print("- 市值比值 < 1 表示北方华创市值小于对比公司")
    print("- 市值比值 > 1 表示北方华创市值大于对比公司")
    print("- 实际数据请运行 main.py")


if __name__ == "__main__":
    main()

# 半导体设备公司市值对比分析

## 项目简介

本项目对比分析三家全球领先的半导体设备制造商的市值变化：

- **北方华创** (NAURA, 002371.SZ) - 中国
- **应用材料** (Applied Materials, AMAT) - 美国
- **东京电子** (Tokyo Electron, TEL, 8035.T) - 日本

## 功能特性

1. **数据获取**：自动获取最近2年的股票历史数据
2. **汇率转换**：将所有市值统一转换为美元，确保可比性
3. **市值计算**：使用总市值（股价 × 总股本）进行对比
4. **可视化展示**：
   - 左Y轴：北方华创股价（人民币）
   - 右Y轴：市值比值（北方华创/AMAT、北方华创/TEL）
   - X轴：时间序列

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法一：使用真实数据（推荐）

需要网络连接到Yahoo Finance：

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行主程序
python main.py
```

程序将：
1. 获取股票和汇率数据
2. 计算市值并转换为美元
3. 生成对比图表
4. 保存图表为 `market_cap_comparison.png`

### 方法二：使用示例数据演示

如果网络受限或仅想查看功能演示：

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行演示程序
python demo.py
```

演示程序使用模拟数据，无需网络连接，生成图表为 `market_cap_comparison_demo.png`

## 数据说明

- **数据源**：Yahoo Finance (yfinance)
- **时间范围**：最近2年
- **市值计算**：总市值（Total Market Cap）
- **货币统一**：所有市值转换为美元（USD）

## 输出结果

- 图表文件：`market_cap_comparison.png`
- 控制台输出：最新市值数据和比值

## 项目文件

- `main.py` - 主程序（使用真实数据）
- `demo.py` - 演示程序（使用模拟数据）
- `requirements.txt` - 依赖包列表
- `README.md` - 项目说明文档
- `venv/` - Python虚拟环境（已配置）

## 注意事项

- 需要网络连接以获取实时数据（main.py）
- 首次运行可能需要下载较多数据
- 建议在交易时间后运行以获取最新数据
- Linux系统需要安装中文字体以正确显示图表
- 如遇网络问题，可使用 demo.py 演示功能

## 许可证

MIT License

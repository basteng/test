# XuLiangdang 期权交易管理系统

一个用于管理和跟踪期权交易的Python程序，支持双向操作（看涨和看跌）的自动化记录和分析。

## 项目简介

本项目提供了完整的期权交易管理功能，包括：
- 交易记录的自动化管理
- 双CSV文件写入（总文件和月度文件）
- 收益率计算和分析
- 数据备份和恢复
- 历史数据修复工具

## 主要文件说明

### 核心程序
- `XuTwo.py` - 主程序，用于记录和管理期权交易

### 工具脚本
- `backup_and_check_monthly.py` - 月度数据备份和检查工具
- `fix_*.py` - 各种数据修复脚本
- `add_header_202512.py` - 为CSV文件添加表头
- `analyze_error_data.py` - 错误数据分析
- `clean_*.py` - 数据清理工具
- `inspect_csv.py` - CSV文件检查工具

### 测试文件
- `test_*.py` - 各种功能测试脚本
- `simple_*.py` - 简单测试脚本
- `validate_changes.py` - 变更验证工具

### 文档
- `操作指南.md` - 详细的操作指南
- `dual_csv_write_report.md` - 双CSV写入功能报告

## 使用方法

### 环境要求
- Python 3.x
- 依赖库：（根据实际情况添加）

### 快速开始

1. 克隆本仓库到本地
```bash
git clone <你的仓库地址>
cd XuLiangdang
```

2. 首次运行前，程序会自动创建所需的数据文件：
   - `option_trading_YYYYMM.csv` - 月度交易记录
   - `option_trading_YYYYMMDD.csv` - 总交易记录
   - `option_trading_state_YYYYMM.json` - 状态文件

3. 运行主程序
```bash
python XuTwo.py
```

## 数据文件说明

本项目使用以下类型的数据文件（这些文件不包含在Git仓库中）：
- **CSV数据文件** - 存储实际交易记录
- **JSON状态文件** - 保存程序运行状态
- **LOG日志文件** - 记录程序运行日志

首次在新电脑上使用时，程序会自动创建这些文件。

## 注意事项

1. 数据文件包含个人交易信息，不会被推送到GitHub
2. 建议定期备份数据文件到本地安全位置
3. 详细的使用说明请参考 `操作指南.md`

## 许可证

（根据需要添加许可证信息）

## 联系方式

（根据需要添加联系方式）

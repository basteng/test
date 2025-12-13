# 文件大小错误修复说明

## 错误原因

您遇到的 `FileNotFoundError` 错误有以下几个可能的原因：

### 1. **文件路径不存在**
```
'06_Paper\\iNOW2013\\会议见闻\\Aug_25\\Calleja_Selective area growth...'
```
这个路径可能：
- 文件已被移动或删除
- 路径拼接错误（相对路径 vs 绝对路径）
- 文件夹名称中有特殊字符导致路径解析错误

### 2. **Windows 路径长度限制**
- Windows 默认最大路径长度为 260 字符
- 您的路径包含很长的文件夹名称，可能超过了这个限制
- 路径：`Calleja_Selective area growth of InGaN GaN nanorods on plar semipolar and nonpolar substrates emission from UV to IR and white light`

### 3. **相对路径问题**
- 代码可能使用了相对路径，但当前工作目录不正确
- 需要使用绝对路径或正确设置工作目录

## 修复方案

### 修复 1: 使用 `pathlib.Path` (推荐)

```python
from pathlib import Path

def get_file_size_mb(file_path):
    path_obj = Path(file_path)

    # 检查文件是否存在
    if not path_obj.exists():
        print(f"警告: 文件不存在: {file_path}")
        return 0.0

    # 获取文件大小
    size_bytes = path_obj.stat().st_size
    size_mb = size_bytes / (1024 * 1024)
    return round(size_mb, 2)
```

**优点:**
- 自动处理路径分隔符（/ 和 \）
- 更好的跨平台支持
- 提供 `exists()` 和 `is_file()` 等便捷方法

### 修复 2: 处理 Windows 长路径

```python
import os
import sys

def get_file_size_mb(file_path):
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except FileNotFoundError:
        # 尝试使用 Windows 长路径前缀
        if sys.platform == 'win32':
            long_path = f"\\\\?\\{os.path.abspath(file_path)}"
            size_bytes = os.path.getsize(long_path)
            return size_bytes / (1024 * 1024)
        raise
```

**Windows 长路径前缀:** `\\?\C:\very\long\path\...`

### 修复 3: 添加详细的错误处理

```python
def get_file_size_mb(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return 0.0

        if not os.path.isfile(file_path):
            print(f"不是文件: {file_path}")
            return 0.0

        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)

    except PermissionError:
        print(f"没有权限访问: {file_path}")
        return 0.0
    except Exception as e:
        print(f"错误: {e}")
        return 0.0
```

### 修复 4: 确保使用正确的路径

```python
# 方法 1: 使用绝对路径
pdf_file = os.path.abspath(relative_path)

# 方法 2: 使用 os.path.join 构建路径
pdf_file = os.path.join(base_dir, folder, filename)

# 方法 3: 使用 Path 对象
from pathlib import Path
pdf_file = Path(base_dir) / folder / filename
```

## 如何使用修复后的代码

### 方法 1: 替换整个文件
将新的 `generate_excel.py` 覆盖您的原文件

### 方法 2: 只修改 `get_file_size_mb` 函数
在您的原文件中，将 `get_file_size_mb` 函数替换为新版本

### 方法 3: 调试当前问题

添加调试代码找出具体问题：

```python
def get_file_size_mb(file_path):
    print(f"DEBUG: 检查文件: {file_path}")
    print(f"DEBUG: 文件路径长度: {len(file_path)}")
    print(f"DEBUG: 绝对路径: {os.path.abspath(file_path)}")
    print(f"DEBUG: 文件存在: {os.path.exists(file_path)}")
    print(f"DEBUG: 当前工作目录: {os.getcwd()}")

    # 原来的代码...
```

## Windows 特定解决方案

### 启用长路径支持 (Windows 10 1607+)

1. **通过注册表启用:**
   ```
   HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\FileSystem
   LongPathsEnabled = 1
   ```

2. **通过组策略启用:**
   - Win + R → `gpedit.msc`
   - 计算机配置 → 管理模板 → 系统 → 文件系统
   - 启用 "启用 Win32 长路径"

3. **在代码中声明支持长路径 (Python 3.6+):**
   在 manifest 中添加 `longPathAware`

## 建议

1. **重命名长文件夹:** 考虑缩短文件夹名称
2. **移动文件:** 将文件移到更短的路径
3. **使用 pathlib:** 更现代、更安全的路径处理
4. **添加日志:** 记录所有文件处理错误，方便调试

## 测试

运行以下代码测试修复：

```python
from pathlib import Path

# 测试文件路径
test_path = r"06_Paper\iNOW2013\会议见闻\Aug_25\..."

# 检查
print(f"文件存在: {Path(test_path).exists()}")
print(f"是文件: {Path(test_path).is_file()}")
print(f"父目录存在: {Path(test_path).parent.exists()}")
```

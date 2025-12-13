import os
import sys
from pathlib import Path

def get_file_size_mb(file_path):
    """
    获取文件大小（MB）
    处理 Windows 长路径和文件不存在的情况
    """
    try:
        # 使用 Path 对象处理路径
        path_obj = Path(file_path)

        # 检查文件是否存在
        if not path_obj.exists():
            print(f"警告: 文件不存在: {file_path}", file=sys.stderr)
            return 0.0

        # 检查是否是文件（而不是目录）
        if not path_obj.is_file():
            print(f"警告: 路径不是文件: {file_path}", file=sys.stderr)
            return 0.0

        # 获取文件大小
        size_bytes = path_obj.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)

    except PermissionError:
        print(f"警告: 没有权限访问文件: {file_path}", file=sys.stderr)
        return 0.0
    except OSError as e:
        # 处理 Windows 长路径问题
        if sys.platform == 'win32' and len(str(file_path)) > 260:
            try:
                # 尝试使用 Windows 长路径前缀
                long_path = f"\\\\?\\{os.path.abspath(file_path)}"
                size_bytes = os.path.getsize(long_path)
                size_mb = size_bytes / (1024 * 1024)
                return round(size_mb, 2)
            except Exception as e2:
                print(f"警告: 无法获取文件大小 (长路径): {file_path}", file=sys.stderr)
                print(f"错误详情: {e2}", file=sys.stderr)
                return 0.0
        else:
            print(f"警告: 无法获取文件大小: {file_path}", file=sys.stderr)
            print(f"错误详情: {e}", file=sys.stderr)
            return 0.0
    except Exception as e:
        print(f"警告: 处理文件时出现未知错误: {file_path}", file=sys.stderr)
        print(f"错误详情: {e}", file=sys.stderr)
        return 0.0


def process_pdf_files(root_dir):
    """
    遍历目录并处理所有 PDF 文件
    """
    root_path = Path(root_dir)

    if not root_path.exists():
        print(f"错误: 根目录不存在: {root_dir}", file=sys.stderr)
        return []

    pdf_files = []

    # 使用 Path.rglob 递归查找所有 PDF 文件
    try:
        for pdf_file in root_path.rglob("*.pdf"):
            try:
                file_info = {
                    'path': str(pdf_file),
                    'name': pdf_file.name,
                    'size_mb': get_file_size_mb(pdf_file),
                    'relative_path': str(pdf_file.relative_to(root_path))
                }
                pdf_files.append(file_info)
            except Exception as e:
                print(f"警告: 处理文件时出错 {pdf_file}: {e}", file=sys.stderr)
                continue

    except Exception as e:
        print(f"错误: 遍历目录时出错: {e}", file=sys.stderr)

    return pdf_files


def main():
    """
    主函数
    """
    # 示例：处理当前目录
    root_directory = "."

    # 如果有命令行参数，使用第一个参数作为根目录
    if len(sys.argv) > 1:
        root_directory = sys.argv[1]

    print(f"正在扫描目录: {root_directory}")

    # 处理 PDF 文件
    pdf_files = process_pdf_files(root_directory)

    print(f"\n找到 {len(pdf_files)} 个 PDF 文件")

    # 显示结果
    for i, file_info in enumerate(pdf_files, 1):
        print(f"{i}. {file_info['name']} - {file_info['size_mb']} MB")
        if file_info['size_mb'] == 0.0:
            print(f"   警告: 文件大小为 0 或无法访问")

    # 这里可以添加生成 Excel 的代码
    # import openpyxl
    # wb = openpyxl.Workbook()
    # ws = wb.active
    # ...

    return pdf_files


if __name__ == "__main__":
    main()

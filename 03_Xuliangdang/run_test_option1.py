"""
自动选择选项1的测试脚本
"""
from test_dual_csv_write import main
import sys

# 模拟输入选项1
import builtins
original_input = builtins.input

def mock_input(prompt):
    print(prompt)
    return "1"  # 自动返回选项1

builtins.input = mock_input

# 运行主函数
try:
    print("开始运行测试脚本...")
    main()
    print("测试脚本运行完成")
except Exception as e:
    import traceback
    print(f"测试脚本运行出错: {e}")
    print(traceback.format_exc())
finally:
    # 恢复原始输入函数
    builtins.input = original_input

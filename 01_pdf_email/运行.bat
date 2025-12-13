@echo off
chcp 65001 >nul
echo ========================================
echo PDF Email 提取工具
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未检测到Python，请先安装Python
    pause
    exit /b
)

echo 正在运行脚本...
echo.
python generate_excel.py

echo.
echo ========================================
echo 处理完成！请查看生成的Excel文件
echo ========================================
pause

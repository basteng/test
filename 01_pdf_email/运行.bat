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

REM 检查pdfplumber是否安装
echo 检查依赖库...
python -c "import pdfplumber" >nul 2>&1
if errorlevel 1 (
    echo.
    echo 检测到缺少依赖库，正在自动安装...
    echo 执行命令: pip install -r requirements.txt
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo 错误：依赖安装失败，请手动运行: pip install -r requirements.txt
        pause
        exit /b
    )
    echo.
    echo ✓ 依赖库安装成功！
    echo.
)

echo 正在运行脚本...
echo.
python generate_excel.py

echo.
echo ========================================
echo 处理完成！请查看生成的Excel文件
echo ========================================
pause

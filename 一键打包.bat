@echo off
chcp 65001 >nul
title 影视播放器打包工具
echo.
echo ========================================
echo    🎬 影视播放器 - 一键打包工具
echo ========================================
echo.

echo [1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请先安装Python 3.10+
    echo    下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version
echo ✅ Python已安装
echo.

echo [2/4] 安装依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)
echo ✅ 依赖安装完成
echo.

echo [3/4] 安装PyInstaller...
pip install pyinstaller
echo ✅ PyInstaller安装完成
echo.

echo [4/4] 开始打包...
echo    这可能需要几分钟，请耐心等待...
echo.

pyinstaller --name="影视播放器" ^
    --onefile ^
    --windowed ^
    --add-data "core;core" ^
    --add-data "ui;ui" ^
    --add-data "utils;utils" ^
    --hidden-import PyQt6.sip ^
    --hidden-import PyQt6.QtCore ^
    --hidden-import PyQt6.QtGui ^
    --hidden-import PyQt6.QtWidgets ^
    --hidden-import PyQt6.QtWebEngineWidgets ^
    --hidden-import requests ^
    --clean ^
    --noconfirm ^
    run.py

if errorlevel 1 (
    echo.
    echo ❌ 打包失败！
    pause
    exit /b 1
)

echo.
echo ========================================
echo    🎉 打包成功！
echo ========================================
echo.
echo 📁 输出文件位置:
echo    dist�影视播放器.exe
echo.
echo 💡 使用说明:
echo    1. 将 exe 文件复制到任意位置
echo    2. 双击运行即可
echo    3. 无需安装Python环境
echo.
echo ⚠️  注意事项:
echo    • 文件大小约 150MB（包含所有依赖）
echo    • 首次启动可能需要几秒钟
echo    • 如遇杀毒软件提示，请添加信任
echo.
pause

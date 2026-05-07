#!/bin/bash
# 影视播放器安装脚本

echo "=========================================="
echo "🎬 影视播放器 - 安装程序"
echo "=========================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    echo "   请先安装 Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python版本: $PYTHON_VERSION"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 错误: 未找到 pip3"
    exit 1
fi
echo "✅ pip已安装"

# 安装Python依赖
echo ""
echo "📦 安装Python依赖..."
pip3 install -r requirements.txt --break-system-packages

if [ $? -ne 0 ]; then
    echo "⚠️  使用 --break-system-packages 失败，尝试普通安装..."
    pip3 install -r requirements.txt
fi

# 检查系统依赖(Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo ""
    echo "🔧 检查系统依赖..."
    
    # 检查必要的库
    if ! ldconfig -p | grep -q libEGL.so; then
        echo "⚠️  缺少 libEGL，尝试安装..."
        apt-get update -qq && apt-get install -y libegl1 libgles2-mesa
    fi
    
    if ! ldconfig -p | grep -q libXcomposite.so; then
        echo "⚠️  缺少 libXcomposite，尝试安装..."
        apt-get install -y libxcomposite1 libxdamage1 libxrandr2
    fi
fi

# 创建桌面快捷方式(如果可能)
echo ""
echo "📝 创建启动脚本..."

# Linux桌面快捷方式
if [[ "$OSTYPE" == "linux-gnu"* ]] && [ -d "$HOME/Desktop" ]; then
    cat > "$HOME/Desktop/影视播放器.desktop" << EOF
[Desktop Entry]
Name=影视播放器
Comment=在线影视播放器
Exec=python3 $(pwd)/run.py
Icon=$(pwd)/resources/icons/app.png
Type=Application
Terminal=false
Categories=AudioVideo;Video;
EOF
    chmod +x "$HOME/Desktop/影视播放器.desktop"
    echo "✅ 桌面快捷方式已创建"
fi

# Windows批处理
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    cat > "启动播放器.bat" << EOF
@echo off
echo 正在启动影视播放器...
python run.py
pause
EOF
    echo "✅ Windows启动脚本已创建"
fi

# macOS应用包
if [[ "$OSTYPE" == "darwin"* ]]; then
    cat > "启动.command" << EOF
#!/bin/bash
cd "$(dirname "$0")"
python3 run.py
EOF
    chmod +x "启动.command"
    echo "✅ macOS启动脚本已创建"
fi

echo ""
echo "=========================================="
echo "🎉 安装完成!"
echo "=========================================="
echo ""
echo "🚀 启动方式:"
echo "   1. 命令行: python3 run.py"
echo "   2. 双击启动脚本"
if [[ "$OSTYPE" == "linux-gnu"* ]] && [ -d "$HOME/Desktop" ]; then
    echo "   3. 桌面快捷方式"
fi
echo ""
echo "📁 安装目录: $(pwd)"
echo ""
echo "💡 提示:"
echo "   - 首次启动可能需要几秒钟加载"
echo "   - 支持暗色/亮色主题切换"
echo "   - 多线路自动切换，卡顿可换源"
echo ""

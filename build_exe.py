# -*- coding: utf-8 -*-
"""
打包脚本 - 生成exe文件
"""
import os
import sys
import subprocess

def build_exe():
    """使用PyInstaller打包"""
    
    print("="*60)
    print("🎬 影视播放器 - 打包工具")
    print("="*60)
    
    # 检查PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller已安装")
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    
    # 打包参数
    print("\n📦 开始打包...")
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=影视播放器",
        "--onefile",  # 打包成单个exe
        "--windowed",  # 不显示控制台窗口
        "--icon=NONE",
        "--add-data", "core;core",
        "--add-data", "ui;ui",
        "--add-data", "utils;utils",
        "--hidden-import", "PyQt6.sip",
        "--hidden-import", "PyQt6.QtCore",
        "--hidden-import", "PyQt6.QtGui",
        "--hidden-import", "PyQt6.QtWidgets",
        "--hidden-import", "PyQt6.QtWebEngineWidgets",
        "--hidden-import", "requests",
        "--clean",
        "--noconfirm",
        "run.py"
    ]
    
    print(f"执行命令: {' '.join(cmd[:10])}...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("\n✅ 打包成功!")
            print("\n📁 输出文件:")
            exe_path = os.path.join("dist", "影视播放器.exe")
            if os.path.exists(exe_path):
                size = os.path.getsize(exe_path) / (1024*1024)
                print(f"   {exe_path} ({size:.1f} MB)")
            return True
        else:
            print("\n❌ 打包失败!")
            print("错误输出:", result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
            return False
            
    except Exception as e:
        print(f"\n❌ 打包出错: {e}")
        return False

def create_simple_build():
    """创建简化版打包（不包含WebEngine，体积更小）"""
    
    print("\n" + "="*60)
    print("📦 创建简化版播放器（无内置播放器）")
    print("="*60)
    
    # 创建一个简化版入口文件
    simple_main = '''# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.main_window import MainWindow
from utils.config import Config
from utils.theme import ThemeManager

def main():
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
    app = QApplication(sys.argv)
    app.setApplicationName("影视播放器")
    
    font = QFont("Microsoft YaHei", 10)
    app.setFont(font)
    
    config = Config()
    ThemeManager.apply(config.theme)
    
    window = MainWindow(config)
    window.show()
    window.resize(1400, 850)
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
'''
    
    with open("simple_run.py", "w", encoding="utf-8") as f:
        f.write(simple_main)
    
    print("✅ 简化版入口文件已创建: simple_run.py")
    print("\n简化版特点:")
    print("  • 不包含内置视频播放器")
    print("  • 点击播放会调用系统浏览器")
    print("  • 体积更小 (~30MB)")
    print("  • 启动更快")

if __name__ == "__main__":
    print("\n选择打包方式:")
    print("1. 完整版 (包含内置播放器，~150MB)")
    print("2. 简化版 (调用系统播放器，~30MB)")
    print("3. 两者都打包")
    
    choice = input("\n请选择 (1/2/3): ").strip()
    
    if choice == "1":
        build_exe()
    elif choice == "2":
        create_simple_build()
    elif choice == "3":
        build_exe()
        create_simple_build()
    else:
        print("无效选择，默认打包完整版...")
        build_exe()

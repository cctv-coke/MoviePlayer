# -*- coding: utf-8 -*-
"""
MoviePlayer - 影视播放器
参考网飞猫、可可影视、樱花网站的UI布局
"""
import sys
import os

# 将项目根目录添加到系统路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont

from ui.main_window import MainWindow
from utils.config import Config


def main():
    # 高DPI支持
    os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")

    app = QApplication(sys.argv)
    app.setApplicationName("影视播放器")
    app.setApplicationDisplayName("影视播放器")

    # 全局字体
    font = QFont("Microsoft YaHei", 10)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(font)

    # 加载配置
    config = Config()

    # 创建主窗口
    window = MainWindow(config)
    window.show()

    # 窗口大小
    window.resize(1400, 850)
    # 居中显示
    screen = app.primaryScreen().geometry()
    x = (screen.width() - 1400) // 2
    y = (screen.height() - 850) // 2
    window.move(x, y)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

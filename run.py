# -*- coding: utf-8 -*-
"""
启动脚本 - 影视播放器
参考TVBox设计风格
"""
import sys
import os

# 设置环境变量
os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QSplashScreen, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QPixmap, QColor

from ui.main_window import MainWindow
from utils.config import Config
from utils.theme import ThemeManager


class SplashScreen(QWidget):
    """启动画面"""
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 250)
        
        # 主容器
        container = QWidget(self)
        container.setObjectName("splashContainer")
        container.setStyleSheet("""
            #splashContainer {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:0.5 #16213e, stop:1 #0f3460);
                border-radius: 15px;
            }
        """)
        container.setGeometry(0, 0, 400, 250)
        
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)
        
        # Logo
        logo = QLabel("🎬")
        logo.setStyleSheet("font-size: 64px;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        
        # 标题
        title = QLabel("影视播放器")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: white;
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 副标题
        subtitle = QLabel("参考TVBox设计 · 多源聚合 · 极简体验")
        subtitle.setStyleSheet("""
            font-size: 12px;
            color: #888;
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # 加载提示
        self.loading = QLabel("正在加载...")
        self.loading.setStyleSheet("""
            font-size: 11px;
            color: #e94560;
        """)
        self.loading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading)
        
        # 居中显示
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - 400) // 2,
            (screen.height() - 250) // 2
        )


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setApplicationName("影视播放器")
    app.setApplicationDisplayName("影视播放器")
    
    # 全局字体
    font = QFont("Microsoft YaHei", 10)
    font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    app.setFont(font)
    
    # 显示启动画面
    splash = SplashScreen()
    splash.show()
    
    # 加载配置
    config = Config()
    ThemeManager.apply(config.theme)
    
    # 创建主窗口
    window = MainWindow(config)
    
    # 延迟显示主窗口
    def show_main():
        splash.loading.setText("加载完成!")
        splash.close()
        window.show()
        window.resize(1400, 850)
        screen = app.primaryScreen().geometry()
        window.move(
            (screen.width() - 1400) // 2,
            (screen.height() - 850) // 2
        )
    
    QTimer.singleShot(800, show_main)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

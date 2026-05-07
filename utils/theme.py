# -*- coding: utf-8 -*-
"""
主题管理器 - 亮色/暗色双主题
参考网飞猫、可可影视的暗色风格和樱花动漫的亮色风格
"""
from PyQt6.QtWidgets import QApplication


class ThemeManager:
    """主题管理器"""

    DARK_STYLE = """
    /* ===== 全局 ===== */
    QWidget {
        background-color: #1a1a2e;
        color: #e0e0e0;
        font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
        font-size: 13px;
    }

    /* ===== 主窗口 ===== */
    QMainWindow {
        background-color: #16213e;
    }

    /* ===== 侧边栏 ===== */
    #sidebar {
        background-color: #0f3460;
        border-right: 1px solid #1a1a4e;
    }

    /* ===== 导航按钮 ===== */
    #navBtn {
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        color: #a0a0c0;
        font-size: 14px;
        font-weight: bold;
        text-align: left;
        min-height: 44px;
    }
    #navBtn:hover {
        background-color: rgba(233, 69, 96, 0.15);
        color: #e94560;
    }
    #navBtn:checked {
        background-color: rgba(233, 69, 96, 0.25);
        color: #e94560;
        border-left: 3px solid #e94560;
    }

    /* ===== 搜索框 ===== */
    #searchEdit {
        background-color: #1a1a4e;
        border: 2px solid #2a2a5e;
        border-radius: 20px;
        padding: 8px 20px 8px 40px;
        color: #e0e0e0;
        font-size: 13px;
        min-height: 36px;
    }
    #searchEdit:focus {
        border-color: #e94560;
    }
    #searchEdit::placeholder {
        color: #6a6a8a;
    }

    /* ===== 内容区域 ===== */
    #contentArea {
        background-color: #1a1a2e;
        border: none;
    }

    /* ===== 滚动区域 ===== */
    QScrollArea {
        background-color: transparent;
        border: none;
    }
    QScrollBar:vertical {
        background-color: #1a1a2e;
        width: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background-color: #3a3a5e;
        border-radius: 4px;
        min-height: 30px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #e94560;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar:horizontal {
        background-color: #1a1a2e;
        height: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:horizontal {
        background-color: #3a3a5e;
        border-radius: 4px;
        min-width: 30px;
    }
    QScrollBar::handle:horizontal:hover {
        background-color: #e94560;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }

    /* ===== 卡片 ===== */
    #movieCard {
        background-color: #16213e;
        border: 1px solid #2a2a5e;
        border-radius: 10px;
    }
    #movieCard:hover {
        border-color: #e94560;
        background-color: #1a2745;
    }

    /* ===== 标签 ===== */
    #sectionTitle {
        color: #ffffff;
        font-size: 20px;
        font-weight: bold;
        padding: 10px 0;
    }

    /* ===== 按钮 ===== */
    QPushButton {
        background-color: #0f3460;
        border: 1px solid #2a2a5e;
        border-radius: 6px;
        padding: 6px 16px;
        color: #e0e0e0;
        font-size: 13px;
    }
    QPushButton:hover {
        background-color: #e94560;
        border-color: #e94560;
        color: white;
    }
    QPushButton:pressed {
        background-color: #c73650;
    }

    /* ===== 主按钮 ===== */
    #primaryBtn {
        background-color: #e94560;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        color: white;
        font-size: 14px;
        font-weight: bold;
    }
    #primaryBtn:hover {
        background-color: #ff6b81;
    }

    /* ===== 分类标签 ===== */
    #categoryTag {
        background-color: #1a1a4e;
        border: 1px solid #2a2a5e;
        border-radius: 16px;
        padding: 6px 18px;
        color: #a0a0c0;
        font-size: 13px;
    }
    #categoryTag:hover {
        background-color: rgba(233, 69, 96, 0.2);
        border-color: #e94560;
        color: #e94560;
    }
    #categoryTag:checked {
        background-color: #e94560;
        border-color: #e94560;
        color: white;
    }

    /* ===== 分集按钮 ===== */
    #episodeBtn {
        background-color: #1a1a4e;
        border: 1px solid #2a2a5e;
        border-radius: 6px;
        padding: 8px 4px;
        color: #c0c0e0;
        font-size: 12px;
        min-width: 50px;
        min-height: 36px;
    }
    #episodeBtn:hover {
        background-color: rgba(233, 69, 96, 0.2);
        border-color: #e94560;
        color: #e94560;
    }
    #episodeBtn:checked {
        background-color: #e94560;
        border-color: #e94560;
        color: white;
    }

    /* ===== 线路标签 ===== */
    #sourceTab {
        background-color: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 8px 20px;
        color: #a0a0c0;
        font-size: 13px;
        font-weight: bold;
    }
    #sourceTab:hover {
        color: #e0e0e0;
    }
    #sourceTab:checked {
        color: #e94560;
        border-bottom: 2px solid #e94560;
    }

    /* ===== Banner轮播 ===== */
    #bannerContainer {
        background-color: #0f3460;
        border-radius: 12px;
    }

    /* ===== 详情页 ===== */
    #detailInfo {
        background-color: #16213e;
        border-radius: 12px;
    }

    /* ===== 评分标签 ===== */
    #scoreLabel {
        color: #ffd700;
        font-size: 16px;
        font-weight: bold;
    }

    /* ===== 备注标签 ===== */
    #remarksLabel {
        color: #e94560;
        font-size: 11px;
        font-weight: bold;
        background-color: rgba(233, 69, 96, 0.15);
        border-radius: 4px;
        padding: 2px 8px;
    }

    /* ===== 标签页 ===== */
    QTabWidget::pane {
        border: none;
        background-color: transparent;
    }
    QTabBar::tab {
        background-color: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 10px 20px;
        color: #a0a0c0;
        font-size: 14px;
        font-weight: bold;
    }
    QTabBar::tab:hover {
        color: #e0e0e0;
    }
    QTabBar::tab:selected {
        color: #e94560;
        border-bottom: 2px solid #e94560;
    }

    /* ===== 加载动画 ===== */
    #loadingLabel {
        color: #e94560;
        font-size: 14px;
    }

    /* ===== 工具提示 ===== */
    QToolTip {
        background-color: #2a2a5e;
        color: #e0e0e0;
        border: 1px solid #3a3a6e;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 12px;
    }

    /* ===== 菜单 ===== */
    QMenu {
        background-color: #16213e;
        border: 1px solid #2a2a5e;
        border-radius: 8px;
        padding: 6px;
    }
    QMenu::item {
        padding: 8px 30px 8px 20px;
        border-radius: 4px;
    }
    QMenu::item:selected {
        background-color: rgba(233, 69, 96, 0.2);
    }
    QMenu::separator {
        height: 1px;
        background-color: #2a2a5e;
        margin: 4px 10px;
    }

    /* ===== 状态栏 ===== */
    QStatusBar {
        background-color: #0f3460;
        color: #a0a0c0;
        border-top: 1px solid #1a1a4e;
        font-size: 12px;
    }

    /* ===== 标题栏 ===== */
    #titleBar {
        background-color: #0a1628;
    }

    /* ===== 分页按钮 ===== */
    #pageBtn {
        background-color: #1a1a4e;
        border: 1px solid #2a2a5e;
        border-radius: 6px;
        padding: 6px 14px;
        color: #c0c0e0;
        min-width: 36px;
        min-height: 32px;
    }
    #pageBtn:hover {
        background-color: rgba(233, 69, 96, 0.2);
        border-color: #e94560;
        color: #e94560;
    }
    #pageBtn:checked {
        background-color: #e94560;
        border-color: #e94560;
        color: white;
    }
    #pageBtn:disabled {
        background-color: #0f1a30;
        color: #4a4a6a;
        border-color: #1a1a3e;
    }
    """

    LIGHT_STYLE = """
    /* ===== 全局 ===== */
    QWidget {
        background-color: #f5f5f7;
        color: #333333;
        font-family: "Microsoft YaHei", "PingFang SC", sans-serif;
        font-size: 13px;
    }

    /* ===== 主窗口 ===== */
    QMainWindow {
        background-color: #ffffff;
    }

    /* ===== 侧边栏 ===== */
    #sidebar {
        background-color: #ffffff;
        border-right: 1px solid #e8e8ed;
    }

    /* ===== 导航按钮 ===== */
    #navBtn {
        background-color: transparent;
        border: none;
        border-radius: 8px;
        padding: 12px 20px;
        color: #666666;
        font-size: 14px;
        font-weight: bold;
        text-align: left;
        min-height: 44px;
    }
    #navBtn:hover {
        background-color: rgba(255, 107, 107, 0.08);
        color: #ff4757;
    }
    #navBtn:checked {
        background-color: rgba(255, 107, 107, 0.12);
        color: #ff4757;
        border-left: 3px solid #ff4757;
    }

    /* ===== 搜索框 ===== */
    #searchEdit {
        background-color: #f0f0f5;
        border: 2px solid #e0e0e5;
        border-radius: 20px;
        padding: 8px 20px 8px 40px;
        color: #333333;
        font-size: 13px;
        min-height: 36px;
    }
    #searchEdit:focus {
        border-color: #ff4757;
    }
    #searchEdit::placeholder {
        color: #aaaaaa;
    }

    /* ===== 内容区域 ===== */
    #contentArea {
        background-color: #f5f5f7;
        border: none;
    }

    /* ===== 滚动区域 ===== */
    QScrollArea {
        background-color: transparent;
        border: none;
    }
    QScrollBar:vertical {
        background-color: #f5f5f7;
        width: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:vertical {
        background-color: #d0d0d5;
        border-radius: 4px;
        min-height: 30px;
    }
    QScrollBar::handle:vertical:hover {
        background-color: #ff4757;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar:horizontal {
        background-color: #f5f5f7;
        height: 8px;
        border-radius: 4px;
    }
    QScrollBar::handle:horizontal {
        background-color: #d0d0d5;
        border-radius: 4px;
        min-width: 30px;
    }
    QScrollBar::handle:horizontal:hover {
        background-color: #ff4757;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }

    /* ===== 卡片 ===== */
    #movieCard {
        background-color: #ffffff;
        border: 1px solid #e8e8ed;
        border-radius: 10px;
    }
    #movieCard:hover {
        border-color: #ff4757;
        box-shadow: 0 4px 15px rgba(255, 71, 87, 0.15);
    }

    /* ===== 标签 ===== */
    #sectionTitle {
        color: #222222;
        font-size: 20px;
        font-weight: bold;
        padding: 10px 0;
    }

    /* ===== 按钮 ===== */
    QPushButton {
        background-color: #ffffff;
        border: 1px solid #e0e0e5;
        border-radius: 6px;
        padding: 6px 16px;
        color: #333333;
        font-size: 13px;
    }
    QPushButton:hover {
        background-color: #ff4757;
        border-color: #ff4757;
        color: white;
    }
    QPushButton:pressed {
        background-color: #e8384f;
    }

    /* ===== 主按钮 ===== */
    #primaryBtn {
        background-color: #ff4757;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        color: white;
        font-size: 14px;
        font-weight: bold;
    }
    #primaryBtn:hover {
        background-color: #ff6b7a;
    }

    /* ===== 分类标签 ===== */
    #categoryTag {
        background-color: #f0f0f5;
        border: 1px solid #e0e0e5;
        border-radius: 16px;
        padding: 6px 18px;
        color: #666666;
        font-size: 13px;
    }
    #categoryTag:hover {
        background-color: rgba(255, 71, 87, 0.08);
        border-color: #ff4757;
        color: #ff4757;
    }
    #categoryTag:checked {
        background-color: #ff4757;
        border-color: #ff4757;
        color: white;
    }

    /* ===== 分集按钮 ===== */
    #episodeBtn {
        background-color: #f0f0f5;
        border: 1px solid #e0e0e5;
        border-radius: 6px;
        padding: 8px 4px;
        color: #555555;
        font-size: 12px;
        min-width: 50px;
        min-height: 36px;
    }
    #episodeBtn:hover {
        background-color: rgba(255, 71, 87, 0.08);
        border-color: #ff4757;
        color: #ff4757;
    }
    #episodeBtn:checked {
        background-color: #ff4757;
        border-color: #ff4757;
        color: white;
    }

    /* ===== 线路标签 ===== */
    #sourceTab {
        background-color: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 8px 20px;
        color: #666666;
        font-size: 13px;
        font-weight: bold;
    }
    #sourceTab:hover {
        color: #333333;
    }
    #sourceTab:checked {
        color: #ff4757;
        border-bottom: 2px solid #ff4757;
    }

    /* ===== Banner轮播 ===== */
    #bannerContainer {
        background-color: #ffffff;
        border-radius: 12px;
    }

    /* ===== 详情页 ===== */
    #detailInfo {
        background-color: #ffffff;
        border-radius: 12px;
    }

    /* ===== 评分标签 ===== */
    #scoreLabel {
        color: #ff9500;
        font-size: 16px;
        font-weight: bold;
    }

    /* ===== 备注标签 ===== */
    #remarksLabel {
        color: #ff4757;
        font-size: 11px;
        font-weight: bold;
        background-color: rgba(255, 71, 87, 0.1);
        border-radius: 4px;
        padding: 2px 8px;
    }

    /* ===== 标签页 ===== */
    QTabWidget::pane {
        border: none;
        background-color: transparent;
    }
    QTabBar::tab {
        background-color: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        padding: 10px 20px;
        color: #666666;
        font-size: 14px;
        font-weight: bold;
    }
    QTabBar::tab:hover {
        color: #333333;
    }
    QTabBar::tab:selected {
        color: #ff4757;
        border-bottom: 2px solid #ff4757;
    }

    /* ===== 加载动画 ===== */
    #loadingLabel {
        color: #ff4757;
        font-size: 14px;
    }

    /* ===== 工具提示 ===== */
    QToolTip {
        background-color: #333333;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 6px 12px;
        font-size: 12px;
    }

    /* ===== 菜单 ===== */
    QMenu {
        background-color: #ffffff;
        border: 1px solid #e0e0e5;
        border-radius: 8px;
        padding: 6px;
    }
    QMenu::item {
        padding: 8px 30px 8px 20px;
        border-radius: 4px;
    }
    QMenu::item:selected {
        background-color: rgba(255, 71, 87, 0.08);
    }
    QMenu::separator {
        height: 1px;
        background-color: #e0e0e5;
        margin: 4px 10px;
    }

    /* ===== 状态栏 ===== */
    QStatusBar {
        background-color: #ffffff;
        color: #999999;
        border-top: 1px solid #e8e8ed;
        font-size: 12px;
    }

    /* ===== 标题栏 ===== */
    #titleBar {
        background-color: #ffffff;
    }

    /* ===== 分页按钮 ===== */
    #pageBtn {
        background-color: #ffffff;
        border: 1px solid #e0e0e5;
        border-radius: 6px;
        padding: 6px 14px;
        color: #555555;
        min-width: 36px;
        min-height: 32px;
    }
    #pageBtn:hover {
        background-color: rgba(255, 71, 87, 0.08);
        border-color: #ff4757;
        color: #ff4757;
    }
    #pageBtn:checked {
        background-color: #ff4757;
        border-color: #ff4757;
        color: white;
    }
    #pageBtn:disabled {
        background-color: #f5f5f7;
        color: #cccccc;
        border-color: #eeeeee;
    }
    """

    @classmethod
    def apply(cls, theme_name):
        """应用主题"""
        app = QApplication.instance()
        if theme_name == "dark":
            app.setStyleSheet(cls.DARK_STYLE)
        else:
            app.setStyleSheet(cls.LIGHT_STYLE)

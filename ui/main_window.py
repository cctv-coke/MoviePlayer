# -*- coding: utf-8 -*-
"""
主窗口 - 参考网飞猫/可可影视/樱花动漫的布局
左侧导航栏 + 右侧内容区
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QLabel, QStackedWidget, QStatusBar,
    QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QAction

from utils.theme import ThemeManager
from utils.config import Config
from ui.home_page import HomePage
from ui.category_page import CategoryPage
from ui.search_page import SearchPage
from ui.detail_page import DetailPage
from ui.player_page import PlayerPage
from ui.favorites_page import FavoritesPage
from ui.history_page import HistoryPage


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.current_page = "home"

        self._init_ui()
        self._apply_theme()

    def _init_ui(self):
        """初始化UI"""
        # 无边框窗口
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setMinimumSize(1000, 650)

        # 中央部件
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ===== 左侧导航栏 =====
        self._create_sidebar(main_layout)

        # ===== 右侧内容区 =====
        self._create_content_area(main_layout)

        # ===== 状态栏 =====
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

    def _create_sidebar(self, parent_layout):
        """创建侧边栏"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(5)

        # Logo
        logo_label = QLabel("🎬 影视播放器")
        logo_label.setObjectName("logoLabel")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setFont(QFont("Microsoft YaHei", 16, QFont.Weight.Bold))
        logo_label.setFixedHeight(50)
        sidebar_layout.addWidget(logo_label)

        # 分隔线
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background-color: rgba(255,255,255,0.1); max-height: 1px;")
        sidebar_layout.addWidget(line)

        sidebar_layout.addSpacing(10)

        # 导航按钮
        nav_items = [
            ("🏠", "首页", "home"),
            ("🎬", "电影", "movie"),
            ("📺", "电视剧", "tv"),
            ("🎌", "动漫", "anime"),
            ("🎤", "综艺", "variety"),
            ("🔍", "搜索", "search"),
            ("❤️", "收藏", "favorites"),
            ("📋", "历史", "history"),
        ]

        self.nav_buttons = {}
        for icon, text, page_id in nav_items:
            btn = QPushButton(f"  {icon}  {text}")
            btn.setObjectName("navBtn")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, pid=page_id: self._navigate_to(pid))
            sidebar_layout.addWidget(btn)
            self.nav_buttons[page_id] = btn

        # 默认选中首页
        self.nav_buttons["home"].setChecked(True)

        sidebar_layout.addStretch()

        # 底部：主题切换按钮
        theme_line = QFrame()
        theme_line.setFrameShape(QFrame.Shape.HLine)
        theme_line.setStyleSheet("background-color: rgba(255,255,255,0.1); max-height: 1px;")
        sidebar_layout.addWidget(theme_line)

        self.theme_btn = QPushButton("  🌙  暗色主题")
        self.theme_btn.setObjectName("navBtn")
        self.theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.theme_btn.clicked.connect(self._toggle_theme)
        sidebar_layout.addWidget(self.theme_btn)

        parent_layout.addWidget(sidebar)

    def _create_content_area(self, parent_layout):
        """创建内容区"""
        # 标题栏
        title_bar = QFrame()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(40)
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(15, 0, 15, 0)

        # 标题
        self.page_title = QLabel("首页")
        self.page_title.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        title_bar_layout.addWidget(self.page_title)

        title_bar_layout.addStretch()

        # 窗口控制按钮
        btn_size = 32
        for text, slot in [("—", self.showMinimized), ("□", self._toggle_maximize), ("✕", self.close)]:
            btn = QPushButton(text)
            btn.setFixedSize(btn_size, btn_size)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    color: #999;
                    font-size: 16px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: rgba(255,255,255,0.1);
                    color: white;
                }
            """)
            btn.clicked.connect(slot)
            title_bar_layout.addWidget(btn)

        # 页面堆栈
        self.stack = QStackedWidget()
        self.stack.setObjectName("contentArea")

        # 创建各页面
        self.home_page = HomePage(self)
        self.category_page = CategoryPage(self)
        self.search_page = SearchPage(self)
        self.detail_page = DetailPage(self)
        self.player_page = PlayerPage(self)
        self.favorites_page = FavoritesPage(self)
        self.history_page = HistoryPage(self)

        self.stack.addWidget(self.home_page)       # 0
        self.stack.addWidget(self.category_page)   # 1
        self.stack.addWidget(self.search_page)     # 2
        self.stack.addWidget(self.detail_page)     # 3
        self.stack.addWidget(self.player_page)     # 4
        self.stack.addWidget(self.favorites_page)  # 5
        self.stack.addWidget(self.history_page)    # 6

        # 右侧布局
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        right_layout.addWidget(title_bar)
        right_layout.addWidget(self.stack, 1)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        parent_layout.addWidget(right_widget, 1)

    def _navigate_to(self, page_id):
        """导航到指定页面"""
        # 更新导航按钮状态
        for pid, btn in self.nav_buttons.items():
            btn.setChecked(pid == page_id)

        page_map = {
            "home": (0, "首页"),
            "movie": (1, "电影"),
            "tv": (1, "电视剧"),
            "anime": (1, "动漫"),
            "variety": (1, "综艺"),
            "search": (2, "搜索"),
            "favorites": (5, "我的收藏"),
            "history": (6, "观看历史"),
        }

        if page_id in page_map:
            index, title = page_map[page_id]
            self.stack.setCurrentIndex(index)
            self.page_title.setText(title)
            self.current_page = page_id

            # 分类页面需要传入类型
            if page_id in ("movie", "tv", "anime", "variety"):
                self.category_page.load_category(page_id)

        self.status_bar.showMessage(f"当前页面: {title}")

    def show_detail(self, video_id):
        """显示影视详情"""
        self.stack.setCurrentIndex(3)
        self.page_title.setText("影视详情")
        self.detail_page.load_detail(video_id)

        # 取消所有导航按钮选中
        for btn in self.nav_buttons.values():
            btn.setChecked(False)

    def show_player(self, url, title=""):
        """显示播放器"""
        self.stack.setCurrentIndex(4)
        self.page_title.setText(f"正在播放: {title}")
        self.player_page.play(url, title)

        for btn in self.nav_buttons.values():
            btn.setChecked(False)

    def go_back(self):
        """返回上一页"""
        self._navigate_to(self.current_page)

    def _toggle_theme(self):
        """切换主题"""
        current = self.config.theme
        new_theme = "light" if current == "dark" else "dark"
        self.config.theme = new_theme
        self._apply_theme()

    def _apply_theme(self):
        """应用主题"""
        ThemeManager.apply(self.config.theme)
        if self.config.theme == "dark":
            self.theme_btn.setText("  🌙  暗色主题")
        else:
            self.theme_btn.setText("  ☀️  亮色主题")

    def _toggle_maximize(self):
        """切换最大化"""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def mousePressEvent(self, event):
        """鼠标按下事件 - 拖动窗口"""
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().y() < 40:
                self._drag_pos = event.globalPosition() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        """鼠标移动事件 - 拖动窗口"""
        if hasattr(self, '_drag_pos') and event.buttons() == Qt.MouseButton.LeftButton:
            if event.position().y() < 40:
                self.move(event.globalPosition() - self._drag_pos)
                event.accept()

    def mouseDoubleClickEvent(self, event):
        """双击标题栏最大化"""
        if event.position().y() < 40:
            self._toggle_maximize()

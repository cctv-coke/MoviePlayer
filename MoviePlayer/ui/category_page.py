# -*- coding: utf-8 -*-
"""
分类浏览页 - 电影/电视剧/动漫/综艺
参考樱花动漫的分类布局
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QLabel, QGridLayout, QFrame, QPushButton, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from ui.home_page import MovieCard
from core.api import MovieAPI


class LoadThread(QThread):
    """数据加载线程"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, category, page=1):
        super().__init__()
        self.category = category
        self.page = page

    def run(self):
        try:
            api = MovieAPI()
            data = api.get_category_list(self.category, self.page)
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))


class CategoryPage(QWidget):
    """分类浏览页"""

    CATEGORY_NAMES = {
        "movie": "电影",
        "tv": "电视剧",
        "anime": "动漫",
        "variety": "综艺",
    }

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_category = "movie"
        self.current_page = 1
        self.total_pages = 1
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # 分类标签
        tag_layout = QHBoxLayout()
        tag_layout.setSpacing(10)

        categories = [
            ("movie", "🎬 电影"),
            ("tv", "📺 电视剧"),
            ("anime", "🎌 动漫"),
            ("variety", "🎤 综艺"),
        ]

        self.tag_buttons = {}
        for cat_id, text in categories:
            btn = QPushButton(text)
            btn.setObjectName("categoryTag")
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, c=cat_id: self.load_category(c))
            tag_layout.addWidget(btn)
            self.tag_buttons[cat_id] = btn

        self.tag_buttons["movie"].setChecked(True)
        tag_layout.addStretch()
        layout.addLayout(tag_layout)

        # 加载提示
        self.loading_label = QLabel("⏳ 正在加载...")
        self.loading_label.setObjectName("loadingLabel")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_label)

        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.container = QWidget()
        self.grid_layout = QGridLayout(self.container)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(15)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        scroll.setWidget(self.container)
        layout.addWidget(scroll, 1)

        # 分页
        self.page_layout = QHBoxLayout()
        self.page_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.page_layout.setSpacing(8)
        layout.addLayout(self.page_layout)

    def load_category(self, category):
        """加载分类"""
        self.current_category = category
        self.current_page = 1

        # 更新标签状态
        for cat_id, btn in self.tag_buttons.items():
            btn.setChecked(cat_id == category)

        # 清空网格
        self._clear_grid()
        self.loading_label.show()
        self.loading_label.setText("⏳ 正在加载...")

        # 启动加载线程
        self._load_thread = LoadThread(category, 1)
        self._load_thread.finished.connect(self._on_data_loaded)
        self._load_thread.error.connect(self._on_error)
        self._load_thread.start()

    def _clear_grid(self):
        """清空网格"""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        # 清空分页
        while self.page_layout.count():
            item = self.page_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def _on_data_loaded(self, data):
        """数据加载完成"""
        self.loading_label.hide()
        movies = data.get("list", [])
        self.total_pages = data.get("pagecount", 1)

        # 每行6个
        cols = 6
        for i, movie in enumerate(movies):
            card = MovieCard(movie)
            card.clicked.connect(self._on_card_click)
            row = i // cols
            col = i % cols
            self.grid_layout.addWidget(card, row, col)

        # 创建分页按钮
        self._create_pagination()

    def _on_error(self, error_msg):
        """加载失败"""
        self.loading_label.setText(f"❌ 加载失败: {error_msg}")

    def _create_pagination(self):
        """创建分页按钮"""
        while self.page_layout.count():
            item = self.page_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        if self.total_pages <= 1:
            return

        # 上一页
        prev_btn = QPushButton("◀ 上一页")
        prev_btn.setObjectName("pageBtn")
        prev_btn.setEnabled(self.current_page > 1)
        prev_btn.clicked.connect(lambda: self._go_to_page(self.current_page - 1))
        self.page_layout.addWidget(prev_btn)

        # 页码按钮
        max_show = 7
        start = max(1, self.current_page - max_show // 2)
        end = min(self.total_pages + 1, start + max_show)
        if end - start < max_show:
            start = max(1, end - max_show)

        for page in range(start, end):
            btn = QPushButton(str(page))
            btn.setObjectName("pageBtn")
            btn.setCheckable(True)
            btn.setChecked(page == self.current_page)
            btn.clicked.connect(lambda checked, p=page: self._go_to_page(p))
            self.page_layout.addWidget(btn)

        # 下一页
        next_btn = QPushButton("下一页 ▶")
        next_btn.setObjectName("pageBtn")
        next_btn.setEnabled(self.current_page < self.total_pages)
        next_btn.clicked.connect(lambda: self._go_to_page(self.current_page + 1))
        self.page_layout.addWidget(next_btn)

    def _go_to_page(self, page):
        """跳转页码"""
        if page < 1 or page > self.total_pages or page == self.current_page:
            return
        self.current_page = page
        self._clear_grid()
        self.loading_label.show()

        thread = LoadThread(self.current_category, page)
        thread.finished.connect(self._on_data_loaded)
        thread.error.connect(self._on_error)
        thread.start()

    def _on_card_click(self, movie_data):
        """卡片点击"""
        video_id = movie_data.get("id")
        if video_id:
            self.main_window.show_detail(video_id)

# -*- coding: utf-8 -*-
"""
搜索页
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QLabel, QGridLayout, QFrame, QLineEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from ui.home_page import MovieCard
from core.api import MovieAPI


class SearchThread(QThread):
    """搜索线程"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, keyword, page=1):
        super().__init__()
        self.keyword = keyword
        self.page = page

    def run(self):
        try:
            api = MovieAPI()
            data = api.search(self.keyword, self.page)
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))


class SearchPage(QWidget):
    """搜索页"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_keyword = ""
        self.current_page = 1
        self.total_pages = 1
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # 搜索框
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)

        self.search_edit = QLineEdit()
        self.search_edit.setObjectName("searchEdit")
        self.search_edit.setPlaceholderText("🔍 输入电影、电视剧、动漫名称...")
        self.search_edit.setClearButtonEnabled(True)
        self.search_edit.returnPressed.connect(self.do_search)
        search_layout.addWidget(self.search_edit)

        search_btn = QPushButton("搜索")
        search_btn.setObjectName("primaryBtn")
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.clicked.connect(lambda: self.do_search())
        search_layout.addWidget(search_btn)

        layout.addLayout(search_layout)

        # 搜索结果提示
        self.result_label = QLabel("输入关键词开始搜索")
        self.result_label.setObjectName("loadingLabel")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result_label)

        # 结果网格
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

    def do_search(self, keyword=None):
        """执行搜索"""
        if keyword:
            self.search_edit.setText(keyword)
        kw = self.search_edit.text().strip()
        if not kw:
            return

        self.current_keyword = kw
        self.current_page = 1
        self._clear_results()
        self.result_label.setText(f"⏳ 正在搜索 \"{kw}\"...")

        thread = SearchThread(kw, 1)
        thread.finished.connect(self._on_search_done)
        thread.error.connect(self._on_error)
        thread.start()

    def _clear_results(self):
        """清空结果"""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        while self.page_layout.count():
            item = self.page_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def _on_search_done(self, data):
        """搜索完成"""
        movies = data.get("list", [])
        total = data.get("total", 0)
        self.total_pages = data.get("pagecount", 1)

        if not movies:
            self.result_label.setText(f"未找到 \"{self.current_keyword}\" 的相关结果")
            return

        self.result_label.setText(f"搜索 \"{self.current_keyword}\" 找到 {total} 个结果")

        cols = 6
        for i, movie in enumerate(movies):
            card = MovieCard(movie)
            card.clicked.connect(self._on_card_click)
            row = i // cols
            col = i % cols
            self.grid_layout.addWidget(card, row, col)

        self._create_pagination()

    def _on_error(self, error_msg):
        self.result_label.setText(f"❌ 搜索失败: {error_msg}")

    def _create_pagination(self):
        """创建分页"""
        while self.page_layout.count():
            item = self.page_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        if self.total_pages <= 1:
            return

        prev_btn = QPushButton("◀ 上一页")
        prev_btn.setObjectName("pageBtn")
        prev_btn.setEnabled(self.current_page > 1)
        prev_btn.clicked.connect(lambda: self._go_page(self.current_page - 1))
        self.page_layout.addWidget(prev_btn)

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
            btn.clicked.connect(lambda checked, p=page: self._go_page(p))
            self.page_layout.addWidget(btn)

        next_btn = QPushButton("下一页 ▶")
        next_btn.setObjectName("pageBtn")
        next_btn.setEnabled(self.current_page < self.total_pages)
        next_btn.clicked.connect(lambda: self._go_page(self.current_page + 1))
        self.page_layout.addWidget(next_btn)

    def _go_page(self, page):
        if page < 1 or page > self.total_pages or page == self.current_page:
            return
        self.current_page = page
        self._clear_results()
        self.result_label.setText(f"⏳ 正在搜索第{page}页...")

        thread = SearchThread(self.current_keyword, page)
        thread.finished.connect(self._on_search_done)
        thread.error.connect(self._on_error)
        thread.start()

    def _on_card_click(self, movie_data):
        video_id = movie_data.get("id")
        if video_id:
            self.main_window.show_detail(video_id)

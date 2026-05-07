# -*- coding: utf-8 -*-
"""
首页 - 轮播Banner + 各分类推荐
参考网飞猫首页布局
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QLabel, QGridLayout, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPixmap, QImage, QFont

from core.api import MovieAPI


class BannerWidget(QFrame):
    """轮播Banner组件"""
    clicked = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("bannerContainer")
        self.setFixedHeight(320)
        self.items = []
        self.current_index = 0
        self._init_ui()

        # 自动轮播
        self.timer = QTimer()
        self.timer.timeout.connect(self._next_slide)
        self.timer.start(5000)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.image_label.setStyleSheet("border-radius: 12px;")
        layout.addWidget(self.image_label)

        # 指示器
        self.indicator_layout = QHBoxLayout()
        self.indicator_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.indicator_layout.setSpacing(8)
        layout.addLayout(self.indicator_layout)

    def set_items(self, items):
        """设置轮播项"""
        self.items = items[:5]  # 最多5个
        if self.items:
            self._show_slide(0)

    def _show_slide(self, index):
        """显示指定幻灯片"""
        if not self.items:
            return
        self.current_index = index % len(self.items)
        item = self.items[self.current_index]

        # 显示占位
        self.image_label.setText(
            f"<div style='background: linear-gradient(135deg, #0f3460, #e94560); "
            f"border-radius: 12px; width: 100%; height: 280px; "
            f"display: flex; align-items: center; justify-content: center; "
            f"flex-direction: column; color: white;'>"
            f"<h1 style='font-size: 28px; margin: 10px;'>{item.get('name', '')}</h1>"
            f"<p style='font-size: 14px; opacity: 0.8;'>{item.get('remarks', '')}</p>"
            f"<p style='font-size: 12px; opacity: 0.6; margin-top: 5px;'>{item.get('type', '')} | {item.get('year', '')}</p>"
            f"</div>"
        )
        self.image_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.image_label.mouseReleaseEvent = lambda e: self.clicked.emit(item) if e.button() == Qt.MouseButton.LeftButton else None

        # 更新指示器
        while self.indicator_layout.count():
            item_w = self.indicator_layout.takeAt(0).widget()
            if item_w:
                item_w.deleteLater()

        for i in range(len(self.items)):
            dot = QLabel("●")
            dot.setStyleSheet(
                f"color: {'#e94560' if i == self.current_index else '#666'}; "
                f"font-size: {'14px' if i == self.current_index else '10px'};"
            )
            self.indicator_layout.addWidget(dot)

    def _next_slide(self):
        """下一张"""
        if self.items:
            self._show_slide(self.current_index + 1)


class MovieCard(QFrame):
    """影视卡片组件"""
    clicked = pyqtSignal(dict)

    def __init__(self, movie_data, parent=None):
        super().__init__(parent)
        self.movie_data = movie_data
        self.setObjectName("movieCard")
        self.setFixedSize(160, 240)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        # 海报区域
        poster = QLabel()
        poster.setFixedSize(148, 190)
        poster.setAlignment(Qt.AlignmentFlag.AlignCenter)

        name = self.movie_data.get("name", "未知")
        remarks = self.movie_data.get("remarks", "")
        vod_type = self.movie_data.get("type", "")
        year = self.movie_data.get("year", "")

        poster.setStyleSheet(f"""
            QLabel {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a4e, stop:1 #0f3460);
                border-radius: 8px;
                color: white;
                font-size: 13px;
                font-weight: bold;
            }}
        """)
        poster.setText(
            f"<div style='width:100%;height:100%;display:flex;flex-direction:column;"
            f"align-items:center;justify-content:center;padding:10px;'>"
            f"<p style='font-size:14px;text-align:center;word-wrap:break-word;'>{name}</p>"
            f"</div>"
        )
        layout.addWidget(poster)

        # 备注标签（如"更新至第10集"）
        if remarks:
            remarks_label = QLabel(remarks)
            remarks_label.setObjectName("remarksLabel")
            remarks_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(remarks_label)

        # 名称
        title = QLabel(name)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 12px; font-weight: bold;")
        title.setWordWrap(True)
        title.setMaximumHeight(36)
        layout.addWidget(title)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.movie_data)


class SectionWidget(QFrame):
    """分区组件 - 标题 + 横向滚动卡片列表"""
    card_clicked = pyqtSignal(dict)

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.title_text = title
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setSpacing(10)

        # 标题行
        title_layout = QHBoxLayout()
        title = QLabel(self.title_text)
        title.setObjectName("sectionTitle")
        title_layout.addWidget(title)
        title_layout.addStretch()
        layout.addLayout(title_layout)

        # 卡片滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(270)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        self.cards_layout = QHBoxLayout(container)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(12)
        self.cards_layout.addStretch()

        scroll.setWidget(container)
        layout.addWidget(scroll)

    def set_movies(self, movies):
        """设置电影列表"""
        # 清除旧卡片
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        for movie in movies:
            card = MovieCard(movie)
            card.clicked.connect(self.card_clicked.emit)
            self.cards_layout.addWidget(card)

        self.cards_layout.addStretch()


class HomePage(QWidget):
    """首页"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.api = MovieAPI()
        self._init_ui()
        # 延迟加载数据
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(100, self.load_data)

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(20)

        # 搜索框
        search_layout = QHBoxLayout()
        search_layout.setSpacing(10)
        self.search_edit = self._create_search_box()
        self.search_edit.returnPressed.connect(self._do_search)
        search_layout.addStretch()
        search_layout.addWidget(self.search_edit)
        search_layout.addStretch()
        layout.addLayout(search_layout)

        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        self.content_layout = QVBoxLayout(container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)

        # Banner
        self.banner = BannerWidget()
        self.banner.clicked.connect(self._on_banner_click)
        self.content_layout.addWidget(self.banner)

        # 加载提示
        self.loading_label = QLabel("⏳ 正在加载推荐内容...")
        self.loading_label.setObjectName("loadingLabel")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.content_layout.addWidget(self.loading_label)

        self.content_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll, 1)

    def _create_search_box(self):
        """创建搜索框"""
        from PyQt6.QtWidgets import QLineEdit
        edit = QLineEdit()
        edit.setObjectName("searchEdit")
        edit.setPlaceholderText("🔍 搜索电影、电视剧、动漫...")
        edit.setFixedWidth(500)
        edit.setClearButtonEnabled(True)
        return edit

    def _do_search(self):
        """执行搜索"""
        keyword = self.search_edit.text().strip()
        if keyword:
            self.main_window._navigate_to("search")
            self.main_window.search_page.do_search(keyword)

    def load_data(self):
        """加载首页数据"""
        try:
            data = self.api.get_home_recommend()
            self.loading_label.hide()

            # 设置Banner
            all_movies = []
            for movies in data.values():
                all_movies.extend(movies[:3])
            if all_movies:
                self.banner.set_items(all_movies[:5])

            # 创建各分区
            section_names = {
                "最新电影": "🎬 最新电影",
                "最新电视剧": "📺 热播电视剧",
                "最新动漫": "🎌 热门动漫",
                "最新综艺": "🎤 热门综艺",
            }

            for key, display_name in section_names.items():
                movies = data.get(key, [])
                if movies:
                    section = SectionWidget(display_name)
                    section.card_clicked.connect(self._on_card_click)
                    section.set_movies(movies)
                    # 插入到stretch之前
                    self.content_layout.insertWidget(
                        self.content_layout.count() - 1, section
                    )

        except Exception as e:
            self.loading_label.setText(f"❌ 加载失败: {str(e)}")

    def _on_card_click(self, movie_data):
        """卡片点击"""
        video_id = movie_data.get("id")
        if video_id:
            self.main_window.show_detail(video_id)

    def _on_banner_click(self, movie_data):
        """Banner点击"""
        self._on_card_click(movie_data)

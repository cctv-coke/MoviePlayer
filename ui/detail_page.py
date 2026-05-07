# -*- coding: utf-8 -*-
"""
影视详情页 - 海报/简介/选集/线路切换
参考网飞猫的详情页布局
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QLabel, QFrame, QPushButton, QGridLayout, QTabWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

from core.api import MovieAPI


class DetailThread(QThread):
    """详情加载线程"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, video_id):
        super().__init__()
        self.video_id = video_id

    def run(self):
        try:
            api = MovieAPI()
            data = api.get_detail(self.video_id)
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))


class DetailPage(QWidget):
    """影视详情页"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.detail_data = None
        self.current_source_index = 0
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # 返回按钮
        back_btn = QPushButton("◀ 返回")
        back_btn.setObjectName("navBtn")
        back_btn.setFixedWidth(100)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.main_window.go_back)
        layout.addWidget(back_btn)

        # 加载提示
        self.loading_label = QLabel("⏳ 正在加载详情...")
        self.loading_label.setObjectName("loadingLabel")
        self.loading_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_label)

        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.container = QWidget()
        self.content_layout = QVBoxLayout(self.container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)

        scroll.setWidget(self.container)
        layout.addWidget(scroll, 1)

    def load_detail(self, video_id):
        """加载详情"""
        self._clear_content()
        self.loading_label.show()
        self.loading_label.setText("⏳ 正在加载详情...")

        thread = DetailThread(video_id)
        thread.finished.connect(self._on_detail_loaded)
        thread.error.connect(self._on_error)
        thread.start()

    def _clear_content(self):
        """清空内容"""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

    def _on_detail_loaded(self, data):
        """详情加载完成"""
        self.loading_label.hide()
        if not data:
            self.loading_label.setText("❌ 未找到详情信息")
            self.loading_label.show()
            return

        self.detail_data = data
        self._build_detail_ui(data)

    def _on_error(self, error_msg):
        self.loading_label.setText(f"❌ 加载失败: {error_msg}")
        self.loading_label.show()

    def _build_detail_ui(self, data):
        """构建详情UI"""
        # ===== 顶部信息区 =====
        info_frame = QFrame()
        info_frame.setObjectName("detailInfo")
        info_layout = QHBoxLayout(info_frame)
        info_layout.setContentsMargins(20, 20, 20, 20)
        info_layout.setSpacing(25)

        # 海报
        poster_frame = QFrame()
        poster_frame.setFixedSize(200, 280)
        poster_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a4e, stop:1 #0f3460);
                border-radius: 10px;
            }
        """)
        poster_layout = QVBoxLayout(poster_frame)
        poster_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        poster_label = QLabel("🎬")
        poster_label.setStyleSheet("font-size: 48px;")
        poster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        poster_layout.addWidget(poster_label)
        info_layout.addWidget(poster_frame)

        # 信息
        info_right = QVBoxLayout()
        info_right.setSpacing(8)

        # 名称
        name = data.get("name", "未知")
        name_label = QLabel(name)
        name_label.setFont(None)
        name_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        info_right.addWidget(name_label)

        # 评分
        score = data.get("score", "")
        if score:
            score_label = QLabel(f"⭐ 评分: {score}")
            score_label.setObjectName("scoreLabel")
            info_right.addWidget(score_label)

        # 元信息
        meta_parts = []
        for key, label in [("type", "类型"), ("year", "年份"), ("area", "地区"), ("lang", "语言")]:
            val = data.get(key, "")
            if val:
                meta_parts.append(f"{label}: {val}")
        if meta_parts:
            meta_label = QLabel("  |  ".join(meta_parts))
            meta_label.setStyleSheet("color: #999; font-size: 13px;")
            info_right.addWidget(meta_label)

        # 备注
        remarks = data.get("remarks", "")
        if remarks:
            remarks_label = QLabel(remarks)
            remarks_label.setObjectName("remarksLabel")
            info_right.addWidget(remarks_label)

        # 导演
        director = data.get("director", "")
        if director:
            info_right.addWidget(QLabel(f"🎬 导演: {director}"))

        # 演员
        actor = data.get("actor", "")
        if actor:
            actor_label = QLabel(f"🎭 演员: {actor}")
            actor_label.setWordWrap(True)
            actor_label.setStyleSheet("font-size: 12px; color: #aaa;")
            info_right.addWidget(actor_label)

        # 简介
        content = data.get("content", "")
        if content:
            # 去除HTML标签
            import re
            clean_content = re.sub(r'<[^>]+>', '', content)
            if len(clean_content) > 200:
                clean_content = clean_content[:200] + "..."

            desc_title = QLabel("📖 简介")
            desc_title.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
            info_right.addWidget(desc_title)

            desc_label = QLabel(clean_content)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("font-size: 12px; color: #aaa; line-height: 1.6;")
            info_right.addWidget(desc_label)

        info_right.addStretch()
        info_layout.addLayout(info_right, 1)

        self.content_layout.addWidget(info_frame)

        # ===== 操作按钮 =====
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        play_btn = QPushButton("▶ 立即播放")
        play_btn.setObjectName("primaryBtn")
        play_btn.setFixedHeight(42)
        play_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        play_btn.clicked.connect(self._play_first)
        btn_layout.addWidget(play_btn)

        fav_btn = QPushButton("❤️ 收藏")
        fav_btn.setObjectName("primaryBtn")
        fav_btn.setFixedHeight(42)
        fav_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        fav_btn.clicked.connect(self._toggle_favorite)
        btn_layout.addWidget(fav_btn)

        btn_layout.addStretch()
        self.content_layout.addLayout(btn_layout)

        # ===== 播放源和选集 =====
        sources = data.get("sources", [])
        if sources:
            # 播放源标签
            source_layout = QHBoxLayout()
            source_layout.setSpacing(10)

            source_title = QLabel("📡 播放线路:")
            source_title.setStyleSheet("font-weight: bold; font-size: 14px;")
            source_layout.addWidget(source_title)

            self.source_buttons = []
            for i, source in enumerate(sources):
                btn = QPushButton(source["source_name"])
                btn.setObjectName("sourceTab")
                btn.setCheckable(True)
                btn.setChecked(i == 0)
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(lambda checked, idx=i: self._switch_source(idx))
                source_layout.addWidget(btn)
                self.source_buttons.append(btn)

            source_layout.addStretch()
            self.content_layout.addLayout(source_layout)

            # 选集区域
            episodes_label = QLabel("📋 选集:")
            episodes_label.setStyleSheet("font-weight: bold; font-size: 14px; margin-top: 10px;")
            self.content_layout.addWidget(episodes_label)

            self.episodes_frame = QFrame()
            self.episodes_layout = QGridLayout(self.episodes_frame)
            self.episodes_layout.setSpacing(8)
            self.episodes_layout.setContentsMargins(0, 0, 0, 0)

            self._show_episodes(sources[0]["episodes"])
            self.content_layout.addWidget(self.episodes_frame)

        self.content_layout.addStretch()

    def _show_episodes(self, episodes):
        """显示选集"""
        # 清空
        while self.episodes_layout.count():
            item = self.episodes_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        cols = 10
        for i, ep in enumerate(episodes):
            btn = QPushButton(ep["name"])
            btn.setObjectName("episodeBtn")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda checked, e=ep: self._play_episode(e))
            row = i // cols
            col = i % cols
            self.episodes_layout.addWidget(btn, row, col)

    def _switch_source(self, index):
        """切换播放源"""
        if not self.detail_data:
            return
        sources = self.detail_data.get("sources", [])
        if index < len(sources):
            for i, btn in enumerate(self.source_buttons):
                btn.setChecked(i == index)
            self._show_episodes(sources[index]["episodes"])

    def _play_episode(self, episode):
        """播放选集"""
        url = episode.get("url", "")
        name = episode.get("name", "")
        title = self.detail_data.get("name", "") if self.detail_data else ""
        self.main_window.show_player(url, f"{title} - {name}")

        # 记录历史
        if self.detail_data:
            self.main_window.config.add_history({
                "id": self.detail_data.get("id"),
                "name": self.detail_data.get("name"),
                "pic": self.detail_data.get("pic"),
                "type": self.detail_data.get("type"),
                "episode": name,
                "time": self._get_time_str(),
            })

    def _play_first(self):
        """播放第一集"""
        if not self.detail_data:
            return
        sources = self.detail_data.get("sources", [])
        if sources and sources[0].get("episodes"):
            self._play_episode(sources[0]["episodes"][0])

    def _toggle_favorite(self):
        """切换收藏"""
        if not self.detail_data:
            return
        self.main_window.config.add_favorite({
            "id": self.detail_data.get("id"),
            "name": self.detail_data.get("name"),
            "pic": self.detail_data.get("pic"),
            "type": self.detail_data.get("type"),
            "remarks": self.detail_data.get("remarks"),
        })

    def _get_time_str(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")

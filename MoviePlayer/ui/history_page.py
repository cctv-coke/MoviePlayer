# -*- coding: utf-8 -*-
"""
历史记录页
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,
    QLabel, QGridLayout, QFrame, QPushButton, QHeaderView, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt

from ui.home_page import MovieCard


class HistoryPage(QWidget):
    """历史记录页"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(15)

        # 标题行
        header = QHBoxLayout()
        title = QLabel("📋 观看历史")
        title.setObjectName("sectionTitle")
        header.addWidget(title)
        header.addStretch()

        clear_btn = QPushButton("🗑️ 清空历史")
        clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        clear_btn.clicked.connect(self._clear_history)
        header.addWidget(clear_btn)
        layout.addLayout(header)

        # 内容区
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

    def showEvent(self, event):
        """显示时刷新"""
        super().showEvent(event)
        self._load_history()

    def _load_history(self):
        """加载历史"""
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()

        history = self.main_window.config.get_history()
        if not history:
            empty_label = QLabel("📭 暂无观看记录")
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty_label.setStyleSheet("color: #888; font-size: 16px; padding: 50px;")
            self.grid_layout.addWidget(empty_label, 0, 0)
            return

        cols = 6
        for i, item in enumerate(history):
            card = MovieCard(item)
            card.clicked.connect(self._on_card_click)
            row = i // cols
            col = i % cols
            self.grid_layout.addWidget(card, row, col)

    def _on_card_click(self, movie_data):
        video_id = movie_data.get("id")
        if video_id:
            self.main_window.show_detail(video_id)

    def _clear_history(self):
        """清空历史"""
        from PyQt6.QtWidgets import QMessageBox
        reply = QMessageBox.question(
            self, "确认", "确定要清空观看历史吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.main_window.config.clear_history()
            self._load_history()

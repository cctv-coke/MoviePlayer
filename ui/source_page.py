# -*- coding: utf-8 -*-
"""
源管理页面 - 添加/删除/导入影视源
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QDialog, QLineEdit, QTextEdit,
    QFileDialog, QMessageBox, QGroupBox, QCheckBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from utils.source_manager import SourceManager


class AddSourceDialog(QDialog):
    """添加源对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("添加影视源")
        self.setFixedSize(400, 200)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # 源名称
        layout.addWidget(QLabel("源名称:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("例如: 非凡资源")
        layout.addWidget(self.name_edit)
        
        # 源地址
        layout.addWidget(QLabel("源地址 (API URL):"))
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("例如: http://cj.ffzyapi.com/api.php/provide/vod/")
        layout.addWidget(self.url_edit)
        
        # 按钮
        btn_layout = QHBoxLayout()
        
        test_btn = QPushButton("测试连接")
        test_btn.clicked.connect(self._test_source)
        btn_layout.addWidget(test_btn)
        
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        
        layout.addLayout(btn_layout)
    
    def _test_source(self):
        """测试源"""
        url = self.url_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "提示", "请输入源地址")
            return
        
        from utils.source_manager import SourceManager
        sm = SourceManager()
        success, msg = sm.test_source(url)
        
        if success:
            QMessageBox.information(self, "测试成功", msg)
        else:
            QMessageBox.warning(self, "测试失败", msg)
    
    def get_data(self):
        """获取输入数据"""
        return {
            "name": self.name_edit.text().strip(),
            "url": self.url_edit.text().strip()
        }


class ImportDialog(QDialog):
    """导入源对话框"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("导入影视源")
        self.setFixedSize(500, 300)
        self._init_ui()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        
        # 说明
        info = QLabel("""
支持导入格式:
• TVBox配置文件 (JSON格式，包含sites数组)
• MacCMS源列表

导入方式:
1. 从URL导入 - 输入配置文件的网络地址
2. 从文件导入 - 选择本地JSON文件
        """)
        info.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(info)
        
        # URL导入
        url_group = QGroupBox("从URL导入")
        url_layout = QHBoxLayout(url_group)
        
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("输入配置文件URL...")
        url_layout.addWidget(self.url_edit)
        
        import_url_btn = QPushButton("导入")
        import_url_btn.clicked.connect(self._import_from_url)
        url_layout.addWidget(import_url_btn)
        
        layout.addWidget(url_group)
        
        # 文件导入
        file_group = QGroupBox("从文件导入")
        file_layout = QHBoxLayout(file_group)
        
        self.file_edit = QLineEdit()
        self.file_edit.setPlaceholderText("选择本地JSON文件...")
        file_layout.addWidget(self.file_edit)
        
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self._browse_file)
        file_layout.addWidget(browse_btn)
        
        import_file_btn = QPushButton("导入")
        import_file_btn.clicked.connect(self._import_from_file)
        file_layout.addWidget(import_file_btn)
        
        layout.addWidget(file_group)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _browse_file(self):
        """浏览文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择配置文件", "", "JSON文件 (*.json)"
        )
        if file_path:
            self.file_edit.setText(file_path)
    
    def _import_from_url(self):
        """从URL导入"""
        url = self.url_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "提示", "请输入URL")
            return
        
        sm = SourceManager()
        success, msg = sm.import_from_url(url)
        
        if success:
            QMessageBox.information(self, "导入成功", msg)
            self.accept()
        else:
            QMessageBox.warning(self, "导入失败", msg)
    
    def _import_from_file(self):
        """从文件导入"""
        file_path = self.file_edit.text().strip()
        if not file_path:
            QMessageBox.warning(self, "提示", "请选择文件")
            return
        
        sm = SourceManager()
        success, msg = sm.import_from_file(file_path)
        
        if success:
            QMessageBox.information(self, "导入成功", msg)
            self.accept()
        else:
            QMessageBox.warning(self, "导入失败", msg)


class SourcePage(QWidget):
    """源管理页面"""
    
    source_changed = pyqtSignal()
    
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.source_manager = SourceManager()
        self._init_ui()
        self._load_sources()
    
    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel("📡 影视源管理")
        title.setFont(QFont("Microsoft YaHei", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # 说明
        info = QLabel("可以添加、删除、导入影视源，支持TVBox格式配置")
        info.setStyleSheet("color: #888; margin-bottom: 15px;")
        layout.addWidget(info)
        
        # 源列表
        self.source_list = QListWidget()
        self.source_list.setAlternatingRowColors(True)
        layout.addWidget(self.source_list, 1)
        
        # 按钮区
        btn_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ 添加源")
        add_btn.clicked.connect(self._add_source)
        btn_layout.addWidget(add_btn)
        
        import_btn = QPushButton("📥 导入源")
        import_btn.clicked.connect(self._import_source)
        btn_layout.addWidget(import_btn)
        
        export_btn = QPushButton("📤 导出源")
        export_btn.clicked.connect(self._export_source)
        btn_layout.addWidget(export_btn)
        
        delete_btn = QPushButton("🗑️ 删除源")
        delete_btn.clicked.connect(self._delete_source)
        btn_layout.addWidget(delete_btn)
        
        test_btn = QPushButton("🔍 测试源")
        test_btn.clicked.connect(self._test_source)
        btn_layout.addWidget(test_btn)
        
        layout.addLayout(btn_layout)
        
        # 示例配置
        example_group = QGroupBox("TVBox配置示例")
        example_layout = QVBoxLayout(example_group)
        
        example_text = QTextEdit()
        example_text.setReadOnly(True)
        example_text.setMaximumHeight(120)
        example_text.setPlainText("""{
  "sites": [
    {
      "key": "百度云",
      "name": "百度云资源",
      "type": 1,
      "api": "https://api.apibdzy.com/api.php/provide/vod/",
      "searchable": 1
    }
  ]
}""")
        example_layout.addWidget(example_text)
        
        layout.addWidget(example_group)
    
    def _load_sources(self):
        """加载源列表"""
        self.source_list.clear()
        
        for source in self.source_manager.sources:
            item = QListWidgetItem(f"📡 {source['name']} - {source['url'][:50]}...")
            item.setData(Qt.ItemDataRole.UserRole, source)
            
            if not source.get('enabled', True):
                item.setForeground(Qt.GlobalColor.gray)
            
            self.source_list.addItem(item)
    
    def _add_source(self):
        """添加源"""
        dialog = AddSourceDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if data['name'] and data['url']:
                self.source_manager.add_source(data['name'], data['url'])
                self._load_sources()
                self.source_changed.emit()
                QMessageBox.information(self, "成功", f"已添加源: {data['name']}")
    
    def _import_source(self):
        """导入源"""
        dialog = ImportDialog(self)
        dialog.exec()
        self._load_sources()
        self.source_changed.emit()
    
    def _export_source(self):
        """导出源"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出配置", "sources.json", "JSON文件 (*.json)"
        )
        if file_path:
            import json
            data = self.source_manager.export_sources()
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            QMessageBox.information(self, "成功", f"已导出到: {file_path}")
    
    def _delete_source(self):
        """删除源"""
        current = self.source_list.currentItem()
        if current:
            source = current.data(Qt.ItemDataRole.UserRole)
            reply = QMessageBox.question(
                self, "确认删除",
                f"确定要删除源 '{source['name']}' 吗?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.source_manager.remove_source(source['name'])
                self._load_sources()
                self.source_changed.emit()
    
    def _test_source(self):
        """测试选中的源"""
        current = self.source_list.currentItem()
        if current:
            source = current.data(Qt.ItemDataRole.UserRole)
            success, msg = self.source_manager.test_source(source['url'])
            if success:
                QMessageBox.information(self, "测试成功", msg)
            else:
                QMessageBox.warning(self, "测试失败", msg)

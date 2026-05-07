# -*- coding: utf-8 -*-
"""配置管理模块"""
import json
import os


class Config:
    """应用配置管理"""

    CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".movieplayer")
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
    FAVORITES_FILE = os.path.join(CONFIG_DIR, "favorites.json")
    HISTORY_FILE = os.path.join(CONFIG_DIR, "history.json")

    def __init__(self):
        self._ensure_dir()
        self.data = self._load_config()

    def _ensure_dir(self):
        """确保配置目录存在"""
        os.makedirs(self.CONFIG_DIR, exist_ok=True)

    def _load_config(self):
        """加载配置"""
        default = {
            "theme": "dark",
            "api_source": "default",
            "last_category": "movie",
            "window_geometry": None,
            "playback_speed": 1.0,
            "volume": 80,
        }
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    default.update(data)
            except Exception:
                pass
        return default

    def save(self):
        """保存配置"""
        try:
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    @property
    def theme(self):
        return self.data.get("theme", "dark")

    @theme.setter
    def theme(self, value):
        self.data["theme"] = value
        self.save()

    @property
    def api_source(self):
        return self.data.get("api_source", "default")

    @api_source.setter
    def api_source(self, value):
        self.data["api_source"] = value
        self.save()

    def get_favorites(self):
        """获取收藏列表"""
        if os.path.exists(self.FAVORITES_FILE):
            try:
                with open(self.FAVORITES_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def add_favorite(self, item):
        """添加收藏"""
        favorites = self.get_favorites()
        # 检查是否已收藏
        for fav in favorites:
            if fav.get("id") == item.get("id"):
                return
        favorites.insert(0, item)
        self._save_favorites(favorites)

    def remove_favorite(self, item_id):
        """移除收藏"""
        favorites = self.get_favorites()
        favorites = [f for f in favorites if f.get("id") != item_id]
        self._save_favorites(favorites)

    def _save_favorites(self, favorites):
        try:
            with open(self.FAVORITES_FILE, "w", encoding="utf-8") as f:
                json.dump(favorites, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get_history(self):
        """获取观看历史"""
        if os.path.exists(self.HISTORY_FILE):
            try:
                with open(self.HISTORY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return []

    def add_history(self, item):
        """添加观看历史"""
        history = self.get_history()
        # 移除已存在的相同记录
        history = [h for h in history if h.get("id") != item.get("id")]
        history.insert(0, item)
        # 最多保留200条
        history = history[:200]
        self._save_history(history)

    def clear_history(self):
        """清空观看历史"""
        self._save_history([])

    def _save_history(self, history):
        try:
            with open(self.HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

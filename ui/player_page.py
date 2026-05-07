# -*- coding: utf-8 -*-
"""
视频播放器页 - 内嵌Web播放器
使用WebEngineWidget播放m3u8/mp4视频
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSlider
)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel


class PlayerPage(QWidget):
    """视频播放器页"""

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_url = ""
        self.current_title = ""
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 顶部控制栏
        top_bar = QFrame()
        top_bar.setObjectName("titleBar")
        top_bar.setFixedHeight(45)
        top_bar_layout = QHBoxLayout(top_bar)
        top_bar_layout.setContentsMargins(15, 0, 15, 0)

        back_btn = QPushButton("◀ 返回")
        back_btn.setObjectName("navBtn")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.clicked.connect(self.main_window.go_back)
        top_bar_layout.addWidget(back_btn)

        self.title_label = QLabel("正在播放")
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        top_bar_layout.addWidget(self.title_label, 1)

        # 全屏按钮
        fullscreen_btn = QPushButton("⛶ 全屏")
        fullscreen_btn.setObjectName("navBtn")
        fullscreen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        fullscreen_btn.clicked.connect(self._toggle_fullscreen)
        top_bar_layout.addWidget(fullscreen_btn)

        layout.addWidget(top_bar)

        # Web播放器
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("background-color: black;")
        layout.addWidget(self.web_view, 1)

        # 底部提示
        bottom_bar = QFrame()
        bottom_bar.setFixedHeight(35)
        bottom_bar_layout = QHBoxLayout(bottom_bar)
        bottom_bar_layout.setContentsMargins(15, 0, 15, 0)

        hint_label = QLabel("💡 提示: 如无法播放，请尝试切换其他线路")
        hint_label.setStyleSheet("color: #888; font-size: 11px;")
        bottom_bar_layout.addWidget(hint_label)
        bottom_bar_layout.addStretch()

        layout.addWidget(bottom_bar)

    def play(self, url, title=""):
        """播放视频"""
        self.current_url = url
        self.current_title = title
        self.title_label.setText(f"正在播放: {title}")

        # 使用DPlayer播放器（HLS.js支持m3u8）
        html = self._generate_player_html(url)
        self.web_view.setHtml(html)

    def _generate_player_html(self, url):
        """生成播放器HTML"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Player</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/dplayer@1.27.1/dist/DPlayer.min.css">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ background: #000; width: 100vw; height: 100vh; overflow: hidden; }}
                #dplayer {{ width: 100%; height: 100%; }}
            </style>
        </head>
        <body>
            <div id="dplayer"></div>
            <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
            <script src="https://cdn.jsdelivr.net/npm/dplayer@1.27.1/dist/DPlayer.min.js"></script>
            <script>
                var isHls = false;
                var videoUrl = "{url}";

                if (videoUrl.indexOf('.m3u8') !== -1) {{
                    isHls = true;
                }}

                var options = {{
                    container: document.getElementById('dplayer'),
                    autoplay: true,
                    theme: '#e94560',
                    loop: false,
                    lang: 'zh-cn',
                    screenshot: true,
                    hotkey: true,
                    preload: 'auto',
                    volume: 0.8,
                    playbackSpeed: [0.5, 0.75, 1, 1.25, 1.5, 2],
                    video: {{
                        url: videoUrl,
                        type: isHls ? 'hls' : 'normal',
                    }},
                }};

                if (isHls && typeof Hls !== 'undefined' && Hls.isSupported()) {{
                    options.video.type = 'hls';
                }}

                var dp = new DPlayer(options);

                // 错误处理
                dp.on('error', function() {{
                    console.log('播放错误，尝试普通模式');
                    if (isHls) {{
                        var newDp = new DPlayer({{
                            container: document.getElementById('dplayer'),
                            autoplay: true,
                            theme: '#e94560',
                            video: {{
                                url: videoUrl,
                                type: 'normal',
                            }}
                        }});
                    }}
                }});
            </script>
        </body>
        </html>
        """

    def _toggle_fullscreen(self):
        """切换全屏"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def cleanup(self):
        """清理资源"""
        self.web_view.stop()
        self.web_view.setHtml("<html><body style='background:black'></body></html>")

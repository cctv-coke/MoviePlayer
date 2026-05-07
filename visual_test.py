# -*- coding: utf-8 -*-
"""
可视化测试 - 生成界面截图/预览
无需运行GUI即可查看界面布局
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def generate_html_preview():
    """生成HTML界面预览"""
    
    dark_theme = """
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Microsoft YaHei', sans-serif; 
            background: #1a1a2e;
            color: #e0e0e0;
            padding: 20px;
        }
        .window {
            width: 1200px;
            height: 700px;
            background: #16213e;
            border-radius: 10px;
            display: flex;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        .sidebar {
            width: 200px;
            background: #0f3460;
            padding: 20px 10px;
        }
        .logo {
            text-align: center;
            font-size: 18px;
            font-weight: bold;
            padding: 15px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 15px;
        }
        .nav-item {
            padding: 12px 20px;
            margin: 5px 0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 14px;
        }
        .nav-item:hover {
            background: rgba(233, 69, 96, 0.15);
            color: #e94560;
        }
        .nav-item.active {
            background: rgba(233, 69, 96, 0.25);
            color: #e94560;
            border-left: 3px solid #e94560;
        }
        .main {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .header {
            height: 50px;
            background: #0a1628;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
        }
        .search-box {
            background: #1a1a4e;
            border: 2px solid #2a2a5e;
            border-radius: 20px;
            padding: 8px 20px;
            width: 400px;
            color: #888;
            font-size: 13px;
        }
        .content {
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }
        .banner {
            height: 280px;
            background: linear-gradient(135deg, #0f3460, #e94560);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 25px;
            position: relative;
        }
        .banner-content {
            text-align: center;
        }
        .banner h2 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .banner p {
            opacity: 0.8;
            font-size: 14px;
        }
        .section-title {
            font-size: 20px;
            font-weight: bold;
            margin: 20px 0 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .movie-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 15px;
        }
        .movie-card {
            background: #16213e;
            border: 1px solid #2a2a5e;
            border-radius: 10px;
            overflow: hidden;
            cursor: pointer;
            transition: all 0.3s;
        }
        .movie-card:hover {
            border-color: #e94560;
            transform: translateY(-5px);
        }
        .poster {
            height: 180px;
            background: linear-gradient(135deg, #1a1a4e, #0f3460);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 40px;
        }
        .card-info {
            padding: 10px;
        }
        .card-title {
            font-size: 13px;
            font-weight: bold;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .card-tag {
            display: inline-block;
            background: rgba(233, 69, 96, 0.15);
            color: #e94560;
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 4px;
            margin-top: 5px;
        }
        .theme-toggle {
            margin-top: auto;
            padding: 15px 0;
            border-top: 1px solid rgba(255,255,255,0.1);
        }
    </style>
    """
    
    light_theme = dark_theme.replace('#1a1a2e', '#f5f5f7').replace('#16213e', '#ffffff').replace('#0f3460', '#ffffff').replace('#e94560', '#ff4757').replace('#0a1628', '#ffffff').replace('#e0e0e0', '#333333').replace('#888', '#666').replace('#1a1a4e', '#f0f0f5').replace('#2a2a5e', '#e0e0e5').replace('rgba(233, 69, 96, 0.15)', 'rgba(255, 71, 87, 0.08)').replace('rgba(233, 69, 96, 0.25)', 'rgba(255, 71, 87, 0.12)')
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>影视播放器 - 界面预览</title>
    {dark_theme}
</head>
<body>
    <h1 style="text-align: center; margin-bottom: 30px;">🎬 影视播放器 - 界面预览</h1>
    
    <div class="window">
        <div class="sidebar">
            <div class="logo">🎬 影视播放器</div>
            <div class="nav-item active">🏠 首页</div>
            <div class="nav-item">🎬 电影</div>
            <div class="nav-item">📺 电视剧</div>
            <div class="nav-item">🎌 动漫</div>
            <div class="nav-item">🎤 综艺</div>
            <div class="nav-item">🔍 搜索</div>
            <div class="nav-item">❤️ 收藏</div>
            <div class="nav-item">📋 历史</div>
            <div class="theme-toggle">
                <div class="nav-item">🌙 暗色主题</div>
            </div>
        </div>
        <div class="main">
            <div class="header">
                <span style="font-weight: bold;">首页</span>
                <div class="search-box">🔍 搜索电影、电视剧、动漫...</div>
                <span>— □ ✕</span>
            </div>
            <div class="content">
                <div class="banner">
                    <div class="banner-content">
                        <h2>赎梦</h2>
                        <p>张家辉导演作品 | 2024 | 剧情片</p>
                    </div>
                </div>
                
                <div class="section-title">🎬 最新电影</div>
                <div class="movie-grid">
                    <div class="movie-card">
                        <div class="poster">🎬</div>
                        <div class="card-info">
                            <div class="card-title">赎梦</div>
                            <span class="card-tag">HD</span>
                        </div>
                    </div>
                    <div class="movie-card">
                        <div class="poster">🎬</div>
                        <div class="card-info">
                            <div class="card-title">魅力航班第二季</div>
                            <span class="card-tag">更新至10集</span>
                        </div>
                    </div>
                    <div class="movie-card">
                        <div class="poster">🎬</div>
                        <div class="card-info">
                            <div class="card-title">逾梦深情</div>
                            <span class="card-tag">完结</span>
                        </div>
                    </div>
                    <div class="movie-card">
                        <div class="poster">🎬</div>
                        <div class="card-info">
                            <div class="card-title">一个真正的女人</div>
                            <span class="card-tag">更新中</span>
                        </div>
                    </div>
                    <div class="movie-card">
                        <div class="poster">🎬</div>
                        <div class="card-info">
                            <div class="card-title">蓝天伙伴</div>
                            <span class="card-tag">HD</span>
                        </div>
                    </div>
                    <div class="movie-card">
                        <div class="poster">🎬</div>
                        <div class="card-info">
                            <div class="card-title">流浪地球</div>
                            <span class="card-tag">4K</span>
                        </div>
                    </div>
                </div>
                
                <div class="section-title">📺 热播电视剧</div>
                <div class="movie-grid">
                    <div class="movie-card">
                        <div class="poster">📺</div>
                        <div class="card-info">
                            <div class="card-title">三体</div>
                            <span class="card-tag">完结</span>
                        </div>
                    </div>
                    <div class="movie-card">
                        <div class="poster">📺</div>
                        <div class="card-info">
                            <div class="card-title">狂飙</div>
                            <span class="card-tag">完结</span>
                        </div>
                    </div>
                    <div class="movie-card">
                        <div class="poster">📺</div>
                        <div class="card-info">
                            <div class="card-title">漫长的季节</div>
                            <span class="card-tag">完结</span>
                        </div>
                    </div>
                    <div class="movie-card">
                        <div class="poster">📺</div>
                        <div class="card-info">
                            <div class="card-title">繁花</div>
                            <span class="card-tag">完结</span>
                        </div>
                    </div>
                    <div class="movie-card">
                        <div class="poster">📺</div>
                        <div class="card-info">
                            <div class="card-title">庆余年2</div>
                            <span class="card-tag">更新中</span>
                        </div>
                    </div>
                    <div class="movie-card">
                        <div class="poster">📺</div>
                        <div class="card-info">
                            <div class="card-title">与凤行</div>
                            <span class="card-tag">完结</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 30px; color: #888;">
        <p>📐 窗口尺寸: 1200×700 | 🎨 主题: 暗色模式</p>
        <p>🎯 参考设计: 网飞猫 + TVBox + 樱花动漫</p>
    </div>
</body>
</html>"""
    
    return html_content

def generate_detail_preview():
    """生成详情页预览"""
    
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>影视详情 - 预览</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Microsoft YaHei', sans-serif; 
            background: #1a1a2e;
            color: #e0e0e0;
            padding: 20px;
        }
        .detail-container {
            max-width: 1000px;
            margin: 0 auto;
            background: #16213e;
            border-radius: 12px;
            padding: 30px;
        }
        .back-btn {
            display: inline-block;
            padding: 8px 20px;
            background: transparent;
            border: none;
            color: #e94560;
            cursor: pointer;
            margin-bottom: 20px;
        }
        .info-section {
            display: flex;
            gap: 30px;
            margin-bottom: 30px;
        }
        .poster {
            width: 200px;
            height: 280px;
            background: linear-gradient(135deg, #1a1a4e, #0f3460);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
        }
        .info {
            flex: 1;
        }
        .title {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .score {
            color: #ffd700;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .meta {
            color: #888;
            font-size: 13px;
            margin-bottom: 10px;
        }
        .tag {
            display: inline-block;
            background: rgba(233, 69, 96, 0.15);
            color: #e94560;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            margin-bottom: 15px;
        }
        .desc {
            color: #aaa;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        .action-btns {
            display: flex;
            gap: 15px;
        }
        .btn-primary {
            background: #e94560;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
        }
        .btn-secondary {
            background: transparent;
            border: 1px solid #e94560;
            color: #e94560;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 14px;
            cursor: pointer;
        }
        .source-tabs {
            display: flex;
            gap: 20px;
            border-bottom: 1px solid #2a2a5e;
            margin-bottom: 20px;
        }
        .source-tab {
            padding: 10px 20px;
            border-bottom: 2px solid transparent;
            cursor: pointer;
        }
        .source-tab.active {
            color: #e94560;
            border-bottom-color: #e94560;
        }
        .episodes {
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            gap: 10px;
        }
        .episode {
            background: #1a1a4e;
            border: 1px solid #2a2a5e;
            padding: 10px;
            text-align: center;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
        }
        .episode:hover {
            border-color: #e94560;
            color: #e94560;
        }
    </style>
</head>
<body>
    <div class="detail-container">
        <div class="back-btn">◀ 返回</div>
        
        <div class="info-section">
            <div class="poster">🎬</div>
            <div class="info">
                <div class="title">赎梦</div>
                <div class="score">⭐ 评分: 7.5</div>
                <div class="meta">类型: 剧情片 | 年份: 2024 | 地区: 香港</div>
                <div class="tag">HD国语版</div>
                <div class="desc">
                    📖 简介: 张家辉执导并主演的犯罪剧情片。讲述了一个关于救赎与梦想的故事，
                    展现了人性的复杂与挣扎。影片节奏紧凑，演技精湛，是一部值得一看的佳作...
                </div>
                <div class="action-btns">
                    <button class="btn-primary">▶ 立即播放</button>
                    <button class="btn-secondary">❤️ 收藏</button>
                </div>
            </div>
        </div>
        
        <div class="source-tabs">
            <div class="source-tab active">📡 非凡资源</div>
            <div class="source-tab">📡 ffm3u8</div>
        </div>
        
        <h3 style="margin-bottom: 15px;">📋 选集</h3>
        <div class="episodes">
            <div class="episode">国语版</div>
            <div class="episode">粤语版</div>
            <div class="episode">预告片</div>
        </div>
    </div>
    
    <div style="text-align: center; margin-top: 30px; color: #888;">
        <p>🎬 详情页预览 | 支持多线路切换</p>
    </div>
</body>
</html>"""
    
    return html

def main():
    """主函数"""
    print("=" * 60)
    print("🎨 影视播放器 - 可视化测试")
    print("=" * 60)
    
    # 生成首页预览
    print("\n📄 生成首页预览...")
    home_html = generate_html_preview()
    home_path = "/workspace/MoviePlayer/preview_home.html"
    with open(home_path, 'w', encoding='utf-8') as f:
        f.write(home_html)
    print(f"   ✅ 已保存: {home_path}")
    
    # 生成详情页预览
    print("\n📄 生成详情页预览...")
    detail_html = generate_detail_preview()
    detail_path = "/workspace/MoviePlayer/preview_detail.html"
    with open(detail_path, 'w', encoding='utf-8') as f:
        f.write(detail_html)
    print(f"   ✅ 已保存: {detail_path}")
    
    print("\n" + "=" * 60)
    print("📊 生成完成!")
    print("=" * 60)
    print(f"""
🎯 预览文件:
   • 首页布局: {home_path}
   • 详情页面: {detail_path}

💡 使用方式:
   1. 在浏览器中打开 HTML 文件查看界面效果
   2. 对比实际运行效果 (python run.py)
   
🎨 设计特点:
   • 暗色主题: 深蓝背景 + 红色强调色
   • 卡片布局: 6列网格展示
   • 侧边导航: 8个主要功能入口
   • 响应式: 自适应窗口大小
""")

if __name__ == "__main__":
    main()

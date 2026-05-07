# -*- coding: utf-8 -*-
"""
测试脚本 - 验证核心功能（无需GUI）
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_api():
    """测试API聚合功能"""
    print("=" * 50)
    print("📡 测试API聚合功能")
    print("=" * 50)
    
    from core.api import MovieAPI
    api = MovieAPI()
    
    # 测试获取最新列表
    print("\n📂 测试获取最新列表...")
    result = api.get_category_list("movie", page=1)
    movies = result.get("list", [])
    print(f"   获取到 {len(movies)} 条数据")
    
    if movies:
        print("\n   前5条数据:")
        for i, movie in enumerate(movies[:5]):
            print(f"   [{i+1}] {movie.get('name')} ({movie.get('year', '未知')}) - {movie.get('type', '未知类型')}")
        
        # 测试获取详情
        movie = movies[0]
        video_id = movie.get("id")
        if video_id:
            print(f"\n📋 测试获取详情 (ID: {video_id})...")
            detail = api.get_detail(video_id)
            if detail:
                print(f"   - 名称: {detail.get('name')}")
                print(f"   - 导演: {detail.get('director', '未知')[:30]}...")
                print(f"   - 演员: {detail.get('actor', '未知')[:50]}...")
                sources = detail.get("sources", [])
                print(f"   - 播放线路: {len(sources)} 条")
                if sources:
                    print(f"   - 线路名称: {', '.join([s.get('source_name') for s in sources[:3]])}")
                    episodes = sources[0].get("episodes", [])
                    print(f"   - 集数: {len(episodes)} 集")
                    if episodes:
                        print(f"   - 第一集: {episodes[0].get('name')}")
                        url = episodes[0].get('url', '')
                        print(f"   - URL: {url[:60]}...")
    
    # 测试搜索
    print("\n🔍 测试搜索功能...")
    result = api.search("流浪地球")
    movies = result.get("list", [])
    print(f"   搜索到 {len(movies)} 个结果")
    if movies:
        print(f"   第一个: {movies[0].get('name')}")
    
    print("\n✅ API测试完成!")
    return len(movies) > 0

def test_config():
    """测试配置管理"""
    print("\n" + "=" * 50)
    print("⚙️ 测试配置管理")
    print("=" * 50)
    
    from utils.config import Config
    config = Config()
    
    print(f"\n   当前主题: {config.theme}")
    print(f"   API源: {config.api_source}")
    
    # 测试收藏
    test_item = {
        "id": "test123",
        "name": "测试电影",
        "type": "电影",
        "pic": "",
    }
    config.add_favorite(test_item)
    favorites = config.get_favorites()
    print(f"   收藏数量: {len(favorites)}")
    
    # 测试历史
    config.add_history(test_item)
    history = config.get_history()
    print(f"   历史数量: {len(history)}")
    
    print("\n✅ 配置测试完成!")
    return True

def test_ui_import():
    """测试UI组件导入（不创建窗口）"""
    print("\n" + "=" * 50)
    print("🧩 测试UI组件导入")
    print("=" * 50)
    
    try:
        # 只测试不需要QApplication的模块
        from core.api import MovieAPI
        print("   ✅ core.api")
        
        from utils.config import Config
        print("   ✅ utils.config")
        
        # 检查主题样式是否存在
        theme_file = os.path.join(os.path.dirname(__file__), "utils", "theme.py")
        with open(theme_file, 'r', encoding='utf-8') as f:
            content = f.read()
            has_dark = "DARK_STYLE" in content
            has_light = "LIGHT_STYLE" in content
        print(f"   ✅ 主题系统 (暗色:{has_dark}, 亮色:{has_light})")
        
        print("\n✅ UI组件测试完成!")
        return True
    except Exception as e:
        print(f"   ❌ 错误: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "🎬" * 20)
    print("   影视播放器 - 功能测试")
    print("🎬" * 20 + "\n")
    
    results = []
    results.append(("API聚合", test_api()))
    results.append(("配置管理", test_config()))
    results.append(("UI组件", test_ui_import()))
    
    print("\n" + "=" * 50)
    print("📊 测试结果汇总")
    print("=" * 50)
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"   {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print("\n" + ("🎉 全部测试通过!" if all_passed else "⚠️ 部分测试失败"))

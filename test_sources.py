# -*- coding: utf-8 -*-
"""
测试可用的影视API源
"""
import requests
import json

# 收集到的可用API源
SOURCES = [
    {
        "name": "飞速资源",
        "base_url": "http://feisuzy.com/api.php/provide/vod/",
        "list_url": "http://feisuzy.com/api.php/provide/vod/?ac=list",
        "detail_url": "http://feisuzy.com/api.php/provide/vod/?ac=detail",
    },
    {
        "name": "天空资源", 
        "base_url": "http://www.tiankongzy.com/api.php/provide/vod/",
        "list_url": "http://www.tiankongzy.com/api.php/provide/vod/?ac=list",
        "detail_url": "http://www.tiankongzy.com/api.php/provide/vod/?ac=detail",
    },
    {
        "name": "番茄资源",
        "base_url": "http://api.fqzy.cc/api.php/provide/vod/",
        "list_url": "http://api.fqzy.cc/api.php/provide/vod/?ac=list",
        "detail_url": "http://api.fqzy.cc/api.php/provide/vod/?ac=detail",
    },
    {
        "name": "百度云资源",
        "base_url": "https://api.apibdzy.com/api.php/provide/vod/",
        "list_url": "https://api.apibdzy.com/api.php/provide/vod/?ac=list",
        "detail_url": "https://api.apibdzy.com/api.php/provide/vod/?ac=detail",
    },
    {
        "name": "88资源网",
        "base_url": "http://www.88zyw.net/api.php/provide/vod/",
        "list_url": "http://www.88zyw.net/api.php/provide/vod/?ac=list",
        "detail_url": "http://www.88zyw.net/api.php/provide/vod/?ac=detail",
    },
    {
        "name": "黑木耳影视",
        "base_url": "https://heimuer.tv/api.php/provide/vod/",
        "list_url": "https://heimuer.tv/api.php/provide/vod/?ac=list",
        "detail_url": "https://heimuer.tv/api.php/provide/vod/?ac=detail",
    },
]

def test_source(source):
    """测试单个API源"""
    print(f"\n{'='*60}")
    print(f"🧪 测试: {source['name']}")
    print(f"{'='*60}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
    }
    
    try:
        # 测试列表接口
        resp = requests.get(source['list_url'], headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get('list'):
            count = len(data['list'])
            print(f"   ✅ 列表接口正常 - 获取到 {count} 条数据")
            
            # 显示第一条数据
            first = data['list'][0]
            print(f"   📺 示例: {first.get('vod_name', 'N/A')} ({first.get('type_name', 'N/A')})")
            
            # 测试详情接口
            vod_id = first.get('vod_id')
            if vod_id:
                detail_url = f"{source['detail_url']}&ids={vod_id}"
                resp2 = requests.get(detail_url, headers=headers, timeout=10)
                detail_data = resp2.json()
                
                if detail_data.get('list'):
                    detail = detail_data['list'][0]
                    play_url = detail.get('vod_play_url', '')
                    if play_url:
                        print(f"   ✅ 详情接口正常 - 有播放地址")
                        # 解析播放地址
                        episodes = play_url.split('#')
                        print(f"   📁 集数: {len(episodes)} 集")
                        if episodes:
                            first_ep = episodes[0].split('$')
                            if len(first_ep) >= 2:
                                print(f"   🎬 第一集: {first_ep[0]} - {first_ep[1][:50]}...")
                        return True
                    else:
                        print(f"   ⚠️ 详情接口正常 - 但无播放地址")
                else:
                    print(f"   ⚠️ 详情接口返回空数据")
            return True
        else:
            print(f"   ❌ 列表接口返回空数据")
            return False
            
    except Exception as e:
        print(f"   ❌ 请求失败: {str(e)}")
        return False

def main():
    print("\n" + "🎬"*30)
    print("   影视API源可用性测试")
    print("🎬"*30)
    
    results = []
    for source in SOURCES:
        working = test_source(source)
        results.append((source['name'], working))
    
    print("\n" + "="*60)
    print("📊 测试结果汇总")
    print("="*60)
    
    working_sources = []
    for name, working in results:
        status = "✅ 可用" if working else "❌ 不可用"
        print(f"   {name}: {status}")
        if working:
            working_sources.append(name)
    
    print(f"\n🎯 可用源: {len(working_sources)}/{len(SOURCES)}")
    
    return working_sources

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
影视API聚合层 - 支持动态导入源
"""
import requests
import json
import os
from urllib.parse import urljoin, quote
from utils.source_manager import SourceManager


class MovieAPI:
    """影视API聚合器 - 支持导入自定义源"""

    def __init__(self):
        self.source_manager = SourceManager()
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
        })
        self.timeout = 15
        self.current_source_index = 0

    def _get_sources(self):
        """获取启用的源列表"""
        return self.source_manager.get_sources()

    def _get_current_source(self):
        """获取当前源"""
        sources = self._get_sources()
        if not sources:
            return None
        return sources[self.current_source_index % len(sources)]

    def _switch_source(self):
        """切换到下一个源"""
        sources = self._get_sources()
        if len(sources) > 1:
            self.current_source_index = (self.current_source_index + 1) % len(sources)

    def _request(self, url, retry=3):
        """发送请求"""
        errors = []
        sources = self._get_sources()
        
        for attempt in range(min(retry, len(sources))):
            try:
                source = sources[(self.current_source_index + attempt) % len(sources)]
                print(f"   [API] 尝试 {source['name']}: {url[:50]}...")
                
                resp = self.session.get(url, timeout=self.timeout)
                resp.raise_for_status()
                data = resp.json()
                
                if data and (data.get("list") or data.get("total") is not None):
                    self.current_source_index = (self.current_source_index + attempt) % len(sources)
                    return data
                else:
                    errors.append(f"{source['name']}: 返回空数据")
            except Exception as e:
                errors.append(f"{sources[(self.current_source_index + attempt) % len(sources)]['name']}: {str(e)[:30]}")
        
        print(f"   [API] 所有源尝试失败")
        return None

    def _build_url(self, action, **params):
        """构建API URL"""
        source = self._get_current_source()
        if not source:
            return None
        
        base_url = source['url']
        if not base_url.endswith('/'):
            base_url += '/'
        
        url = f"{base_url}?ac={action}"
        for key, value in params.items():
            url += f"&{key}={quote(str(value))}"
        
        return url

    def search(self, keyword, page=1):
        """搜索影视"""
        url = self._build_url("detail", wd=keyword, pg=page)
        if not url:
            return {"list": [], "total": 0, "pagecount": 0}
        
        data = self._request(url)
        if data:
            return self._parse_list(data)
        return {"list": [], "total": 0, "pagecount": 0}

    def get_category_list(self, category="movie", page=1):
        """获取分类列表"""
        url = self._build_url("list", pg=page)
        if not url:
            return {"list": [], "total": 0, "pagecount": 0}
        
        data = self._request(url)
        if data:
            return self._parse_list(data)
        return {"list": [], "total": 0, "pagecount": 0}

    def get_detail(self, video_id):
        """获取影视详情"""
        url = self._build_url("detail", ids=video_id)
        if not url:
            return None
        
        data = self._request(url)
        if data and data.get("list"):
            return self._parse_detail(data["list"][0])
        return None

    def get_home_recommend(self):
        """获取首页推荐"""
        result = {}
        data = self.get_category_list("movie", page=1)
        movies = data.get("list", [])
        
        result["最新电影"] = movies[:12]
        result["最新电视剧"] = movies[:12]
        result["最新动漫"] = movies[:12]
        result["最新综艺"] = movies[:12]
        
        return result

    def _parse_list(self, data):
        """解析列表数据"""
        movie_list = []
        items = data.get("list", [])
        for item in items:
            movie_list.append(self._parse_video_item(item))
        return {
            "list": movie_list,
            "total": data.get("total", len(items)),
            "pagecount": data.get("pagecount", 1),
        }

    def _parse_video_item(self, item):
        """解析单个视频条目"""
        return {
            "id": item.get("vod_id", ""),
            "name": item.get("vod_name", "未知"),
            "pic": item.get("vod_pic", ""),
            "type": item.get("type_name", ""),
            "year": item.get("vod_year", ""),
            "area": item.get("vod_area", ""),
            "remarks": item.get("vod_remarks", "") or item.get("vod_note", ""),
            "actor": item.get("vod_actor", ""),
            "director": item.get("vod_director", ""),
            "content": item.get("vod_content", ""),
            "lang": item.get("vod_lang", ""),
            "score": item.get("vod_score", ""),
        }

    def _parse_detail(self, item):
        """解析详情数据"""
        data = self._parse_video_item(item)

        play_urls = item.get("vod_play_url", "")
        play_from = item.get("vod_play_from", "")

        sources = []
        if play_urls and play_from:
            from_list = play_from.split("$$$")
            url_list = play_urls.split("$$$")

            for i, from_name in enumerate(from_list):
                if i < len(url_list):
                    episodes = []
                    parts = url_list[i].split("#")
                    for part in parts:
                        if part.strip():
                            ep_parts = part.split("$")
                            if len(ep_parts) >= 2:
                                episodes.append({
                                    "name": ep_parts[0].strip(),
                                    "url": ep_parts[1].strip(),
                                })
                    if episodes:
                        sources.append({
                            "source_name": from_name.strip() or f"线路{i+1}",
                            "episodes": episodes,
                        })

        data["sources"] = sources
        return data

    def add_source(self, name, url):
        """添加源"""
        return self.source_manager.add_source(name, url)

    def import_sources_from_url(self, url):
        """从URL导入源"""
        return self.source_manager.import_from_url(url)

    def get_sources(self):
        """获取所有源"""
        return self.source_manager.get_sources()

# -*- coding: utf-8 -*-
"""
源管理模块 - 支持导入自定义影视源
"""
import json
import os
import requests
from urllib.parse import urljoin

class SourceManager:
    """影视源管理器"""
    
    # 默认源
    DEFAULT_SOURCES = [
        {
            "name": "百度云资源",
            "url": "https://api.apibdzy.com/api.php/provide/vod/",
            "type": "maccms",
            "enabled": True
        },
        {
            "name": "非凡资源",
            "url": "http://cj.ffzyapi.com/api.php/provide/vod/",
            "type": "maccms",
            "enabled": True
        },
        {
            "name": "量子资源",
            "url": "http://cj.lziapi.com/api.php/provide/vod/",
            "type": "maccms",
            "enabled": True
        }
    ]
    
    # TVBox格式示例
    TVBOX_EXAMPLE = {
        "sites": [
            {
                "key": "百度云",
                "name": "百度云资源",
                "type": 1,
                "api": "https://api.apibdzy.com/api.php/provide/vod/",
                "searchable": 1,
                "quickSearch": 1,
                "filterable": 0
            }
        ]
    }
    
    def __init__(self):
        self.config_dir = os.path.join(os.path.expanduser("~"), ".movieplayer")
        self.source_file = os.path.join(self.config_dir, "sources.json")
        self.sources = self._load_sources()
    
    def _load_sources(self):
        """加载源配置"""
        if os.path.exists(self.source_file):
            try:
                with open(self.source_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return self.DEFAULT_SOURCES.copy()
    
    def save_sources(self):
        """保存源配置"""
        os.makedirs(self.config_dir, exist_ok=True)
        with open(self.source_file, 'w', encoding='utf-8') as f:
            json.dump(self.sources, f, ensure_ascii=False, indent=2)
    
    def get_sources(self):
        """获取所有源"""
        return [s for s in self.sources if s.get('enabled', True)]
    
    def add_source(self, name, url, source_type="maccms"):
        """添加源"""
        self.sources.append({
            "name": name,
            "url": url,
            "type": source_type,
            "enabled": True
        })
        self.save_sources()
    
    def remove_source(self, name):
        """删除源"""
        self.sources = [s for s in self.sources if s['name'] != name]
        self.save_sources()
    
    def toggle_source(self, name, enabled):
        """启用/禁用源"""
        for s in self.sources:
            if s['name'] == name:
                s['enabled'] = enabled
        self.save_sources()
    
    def import_from_url(self, url):
        """从URL导入源配置（支持TVBox格式）"""
        try:
            resp = requests.get(url, timeout=10)
            data = resp.json()
            
            # TVBox格式
            if 'sites' in data:
                for site in data['sites']:
                    if site.get('api'):
                        self.add_source(
                            name=site.get('name', '未命名'),
                            url=site['api'],
                            source_type="maccms"
                        )
                return True, f"成功导入 {len(data['sites'])} 个源"
            
            # MacCMS格式列表
            if isinstance(data, list):
                for item in data:
                    if item.get('url'):
                        self.add_source(
                            name=item.get('name', '未命名'),
                            url=item['url'],
                            source_type="maccms"
                        )
                return True, f"成功导入 {len(data)} 个源"
            
            return False, "不支持的格式"
        except Exception as e:
            return False, f"导入失败: {str(e)}"
    
    def import_from_file(self, file_path):
        """从本地文件导入"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # TVBox格式
            if 'sites' in data:
                for site in data['sites']:
                    if site.get('api'):
                        self.add_source(
                            name=site.get('name', '未命名'),
                            url=site['api'],
                            source_type="maccms"
                        )
                return True, f"成功导入 {len(data['sites'])} 个源"
            
            return False, "不支持的格式"
        except Exception as e:
            return False, f"导入失败: {str(e)}"
    
    def export_sources(self):
        """导出源配置"""
        return {
            "sites": [
                {
                    "key": s['name'],
                    "name": s['name'],
                    "type": 1,
                    "api": s['url'],
                    "searchable": 1,
                    "quickSearch": 1
                }
                for s in self.sources
            ]
        }
    
    def test_source(self, url):
        """测试源是否可用"""
        try:
            test_url = url
            if not test_url.endswith('/'):
                test_url += '/'
            test_url += '?ac=list&pg=1'
            
            resp = requests.get(test_url, timeout=10)
            data = resp.json()
            
            if data.get('list'):
                return True, f"可用 - {len(data['list'])} 条数据"
            return False, "源返回空数据"
        except Exception as e:
            return False, f"连接失败: {str(e)}"

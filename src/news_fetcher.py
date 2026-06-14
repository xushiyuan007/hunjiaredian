#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
婚姻家事领域热点新闻智能抓取脚本
用于每日自动获取婚姻家事相关法律新闻、司法解释、典型案例
"""

import os
import json
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict
import pytz

class MarriageNewsFetcher:
    def __init__(self):
        self.beijing_tz = pytz.timezone('Asia/Shanghai')
        self.today = datetime.now(self.beijing_tz).strftime('%Y-%m-%d')
        
        # 婚姻家事搜索关键词
        self.keywords = [
            '婚姻法 司法解释',
            '离婚 财产分割 案例',
            '子女抚养权 判决',
            '民法典 婚姻家庭编',
            '家暴 人身保护令',
            '夫妻共同债务 新规',
            '遗产继承 典型案例',
            '离婚冷静期 案例',
            '婚姻家事 指导案例',
            '彩礼返还 新规',
            '涉外婚姻 法律',
            '亲子鉴定 司法'
        ]
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def search_baidu_news(self, keyword: str, limit: int = 5) -> List[Dict]:
        """搜索百度新闻"""
        news_list = []
        try:
            url = f'https://news.baidu.com/ns?word={keyword}&tn=news&from=news&cl=2&rn=20&ct=1'
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('.result-op')[:limit]
            
            for item in items:
                try:
                    title_elem = item.select_one('h3 a')
                    source_elem = item.select_one('.c-color-gray')
                    time_elem = item.select_one('.c-color-gray2')
                    
                    if title_elem:
                        news = {
                            'title': title_elem.get_text(strip=True),
                            'url': title_elem.get('href', ''),
                            'source': source_elem.get_text(strip=True) if source_elem else '未知来源',
                            'time': time_elem.get_text(strip=True) if time_elem else '',
                            'keyword': keyword,
                            'category': self._categorize_news(keyword)
                        }
                        news_list.append(news)
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"百度新闻搜索失败 [{keyword}]: {str(e)}")
        
        time.sleep(1)
        return news_list

    def _categorize_news(self, keyword: str) -> str:
        """新闻分类"""
        categories = {
            '司法解释': '法规解读',
            '民法典': '法规解读',
            '新规': '法规解读',
            '财产分割': '财产纠纷',
            '抚养权': '子女抚养',
            '继承': '遗产继承',
            '家暴': '人身保护',
            '债务': '债务纠纷',
            '彩礼': '彩礼纠纷',
            '冷静期': '离婚程序',
            '涉外': '涉外婚姻',
            '亲子鉴定': '亲子关系'
        }
        
        for key, category in categories.items():
            if key in keyword:
                return category
        return '综合资讯'

    def fetch_all_news(self) -> List[Dict]:
        """获取所有新闻"""
        all_news = []
        seen_titles = set()
        
        print(f"开始搜索婚姻家事热点新闻 - {self.today}")
        print("=" * 60)
        
        for keyword in self.keywords:
            print(f"正在搜索: {keyword}")
            news = self.search_baidu_news(keyword)
            
            for item in news:
                # 去重
                if item['title'] not in seen_titles:
                    seen_titles.add(item['title'])
                    all_news.append(item)
        
        # 按分类整理
        categorized = {}
        for news in all_news:
            cat = news['category']
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(news)
        
        print(f"\n搜索完成，共获取 {len(all_news)} 条新闻")
        for cat, items in categorized.items():
            print(f"  - {cat}: {len(items)} 条")
        
        return all_news

    def generate_markdown(self, news_list: List[Dict]) -> str:
        """生成Markdown格式报告"""
        # 按分类分组
        categorized = {}
        for news in news_list:
            cat = news['category']
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(news)
        
        md_content = f"""# 📢 婚姻家事每日热点新闻推送
**日期**: {self.today}
**更新时间**: {datetime.now(self.beijing_tz).strftime('%H:%M:%S')}
**新闻总数**: {len(news_list)} 条

---

"""
        # 分类输出
        category_order = ['法规解读', '财产纠纷', '子女抚养', '遗产继承', '人身保护', '债务纠纷', '彩礼纠纷', '离婚程序', '涉外婚姻', '亲子关系', '综合资讯']
        
        for cat in category_order:
            if cat in categorized and categorized[cat]:
                md_content += f"## 📌 {cat}\n\n"
                for i, news in enumerate(categorized[cat], 1):
                    md_content += f"{i}. **{news['title']}**\n"
                    md_content += f"   - 来源: {news['source']} | {news['time']}\n"
                    md_content += f"   - 链接: [{news['url'][:50]}...]({news['url']})\n\n"
                md_content += "---\n\n"
        
        md_content += """
## 💡 自媒体选题建议

1. **热点解读型**: 选取最新司法解释或典型案例进行深度解读
2. **普法科普型**: 结合新闻热点普及相关法律知识
3. **案例分析型**: 选取典型案例进行拆解分析
4. **风险提示型**: 针对热点事件提示相关法律风险

---
*本推送由婚姻家事新闻智能体自动生成*
"""
        return md_content

    def push_to_dingtalk(self, news_list: List[Dict], webhook_url: str) -> bool:
        """推送到钉钉群"""
        if not webhook_url:
            print("未配置钉钉Webhook，跳过推送")
            return False
        
        try:
            # 生成摘要
            summary = f"【婚姻家事每日热点】{self.today}\n\n"
            summary += f"📊 今日共获取 {len(news_list)} 条热点新闻\n\n"
            
            # 取前10条重要新闻
            for i, news in enumerate(news_list[:10], 1):
                summary += f"{i}. {news['title'][:30]}...\n"
            
            summary += f"\n🔗 详细内容已生成，共涵盖 {len(set(n['category'] for n in news_list))} 个分类"
            
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "title": f"婚姻家事热点新闻 {self.today}",
                    "text": summary
                }
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            result = response.json()
            
            if result.get('errcode') == 0:
                print("钉钉推送成功")
                return True
            else:
                print(f"钉钉推送失败: {result}")
                return False
                
        except Exception as e:
            print(f"钉钉推送异常: {str(e)}")
            return False

    def push_to_lark(self, news_list: List[Dict], webhook_url: str) -> bool:
        """推送到飞书群"""
        if not webhook_url:
            print("未配置飞书Webhook，跳过推送")
            return False
        
        try:
            summary = f"**婚姻家事每日热点新闻 - {self.today}**\n\n"
            summary += f"📊 今日共获取 **{len(news_list)}** 条热点新闻\n\n"
            
            for i, news in enumerate(news_list[:8], 1):
                summary += f"{i}. {news['title']}\n"
            
            data = {
                "msg_type": "text",
                "content": {
                    "text": summary
                }
            }
            
            response = requests.post(webhook_url, json=data, timeout=10)
            print("飞书推送完成")
            return True
            
        except Exception as e:
            print(f"飞书推送异常: {str(e)}")
            return False

    def save_report(self, news_list: List[Dict], output_dir: str = 'output'):
        """保存报告到文件"""
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存Markdown
        md_content = self.generate_markdown(news_list)
        md_file = os.path.join(output_dir, f'marriage_news_{self.today}.md')
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        # 保存JSON
        json_file = os.path.join(output_dir, f'marriage_news_{self.today}.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        
        print(f"报告已保存: {md_file}")
        return md_file


def main():
    """主函数"""
    fetcher = MarriageNewsFetcher()
    
    # 获取新闻
    news_list = fetcher.fetch_all_news()
    
    if not news_list:
        print("未获取到新闻")
        return
    
    # 保存报告
    fetcher.save_report(news_list)
    
    # 推送（从环境变量获取webhook）
    dingtalk_webhook = os.environ.get('DINGTALK_WEBHOOK', '')
    lark_webhook = os.environ.get('LARK_WEBHOOK', '')
    
    if dingtalk_webhook:
        fetcher.push_to_dingtalk(news_list, dingtalk_webhook)
    
    if lark_webhook:
        fetcher.push_to_lark(news_list, lark_webhook)
    
    print("\n✅ 任务执行完成!")


if __name__ == '__main__':
    main()

import requests
from datetime import datetime, timedelta
import json
import os

class NewsFetcher:
    def __init__(self):
        self.keywords = [
            "婚姻法 司法解释",
            "离婚 财产分割 案例",
            "抚养权 判决 案例",
            "彩礼 返还 新规",
            "家暴 人身保护令",
            "遗产继承 纠纷",
            "夫妻共同债务",
            "涉外婚姻 法律",
        ]
    
    def fetch_recent_news(self, days=3):
        news_list = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        mock_news = [
            {
                "title": "2026年婚姻登记新规解读：4种情形仍禁止结婚",
                "category": "法规解读",
                "date": "2026-06-12",
                "summary": "2026年婚姻登记手续简化，取消户口簿强制要求，但重婚、近亲结婚、未达法定婚龄、患有医学上不应当结婚疾病且未治愈这4种情形仍禁止结婚。"
            },
            {
                "title": "婚前隐瞒精神分裂症，法院判决撤销婚姻",
                "category": "典型案例",
                "date": "2026-06-11",
                "summary": "江苏常州一男子结婚半年后发现妻子婚前患有精神分裂症，法院依据《民法典》判决撤销婚姻关系。"
            },
            {
                "title": "婚内出轨赠与第三者47.8万元，法院判决全额返还",
                "category": "财产纠纷",
                "date": "2026-06-13",
                "summary": "最高法明确婚内一方为维系婚外关系向第三者赠与财产一律无效，原配主张返还应予支持。"
            },
            {
                "title": "夫妻分居期间子女抚养问题：法院判决暂由母亲直接抚养",
                "category": "子女抚养",
                "date": "2026-06-12",
                "summary": "保定中院终审判决，夫妻分居期间双方仍对子女享有平等监护权，应从有利于子女身心健康出发确定抚养事宜。"
            },
            {
                "title": "定安法院成功调解一起同居关系子女抚养纠纷",
                "category": "子女抚养",
                "date": "2026-06-12",
                "summary": "定安法院通过法官加特邀调解员，线上协同调解模式，成功化解一起未达法定婚龄同居后的子女抚养纠纷。"
            },
        ]
        
        for news in mock_news:
            news_date = datetime.strptime(news["date"], "%Y-%m-%d")
            if start_date <= news_date <= end_date:
                news_list.append(news)
        
        return news_list


class DingTalkPusher:
    def __init__(self, webhook, secret=None):
        self.webhook = webhook
        self.secret = secret
    
    def push_news(self, news_list):
        if not news_list:
            return False
        
        categories = {}
        for news in news_list:
            cat = news["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(news)
        
        today = datetime.now().strftime("%Y年%m月%d日")
        markdown = "# 📰 婚姻家事每日热点新闻\n📅 " + today + "\n\n"
        
        for category, items in categories.items():
            markdown += "## 【" + category + "】\n"
            for i, news in enumerate(items, 1):
                markdown += "**" + str(i) + ". " + news["title"] + "**\n"
                markdown += "> " + news["summary"] + "\n\n"
        
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": "婚姻家事热点新闻",
                "text": markdown
            }
        }
        
        try:
            response = requests.post(self.webhook, json=data)
            return response.status_code == 200
        except Exception as e:
            print("推送失败:", e)
            return False

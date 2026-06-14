import requests
from datetime import datetime, timedelta

class NewsFetcher:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"
    
    def fetch_news(self, keywords, days=3):
        """抓取新闻（没有API时返回演示数据）"""
        if not self.api_key:
            return self.get_demo_data()
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            query = " OR ".join(keywords)
            params = {
                "q": query,
                "from": start_date.strftime("%Y-%m-%d"),
                "to": end_date.strftime("%Y-%m-%d"),
                "language": "zh",
                "apiKey": self.api_key,
                "pageSize": 20
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            data = response.json()
            
            if data.get("status") == "ok":
                return self.format_news(data["articles"])
            
        except Exception as e:
            print(f"API抓取失败: {e}")
        
        return self.get_demo_data()
    
    def format_news(self, articles):
        """格式化新闻数据"""
        news_list = []
        for article in articles[:10]:
            news_list.append({
                "title": article["title"],
                "summary": article.get("description", article.get("content", "")),
                "source": article["source"].get("name", "网络"),
                "url": article["url"],
                "date": article["publishedAt"][:10]
            })
        return news_list
    
    def get_demo_data(self):
        """演示数据（API不可用时使用）"""
        return [
            {
                "title": "2026年婚姻登记新规正式实施：4种情形仍禁止结婚",
                "category": "📜 法规解读",
                "date": "2026-06-12",
                "summary": "2026年最新修订的《婚姻登记条例》正式实施，核心变化：①取消提供户口簿强制要求，实现全国通办；②虚假登记将记入信用记录；③隐私保护升级。\n\n**重点**：重婚、近亲结婚、未达法定婚龄、患有医学上不应当结婚疾病且未治愈，这4种情形仍禁止结婚。",
                "source": "民政部官网",
                "url": "https://www.mca.gov.cn/",
                "tip": "可做选题：《2026年结婚不用带户口本了！》"
            },
            {
                "title": "婚前隐瞒精神分裂症，常州法院判决撤销婚姻",
                "category": "⚖️ 典型案例",
                "date": "2026-06-11",
                "summary": "【裁判要点】《民法典》第1053条：一方患有重大疾病的，应当在结婚登记前如实告知另一方；不如实告知的，另一方可以请求撤销婚姻。\n\n【判决】依法撤销婚姻关系，同居期间财产按共有处理。",
                "source": "常州市中级人民法院",
                "url": "https://czfy.chinacourt.gov.cn/",
                "tip": "可做选题：《结婚半年发现妻子有精神病，法院：撤销！》"
            },
            {
                "title": "婚内出轨赠与第三者47.8万元，法院判决全额返还",
                "category": "💰 财产纠纷",
                "date": "2026-06-13",
                "summary": "【裁判要旨】夫妻关系存续期间，一方与他人发展不正当关系，并赠与第三者大额财产的行为，既违反公序良俗，也侵犯了夫妻共同财产权，该赠与行为全部无效。",
                "source": "最高人民法院",
                "url": "https://www.court.gov.cn/",
                "tip": "可做选题：《给小三的47.8万，原配一分不少全要回来了！》"
            },
        ]

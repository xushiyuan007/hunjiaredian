class AIAnalyzer:
    def __init__(self):
        self.category_map = {
            "婚姻法": "📜 法规解读",
            "司法解释": "📜 法规解读",
            "民法典": "📜 法规解读",
            "离婚": "⚖️ 典型案例",
            "财产分割": "💰 财产纠纷",
            "共同债务": "💰 财产纠纷",
            "抚养权": "👶 子女抚养",
            "抚养费": "👶 子女抚养",
            "彩礼": "💒 彩礼纠纷",
            "家暴": "🛡️ 人身保护",
            "继承": "🏛️ 遗产继承",
            "涉外": "🌍 涉外婚姻",
        }
    
    def analyze(self, news):
        """单条新闻智能分析"""
        # 智能分类
        category = "📰 热点新闻"
        for keyword, cat in self.category_map.items():
            if keyword in news["title"] or keyword in news.get("summary", ""):
                category = cat
                break
        
        news["category"] = category
        
        # 生成创作提示
        title = news["title"]
        if "法院" in title or "判决" in title:
            news["tip"] = f"案例解读：《{title[:20]}...》，附裁判要点"
        elif "新规" in title or "条例" in title:
            news["tip"] = f"新规解读：《{title[:20]}...》，附律师提示"
        else:
            news["tip"] = f"热点分析：《{title[:20]}...》"
        
        return news
    
    def analyze_batch(self, news_list):
        """批量分析"""
        return [self.analyze(news) for news in news_list]

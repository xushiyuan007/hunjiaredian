class DingTalkPusher:
    def __init__(self, webhook, secret=None):
        self.webhook = webhook
    
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
                "title": "新闻推送",
                "text": markdown
            }
        }
        
        try:
            response = requests.post(self.webhook, json=data)
            print("钉钉返回:", response.text)
            return response.status_code == 200
        except Exception as e:
            print("推送失败:", e)
            return False

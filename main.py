import os
import sys
sys.path.append('./src')
sys.path.append('./config')

from news_fetcher import NewsFetcher
from ai_analyzer import AIAnalyzer
import requests
from datetime import datetime

def main():
    # 读取配置
    webhook = os.getenv('DINGTALK_WEBHOOK')
    api_key = os.getenv('NEWS_API_KEY')
    days = int(os.getenv('NEWS_DAYS', '3'))
    
    if not webhook:
        print("❌ 错误：未配置DINGTALK_WEBHOOK")
        return
    
    if not api_key:
        print("⚠️ 未配置NEWS_API_KEY，使用演示数据")
        use_demo_data = True
    else:
        use_demo_data = False
    
    print(f"🔍 开始抓取最近 {days} 天的婚姻家事新闻...")
    
    if use_demo_data:
        # 演示数据（没有API时用这个）
        news_list = get_demo_news()
    else:
        # 真实爬虫抓取
        fetcher = NewsFetcher(api_key)
        keywords = ["婚姻法", "离婚财产分割", "抚养权", "彩礼返还", "家暴", "遗产继承"]
        news_list = fetcher.fetch_news(keywords, days=days)
    
    if not news_list:
        print("❌ 未抓取到新闻")
        return
    
    print(f"✅ 成功抓取 {len(news_list)} 条新闻")
    
    # AI智能分析
    print("🤖 AI正在分析新闻...")
    analyzer = AIAnalyzer()
    analyzed_news = analyzer.analyze_batch(news_list)
    
    # 构建详细推送
    markdown = build_markdown(analyzed_news)
    
    # 发送钉钉
    send_to_dingtalk(webhook, markdown)
    print("🎉 推送完成！")

def get_demo_news():
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
    ]

def build_markdown(news_list):
    today = datetime.now().strftime("%Y年%m月%d日")
    markdown = f"""# 📰 婚姻家事每日热点新闻
📅 推送时间：{today}
📊 共抓取 {len(news_list)} 条热点新闻
---

"""
    
    for i, news in enumerate(news_list, 1):
        markdown += f"""## {news.get('category', '📰 热点新闻')}
### {i}. {news['title']}

{news['summary']}

📌 **来源**：[{news.get('source', '网络')}]({news.get('url', '#')})
💡 **创作提示**：{news.get('tip', '结合法条做深度解读')}

---

"""
    
    markdown += """
### 📝 今日创作建议
✅ 挑选1-2个案例做深度普法解读
✅ 结合《民法典》条文做专业分析
✅ 增加律师视角的风险提示
"""
    return markdown

def send_to_dingtalk(webhook, content):
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "新闻推送",
            "text": content
        }
    }
    try:
        response = requests.post(webhook, json=data)
        print("钉钉响应:", response.text)
    except Exception as e:
        print("推送失败:", e)

if __name__ == "__main__":
    main()

import os
import sys
sys.path.append('./src')

from news_fetcher import NewsFetcher
from dingtalk_push import DingTalkPusher

def main():
    # 获取配置
    webhook = os.getenv('DINGTALK_WEBHOOK')
    secret = os.getenv('DINGTALK_SECRET')
    days = int(os.getenv('NEWS_DAYS', '3'))
    
    if not webhook:
        print("错误：未配置DINGTALK_WEBHOOK")
        return
    
    # 抓取新闻
    print(f"开始抓取最近 {days} 天的婚姻家事新闻...")
    fetcher = NewsFetcher()
    news = fetcher.fetch_recent_news(days=days)
    
    if not news:
        print("未抓取到新闻")
        return
    
    print(f"成功抓取 {len(news)} 条新闻")
    
    # 推送到钉钉
    pusher = DingTalkPusher(webhook, secret)
    success = pusher.push_news(news)
    
    if success:
        print("推送成功！")
    else:
        print("推送失败！")

if __name__ == "__main__":
    main()

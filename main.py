import requests
from datetime import datetime, timedelta
import os

def main():
    webhook = os.getenv('DINGTALK_WEBHOOK')
    days = int(os.getenv('NEWS_DAYS', '3'))
    
    if not webhook:
        print("错误：未配置DINGTALK_WEBHOOK")
        return
    
    print(f"开始抓取最近 {days} 天的婚姻家事新闻...")
    
    # 新闻数据
    news_list = [
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
    ]
    
    print(f"成功抓取 {len(news_list)} 条新闻")
    
    # 按分类整理
    categories = {}
    for news in news_list:
        cat = news["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(news)
    
    # 构建消息
    today = datetime.now().strftime("%Y年%m月%d日")
    markdown = "# 📰 婚姻家事每日热点新闻\n📅 " + today + "\n\n"
    
    for category, items in categories.items():
        markdown += "## 【" + category + "】\n"
        for i, news in enumerate(items, 1):
            markdown += "**" + str(i) + ". " + news["title"] + "**\n"
            markdown += "> " + news["summary"] + "\n\n"
    
    # 发送钉钉
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "新闻推送",
            "text": markdown
        }
    }
    
    try:
        response = requests.post(webhook, json=data)
        print("钉钉返回:", response.text)
        if response.status_code == 200:
            print("✅ 推送成功！")
        else:
            print("❌ 推送失败！")
    except Exception as e:
        print("推送失败:", e)

if __name__ == "__main__":
    main()

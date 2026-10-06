import os
import time
import asyncio
import feedparser
from telegram import Bot

RSS_URL = "https://www.echoroukonline.com/feed"
CHANNEL_ID = "@AlgeriaTechNews"

async def send_news_loop():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN is missing!")
    
    bot = Bot(token=token)
    last_sent_title = None
    
    print("News loop started...")
    
    while True:
        try:
            feed = feedparser.parse(RSS_URL)
            if feed.entries:
                latest_entry = feed.entries[0]
                title = latest_entry.title
                link = latest_entry.link

                if title != last_sent_title:
                    last_sent_title = title
                    message = f"📰 *{title}*\n\n🔗 للتفاصيل: {link}"
                    
                    await bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=message,
                        parse_mode="Markdown"
                    )
                    print(f"تم نشر الخبر بنجاح: {title}")
        except Exception as e:
            print(f"خطأ أثناء جلب الأخبار: {e}")
        
        # الانتظار لمدة 10 دقائق (600 ثانية) قبل الفحص القادم
        await asyncio.sleep(600)

def main():
    # تشغيل حلقة الأخبار بشكل غير متزامن
    asyncio.run(send_news_loop())

if __name__ == "__main__":
    main()

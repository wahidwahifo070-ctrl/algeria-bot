import os
import asyncio
import threading
import feedparser
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# 1. سيرفر خفيف لإبقاء منصة Render تعمل بدون توقف
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot and News Auto-poster are Running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# 2. إعدادات الأخبار والقناة
RSS_URL = "https://www.echoroukonline.com/feed" 
CHANNEL_ID = "@AlgeriaTechNews" 
seen_news_links = set()

async def fetch_and_post_news(app):
    global seen_news_links
    while True:
        try:
            feed = feedparser.parse(RSS_URL)
            for entry in feed.entries[:3]:
                if entry.link not in seen_news_links:
                    seen_news_links.add(entry.link)
                    title = entry.title
                    link = entry.link
                    message_text = f"📰 **خبر جديد**\n\n**{title}**\n\n🔗 [قراءة التفاصيل كاملة]({link})\n\n📢 اشترك في القناة ليصلك الجديد: {CHANNEL_ID}"
                    await app.bot.send_message(
                        chat_id=CHANNEL_ID,
                        text=message_text,
                        parse_mode="Markdown"
                    )
        except Exception as e:
            print(f"خطأ أثناء جلب الأخبار: {e}")
            
        await asyncio.sleep(600) # فحص كل 10 دقائق

async def start_news_loop(app):
    asyncio.create_task(fetch_and_post_news(app))

# 3. أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! البوت يعمل بنجاح وينشر الأخبار تلقائياً.")

if __name__ == "__main__":
    threading.Thread(target=run_web_server, daemon=True).start()
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN غير مضبوط!")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    
    loop = asyncio.get_event_loop()
    loop.create_task(start_news_loop(app))
    
    app.run_polling()

import os
import asyncio
import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# رابط الـ RSS وقناة النشر (تأكد من وضع معرف قناتك الصحيح هنا)
RSS_URL = "https://www.echoroukonline.com/feed"
CHANNEL_ID = "@AlgeriaTechNews"

# متغير لتخزين آخر خبر تم نشره لعدم تكراره
last_sent_title = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! بوت الأخبار يعمل بنجاح وجاهز لنشر التحديثات.")

async def check_news(context: ContextTypes.DEFAULT_TYPE):
    global last_sent_title
    try:
        # جلب الأخبار من رابط الـ RSS
        feed = feedparser.parse(RSS_URL)
        if feed.entries:
            latest_entry = feed.entries[0]
            title = latest_entry.title
            link = latest_entry.link

            # إذا كان الخبر جديداً ولم يتم نشره من قبل
            if title != last_sent_title:
                last_sent_title = title
                message = f"📰 *{title}*\n\n🔗 للتفاصيل: {link}"
                
                # إرسال الخبر إلى القناة
                await context.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=message,
                    parse_mode="Markdown"
                )
                print(f"تم نشر الخبر بنجاح: {title}")
    except Exception as e:
        print(f"حدث خطأ أثناء جلب الأخبار: {e}")

async def post_init(application: ApplicationBuilder):
    # جدولة فحص الأخبار تلقائياً كل 10 دقائق (600 ثانية)
    job_queue = application.job_queue
    job_queue.run_repeating(check_news, interval=600, first=10)

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN is missing!")

    # بناء التطبيق مع تفعيل نظام الوظائف (Job Queue)
    app = ApplicationBuilder().token(token).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))

    print("Bot with auto-news feature is starting polling...")
    app.run_polling()

if __name__ == "__main__":
    main()

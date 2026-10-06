import os
import feedparser
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

RSS_URL = "https://www.echoroukonline.com/feed"
CHANNEL_ID = "@AlgeriaTechNews"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! البوت يعمل بنجاح.")

def main():
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN is missing!")

    # بناء تطبيق البوت مباشرة وبكل بساطة
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot is starting polling...")
    app.run_polling()

if __name__ == "__main__":
    main()

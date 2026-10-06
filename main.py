import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# سيرفر خفيف لإبقاء Render يعمل بنجاح
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# أمر البدء عند مراسلة البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك! البوت يعمل بنجاح الآن.")

if __name__ == "__main__":
    # تشغيل السيرفر في الخلفية
    threading.Thread(target=run_web_server, daemon=True).start()
    
    # جلب التوكن من متغيرات البيئة
    token = os.environ.get("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("لم يتم ضبط متغير TELEGRAM_TOKEN في Render!")

    # تشغيل البوت
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


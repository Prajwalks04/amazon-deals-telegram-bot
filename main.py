import os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, ContextTypes, JobQueue
)
from deal_fetcher import fetch_trending_deals
from utils import format_deal_message, is_duplicate, save_deal_to_db
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

app = Application.builder().token(TELEGRAM_TOKEN).build()

# === COMMAND HANDLERS ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm your deal bot. Stay tuned for trending offers!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start to begin. I’ll post deals automatically.")

# === DEAL POSTING JOB ===

async def post_deals(context: ContextTypes.DEFAULT_TYPE):
    deals = fetch_trending_deals()
    for deal in deals:
        if not is_duplicate(deal['url']):
            save_deal_to_db(deal['url'])
            message = format_deal_message(deal)
            await context.bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=deal["image"],
                caption=message,
                parse_mode="Markdown"
            )

# === HEALTH CHECK SERVER ===

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/8080':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running.")
        else:
            self.send_response(404)
            self.end_headers()

def run_health_check_server():
    server = HTTPServer(('', 8080), HealthCheckHandler)
    server.serve_forever()

# === MAIN ===

if __name__ == "__main__":
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    job_queue: JobQueue = app.job_queue
    job_queue.run_repeating(post_deals, interval=3600, first=10)

    # Start health check server in background
    threading.Thread(target=run_health_check_server, daemon=True).start()

    # Start the bot
    app.run_polling()

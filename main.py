import os
from telegram.ext import Application, CommandHandler, ContextTypes, JobQueue
from telegram import Update
from deal_fetcher import fetch_trending_deals
from utils import format_deal_message, is_duplicate, save_deal_to_db
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
PORT = int(os.getenv("PORT", 8080))

app = Application.builder().token(TELEGRAM_TOKEN).build()

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

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is running!")

app.add_handler(CommandHandler("start", start_command))

# Job scheduling
job_queue: JobQueue = app.job_queue
job_queue.run_repeating(post_deals, interval=3600, first=10)

# Health check server
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/8080":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def run_health_server():
    server = HTTPServer(("", PORT), HealthHandler)
    print(f"Health check server running on port {PORT}...")
    server.serve_forever()

# Run health check server in a separate thread
threading.Thread(target=run_health_server, daemon=True).start()

# Start bot using webhook or polling (only use one!)
if __name__ == "__main__":
    app.run_polling()  # Use only this OR webhook

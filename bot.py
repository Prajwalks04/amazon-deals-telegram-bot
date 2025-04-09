import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, JobQueue
from telegram import Update
from deal_fetcher import fetch_trending_deals
from utils import format_deal_message, is_duplicate, save_deal_to_db

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

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

def run_health_server():
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")

    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    print("Health check server running on port 8080...")
    server.serve_forever()

def start_bot():
    # Start the health server in the background
    threading.Thread(target=run_health_server, daemon=True).start()

    # Schedule job
    job_queue = app.job_queue
    job_queue.run_repeating(post_deals, interval=3600, first=10)

    # Start bot polling
    app.run_polling()

if __name__ == "__main__":
    start_bot()

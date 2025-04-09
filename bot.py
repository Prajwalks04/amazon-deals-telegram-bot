import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from utils import get_welcome_buttons

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"*Welcome to PSBOTz - Your 24x7 Deal Finder!*\n\n"
        "This bot finds 🔥 trending Amazon deals and posts them automatically in your channel and DM.\n\n"
        "Maintained by *ChatGPT*, powered by *OpenAI*.\n\n"
        "For more bots like this, join [@ps_botz](https://t.me/ps_botz)"
    )

    buttons = get_welcome_buttons()
    await update.message.reply_photo(
        photo="https://te.legra.ph/file/5f61e59f99f29e1c7f29a.jpg",
        caption=welcome_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons),
    )

# Health check endpoint
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/8080":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def run_health_check_server():
    server = HTTPServer(("0.0.0.0", 8080), HealthCheckHandler)
    server.serve_forever()

# Main bot function
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    logger.info("Bot is running...")
    app.run_polling()

# Start the bot and health check server
if __name__ == "__main__":
    threading.Thread(target=run_health_check_server, daemon=True).start()
    main()

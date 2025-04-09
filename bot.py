import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from utils import is_admin, get_welcome_buttons

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = (
        f"*Welcome to PSBOTz - Your 24x7 Deal Finder!*\n\n"
        "This bot fetches trending deals with crazy discounts and delivers them to your DM and channel in real-time!\n\n"
        "Bot maintained by *ChatGPT* and powered by *OpenAI*.\n"
        "For more bots like this, join [@ps_botz](https://t.me/ps_botz)"
    )

    buttons = get_welcome_buttons()
    await update.message.reply_photo(
        photo="https://te.legra.ph/file/5f61e59f99f29e1c7f29a.jpg",
        caption=welcome_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Health check handler
async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is running!")

# Main entry
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("health", health_check))

    # Run polling and health server
    logger.info("Bot starting...")
    app.run_polling()

# Web server for Koyeb health check
if __name__ == "__main__":
    import threading
    from http.server import BaseHTTPRequestHandler, HTTPServer

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
        server = HTTPServer(("0.0.0.0", 8080), HealthHandler)
        server.serve_forever()

    threading.Thread(target=run_health_server, daemon=True).start()
    main()

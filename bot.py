import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from admin_commands import (
    start_command, setting_command, status_command,
    category_callback, discount_callback, handle_message
)

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def run_bot(token: str):
    app = Application.builder().token(token).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("setting", setting_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("channel", setting_command))
    app.add_handler(CommandHandler("connects", setting_command))
    app.add_handler(CommandHandler("users", setting_command))

    # Register callback handlers
    app.add_handler(CallbackQueryHandler(category_callback, pattern="^category_"))
    app.add_handler(CallbackQueryHandler(discount_callback, pattern="^discount_"))

    # Register a message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    app.run_polling()

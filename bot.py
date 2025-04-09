import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from admin_commands import start_command, setting_command, status_command, category_callback, discount_callback, handle_message, show_buttons

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Initialize the bot app
def run_bot(token: str):
    app = Application.builder().token(token).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("setting", setting_command))
    app.add_handler(CommandHandler("status", status_command))
    app.add_handler(CommandHandler("channel", setting_command))
    app.add_handler(CommandHandler("connects", setting_command))
    app.add_handler(CommandHandler("users", setting_command))

    # Callback query handlers for button interactions
    app.add_handler(CallbackQueryHandler(category_callback, pattern=r"^category_"))
    app.add_handler(CallbackQueryHandler(discount_callback, pattern=r"^discount_"))

    # Handle other messages (fallbacks)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot with polling
    app.run_polling()

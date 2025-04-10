import logging
import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ConversationHandler, ContextTypes,
    filters
)
from dotenv import load_dotenv

from admin_commands import (
    send_category_buttons, handle_category_selection,
    handle_discount_selection, handle_custom_category_input,
    CATEGORY_SELECTION, DISCOUNT_SELECTION, CUSTOM_CATEGORY
)

load_dotenv()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Admin ID
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# --- Basic Bot Commands ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Welcome {user.first_name}!\nUse /help to see available commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Welcome message\n"
        "/help - List commands\n"
        "/id - Show your Telegram ID\n"
        "/channel - Show main channel"
    )

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    await update.message.reply_text(f"Your Telegram ID: `{user_id}`", parse_mode='Markdown')

async def channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Main channel: @ps_botz")

async def setting_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("This command is for admin only.")
        return ConversationHandler.END
    return await send_category_buttons(update, context)

# --- Main Function ---

def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    application = ApplicationBuilder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("id", id_command))
    application.add_handler(CommandHandler("channel", channel_command))

    # Conversation handler for category/discount selection
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("setting", setting_command)],
        states={
            CATEGORY_SELECTION: [CallbackQueryHandler(handle_category_selection)],
            CUSTOM_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_category_input)],
            DISCOUNT_SELECTION: [CallbackQueryHandler(handle_discount_selection)],
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)

    # Start bot
    application.run_polling()

if __name__ == "__main__":
    main()

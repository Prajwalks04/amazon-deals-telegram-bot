import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from deal_fetcher import post_deals
from bot import start_handler, help_handler
from utils import is_admin_user
from admin_commands import (
    settings_handler,
    status_handler,
    channel_handler,
    connects_handler,
    users_handler,
    category_buttons,
    discount_buttons,
    handle_callback_query
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_USER = os.getenv("ADMIN_USER")  # Telegram user ID of admin (as string)

app = Application.builder().token(TELEGRAM_TOKEN).build()


# /welcome command
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Source - GitHub.com", url="https://github.com")],
        [InlineKeyboardButton("Owner - @ps_botz", url="https://t.me/ps_botz")],
        [InlineKeyboardButton("Database - mongodb.com", url="https://mongodb.com")],
        [InlineKeyboardButton("Main Channel - @ps_botz", url="https://t.me/ps_botz")],
        [InlineKeyboardButton("Explore Deals - @trendyofferz", url="https://t.me/trendyofferz")]
    ]

    if str(update.effective_user.id) == ADMIN_USER:
        keyboard.append([InlineKeyboardButton("Admin Panel", callback_data="admin_panel")])

    welcome_text = (
        "**Welcome to PSBOTz Deals Bot!**\n\n"
        "Here you'll get *premium trending deals*, updated 24×7 directly in your inbox and channel.\n\n"
        "_Bot fully maintained by ChatGPT, powered by OpenAI._\n"
        "For more bots like this, join: @ps_botz"
    )

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://via.placeholder.com/700x400.png?text=PSBOTz+Deals",
        caption=welcome_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


# Register all handlers
app.add_handler(CommandHandler("start", start_handler))
app.add_handler(CommandHandler("help", help_handler))
app.add_handler(CommandHandler("welcome", welcome))
app.add_handler(CommandHandler("setting", settings_handler))
app.add_handler(CommandHandler("status", status_handler))
app.add_handler(CommandHandler("channel", channel_handler))
app.add_handler(CommandHandler("connects", connects_handler))
app.add_handler(CommandHandler("users", users_handler))

app.add_handler(CallbackQueryHandler(handle_callback_query))

# Run posting job
job_queue = app.job_queue
job_queue.run_repeating(post_deals, interval=3600, first=5)

if __name__ == "__main__":
    print("Bot starting on Koyeb...")
    app.run_polling()

import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, JobQueue
)
from utils import send_welcome_message, is_admin
from deal_fetcher import fetch_and_post_deals
from server import start_health_check

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

app = Application.builder().token(TELEGRAM_TOKEN).build()
job_queue: JobQueue = app.job_queue

# START Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_welcome_message(update, context)

# Admin command placeholder
async def setting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update, ADMIN_ID):
        await update.message.reply_text("Access denied.")
        return

    keyboard = [
        [InlineKeyboardButton("Clothes", callback_data='category_clothes')],
        [InlineKeyboardButton("Accessories", callback_data='category_accessories')],
        [InlineKeyboardButton("Electronics", callback_data='category_electronics')],
    ]
    await update.message.reply_text("Choose a category:", reply_markup=InlineKeyboardMarkup(keyboard))

# Callback Handler for Categories & Discounts
async def handle_category_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.replace("category_", "")
    keyboard = [
        [InlineKeyboardButton("25% OFF", callback_data=f"discount_25_{category}")],
        [InlineKeyboardButton("50% OFF", callback_data=f"discount_50_{category}")],
    ]
    await query.edit_message_text(
        text=f"Selected Category: *{category.title()}*. Now pick a discount:",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Handler for Discount Selection
async def handle_discount_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, discount, category = query.data.split("_")
    await query.edit_message_text(
        text=f"Fetching *{discount}% OFF* deals in *{category.title()}*...",
        parse_mode="Markdown"
    )

    await fetch_and_post_deals(context, category, int(discount))

# Register Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setting", setting))
app.add_handler(CallbackQueryHandler(handle_category_callback, pattern=r"^category_"))
app.add_handler(CallbackQueryHandler(handle_discount_callback, pattern=r"^discount_"))

# Schedule 24/7 deal posting
job_queue.run_repeating(fetch_and_post_deals, interval=3600, first=10)

if __name__ == "__main__":
    start_health_check()
    print("Bot is running...")
    app.run_polling()

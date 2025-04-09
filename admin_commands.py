# admin_commands.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from utils import is_admin, CATEGORY_OPTIONS, DISCOUNT_OPTIONS, set_admin_filter

admin_filters = {}

async def setting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return await update.message.reply_text("You are not authorized to access this command.")
    
    keyboard = [[InlineKeyboardButton(cat, callback_data=f"category_{cat}")]
                for cat in CATEGORY_OPTIONS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a product category:", reply_markup=reply_markup)

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data.split("_", 1)[1]
    user_id = query.from_user.id
    admin_filters[user_id] = {"category": category}

    keyboard = [[InlineKeyboardButton(discount, callback_data=f"discount_{discount}")]
                for discount in DISCOUNT_OPTIONS]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"Selected category: *{category}*\nNow choose a minimum discount:",
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def handle_discount_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    discount = query.data.split("_", 1)[1]
    user_id = query.from_user.id

    if user_id in admin_filters:
        admin_filters[user_id]["discount"] = discount
        set_admin_filter(user_id, admin_filters[user_id])  # Save to global or DB
        await query.edit_message_text(
            text=f"✅ Filter set:\n*Category:* {admin_filters[user_id]['category']}\n"
                 f"*Minimum Discount:* {discount}",
            parse_mode="Markdown"
        )

def register_admin_handlers(app):
    app.add_handler(CommandHandler("setting", setting))
    app.add_handler(CallbackQueryHandler(handle_category_selection, pattern="^category_"))
    app.add_handler(CallbackQueryHandler(handle_discount_selection, pattern="^discount_"))

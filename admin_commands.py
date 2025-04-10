from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler
)

# States for ConversationHandler
CATEGORY_SELECTION, DISCOUNT_SELECTION, CUSTOM_CATEGORY = range(3)

# Predefined categories
categories = ["Clothes", "Accessories", "Electronics", "Home", "Kitchen", "Kids"]

def send_category_buttons(update: Update, context: CallbackContext) -> int:
    keyboard = [[InlineKeyboardButton(cat, callback_data=cat)] for cat in categories]
    keyboard.append([InlineKeyboardButton("Search", callback_data="search_custom")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text("Select a category or tap 'Search' to type your own:", reply_markup=reply_markup)
    return CATEGORY_SELECTION

def handle_category_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    selected = query.data

    if selected == "search_custom":
        query.edit_message_text("Type the category or keyword you want to search:")
        return CUSTOM_CATEGORY

    context.user_data['category'] = selected
    return ask_discount(query, context)

def handle_custom_category_input(update: Update, context: CallbackContext) -> int:
    category = update.message.text.strip()
    context.user_data['category'] = category
    return ask_discount(update, context)

def ask_discount(updateable, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("25%+", callback_data="25")],
        [InlineKeyboardButton("50%+", callback_data="50")],
        [InlineKeyboardButton("75%+", callback_data="75")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = f"Selected Category: *{context.user_data['category']}*\nNow, select discount filter:"
    
    if hasattr(updateable, 'edit_message_text'):
        updateable.edit_message_text(msg, reply_markup=reply_markup, parse_mode='Markdown')
    else:
        updateable.message.reply_text(msg, reply_markup=reply_markup, parse_mode='Markdown')

    return DISCOUNT_SELECTION

def handle_discount_selection(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    discount = query.data

    category = context.user_data.get('category', 'Unknown')
    # You can now process this category and discount filter for deal fetching
    query.edit_message_text(f"Category: *{category}*\nDiscount Filter: *{discount}%+*", parse_mode='Markdown')

    # TODO: Trigger deal filtering based on selected category & discount
    return ConversationHandler.END

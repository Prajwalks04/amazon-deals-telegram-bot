import re
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def format_price(price):
    return f"₹{price:,.0f}"

def extract_price(text):
    match = re.search(r'₹[\d,]+', text)
    if match:
        return int(match.group(0).replace('₹', '').replace(',', ''))
    return None

def is_trending_deal(title, discount):
    trending_keywords = ['Hot Deal', 'Limited Offer', 'Best Price', 'Great Discount', 'Price Drop', '₹1 Deal']
    return any(keyword.lower() in title.lower() for keyword in trending_keywords) or discount >= 50

def build_caption(title, price, discount, coupon_code=None, card_offer=None, is_limited=False):
    caption = f"<b>{title}</b>\n"
    caption += f"Price: <b>{format_price(price)}</b>\n"
    caption += f"Discount: <b>{discount}%</b>\n"
    if is_limited:
        caption += "⏳ <b>Limited Time Offer!</b>\n"
    if coupon_code:
        caption += f"Coupon Code: <code>{coupon_code}</code>\n"
    if card_offer:
        caption += f"Card Offer: {card_offer}\n"
    caption += "#Deals #Offers"
    return caption

def get_category_buttons():
    keyboard = [
        [InlineKeyboardButton("👗 Clothes", callback_data='category_clothes')],
        [InlineKeyboardButton("👜 Accessories", callback_data='category_accessories')],
        [InlineKeyboardButton("📱 Electronics", callback_data='category_electronics')],
        [InlineKeyboardButton("🏠 Home", callback_data='category_home')],
        [InlineKeyboardButton("⬅️ Back", callback_data='admin_back')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_discount_buttons(category):
    keyboard = [
        [InlineKeyboardButton("25% Off", callback_data=f'{category}_25')],
        [InlineKeyboardButton("50% Off", callback_data=f'{category}_50')],
        [InlineKeyboardButton("70% Off", callback_data=f'{category}_70')],
        [InlineKeyboardButton("Back", callback_data='select_category')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_welcome_buttons():
    keyboard = [
        [
            InlineKeyboardButton("📂 Source - GitHub.com", url="https://github.com"),
            InlineKeyboardButton("👤 Owner - @ps_botz", url="https://t.me/ps_botz"),
        ],
        [
            InlineKeyboardButton("🧠 Powered by OpenAI", url="https://openai.com"),
            InlineKeyboardButton("🗃️ Database - mongodb.com", url="https://mongodb.com"),
        ],
        [
            InlineKeyboardButton("🔥 Explore Deals - @trendyofferz", url="https://t.me/trendyofferz"),
            InlineKeyboardButton("💥 More Bots - @ps_botz", url="https://t.me/ps_botz")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

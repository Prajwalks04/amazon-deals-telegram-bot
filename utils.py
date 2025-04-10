from datetime import datetime
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def format_price(price_str):
    try:
        price = float(price_str.replace("₹", "").replace(",", ""))
        return f"₹{price:,.2f}"
    except:
        return price_str


def is_valid_url(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False


def bold(text):
    return f"*{text}*"


def monospace(text):
    return f"`{text}`"


def generate_deal_caption(deal):
    title = bold(deal['title'])
    price = format_price(deal['price'])
    original_price = format_price(deal.get('original_price', ''))
    coupon = f"\nCoupon: {monospace(deal['coupon'])}" if deal.get('coupon') else ""
    credit_card = f"\nCard Offer: {deal['card_offer']}" if deal.get('card_offer') else ""
    offer_tag = ""

    if "₹1" in price or "1.00" in price:
        offer_tag = "\n‼️ *Buy Now ₹1 Deal!*"
    elif deal.get('limited_offer'):
        offer_tag = "\n⏰ *Limited Time Offer!*"
    elif deal.get('price_drop'):
        offer_tag = "\n⬇️ *Price Dropped!*"

    caption = f"{title}\nPrice: {price}\nOriginal: {original_price}{coupon}{credit_card}{offer_tag}"
    return caption.strip()


def generate_deal_buttons(deal):
    buttons = [
        [InlineKeyboardButton("Buy Now", url=deal['url'])],
    ]

    if deal.get('source'):
        buttons.append([
            InlineKeyboardButton("Source", url=deal['source'])
        ])

    return InlineKeyboardMarkup(buttons)


def get_welcome_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Source - GitHub", url="https://github.com/Prajwalks04"),
            InlineKeyboardButton("Owner - @PSBOTz", url="https://t.me/PSBOTz"),
        ],
        [
            InlineKeyboardButton("Database - MongoDB", url="https://mongodb.com"),
            InlineKeyboardButton("Main Channel - @ps_botz", url="https://t.me/ps_botz"),
        ],
        [
            InlineKeyboardButton("Explore More Deals", url="https://t.me/trendyofferz")
        ]
    ])


def get_admin_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Post Controls", callback_data="admin_post_controls"),
            InlineKeyboardButton("Scheduling", callback_data="admin_scheduling"),
        ],
        [
            InlineKeyboardButton("Accepted Channels", callback_data="admin_channels"),
            InlineKeyboardButton("User Access", callback_data="admin_users"),
        ],
        [
            InlineKeyboardButton("24/7 Toggle", callback_data="admin_247toggle")
        ]
    ])


def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_text(text):
    return text.replace('\n', ' ').replace('\r', '').strip()

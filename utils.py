from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
import hashlib
import pymongo
import os

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "dealbot")
COLLECTION_NAME = "posted_deals"

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# Format deals before posting
def format_deal_message(deal):
    title = f"*{deal['title']}*"
    price = f"Price: ₹{deal['price']}"
    link = f"[Buy Now]({deal['url']})"
    tags = deal.get("tags", "")

    caption = f"{title}\n{price}\n{tags}\n{link}"

    if "₹1" in price or "₹1.00" in price:
        caption += "\n\n🔥 *₹1 Deal! Limited Time Offer!* 🔥"

    return caption

# Check duplicate
def is_duplicate(deal_url):
    deal_hash = hashlib.md5(deal_url.encode()).hexdigest()
    return collection.find_one({"hash": deal_hash}) is not None

# Save to DB
def save_deal_to_db(deal_url):
    deal_hash = hashlib.md5(deal_url.encode()).hexdigest()
    collection.insert_one({"hash": deal_hash})

# Admin Check
def is_admin(update: Update, admin_id: int):
    user_id = update.effective_user.id
    return user_id == admin_id

# Welcome Message
async def send_welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("Source - GitHub.com", url="https://github.com")],
        [InlineKeyboardButton("Owner - @ps_botz", url="https://t.me/ps_botz")],
        [InlineKeyboardButton("Database - mongodb.com", url="https://mongodb.com")],
        [InlineKeyboardButton("Main Channel - @ps_botz", url="https://t.me/ps_botz")],
        [InlineKeyboardButton("Explore Deals - @trendyofferz", url="https://t.me/trendyofferz")],
    ]

    welcome_text = (
        "*Welcome to PSBOTz Deals Bot!*\n\n"
        "This bot is maintained by *ChatGPT* and *powered by OpenAI*.\n\n"
        "Stay updated with the hottest deals 24×7 posted directly here and in your DM!\n\n"
        "For more amazing bots like this, join @ps_botz."
    )

    await update.message.reply_photo(
        photo="https://i.imgur.com/0ZCvF2r.png",  # You can replace with your own logo link
        caption=welcome_text,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

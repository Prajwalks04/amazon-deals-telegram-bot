
import pymongo
import os

mongo_uri = os.getenv("MONGO_URI")
client = pymongo.MongoClient(mongo_uri)
db = client["telegram_bot"]
collection = db["posted_deals"]

def is_duplicate(url):
    return collection.find_one({"url": url}) is not None

def save_deal_to_db(url):
    collection.insert_one({"url": url})

def format_deal_message(deal):
    tags = []
    if deal.get("tag"):
        tags.append(f"*{deal['tag']}*")
    if deal.get("urgent"):
        tags.append("*BUY NOW*")
    if deal.get("limited_offer"):
        tags.append("_Limited Time Offer_")
    return f"{' '.join(tags)}\n*{deal['title']}* - `{deal['price']}`\nCoupon: `{deal['coupon']}`\n{deal['card_offer']}\n[Buy Now]({deal['url']})"

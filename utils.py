from datetime import datetime
import requests


def format_price(price_str):
    """Format price to ₹ symbol and commas."""
    try:
        price = float(price_str.replace("₹", "").replace(",", ""))
        return f"₹{price:,.2f}"
    except:
        return price_str


def is_valid_url(url):
    """Check if a URL is reachable (status 200)."""
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
    """Generates a caption with styling and alerts for a deal."""
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


def get_current_time():
    """Returns current time formatted."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def clean_text(text):
    """Remove extra spaces and unwanted characters."""
    return text.replace('\n', ' ').replace('\r', '').strip()

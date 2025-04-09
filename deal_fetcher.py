import random
import datetime

# Sample categories and dummy products
CATEGORIES = {
    "Clothes": ["T-Shirt", "Jeans", "Jacket"],
    "Accessories": ["Watch", "Wallet", "Belt"],
    "Electronics": ["Headphones", "Smartphone", "Charger"],
    "Home": ["Mixer", "Vacuum Cleaner", "Water Bottle"]
}

# Simulate trending deals (this would be replaced by real API calls)
def fetch_trending_deals():
    deals = []
    for category, items in CATEGORIES.items():
        for item in items:
            discount = random.choice([10, 25, 50, 75])
            price = random.randint(100, 1000)
            deal = {
                "title": f"{item} - {discount}% OFF",
                "price": price,
                "url": f"https://example.com/{item.lower()}",
                "image": "https://via.placeholder.com/300.png?text=Deal+Image",
                "tags": f"{category} | {discount}% OFF",
                "category": category,
                "discount": discount,
                "timestamp": datetime.datetime.utcnow()
            }
            deals.append(deal)
    return deals

# Filter based on category and discount
def filter_deals_by_category_and_discount(deals, category, discount):
    return [
        deal for deal in deals
        if deal["category"] == category and deal["discount"] >= discount
    ]

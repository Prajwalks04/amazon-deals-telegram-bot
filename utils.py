from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8669512360:AAH7jZottDphEey4m0at05KKwD-S-_irTUQ"
ADMIN_ID = 5859471026

bot = telebot.TeleBot(TOKEN)

# -------- منو --------
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🚀 خرید سرویس")
    markup.add("💰 تعرفه‌ها", "📩 پشتیبانی")
    markup.add("📚 آموزش اتصال")
    return markup

# -------- متن‌ها --------
welcome = """
🌐 فروش سرویس پرسرعت V2Ray

✅ مناسب تلگرام، اینستاگرام، واتساپ
✅ بدون قطعی
✅ چند لوکیشن فعال
✅ پشتیبانی سریع

از منوی زیر انتخاب کنید 👇
"""

plans = """
💲 لیست قیمت‌ها 💲

10 گیگ — 50
15 گیگ — 70
30 گیگ — 100
45 گیگ — 150
65 گیگ — 270
100 گیگ — 389
150 گیگ — 459
200 گیگ — 689
"""

card = """
💳 پرداخت کارت به کارت

5859471026418461
ابوالفضل متاجی

بعد از پرداخت، رسید را ارسال کنید.
"""

support = "برای پشتیبانی پیام بدهید:\n@abolmtj"

learn = "آموزش اتصال بعد از خرید برایتان ارسال می‌شود."

# -------- دستورات --------
@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, welcome, reply_markup=main_menu())

@bot.message_handler(func=lambda m: m.text == "💰 تعرفه‌ها")
def price(msg):
    bot.send_message(msg.chat.id, plans)

@bot.message_handler(func=lambda m: m.text == "🚀 خرید سرویس")
def buy(msg):
    bot.send_message(msg.chat.id, card)

@bot.message_handler(func=lambda m: m.text == "📩 پشتیبانی")
def sup(msg):
    bot.send_message(msg.chat.id, support)

@bot.message_handler(func=lambda m: m.text == "📚 آموزش اتصال")
def lr(msg):
    bot.send_message(msg.chat.id, learn)

@bot.message_handler(content_types=['photo'])
def receipt(msg):
    bot.send_message(msg.chat.id, "✅ رسید دریافت شد، پس از بررسی لینک برای شما ارسال می‌شود.")
    bot.forward_message(ADMIN_ID, msg.chat.id, msg.message_id)

bot.infinity_polling()

import telebot

TOKEN = "8669512360:AAH7jZottDphEey4m0at05KKwD-S-_irTUQ"
ADMIN_ID = 5859471026   # آیدی عددی خودت

bot = telebot.TeleBot(TOKEN)

plans = """
💲 لیست قیمت ها 💲

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

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id,
                     "سلام 👋\nبه ربات فروش VPN خوش آمدید\n\n/price تعرفه‌ها\n/buy خرید سرویس")

@bot.message_handler(commands=['price'])
def price(msg):
    bot.send_message(msg.chat.id, plans)

@bot.message_handler(commands=['buy'])
def buy(msg):
    bot.send_message(msg.chat.id, card)

@bot.message_handler(content_types=['photo'])
def receipt(msg):
    bot.send_message(msg.chat.id, "✅ رسید دریافت شد، بعد از بررسی لینک برای شما ارسال می‌شود.")
    bot.forward_message(ADMIN_ID, msg.chat.id, msg.message_id)

bot.infinity_polling()

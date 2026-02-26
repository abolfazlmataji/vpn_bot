import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

8669512360:AAH7jZottDphEey4m0at05KKwD-S-_irTUQ= "توکن_ربات_اینجا"
ADMIN_ID = 5955376400   # آیدی عددی خودت

bot = telebot.TeleBot(TOKEN)

# --------- پلن ها ----------
plans = {
    "10": ("10 گیگ", "50"),
    "30": ("30 گیگ", "100"),
    "50": ("50 گیگ", "200"),
    "100": ("100 گیگ", "350"),
}

# --------- پنل شیشه ای ----------
def glass(user, volume, price):
    return f"""
╔══════════════════╗
      🧊 سرویس انتخابی
╚══════════════════╝

👤 کاربر: {user}
📦 حجم: {volume}
💰 مبلغ: {price} هزار تومان

━━━━━━━━━━━━━━━
⚡ سرعت بالا
🌍 آیپی ثابت
📶 بدون قطعی
━━━━━━━━━━━━━━━

پس از پرداخت، کانفیگ فوراً ارسال می‌شود.
"""

# --------- استارت ----------
@bot.message_handler(commands=['start'])
def start(msg):
    kb = InlineKeyboardMarkup(row_width=2)
    for key in plans:
        kb.add(InlineKeyboardButton(f"{plans[key][0]}", callback_data=key))

    bot.send_message(msg.chat.id,
        "🌐 به فروشگاه VPN خوش آمدی\n\nپلن مورد نظر رو انتخاب کن 👇",
        reply_markup=kb)

# --------- انتخاب پلن ----------
@bot.callback_query_handler(func=lambda call: call.data in plans)
def choose(call):
    volume, price = plans[call.data]

    text = glass(call.from_user.first_name, volume, price)

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("💳 ثبت سفارش", callback_data=f"buy_{call.data}"),
        InlineKeyboardButton("🔙 بازگشت", callback_data="back")
    )

    bot.edit_message_text(text, call.message.chat.id,
                          call.message.message_id,
                          reply_markup=kb)

# --------- ثبت سفارش ----------
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy(call):
    key = call.data.split("_")[1]
    volume, price = plans[key]

    # پیام به مشتری
    bot.send_message(call.message.chat.id,
        "✅ سفارش ثبت شد\nادمین بزودی پیام می‌دهد.")

    # ارسال به ادمین
    admin_text = f"""
🛒 سفارش جدید

👤 نام: {call.from_user.first_name}
🆔 آیدی: @{call.from_user.username}
📦 پلن: {volume}
💰 قیمت: {price} هزار تومان
"""
    bot.send_message(ADMIN_ID, admin_text)

# --------- بازگشت ----------
@bot.callback_query_handler(func=lambda call: call.data=="back")
def back(call):
    start(call.message)

print("Bot is running...")
bot.infinity_polling()

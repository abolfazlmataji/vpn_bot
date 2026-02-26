import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8669512360:AAH7jZottDphEey4m0at05KKwD-S-_irTUQ"
ADMIN_ID = 5955376400

bot = telebot.TeleBot(TOKEN)

# ذخیره کاربران
users = set()

# پلن ها
plans = {
    "10": ("10 گیگ", "50"),
    "30": ("30 گیگ", "100"),
    "50": ("50 گیگ", "200"),
    "100": ("100 گیگ", "350"),
}

# کارت شیشه ای
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
"""

# استارت
@bot.message_handler(commands=['start'])
def start(msg):
    users.add(msg.chat.id)

    kb = InlineKeyboardMarkup(row_width=2)
    for key in plans:
        kb.add(InlineKeyboardButton(plans[key][0], callback_data=key))

    bot.send_message(msg.chat.id,
        "🌐 به فروشگاه VPN خوش آمدی\n\nپلن مورد نظر رو انتخاب کن 👇",
        reply_markup=kb)

# انتخاب پلن
@bot.callback_query_handler(func=lambda call: call.data in plans)
def choose(call):
    volume, price = plans[call.data]

    text = glass(call.from_user.first_name, volume, price)

    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("💳 ثبت سفارش", callback_data=f"buy_{call.data}"),
        InlineKeyboardButton("🔙 بازگشت", callback_data="back")
    )

    bot.edit_message_text(text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb)

# ثبت سفارش
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def buy(call):
    key = call.data.split("_")[1]
    volume, price = plans[key]

    bot.send_message(call.message.chat.id,
        "✅ سفارش ثبت شد\nادمین بزودی پیام می‌دهد.")

    admin_text = f"""
🛒 سفارش جدید

👤 نام: {call.from_user.first_name}
🆔 آیدی: @{call.from_user.username}
📦 پلن: {volume}
💰 قیمت: {price} هزار تومان
"""

    bot.send_message(ADMIN_ID, admin_text)

# بازگشت
@bot.callback_query_handler(func=lambda call: call.data=="back")
def back(call):
    start(call.message)

# پنل ادمین
@bot.message_handler(commands=['panel'])
def admin_panel(msg):
    if msg.from_user.id != ADMIN_ID:
        return
    
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("📊 آمار", callback_data="stats"),
        InlineKeyboardButton("📢 پیام همگانی", callback_data="broadcast"),
        InlineKeyboardButton("📝 تغییر قیمت", callback_data="editprice")
    )

    bot.send_message(msg.chat.id, "⚙️ پنل مدیریت", reply_markup=kb)

# آمار
@bot.callback_query_handler(func=lambda call: call.data=="stats")
def stats(call):
    if call.from_user.id != ADMIN_ID:
        return
    bot.send_message(call.message.chat.id,
        f"👥 تعداد کاربران: {len(users)}")

# پیام همگانی
@bot.callback_query_handler(func=lambda call: call.data=="broadcast")
def bc(call):
    if call.from_user.id != ADMIN_ID:
        return
    
    msg = bot.send_message(call.message.chat.id,
        "✉️ متن پیام همگانی را بفرست")

    bot.register_next_step_handler(msg, send_bc)

def send_bc(message):
    for u in users:
        try:
            bot.send_message(u, message.text)
        except:
            pass
    bot.send_message(message.chat.id, "✅ ارسال شد")

# تغییر قیمت
@bot.callback_query_handler(func=lambda call: call.data=="editprice")
def edit(call):
    if call.from_user.id != ADMIN_ID:
        return
    
    bot.send_message(call.message.chat.id,
        "مثال ارسال:\n50=180")
    
    bot.register_next_step_handler(call.message, change_price)

def change_price(message):
    try:
        key, value = message.text.split("=")
        plans[key] = (plans[key][0], value)
        bot.send_message(message.chat.id, "✅ قیمت تغییر کرد")
    except:
        bot.send_message(message.chat.id, "❌ فرمت اشتباه")

print("Bot is running...")
bot.infinity_polling()

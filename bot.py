import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8669512360:AAH7jZottDphEey4m0at05KKwD-S-_irTUQ"
ADMIN_ID = 5955376400

bot = telebot.TeleBot(TOKEN)

users=set()
orders={}
used_test=set()

# نمونه کانفیگ‌ها (بعداً میتونی عوض کنی)
configs={
    "test":"v2ray://TEST-CONFIG",
    "30":"v2ray://CONFIG-30",
    "50":"v2ray://CONFIG-50",
    "100":"v2ray://CONFIG-100"
}

plans={
    "30":("30 گیگ","100"),
    "50":("50 گیگ","200"),
    "100":("100 گیگ","350"),
}

# ---------- منوی اصلی ----------
def main_menu():
    kb=InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🛒 خرید سرویس",callback_data="buy"),
        InlineKeyboardButton("🎁 تست رایگان",callback_data="test"),
        InlineKeyboardButton("👤 پنل کاربری",callback_data="panel"),
        InlineKeyboardButton("💬 پشتیبانی",url="https://t.me/YOURID")
    )
    return kb

# ---------- استارت ----------
@bot.message_handler(commands=['start'])
def start(msg):
    users.add(msg.chat.id)
    bot.send_message(msg.chat.id,
        "🌐 به فروشگاه VPN خوش آمدی",
        reply_markup=main_menu())

# ---------- خرید ----------
@bot.callback_query_handler(func=lambda c:c.data=="buy")
def buy(call):
    kb=InlineKeyboardMarkup()
    for k in plans:
        kb.add(InlineKeyboardButton(plans[k][0],callback_data=f"plan_{k}"))
    kb.add(InlineKeyboardButton("🔙 بازگشت",callback_data="home"))
    bot.edit_message_text("پلن را انتخاب کن:",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=kb)

# ---------- انتخاب پلن ----------
@bot.callback_query_handler(func=lambda c:c.data.startswith("plan_"))
def plan(call):
    key=call.data.split("_")[1]
    orders[call.from_user.id]=key
    volume,price=plans[key]

    text=f"""
📦 پلن: {volume}
💰 مبلغ: {price} هزار تومان

لطفاً رسید پرداخت را ارسال کن
"""
    bot.send_message(call.message.chat.id,text)

# ---------- دریافت رسید ----------
@bot.message_handler(content_types=['photo'])
def receipt(msg):
    if msg.from_user.id not in orders:
        return

    key=orders[msg.from_user.id]
    volume,_=plans[key]

    kb=InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✅ تایید",callback_data=f"ok_{msg.from_user.id}"),
        InlineKeyboardButton("❌ رد",callback_data=f"no_{msg.from_user.id}")
    )

    bot.send_photo(ADMIN_ID,msg.photo[-1].file_id,
        caption=f"رسید جدید\nکاربر:{msg.from_user.first_name}\nپلن:{volume}",
        reply_markup=kb)

    bot.send_message(msg.chat.id,"رسید ارسال شد، منتظر تایید بمان")

# ---------- تایید ادمین ----------
@bot.callback_query_handler(func=lambda c:c.data.startswith("ok_"))
def ok(call):
    uid=int(call.data.split("_")[1])
    key=orders.get(uid)

    if not key:
        return

    bot.send_message(uid,"✅ پرداخت تایید شد\nکانفیگ شما:")
    bot.send_message(uid,configs[key])
    bot.answer_callback_query(call.id,"ارسال شد")

# ---------- رد ادمین ----------
@bot.callback_query_handler(func=lambda c:c.data.startswith("no_"))
def no(call):
    uid=int(call.data.split("_")[1])
    bot.send_message(uid,"❌ پرداخت رد شد")
    bot.answer_callback_query(call.id,"رد شد")

# ---------- تست رایگان ----------
@bot.callback_query_handler(func=lambda c:c.data=="test")
def test(call):
    if call.from_user.id in used_test:
        bot.send_message(call.message.chat.id,"قبلاً تست گرفتی")
        return

    used_test.add(call.from_user.id)
    bot.send_message(call.message.chat.id,"🎁 کانفیگ تست:")
    bot.send_message(call.message.chat.id,configs["test"])

# ---------- پنل کاربر ----------
@bot.callback_query_handler(func=lambda c:c.data=="panel")
def panel(call):
    bot.send_message(call.message.chat.id,
        "👤 پنل کاربری\nبرای خرید جدید /start بزن")

# ---------- پنل ادمین ----------
@bot.message_handler(commands=['admin'])
def admin(msg):
    if msg.from_user.id!=ADMIN_ID:return
    kb=InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("📊 آمار کاربران",callback_data="stats"),
        InlineKeyboardButton("📢 پیام همگانی",callback_data="bc")
    )
    bot.send_message(msg.chat.id,"پنل مدیریت",reply_markup=kb)

@bot.callback_query_handler(func=lambda c:c.data=="stats")
def stats(call):
    if call.from_user.id!=ADMIN_ID:return
    bot.send_message(call.message.chat.id,
        f"👥 کاربران: {len(users)}")

@bot.callback_query_handler(func=lambda c:c.data=="bc")
def bc(call):
    if call.from_user.id!=ADMIN_ID:return
    msg=bot.send_message(call.message.chat.id,"متن پیام را بفرست")
    bot.register_next_step_handler(msg,sendbc)

def sendbc(message):
    for u in users:
        try:
            bot.send_message(u,message.text)
        except:
            pass
    bot.send_message(message.chat.id,"ارسال شد")

# ---------- بازگشت ----------
@bot.callback_query_handler(func=lambda c:c.data=="home")
def home(call):
    bot.edit_message_text("منوی اصلی",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=main_menu())

print("BOT RUNNING")
bot.infinity_polling()

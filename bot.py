import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8669512360:AAH7jZottDphEey4m0at05KKwD-S-_irTUQ"
ADMIN_ID = 5955376400

logging.basicConfig(level=logging.INFO)

CARD = """
💳 پرداخت به کارت:

5859-4710-2641-8461
ابوالفضل متاجی

بعد پرداخت رسید بفرست 👇
"""

# ---------- تعرفه های واقعی تو ----------
PLANS = {
    "10": {"name":"10 گیگ","price":"50 تومان","desc":"مصرف سبک، مناسب تلگرام و چت"},
    "15": {"name":"15 گیگ","price":"70 تومان","desc":"استفاده معمولی روزانه"},
    "30": {"name":"30 گیگ","price":"100 تومان","desc":"اینستاگرام و استفاده متوسط"},
    "45": {"name":"45 گیگ","price":"150 تومان","desc":"استفاده سنگین و تماس"},
    "65": {"name":"65 گیگ","price":"270 تومان","desc":"مناسب دانلود و مصرف بالا"},
    "100": {"name":"100 گیگ","price":"420 تومان","desc":"استفاده حرفه ای و طولانی"},
    "150": {"name":"150 گیگ","price":"459 تومان","desc":"مصرف بسیار بالا"},
    "200": {"name":"200 گیگ","price":"689 تومان","desc":"بیشترین حجم برای مصرف سنگین"}
}

# ---------- منو ----------
def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 خرید سرویس", callback_data="buy")],
        [InlineKeyboardButton("📞 پشتیبانی", callback_data="support")]
    ])

# ---------- لیست شیشه ای ----------
def glass_list():
    btns=[]
    for k,v in PLANS.items():
        btns.append([InlineKeyboardButton(
            f"🧊 {v['name']} | {v['price']}",
            callback_data=f"plan_{k}"
        )])
    btns.append([InlineKeyboardButton("🔙 بازگشت",callback_data="back")])
    return InlineKeyboardMarkup(btns)

# ---------- صفحه هر پلن ----------
def plan_page(code):
    p=PLANS[code]
    text=f"""
🧊 پلن {p['name']}

💰 قیمت: {p['price']}

📊 توضیحات:
{p['desc']}

برای خرید دکمه زیر 👇
"""
    kb=InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 خرید این پلن",callback_data=f"buy_{code}")],
        [InlineKeyboardButton("🔙 بازگشت",callback_data="buy")]
    ])
    return text,kb

# ---------- استارت ----------
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚡ به فروشگاه VPN سلام ابوالفضل هستم خوش آمدید ",
        reply_markup=main_menu()
    )

# ---------- دکمه ها ----------
async def buttons(update:Update,context:ContextTypes.DEFAULT_TYPE):
    q=update.callback_query
    await q.answer()

    if q.data=="buy":
        await q.message.edit_text("🧊 انتخاب پلن 👇",reply_markup=glass_list())

    elif q.data.startswith("plan_"):
        code=q.data.split("_")[1]
        t,k=plan_page(code)
        await q.message.edit_text(t,reply_markup=k)

    elif q.data.startswith("buy_"):
        code=q.data.split("_")[1]
        context.user_data["plan"]=PLANS[code]["name"]
        await q.message.reply_text(
            f"🧾 سفارش شما: {PLANS[code]['name']}\n{CARD}"
        )

    elif q.data=="support":
        await q.message.reply_text("پیام خود را ارسال کنید 👇")

    elif q.data=="back":
        await q.message.edit_text("منو اصلی",reply_markup=main_menu())

# ---------- دریافت رسید ----------
async def receive(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user=update.message.from_user
    plan=context.user_data.get("plan","نامشخص")

    msg=f"""
📥 سفارش جدید

👤 {user.first_name}
🆔 {user.id}
💎 پلن: {plan}
"""

    await context.bot.send_message(ADMIN_ID,msg)
    await update.message.reply_text("✅ رسید ثبت شد، بعد تایید ارسال می‌شود")

# ---------- اجرا ----------
app=ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start",start))
app.add_handler(CallbackQueryHandler(buttons))
app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO,receive))

app.run_polling()

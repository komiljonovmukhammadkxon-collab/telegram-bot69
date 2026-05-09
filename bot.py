from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

TOKEN = "8698831407:AAHBqoQIDSs4gTIYdiyBxSiCzVpeJNIEjuU"

# 👤 HAR USER O‘Z DATA
data = {}

def get_user_data(user_id):
    if user_id not in data:
        data[user_id] = {
            "video": [],
            "image": [],
            "link": []
        }
    return data[user_id]

# 🏠 MENU
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📺 VIDEOLAR", callback_data="video")],
        [InlineKeyboardButton("🖼 RASMLAR", callback_data="image")],
        [InlineKeyboardButton("🔗 LINKLAR", callback_data="link")]
    ]

    await update.message.reply_text(
        "📂 O‘zingni kategoriya tanla:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# 📩 SAQLASH (HAR USER ALOHIDA)
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    user_data = get_user_data(user_id)

    msg = update.message

    if msg.video:
        user_data["video"].append(msg.video.file_id)
        return

    if msg.photo:
        user_data["image"].append(msg.photo[-1].file_id)
        return

    if msg.text and msg.text.startswith("http"):
        user_data["link"].append(msg.text)
        return

# 🔘 KO‘RISH
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_data = get_user_data(user_id)

    cat = query.data
    items = user_data.get(cat, [])

    if not items:
        await query.edit_message_text("❌ Hech narsa yo‘q")
        return

    if cat == "video":
        for v in items:
            await query.message.reply_video(v)

    elif cat == "image":
        for i in items:
            await query.message.reply_photo(i)

    elif cat == "link":
        await query.message.reply_text("\n".join(items))

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()


# =========================
# 🚀 RENDER UCHUN QO‘SHIMCHA
# =========================

import os
from flask import Flask
from threading import Thread

web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

Thread(target=run_web).start()

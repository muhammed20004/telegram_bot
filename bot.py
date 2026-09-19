from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
import os

# =========================
# SOZLAMALAR
# =========================

TOKEN = "BOT_TOKEN"

# Sizning Telegram ID raqamingiz
ADMIN_ID = 7873645684

# Rasmlar saqlanadigan papka
IMAGE_FOLDER = "rasmlar"
os.makedirs(IMAGE_FOLDER, exist_ok=True)


# =========================
# ASOSIY MENYU
# =========================

def main_menu():
    keyboard = [
        ["🎨 Dizayn xizmatlari", "🛒 Mahsulotlar"],
        ["🖼️ Rasm yuborish", "📦 Buyurtma berish"],
        ["💬 Savol-javob", "📞 Bog‘lanish"]
    ]

    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Assalomu alaykum! 👋\n\n"
        "Men Ro‘zimuhammad Design Botman. 🤖\n"
        "Quyidagi menyudan kerakli bo‘limni tanlang:",
        reply_markup=main_menu()
    )


# =========================
# DIZAYN XIZMATLARI
# =========================

async def design_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎨 DIZAYN XIZMATLARI\n\n"
        "1. Grafik dizayn\n"
        "2. Tekstil dizayn\n"
        "3. Mato uchun pattern va desen\n"
        "4. Logo dizayn\n"
        "5. Photoshop va Illustrator xizmatlari"
    )


# =========================
# MAHSULOTLAR
# =========================

async def products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛒 MAHSULOTLAR VA XIZMATLAR\n\n"
        "• Mato naqshlari\n"
        "• Tayyor patternlar\n"
        "• Logo dizaynlar\n"
        "• Kiyim uchun printlar\n\n"
        "Buyurtma berish uchun 📦 Buyurtma berish tugmasini bosing."
    )


# =========================
# BUYURTMA BERISH
# =========================

async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_order"] = True

    await update.message.reply_text(
        "📦 BUYURTMA BERISH\n\n"
        "Buyurtmangizni batafsil yozib yuboring.\n"
        "Masalan: Menga futbolka uchun desen kerak."
    )


# =========================
# RASM QABUL QILISH
# =========================

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]

    user = update.effective_user
    username = f"@{user.username}" if user.username else "Username yo‘q"

    # Rasmni kompyuterga saqlash
    file = await context.bot.get_file(photo.file_id)

    filename = os.path.join(
        IMAGE_FOLDER,
        f"{user.id}_{photo.file_unique_id}.jpg"
    )

    await file.download_to_drive(filename)

    # Sizga rasmni yuborish
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo.file_id,
        caption=(
            "🔔 YANGI RASM VA BUYURTMA!\n\n"
            f"👤 Mijoz: {user.full_name}\n"
            f"📱 Username: {username}\n"
            f"🆔 ID: {user.id}\n\n"
            "Mijoz rasm yubordi."
        )
    )

    await update.message.reply_text(
        "✅ Rasmingiz qabul qilindi!\n"
        "Tez orada siz bilan bog‘lanamiz."
    )


# =========================
# SAVOL-JAVOB
# =========================

async def questions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💬 Savolingizni yozib yuboring.\n"
        "Imkon qadar yordam beraman."
    )


# =========================
# BOG‘LANISH
# =========================

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📞 BOG‘LANISH\n\n"
        "👤 Ro‘zimuhammad\n"
        "🎨 Grafik va tekstil dizayner\n"
        "📱 Telegram: @Muhammed_jan04"
    )


# =========================
# MATNLI XABARLAR
# =========================

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    username = f"@{user.username}" if user.username else "Username yo‘q"

    if text == "🎨 Dizayn xizmatlari":
        await design_services(update, context)

    elif text == "🛒 Mahsulotlar":
        await products(update, context)

    elif text == "🖼️ Rasm yuborish":
        await update.message.reply_text(
            "🖼️ Iltimos, rasm yuboring."
        )

    elif text == "📦 Buyurtma berish":
        await order_start(update, context)

    elif text == "💬 Savol-javob":
        await questions(update, context)

    elif text == "📞 Bog‘lanish":
        await contact(update, context)

    elif context.user_data.get("waiting_order"):

        # Buyurtmani sizga yuborish
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "🔔 YANGI BUYURTMA!\n\n"
                f"👤 Mijoz: {user.full_name}\n"
                f"📱 Username: {username}\n"
                f"🆔 ID: {user.id}\n\n"
                f"💬 Buyurtma:\n{text}"
            )
        )

        context.user_data["waiting_order"] = False

        await update.message.reply_text(
            "✅ Buyurtmangiz qabul qilindi!\n"
            "Tez orada siz bilan bog‘lanamiz."
        )

    else:
        await update.message.reply_text(
            "Menyudan kerakli bo‘limni tanlang. 😊",
            reply_markup=main_menu()
        )


# =========================
# BOTNI ISHGA TUSHIRISH
# =========================

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.PHOTO, receive_photo)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )

    print("🤖 Bot ishga tushdi!")

    app.run_polling()


if __name__ == "__main__":
    main()

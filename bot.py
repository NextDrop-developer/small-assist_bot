from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os 
TOKEN = "YOUR_TOKEN"
ADMIN_ID = 123456789

menu = [["Отзывы", "Тех. поддержка"]]

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(menu, resize_keyboard=True)

    await update.message.reply_text(
        "Добро пожаловать!\nВыберите действие:",
        reply_markup=keyboard
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if text == "Отзывы":
        user_state[user_id] = "review"
        await update.message.reply_text("Напишите ваш отзыв:")

    elif text == "Тех. поддержка":
        user_state[user_id] = "support"
        await update.message.reply_text("Опишите вашу проблему:")

    else:
        state = user_state.get(user_id)

        if state == "review":

            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"Новый отзыв:\n\n{text}\n\nот @{update.message.from_user.username}"
            )

            await update.message.reply_text("Спасибо за отзыв!")

            user_state[user_id] = None

        elif state == "support":

            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"Запрос в поддержку:\n\n{text}\n\nот @{update.message.from_user.username}"
            )

            await update.message.reply_text("Ваш запрос отправлен в поддержку.")

            user_state[user_id] = None


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except (KeyboardInterrupt, SystemExit):
        pass
    

import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TELEGRAM_TOKEN")  #Railway
ADMIN_ID = 6127906696  # Telegram ID

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
                text=f"Новый отзыв:\n\n{text}\n\nОт: @{update.message.from_user.username}"
            )

            await update.message.reply_text("Спасибо за отзыв!")
            user_state[user_id] = None

        elif state == "support":

            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"Запрос в поддержку:\n\n{text}\n\nОт: @{update.message.from_user.username}"
            )

            await update.message.reply_text("Ваш запрос отправлен в поддержку.")
            user_state[user_id] = None


async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    await app.run_polling()

    await context.bot.send_message(
    chat_id=ADMIN_ID, 
    text=f"Новий відгук: {text} від @{update.message.from_user.username}"
)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    
    print("Бот запущен...")
    app.run_polling()

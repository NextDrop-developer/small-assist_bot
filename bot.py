import os
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 1. Твои данные (Проверь TOKEN на Railway в переменных!)
TOKEN = os.getenv("TELEGRAM_TOKEN") 
ADMIN_ID = 6127906696 

# Глобальные переменные
menu = [["Отзывы", "Тех. поддержка"]]
user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup(menu, resize_keyboard=True)
    await update.message.reply_text("Добро пожаловать!\nВыберите действие:", reply_markup=keyboard)

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # Если нажали кнопку меню
    if text == "Отзывы":
        user_state[user_id] = "review"
        await update.message.reply_text("Напишите ваш отзыв:")
        return

    elif text == "Тех. поддержка":
        user_state[user_id] = "support"
        await update.message.reply_text("Опишите вашу проблему:")
        return

    # Если прислали текст сообщения
    state = user_state.get(user_id)

    if state == "review":
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"✅ Новый отзыв:\n{text}\nОт: @{update.message.from_user.username}"
        )
        await update.message.reply_text("Спасибо за отзыв!")
        user_state[user_id] = None

    elif state == "support":
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🆘 Запрос в поддержку:\n{text}\nОт: @{update.message.from_user.username}"
        )
        await update.message.reply_text("Ваш запрос отправлен в поддержку.")
        user_state[user_id] = None

async def main():
    # Создаем и настраиваем приложение
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("Бот запущен...")
    
    # На Railway лучше использовать этот метод запуска
    await app.initialize()
    await app.start()
    await app.run_polling(close_loop=False)

if name == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, RuntimeError):
        pass

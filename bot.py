from telegram.ext import ApplicationBuilder
import random
import asyncio
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

choices = ["Камень", "Ножницы", "Бумага"]

menu_keyboard = [["Играть", "Правила"]]
game_keyboard = [["Камень", "Ножницы", "Бумага"]]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Добро пожаловать в игру Камень Ножницы Бумага!\n\nВыбери действие:",
        reply_markup=reply_markup
    )

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Правила:\n\n"
        "Камень бьёт ножницы\n"
        "Ножницы режут бумагу\n"
        "Бумага накрывает камень\n\n"
        "После команды 'Раз Два Три' нажми свой выбор."
    )

async def game_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Готовься...")

    await asyncio.sleep(1)
    await update.message.reply_text("Раз...")

    await asyncio.sleep(1)
    await update.message.reply_text("Два...")

    await asyncio.sleep(1)
    await update.message.reply_text("ТРИ! Выбирай!")

    reply_markup = ReplyKeyboardMarkup(game_keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Нажми кнопку:",
        reply_markup=reply_markup
    )

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.text
    bot = random.choice(choices)

    if user == bot:
        result = "Ничья!"
    elif (
        (user == "Камень" and bot == "Ножницы") or
        (user == "Ножницы" and bot == "Бумага") or
        (user == "Бумага" and bot == "Камень")
    ):
        result = "Ты выиграл!"
    else:
        result = "Я выиграл!"

    reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"Ты выбрал: {user}\n"
        f"Я выбрал: {bot}\n\n"
        f"{result}",
        reply_markup=reply_markup
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Играть":
        await game_start(update, context)

    elif text == "Правила":
        await rules(update, context)

    elif text in choices:
        await play(update, context)

app = ApplicationBuilder().token("8774878227:AAFuoOIU7JYKQ9vgPSYGihh74LG9bDIIx9Q").build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, text_handler))

app.run_polling()
    

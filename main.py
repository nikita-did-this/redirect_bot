from dotenv import load_dotenv
import logging
import os
from asyncio import sleep
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
    PicklePersistence)


load_dotenv()  # использую библиотеку dotenv для доступа к персональной информации
BOT_API = os.getenv("BOT_API")  # HTTP API от BotFather
CHAT_ID = os.getenv("CHAT_ID")  # ID чата для пересылки сообщений

logging.basicConfig(  # Конфигурация логирования для лучшего понимания работы бота
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция запуска бота"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the little goblin's treasury")


async def meme_photo_sender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция пересылки изображения по идентификатору чата"""
    await context.bot.send_photo(chat_id=CHAT_ID, photo=update.message.photo[-1])
    await sleep(4)  # Использую функцию sleep для избежания таймаута бота


async def meme_video_sender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция пересылки видео по идентификатору чата"""
    await context.bot.send_video(chat_id=CHAT_ID, video=update.message.video)
    await sleep(4)  # Использую функцию sleep для избежания таймаута бота


if __name__ == "__main__":  # Точка входа в программу
    # Добавляем персистентность боту (способность кэшировать свое состояние; с персистентностью бот не будет игнорировать сообщения, отправленные вне времени его активности)
    meme_bot_persistence = PicklePersistence(filepath="memebot")
    application = ApplicationBuilder().token(  # Класс-инициатор бота
        BOT_API).persistence(meme_bot_persistence).build()

    # Хэндлер, выполняющий функцию start
    start_handler = CommandHandler("start", start)
    memas_photo_handler = MessageHandler(  # Хэндлер, выполняющий фильтрацию сообщений по параметру (убирает всё, кроме самого фото) и выполняет функцию meme_photo_sender
        filters.FORWARDED & (
            filters.PHOTO |
            filters.PHOTO & filters.TEXT
        ) |
        filters.PHOTO |
        filters.PHOTO & filters.TEXT,
        meme_photo_sender
    )

    memas_video_handler = MessageHandler(  # Хэндлер, выполняющий фильтрацию сообщений по параметру (убирает всё, кроме самого видео) и выполняет функцию meme_video_sender
        filters.FORWARDED & (
            filters.VIDEO |
            filters.VIDEO & filters.TEXT
        ) |
        filters.VIDEO |
        filters.VIDEO & filters.TEXT,
        meme_video_sender
    )

    # Добавление всех ранее описанных хэндлеров с помощью метода класса ApplicationBuilder
    application.add_handler(start_handler)
    application.add_handler(memas_photo_handler)
    application.add_handler(memas_video_handler)

    # Инициализация и запуск бота при помощи метода класса ApplicationBuilder, отключение бота через KeyboardInterrupt или SystemExit
    application.run_polling()

from dotenv import load_dotenv
import logging
import os
from asyncio import Semaphore, sleep
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    BasePersistence,
    ContextTypes,
    CommandHandler,
    filters,
    MessageHandler,
    PicklePersistence)


load_dotenv()
BOT_API = os.getenv("BOT_API")
CHAT_ID = os.getenv("CHAT_ID")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

limit = Semaphore(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    async with limit:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Max bro ya bota napisal")
        await sleep(4)


async def meme_photo_sender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with limit:
        await context.bot.send_photo(chat_id=CHAT_ID, photo=update.message.photo[-1])
        await sleep(4)


async def meme_video_sender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with limit:
        await context.bot.send_video(chat_id=CHAT_ID, video=update.message.video)
        await sleep(4)


if __name__ == "__main__":
    meme_bot_persistence = PicklePersistence(filepath="memebot")
    application = ApplicationBuilder().token(BOT_API).persistence(meme_bot_persistence).build()

    start_handler = CommandHandler("start", start)
    memas_photo_handler = MessageHandler(
        filters.FORWARDED & (
            filters.PHOTO |
            filters.PHOTO & filters.TEXT
        ) |
        filters.PHOTO |
        filters.PHOTO & filters.TEXT,
        meme_photo_sender
    )

    memas_video_handler = MessageHandler(
        filters.FORWARDED & (
            filters.VIDEO |
            filters.VIDEO & filters.TEXT
        ) |
        filters.VIDEO |
        filters.VIDEO & filters.TEXT,
        meme_video_sender
    )

    application.add_handler(start_handler)
    application.add_handler(memas_photo_handler)
    application.add_handler(memas_video_handler)

    application.run_polling()

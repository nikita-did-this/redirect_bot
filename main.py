from dotenv import load_dotenv
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters


load_dotenv()
BOT_API = os.getenv("BOT_API")
CHAT_ID = os.getenv("CHAT_ID")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Max bro ya bota napisal")


async def meme_photo_sender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_photo(chat_id=CHAT_ID, photo=update.message.photo[-1])


async def meme_video_sender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_video(chat_id=CHAT_ID, video=update.message.video)


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_API).build()

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

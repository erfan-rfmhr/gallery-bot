import os

from telegram import Update
from telegram.ext import ContextTypes

from config.settings import STATES
from gallery.markups import CANCEL
from gallery.markups import MAIN_MENU
from services.post import PostService
from services.scrap import ScrapService


async def cancel(update: Update, context: ContextTypes):
    await update.message.reply_text('لغو شد', reply_markup=MAIN_MENU)
    return STATES.START


async def immediate_send(update: Update, context: ContextTypes):
    await update.message.reply_text('لینک را بفرستید.', reply_markup=CANCEL)
    return STATES.SEND_NOW


async def perform_immediate_send(update: Update, context: ContextTypes):
    link = update.message.text

    scrap_service = ScrapService(link)
    image = await scrap_service.download_image()

    with open('temp.jpg', 'wb') as f:
        f.write(image)

    post_service = PostService(caption='تست')
    await post_service.upload_to_telegram(filename='temp.jpg')

    await update.message.reply_text('پست ارسال شد.', reply_markup=MAIN_MENU)

    # delete temp.jpg
    os.remove('temp.jpg')

    return STATES.START

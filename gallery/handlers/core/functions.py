from telegram import Update
from telegram.ext import ContextTypes

from config.settings import STATES
from gallery.markups import CANCEL
from gallery.markups import MAIN_MENU
from gallery.utils import download_image, post_image


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('لغو شد', reply_markup=MAIN_MENU)
    return STATES.START


async def immediate_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('لینک را بفرستید.', reply_markup=CANCEL)
    return STATES.SEND_NOW


async def perform_immediate_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text
    await download_image(link)
    await post_image('temp.jpg')
    await update.message.reply_text('پست ارسال شد.', reply_markup=MAIN_MENU)
    return STATES.START

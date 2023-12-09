from threading import Thread

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
    bot = context.bot
    await bot.send_chat_action(chat_id=update.message.chat_id, action='typing')
    link = update.message.text
    image_src = await download_image(link)
    Thread(target=post_image, args=('test', bot, image_src)).start()
    await update.message.reply_text('پست ارسال شد.', reply_markup=MAIN_MENU)
    return STATES.START


async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('پست مورد نظر را ارسال کنید(عکس به همراه کپشن).', reply_markup=CANCEL)
    return STATES.SEND_NEWS


async def perform_send_news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    file = await bot.get_file(update.message.photo[-1].file_id)
    photo = await file.download_to_drive()
    # TODO: can not upload to facebook because we don't have image source
    Thread(target=post_image, args=(update.message.caption, bot, None, photo.name)).start()

    await update.message.reply_text('پست در حال ارسال است.', reply_markup=MAIN_MENU, connect_timeout=100,
                                    pool_timeout=100,
                                    read_timeout=100, write_timeout=100)
    return STATES.START

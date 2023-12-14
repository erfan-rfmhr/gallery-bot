from datetime import time
from threading import Thread

import pytz
from telegram import Update
from telegram.ext import ContextTypes

from config.settings import STATES
from config.settings import settings
from gallery.markups import CANCEL
from gallery.markups import MAIN_MENU
from gallery.utils import download_image, post_image, post_task


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('لغو شد', reply_markup=MAIN_MENU)
    return STATES.START


async def scheduling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('ساعت های مورد نظر را با فرمت زیر بفرستید.', reply_markup=CANCEL)
    await update.message.reply_text('times:\n8:00\n20:30\n3:10', reply_markup=CANCEL)
    return STATES.SCHEDULE


async def perform_scheduling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.chat_data['id'] = update.message.chat_id
    times = update.message.text.split('\n')[1:]
    for t in times:
        h, m = t.split(':')
        context.job_queue.run_daily(post_task,
                                    time=time(hour=int(h), minute=int(m), tzinfo=pytz.timezone(settings.TIME_ZONE)),
                                    chat_id=update.message.chat_id)
    await update.message.reply_text('زمانبندی انجام شد.', reply_markup=MAIN_MENU)
    return STATES.START


async def immediate_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('لینک را بفرستید.', reply_markup=CANCEL)
    return STATES.SEND_NOW


async def perform_immediate_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    await bot.send_chat_action(chat_id=update.message.chat_id, action='typing')
    link = update.message.text
    image = await download_image(link)
    caption = f'{image.title} | {image.photographer}'
    Thread(target=post_image, args=(caption, bot, image.src)).start()
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

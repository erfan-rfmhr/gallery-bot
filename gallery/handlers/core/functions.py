from datetime import time
from threading import Thread

import aiosqlite
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


async def send_new_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('لینک جدید را بفرستید.', reply_markup=CANCEL)
    return STATES.SEND_NEW_LINK


async def perform_send_new_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with aiosqlite.connect('bot.db') as db:
        links = update.message.text.split('\n')
        for link in links:
            await db.execute('INSERT INTO links (url) VALUES (?)', (link,))
        await db.commit()
    await update.message.reply_text('لینک ذخیره شد.', reply_markup=MAIN_MENU)
    return STATES.START


async def get_links_in_queue(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with aiosqlite.connect('bot.db') as db:
        cursor = await db.execute('SELECT url FROM links WHERE isSent = 0')
        links = await cursor.fetchall()
        if len(list(links)) == 0:
            await update.message.reply_text('هیچ پستی برای ارسال وجود ندارد.', reply_markup=MAIN_MENU)
        else:
            await update.message.reply_text('پست های در صف ارسال:\n' + '\n'.join([link[0] for link in links]),
                                            reply_markup=MAIN_MENU)
        return STATES.START


async def get_posted_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with aiosqlite.connect('bot.db') as db:
        cursor = await db.execute('SELECT url FROM links WHERE isSent = 1')
        links = await cursor.fetchall()
        if len(list(links)) == 0:
            await update.message.reply_text('هیچ پستی ارسال نشده است.', reply_markup=MAIN_MENU)
        else:
            await update.message.reply_text('پست های ارسال شده:\n' + '\n'.join([link[0] for link in links]),
                                            reply_markup=MAIN_MENU)
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
    caption = f'{image.title} | {image.photographer}\n\n'
    for tag in image.tags:
        tag = tag.replace(' ', '')
        caption += f'#{tag} '
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

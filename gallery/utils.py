import asyncio
import hashlib
import os

import aiosqlite
from telegram import Bot as TelegramBot
from telegram.ext import ContextTypes

from services.post import PostService
from services.scrap import ScrapService


def save_image(image: bytes, filename: str = 'temp.jpg'):
    with open(filename, 'wb') as f:
        f.write(image)


def remove_image(filename: str = 'temp.jpg'):
    if os.path.exists(f'{filename}.REMOVE_ME'):
        os.remove(f'{filename}.REMOVE_ME')
    if os.path.exists(filename):
        os.remove(filename)


async def download_image(link: str):
    """Download image from link and save it to temp.jpg"""
    scrap_service = ScrapService(link)
    text = await scrap_service.fetch_url()
    image = await scrap_service.parse(text)
    image_content = await scrap_service.download_image(image.src)

    save_image(image_content, filename=image.name)
    return image


def post_image(caption: str, telegram_bot: TelegramBot, source: str | None = None, filename: str = 'temp.jpg'):
    """Post image to telegram and remove it from disk"""
    post_service = PostService(caption, source)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(post_service.upload_to_telegram(filename=filename, bot=telegram_bot))
    loop.run_until_complete(post_service.upload_to_facebook())
    # await post_service.upload_to_instagram(filename=filename)
    loop.close()
    remove_image(filename=filename)


async def post_task(context: ContextTypes.DEFAULT_TYPE):
    async with aiosqlite.connect('bot.db') as db:
        cursor = await db.execute('SELECT url FROM links WHERE isSent = 0')
        url = await cursor.fetchone()
        if url is None:
            await context.bot.send_message(chat_id=context.chat_data['id'], text='هیچ پستی برای ارسال وجود ندارد.')
            return
        image = await download_image(url[0])
        caption = f'{image.title} | {image.photographer}'
        post_service = PostService(caption=caption, source=image.src)
        # TODO: add facebook and instagram
        await post_service.upload_to_telegram(filename=image.name, bot=context.bot)
        await db.execute('UPDATE links SET isSent = 1 WHERE url = ?', (url[0],))
        await db.commit()
    remove_image(filename=image.name)

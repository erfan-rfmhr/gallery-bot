import asyncio
import os

from telegram import Bot as TelegramBot

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


async def download_image(link: str, filename: str = 'temp.jpg') -> str:
    """Download image from link and save it to temp.jpg"""
    scrap_service = ScrapService(link)
    text = await scrap_service.fetch_url()
    image_src = await scrap_service.parse(text)
    image = await scrap_service.download_image(image_src)
    save_image(image, filename=filename)
    return image_src


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

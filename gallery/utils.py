import os

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


async def download_image(link: str, filename: str = 'temp.jpg'):
    """Download image from link and save it to temp.jpg"""
    scrap_service = ScrapService(link)
    image = await scrap_service.download_image()
    save_image(image, filename=filename)


async def post_image(caption: str, filename: str = 'temp.jpg'):
    """Post image to telegram and remove it from disk"""
    post_service = PostService(caption=caption)
    await post_service.upload_to_telegram(filename=filename)
    await post_service.upload_to_facebook()
    # await post_service.upload_to_instagram(filename=filename)
    remove_image(filename=filename)

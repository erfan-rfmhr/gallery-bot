import os

from services.post import PostService
from services.scrap import ScrapService


async def download_image(link: str, filename: str = 'temp.jpg'):
    """Download image from link and save it to temp.jpg"""
    scrap_service = ScrapService(link)
    image = await scrap_service.download_image()

    with open(filename, 'wb') as f:
        f.write(image)


async def post_image(caption: str, filename: str = 'temp.jpg'):
    """Post image to telegram and remove it from disk"""
    post_service = PostService(caption=caption)
    await post_service.upload_to_telegram(filename=filename)
    post_service.upload_to_instagram(filename=filename)
    if os.path.exists(f'{filename}.REMOVE_ME'):
        os.remove(f'{filename}.REMOVE_ME')
    if os.path.exists(filename):
        os.remove(filename)

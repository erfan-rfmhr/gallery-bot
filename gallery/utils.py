import os

from services.post import PostService
from services.scrap import ScrapService


async def download_image(link: str):
    """Download image from link and save it to temp.jpg"""
    scrap_service = ScrapService(link)
    image = await scrap_service.download_image()

    with open('temp.jpg', 'wb') as f:
        f.write(image)


async def post_image(filename: str):
    """Post image to telegram and remove it from disk"""
    post_service = PostService(caption='تست')
    await post_service.upload_to_telegram(filename=filename)
    os.remove('temp.jpg')

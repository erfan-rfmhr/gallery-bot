from typing import Type

import httpx
from bs4 import BeautifulSoup
from collections import namedtuple

class ScrapService:
    def __init__(self, url: str):
        self.url = url

    async def fetch_url(self) -> str:
        async with httpx.AsyncClient() as client:
            r = await client.get(url=self.url)
            return r.text

    @staticmethod
    async def parse(text: str):
        soup = BeautifulSoup(text, 'html.parser')
        image_src = soup.main.div.div.div.img['src']
        image_title = soup.find('div', class_='image-title').text
        photographer = soup.find('div', class_='detail').a.text

        return namedtuple('Image', ('src', 'title', 'photographer'))(image_src, image_title, photographer)

    @staticmethod
    async def download_image(image_src: str) -> bytes:
        async with httpx.AsyncClient() as client:
            r = await client.get(url=image_src)
            return r.content

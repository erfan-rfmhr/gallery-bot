import hashlib
from collections import namedtuple

import httpx
from bs4 import BeautifulSoup


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
        hashtags_div = soup.find_all('div', class_='image-info-item')[-1]
        a_tags = hashtags_div.find_all('a')
        tags = [a.text for a in a_tags]
        name = image_title + '_' + hashlib.sha256(photographer.encode()).hexdigest() + '.jpg'

        return namedtuple('Image', ('src', 'title', 'photographer', 'tags', 'name'))(image_src, image_title,
                                                                                     photographer, tags, name)

    @staticmethod
    async def download_image(image_src: str) -> bytes:
        async with httpx.AsyncClient() as client:
            r = await client.get(url=image_src)
            return r.content

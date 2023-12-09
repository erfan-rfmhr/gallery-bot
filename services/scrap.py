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
    async def parse(text: str) -> str:
        soup = BeautifulSoup(text, 'html.parser')
        image_src = soup.main.div.div.div.img['src']
        return image_src

    @staticmethod
    async def download_image(image_src: str) -> bytes:
        async with httpx.AsyncClient() as client:
            r = await client.get(url=image_src)
            return r.content

from instabot import Bot as InstaBot
import httpx
from telegram import Bot as TelegramBot

from config.settings import settings


class PostService:
    insta_bot = InstaBot()
    insta_username = settings.INSTAGRAM_USERNAME
    insta_password = settings.INSTAGRAM_PASSWORD

    def __init__(self, caption: str, source: str | None = None):
        self.caption = caption
        self.source = source

    async def upload_to_instagram(self, filename: str):
        bot = self.insta_bot
        bot.login(username=self.insta_username, password=self.insta_password, use_cookie=False)
        bot.upload_photo(photo=filename, caption=self.caption)

    async def upload_to_telegram(self, filename: str, bot: TelegramBot):
        await bot.send_photo(chat_id=settings.TELEGRAM_CHANNEL_ID, photo=open(filename, 'rb'),
                             caption=self.caption, connect_timeout=100, pool_timeout=100, read_timeout=100,
                             write_timeout=100)

    async def upload_to_facebook(self):
        if self.source is not None:
            async with httpx.AsyncClient() as client:
                payload = {
                    'url': self.source,
                    'message': self.caption,
                    'access_token': settings.FACEBOOK_TOKEN
                }
                await client.post(url=settings.FACEBOOK_URL, data=payload)

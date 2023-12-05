# from instabot import Bot as InstaBot
import httpx
from telegram import Bot as TelegramBot

from config.settings import settings


class PostService:
    # insta_bot = InstaBot()
    # insta_username = settings.INSTAGRAM_USERNAME
    # insta_password = settings.INSTAGRAM_PASSWORD

    telegram_channel_id = settings.TELEGRAM_CHANNEL_ID

    def __init__(self, caption: str):
        self.caption = caption

    # async def upload_to_instagram(self, filename: str):
    #     bot = self.insta_bot
    #     bot.login(username=self.insta_username, password=self.insta_password, use_cookie=False)
    #     bot.upload_photo(photo=filename, caption=self.caption)

    async def upload_to_telegram(self, filename: str):
        bot = TelegramBot(token=settings.TELEGRAM_TOKEN)
        await bot.send_photo(chat_id=self.telegram_channel_id, photo=open(filename, 'rb'),
                             caption=self.caption, connect_timeout=100, pool_timeout=100, read_timeout=100, write_timeout=100)
        await bot.close()

    async def upload_to_facebook(self):
        async with httpx.AsyncClient() as client:
            payload = {
                'message': self.caption,
                'access_token': settings.FACEBOOK_TOKEN
            }
            await client.post(url=settings.FACEBOOK_URL, data=payload)

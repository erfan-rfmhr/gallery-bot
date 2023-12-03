from instabot import Bot as InstaBot
from telegram import Bot as TelegramBot

from config.settings import settings


class PostService:
    insta_bot = InstaBot()
    insta_username = settings.INSTAGRAM_USERNAME
    insta_password = settings.INSTAGRAM_PASSWORD

    telegram_bot = TelegramBot(token=settings.TELEGRAM_TOKEN)
    telegram_channel_id = settings.TELEGRAM_CHANNEL_ID

    def __init__(self, caption: str):
        self.caption = caption

    def upload_to_instagram(self, filename: str):
        bot = self.insta_bot
        bot.login(username=self.insta_username, password=self.insta_password)
        bot.upload_photo(photo=filename, caption=self.caption)

    async def upload_to_telegram(self, filename: str):
        await self.telegram_bot.send_photo(chat_id=self.telegram_channel_id, photo=open(filename, 'rb'),
                                           caption=self.caption)

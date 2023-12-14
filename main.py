import asyncio

from telegram.ext import ApplicationBuilder

from config.settings import settings
from database import create_db
from gallery import conversation_handler


def main():
    asyncio.get_event_loop().run_until_complete(create_db())
    app = ApplicationBuilder().token(token=settings.TELEGRAM_TOKEN).build()

    app.add_handler(conversation_handler)

    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()

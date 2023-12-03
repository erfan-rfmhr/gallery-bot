from telegram.ext import ApplicationBuilder

from config.settings import settings


def main():
    app = ApplicationBuilder().token(token=settings.TOKEN).build()

    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()

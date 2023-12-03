from telegram.ext import ApplicationBuilder

from config.settings import settings
from gallery import command_handlers


def main():
    app = ApplicationBuilder().token(token=settings.TOKEN).build()

    for command in command_handlers:
        app.add_handler(command)

    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()

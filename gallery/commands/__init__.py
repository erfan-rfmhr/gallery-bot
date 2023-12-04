from telegram.ext import CommandHandler

from .core import start

start_handler = CommandHandler(start.__name__, start)

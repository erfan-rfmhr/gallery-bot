from telegram.ext import MessageHandler, filters

from .core import cancel

cancel_handler = MessageHandler(callback=cancel, filters=filters.Text(strings=['لغو']))

from telegram.ext import MessageHandler, filters

from .core import cancel, immediate_send

cancel_handler = MessageHandler(callback=cancel, filters=filters.Text(strings=['لغو']))
immediate_send_handler = MessageHandler(callback=immediate_send, filters=filters.Text(strings=['ارسال فوری']))

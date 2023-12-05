from telegram.ext import MessageHandler, filters

from .core import cancel, immediate_send, perform_immediate_send, send_news, perform_send_news

cancel_handler = MessageHandler(callback=cancel, filters=filters.Text(strings=['لغو']))
immediate_send_handler = MessageHandler(callback=immediate_send, filters=filters.Text(strings=['ارسال فوری']))
perform_immediate_send_handler = MessageHandler(callback=perform_immediate_send,
                                                filters=filters.Regex(pattern=r'^https?://.*'))
send_news_handler = MessageHandler(callback=send_news, filters=filters.Text(strings=['ارسال خبر']))
perform_send_news_handler = MessageHandler(callback=perform_send_news, filters=filters.PHOTO)

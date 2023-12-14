from telegram.ext import ConversationHandler

from config.settings import STATES
from .commands import start_handler
from .handlers import (
    cancel_handler, immediate_send_handler, perform_immediate_send_handler, send_news_handler,
    perform_send_news_handler, scheduling_handler, perform_scheduling_handler
)

conversation_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        STATES.START: [start_handler, immediate_send_handler, send_news_handler, scheduling_handler],
        STATES.SEND_NOW: [perform_immediate_send_handler],
        STATES.SEND_NEWS: [perform_send_news_handler],
        STATES.SCHEDULE: [perform_scheduling_handler],
    },
    fallbacks=[cancel_handler],
)

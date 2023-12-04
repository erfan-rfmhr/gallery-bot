from telegram.ext import ConversationHandler

from config.settings import STATES
from .commands import start_handler
from .handlers import cancel_handler, immediate_send_handler

conversation_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        STATES.START: [start_handler, immediate_send_handler],
        STATES.SEND_NOW: [],
    },
    fallbacks=[cancel_handler],
)

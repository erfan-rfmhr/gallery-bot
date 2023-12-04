from telegram.ext import ConversationHandler

from config.settings import STATES
from .commands import start_handler
from .handlers import cancel_handler

conversation_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        STATES.START: [start_handler],
    },
    fallbacks=[cancel_handler],
)

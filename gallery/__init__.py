from .commands import start_handler
from telegram.ext import ConversationHandler
from config.settings import STATES
conversation_handler = ConversationHandler(
    entry_points=[start_handler],
    states={
        STATES.START: [start_handler],
    },
    fallbacks=[],
)

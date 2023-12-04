from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from config.settings import STATES
from gallery.markups import MAIN_MENU


async def cancel(update: Update, context: ContextTypes):
    await update.message.reply_text('لغو شد', reply_markup=MAIN_MENU)
    return STATES.START

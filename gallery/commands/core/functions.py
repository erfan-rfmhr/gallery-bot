from telegram import Update
from telegram.ext import ContextTypes

from config.settings import STATES
from gallery.markups import MAIN_MENU


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_text = 'سلام. به ربات gallery خوش آمدید.'
    await update.message.reply_text(text=reply_text, reply_markup=MAIN_MENU)
    return STATES.START

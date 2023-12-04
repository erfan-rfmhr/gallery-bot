from telegram import Update
from telegram.ext import ContextTypes

from config.settings import STATES
from gallery.markups import CANCEL
from gallery.markups import MAIN_MENU


async def cancel(update: Update, context: ContextTypes):
    await update.message.reply_text('لغو شد', reply_markup=MAIN_MENU)
    return STATES.START


async def immediate_send(update: Update, context: ContextTypes):
    await update.message.reply_text('لینک را بفرستید.', reply_markup=CANCEL)
    return STATES.SEND_NOW

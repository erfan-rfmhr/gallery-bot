from telegram import ReplyKeyboardMarkup

_main_markups = [
    ['ارسال لینک جدید', 'لیست لینکای در نوبت ارسال', 'عکسهای ارسال شده'],
    ['ارسال فوری', 'ارسال خبر', 'تنظیم هشتگهای عمومی'],
    ['زمانبندی'],
]

_cancel_markup = [['لغو']]

MAIN_MENU = ReplyKeyboardMarkup(keyboard=_main_markups, resize_keyboard=True)

CANCEL = ReplyKeyboardMarkup(keyboard=_cancel_markup, resize_keyboard=True)

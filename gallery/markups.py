from telegram import ReplyKeyboardMarkup

_main_markups = [
    ['ارسال لینک جدید', 'لیست لینکای در نوبت ارسال', 'عکسهای ارسال شده'],
    ['ارسال فوری', 'ارسال خبر', 'تنظیم هشتگهای عمومی'],
    ['زمانبندی'],
]

MAIN_MENU = ReplyKeyboardMarkup(keyboard=_main_markups, resize_keyboard=True)

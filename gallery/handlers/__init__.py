from telegram.ext import MessageHandler, filters

from .core import cancel, immediate_send, perform_immediate_send, send_news, perform_send_news, scheduling, \
    perform_scheduling, send_new_link, perform_send_new_link, get_links_in_queue, get_posted_links, \
    perform_set_hashtags, set_hashtags

cancel_handler = MessageHandler(callback=cancel, filters=filters.Text(strings=['لغو']))
send_new_link_handler = MessageHandler(callback=send_new_link, filters=filters.Text(strings=['ارسال لینک جدید']))
perform_send_new_link_handler = MessageHandler(callback=perform_send_new_link,
                                               filters=filters.Regex(pattern=r'^https?://.*'))
get_links_in_queue_handler = MessageHandler(callback=get_links_in_queue,
                                            filters=filters.Text(strings=['لیست لینکای در نوبت ارسال']))
get_posted_links_handler = MessageHandler(callback=get_posted_links, filters=filters.Text(strings=['عکسهای ارسال شده']))
immediate_send_handler = MessageHandler(callback=immediate_send, filters=filters.Text(strings=['ارسال فوری']))
perform_immediate_send_handler = MessageHandler(callback=perform_immediate_send,
                                                filters=filters.Regex(pattern=r'^https?://.*'))
send_news_handler = MessageHandler(callback=send_news, filters=filters.Text(strings=['ارسال خبر']))
perform_send_news_handler = MessageHandler(callback=perform_send_news, filters=filters.PHOTO)
scheduling_handler = MessageHandler(callback=scheduling, filters=filters.Text(strings=['زمانبندی']))
perform_scheduling_handler = MessageHandler(callback=perform_scheduling, filters=filters.Regex("^times:"))
set_hashtags_handler = MessageHandler(callback=set_hashtags, filters=filters.Text(strings=['تنظیم هشتگهای عمومی']))
perform_set_hashtags_handler = MessageHandler(callback=perform_set_hashtags, filters=filters.Regex("^hashtags:"))

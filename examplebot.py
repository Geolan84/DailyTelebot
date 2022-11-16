import datetime
from telegram.ext import Updater, CommandHandler, CallbackContext
import redis
import pytz

TOKEN = "5612846123:AAEWlwDoAKg99DGnU06X-xPFy_F4z347E9I"
redis_server = redis.Redis("localhost")

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
    text="Привет, я буду напоминать тебе о наших мероприятих!")
    if redis_server.get(update.effective_chat.id) == None:
        redis_server.set(update.effective_chat.id, 1)

def daily_suggestion(context: CallbackContext):    
    for chat_id in redis_server.keys():
        context.bot.send_message(chat_id=int(chat_id.decode("UTF-8")),
        text="Просто здравствуй, просто как дела?\n Ждём тебя на встрече сегодня в 14:00!")

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
start_handler = CommandHandler('start', start, pass_job_queue=True)
dispatcher.add_handler(start_handler)

j = updater.job_queue
job_daily = j.run_daily(daily_suggestion, days=(1, 2, 3), time=datetime.time(hour=16, minute=29, tzinfo=pytz.timezone('Europe/Moscow')))

updater.start_polling()
updater.idle()
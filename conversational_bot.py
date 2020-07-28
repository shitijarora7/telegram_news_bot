import logging
from flask import Flask, request
from telegram.ext import CommandHandler, MessageHandler, Filters, Dispatcher
from telegram import Bot, Update, ReplyKeyboardMarkup
from utils import get_reply, fetch_news, topics_keyboard
#the utils library interacts with the news_bot agent we have created on dialogflow

#logging enabled
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

token = '1313444331:AAF1UdOwl25hxDprSQe6zqjYnjTkd51V2NU'

#we create an Flask app object
app = Flask(__name__)


@app.route('/')
def index():
    return "Hello!"


@app.route(f'/{token}', methods=['GET', 'POST'])
def webhook():
    """Webhook view which receives the updates from Telegram"""
    #create update object from json-format request data, we use the request library of the flask module as well
    update = Update.de_json(request.get_json(), bot)
    #process the update
    dp.process_update(update)
    return "Ok"


def start(bot, update):
    print(update)
    author = update.message.from_user.first_name
    msg = update.message.text
    reply = "Hi! {}".format(author)
    bot.send_message(chat_id=update.message.chat_id, text=reply)


def _help(bot, update):
    help_text = "Hey! This is HelpText"
    bot.send_message(chat_id=update.message.chat_id, text=help_text)


def news(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Choose a Category",
                     reply_markup=ReplyKeyboardMarkup(keyboard=topics_keyboard, one_time_keyboard=True))


#we change this function to stop echoing and provide the required output.
def reply_text(bot, update):
    intent, reply = get_reply(update.message.text, update.message.chat_id)
    #the get_reply function uses the chat_id as the session_id for multiple interactions with different users
    #also to prevent the bot to send the required text of one user to another
    #we are also receiving the intent from the return statement in the utils module

    if intent == "get_news":
        articles = fetch_news(reply)
        for article in articles:
            bot.send_message(chat_id=update.message.chat_id, text=article['link'])
        # reply_text = "Ok! I will show you the news with {}".format(reply)
        # bot.send_message(chat_id=update.message.chat_id, text=reply_text)
    else:
        bot.send_message(chat_id=update.message.chat_id, text=reply)


def echo_sticker(bot, update):
    sticker = update.message.sticker.file_id
    bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker)


def error(bot, update):
    logger.error("Update '%s' caused error '%s'", update, update.error)


def main():
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', _help))
    dp.add_handler(CommandHandler('news', news))
    dp.add_handler(MessageHandler(Filters.text, reply_text))
    dp.add_handler(MessageHandler(Filters.sticker, echo_sticker))
    dp.add_error_handler(error)


bot = Bot(token)
try:
    bot.set_webhook("https://telegranewsbot.herokuapp.com/" + token)
except Exception as e:
    print(e)

dp = Dispatcher(bot, None)

main()

if __name__ == '__main__':
    app.run(port=8443)

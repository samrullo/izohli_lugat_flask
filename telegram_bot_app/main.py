from config import Config
import logging
from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters
import requests
import json

updater = Updater(token=Config.bot_token, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="I am flask bot. I will talk to backend flask application!")


def stop(update: Update, context: CallbackContext):
    logging.info(f"will stop the bot {Config.bot_name}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bye, bye, I will stop myself now...")
    updater.stop()


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)

# conversation handler to get user name and email
USERNAME, EMAIL = range(2)
user = {}


def user_register_start(update: Update, context: CallbackContext):
    update.message.reply_text("Let's register a new user! Enter user name first")
    return USERNAME


def username(update: Update, context: CallbackContext):
    user["name"] = update.message.text
    update.message.reply_text("Now enter email")
    return EMAIL


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Cancelling new user registration")
    return ConversationHandler.END


def email(update: Update, context: CallbackContext):
    user["email"] = update.message.text
    response = requests.post(Config.new_user_api_url, json=user)
    update.message.reply_text(f"Yay, we registered {user} and the response is {response.json()}")
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('newuser', user_register_start)],
    states={USERNAME: [MessageHandler(Filters.text & (~Filters.command), username)],
            EMAIL: [MessageHandler(Filters.text & (~Filters.command), email)]},
    fallbacks=[CommandHandler('cancel', cancel)]
)

dispatcher.add_handler(conv_handler)


# get users from API
def all_users(update: Update, context: CallbackContext):
    response = requests.get(Config.users_api_url)
    update.message.reply_text(response.json())


all_users_handler = CommandHandler('all_users', all_users)
dispatcher.add_handler(all_users_handler)

updater.start_polling()

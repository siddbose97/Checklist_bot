import telegram
import telegram.ext
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
import os
from pymongo import MongoClient
import datetime
import logging
from create import create, checkpw, namecl
from dotenv import load_dotenv


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# The API Key we received for our bot
API_KEY = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', 8443))

# Create an updater object with our API Key
updater = Updater(API_KEY)
# Retrieve the dispatcher, which will be used to add handlers
dispatcher = updater.dispatcher
# Our states, as integers

CREATE, CHECKPW, NAMECL, CREATECL, END, CANCEL = range(6)
load_dotenv()

mongo_string = os.getenv('MONGO_STRING')

# The entry function
def start(update_obj, context):
  
    try:

        client = MongoClient(mongo_string)
        db = client.checklists
        creds = db.creds
        creds.insert_one({"date":datetime.datetime.today()})
        update_obj.message.reply_text("Thanks")
        return ConversationHandler.END 
    except Exception as e:
        cancel(e, context)

        

def end(update_obj, context):
    try:
        chat_id = update_obj.message.chat_id
        msg = update_obj.message.text
        update_obj.message.reply_text("Thanks")

        return ConversationHandler.END
    except Exception as e:        
        cancel(update_obj, context)
        return ConversationHandler.END 
    




def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no question for you then, take care, {first_name}! Please click /start to start again",\
             reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END

def outside_of_handler(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Hi {first_name}! Please click /start to start the bot or click /help to learn more",\
             reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END


def main():


    handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),CommandHandler('create', create),CommandHandler('help', help)],
        states={
                CHECKPW: [MessageHandler(Filters.text, checkpw)],
                NAMECL: [MessageHandler(Filters.text, namecl)],
                END: [MessageHandler(Filters.text, end)],
                CANCEL: [MessageHandler(Filters.text, cancel)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        )
    # add the handler to the dispatcher
    dispatcher.add_handler(handler)
    dispatcher.add_handler(MessageHandler(Filters.text | ~Filters.text, outside_of_handler))

    # start polling for updates from Telegram
    updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=API_KEY,
                            webhook_url="https://checklist-bot-62.herokuapp.com/" + API_KEY)
    updater.idle()


if __name__ == '__main__':
    main()
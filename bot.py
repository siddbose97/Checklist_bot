import telegram
import telegram.ext
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
import os
from pymongo import MongoClient
import datetime
import logging
from create import create, checkpw, namecl
from check import checkcl, printcl
from access import accesscl, choosecl, entername
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

CREATE, CHECKPW, NAMECL, CREATECL,CHECKCL,PRINTCL, ACCESSCL, CHOOSECL, ENTERNAME, RETCL, END, CANCEL = range(12)
load_dotenv()

mongo_string = os.getenv('MONGO_STRING')


def help(update_obj, context):
      
    try:

        ret_string = """
        
        Commands are as follows:
        /create - create a new checklist (requires admin password)
        /access - add your name to a checklist
        /check - check the status of an active checklist
        
        Thanks for using the checklist bot!
        """
        update_obj.message.reply_text(ret_string)
        return ConversationHandler.END 
    except Exception as e:
        cancel(e, context)       


def cancel(update_obj, context):
    update_obj.message.reply_text(
        f"You have cancelled the transaction, please click /help for a list of commands",\
             reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END

def outside_of_handler(update_obj, context):
    update_obj.message.reply_text(
        f"Incorrect input, please click /help for a list of commands",\
             reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END


def main():


    handler = ConversationHandler(
        entry_points=[CommandHandler('start', help),CommandHandler('create', create),CommandHandler('check', checkcl),\
            CommandHandler('access', accesscl), CommandHandler('help', help)],
        states={
                CHECKPW: [MessageHandler(Filters.text, checkpw)],
                NAMECL: [MessageHandler(Filters.text, namecl)],
                PRINTCL: [MessageHandler(Filters.text, printcl)],
                CHOOSECL: [MessageHandler(Filters.text, choosecl)],
                ENTERNAME: [MessageHandler(Filters.text, entername)],
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
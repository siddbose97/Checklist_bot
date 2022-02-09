from pymongo import MongoClient
import os
from dotenv import load_dotenv
import telegram
import telegram.ext
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
CREATE, CHECKPW, NAMECL, CREATECL, END, CANCEL = range(6)

########################################################################
load_dotenv()

mongo_string = os.getenv('MONGO_STRING')
client = MongoClient(mongo_string)

########################################################################

def create(update_obj, context):
      
    try:
        update_obj.message.reply_text("Please enter password to create checklist")
    # go to the Batallion state
        return CHECKPW
    except Exception as e:
        cancel(e, context)

def checkpw(update_obj, context):
    try:
        msg = update_obj.message.text
        pw = "admin62"
        if msg == pw:
            update_obj.message.reply_text("Correct PW! Please type in name of checklist")
            return NAMECL
        else:
            update_obj.message.reply_text("SORRY INCORRECT PW")
            return ConversationHandler.END    
    except Exception as e:
        cancel(e, context)

def namecl(update_obj, context):
    try:
        msg = update_obj.message.text

        db = client.checklists
        active_checklists = db.active_checklists
        result = active_checklists.insert_one({"checklist name":msg})

        update_obj.message.reply_text(f"Your new checklist is named {msg}. Please ask depot to access this checklist")
        return ConversationHandler.END
    except Exception as e:
        cancel(e, context)

def cancel(update_obj, context):
    # get the user's first name
    first_name = update_obj.message.from_user['first_name']
    update_obj.message.reply_text(
        f"Okay, no question for you then, take care, {first_name}! Please click /start to start again",\
             reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END
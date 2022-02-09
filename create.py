from pymongo import MongoClient
import os
from dotenv import load_dotenv
import telegram
import telegram.ext
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
CREATE, CHECKPW, NAMECL, CREATECL, END, CANCEL = range(6)

########################################################################
load_dotenv()

mongo_string = str(os.getenv('MONGO_STRING'))


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
        client = MongoClient(mongo_string)
        db = client.checklists
        creds = db.creds
        creds.insert_one({"password":"hi"})
        return ConversationHandler.END
        # my_query = {"password": msg}

        # try:
        #     
        #     update_obj.message.reply_text(cursor)
        #     return NAMECL

        # pw = "admin62"
        # if msg == pw:
        #     # update_obj.message.reply_text("Correct PW! Please type in name of checklist")
        #     update_obj.message.reply_text(type(mongo_string))
        #     return NAMECL
        # except:
        #     update_obj.message.reply_text("SORRY INCORRECT PW")
        #     return ConversationHandler.END    
    except Exception as e:
        cancel(e, context)

def namecl(update_obj, context):
    try:
        msg = update_obj.message.text
        # client = MongoClient(mongo_string)
        # db = client.checklists
        # active_checklists = db.active_checklists
        # print(f"db = {db}")
        # print(f"checklists={active_checklists}")
        update_obj.message.reply_text(f"Your new checklist is named {msg}. Please ask depot to access this checklist")
        # active_checklists.insert_one({"checklist name":msg})

        return ConversationHandler.END
    except Exception as e:
        cancel(e, context)

def cancel(update_obj, context):
    # get the user's first name
    #update_obj.message.reply_text(
    #    f"Okay, no question for you then, take care! Please click /start to start again",\
    #         reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END
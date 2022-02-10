from construct import Check
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import telegram
import telegram.ext
from datetime import datetime
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters
CREATE, CHECKPW, NAMECL, CREATECL, END, CANCEL = range(6)

########################################################################
class Checklist:
    def __init__(self, roster, name):
        self.name = name
        self.unchecked = roster
        self.checked = []
        self.date = datetime.today()
    
    def ret_dict(self):
        dic = {
            "name":self.name,
            "unchecked":self.unchecked,
            "checked":self.checked,
            "date":self.date
        }


########################################################################

def create(update_obj, context):
      
    try:
        update_obj.message.reply_text("Please enter password to create checklist")
        return CHECKPW
    except Exception as e:
        cancel(e, context)

def checkpw(update_obj, context):
    try:
        load_dotenv()
        mongo_string = str(os.getenv('MONGO_STRING'))
        msg = update_obj.message.text
        print("here1")
        client = MongoClient(mongo_string)
        db = client.checklists
        creds = db.creds
        print("here2")
        my_query = {"password": msg}
        print("here3")
        if creds.count_documents(my_query, limit = 1):
            print("here4")
            update_obj.message.reply_text("Thank you, please enter name of new checklist")
            return NAMECL
        else:
            update_obj.message.reply_text("SORRY INCORRECT PW")
            return ConversationHandler.END
   
    except Exception as e:
        cancel(e, context)

def namecl(update_obj, context):
    try:
        msg = update_obj.message.text
        load_dotenv()
        mongo_string = str(os.getenv('MONGO_STRING'))
        msg = update_obj.message.text
        client = MongoClient(mongo_string)

        db = client.checklists
        active_checklists = db.active_checklists

        roster = active_checklists.find_one({"is_roster":"yes"})["roster"]
        new_check = Checklist(roster, msg)
        active_checklists.insert_one(new_check.ret_dict())

        #still need to check for old dicts and remove them
        update_obj.message.reply_text(f"Your new checklist is named {msg}. Please ask depot to access this checklist")

        return ConversationHandler.END
    except Exception as e:
        cancel(e, context)

def cancel(update_obj, context):
    # get the user's first name
    #update_obj.message.reply_text(
    #    f"Okay, no question for you then, take care! Please click /start to start again",\
    #         reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END
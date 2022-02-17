from pymongo import MongoClient
import os
from dotenv import load_dotenv
import telegram
import telegram.ext
from datetime import datetime, timedelta
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

CREATE, CHECKPW, NAMECL, CREATECL,CHECKCL,PRINTCL, ACCESSCL, CHOOSECL, ENTERNAME, RETCL, END, CANCEL = range(12)

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
            "date":self.date,
            "is_list":"yes"
        }

        return dic


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
        client = MongoClient(mongo_string)
        db = client.checklists
        creds = db.creds
        my_query = {"password": msg}
        if creds.count_documents(my_query, limit = 1):
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
        doc_to_insert = new_check.ret_dict()
        active_checklists.insert_one(doc_to_insert)

        #still need to check if a checklist with the given name already exists!!!!!!
        
        update_obj.message.reply_text(f"Your new checklist is named {msg}. Please ask depot to access this checklist")
        
        
        week_ago = datetime.today()- timedelta(days=5)
        week_ago_query = {"date": {"$lt":week_ago}}
        cursor = active_checklists.find(week_ago_query)
        
        for old_checklist in cursor:
            print(old_checklist)
            active_checklists.delete_one(old_checklist)

        return ConversationHandler.END
    except Exception as e:
        cancel(e, context)

def cancel(update_obj, context):
    # get the user's first name
    #update_obj.message.reply_text(
    #    f"Okay, no question for you then, take care! Please click /start to start again",\
    #         reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import telegram
import telegram.ext
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

CREATE, CHECKPW, NAMECL, CREATECL,CHECKCL,PRINTCL, ACCESSCL, CHOOSECL, ENTERNAME, RETCL, END, CANCEL = range(12)


def accesscl(update_obj, context):
      
    try:
        load_dotenv()
        mongo_string = str(os.getenv('MONGO_STRING'))
        client = MongoClient(mongo_string)

        db = client.checklists
        active_checklists = db.active_checklists
        arr_of_checklists = []
        is_list_query = {"is_list":"yes"}
        cursor = active_checklists.find(is_list_query)
        
        for checklist in cursor:
            arr_of_checklists.append(checklist["name"])
        
        if arr_of_checklists:
            
            list1 = [[telegram.KeyboardButton(text=checklist_name)] for checklist_name in arr_of_checklists]
            kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

            update_obj.message.reply_text("Please choose a checklist from the following active lists",reply_markup=kb)
            return CHOOSECL
        else:
            
            update_obj.message.reply_text("There are no active checklists at the moment")
            return ConversationHandler.END
    except Exception as e:
        cancel(e, context)

def choosecl(update_obj, context):
      
    try:
        msg = update_obj.message.text
        global checklist_name 
        checklist_name = msg
        load_dotenv()
        mongo_string = str(os.getenv('MONGO_STRING'))
        client = MongoClient(mongo_string)

        db = client.checklists
        active_checklists = db.active_checklists
        checklist = active_checklists.find_one({"name":msg})
        unchecked = checklist["unchecked"]

        list1 = [[telegram.KeyboardButton(text=names)] for names in unchecked]
        kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

        update_obj.message.reply_text("Please select your name from the list",reply_markup=kb)


        return ENTERNAME
    except Exception as e:
        cancel(e, context)

def entername(update_obj, context):
      
    try:
        msg = update_obj.message.text

        load_dotenv()
        mongo_string = str(os.getenv('MONGO_STRING'))
        client = MongoClient(mongo_string)

        db = client.checklists
        active_checklists = db.active_checklists
        checklist = active_checklists.find_one({"name":checklist_name})
        checked = checklist["checked"]
        unchecked = checklist["unchecked"]

        unchecked.remove(msg)
        checked.append(msg)

        active_checklists.update_one({"name":checklist_name},{ "$set": { 'checked': checked } })
        active_checklists.update_one({"name":checklist_name},{ "$set": { 'unchecked': unchecked } })

        checked_string = "People who have been checked off: "
        for names in checked:
            checked_string += names
            checked_string += "\n"
        unchecked_string = "People who have NOT been checked off: "
        for names in unchecked:
            unchecked_string += names
            unchecked_string += "\n"

        update_obj.message.reply_text(f"The updated checklist is as follows:")
        update_obj.message.reply_text(checked_string)
        update_obj.message.reply_text(unchecked_string)




        return ConversationHandler.END
    except Exception as e:
        cancel(e, context)

def retcl(update_obj, context):
      
    try:
        

        return ConversationHandler.END
    except Exception as e:
        cancel(e, context)

def cancel(update_obj, context):
    # get the user's first name
    #update_obj.message.reply_text(
    #    f"Okay, no question for you then, take care! Please click /start to start again",\
    #         reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END
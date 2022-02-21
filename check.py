from pymongo import MongoClient
import os
from dotenv import load_dotenv
import telegram
import telegram.ext
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters

CREATE, CHECKPW, NAMECL, CREATECL,CHECKCL,PRINTCL, ACCESSCL, CHOOSECL, ENTERNAME, RETCL, END, CANCEL = range(12)

def checkcl(update_obj, context):
      
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
            list1.append([telegram.KeyboardButton(text="QUIT")])
            kb = telegram.ReplyKeyboardMarkup(keyboard=list1,resize_keyboard = True, one_time_keyboard = True)

            update_obj.message.reply_text("Please choose a checklist from the following active lists",reply_markup=kb)
            return PRINTCL
        else:
            update_obj.message.reply_text("There are no active checklists at the moment. Please click /help for a list of commands")
            return ConversationHandler.END
    except Exception as e:
        cancel(e, context)

def printcl(update_obj, context):
      
    try:
        msg = update_obj.message.text

        if msg == "QUIT":
            cancel(update_obj, context)
            return ConversationHandler.END

        load_dotenv()
        mongo_string = str(os.getenv('MONGO_STRING'))
        msg = update_obj.message.text
        client = MongoClient(mongo_string)

        db = client.checklists
        active_checklists = db.active_checklists

        checklist = active_checklists.find_one({"name":msg})
        if checklist == None:
            update_obj.message.reply_text(f"No checklist with the given name was found. Please click /help for a list of commands", reply_markup=telegram.ReplyKeyboardRemove())
        else:
            checked = checklist["checked"]
            unchecked = checklist["unchecked"]

            len_checked = len(checked)
            len_unchecked = len(unchecked)
            checked_string = f"People who have been checked off: ({len_checked}) \n"
            for names in checked:
                checked_string += names
                checked_string += "\n"
            unchecked_string = f"People who have NOT been checked off: ({len_unchecked}) \n"
            for names in unchecked:
                unchecked_string += names
                unchecked_string += "\n"

            update_obj.message.reply_text(f"For the checklist named {msg} the information is as follows:", reply_markup=telegram.ReplyKeyboardRemove())
            update_obj.message.reply_text(checked_string)
            update_obj.message.reply_text(unchecked_string)

        return ConversationHandler.END
    except Exception as e:
        cancel(e, context)


def cancel(update_obj, context):
    update_obj.message.reply_text(
        f"You have cancelled the transaction, please click /help for a list of commands",\
             reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END
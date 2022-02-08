from pymongo import MongoClient
import datetime
from pprint import pprint
import os
from dotenv import load_dotenv

load_dotenv()

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
mongo_string = os.getenv('MONGO_STRING')
client = MongoClient(mongo_string)
db = client.gettingStarted

class Checklist:
    def __init__(self, roster, name):
        self.name = name
        self.unchecked = roster
        self.checked = []
        self.date = ""

roster = ["sidd", "somu"]
name = "new list"
new_check = Checklist(roster, name)
new_check_dict = {
    "name":new_check.name,
    "unchecked":new_check.unchecked,
    "checked":new_check.checked,
    "date":datetime.datetime.now()
}

checklists = db.checklists


#result = checklists.insert_one(new_check_dict)
#new_check_dict = checklists.find_one({'_id': result.inserted_id})
if new_check_dict is not None:
    checked = new_check_dict["checked"]
    unchecked = new_check_dict["unchecked"]

    checked.append("sidd1")
    unchecked.remove("sidd")
    
    newvalues = { "$set": { 'unchecked': unchecked } }
    newvalues1 = { "$set": { 'checked': checked } }

    checklists.update_one({'name' :new_check.name},newvalues)
    checklists.update_one({'name' :new_check.name},newvalues1)


#create database 
db = client.checklists

#create collection 
active_checklists = db.active_checklists

#add checklist (document) to collection 
result = active_checklists.insert_one({"date":datetime.datetime.today()})

#make a query
week_ago = datetime.datetime.today()- datetime.timedelta(days=7)
my_query = {"date": {"$lt":week_ago}}

name_query = {"name": "new checklist"}

#find checklist
cursor = active_checklists.find(my_query)
cursor1= active_checklists.find(name_query)

#write to/update checklist

#delete checklist

#change default roster

#delete checklist(s) based on date query
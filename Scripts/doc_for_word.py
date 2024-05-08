import os

from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
from pymongo.server_api import ServerApi
from lxml import html
from datetime import datetime
from bs4 import BeautifulSoup
uri = "mongodb+srv://yehonatanavami:ssYyqfJCrDmbwulW@hamas1.ntgslmi.mongodb.net/?retryWrites=true&w=majority&appName=hamas1"
# Connect to MongoDB
client = MongoClient(uri, server_api=ServerApi('1'), unicode_decode_error_handler='ignore')
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['hamas1']
collection = db['hamas_arc1']
cursor = collection.find({})  # Retrieve all documents, you can add query filters as needed

# Iterate over the cursor to access the documents

category_words1 = ["لقد أعذر من أنذر","بانفجار كبير","انفجار كبير","سلسلة من الانفجارات","غضب الأقصى سينفجر", "سيفجر المنطقة","انفجار الأوضاع","تفجير الأوضاع","سيفجر بركاناً من الغضب","بركانا سيحرق","صاعق التفجير","انفجار مبكرًا","فتيل الانفجار قصير","أعمال المقاومة","بداية المعركة","عواقب في المنطقة","لدفع الروح والدم فداء لمسجدهم المقدس"]


def create_dirs(dir_name):
    # Step 1: Create the directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"Directory '{dir_name}' created.")
    else:
        print(f"Directory '{dir_name}' already exists.")
def create_files(i, text):
    file_path = os.path.join("category_one", str(i)+".txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)


def create_text(item,i):
    text=""
    title = item.get("title", "").strip()  # Get the title and remove leading/trailing spaces
    body = item.get("body", "").strip()  # Get the text and remove leading/trailing spaces
    link = item.get("link", "").strip()  # Get the text and remove leading/trailing spaces
    category1_list = item.get('category1_list', "")
    category2_list = item.get('category2_list', "")
    category3_list = item.get('category3_list', "")
    count_category1 = item.get('count_category1', "")
    count_category2 = item.get("count_category2", "")
    count_category3 = item.get("count_category3", "")
    text="title: " + title + "\n\nlink: " + link
    text+= "\nWords level 1:" + str(count_category1) + "   " + str(category1_list)
    text+= "\nWords level 2:" + str(count_category2) + "   " + str(category2_list)
    text+=  "\nWords level 3:" + str(count_category3) + "   " + str(category3_list)
    text+= "\n\n\n"+body
    create_files(i,text)


bank={}
create_dirs("category_one")

for word in category_words1:
    i = 1;
    cursor.rewind()
    bank[word]=-1
    for document in cursor:
        title = document.get("title", "").strip()  # Get the title and remove leading/trailing spaces
        text = document.get("body", "").strip()  # Get the text and remove leading/trailing spaces
        s=title+" "+text
        if word in s:
            bank[word]=i
            create_text(document, i)
            break
        print(i)
        i+=1

print(bank)

print("Categorization process completed.")
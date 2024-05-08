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


def extract_last_number(url):
    # Split the URL by '/' and filter out empty strings
    parts = [part for part in url.split('/') if part]
    # The last number is the last part of the URL
    return parts[-1]

bank=[]
i=0
for document in cursor:
    link = document.get("link", "").strip()
    number = extract_last_number(link)
    bank.append(int(number))
    print(i)
    i+=1

print(bank)
print(min(bank))
print(max(bank))
print("Categorization process completed.")
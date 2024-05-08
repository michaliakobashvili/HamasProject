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

bank = {}
category_words1 = ["لقد أعذر من أنذر","بانفجار كبير","انفجار كبير","سلسلة من الانفجارات","غضب الأقصى سينفجر", "سيفجر المنطقة","انفجار الأوضاع","تفجير الأوضاع","سيفجر بركاناً من الغضب","بركانا سيحرق","صاعق التفجير","انفجار مبكرًا","فتيل الانفجار قصير","أعمال المقاومة","بداية المعركة","عواقب في المنطقة","لدفع الروح والدم فداء لمسجدهم المقدس"]
category_words2 = ["وقود نار سيحرقه", "آتون بطوفان هادر" , "يلعب بالنار" , "بإشعال المنطقة", "إشعال المنطقة" , "نحرق الأرض","سنحرق الأرض تحت أقدامهم" , "حرب دينية" , "تنقل هذه النيران إلى عمق كيان الاحتلال" , "حقل ألغام" , "سيأجج الأوضاع"]
category_words3 =["اعلان حرب", "الهولوكوست", "هولوكوست", "سيناريوهات التصعيد", "نضرب بقبضة واحدة", "طريق الرشاش", "تجاوز الخطوط الحمراء", "الخطوط الحمراء", "المقاومة لن تسمح بتجاوز الخطوط الحمراء في المسجد الأقصى", "ضرب هذا العدو المتغطرس بيد من حديد", "ضرب بيد من حديد", "بالدم والرصاص والسلاح", "سيدفع العدو ثمنه غاليًا", "مواجهة اضطرارية", "الالتحام قريباً", "الأقصى ليس وحيداً ودونه الدماء والأرواح", "رد بكل قوة وبكل الأدوات", "لمواجهة المخططات الصهيونية", "التصدي لاعتداءات الاحتلال"]

def create_bank():
    for word in category_words1:
        bank[word]=0
    for word in category_words2:
        bank[word]=0
    for word in category_words3:
        bank[word]=0

def word_in_text(text):
    for word in category_words1:
        if word in text:
            bank[word]+=1
    for word in category_words2:
        if word in text:
            bank[word]+=1
    for word in category_words3:
        if word in text:
            bank[word]+=1
i=1;
create_bank()
for document in cursor:
    title = document.get("title", "").strip()  # Get the title and remove leading/trailing spaces
    text = document.get("body", "").strip()  # Get the text and remove leading/trailing spaces
    word_in_text(title+" "+text)
    print(i)
    i+=1
print("category 1: ")
for word_in_bank in bank:
    # Check if the word in the bank is also in the list of words
    if word_in_bank in category_words1:
        print(word_in_bank + ": "+ str(bank[word_in_bank]))
print("category 2: ")
for word_in_bank in bank:
    # Check if the word in the bank is also in the list of words
    if word_in_bank in category_words2:
        print(word_in_bank + ": "+ str(bank[word_in_bank]))
print("category 3: ")
for word_in_bank in bank:
    # Check if the word in the bank is also in the list of words
    if word_in_bank in category_words3:
        print(word_in_bank + ": "+ str(bank[word_in_bank]))
#print(bank)
print("Categorization process completed.")
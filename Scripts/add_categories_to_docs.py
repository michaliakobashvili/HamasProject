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
category_words2 = ["وقود نار سيحرقه", "آتون بطوفان هادر" , "يلعب بالنار" , "بإشعال المنطقة", "إشعال المنطقة" , "نحرق الأرض","سنحرق الأرض تحت أقدامهم" , "حرب دينية" , "تنقل هذه النيران إلى عمق كيان الاحتلال" , "حقل ألغام" , "سيأجج الأوضاع"]
category_words3 =["اعلان حرب", "الهولوكوست", "هولوكوست", "سيناريوهات التصعيد", "نضرب بقبضة واحدة", "طريق الرشاش", "تجاوز الخطوط الحمراء", "الخطوط الحمراء", "المقاومة لن تسمح بتجاوز الخطوط الحمراء في المسجد الأقصى", "ضرب هذا العدو المتغطرس بيد من حديد", "ضرب بيد من حديد", "بالدم والرصاص والسلاح", "سيدفع العدو ثمنه غاليًا", "مواجهة اضطرارية", "الالتحام قريباً", "الأقصى ليس وحيداً ودونه الدماء والأرواح", "رد بكل قوة وبكل الأدوات", "لمواجهة المخططات الصهيونية", "التصدي لاعتداءات الاحتلال"]
def assign_category(item,category_words):
    sum=0

    title = item.get("title", "").strip()  # Get the title and remove leading/trailing spaces
    text = item.get("body", "").strip()  # Get the text and remove leading/trailing spaces
    bank={}
    for word in category_words:
        if word in title or word in text:
            sum+=1
            bank[word]=text.count(word)+title.count(word)

    return bank,sum  # No matching category found

# Iterate through each item in the collection

# Define the target document _id
#target_document_id = ObjectId("66001f3f3482ab47840e977c")

# Query for the document with the specified _id
#document = collection.find_one({"_id": target_document_id})
i=0;
for document in cursor:
    # Perform your action on the target document here
    category1, sum1 = assign_category(document, category_words1)
    category2, sum2 = assign_category(document, category_words2)
    category3, sum3 = assign_category(document, category_words3)
    # Update the item with the assigned category
    collection.update_one({"_id": document["_id"]}, {"$set": {"category1_list": category1}})
    collection.update_one({"_id": document["_id"]}, {"$set": {"count_category1": sum1}})
    collection.update_one({"_id": document["_id"]}, {"$set": {"category2_list": category2}})
    collection.update_one({"_id": document["_id"]}, {"$set": {"count_category2": sum2}})
    collection.update_one({"_id": document["_id"]}, {"$set": {"category3_list": category3}})
    collection.update_one({"_id": document["_id"]}, {"$set": {"count_category3": sum3}})
    print(f"{i}: Item '{document['title']}' categorized as '{category3}'.")
    i=i+1;


print("Categorization process completed.")
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


import os


def create_dirs(dir_name):
    # Step 1: Create the directory if it does not exist
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print(f"Directory '{dir_name}' created.")
    else:
        print(f"Directory '{dir_name}' already exists.")
def create_files(i, text,dir):
    file_path = os.path.join(dir, str(i)+".txt")
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)


# Create directory and files
create_dirs("C1")
create_dirs("C2")
create_dirs("C3")
create_dirs("C4")
i=1
for item in cursor:
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
    count_category1 = item.get('count_category1', "")
    count_category2 = item.get("count_category2", "")
    count_category3 = item.get("count_category3", "")
    if "أعمال المقاومة" in category1_list:
        del category1_list["أعمال المقاومة"]
    if(len(category1_list)>1 or count_category2>1 or count_category3>1):
        create_files(i, text, "C1")
    else:
        if(len(category1_list)>0):
            create_files(i, text, "C2")
        else:
            if (count_category3 > 0 or count_category2 > 0):
                create_files(i, text, "C3")
            else:
                create_files(i, text, "C4")
    i=i+1;
    print(i)






category_words1 = ["لقد أعذر من أنذر","بانفجار كبير","انفجار كبير","سلسلة من الانفجارات","غضب الأقصى سينفجر", "سيفجر المنطقة","انفجار الأوضاع","تفجير الأوضاع","سيفجر بركاناً من الغضب","بركانا سيحرق","صاعق التفجير","انفجار مبكرًا","فتيل الانفجار قصير","أعمال المقاومة","بداية المعركة","عواقب في المنطقة","لدفع الروح والدم فداء لمسجدهم المقدس"]
category_words2 = ["وقود نار سيحرقه", "آتون بطوفان هادر" , "يلعب بالنار" , "بإشعال المنطقة", "إشعال المنطقة" , "نحرق الأرض","سنحرق الأرض تحت أقدامهم" , "حرب دينية" , "تنقل هذه النيران إلى عمق كيان الاحتلال" , "حقل ألغام" , "سيأجج الأوضاع"]
category_words3 =["اعلان حرب", "الهولوكوست", "هولوكوست", "سيناريوهات التصعيد", "نضرب بقبضة واحدة", "طريق الرشاش", "تجاوز الخطوط الحمراء", "الخطوط الحمراء", "المقاومة لن تسمح بتجاوز الخطوط الحمراء في المسجد الأقصى", "ضرب هذا العدو المتغطرس بيد من حديد", "ضرب بيد من حديد", "بالدم والرصاص والسلاح", "سيدفع العدو ثمنه غاليًا", "مواجهة اضطرارية", "الالتحام قريباً", "الأقصى ليس وحيداً ودونه الدماء والأرواح", "رد بكل قوة وبكل الأدوات", "لمواجهة المخططات الصهيونية", "التصدي لاعتداءات الاحتلال"]


print("Categorization process completed.")
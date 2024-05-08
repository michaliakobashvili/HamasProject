from pymongo import MongoClient
import requests
from pymongo.server_api import ServerApi
from lxml import html
from datetime import datetime
from bs4 import BeautifulSoup
uri = "mongodb+srv://yehonatanavami:ssYyqfJCrDmbwulW@hamas1.ntgslmi.mongodb.net/?retryWrites=true&w=majority&appName=hamas1"
# Connect to MongoDB
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['hamas1']
collection = db['hamas_arc1']
words = { "القدس","قدس","المسجد الأقصى","الأقصى","الحرم الشريف"}
# Function to scrape articles and store them in MongoDB
def store_articles(link,title,body):
        print("yes store #####################")
        article_data = {
            'link': link,
            'title': title,
            'body': body
        }
        collection.insert_one(article_data)



def artc(url):
    try:
        # Send a GET request to the URL
        headers = {'User-Agent': 'Mozilla/5.0'}  # Providing a user-agent header
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            tree = html.fromstring(response.content)
            # Define XPath expression to select links inside <h2> tags within <article> div
            xpath_expression = "//div[contains(@class,'et_pb_column et_pb_column_2_3')]//div[contains(@class, 'et_pb_blog_0_tb_body')]//h2//a/@href"
            # Extract links using XPath
            links = tree.xpath(xpath_expression)
            # Print the links
            for link in links:
                if(is_within_date_range(link)):
                   get_title_and_paragraph(link)
                   print("Link:", link)

        elif response.status_code == 403:
            print("Access to the requested resource is forbidden (HTTP 403).")
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
    except requests.RequestException as e:
        print("An error occurred:", e)


def is_within_date_range(url):
    # Extract year, month, and day from the URL
    parts = url.split('/')
    year = int(parts[4])
    month = int(parts[5])
    day = int(parts[6])

    # Create datetime object from the extracted date
    date = datetime(year, month, day)

    # Define the start and end dates of the range
    start_date = datetime(2022, 10, 1)
    end_date = datetime(2023, 10, 31)

    # Check if the extracted date falls within the range
    return start_date <= date <= end_date


def get_title_and_paragraph(url):
    headers = {'User-Agent': 'Mozilla/5.0'}  # Providing a user-agent header
    response = requests.get(url, headers=headers)
    f=0
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the title element
        title_element = soup.find('h1', class_='post_title')
        if title_element:
            title = title_element.text.strip()
            for word in words:
                  if word in title:
                     f = 1
        else:
            print("Title not found.")

        # Find the paragraph element
        paragraph_element = soup.find('div',
                                      class_='et_pb_module et_pb_post_content et_pb_post_content_0_tb_body post-content-text')
        if paragraph_element:
            paragraph = paragraph_element.text.strip()
            for word in words:
                if word in paragraph:
                    f = 1
        else:
            print("Paragraph not found.")
        if f==1:
          store_articles(url,title,paragraph)
    else:
        print("Failed to fetch the webpage.")

if __name__ == "__main__":

    base_url = "https://palinfo.com/category/news/page/{}/?et_blog"

    for page_number in range(317, 1350):
        url = base_url.format(page_number)
        print (url);
        response = requests.get(url)
        artc(url)



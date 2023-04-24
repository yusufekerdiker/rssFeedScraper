"""
import requests
import json
import xmltodict

result = requests.get("https://www.technopat.net/feed")
with open(result) as xml_file:
    data_dict = xmltodict.parse(xml_file.read())
    json_data = json.dumps(data_dict)
# result = result.text
json_data = json.loads(json_data.text)

# print(type(result))
# print(result)
print(json_data[0]["title"])
"""

### START OF MONGO SETUP ###
from dotenv import load_dotenv, find_dotenv
import os
import pprint
from pymongo import MongoClient
import json

# https://stackoverflow.com/questions/52930341/pymongo-dnspython-module-must-be-installed-to-use-mongodbsrv-uris
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connection_string = f"mongodb+srv://yusufekerdiker:{password}@mycluster.fma9e4h.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
### END OF MONGO SETUP ###

from bs4 import BeautifulSoup
import requests

url = requests.get("https://www.technopat.net/feed")
# print(url)
soup = BeautifulSoup(url.content, "xml")

# find all news which is inside item tag
items = soup.find_all("item")

for item in items:
    # loop in the news and get details of it
    title = item.title.text
    link = item.link.text
    creator = item.creator.text
    publishDate = item.pubDate.text

    """
    # technopat halihazırda kelime temelli kategorileme yapıyor
    # buna ulaşmak için her bir haberin yani item',in
    # içinde gezip o kategorileri bir arrey'e atıyorum
    # soup.findall dersek sayfadaki tüm kategorileri çekiyor, sonradan farkettiğim bir hata :)
    """
    category_elements = item.find_all("category")
    category_names = []
    for category_element in category_elements:
        category_names.append(category_element.text)

    """
    # for category_item in categories:
    #     category = category_item.category.text
    # categories = item.category.text

    # content = item.description.find('p').text
    # technopat haberin açıklamasını descriptionun içindeki ilk p tagında yazıyor, && yerine and ! yerine not
    # Recursive = False returns only the children of the element of the tag you are trying to find.
    # https://stackoverflow.com/a/69891061
    # content = item.description.find(lambda tag: tag.name == 'p' and not tag.find('img', recursive=False)).text

    # if item.find("description") is not None and item.find("description").text.strip():
    #     first_p_tag = item.find("p")
    #     content = first_p_tag.text if first_p_tag is not None else ""
    # else:
    #     content = ""
    """

    description = item.description.text
    """
    # yukarıdaki bs de işlemi xml olarak yapıyordum ama burada açıklamanın içi
    # html olduğu için yeni bs tipine geçtim yani html okuma
    # fikrin kaynağı https://stackoverflow.com/questions/56007924/i-want-to-get-the-image-link-inside-a-rss-feed-description-tag
    # eğer first p varsa onun textini yani içindeki metini yeni bir değer ata
    # eğer yoksa değeri boş olarak göster
    """
    desc_soup = BeautifulSoup(description, "html.parser")
    first_p = desc_soup.find(
        "p"
    )  # yukarıda da dediğim gibi haber açıklaması ilk p de olduğu için sadece find ile buldum

    if first_p:
        first_p_content = first_p.text
    else:
        first_p_content = ""

    articleImage = item.thumbnail["url"]

    # load all data
    test_db3 = client.test3
    collection3 = test_db3.test3
    data = {
    "title": title,
    "link": link,
    "creator": creator,
    "publishDate": publishDate,
    "categories": category_names,
    "description": first_p_content
    }
    collection3.insert_one(data)


    # print(f"Title:{title}\n\nLink:{link}\n\nCreator:{creator}\n\nPublish Date:{publishDate}\n\nCategories:{category_names}\n\nDescription:{first_p_content}\n\nImage:{articleImage}\n\n----------------------------------\n\n")


"""
What I have written so far is for scraping the data from RSS and getting the stuff i need while cleaning the data, after this point the is to convert my data to json for uploading it to mongodb
"""

### TUTORIAL START ###
"""
dbs = client.list_database_names()
# print(dbs)
test_db = client.test
collections = test_db.list_collection_names()
print(collections)

def insert_test_doc():
    collection = test_db.test
    data = {
        "title": title,
        "link": link,
        "creator": creator,
        "publishDate": publishDate,
        "categories": category_names,
        "description": first_p_content,
    }
    inserted_id = collection.insert_one(data).inserted_id
    print(inserted_id)

# insert_test_doc()
"""

"""
production = client.production
person_collection = production.person_collection

def create_documents():
    first_names = ["tim", "sarah", "jenn"]
    last_names = ["ruscica", "smith", "bart"]
    ages = [21, 40, 23]

    docs = []

    for first_name, last_name, age in zip(first_names, last_names, ages):
        doc = {"first_name": first_name, "last_name": last_name, "age": age}
        docs.append(doc)

    person_collection.insert_many(docs)

create_documents()
"""

### TUTORIAL END ###

"""
test_db2 = client.test2
collection2 = test_db2.test2
# inserted_id = collection.insert_one(data).inserted_id

# title, link, creator, publishDate, category names(array), description(first_p), image link
data = {
    "title": title,
    "link": link,
    "creator": creator,
    "publishDate": publishDate,
    "categories": category_names,
    "description": first_p_content
}
# convert data to json for insert
# json_data = json.dumps(data)

# collection2.insert_many(json.loads(json_data))
collection2.insert_one(data)
"""
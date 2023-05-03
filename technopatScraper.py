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

from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
import json

### START OF MONGO SETUP ###
# https://stackoverflow.com/questions/52930341/pymongo-dnspython-module-must-be-installed-to-use-mongodbsrv-uris
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://yusufekerdiker:{password}@mycluster.fma9e4h.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

from bs4 import BeautifulSoup
import requests

import time

rss_feed_links = {
    "Technopat" : "https://www.technopat.net/feed/",
    "DonanimArsivi" : "https://donanimarsivi.com/feed/"
}

database = client.rssFeeds

# title of the news can change but guid cannot so 
# for checking the rss for new item we can use guid link
existing_guids = set()


"""
for feed_name, feed_url in rss_feed_links.items():
    url = requests.get(feed_url)
    soup = BeautifulSoup(url.content, "xml")
    items = soup.find_all("item")

    # aşağıdaki gibi title = title link link eşlemesini yap ama şu an var mı yok mu kontrolu yapmıyorum o taglar ve tagların içini
    for item in items:
        database[feed_name].insert_one(
            {
                "title": title,
                "link": link,
                "creator": creator,
                "publishDate": publishDate,
                "categories": category_names,
                "description": first_p_content,
            }
        )
"""


while True:

    website = "https://www.technopat.net/feed"
    url = requests.get(website)
    soup = BeautifulSoup(url.content, "xml")

    # find all news which is inside item tag
    items = soup.find_all("item")

    for item in items:
        guid = item.guid.text

        # loop in the news and get details of it
        title = item.title.text or ""
        link = item.link.text or ""
        creator = item.creator.text or ""
        publishDate = item.pubDate.text or ""
        description = item.description.text or ""

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
        """
        # yukarıdaki bs de işlemi xml olarak yapıyordum ama burada açıklamanın içi
        # html olduğu için yeni bs tipine geçtim yani html okuma
        # fikrin kaynağı https://stackoverflow.com/questions/56007924/i-want-to-get-the-image-link-inside-a-rss-feed-description-tag
        # eğer first p varsa onun textini yani içindeki metini yeni bir değer ata
        # eğer yoksa değeri boş olarak göster
        """
        desc_soup = BeautifulSoup(description, "html.parser")
        first_p = desc_soup.find("p")  # yukarıda da dediğim gibi haber açıklaması ilk p de olduğu için sadece find ile buldum

        if first_p:
            first_p_content = first_p.text
        else:
            first_p_content = ""

        articleImage = item.thumbnail["url"]

        # load all data
        # title, link, creator, publishDate, category names(array), description(first_p), image link
        collection4 = database.test4
        # inserts new news if the guid is not in the list
        if guid not in existing_guids:
            existing_guids.add(guid)
            data = {
                "title": title,
                "link": link,
                "creator": creator,
                "publishDate": publishDate,
                "categories": category_names,
                "description": first_p_content,
            }
            collection4.insert_one(data)
            # convert data to json for insert
            # json_data = json.dumps(data)
            # no need to convert the data to json for mongodb it automatically recognizes the data types

            # collection2.insert_many(json.loads(json_data))

            # print(f"Title:{title}\n\nLink:{link}\n\nCreator:{creator}\n\nPublish Date:{publishDate}\n\nCategories:{category_names}\n\nDescription:{first_p_content}\n\nImage:{articleImage}\n\n----------------------------------\n\n")
        
    time.sleep(180)

    """
    What I have written so far is for scraping the data from RSS and getting the stuff i need while cleaning the data, after this point the is to convert my data to json for uploading it to mongodb
    """
    """
    ### TUTORIAL
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

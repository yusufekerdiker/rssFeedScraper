from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time

from flask import Flask, jsonify

### MONGO SETUP ###
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://yusufekerdiker:{password}@mycluster.fma9e4h.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

rss_feed_links = {
    "Technopat": "https://www.technopat.net/feed/",
    "ShiftdeleteNet": "https://shiftdelete.net/feed",
}

# title of the news can change but guid cannot so
# for checking the rss for new item we can use guid link
existing_guids = set()


def insertRssFeeds(db, rss_links):
    for feed_name, feed_url in rss_feed_links.items():
        url = requests.get(feed_url)
        soup = BeautifulSoup(url.content, "xml")

        items = soup.find_all("item")

        for item in items:
            guid = item.guid.text

            title = item.title.text or ""
            link = item.link.text or ""
            creator = item.creator.text or ""
            publishDate = item.pubDate.text or ""

            category_elements = item.find_all("category")
            category_names = []
            for category_element in category_elements:
                category_names.append(category_element.text)

            description = getAndCleanDescription(feed_url, item.description.text)

            articleImage = getArticleImage(feed_url, item)

            # load all data
            # inserts new news if the guid is not in the list
            if guid not in existing_guids:
                existing_guids.add(guid)
                database[feed_name].insert_one(
                    {
                        "title": title,
                        "link": link,
                        "creator": creator,
                        "publishDate": publishDate,
                        "categories": category_names,
                        "description": description,
                        "articleImg": articleImage,
                    }
                )


def getAndCleanDescription(rss_url, desc):
    desc_soup = BeautifulSoup(desc, "html.parser")
    if rss_url == "https://www.technopat.net/feed/":
        first_p = desc_soup.find("p")
        if first_p:
            first_p_content = first_p.text
        else:
            first_p_content = ""
        return first_p_content

    elif rss_url == "https://shiftdelete.net/feed":
        last_p = desc_soup.find_all("p")[-1]
        a_tag = last_p.find("a")
        a_tag_content = a_tag.text if a_tag else ""
        return a_tag_content
"""         
        a_tag = last_p.find("a")
        if a_tag:
            a_tag_content = a_tag.text
        else:
            a_tag_content = ""
        return a_tag_content 
"""


def getArticleImage(rss_url, item):
    if rss_url == "https://www.technopat.net/feed/":
        articleImage = item.thumbnail["url"]
    elif rss_url == "https://shiftdelete.net/feed":
        desc_soup = BeautifulSoup(item.description.text, "html.parser")
        articleImage = desc_soup.find("img")["src"]
    return articleImage


# if __name__ == "__main__":
#     database = client.rssFeeds

#     app = Flask(__name__)
#     @app.route('/api/data')
#     def get_data():
#         collection = database['Technopat']
#         data = list(collection.find({}, {'_id': 0}))
#         return jsonify(data)
#     app.run()

#     while True:
#         insertRssFeeds(database, rss_feed_links)
#         time.sleep(60*3)

if __name__ == "__main__":
    database = client.rssFeeds

    insertRssFeeds(database, rss_feed_links)

    app = Flask(__name__)

    @app.route("/api/data")
    def get_data():
        data = {}
        for feed_name, feed_url in rss_feed_links.items():
            collection = database[feed_name]
            data[feed_name] = list(collection.find({}, {"_id": 0}))
        return jsonify(data)

    app.run()

    while True:
        insertRssFeeds(database, rss_feed_links)
        time.sleep(60 * 3)

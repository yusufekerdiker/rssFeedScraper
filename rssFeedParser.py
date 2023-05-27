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

rss_feed_links = {
    "Technopat": "https://www.technopat.net/feed/",
    "ShiftdeleteNet": "https://shiftdelete.net/feed"
}

existing_guids = set()

def parse_and_insert_rss_feeds(db, rss_links):
    for feed_name, feed_url in rss_links.items():
        response = requests.get(feed_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")
            for item in items:
                guid = item.guid.text
                if guid not in existing_guids:
                    existing_guids.add(guid)
                    insert_news(db, feed_name, item)

def insert_news(db, collection_name, item):
    guid = item.guid.text
    if guid not in existing_guids:
        existing_guids.add(guid)
    db[collection_name].insert_one({
        "title": item.title.text.strip() or "",
        "link": item.link.text.strip() or "",
        "creator": item.creator.text.strip() or "",
        "publishDate": item.pubDate.text.strip() or "",
        "categories": get_or_create_category(item),
        "description": get_clean_description(item),
        "articleImg": get_article_image(item),
    })

def get_or_create_category(item):
    rss_url = item.find_parent("rss").find("link").text
    if rss_url == "https://www.technopat.net/feed/":
        category_elements = item.find_all("category")
        category_names = []
        for category_element in category_elements:
            category_names.append(category_element.text)
        return category_names

def get_clean_description(item):
    desc_soup = BeautifulSoup(item.description.text, "html.parser")
    rss_url = item.find_parent("rss").find("link").text
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
        if a_tag:
            a_tag_content = a_tag.text
        else:
            a_tag_content = ""
        return a_tag_content 

def get_article_image(item):
    rss_url = item.find_parent("rss").find("link").text
    if rss_url == "https://www.technopat.net/feed/":
        articleImage = item.thumbnail["url"]
        return articleImage
    elif rss_url == "https://shiftdelete.net/feed":
        desc_soup = BeautifulSoup(item.description.text, "html.parser")
        articleImage = desc_soup.find("img")["src"]
        return articleImage
    
def connect_to_mongodb():
    client = MongoClient(connection_string)
    return client.rssFeeds

def close_mongodb_connection(client):
    client.close()

def create_app():
    app = Flask(__name__)

    @app.route('/api/data')
    def get_data():
        data = {}
        for feed_name, _ in rss_feed_links.items():
            collection = database[feed_name]
            data[feed_name] = list(collection.find({}, {'_id': 0}))
        return jsonify(data)

    return app    

if __name__ == "__main__":

    """
    client = MongoClient(connection_string)
    database = client.rssFeeds
    """
    database = connect_to_mongodb()

    parse_and_insert_rss_feeds(database, rss_feed_links)

    app = create_app()
    app.run()

    """
    app = Flask(__name__)
    @app.route('/api/data')
    def get_data():
        data = {}
        for feed_name, _ in rss_feed_links.items():
            collection = database[feed_name]
            data[feed_name] = list(collection.find({}, {'_id': 0}))
        return jsonify(data)
    app.run()
    """
    
    while True:
        time.sleep(60 * 3)
        parse_and_insert_rss_feeds(database, rss_feed_links)

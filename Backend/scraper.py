from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time

from rake_nltk import Rake

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://yusufekerdiker:{password}@mycluster.fma9e4h.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
database = client.rssFeeds

rss_feed_links = {
    "CNET": "https://www.cnet.com/rss/news/",
    "Wired": "https://www.wired.com/feed/rss",
}

# existing_guids = set()

def insertRssFeeds(db, rss_links):
    for feed_name, feed_url in rss_links.items():
        url = requests.get(feed_url)
        soup = BeautifulSoup(url.content, "xml")

        items = soup.find_all("item")

        for item in items:
            guid = item.guid.text

            title = item.title.text if item.title is not None else ""
            link = item.link.text if item.link is not None else ""
            creator = item.creator.text if item.creator is not None else ""
            publishDate = item.pubDate.text if item.pubDate is not None else ""

            categories = getArticleCategory(feed_url, item)

            description = getArticleDescription(feed_url, item)

            articleImage = getArticleImage(feed_url, item)

            # if guid not in existing_guids:
            # existing_guids.add(guid)
            if (
                db[feed_name].find_one({"guid": guid}) is None
            ):  # Check if the document already exists IN DATABASE
                db[feed_name].insert_one(
                    {
                        "guid": guid,
                        "title": title,
                        "link": link,
                        "creator": creator,
                        "publishDate": publishDate,
                        "categories": categories,
                        "description": description,
                        "articleImg": articleImage,
                    }
                )


def getArticleDescription(rss_url, item):
    description = item.find("description")
    if description and description.text:
        if (
            rss_url == "https://www.cnet.com/rss/news/"
            or rss_url == "https://www.wired.com/feed/rss"
        ):
            return description.text
    else:
        return ""

def getArticleImage(rss_url, item):
    if rss_url == "https://www.cnet.com/rss/news/":
        articleImage = item.thumbnail["url"]
        image = articleImage.split("?")[0]
        resize_index = image.find("resize/")
        if resize_index != -1:
            modified_url = image[:resize_index] + image[resize_index + len("resize/") :]
        else:
            modified_url = image
        return modified_url
    elif rss_url == "https://www.wired.com/feed/rss":
        articleImage = item.thumbnail["url"]
        return articleImage

def getArticleCategory(rss_url, item):
    category_elements = item.find_all("category")
    category_names = []
    for category_element in category_elements:
        category_names.append(category_element.text)

    keywords_element = item.keywords
    keywords_list = []
    if keywords_element:
        keywords = keywords_element.text
        keywords_categories = keywords.split(", ")
        for category in keywords_categories:
            keywords_list.append(category)

    desc = getArticleDescription(rss_url, item)

    desc_soup = BeautifulSoup(desc, "html.parser")
    description_text = desc_soup.get_text()

    r = Rake()
    r.extract_keywords_from_text(description_text)

    ranked_phrases = r.get_ranked_phrases()
    # keywords = r.get_ranked_phrases()[:10]
    # with this code rake only return top 10 popular multi-word or single word keywords which is sometimes not enough or not working properly so i modified to code for getting both type of keywords separately

    single_words = []
    multi_words = []
    for phrase in ranked_phrases:
        if " " in phrase:
            multi_words.append(phrase)
        else:
            single_words.append(phrase)

        if len(single_words) >= 5 and len(multi_words) >= 5:
            break

    categories = category_names + single_words[:5] + multi_words[:5] + keywords_list

    return categories

if __name__ == "__main__":
    while True:
        insertRssFeeds(database, rss_feed_links)
        time.sleep(60 * 3)

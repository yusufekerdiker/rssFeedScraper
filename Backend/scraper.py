from dotenv import (
    load_dotenv,
    find_dotenv,
)  # this library is used to load environment variables from a .env file, where sensitive information like database passwords are usually stored
import os  # is a standard Python library for interacting with the operating system. its being used here to get environment variables with os.environ.get
from pymongo import (
    MongoClient,
)  # is a py library for interacting with mongodb, a NoSql database and pymongo handles interactions with the mongodb server
from bs4 import (
    BeautifulSoup,
)  # is a python library for parsing html and xml documents. It's used for web scraping
from rake_nltk import (
    Rake,
)  # is a python lib. that uses the NLTK (Natural Language Toolkit) library in combination with the RAKE (Rapid Automatic Keyword Extraction) algorithm to extract keywords from text. Its used here to extract keywords from the description of each news article

# RAKE (Rapid Automatic Keyword Extraction) is a quick and efficient way to pull out the main points from a block of text. It does this by breaking the text down into individual words (called tokenization), then groups these words into potential key phrases. These phrases are scored based on how often each word appears in the text and how many other words it appears with. The phrases with the highest scores are considered the most important. In this Python code, RAKE is used to automatically figure out the main topics of each news item in the RSS feeds.

import aiohttp
import asyncio

# load environment variables from .enb file which includes our sensitive info like mongodb username and passwords
load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")
username = os.environ.get("MONGODB_USR")

# mongo connection string, it is like address/url of our database
connection_string = f"mongodb+srv://{username}:{password}@mycluster.fma9e4h.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(connection_string)
# get or create mongo database from our client
database = client.rssFeeds

# defined a dict for both containing our rss feed links and names which we are going to use for creating mongo collection

# A collection is a grouping of MongoDB documents. Documents within a collection can have different fields. A collection is the equivalent of a table in a relational database system. A collection exists within a single database.
rss_feed_links = {
    "CNET": "https://www.cnet.com/rss/news/",
    "Wired": "https://www.wired.com/feed/rss",
}


# function to fetch content from feed URLs, this coroutine fetches the content of an RSS feed
async def fetch(feed_url, session):
    # creating get request for the feed link
    async with session.get(feed_url) as resp:
        # wait for the request to complete and return the response
        return await resp.text()


# our main function for getting data from rss feeds, processing it and inserting into mongodb
# coroutine for processes a single feed
async def process_feed(db, feed_name, feed_url):
    # creating a new aiohttp session
    async with aiohttp.ClientSession() as session:
        # fetch the content from the feed link
        content = await fetch(feed_url, session)
        # parse the raw data into a format we can work with which is XML in this case (we are scraping website's rss feed which is in xml format)
        soup = BeautifulSoup(content, "xml")

        # extract each individual new from feed which is under item tag
        items = soup.find_all("item")

        # loop thru every news
        for item in items:
            # extract the unique identifier GUID, title, link, creator, and publish date of the item
            guid = item.guid.text

            title = item.title.text if item.title is not None else ""
            link = item.link.text if item.link is not None else ""
            creator = item.creator.text if item.creator is not None else ""
            publishDate = item.pubDate.text if item.pubDate is not None else ""

            # get additional data from the news item using functions
            categories = getArticleCategory(feed_url, item)

            description = getArticleDescription(feed_url, item)

            articleImage = getArticleImage(feed_url, item)

            # check if we've already stored this item in the database. we don't want to store duplicates so we skip any items we've already scraped
            if db[feed_name].find_one({"guid": guid}) is None:
                # insert the news item into the database one by one
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


# the function getArticleDescription extracts the article's description based on the link of rss feed and the item/news
# different treatments are applied depending on the feed source.
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


# the function getArticleImage extracts the image's url
# different treatments are applied depending on the feed source
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


# the function getArticleCategory gets the category names from the "category" elements and the "keywords" elements
# it also extracts keywords from the description using the RAKE algorithm.
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

    # ignore category which includes only the ’ (u+2019) character
    categories = [c for c in categories if c != "’"]

    # split categories by the / character (for wired)
    split_categories = []
    for category in categories:
        split_categories.extend(category.split("/"))

    # remove — and ... from all categories
    clean_categories = [
        category.replace("—", "").replace("...", "").replace("--", "")
        for category in split_categories
    ]

    # Remove ’ from categories that are ending with that
    clean_categories = [category.rstrip("’") for category in clean_categories]

    # Replace double spaces with single spaces
    clean_categories = [category.replace("  ", " ") for category in clean_categories]

    # Remove extra spaces
    clean_categories = [category.strip() for category in clean_categories]

    # convert to set and then back to a list to remove duplicates
    clean_categories = list(set(clean_categories))

    return clean_categories


# function to insert feeds into the database
async def insertRssFeeds(db, rss_links):
    # create list of tasks for the event loop
    tasks = []
    # created a process_feed task for each feed link
    for feed_name, feed_url in rss_links.items():
        tasks.append(process_feed(db, feed_name, feed_url))
    # used asyncio.gather to run all the tasks concurrently
    await asyncio.gather(*tasks)


# main coroutine
async def main(db, rss_links):
    while True:
        # handle all feeds
        await insertRssFeeds(db, rss_links)
        await asyncio.sleep(60 * 10)


if __name__ == "__main__":
    asyncio.run(main(database, rss_feed_links))

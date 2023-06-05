from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

nltk.download('punkt')
nltk.download('stopwords')

from sklearn.feature_extraction.text import TfidfVectorizer

from rake_nltk import Rake

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://yusufekerdiker:{password}@mycluster.fma9e4h.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
database = client.rssFeeds4

rss_feed_links = {
    "CNET": "https://www.cnet.com/rss/news/",
    "Wired": "https://www.wired.com/feed/rss",
}

existing_guids = set()

def insertRssFeeds(db, rss_links):
    for feed_name, feed_url in rss_links.items():
        url = requests.get(feed_url)
        soup = BeautifulSoup(url.content, "xml")

        items = soup.find_all("item")

        for item in items:
            guid = item.guid.text

            title = item.title.text or ""
            link = item.link.text or ""
            creator = item.creator.text or ""
            publishDate = item.pubDate.text or ""

            categories = getArticleCategory(feed_url, item)

            description = getArticleDescription(feed_url, item)

            articleImage = getArticleImage(feed_url, item)

            if guid not in existing_guids:
                existing_guids.add(guid)
                db[feed_name].insert_one(
                    {
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
        if rss_url == "https://www.cnet.com/rss/news/" or rss_url == "https://www.wired.com/feed/rss":
            return description.text
    else:
        return ""
"""     
    if rss_url == "https://www.cnet.com/rss/news/":
        return item.description.text
    elif rss_url == "https://www.wired.com/feed/rss":
        return item.description.text 
"""
""" 
        elif rss_url == "https://techspices.com/feed/":
        desc_soup = BeautifulSoup(item.description.text, "html.parser")
        first_p = desc_soup.find("p")
        if first_p:
            first_p_content = first_p.text
        else:
            first_p_content = ""
        return first_p_content
"""
"""     
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


def getArticleImage(rss_url, item):
    if rss_url == "https://www.cnet.com/rss/news/":
        articleImage = item.thumbnail["url"]
        image = articleImage.split("?")[0]
        return image
    elif rss_url == "https://www.wired.com/feed/rss":
        articleImage = item.thumbnail["url"]
        return articleImage

def getArticleCategory(rss_url, item):
    category_elements = item.find_all("category")
    category_names = []
    for category_element in category_elements:
        category_names.append(category_element.text)
 
    keywords_element = item.keywords
    # keywords_list = keywords_element.text.split(", ") if keywords_element and keywords_element.text else []
    
    keywords_list = []
    if keywords_element:
        keywords = keywords_element.text
        keywords_categories = keywords.split(", ")
        for category in keywords_categories:
            keywords_list.append(category)

    desc = getArticleDescription(rss_url, item)

    desc_soup = BeautifulSoup(desc, "html.parser")
    description_text = desc_soup.get_text()

    # Use RAKE to extract keywords
    r = Rake()
    r.extract_keywords_from_text(description_text)

    # Get top 10 single-word and multi-word keywords
    ranked_phrases = r.get_ranked_phrases()
    # keywords = r.get_ranked_phrases()[:10] # with this code rake only return top 10 popular multi-word or single word keywords which is sometimes not enough or not working properly so i modified to code for getting both type of keywords separately

    single_words = []
    multi_words = []

    for phrase in ranked_phrases:
        if ' ' in phrase:
            multi_words.append(phrase)
        else:
            single_words.append(phrase)

        if len(single_words) >= 5 and len(multi_words) >= 5:
            break

    # Add keywords to existing categories
    categories = category_names + single_words[:5] + multi_words[:5] + keywords_list

    return categories

"""
#Extraction with nltk
    desc_soup = BeautifulSoup(item.description.text, "html.parser")
    description_text = desc_soup.get_text()

    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(description_text)

    filtered_sentence = [w for w in word_tokens if not w in stop_words]

    fdist = FreqDist(filtered_sentence)
    most_common = fdist.most_common(5)  # adjust the number here to get more or less keywords

    keywords = [word[0] for word in most_common]

    # Add keywords to existing categories
    categories = category_names + keywords

    return categories
"""


if __name__ == "__main__":
    while True:
        insertRssFeeds(database, rss_feed_links)
        time.sleep(60 * 3)

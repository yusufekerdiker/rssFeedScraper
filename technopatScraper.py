from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
import time

### START OF MONGO SETUP ###
# https://stackoverflow.com/questions/52930341/pymongo-dnspython-module-must-be-installed-to-use-mongodbsrv-uris
load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://yusufekerdiker:{password}@mycluster.fma9e4h.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

rss_feed_links = {
    "Technopat" : "https://www.technopat.net/feed/",
    "ShiftdeleteNet" : "https://shiftdelete.net/feed"
}

# title of the news can change but guid cannot so 
# for checking the rss for new item we can use guid link
existing_guids = set()

def insertRssFeeds(db, rss_links):
    
    for feed_name, feed_url in rss_feed_links.items():

        url = requests.get(feed_url)
        soup = BeautifulSoup(url.content, "xml")
        
        items = soup.find_all("item") # find all news which is inside item tag

        for item in items:
            guid = item.guid.text

            # loop in the news and get details of it
            title = item.title.text or ""
            link = item.link.text or ""
            creator = item.creator.text or ""
            publishDate = item.pubDate.text or ""

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
            # content = item.description.find('p').text
            # technopat haberin açıklamasını descriptionun içindeki ilk p tagında yazıyor, && yerine and ! yerine not
            # Recursive = False returns only the children of the element of the tag you are trying to find.
            # https://stackoverflow.com/a/69891061
            """
            """
            # yukarıdaki bs de işlemi xml olarak yapıyordum ama burada açıklamanın içi
            # html olduğu için yeni bs tipine geçtim yani html okuma
            # fikrin kaynağı https://stackoverflow.com/questions/56007924/i-want-to-get-the-image-link-inside-a-rss-feed-description-tag
            # eğer first p varsa onun textini yani içindeki metini yeni bir değer ata
            # eğer yoksa değeri boş olarak göster
            """
            
            description = getAndCleanDescription(feed_url, item.description.text)
            """         
            description = item.description.text or ""
            desc_soup = BeautifulSoup(description, "html.parser")
            first_p = desc_soup.find("p")  # yukarıda da dediğim gibi haber açıklaması ilk p de olduğu için sadece find ile buldum
            if first_p:
                first_p_content = first_p.text
            else:
                first_p_content = ""
            """

            # articleImage = item.thumbnail["url"]
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
    if (rss_url == "https://www.technopat.net/feed/"):
        first_p = desc_soup.find("p")  # yukarıda da dediğim gibi haber açıklaması ilk p de olduğu için sadece find ilebuldum
        if first_p:
            first_p_content = first_p.text
        else:
            first_p_content = ""
        return first_p_content
    
    elif (rss_url == "https://shiftdelete.net/feed"):
        last_p = desc_soup.find_all("p")[-1]
        a_tag = last_p.find("a")
        if a_tag:
            a_tag_content = a_tag.text
        else:
            a_tag_content = ""
        return a_tag_content
        """     
        a_tag_remove = desc_soup.find_all("p")[-1].find("a")
        a_tag_remove.replace_with("")
        last_p = desc_soup.find_all("p")[-1]
        if last_p:
            last_p_content = last_p.text
        else:
            last_p_content = ""
        return last_p_content
        """

def getArticleImage(rss_url, item):
    if (rss_url == "https://www.technopat.net/feed/"):
        articleImage = item.thumbnail["url"]
    elif (rss_url == "https://shiftdelete.net/feed"):
        desc_soup = BeautifulSoup(item.description.text, "html.parser")
        articleImage = desc_soup.find("img")["src"]
    return articleImage

"""         
if "media_thumbnail" in str(item):
    return item.find("media_thumbnail")["url"]
elif "media_content" in str(item):
    return item.find("media_content")["url"]
elif "enclosure" in str(item):
    return item.enclosure["url"]
else:
    return ""
"""

if __name__ == "__main__":
    database = client.rssFeeds
    while True:
        insertRssFeeds(database, rss_feed_links)
        time.sleep(60*3)

    """
    What I have written so far is for scraping the data from RSS and getting the stuff i need while cleaning the data, after this point the is to convert my data to json for uploading it to mongodb
    """

from flask import Flask, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
connection_string = f"mongodb+srv://yusufekerdiker:{password}@mycluster.fma9e4h.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

rss_feed_links = {
    "CNET": "https://www.cnet.com/rss/news/",
    "TechSpices": "https://techspices.com/feed/",
}

database = client.rssFeeds

app = Flask(__name__)

@app.route("/api/data")
def get_data():
    data = {}
    for feed_name, feed_url in rss_feed_links.items():
        collection = database[feed_name]
        data[feed_name] = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == "__main__":
    app.run()

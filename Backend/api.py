from flask import Flask, jsonify
from pymongo import MongoClient, errors
from dotenv import load_dotenv, find_dotenv
import os
from flask_cors import CORS

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PWD")
username = os.environ.get("MONGODB_USR")

try:
    connection_string = f"mongodb+srv://{username}:{password}@mycluster.fma9e4h.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_string)
except errors.PyMongoError as e:
    print(f"Failed to connect to MongoDB: {e}")

rss_feed_links = {
    "CNET": "https://www.cnet.com/rss/news/",
    "Wired": "https://www.wired.com/feed/rss",
}

database = client.rssFeeds

app = Flask(__name__)
CORS(app)

@app.route("/api/data")
def get_data():
    data = {}
    try:
        for feed_name, feed_url in rss_feed_links.items():
            collection = database[feed_name]
            try:
                data[feed_name] = list(collection.find({}, {"_id": 0}))
            except errors.PyMongoError as e:
                return jsonify({"error": f"Failed to find data in MONGODB: {e}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify(data)

if __name__ == "__main__":
    app.run()

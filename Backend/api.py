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

rss_feed_names = {
    "cnet": "CNET",
    "wired": "Wired"
}

database = client.rssFeeds

app = Flask(__name__)
CORS(app)

@app.route("/", defaults={'path': ''})
@app.route("/<path:path>")
def get_data(path):
    data = {}
    path = path.lower() #convert path to lower case
    try:
        if path in rss_feed_names:
            #if path matches a feed name, retrieve data for that specific feed
            data[rss_feed_names[path]] = list(database[rss_feed_names[path]].find({}, {"_id": 0}))
        elif path == '':
            #if path is not provided or empty return all the data
            for feed_name, collection_name in rss_feed_names.items():
                data[collection_name] = list(database[collection_name].find({}, {"_id": 0}))
        else:
            #if path doesnt match any feed name and isnt empty return an error
            return jsonify({"error": "Invalid path"}), 404
    
    #handle errors when retrieving data from mongodb
    except errors.PyMongoError as e:
        return jsonify({"error": f"Failed to find data in MongoDB: {e}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    #if data retrieval is successful, return the data    
    return jsonify(data)

if __name__ == "__main__":
    app.run()

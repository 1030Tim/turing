from pymongo import MongoClient
import os


client = None
db = None


def init_db():

    global client
    global db


    mongo_url = os.environ.get(
        "MONGO_URI"
    )


    if mongo_url:

        client = MongoClient(
            mongo_url
        )

    else:

        client = MongoClient(
            "mongodb://localhost:27017/"
        )


    db = client["JunOS"]


    print(
        "MongoDB connected"
    )



def get_db():

    global db


    if db is None:

        init_db()


    return db["daily_records"]
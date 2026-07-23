from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")


client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000
)


db = client["JunOS"]


records_collection = db["records"]



def init_db():

    try:

        client.admin.command("ping")

        print("MongoDB connected")

    except Exception as e:

        print("MongoDB connection error:")
        print(e)




def get_db():

    return records_collection
from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")


client = None



def get_db():

    global client


    if client is None:

        client = MongoClient(
            MONGO_URI
        )


    db = client["junos"]


    return db["records"]




def init_db():

    print("MongoDB connected")
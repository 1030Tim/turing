from pymongo import MongoClient
import os
from dotenv import load_dotenv


load_dotenv()


MONGO_URI = os.getenv("MONGO_URI")


client = MongoClient(MONGO_URI)


db = client["JunOS"]


records_collection = db["records"]



def get_db():

    return records_collection



def init_db():

    print("MongoDB connected")
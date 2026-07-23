from pymongo import MongoClient
from dotenv import load_dotenv
import os


# 讀取 .env
load_dotenv()


# 連線 MongoDB Atlas
client = MongoClient(
    os.getenv("MONGO_URI")
)


# 建立 database
db = client["JunOS"]


# 建立 collection
records = db["records"]



def init_db():

    # MongoDB 不需要 CREATE TABLE
    # 第一次 insert 時會自動建立 collection

    return True



def get_db():

    return records
from pymongo import MongoClient
from dotenv import load_dotenv
import os



# =========================
# Load Environment Variable
# =========================

load_dotenv()



MONGO_URI = os.getenv(
    "MONGO_URI"
)



if not MONGO_URI:

    raise ValueError(
        "MONGO_URI 未設定，請確認 .env 或 Render Environment Variables"
    )





# =========================
# MongoDB Connection
# =========================


client = MongoClient(
    MONGO_URI,

    serverSelectionTimeoutMS=5000
)





# =========================
# Database
# =========================


db = client["JunOS"]





# =========================
# Collection
# =========================


records_collection = db["records"]









# =========================
# Initialize Database
# =========================


def init_db():

    try:

        client.admin.command(
            "ping"
        )


        print(
            "MongoDB connected"
        )


    except Exception as e:


        print(
            "MongoDB connection failed:"
        )

        print(e)









# =========================
# Get Collection
# =========================


def get_db():

    return records_collection
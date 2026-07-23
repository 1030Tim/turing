from database import get_db


records = get_db()


data = records.find()


for record in data:
    print(record)
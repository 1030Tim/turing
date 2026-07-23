from database import get_db


collection = get_db()


result = collection.delete_many({})


print(
    "Deleted:",
    result.deleted_count
)
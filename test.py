from database import get_db
import csv


records = get_db()

data = list(records.find())


keys = [
    key 
    for key in data[0].keys()
    if key != "_id"
]


with open(
    "junos_records.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=keys
    )

    writer.writeheader()


    for record in data:
        record.pop("_id", None)
        writer.writerow(record)


print("export done")
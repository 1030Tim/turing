from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_file
)

from database import init_db, get_db

from datetime import datetime

import csv



app = Flask(__name__)


init_db()



# ======================
# 首頁
# ======================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )



# ======================
# pages
# ======================

@app.route("/pages/<page>")
def pages(page):

    try:

        return render_template(
            f"pages/{page}.html"
        )

    except:

        return "Page Not Found",404




# ======================
# Dashboard
# ======================

@app.route("/records/dashboard")
def dashboard():

    records_collection = get_db()


    records = list(
        records_collection.find()
        .sort(
            "_id",
            -1
        )
    )


    return render_template(
        "records/dashboard.html",
        records=records
    )





# ======================
# 新增紀錄
# ======================

@app.route(
    "/records/add",
    methods=["POST"]
)

def add_record():

    collection = get_db()



    record = {

        "date":
        datetime.now()
        .strftime("%Y-%m-%d"),


        "sleep":
        float(
            request.form.get(
                "sleep",
                0
            )
        ),


        "energy":
        int(
            request.form.get(
                "energy",
                0
            )
        ),


        "focus":
        int(
            request.form.get(
                "focus",
                0
            )
        ),


        "stress":
        int(
            request.form.get(
                "stress",
                0
            )
        ),


        "thoughts":
        request.form.get(
            "thoughts",
            ""
        )

    }



    collection.insert_one(
        record
    )



    return redirect(
        "/records/dashboard"
    )






# ======================
# CSV Export
# ======================

@app.route(
    "/records/export"
)

def export_records():


    collection = get_db()



    records = collection.find()



    filename="junos_records.csv"



    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as f:


        writer = csv.writer(f)


        writer.writerow(
            [
                "日期",
                "睡眠",
                "能量",
                "專注",
                "壓力",
                "內耗"
            ]
        )



        for r in records:


            writer.writerow(
                [
                    r.get("date"),
                    r.get("sleep"),
                    r.get("energy"),
                    r.get("focus"),
                    r.get("stress"),
                    r.get("thoughts")
                ]
            )



    return send_file(
        filename,
        as_attachment=True
    )






if __name__=="__main__":


    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
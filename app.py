from flask import (
    Flask,
    render_template,
    request,
    redirect,
    send_file
)

from database import (
    init_db,
    get_db
)

from datetime import datetime

import csv



app = Flask(__name__)


init_db()



# =====================
# 首頁
# =====================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )



# =====================
# 靜態 pages
# =====================

@app.route("/pages/<page>")
def pages(page):

    try:

        return render_template(
            f"pages/{page}.html"
        )

    except:

        return "Page Not Found",404





# =====================
# Dashboard
# =====================

@app.route("/records/dashboard")
def dashboard():


    collection = get_db()


    records = list(
        collection.find()
        .sort(
            "created_at",
            -1
        )
    )


    return render_template(
        "records/dashboard.html",
        records=records
    )





# =====================
# 新增紀錄
# =====================


@app.route(
    "/records/add",
    methods=["POST"]
)

def add_record():


    collection = get_db()



    def get_int(name):

        value = request.form.get(name)

        if value == "" or value is None:
            return None

        return int(value)



    def get_float(name):

        value = request.form.get(name)

        if value == "" or value is None:
            return None

        return float(value)



    record = {


        "date":

        datetime.now()
        .strftime("%Y-%m-%d"),



        "created_at":

        datetime.now(),



        "sleep":

        get_float("sleep"),



        "energy":

        get_int("energy"),



        "focus":

        get_int("focus"),



        "stress":

        get_int("stress"),



        "emotion":

        request.form.get(
            "emotion"
        ),



        "brain":

        {

            "flow":

            request.form.get(
                "flow"
            ),


            "thoughts":

            request.form.get(
                "thoughts"
            )

        },



        "life":

        {

            "training":

            request.form.get(
                "training"
            ),


            "coding":

            request.form.get(
                "coding"
            ),


            "music":

            request.form.get(
                "music"
            )

        },


        "reflection":

        request.form.get(
            "reflection"
        )



    }



    collection.insert_one(
        record
    )



    return redirect(
        "/records/dashboard"
    )





# =====================
# CSV
# =====================


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
            "時間",
            "睡眠",
            "能量",
            "專注",
            "壓力",
            "情緒",
            "Flow",
            "想法",
            "訓練",
            "Coding",
            "音樂",
            "反思"

            ]

        )



        for r in records:


            writer.writerow(

                [

                r.get("date"),

                r.get("created_at"),


                r.get("sleep"),


                r.get("energy"),


                r.get("focus"),


                r.get("stress"),


                r.get("emotion"),


                r.get("brain",{}).get("flow"),


                r.get("brain",{}).get("thoughts"),


                r.get("life",{}).get("training"),


                r.get("life",{}).get("coding"),


                r.get("life",{}).get("music"),


                r.get("reflection")

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
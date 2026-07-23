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


# =========================
# 初始化 MongoDB
# =========================

init_db()



# =========================
# 首頁
# =========================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )



# =========================
# 靜態 Pages
# /pages/adhd
# /pages/desire
# =========================

@app.route("/pages/<page>")
def pages(page):

    try:

        return render_template(
            f"pages/{page}.html"
        )


    except Exception as e:

        print("PAGE ERROR:", e)

        return "Page Not Found", 404



# =========================
# Dashboard
# =========================

@app.route("/records/dashboard")
def dashboard():

    collection = get_db()


    records = collection.find().sort(
        "_id",
        -1
    )


    return render_template(
        "records/dashboard.html",
        records=records
    )



# =========================
# 新增每日紀錄
# =========================

@app.route(
    "/records/add",
    methods=["POST"]
)
def add_record():

    collection = get_db()


    sleep = request.form.get("sleep")

    energy = request.form.get("energy")

    focus = request.form.get("focus")

    stress = request.form.get("stress")



    record = {

        "date":
        datetime.now().strftime("%Y-%m-%d"),


        "sleep":
        float(sleep) if sleep else 0,


        "energy":
        int(energy) if energy else 0,


        "focus":
        int(focus) if focus else 0,


        "stress":
        int(stress) if stress else 0,


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



# =========================
# 匯出 CSV
# =========================

@app.route(
    "/records/export"
)
def export_records():


    collection = get_db()


    records = collection.find().sort(
        "_id",
        -1
    )



    filename = "junos_records.csv"



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
                "內耗事項"
            ]
        )



        for record in records:


            writer.writerow(
                [

                    record.get(
                        "date",
                        ""
                    ),


                    record.get(
                        "sleep",
                        0
                    ),


                    record.get(
                        "energy",
                        0
                    ),


                    record.get(
                        "focus",
                        0
                    ),


                    record.get(
                        "stress",
                        0
                    ),


                    record.get(
                        "thoughts",
                        ""
                    )

                ]
            )



    return send_file(
        filename,
        as_attachment=True
    )



# =========================
# Run Server
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
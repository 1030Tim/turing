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


# MongoDB 初始化

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
# 靜態 pages
# =========================


@app.route("/pages/<page>")
def pages(page):

    try:

        return render_template(
            f"pages/{page}.html"
        )

    except Exception as e:

        print(e)

        return "Page Not Found",404








# =========================
# Daily Record Dashboard
# =========================


@app.route("/records/dashboard")
def dashboard():


    collection = get_db()



    # 最近紀錄

    records = list(

        collection.find()

        .sort(
            [
                (
                    "date",
                    -1
                ),
                (
                    "time",
                    -1
                )
            ]
        )

        .limit(100)

    )



    return render_template(
        "records/dashboard.html",
        records=records
    )









# =========================
# 新增 Event
# =========================


@app.route(
    "/records/add",
    methods=["POST"]
)

def add_record():


    collection=get_db()



    now=datetime.now()



    record={


        # 日期

        "date":
        now.strftime(
            "%Y-%m-%d"
        ),



        # 時間

        "time":
        now.strftime(
            "%H:%M"
        ),




        # 紀錄類型

        "type":
        request.form.get(
            "type",
            "daily"
        ),





        # 身體

        "body":{


            "sleep":

            float(
                request.form.get(
                    "sleep",
                    0
                )
            ),


            "fatigue":

            int(
                request.form.get(
                    "fatigue",
                    0
                )
            )

        },






        # 大腦狀態

        "brain":{


            "focus":

            int(
                request.form.get(
                    "focus",
                    0
                )
            ),



            "flow":

            int(
                request.form.get(
                    "flow",
                    0
                )
            ),



            "adhd_start":

            int(
                request.form.get(
                    "adhd_start",
                    0
                )
            )

        },






        # 輸出

        "output":{


            "coding":

            int(
                request.form.get(
                    "coding",
                    0
                )
            ),



            "study":

            int(
                request.form.get(
                    "study",
                    0
                )
            ),



            "training":

            int(
                request.form.get(
                    "training",
                    0
                )
            ),



            "music":

            int(
                request.form.get(
                    "music",
                    0
                )
            )

        },







        # 情緒

        "emotion":{


            "stress":

            int(
                request.form.get(
                    "stress",
                    0
                )
            ),



            "noise":

            int(
                request.form.get(
                    "noise",
                    0
                )
            )

        },







        # 文字紀錄

        "note":

        request.form.get(
            "note",
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
# CSV Export
# =========================


@app.route(
    "/records/export"
)

def export_records():


    collection=get_db()



    records=collection.find()



    filename="junos_records.csv"




    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as f:



        writer=csv.writer(f)



        writer.writerow(
            [
                "日期",
                "時間",
                "類型",
                "睡眠",
                "疲勞",
                "專注",
                "Flow",
                "Coding",
                "Study",
                "Training",
                "Music",
                "壓力",
                "紀錄"
            ]
        )





        for r in records:



            writer.writerow(
                [

                    r.get(
                        "date"
                    ),


                    r.get(
                        "time"
                    ),



                    r.get(
                        "type"
                    ),



                    r["body"]
                    .get(
                        "sleep"
                    ),



                    r["body"]
                    .get(
                        "fatigue"
                    ),



                    r["brain"]
                    .get(
                        "focus"
                    ),



                    r["brain"]
                    .get(
                        "flow"
                    ),



                    r["output"]
                    .get(
                        "coding"
                    ),



                    r["output"]
                    .get(
                        "study"
                    ),



                    r["output"]
                    .get(
                        "training"
                    ),



                    r["output"]
                    .get(
                        "music"
                    ),



                    r["emotion"]
                    .get(
                        "stress"
                    ),



                    r.get(
                        "note"
                    )

                ]
            )





    return send_file(
        filename,
        as_attachment=True
    )









# =========================
# Run
# =========================


if __name__=="__main__":


    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
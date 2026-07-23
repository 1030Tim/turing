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


# 初始化 MongoDB

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
# Dashboard
# =========================


@app.route("/records/dashboard")
def dashboard():


    collection = get_db()


    records = list(
        collection.find()
        .sort(
            "date",
            -1
        )
    )


    return render_template(
        "records/dashboard.html",
        records=records
    )







# =========================
# 新增紀錄
# =========================


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



        "sleep":{


            "hours":
            float(
                request.form.get(
                    "sleep",
                    0
                )
            ),



            "quality":
            int(
                request.form.get(
                    "sleep_quality",
                    0
                )
            )

        },



        "brain":{


            "adhd_start":
            int(
                request.form.get(
                    "adhd_start",
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



            "flow":
            int(
                request.form.get(
                    "flow",
                    0
                )
            )


        },





        "body":{


            "fatigue":
            int(
                request.form.get(
                    "fatigue",
                    0
                )
            ),



            "training":
            int(
                request.form.get(
                    "training",
                    0
                )
            )


        },






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



            "creation":
            int(
                request.form.get(
                    "creation",
                    0
                )
            )


        },







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
            ),



            "stability":
            int(
                request.form.get(
                    "emotion",
                    0
                )
            )


        },







        "desire":{


            "urge":
            int(
                request.form.get(
                    "urge",
                    0
                )
            ),



            "trigger":
            request.form.get(
                "trigger"
            )


        },








        "reflection":{


            "win":
            request.form.get(
                "win"
            ),



            "problem":
            request.form.get(
                "problem"
            ),



            "tomorrow":
            request.form.get(
                "tomorrow"
            )


        }


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
                "date",
                "sleep",
                "focus",
                "flow",
                "coding",
                "study",
                "stress",
                "win"
            ]
        )



        for r in records:


            writer.writerow(
                [

                    r.get(
                        "date"
                    ),


                    r["sleep"]
                    .get(
                        "hours"
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


                    r["emotion"]
                    .get(
                        "stress"
                    ),


                    r["reflection"]
                    .get(
                        "win"
                    )

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
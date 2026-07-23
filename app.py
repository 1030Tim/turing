from flask import Flask, render_template, request, redirect
from datetime import datetime
from database import init_db, get_db
import os


app = Flask(__name__)


collection = get_db()


# =====================
# 首頁
# =====================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )



# =====================
# Daily Record Dashboard
# =====================

@app.route("/records/dashboard")
def dashboard():


    records = list(
        collection.find()
        .sort(
            "created_at",
            -1
        )
    )


    # 防止舊資料缺欄位
    for r in records:


        if "sleep" not in r:
            r["sleep"] = {}


        if "brain" not in r:
            r["brain"] = {}


        if "body" not in r:
            r["body"] = {}


        if "output" not in r:
            r["output"] = {}


        if "emotion" not in r:
            r["emotion"] = {}


        if "reflection" not in r:
            r["reflection"] = {}



        # 預設值

        r["sleep"].setdefault(
            "hours",
            "-"
        )

        r["sleep"].setdefault(
            "quality",
            "-"
        )


        r["brain"].setdefault(
            "adhd_start",
            "-"
        )

        r["brain"].setdefault(
            "focus",
            "-"
        )

        r["brain"].setdefault(
            "flow",
            "-"
        )


        r["output"].setdefault(
            "coding",
            "-"
        )

        r["output"].setdefault(
            "study",
            "-"
        )

        r["output"].setdefault(
            "creation",
            "-"
        )


        r["emotion"].setdefault(
            "stress",
            "-"
        )

        r["emotion"].setdefault(
            "noise",
            "-"
        )

        r["emotion"].setdefault(
            "stability",
            "-"
        )


        r["reflection"].setdefault(
            "win",
            ""
        )

        r["reflection"].setdefault(
            "problem",
            ""
        )

        r["reflection"].setdefault(
            "tomorrow",
            ""
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


    data = {


        "date":
        datetime.now()
        .strftime(
            "%Y-%m-%d"
        ),



        "created_at":
        datetime.now(),



        "sleep":
        {

            "hours":
            float(
                request.form.get(
                    "sleep"
                )
                or 0
            ),


            "quality":
            int(
                request.form.get(
                    "sleep_quality"
                )
                or 0
            )

        },



        "brain":
        {

            "adhd_start":
            int(
                request.form.get(
                    "adhd_start"
                )
                or 0
            ),


            "focus":
            int(
                request.form.get(
                    "focus"
                )
                or 0
            ),


            "flow":
            int(
                request.form.get(
                    "flow"
                )
                or 0
            )

        },



        "body":
        {

            "fatigue":
            int(
                request.form.get(
                    "fatigue"
                )
                or 0
            ),


            "training":
            int(
                request.form.get(
                    "training"
                )
                or 0
            )

        },



        "output":
        {

            "coding":
            int(
                request.form.get(
                    "coding"
                )
                or 0
            ),


            "study":
            int(
                request.form.get(
                    "study"
                )
                or 0
            ),


            "creation":
            int(
                request.form.get(
                    "creation"
                )
                or 0
            )

        },



        "emotion":
        {

            "stress":
            int(
                request.form.get(
                    "stress"
                )
                or 0
            ),


            "noise":
            int(
                request.form.get(
                    "noise"
                )
                or 0
            ),


            "stability":
            int(
                request.form.get(
                    "emotion"
                )
                or 0
            )

        },



        "desire":
        {

            "urge":
            int(
                request.form.get(
                    "urge"
                )
                or 0
            ),


            "trigger":
            request.form.get(
                "trigger",
                ""
            )

        },



        "reflection":
        {

            "win":
            request.form.get(
                "win",
                ""
            ),


            "problem":
            request.form.get(
                "problem",
                ""
            ),


            "tomorrow":
            request.form.get(
                "tomorrow",
                ""
            )

        }

    }



    collection.insert_one(
        data
    )


    return redirect(
        "/records/dashboard"
    )





# =====================
# Add page
# =====================

@app.route("/records/add")
def add_page():

    return render_template(
        "records/add.html"
    )




if __name__ == "__main__":


    init_db()


    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
from flask import Flask, render_template, request, redirect
from datetime import datetime
from database import init_db, get_db


app = Flask(__name__)

collection = get_db()



# =====================
# Home
# =====================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )



# =====================
# Dashboard
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


    for r in records:


        # =====================
        # 舊資料格式轉換
        # =====================


        if not isinstance(
            r.get("sleep"),
            dict
        ):

            old_sleep = r.get(
                "sleep",
                "-"
            )

            r["sleep"] = {

                "hours": old_sleep,

                "quality": "-"

            }



        if not isinstance(
            r.get("brain"),
            dict
        ):

            r["brain"] = {}



        if not isinstance(
            r.get("body"),
            dict
        ):

            r["body"] = {}



        if not isinstance(
            r.get("output"),
            dict
        ):

            r["output"] = {}



        if not isinstance(
            r.get("emotion"),
            dict
        ):

            r["emotion"] = {}



        if not isinstance(
            r.get("desire"),
            dict
        ):

            r["desire"] = {}



        if not isinstance(
            r.get("reflection"),
            dict
        ):

            r["reflection"] = {}




        # =====================
        # Default values
        # =====================


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



        r["body"].setdefault(
            "fatigue",
            "-"
        )

        r["body"].setdefault(
            "training",
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



        r["desire"].setdefault(
            "urge",
            "-"
        )

        r["desire"].setdefault(
            "trigger",
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
# Add Page
# =====================

@app.route(
    "/records/add",
    methods=["GET"]
)
def add_page():


    return render_template(
        "records/add.html"
    )







# =====================
# Add Record
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
# Static Pages
# =====================


@app.route("/pages/<name>")
def pages(name):

    return render_template(
        f"pages/{name}.html"
    )







# =====================
# Run
# =====================

if __name__ == "__main__":


    init_db()


    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
from flask import Flask, render_template, request, redirect
from datetime import datetime
from database import init_db, get_db


app = Flask(__name__)


collection = get_db()



# =========================
# 首頁
# =========================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )




# =========================
# Dashboard
# =========================

@app.route("/records/dashboard")
def dashboard():


    records = list(
        collection.find()
        .sort(
            "created_at",
            -1
        )
    )


    # 防止舊資料格式錯誤

    for r in records:


        if not isinstance(
            r.get("sleep"),
            dict
        ):
            r["sleep"] = {}


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
            r.get("digital"),
            dict
        ):
            r["digital"] = {}


        if not isinstance(
            r.get("reflection"),
            dict
        ):
            r["reflection"] = {}



        # default


        for key in [
            "hours",
            "quality"
        ]:
            r["sleep"].setdefault(
                key,
                "-"
            )


        for key in [
            "adhd_start",
            "focus",
            "flow"
        ]:
            r["brain"].setdefault(
                key,
                "-"
            )



        for key in [
            "fatigue",
            "training",
            "pain"
        ]:
            r["body"].setdefault(
                key,
                "-"
            )



        for key in [
            "coding",
            "study",
            "research",
            "writing",
            "music",
            "polevault"
        ]:
            r["output"].setdefault(
                key,
                "-"
            )



        for key in [
            "stress",
            "anxiety",
            "happiness",
            "confidence",
            "loneliness"
        ]:
            r["emotion"].setdefault(
                key,
                "-"
            )



        for key in [
            "urge",
            "trigger",
            "control"
        ]:
            r["desire"].setdefault(
                key,
                "-"
            )



        for key in [
            "phone",
            "youtube",
            "shorts",
            "social"
        ]:
            r["digital"].setdefault(
                key,
                "-"
            )



        for key in [
            "win",
            "problem",
            "tomorrow",
            "achievement",
            "insight"
        ]:
            r["reflection"].setdefault(
                key,
                ""
            )



    return render_template(
        "records/dashboard.html",
        records=records
    )






# =========================
# Add Page
# =========================


@app.route("/records/add")
def add_page():


    return render_template(
        "records/add.html"
    )







# =========================
# Add Record
# =========================


@app.route(
    "/records/add",
    methods=[
        "POST"
    ]
)
def add_record():


    now = datetime.now()



    def get_int(name):

        value = request.form.get(
            name,
            ""
        )

        try:

            return int(value)

        except:

            return 0




    def get_float(name):

        value = request.form.get(
            name,
            ""
        )

        try:

            return float(value)

        except:

            return 0





    data = {


        "date":
        now.strftime(
            "%Y-%m-%d"
        ),



        "created_at":
        now,



        "type":
        request.form.get(
            "type",
            "daily"
        ),



        "sleep":
        {

            "hours":
            get_float(
                "sleep"
            ),


            "quality":
            get_int(
                "sleep_quality"
            )

        },



        "brain":
        {

            "adhd_start":
            get_int(
                "adhd_start"
            ),


            "focus":
            get_int(
                "focus"
            ),


            "flow":
            get_int(
                "flow"
            )

        },



        "body":
        {

            "fatigue":
            get_int(
                "fatigue"
            ),


            "training":
            get_int(
                "training"
            ),


            "pain":
            get_int(
                "pain"
            )

        },



        "output":
        {

            "coding":
            get_int(
                "coding"
            ),


            "study":
            get_int(
                "study"
            ),


            "research":
            get_int(
                "research"
            ),


            "writing":
            get_int(
                "writing"
            ),


            "music":
            get_int(
                "music"
            ),


            "polevault":
            get_int(
                "polevault"
            )

        },



        "emotion":
        {

            "stress":
            get_int(
                "stress"
            ),


            "anxiety":
            get_int(
                "anxiety"
            ),


            "happiness":
            get_int(
                "happiness"
            ),


            "confidence":
            get_int(
                "confidence"
            ),


            "loneliness":
            get_int(
                "loneliness"
            )

        },



        "desire":
        {

            "urge":
            get_int(
                "urge"
            ),


            "trigger":
            request.form.get(
                "trigger",
                ""
            ),


            "control":
            request.form.get(
                "control",
                ""
            )

        },



        "digital":
        {

            "phone":
            get_int(
                "phone"
            ),


            "youtube":
            get_int(
                "youtube"
            ),


            "shorts":
            get_int(
                "shorts"
            ),


            "social":
            get_int(
                "social"
            )

        },



        "reflection":
        {

            "thoughts":
            request.form.get(
                "thoughts",
                ""
            ),


            "achievement":
            request.form.get(
                "achievement",
                ""
            ),


            "breakthrough":
            request.form.get(
                "breakthrough",
                ""
            ),


            "problem":
            request.form.get(
                "problem",
                ""
            ),


            "cause":
            request.form.get(
                "cause",
                ""
            ),


            "insight":
            request.form.get(
                "insight",
                ""
            ),


            "idea":
            request.form.get(
                "idea",
                ""
            ),


            "next_action":
            request.form.get(
                "next_action",
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







# =========================
# Pages
# =========================


@app.route("/pages/<name>")
def pages(name):

    try:

        return render_template(
            f"pages/{name}.html"
        )

    except:

        return "Page Not Found",404





# =========================
# Run
# =========================


if __name__ == "__main__":


    init_db()


    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
from flask import Flask, render_template, request, redirect
from datetime import datetime

from database import init_db, get_db
from daily_manager import DailyManager


app = Flask(__name__)


# =========================
# Database Manager
# =========================

collection = get_db()

daily_manager = DailyManager(
    collection
)



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


    records = daily_manager.get_records()


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
        "records/add.html",
        records=[]
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
            name
        )


        try:

            return int(value)

        except:

            return 0



    def get_float(name):

        value = request.form.get(
            name
        )


        try:

            return float(value)

        except:

            return 0.0



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



        "title":
        request.form.get(
            "title",
            ""
        ),



        "summary":
        request.form.get(
            "summary",
            ""
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
            ),


            "thinking_speed":
            get_int(
                "thinking_speed"
            ),


            "noise":
            get_int(
                "noise"
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
            ),


            "recovery":
            get_int(
                "recovery"
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



    daily_manager.insert(
        data
    )



    return redirect(
        "/records/dashboard"
    )



# =========================
# Pages
# =========================

@app.route(
    "/pages/<name>"
)
def pages(name):

    try:

        return render_template(
            f"pages/{name}.html"
        )


    except Exception:

        return (
            "Page Not Found",
            404
        )



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
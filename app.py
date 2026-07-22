from flask import Flask, render_template, request, redirect
from database import init_db, get_db
from datetime import datetime
import csv
import sqlite3

from flask import send_file

app = Flask(__name__)


init_db()



@app.route("/")
def index():

    return render_template("index.html")



@app.route("/records/dashboard")
def dashboard():

    conn = get_db()

    records = conn.execute(
        """
        SELECT * FROM records
        ORDER BY id DESC
        """
    ).fetchall()


    conn.close()


    return render_template(
        "records/dashboard.html",
        records=records
    )

@app.route("/records/export")
def export_records():

    conn = sqlite3.connect("junos.db")

    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
        sleep,
        energy,
        focus,
        stress,
        thoughts,
        created_at
        FROM daily_records
    """)

    data = cursor.fetchall()

    conn.close()


    file_path = "junos_records.csv"


    with open(
        file_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "睡眠時間",
            "能量評估",
            "專注度",
            "壓力",
            "內耗事項",
            "日期"
        ])

        writer.writerows(data)



    return send_file(
        file_path,
        as_attachment=True
    )


@app.route("/records/add", methods=["POST"])
def add_record():


    conn = get_db()


    conn.execute(
        """
        INSERT INTO records
        (
        date,
        sleep,
        energy,
        focus,
        stress,
        thoughts
        )

        VALUES(?,?,?,?,?,?)

        """,
        (

        datetime.now().strftime("%Y-%m-%d"),

        request.form["sleep"],

        request.form["energy"],

        request.form["focus"],

        request.form["stress"],

        request.form["thoughts"]

        )

    )


    conn.commit()
    conn.close()


    return redirect("/records/dashboard")




if __name__=="__main__":
    app.run(debug=True)
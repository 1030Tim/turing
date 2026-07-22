from flask import Flask, render_template, request, redirect, send_file
from database import init_db, get_db
from datetime import datetime
import csv
import tempfile


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



# CSV 匯出
@app.route("/records/export")
def export_records():

    conn = get_db()


    records = conn.execute(
        """
        SELECT
        date,
        sleep,
        energy,
        focus,
        stress,
        thoughts
        FROM records
        ORDER BY id DESC
        """
    ).fetchall()


    conn.close()



    temp = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".csv"
    )


    with open(
        temp.name,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as f:


        writer = csv.writer(f)


        writer.writerow([
            "日期",
            "睡眠",
            "能量",
            "專注",
            "壓力",
            "內耗事項"
        ])


        writer.writerows(records)



    return send_file(
        temp.name,
        as_attachment=True,
        download_name="JunOS_records.csv"
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
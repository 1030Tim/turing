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
import os


app = Flask(__name__)


# 初始化資料庫
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
# 靜態心理 pages
# /pages/desire
# /pages/emotion
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

    conn = get_db()


    records = conn.execute(
        """
        SELECT
        id,
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

        VALUES
        (?,?,?,?,?,?)

        """,

        (

            datetime.now()
            .strftime("%Y-%m-%d"),


            request.form.get(
                "sleep"
            ),


            request.form.get(
                "energy"
            ),


            request.form.get(
                "focus"
            ),


            request.form.get(
                "stress"
            ),


            request.form.get(
                "thoughts"
            )

        )
    )


    conn.commit()

    conn.close()


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



        writer.writerows(
            records
        )



    return send_file(
        filename,
        as_attachment=True
    )





# =========================
# Render 啟動
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
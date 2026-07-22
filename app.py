from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/pages/<page>")
def pages(page):

    return render_template(f"pages/{page}.html")


if __name__ == "__main__":
    app.run(debug=True)
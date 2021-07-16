import logging
from flask import Flask, session, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.db"
app.secret_key = "Elohell"
db = SQLAlchemy(app)
logging.basicConfig(level=logging.DEBUG)


class Transaction(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    currency = db.Column(db.String(1), nullable=False)
    value = db.Column(db.Float, nullable=False)
    madeby = db.Column(db.String(200), nullable=False)
    approvedby = db.Column(db.String(200), nullable=True)


@app.route("/", methods=['GET'])
def index():
    logging.debug(f"{session}")
    if "user" in session:
        return render_template("index.html", user=session['user'])
    else:
        return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    # transactions = Transaction.query.all()
    transactions = [Transaction(
        id=2, currency="$", value=1238.0, madeby="Luke", approvedby="skywalker")]
    return render_template("dashboard.html", user=session['user'], transactions=transactions)


@app.route("/create-transaction")
def create_transaction():
    return "almost there"


@app.route("/login", methods=['GET', 'POST'])
def login():
    # logging.debug(f"{request.method =}")
    # logging.debug(f"{session =}")
    if request.method == 'POST':
        logging.debug(f"{request.form['login'] =}")
        if request.form['login'] != "":
            session['user'] = request.form['login']
            return redirect(url_for("index"))
        else:
            session.pop('user', None)
            return render_template("login.html")
    else:
        return render_template("login.html")


if __name__ == '__main__':
    app.run(debug=True)

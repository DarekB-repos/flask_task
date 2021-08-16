import logging
from flask import Flask, session, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank.db"
app.secret_key = "Elohell"
db = SQLAlchemy(app)
logging.basicConfig(level=logging.DEBUG)

approvers = ["Admin", "Tommy"]


class Transaction(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    currency = db.Column(db.String(3), nullable=False)
    value = db.Column(db.Float, nullable=False)
    tran_date = db.Column(db.Date, nullable=False)
    approve_date = db.Column(db.Date, nullable=True)
    madeby = db.Column(db.String(200), nullable=False)
    approvedby = db.Column(db.String(200), nullable=True)


@app.route("/", methods=["GET"])
def index():
    logging.debug(f"{session}")
    if "user" in session:
        return render_template("index.html", user=session["user"])
    else:
        return redirect(url_for("login"))


@app.route("/dashboard")
def dashboard():
    transactions = Transaction.query.all()
    able_to_approve = session["user"] in approvers
    return render_template(
        "dashboard.html",
        user=session["user"],
        transactions=transactions,
        able_to_approve=able_to_approve,
    )


@app.route("/create-transaction", methods=["GET", "POST"])
def create_transaction():
    if request.method == "POST":
        transaction = Transaction(
            id=str(uuid4()),
            currency=request.form["currency"],
            value=request.form["value"],
            tran_date=datetime.datetime.now(),
            madeby=session["user"],
        )

        try:
            db.session.add(transaction)
            db.session.commit()
        except Exception as e:
            return f"well... why don't you just fuck off -- {str(e)}"

        else:
            return render_template("create_transaction.html")
    else:
        return render_template("create_transaction.html")


@app.route("/approve/<id>")
def approve(id):
    tran = Transaction.query.get_or_404(id)

    tran.approve_date = datetime.datetime.now()
    tran.approvedby = session["user"]

    try:
        db.session.commit()
        return redirect(url_for("dashboard"))

    except Exception as e:
        return f"Well why don't you just fuck off -- {str(e)}"


@app.route("/cancel/<id>")
def cancel(id):
    tran = Transaction.query.get_or_404(id)

    try:
        db.session.delete(tran)
        db.session.commit()
        return redirect(url_for("dashboard"))

    except Exception as e:
        return f"Well why don't you just fuck off -- {str(e)}"


@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user", None)

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    # logging.debug(f"{request.method =}")
    # logging.debug(f"{session =}")
    if request.method == "POST":
        logging.debug(f"{request.form['login'] =}")
        if request.form["login"] != "":
            session["user"] = request.form["login"]
            return redirect(url_for("index"))
        else:
            session.pop("user", None)
            return render_template("login.html")
    else:
        return render_template("login.html")


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0")

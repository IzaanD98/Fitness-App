import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime

from helpers import apology, login_required

# Configure application

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    return render_template("main.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/push", methods=["GET", "POST"])
@login_required
def push():
    if request.method == "GET":
        return render_template("push.html")

    else:
        data = request.form
        date = datetime.datetime.now()
        exercise = request.form.get('exercise')
        weight = request.form.get('weight')
        repetitions = request.form.get('repetitions')

        db.execute("INSERT INTO records (exercise, weight, repetitions, date) VALUES (?, ?, ?, ?)", exercise, weight, repetitions, date)

        flash("Recorded")
        return redirect("/push")

@app.route("/pull", methods=["GET", "POST"])
@login_required
def pull():

    if request.method == "GET":
        return render_template("pull.html")

    else:
        data = request.form
        date = datetime.datetime.now()
        exercise = request.form.get('exercise')
        weight = request.form.get('weight')
        repetitions = request.form.get('repetitions')

        db.execute("INSERT INTO records (exercise, weight, repetitions, date) VALUES (?, ?, ?, ?)", exercise, weight, repetitions, date)

        flash("Recorded")
        return redirect("/pull")

@app.route("/legs", methods=["GET", "POST"])
@login_required
def legs():

    if request.method == "GET":
        return render_template("legs.html")

    else:
        data = request.form
        date = datetime.datetime.now()
        exercise = request.form.get('exercise')
        weight = request.form.get('weight')
        repetitions = request.form.get('repetitions')

        db.execute("INSERT INTO records (exercise, weight, repetitions, date) VALUES (?, ?, ?, ?)", exercise, weight, repetitions, date)

        flash("Recorded")
        return redirect("/legs")

@app.route("/records")
@login_required
def records():
    records = db.execute("SELECT * FROM records")
    return render_template("records.html", records=records)




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("Username missing")

        if not password:
            return apology("Password is missing")

        if not confirmation:
            return apology("Confirmation Password is missing")

        if password != confirmation:
            return apology("Passwords do not match")

        hash = generate_password_hash(password)

        try:
            new_user = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
        except:
            return apology("Please use another Username")

        session["user_id"] = new_user

        return redirect("/")


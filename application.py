import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # Check if user already logged in
        if session.get("user_name") is None:
            return render_template("login.html")
        else:
            return redirect(url_for("welcome"))

    if request.method == "POST":
        # Try to login user
        name = request.form.get("user_name")
        pwd = request.form.get("user_pwd")
        user = db.execute("SELECT * FROM users WHERE name = :name AND password = :password",
                          {"name": name, "password": pwd}).fetchone()

        if user is None:
            return render_template("login.html", error_message="Invalid username or password")
        else:
            session["user_name"] = user.name
            return redirect(url_for("welcome"))


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        # Try to register user
        name = request.form.get("user_name")
        pwd = request.form.get("user_pwd")

        if db.execute("SELECT * FROM users WHERE name = :name", {"name": name}).rowcount == 1:
            return render_template("register.html", error_message="Username is already exists")
        else:
            db.execute("INSERT INTO users (name, password) VALUES (:name, :pwd)", {
                       "name": name, "pwd": pwd})
            db.commit()
            return render_template("login.html", message="Registration successful")


@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    if session.get("user_name") is None:
        return redirect("index")
    elif request.method == "POST":
        # Search the books
        text = request.form.get("text")
        results = db.execute(
            "SELECT * FROM books WHERE title LIKE :text OR author LIKE :text OR year LIKE :text OR isbn LIKE :text LIMIT 10", {"text": f"%{text}%"}).fetchall()
        return render_template("welcome.html", user_name=session["user_name"], results=results, input_value=text, alert_message="No matches found")
    else:
        return render_template("welcome.html", user_name=session["user_name"])


@app.route("/logout")
def logout():
    session["user_name"] = None
    return redirect(url_for("index"))


@app.route("/books/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
    reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
    book_info = db.execute(
            "SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if request.method == "GET":
        # Show the page
        if session.get("user_name") is None:
            return redirect("index")
        else:
            return render_template("book.html", book=book_info, user_name=session["user_name"], reviews=reviews)

    elif request.method == "POST":
        # Add a review
        # Check if user already did a review for this book
        if db.execute("SELECT * FROM reviews WHERE username = :username AND isbn = :isbn", {"username": session["user_name"], "isbn": isbn}).rowcount > 0:
            return render_template("book.html", book=book_info, user_name=session["user_name"], alert_message="You've already done review", reviews=reviews)
        else:
            rating = request.form.get("rating")
            text = request.form.get("text")
            db.execute("INSERT INTO reviews(rating, text, isbn, username) VALUES (:rating, :text, :isbn, :username)", {
                       "rating": rating, "text": text, "isbn": isbn, "username": session["user_name"]})
            db.commit()
            reviews = db.execute("SELECT * FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchall()
            return render_template("book.html", book=book_info, user_name=session["user_name"], reviews=reviews)
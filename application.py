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
        if session["user_id"] is None:
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
            session["user_id"] = user.id
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
    user = db.execute("SELECT * FROM users WHERE id = :id",
                      {"id": session["user_id"]}).fetchone()
    if user is None:
        return redirect("index")
    elif request.method == "POST":
        text = request.form.get("text")
        results = db.execute(
            "SELECT * FROM books WHERE title LIKE :text OR author LIKE :text OR year LIKE :text OR isbn LIKE :text LIMIT 10", {"text": f"%{text}%"}).fetchall()
        return render_template("welcome.html", user_name=user.name, results=results, input_value=text)
    else:
        return render_template("welcome.html", user_name=user.name)


@app.route("/logout")
def logout():
    session["user_id"] = None
    return redirect(url_for("index"))

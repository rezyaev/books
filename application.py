import os

from flask import Flask, session, render_template, request
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
    return render_template("login.html")


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
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
    else:
        return render_template("register.html")

@app.route("/welcome")
def welcome():
    return render_template("welcome.html", user_name="Admin")
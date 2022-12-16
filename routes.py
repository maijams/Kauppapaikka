from app import app
from flask import render_template, redirect, request
from db import db
import users


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Annetut salasanat eivät täsmää")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/items")
def listings():
    result = db.session.execute("SELECT * FROM items")
    items = result.fetchall()
    return render_template("listings.html", items=items)


@app.route("/new")
def new():
    return render_template("new.html")


@app.route("/send", methods=["POST"])
def send():
    header = request.form["header"]
    content = request.form["content"]
    price = request.form["price"]
    location = request.form["location"]
    sql = "INSERT INTO items (header, content, price, location) VALUES (:header, :content, :price, :location)"
    db.session.execute(
        sql, {"header": header, "content": content, "price": price, "location": location})
    db.session.commit()
    return redirect("/items")

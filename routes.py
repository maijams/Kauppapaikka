from app import app
from flask import render_template, redirect, request
from db import db

@app.route("/")
def index():
    return render_template("index.html")

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
    db.session.execute(sql, {"header":header,"content":content, "price":price, "location":location})
    db.session.commit()
    return redirect("/items")
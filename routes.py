from app import app
from flask import render_template, redirect, request
import users
import items
import user_favourites as fav
import comments
import photos

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
def all_items():
    try:
        list = items.get_sorted_items("sent_at", "DESC")
    except:
        return render_template("error.html", message="Ilmoitusten haussa tapahtui virhe")
    return render_template("items.html", items=list)


@app.route("/item/<id>")
def item(id):
    try:
        data = items.get_item_by_id(id)
        user = data[0].user_id
        username = users.get_username(user)
        photo = photos.get_photo(id)
        comment = comments.get_comments(id)
    except:
        return render_template("error.html", message="Ilmoituksen näyttämisessä tapahtui virhe")
    return render_template("item.html", item=data, username=username, photo=photo, comments=comment)


@app.route("/image/<id>")
def get_photo(id):
    photo = photos.get_photo(id)
    return photo


@app.route("/own_items")
def own_items():
    user = users.user_id()
    try:
        list = items.get_own_items(user)
    except:
        return render_template("error.html", message="Ilmoitusten haussa tapahtui virhe")
    return render_template("own_items.html", items=list)
            
        
@app.route("/delete_item", methods=["POST"])
def delete_item():
    users.check_csrf()
    id = request.form["id"]
    try:
        items.delete_item(id)
    except:
        return render_template("error.html", message="Ilmoituksen poistamisessa tapahtui virhe")
    return redirect("/own_items")


@app.route("/own_data")
def own_data():
    return render_template("own_data.html")


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")

    if request.method == "POST":
        users.check_csrf()
        try:
            header = request.form["header"]
            type = request.form["type"]
            content = request.form["content"]
            price = request.form["price"]
            location = request.form["location"]
            user_id = users.user_id()
            items.add_item(header, type, content, price, location, user_id)
        except:
            message = "Ilmoituksen lisääminen ei onnistunut. Täytithän kaikki vaaditut kentät?"
            return render_template("error.html", message=message)
        photo = request.files["photo"]
        if photo is not None:
            id = items.get_latest_item_id()
            name = photo.filename
            try:
                photos.add_photo(name, photo, id)
            except:
                return render_template("error.html", message="Kuvan lisääminen ei onnistunut")
        return redirect("/items")
    

@app.route("/items_sort_newest")
def items_newest():
    try:
        list = items.get_sorted_items("sent_at", "DESC")
    except:
        return render_template("error.html", message="Tuotteiden järjestämisessä tapahtui virhe")
    return render_template("items.html", items=list)
 
    
@app.route("/items_sort_oldest")
def items_oldest():
    try:
        list = items.get_sorted_items("sent_at", "")
    except:
        return render_template("error.html", message="Tuotteiden järjestämisessä tapahtui virhe")
    return render_template("items.html", items=list)


@app.route("/items_sort_lowest_price")
def items_lowest_price():
    try:
        list = items.get_sorted_items("price", "")
    except:
        return render_template("error.html", message="Tuotteiden järjestämisessä tapahtui virhe")
    return render_template("items.html", items=list)


@app.route("/items_sort_highest_price")
def items_highest_price():
    try:
        list = items.get_sorted_items("price", "DESC")
    except:
        return render_template("error.html", message="Tuotteiden järjestämisessä tapahtui virhe")
    return render_template("items.html", items=list)


@app.route("/items_sort_type_asc")
def items_type_asc():
    try:
        list = items.get_sorted_items("type", "")
    except:
        return render_template("error.html", message="Tuotteiden järjestämisessä tapahtui virhe")
    return render_template("items.html", items=list)


@app.route("/items_sort_type_desc")
def items_type_desc():
    try:
        list = items.get_sorted_items("type", "DESC")
    except:
        return render_template("error.html", message="Tuotteiden järjestämisessä tapahtui virhe")
    return render_template("items.html", items=list)


@app.route("/favourites")
def get_favourites():
    user_id = users.user_id()
    try:
        list = fav.get_favourites(user_id)
    except:
        return render_template("error.html", message="Suosikkien haussa tapahtui virhe")
    return render_template("favourites.html", items=list)


@app.route("/add_favourite/<item>")
def add_favourite(item):
    user_id = users.user_id()
    if fav.is_already_favourite(user_id, item):
        return render_template("error.html", message="Tuote on jo suosikkilistallasi")
    fav.add_favourite(user_id, item)
    return redirect("/favourites")


@app.route("/delete_favourite", methods=["POST"])
def delete_favourite():
    users.check_csrf()
    user_id = users.user_id()
    item = request.form["id"]
    try:
        fav.delete_favourite(user_id, item)
    except:
        return render_template("error.html", message="Suosikkien haussa tapahtui virhe")
    return redirect("/favourites")


@app.route("/add_comment", methods=["POST"])
def add_comment():
    users.check_csrf()
    comment = request.form["comment"]
    item_id = request.form["item_id"]
    user_id = users.user_id()
    try:
        comments.add_comment(comment, item_id, user_id)
    except:
        return render_template("error.html", message="Kommentin lisäyksessä tapahtui virhe")
    return redirect("/item/" + str(item_id))
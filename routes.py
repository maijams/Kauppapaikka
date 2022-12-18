from app import app
from flask import render_template, redirect, request
import users
import items
import user_favourites as fav
import comments

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if password1 != password2:
            return render_template('error.html', message='Annetut salasanat eivät täsmää')
        if users.register(username, password1):
            return redirect('/')
        else:
            return render_template('error.html', message='Rekisteröinti ei onnistunut')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users.login(username, password):
            return redirect('/')
        else:
            return render_template('error.html', message='Väärä tunnus tai salasana')


@app.route('/logout')
def logout():
    users.logout()
    return redirect('/')


@app.route('/items')
def all_items():
    list = items.get_sorted_items('sent_at', 'DESC')
    return render_template('items.html', items=list)


@app.route('/item/<id>')
def item(id):
    data = items.get_item_by_id(id)
    photo = items.show_photo(id)
    comment = comments.get_comments(id)
    return render_template('item.html', item=data, photo=photo, comments=comment)


@app.route('/show_photo/<id>')
def show_photo(id):
    photo = items.show_photo(id)
    return photo


@app.route('/own_items')
def own_items():
    user = users.user_id()
    list = items.get_own_items(user)
    return render_template('own_items.html', items=list)
            
        
@app.route('/delete_item', methods=['POST'])
def delete_item():
    id = request.form['id']
    items.delete_item(id)
    return redirect('/own_items')


@app.route('/own_data')
def own_data():
    return render_template('own_data.html')


@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        return render_template('new.html')

    if request.method == 'POST':
        header = request.form['header']
        type = request.form['type']
        content = request.form['content']
        price = request.form['price']
        location = request.form['location']
        user_id = users.user_id()
        id = items.add_item(header, type, content, price, location, user_id)
        
        photo = request.files['photo']
        name = photo.filename
        items.add_photo(name, photo, id)
        return redirect('/items')
    

@app.route('/items_sort_newest')
def items_newest():
    list = items.get_sorted_items('sent_at', 'DESC')
    return render_template('items.html', items=list)
 
    
@app.route('/items_sort_oldest')
def items_oldest():
    list = items.get_sorted_items('sent_at', '')
    return render_template('items.html', items=list)


@app.route('/items_sort_lowest_price')
def items_lowest_price():
    list = items.get_sorted_items('price', '')
    return render_template('items.html', items=list)


@app.route('/items_sort_highest_price')
def items_highest_price():
    list = items.get_sorted_items('price', 'DESC')
    return render_template('items.html', items=list)


@app.route('/items_sort_type_asc')
def items_type_asc():
    list = items.get_sorted_items('type', '')
    return render_template('items.html', items=list)


@app.route('/items_sort_type_desc')
def items_type_desc():
    list = items.get_sorted_items('type', 'DESC')
    return render_template('items.html', items=list)


@app.route('/favourites')
def get_favourites():
    user_id = users.user_id()
    list = fav.get_favourites(user_id)
    return render_template('favourites.html', items=list)


@app.route('/add_favourite/<item>')
def add_favourite(item):
    user_id = users.user_id()
    if fav.is_already_favourite(user_id, item):
        return render_template('error.html', message='Tuote on jo suosikkilistallasi')
    fav.add_favourite(user_id, item)
    return redirect('/favourites')


@app.route('/delete_favourite', methods=['POST'])
def delete_favourite():
    user_id = users.user_id()
    item = request.form['id']
    fav.delete_favourite(user_id, item)
    return redirect('/favourites')


@app.route("/add_comment", methods=["POST"])
def add_comment():
    comment = request.form["comment"]
    item_id = request.form["item_id"]
    user_id = users.user_id()
    comments.add_comment(comment, item_id, user_id)
    return redirect("/item/" + str(item_id))
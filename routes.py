from app import app
from flask import render_template, redirect, request
import users
import items


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
    return render_template('item.html', item=data)


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
        content = request.form['content']
        price = request.form['price']
        location = request.form['location']
        user_id = users.user_id()
        items.add_item(header, content, price, location, user_id)
        return redirect('/items')
    

@app.route('/items_newest')
def items_newest():
    list = items.get_sorted_items('sent_at', 'DESC')
    return render_template('items.html', items=list)
 
    
@app.route('/items_oldest')
def items_oldest():
    list = items.get_sorted_items('sent_at', '')
    return render_template('items.html', items=list)


@app.route('/items_lowest_price')
def items_lowest_price():
    list = items.get_sorted_items('price', '')
    return render_template('items.html', items=list)


@app.route('/items_highest_price')
def items_highest_price():
    list = items.get_sorted_items('price', 'DESC')
    return render_template('items.html', items=list)



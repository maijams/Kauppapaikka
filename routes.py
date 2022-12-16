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
    list = items.get_items()
    return render_template('items.html', items=list)


@app.route('/own_items')
def own_items():
    user = users.user_id()
    list = items.get_own_items(user)
    return render_template('own_items.html', items=list)


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
    

    



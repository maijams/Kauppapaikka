from db import db
from flask import make_response

def get_sorted_items(sort, direction):
    sql = f'SELECT * FROM items WHERE visible=TRUE ORDER BY {sort} {direction}'
    result = db.session.execute(sql)
    return result.fetchall()

def get_own_items(user_id):
    sql = 'SELECT * FROM items WHERE visible=TRUE AND user_id=:user_id ORDER BY sent_at DESC'
    result = db.session.execute(sql, {'user_id':user_id})
    return result.fetchall()

def add_item(header, content, price, location, user_id):
    sql = ('INSERT INTO items (header, content, price, location, user_id, sent_at, visible) '
           'VALUES (:header, :content, :price, :location, :user_id, NOW(), true)')
    db.session.execute(
        sql,
        {'header':header, 'content':content, 'price':price, 'location':location, 'user_id':user_id})
    db.session.commit()
    sql = 'SELECT id FROM items ORDER BY id DESC'
    new_id = db.session.execute(sql).fetchone()[0]
    return new_id

def delete_item(id):
    sql = 'UPDATE items SET visible=false WHERE id=:id'
    db.session.execute(sql, {'id':id})
    db.session.commit()
    
def get_item_by_id(id):
    sql = 'SELECT * FROM items WHERE visible=TRUE AND id=:id'
    result = db.session.execute(sql, {'id':id})
    return result.fetchall()

def add_photo(name, file, item_id):
    data = file.read()
    sql = 'INSERT INTO photos (name, data, item_id) VALUES (:name, :data, :item_id)'
    db.session.execute(sql, {'name':name, 'data':data, 'item_id':item_id})
    db.session.commit()
    
def show_photo(item):
    try:
        sql = 'SELECT data FROM photos WHERE :item_id'
        result = db.session.execute(sql, {'item_id':item})
        data = result.fetchone()[0]
        photo = make_response(bytes(data))
        photo.headers.set("Content-Type","image/png")
        return photo
    except:
        return None
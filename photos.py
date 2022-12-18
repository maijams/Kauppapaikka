from db import db
from flask import make_response


def add_photo(name, file, item_id):
    data = file.read()
    sql = 'INSERT INTO photos (name, data, item_id) VALUES (:name, :data, :item_id)'
    db.session.execute(sql, {'name':name, 'data':data, 'item_id':item_id})
    db.session.commit()
    
    
def show_photo(item):
    sql = 'SELECT data FROM photos WHERE item_id=:item'
    result = db.session.execute(sql, {'item':item})
    data = result.fetchone()[0]
    if len(data) > 0:
        photo = make_response(bytes(data))
        photo.headers.set("Content-Type","image/png")
        return photo
    return None
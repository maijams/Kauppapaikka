from db import db


def get_items():
    sql = 'SELECT * FROM items'
    result = db.session.execute(sql)
    return result.fetchall()

def get_own_items(user_id):
    sql = 'SELECT * FROM items WHERE user_id=:user_id'
    result = db.session.execute(sql, {'user_id':user_id})
    return result.fetchall()

def add_item(header, content, price, location, user_id):
    sql = ('INSERT INTO items (header, content, price, location, user_id, sent_at) '
           'VALUES (:header, :content, :price, :location, :user_id, NOW())')
    db.session.execute(
        sql, 
        {'header':header, 'content':content, 'price':price, 'location':location, 'user_id':user_id})
    db.session.commit()
    
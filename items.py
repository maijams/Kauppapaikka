from db import db


def get_sorted_items(sort, direction):
    sql = f'SELECT * FROM items WHERE visible=TRUE ORDER BY {sort} {direction}'
    result = db.session.execute(sql)
    return result.fetchall()

def get_items():
    sql = 'SELECT * FROM items WHERE visible=TRUE'
    result = db.session.execute(sql)
    return result.fetchall()

def get_own_items(user_id):
    sql = f'SELECT * FROM items WHERE user_id={user_id} AND visible=TRUE'
    result = db.session.execute(sql)
    return result.fetchall()

def add_item(header, content, price, location, user_id):
    sql = ('INSERT INTO items (header, content, price, location, user_id, sent_at, visible) '
           'VALUES (:header, :content, :price, :location, :user_id, NOW(), true)')
    db.session.execute(
        sql,
        {'header':header, 'content':content, 'price':price, 'location':location, 'user_id':user_id})
    db.session.commit()
    
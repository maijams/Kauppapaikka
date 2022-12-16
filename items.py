from db import db


def get_sorted_items(sort, direction):
    sql = f'SELECT * FROM items WHERE visible=TRUE ORDER BY {sort} {direction}'
    result = db.session.execute(sql)
    return result.fetchall()

def get_own_items(user_id):
    sql = f'SELECT * FROM items WHERE visible=TRUE AND user_id={user_id} ORDER BY sent_at DESC'
    result = db.session.execute(sql)
    return result.fetchall()

def add_item(header, content, price, location, user_id):
    sql = ('INSERT INTO items (header, content, price, location, user_id, sent_at, visible) '
           'VALUES (:header, :content, :price, :location, :user_id, NOW(), true)')
    db.session.execute(
        sql,
        {'header':header, 'content':content, 'price':price, 'location':location, 'user_id':user_id})
    db.session.commit()
    
def delete_item(id):
    sql = f'UPDATE items SET visible=false WHERE id={id}'
    db.session.execute(sql)
    db.session.commit()
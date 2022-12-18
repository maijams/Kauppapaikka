from db import db


def get_sorted_items(sort, direction):
    if sort == 'sent_at' and direction == 'DESC':
        sql = ('SELECT id, header, type, price, location, sent_at '
               'FROM items WHERE visible=TRUE ORDER BY sent_at DESC')
        
    elif sort == 'sent_at' and direction == '':
        sql = ('SELECT id, header, type, price, location, sent_at '
               'FROM items WHERE visible=TRUE ORDER BY sent_at')
        
    elif sort == 'price' and direction == 'DESC':
        sql = ('SELECT id, header, type, price, location, sent_at '
               'FROM items WHERE visible=TRUE ORDER BY price DESC')
        
    elif sort == 'price' and direction == '':
        sql = ('SELECT id, header, type, price, location, sent_at '
               'FROM items WHERE visible=TRUE ORDER BY price')
        
    elif sort == 'type' and direction == 'DESC':
        sql = ('SELECT id, header, type, price, location, sent_at '
               'FROM items WHERE visible=TRUE ORDER BY type DESC')
        
    elif sort == 'type' and direction == '':
        sql = ('SELECT id, header, type, price, location, sent_at '
               'FROM items WHERE visible=TRUE ORDER BY type')

    result = db.session.execute(sql)
    return result.fetchall()


def get_own_items(user_id):
    sql = ('SELECT id, header, type, price, location, sent_at '
           'FROM items WHERE visible=TRUE AND user_id=:user_id ORDER BY sent_at DESC')
    result = db.session.execute(sql, {'user_id':user_id})
    return result.fetchall()


def add_item(header, type, content, price, location, user_id):
    sql = ('INSERT INTO items (header, type, content, price, location, user_id, sent_at, visible) '
           'VALUES (:header, :type, :content, :price, :location, :user_id, NOW(), true)')
    db.session.execute(
        sql,
        {'header':header, 'type':type, 'content':content, 'price':price, 'location':location, 'user_id':user_id})
    db.session.commit()
   
    
def get_latest_item_id():
    sql = 'SELECT id FROM items ORDER BY id DESC'
    id = db.session.execute(sql).fetchone()[0]
    return id


def delete_item(id):
    sql = 'UPDATE items SET visible=false WHERE id=:id'
    db.session.execute(sql, {'id':id})
    db.session.commit()
    
    
def get_item_by_id(id):
    sql = ('SELECT id, header, type, content, price, user_id, location, sent_at '
           'FROM items WHERE visible=TRUE AND id=:id')
    result = db.session.execute(sql, {'id':id})
    return result.fetchall()
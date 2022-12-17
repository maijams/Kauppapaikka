from db import db
import items

def add_favourite(user_id, item):
    sql = f'INSERT INTO user_favourites (user_id, sale_item_id, visible) VALUES ({user_id}, {item}, true)'
    db.session.execute(sql)
    db.session.commit()
    
def get_favourites(user_id):
    sql = f'SELECT sale_item_id FROM user_favourites WHERE visible=TRUE AND user_id={user_id}'
    result = db.session.execute(sql)
    item_ids =  result.fetchall()

    favourites = []
    for id in item_ids:
        item = items.get_item_by_id(id[0])
        favourites.append(item)

    return favourites

def is_already_favourite(user_id, item):
    sql = f'SELECT * FROM user_favourites WHERE visible=TRUE AND user_id={user_id} AND sale_item_id={item}'
    result = db.session.execute(sql)
    if len(result.fetchall()) > 0:
        return True
    return False

def delete_favourite(user_id, item):
    sql = f'UPDATE user_favourites SET visible=false WHERE visible=TRUE AND user_id={user_id} AND sale_item_id={item}'
    db.session.execute(sql)
    db.session.commit()
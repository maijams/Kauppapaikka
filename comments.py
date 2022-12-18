from db import db


def add_comment(comment, item_id, user_id):
    sql = ("INSERT INTO comments (content, item_id, sender_id, sent_at) "
           "VALUES (:content, :item_id, :user_id, NOW())")
    db.session.execute(sql, {"content":comment, "item_id":item_id, "user_id":user_id})
    db.session.commit()
    
    
def get_comments(item):
    sql = ("SELECT C.content, U.username, C.sent_at FROM comments C, users U "
           "WHERE item_id=:item AND U.id=C.sender_id ORDER BY C.sent_at DESC")
    result = db.session.execute(sql, {"item":item})
    comments = result.fetchall()
    return comments

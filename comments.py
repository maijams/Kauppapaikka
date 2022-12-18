from db import db


def add_comment(comment, item_id, user_id):
    sql = "INSERT INTO comments (content, item_id, sender_id, sent_at) VALUES (:content, :item_id, :user_id, NOW())"
    db.session.execute(sql, {"content":comment, "item_id":item_id, "user_id":user_id})
    db.session.commit()
    
def get_comments(id):
    sql = "SELECT c.content, u.username, c.sent_at FROM comments c, users u WHERE item_id=:id AND u.id=c.sender_id"
    result1 = db.session.execute(sql, {"id":id})
    comments = result1.fetchall()
    return comments

from db import db
from flask import session, request, abort
import secrets
from werkzeug.security import check_password_hash, generate_password_hash


def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user[0]
            session["user_name"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return True
    return False
    

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["csrf_token"]


def user_id():
    return session.get("user_id",0)


def get_username(id):
    sql = "SELECT username FROM users WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchall()


def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
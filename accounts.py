from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import os

def login(username, password):
    sql = "SELECT password, id FROM accounts WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def register(username, password):
    if len(username) < 4 or len(password) < 6:
        return False
    if is_in_usernames(username):
        return False
    hash_value = generate_password_hash(password)
    try: 
        sql ='''INSERT INTO accounts (username,password) 
                VALUES (:username,:password)'''
        db.session.execute(sql,{"username":username,"password":hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["user_id"]

def user_id():
    return session.get("user_id",0)

def get_username():
    username = 0
    if user_id() != 0:
        id = user_id()
        sql = "SELECT username FROM accounts WHERE id=:id"
        result = db.session.execute(sql, {"id":id})
        username = result.fetchone()[0]
    return username

def is_in_usernames(username):
    visible = 1
    sql ='''SELECT 1 
            FROM accounts 
            WHERE username=:username AND visible=:visible'''
    result = db.session.execute(sql,{"username":username, "visible":visible})
    if result.fetchone() != None:
        return True
    return False
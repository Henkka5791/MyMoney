from db import db
import accounts
from flask import make_response
import datetime

def all_years():
    id = accounts.user_id()
    sql = '''SELECT DISTINCT EXTRACT(YEAR FROM created_at) 
             FROM TRANSACTIONS t, SUBCATEGORIES s, CATEGORIES c, ACCOUNTS a
             WHERE 
                a.id = :id AND 
                c.account_id = a.id 
                AND s.category_id = c.id 
                AND t.subcategory_id = s.id 
                AND t.visible = 1'''
    result = db.session.execute(sql,{"id":id})
    years = result.fetchall()
    for i in range(len(years)):
        years[i] = int(years[i][0])
    if len(years) == 0:
        time = datetime.datetime.now()
        years.append(time.strftime("%Y"))
    return years

def add(subcategory_id, amount, description, data, name):
    amount = amount_validate(amount, subcategory_id)
    if description == "Maksimi 100":
        description = ""
    if len(description) > 100:
        return False
    if len(data) == 0:
        try:
            sql = "INSERT INTO transactions(description,amount,created_at,subcategory_id) VALUES(:description, :amount, NOW(),:subcategory_id)"
            db.session.execute(sql, \
                {"description":description, "amount":amount, "subcategory_id":subcategory_id})
            db.session.commit()
            return True
        except:
            return False
    else:
        try:
            sql = "INSERT INTO pictures (name,data) VALUES (:name,:data) RETURNING id"
            result = db.session.execute(sql, {"name":name, "data":data})
            id = result.fetchone()[0]
            sql ='''INSERT INTO transactions(description,amount,created_at,subcategory_id,picture_id) 
                    VALUES(:description, :amount, NOW(),:subcategory_id,:id)'''
            db.session.execute(sql,\
                {"description":description, "amount":amount, "subcategory_id":subcategory_id, "id":id})
            db.session.commit()
            return True
        except:
            return False

def list():
    id = accounts.user_id()
    sql ='''SELECT 
                t.created_at,
                t.amount,
                c.name,
                s.name,
                t.description,
                t.id,
                p.id,
                p.visible 
            FROM categories c, subcategories s, accounts a,transactions t 
            LEFT JOIN pictures p ON p.id=t.picture_id 
            WHERE t.visible=1 AND
                c.visible = 1 AND
                s.visible = 1 AND 
                t.subcategory_id=s.id AND 
                s.category_id=c.id AND 
                c.account_id=a.id AND 
                a.id=:id 
            ORDER BY t.created_at DESC LIMIT 10'''
    result = db.session.execute(sql, {"id":id})
    transactions = result.fetchall()
    return transactions

def is_outcome(subcategory_id):
    sql ='''SELECT c.outcome 
            FROM categories c, subcategories s 
            WHERE s.id=:subcategory_id AND c.id=s.category_id'''
    result = db.session.execute(sql, {"subcategory_id":subcategory_id})
    outcome = result.fetchone()[0]
    if outcome == 1:
        return True
    return False

def view_one(id):
    account_id = accounts.user_id()
    sql ='''SELECT t.created_at,t.amount,t.description,t.id,p.id,p.visible 
            FROM categories c, subcategories s,transactions t 
            LEFT JOIN pictures p ON p.id=t.picture_id 
            WHERE 
                t.id=:id AND 
                t.subcategory_id=s.id AND
                c.id = s.category_id AND
                c.account_id=:account_id'''
    result = db.session.execute(sql, {"id":id, "account_id":account_id})
    transaction = result.fetchone()
    return transaction 

def update(subcategory_id, amount, description, id, file):
    amount = amount_validate(amount, subcategory_id)
    if len(file) == 0:
        try:
            sql ='''UPDATE transactions 
                    SET 
                        description=:description, 
                        amount=:amount, 
                        subcategory_id=:subcategory_id 
                    WHERE id=:id'''
            result = db.session.execute(sql,\
                {"description":description, "amount":amount, "subcategory_id":subcategory_id, "id":id})
            db.session.commit()
            return True
        except:
            return False
    else:
        try:
            sql = "INSERT INTO pictures (data) VALUES (:file) RETURNING id"
            result = db.session.execute(sql, {"file":file})
            picture_id = result.fetchone()[0]
            sql ='''UPDATE transactions 
                    SET description=:description, amount=:amount, subcategory_id=:subcategory_id, picture_id=:picture_id 
                    WHERE id=:id'''
            result = db.session.execute(sql,\
                {"description":description, "amount":amount, "subcategory_id":subcategory_id, "picture_id":picture_id, "id":id})
            db.session.commit()
            return True
        except:
            return False

def remove(id):
    visible = 0
    try:
        sql="UPDATE transactions SET visible=:visible WHERE id=:id"
        result = db.session.execute(sql, {"visible":visible, "id":id})
        db.session.commit()
        return True
    except:
        return False

def valid_picture_id(transaction_id, picture_id):
    visible = 1
    sql ='''SELECT p.id FROM pictures p,transactions t 
            WHERE 
                t.id=:transaction_id AND
                p.id=:picture_id AND
                p.visible=:visible'''
    result = db.session.execute(sql,\
        {"transaction_id":transaction_id, "picture_id":picture_id, "visible":visible})
    picture_id = result.fetchone()[0]
    if picture_id == None:
        picture_id = 0
    return picture_id

def show_picture(id):
    sql = "SELECT data,visible FROM pictures WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    data = result.fetchone()[0]
    response = make_response(bytes(data))
    response.headers.set("Content-Type", "image/jpeg")
    return response

def amount_validate(amount, subcategory_id):
    amount = amount.replace(",",".")
    amount = amount.replace("-","")
    try:
        amount_float = float(amount)
        amount_float = round(amount_float, 2)
        if is_outcome(subcategory_id):
            amount_float = -1*amount_float
        return amount_float
    except:
        return amount

def get_picture_id(transaction_id):
    sql = "SELECT picture_id FROM transactions WHERE id=:transaction_id"
    result = db.session.execute(sql,\
        {"transaction_id":transaction_id})
    picture_id = result.fetchone()[0]
    return picture_id

def picture_remove(transaction_id):
    try:
        picture_id = get_picture_id(transaction_id)
        visible = 0
        sql = "UPDATE pictures SET visible=:visible WHERE id=:picture_id"
        db.session.execute(sql, {"visible":visible, "picture_id":picture_id})
        db.session.commit()
        return True
    except:
        return False

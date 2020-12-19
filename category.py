from db import db
import accounts

def income_categories():
    account_id = accounts.user_id()
    visible = 1
    outcome = 0
    sql = "SELECT name FROM categories WHERE account_id=:account_id AND visible=:visible AND outcome=:outcome"
    result = db.session.execute(sql, {"account_id":account_id,"visible":visible,"outcome":outcome})
    categories_income = result.fetchall()
    return categories_income

def outcome_categories():
    account_id = accounts.user_id()
    visible = 1
    outcome = 1
    sql = "SELECT name FROM categories WHERE account_id=:account_id AND visible=:visible AND outcome=:outcome"
    result = db.session.execute(sql, {"account_id":account_id,"visible":visible,"outcome":outcome})
    categories_outcome = result.fetchall()
    return categories_outcome

def add_category(name,outcome):
    account_id = accounts.user_id()
    try:
        sql = "INSERT INTO categories (name, outcome, account_id) VALUES (:name,:outcome,:account_id)"
        db.session.execute(sql,{"name":name,"outcome":outcome,"account_id":account_id})
        db.session.commit()
        return True
    except:
        return False

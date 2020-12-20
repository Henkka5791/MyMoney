from db import db
import accounts

def income_categories():
    account_id = accounts.user_id()
    visible = 1
    outcome = 0
    sql = "SELECT id,name FROM categories WHERE account_id=:account_id AND visible=:visible AND outcome=:outcome"
    result = db.session.execute(sql, {"account_id":account_id,"visible":visible,"outcome":outcome})
    categories_income = result.fetchall()
    return categories_income

def outcome_categories():
    account_id = accounts.user_id()
    visible = 1
    outcome = 1
    sql = "SELECT id,name FROM categories WHERE account_id=:account_id AND visible=:visible AND outcome=:outcome"
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

def subcategory_list(id):
    visible = 1
    category_id = id
    sql = "SELECT id, name FROM subcategories WHERE category_id=:category_id AND visible=:visible"
    result = db.session.execute(sql,{"category_id":category_id, "visible":visible})
    subcategories = result.fetchall()
    return subcategories

def category_name(id):
    visible = 1
    sql = "SELECT name FROM categories WHERE id=:id AND visible=:visible"
    result = db.session.execute(sql,{"id":id,"visible":visible})
    name = result.fetchone()[0]
    return name

def add_subcategory(name,category_id):
    try:
        sql = "INSERT INTO subcategories(name,category_id) VALUES (:name,:category_id)"
        db.session.execute(sql,{"name":name,"category_id":category_id})
        db.session.commit()
        return True
    except:
        return False
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

def category_list():
    account_id = accounts.user_id()
    visible = 1
    sql = "SELECT id,name FROM categories WHERE account_id=:account_id AND visible=:visible"
    result = db.session.execute(sql, {"account_id":account_id,"visible":visible})
    categories = result.fetchall()
    return categories

def category_subcategory_list_all():
    account_id = accounts.user_id()
    visible = 1
    sql = "SELECT c.name,sc.name,sc.id FROM categories c, subcategories sc WHERE c.account_id=:account_id AND c.id=sc.category_id AND c.visible=:visible AND sc.visible=:visible"
    result = db.session.execute(sql,{"account_id":account_id,"visible":visible})
    category_subcategory_list = result.fetchall()
    return category_subcategory_list

def add_category(name,outcome):
    account_id = accounts.user_id()
    try:
        sql = "INSERT INTO categories (name, outcome, account_id) VALUES (:name,:outcome,:account_id)"
        db.session.execute(sql,{"name":name,"outcome":outcome,"account_id":account_id})
        db.session.commit()
        return True
    except:
        return False

def subcategory_list(category_id):
    visible = 1
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

def category_id(name):
    sql = "SELECT id FROM categories"

def add_subcategory(name,category_id):
    try:
        sql = "INSERT INTO subcategories(name,category_id) VALUES (:name,:category_id)"
        db.session.execute(sql,{"name":name,"category_id":category_id})
        db.session.commit()
        return True
    except:
        return False

def category_remove(id):
    visible = 0
    try:
        sql = "UPDATE categories SET visible=:visible WHERE id=:id"
        db.session.execute(sql,{"visible":visible,"id":id})
        db.session.commit()
        return True
    except:
        return False

def subcategory_remove(id):
    visible = 0
    try:
        sql = "UPDATE subcategories SET visible=:visible WHERE id=:id"
        db.session.execute(sql,{"visible":visible,"id":id})
        db.session.commit()
        return True
    except:
        return False
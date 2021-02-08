from db import db
import accounts,budgets

def income_categories():
    account_id = accounts.user_id()
    visible = 1
    outcome = 0
    sql ='''SELECT id,name 
            FROM categories 
            WHERE 
                account_id=:account_id AND 
                visible=:visible AND 
                outcome=:outcome'''
    result = db.session.execute(sql,\
        {"account_id":account_id, "visible":visible, "outcome":outcome})
    categories_income = result.fetchall()
    return categories_income

def outcome_categories():
    account_id = accounts.user_id()
    visible = 1
    outcome = 1
    sql ='''SELECT id,name 
            FROM categories 
            WHERE 
                account_id=:account_id AND 
                visible=:visible AND 
                outcome=:outcome'''
    result = db.session.execute(sql,\
        {"account_id":account_id, "visible":visible, "outcome":outcome})
    categories_outcome = result.fetchall()
    return categories_outcome

def category_list():
    account_id = accounts.user_id()
    visible = 1
    sql ='''SELECT id,name 
            FROM categories 
            WHERE account_id=:account_id AND visible=:visible'''
    result = db.session.execute(sql,\
        {"account_id":account_id, "visible":visible})
    categories = result.fetchall()
    return categories

def category_subcategory_list_all():
    account_id = accounts.user_id()
    visible = 1
    sql ='''SELECT c.name,sc.name,sc.id 
            FROM categories c, subcategories sc 
            WHERE c.account_id=:account_id AND c.id=sc.category_id AND c.visible=:visible AND sc.visible=:visible'''
    result = db.session.execute(sql,\
        {"account_id":account_id, "visible":visible})
    category_subcategory_list = result.fetchall()
    return category_subcategory_list

def add_category(name, outcome):
    account_id = accounts.user_id()
    if in_categories(name, account_id):
        return False
    try:
        sql ='''INSERT INTO categories (name, outcome, account_id) 
                VALUES (:name,:outcome,:account_id) RETURNING ID'''
        result = db.session.execute(sql,\
            {"name":name, "outcome":outcome, "account_id":account_id})
        category_id = result.fetchone()[0]
        years = budgets.budget_years()
        for year in years:
            year = int(year[0])
            if budgets.category_not_in_budget(year, category_id):
                budgets.budget_add_category(year, category_id)
        db.session.commit()
        return True
    except:
        return False

def subcategory_list(category_id):
    visible = 1
    sql ='''SELECT id, name 
            FROM subcategories 
            WHERE category_id=:category_id AND visible=:visible'''
    result = db.session.execute(sql,\
        {"category_id":category_id, "visible":visible})
    subcategories = result.fetchall()
    return subcategories

def category_name(id):
    visible = 1
    sql = "SELECT name FROM categories WHERE id=:id AND visible=:visible"
    result = db.session.execute(sql, {"id":id, "visible":visible})
    name = result.fetchone()[0]
    return name

def category_id(name):
    sql = "SELECT id FROM categories"

def add_subcategory(name, category_id):
    account_id = accounts.user_id()
    if in_subcategory(name, account_id):
        return False
    try:
        sql ='''INSERT INTO subcategories(name,category_id) 
                VALUES (:name,:category_id)'''
        db.session.execute(sql, {"name":name, "category_id":category_id})
        db.session.commit()
        return True
    except:
        return False

def category_remove(id):
    visible = 0
    try:
        sql = "UPDATE categories SET visible=:visible WHERE id=:id"
        db.session.execute(sql, {"visible":visible, "id":id})
        db.session.commit()
        return True
    except:
        return False

def subcategory_remove(id):
    visible = 0
    try:
        sql = "UPDATE subcategories SET visible=:visible WHERE id=:id"
        db.session.execute(sql, {"visible":visible, "id":id})
        db.session.commit()
        return True
    except:
        return False

def in_categories(name, id):
    visible = 1
    sql ='''SELECT 1 from categories 
            WHERE 
                UPPER(name)=UPPER(:name) AND 
                account_id=:id AND 
                visible=:visible'''
    result = db.session.execute(sql, {"name":name, "id":id, "visible":visible})
    if result.fetchone() != None:
        return True
    return False

def in_subcategory(name, id):
    visible = 1
    sql ='''SELECT 1 
            FROM subcategories s, categories c 
            WHERE UPPER(s.name)=UPPER(:name) AND s.category_id=c.id AND c.account_id=:id AND s.visible=:visible'''
    result = db.session.execute(sql, {"name":name, "id":id, "visible":visible})
    if result.fetchone() != None:
        return True
    return False
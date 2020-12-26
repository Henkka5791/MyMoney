from db import db
import accounts

def add(subcategory_id,amount,description):
    amount = amount_validate(amount,subcategory_id)
    try:
        sql = "INSERT INTO transactions(description,amount,created_at,subcategory_id) VALUES(:description, :amount, NOW(),:subcategory_id)"
        db.session.execute(sql, {"description":description,"amount":amount,"subcategory_id":subcategory_id})
        db.session.commit()
        return True
    except:
        return False

def list():
    sql = "SELECT t.created_at,t.amount,c.name,s.name,t.description, t.id FROM transactions t, categories c, subcategories s WHERE t.visible=1 AND c.visible = 1 AND s.visible = 1 AND t.subcategory_id=s.id AND s.category_id=c.id ORDER BY t.created_at DESC LIMIT 10"
    result = db.session.execute(sql)
    transactions = result.fetchall()
    return transactions

def is_outcome(subcategory_id):
    sql = "SELECT c.outcome FROM categories c, subcategories s WHERE s.id=:subcategory_id AND c.id=s.category_id"
    result = db.session.execute(sql, {"subcategory_id":subcategory_id})
    outcome = result.fetchone()[0]
    if outcome == 1:
        return True
    return False

def view_one(id):
    sql = "SELECT t.created_at,t.amount,t.description,t.id,c.name,s.name,p.data FROM categories c, subcategories s,transactions t LEFT JOIN pictures p ON p.id=t.picture_id WHERE t.id=:id AND t.subcategory_id=s.id AND c.id = s.category_id"
    result = db.session.execute(sql,{"id":id})
    transaction = result.fetchone()
    print(transaction[0])
    return transaction 

def update(subcategory_id,amount,description,id):
    amount = amount_validate(amount,subcategory_id)
    try:
        sql = "UPDATE transactions SET description=:description, amount=:amount, subcategory_id=:subcategory_id WHERE id=:id"
        result = db.session.execute(sql,{"description":description,"amount":amount,"subcategory_id":subcategory_id,"id":id})
        db.session.commit()
        return True
    except:
        return False

def remove(id):
    visible = 0
    try:
        sql="UPDATE transactions SET visible=:visible WHERE id=:id"
        resul = db.session.execute(sql,{"visible":visible,"id":id})
        db.session.commit()
        return True
    except:
        return False

def amount_validate(amount,subcategory_id):
    amount = amount.replace(",",".")
    amount = amount.replace("-","")
    try:
        amount_float = float(amount)
        amount_float = round(amount_float,2)
        if is_outcome(subcategory_id):
            amount_float = -1*amount_float
        return amount_float
    except:
        return amount

from db import db
import accounts

def add(subcategory_id,amount,description):
    amount = float(amount)
    if is_outcome(subcategory_id):
        amount = -1*amount
    print(subcategory_id,amount,description)
    try:
        sql = "INSERT INTO transactions(description,amount,created_at,subcategory_id) VALUES(:description, :amount, NOW(),:subcategory_id)"
        db.session.execute(sql, {"description":description,"amount":amount,"subcategory_id":subcategory_id})
        db.session.commit()
        return True
    except:
        return False

def list():
    sql = "SELECT created_at, amount, description FROM transactions WHERE visible=1"
    result = db.session.execute(sql)
    transactions = result.fetchall()
    return transactions

def is_outcome(subcategory_id):
    sql = "SELECT c.outcome FROM categories c, subcategories s WHERE s.id=:subcategory_id AND c.id=s.category_id"
    result = db.session.execute(sql, {"subcategory_id":subcategory_id})
    outcome = result.fetchone()[0];
    if outcome == 1:
        return True
    return False

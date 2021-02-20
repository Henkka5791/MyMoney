from db import db
import categories,accounts
import datetime

def create_budget(year):
    category_list = categories.category_list()
    try:
        if year in budget_years():
            return False
        if year < datetime.datetime.now().year-1 or year > datetime.datetime.now().year+10:
            return False
        for category in category_list:
            for i in range(1,13):
                category_id = category[0]
                period = str(year)+"-"+str(i)+"-"+"1"
                sql ='''INSERT INTO budgets(period,category_id) 
                        VALUES (:period,:category_id)'''
                db.session.execute(sql,\
                    {"period":period, "category_id":category_id})
        db.session.commit()
        return True
    except:
        return False

def budget_years():
    id = accounts.user_id()
    sql ='''SELECT extract(year FROM period) as yyyy 
            FROM budgets b, categories c, accounts a 
            WHERE b.category_id=c.id AND c.account_id=a.id AND a.id=:id 
            GROUP BY yyyy 
            ORDER BY yyyy DESC'''
    result = db.session.execute(sql, {"id":id})
    years = result.fetchall()
    return years

def budget_add_category(year, category_id):
    try:
        for i in range(1,13):
            period = str(year)+"-"+str(i)+"-"+"1"
            print(period)
            sql ='''INSERT INTO budgets(period,category_id) 
                    VALUES (:period,:category_id)'''
            db.session.execute(sql,{"period":period,"category_id":category_id})
        db.session.commit()
        return True
    except:
        return False
 
def category_not_in_budget(year, category_id):
    period = str(year)+"-"+"1"+"-"+"1"
    sql = "SELECT :category_id FROM budgets WHERE period=:period AND category_id=:category_id"
    result = db.session.execute(sql,\
        {"category_id":category_id, "period":period})
    is_category = result.fetchone()
    if is_category == None:
        return True
    return False

def budget_list(year):
    account_id = accounts.user_id()
    period_start = str(year)+"-"+"1"+"-"+"1"
    period_end = str(year)+"-"+"12"+"-"+"2"
    visible = 1
    sql = '''SELECT 
                c.name,
                ROUND(b.amount::numeric,2),
                extract(month FROM b.period) AS month,
                b.id 
            FROM 
                categories c, 
                budgets b 
            WHERE 
                c.account_id=:account_id 
                AND c.id=b.category_id 
                AND b.period>=:period_start 
                AND b.period<:period_end 
                AND c.visible=:visible 
            ORDER BY c.name,month ASC'''
    result = db.session.execute(sql,\
        {"account_id":account_id, "period_start":period_start, "period_end":period_end, "visible":visible})
    budgets = result.fetchall()
    return budgets

def budget_update(ids, amounts):
    try:
        for idx in enumerate(ids):
            amount = amounts[idx[0]]
            amount = amount.replace(",",".")
            amount = amount.replace("-","")
            id = idx[1]
            sql = "UPDATE budgets SET amount=:amount WHERE id=:id"
            db.session.execute(sql, {"amount":amount, "id":id})
        db.session.commit()
        return True
    except:
        return False

def budget_sum(budget_year):
    account_id = accounts.user_id()
    visible = 1
    sql = '''SELECT 
                c.name,
                ROUND(sum(b.amount)::numeric,2) 
            FROM 
                categories c, 
                budgets b 
            WHERE 
                c.account_id=:account_id 
                AND b.category_id=c.id 
                AND c.visible=:visible 
                AND extract(year FROM b.period)=:budget_year 
            GROUP BY 1'''
    result = db.session.execute(sql,\
        {"account_id":account_id, "visible":visible, "budget_year":budget_year})
    sums = result.fetchall()
    return sums
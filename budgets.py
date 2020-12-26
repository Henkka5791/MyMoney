from db import db
import categories,accounts

def create_budget(year):
    category_list = categories.category_list()
    try:
        for category in category_list:
            print(category)
            for i in range(1,13):
                category_id = category[0]
                period = str(year)+"-"+str(i)+"-"+"1"
                sql = "INSERT INTO budgets(period,category_id) VALUES (:period,:category_id)"
                db.session.execute(sql,{"period":period,"category_id":category_id})
        db.session.commit()
        return True
    except:
        return False

def budget_years():
    id = accounts.user_id()
    sql = "SELECT extract(year FROM period) as yyyy FROM budgets b, categories c, accounts a WHERE b.category_id=c.id AND c.account_id=a.id AND a.id=:id GROUP BY yyyy"
    result = db.session.execute(sql,{"id":id})
    years = result.fetchall()
    return years
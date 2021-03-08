from db import db
import accounts
from calendar import monthrange
from datetime import datetime,timedelta

def set_days(month_from, year_from, month_to, year_to):
    time_from = datetime.strptime(year_from+"-"+month_from+"-"+"01",'%Y-%m-%d')
    last_day = monthrange(int(year_to),int(month_to))
    time_to = datetime.strptime\
        (year_to+"-"+month_to+"-"+str(last_day[1])+" "+"23:59:59",'%Y-%m-%d %H:%M:%S')
    if time_from > time_to:
        time_from = time_to - timedelta(days=30)
    print(time_from)
    return (time_from, time_to)

def monthly(time_from, time_to):
    id = accounts.user_id()
    visible = 1
    sql = '''SELECT 
                b.year::numeric::integer,
                b.month::numeric::integer,
                COALESCE(t.income,0),
                COALESCE(b.budget_income,0),
                COALESCE(t.outcome,0),
                COALESCE(b.budget_outcome,0),
                COALESCE(t.income,0)+COALESCE(t.outcome,0) AS balance,
                COALESCE(b.budget_outcome,0)+COALESCE(t.outcome,0) AS budget_balance
            FROM (
                SELECT 
                    EXTRACT(year FROM t.created_at) AS year,
                    EXTRACT(month FROM t.created_at) AS month,
                    ROUND(SUM(CASE WHEN t.amount > 0 THEN t.amount ELSE 0 END)::numeric,2) AS income,
                    ROUND(SUM(CASE WHEN t.amount < 0 THEN t.amount ELSE 0 END)::numeric,2) AS outcome 
                FROM    
                    transactions t,
                    subcategories s,
                    categories c 
                WHERE 
                    t.subcategory_id=s.id
                    AND s.category_id=c.id 
                    AND c.account_id=:id 
                    AND t.visible=:visible
                    AND s.visible=:visible 
                    AND c.visible=:visible 
                GROUP BY 
                    1,2
                ) AS t 
            FULL OUTER JOIN (
                SELECT 
                    EXTRACT(year FROM b.period) AS year,
                    EXTRACT(month FROM b.period) AS month, 
                    b.period AS period,
                    sum(CASE WHEN c.outcome=0 THEN b.amount ELSE 0 END) AS budget_income,
                    sum(CASE WHEN c.outcome=1 THEN b.amount ELSE 0 END) AS budget_outcome 
                FROM 
                    budgets b, 
                    categories c 
                WHERE 
                    b.category_id=c.id 
                    AND c.account_id=:id 
                    AND c.visible=:visible 
                GROUP BY 1,2,3) AS b 
            ON 
                t.year=b.year 
                AND t.month=b.month 
            WHERE 
                b.period>=:time_from 
                AND b.period<=:time_to'''
    result = db.session.execute(sql,\
        {"time_from":time_from, "time_to":time_to, "visible":visible, "id":id})
    monthly_results = result.fetchall()
    return monthly_results

def total_sum(time_from, time_to):
    id = accounts.user_id()
    visible = 1
    sql = '''SELECT 
                count(b.month),
                sum(COALESCE(t.income,0)),
                sum(COALESCE(b.budget_income,0)),
                sum(COALESCE(t.outcome,0)),
                sum(COALESCE(b.budget_outcome,0)),
                sum(COALESCE(t.income,0)+COALESCE(t.outcome,0)),
                sum(COALESCE(b.budget_outcome,0)+COALESCE(t.outcome,0))
            FROM (
                SELECT 
                    EXTRACT(year FROM t.created_at) AS year,
                    EXTRACT(month FROM t.created_at) AS month,
                    ROUND(SUM(CASE WHEN t.amount > 0 THEN t.amount ELSE 0 END)::numeric,2) AS income,
                    ROUND(SUM(CASE WHEN t.amount < 0 THEN t.amount ELSE 0 END)::numeric,2) AS outcome 
                FROM    
                    transactions t,
                    subcategories s,
                    categories c 
                WHERE 
                    t.subcategory_id=s.id
                    AND s.category_id=c.id 
                    AND c.account_id=:id 
                    AND t.visible=:visible
                    AND s.visible=:visible 
                    AND c.visible=:visible 
                GROUP BY 
                    1,2) AS t 
            FULL OUTER JOIN (
                SELECT 
                    EXTRACT(year FROM b.period) AS year,
                    EXTRACT(month FROM b.period) AS month, 
                    b.period AS period,
                    ROUND(sum(CASE WHEN c.outcome=0 THEN b.amount ELSE 0 END)::numeric,2) AS budget_income,
                    ROUND(sum(CASE WHEN c.outcome=1 THEN b.amount ELSE 0 END)::numeric,2) AS budget_outcome  
                FROM 
                    budgets b, 
                    categories c 
                WHERE 
                    b.category_id=c.id 
                    AND c.account_id=:id 
                    AND c.visible=:visible 
                GROUP BY 1,2,3) AS b 
            ON 
                t.year=b.year 
                AND t.month=b.month 
            WHERE 
                b.period>=:time_from 
                AND b.period<=:time_to'''
    result = db.session.execute(sql,\
        {"time_from":time_from, "time_to":time_to, "visible":visible, "id":id})
    total = result.fetchone()
    return total

def by_categories(time_from, time_to):
    id = accounts.user_id()
    visible = 1
    sql ='''SELECT 
                c.name,
                s.name,
                ROUND(sum(t.amount)::numeric,2),
                count(t.amount) 
            FROM 
                transactions t, 
                categories c, 
                subcategories s 
            WHERE 
                t.subcategory_id=s.id 
                AND s.category_id=c.id 
                AND c.account_id=:id
                AND t.created_at>=:time_from
                AND t.created_at<=:time_to
                AND t.visible=:visible
                AND c.visible=:visible
                AND s.visible=:visible 
            GROUP BY 1,2'''
    result = db.session.execute(sql,\
        {"id":id, "time_from":time_from, "time_to":time_to, "visible":visible})
    category_sums = result.fetchall()
    return category_sums
from db import db
import accounts
from calendar import monthrange

def monthly(month_from,month_to,year_from,year_to):
    time_from = str(year_from)+"-"+str(month_from)+"-"+"1"
    last_day = monthrange(year_to,month_to)
    time_to = str(year_to)+"-"+str(month_to)+"-"+str(last_day[1])
    visible = 1
    sql = "SELECT EXTRACT(year FROM t.created_at),EXTRACT(month FROM t.created_at),ROUND(SUM(CASE WHEN t.amount < 0 THEN t.amount ELSE 0 END)::numeric,2),ROUND(SUM(CASE WHEN t.amount > 0 THEN t.amount ELSE 0 END)::numeric,2),ROUND(SUM(t.amount)::numeric,2),a.amount FROM transactions t, (SELECT b.period AS period,SUM(b.amount) AS amount FROM budgets b GROUP BY 1) AS a WHERE EXTRACT(year FROM t.created_at)=EXTRACT(year FROM period) AND EXTRACT(month FROM t.created_at)=EXTRACT(month FROM period) AND t.created_at>=:time_from AND t.created_at<=:time_to AND t.visible=:visible GROUP BY 1,2,6;"
    result = db.session.execute(sql,{"time_from":time_from,"time_to":time_to,"visible":visible})
    monthly_results = result.fetchall()
    return monthly_results

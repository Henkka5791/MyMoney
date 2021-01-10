from db import db
import accounts

def first_and_last():
    id = accounts.user_id()
    visible = 1
    sql ='''SELECT 
                MIN(t.created_at), MAX(t.created_at) 
            FROM 
                transactions t, subcategories s, categories c 
            WHERE
                t.subcategory_id=s.id
                AND s.category_id=c.id
                AND c.account_id=:id
                AND t.visible=:visible
                AND s.visible=:visible
                AND c.visible=:visible'''
    result = db.session.execute(sql,{"id":id,"visible":visible})
    times = result.fetchone()
    return times

def find(time_from,time_to,query):
    print(time_from,time_to,query)
    id = accounts.user_id()
    visible = 1
    sql ='''SELECT 
                t.created_at,ROUND(t.amount::numeric,2),c.name,s.name,t.description,t.id,p.id 
            FROM 
                categories c,subcategories s,transactions t 
            LEFT JOIN pictures p ON p.id=t.picture_id 
            WHERE
                (t.description LIKE :query
                OR c.name LIKE :query
                OR s.name LIKE :query)
                AND t.created_at>=:time_from
                AND t.created_at<=:time_to 
                AND t.visible=:visible 
                AND c.visible=:visible
                AND s.visible=:visible
                AND t.subcategory_id=s.id 
                AND s.category_id=c.id 
                AND c.account_id=:id
            ORDER BY 
                t.created_at,c.name,s.name DESC LIMIT 100'''
    result=db.session.execute(sql,{"query":"%"+query+"%","time_from":time_from,"time_to":time_to,"visible":visible,"id":id})
    transaction_list=result.fetchall()
    return transaction_list

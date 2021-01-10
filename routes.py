from app import app
from flask import redirect, render_template, request, session,make_response
import accounts
import categories, transactions, budgets,summary,search
from datetime import datetime

@app.route("/")
def index():
    username = accounts.get_username()
    return render_template("index.html", username = username)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if accounts.login(username, password):
        return redirect("/")
    else: 
       return render_template("error.html", error = "Väärä tunnus tai salasana")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if accounts.register(username,password):
            return redirect("/")
        else:
            return render_template("register.html",error_message="Rekisteröinti ei onnistunut")

@app.route("/logout")
def logout():
    accounts.logout()
    return redirect("/")

@app.route("/categories", methods=["GET","POST"])
def category_view():
    if request.method == "GET":
        incomes = categories.income_categories()
        outcomes = categories.outcome_categories()
        return render_template("categories.html",incomes = incomes, outcomes = outcomes)
    if request.method == "POST":
        name = request.form["name"]
        outcome = request.form["outcome"]
        if categories.add_category(name,outcome):
            return redirect("/categories")
        else:
            return render_template("categories.html",error_message="Kategorian lisääminen ei onnistunut")

@app.route("/categories/<int:id>",methods=["GET","POST"])
def subcategory_view(id):
    if request.method == "GET":
        subcategory_list = categories.subcategory_list(id)
        name = categories.category_name(id)
        return render_template("subcategory.html", subcategory_list=subcategory_list, name=name, id=id)
    if request.method == "POST":
        name = request.form["name"]
        category_id = id
        if categories.add_subcategory(name,category_id):
            return redirect("/categories/"+str(id))
        else:
            return render_template("error.html", error="Alakategorian lisäy ei onnistunut")

@app.route("/categories/<int:id>/remove",methods=["POST"])
def category_remove(id):
    if categories.category_remove(id):
        return redirect("/categories")
    return render_template("error.html", error="Kategorian poisto ei onnistunut")

@app.route("/categories/<int:id>/<int:sub_id>",methods=["POST"])
def subcategory_remove(id,sub_id):
    if categories.subcategory_remove(sub_id):
        return redirect("/categories/"+str(id))
    else:
        return render_template("error.html", error="Alakategorian poisto ei onnistunut")

@app.route("/transactions", methods=["GET","POST"])
def transactions_view():
    if request.method == "GET":
        categories_subcategories = categories.category_subcategory_list_all()
        transactions_list = transactions.list()
        return render_template("transactions.html",categories_subcategories = categories_subcategories, transactions_list = transactions_list)
    if request.method == "POST":
        subcategory_id = request.form["category_subcategory"]
        amount = request.form["amount"]
        description = request.form["description"]
        file = request.files["file"]
        data = file.read()
        name = file.filename
        if transactions.add(subcategory_id,amount,description,data,name):
            return redirect("/transactions")
        else:
            return render_template("error.html", error="Tapahtuman lisäys ei onnistunut")

@app.route("/transactions/<int:id>", methods=["GET","POST"])
def transaction_edit(id):
    if request.method == "GET":
        picture_id = request.args["picture_id"]
        transaction = transactions.view_one(id)
        categories_subcategories = categories.category_subcategory_list_all()
        return render_template("transaction_single.html",transaction = transaction,categories_subcategories=categories_subcategories,picture_id=picture_id)
    if request.method == "POST":     
        subcategory_id = request.form["category_subcategory"]
        amount = request.form["amount"]
        description = request.form["description"]
        if transactions.update(subcategory_id,amount,description,id):
            return redirect("/transactions")
        else:
            return render_template("error.html", error="Tapahtuman muokkaus ei onnistunut")

@app.route("/transactions/<int:id>/remove",methods=["GET","POST"])
def transaction_remove(id):
    if transactions.remove(id):
        return redirect("/transactions")
    else:
        return render_template("error.html", error="Tapahtuman poistaminen ei onnistunut")

@app.route("/budgets",methods=["GET","POST"])
def budget_create():
    if request.method == "GET":
        years = budgets.budget_years()
        return render_template("budgets.html",years=years)
    if request.method == "POST":
        year = request.form["year"]
        if budgets.create_budget(year):
            return redirect("/budgets")
        else:
            return render_template("error.html", error="Budjetin luonti ei onnistunut")

@app.route("/budgets/<int:year>",methods=["GET","POST"])
def budget_edit(year):
    if request.method == "GET":
        year_budget = budgets.budget_list(year)
        sums = budgets.budget_sum(year)
        return render_template("budget_year.html",year=year,year_budget=year_budget,sums=sums)
    if request.method == "POST":
        budget_ids = request.form.getlist("budget_id")
        amounts = request.form.getlist("amount")
        print("budget_ids: "+str(len(budget_ids))+"amounts: "+str(len(amounts)))
        if budgets.budget_update(budget_ids,amounts):
            year = int(year)
            return redirect("/budgets/"+str(year))
        else:
            return render_template("error.html", error="Budjetin päivittäminen ei onnistunut")

@app.route("/summary")
def summary_result():
    try:
        time_from = request.args["time_from"]
        time_to = request.args["time_to"]
        monthly_result = summary.monthly(time_from,time_to)
        total = summary.total_sum(time_from,time_to)
        by_categories = summary.by_categories(time_from,time_to)
        times = summary.set_days(time_from,time_to)
        return render_template("summary.html", monthly_result=monthly_result,total=total,by_categories=by_categories,time_from=times[0],time_to=times[1])
    except:
        print("except")
        return render_template("summary.html",monthly_result=[],total=[],time_from="", time_to="")

#@app.route("/transactions/pictures/<int:id>")
#def show_pictures(id):
#    return render_template("picture.html",id=id)

@app.route("/transactions/pictures/<int:id>/show")
def show(id):
    picture = transactions.show_picture(id)
    return picture

@app.route("/search")
def view_search():
    time_to=""
    time_from=""
    print(time_from)
    print(type(request.args["time_from"]))
    if not request.args["time_from"]:
        times = search.first_and_last()
        time_from = times[0]
    else:
        time_from = request.args["time_from"]+" "+"00:00:00"
        time_from = datetime.strptime(time_from,"%Y-%m-%d %H:%M:%S")
    if not request.args["time_to"]:
        times = search.first_and_last()
        time_to = times[1]
    else:
        time_to = request.args["time_to"]+" "+"23:59:59"
        time_to = datetime.strptime(time_to,"%Y-%m-%d %H:%M:%S")
        print(time_from,time_to)
    if not request.args["query"]:
        query=""
    else:
        query = request.args["query"]

    transaction_list = search.find(time_from,time_to,query)
    if query=="":
        query = "ei hakusanaa"
    return render_template("search.html",transaction_list=transaction_list,time_from=time_from,time_to=time_to,query=query)

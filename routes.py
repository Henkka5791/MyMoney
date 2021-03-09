from app import app
from flask import redirect, render_template, request, session, make_response,flash, abort
import accounts
import categories, transactions, budgets, summary, search
from datetime import datetime, timedelta

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
        flash(f"Väärä käyttäjätunnus tai salasana")
        return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if accounts.register(username, password):
            return redirect("/")
        else:
            if accounts.is_in_usernames(username):
                flash(f"Käyttäjätunnus on jo käytössä")
            else:
                flash(f"Käyttäjätunnuksen pitää olla vähintään 4 merkkiä pitkä ja salasanan vähintään 6 merkkiä pitkä.")
            return render_template("register.html", error_message="error")

@app.route("/logout")
def logout():
    accounts.logout()
    return redirect("/")

@app.route("/categories", methods=["GET", "POST"])
def category_view():
    if request.method == "GET":
        incomes = categories.income_categories()
        outcomes = categories.outcome_categories()
        return render_template("categories.html", incomes=incomes, outcomes=outcomes)
    if request.method == "POST":
        name = request.form["name"]
        outcome = request.form["outcome"]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if categories.add_category(name, outcome):
            return redirect("/categories")
        else:
            return render_template("error.html",\
                error_message="Kategorian lisääminen ei onnistunut")

@app.route("/categories/<int:id>", methods=["GET","POST"])
def subcategory_view(id):
    if request.method == "GET":
        subcategory_list = categories.subcategory_list(id)
        name = categories.category_name(id)
        return render_template("subcategory.html",\
            subcategory_list=subcategory_list, name=name, id=id)
    if request.method == "POST":
        name = request.form["name"]
        category_id = id
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if categories.add_subcategory(name,category_id):
            return redirect("/categories/"+str(id))
        else:
            return render_template("error.html",\
                error="Alakategorian lisäy ei onnistunut")

@app.route("/categories/<int:id>/remove", methods=["POST"])
def category_remove(id):
    if categories.category_remove(id):
        return redirect("/categories")
    return render_template("error.html",\
        error="Kategorian poisto ei onnistunut")

@app.route("/categories/<int:id>/<int:sub_id>", methods=["POST"])
def subcategory_remove(id,sub_id):
    if categories.subcategory_remove(sub_id):
        return redirect("/categories/"+str(id))
    else:
        return render_template("error.html",\
            error="Alakategorian poisto ei onnistunut")

@app.route("/transactions", methods=["GET", "POST"])
def transactions_view():
    if request.method == "GET":
        categories_subcategories = categories.category_subcategory_list_all()
        transactions_list = transactions.list()
        return render_template("transactions.html",\
             categories_subcategories=categories_subcategories, transactions_list=transactions_list)
    if request.method == "POST":
        subcategory_id = request.form["category_subcategory"]
        amount = request.form["amount"]
        description = request.form["description"]
        file = request.files["file"]
        data = file.read()
        name = file.filename
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if transactions.add(subcategory_id, amount, description, data, name):
            return redirect("/transactions")
        else:
            return render_template("error.html",\
                error="Tapahtuman lisäys ei onnistunut. Muistathan, että summa on pakollinen ja sen pitää olla luku. Lisäksi luokka pitää aina valita. ")

@app.route("/transactions/<int:id>", methods=["GET", "POST"])
def transaction_edit(id):
    if request.method == "GET":
        transaction = transactions.view_one(id)
        picture_id = transaction[4]
        visible = transaction[5]
        if visible == 0:
            picture_id = 0
        categories_subcategories = categories.category_subcategory_list_all()
        return render_template("transaction_single.html",\
             transaction=transaction, categories_subcategories=categories_subcategories, picture_id=picture_id)
    if request.method == "POST":
        subcategory_id = request.form["category_subcategory"]
        amount = request.form["amount"]
        description = request.form["description"]
        file = request.files["file"]
        file = file.read()
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if transactions.update(subcategory_id, amount, description, id, file):
            flash(f" Muokattu")
            return redirect("/transactions/"+str(id))
        else:
            return render_template("error.html",\
                error="Tapahtuman muokkaus ei onnistunut")

@app.route("/transactions/<int:id>/remove",methods=["GET", "POST"])
def transaction_remove(id):
    if transactions.remove(id):
        return redirect("/transactions")
    else:
        return render_template("error.html",\
            error="Tapahtuman poistaminen ei onnistunut")

@app.route("/budgets",methods=["GET", "POST"])
def budget_create():
    if request.method == "GET":
        years = budgets.budget_years()
        return render_template("budgets.html", years=years)
    if request.method == "POST":
        year = request.form["year"]
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if budgets.create_budget(year):
            return redirect("/budgets")
        else:
            return render_template("error.html",\
                error="Budjetin luonti ei onnistunut. Muitstathan, että budjetti pitää olla vuosiluku ja ensimmäinen mahdollinen budjettivuosi on kuluvaa vuotta edeltävä vuosi ja viimeinen kuluva vuosi + 9 vuotta.")

@app.route("/budgets/<int:year>",methods=["GET", "POST"])
def budget_edit(year):
    if request.method == "GET":
        year_budget = budgets.budget_list(year)
        sums = budgets.budget_sum(year)
        return render_template("budget_year.html", year=year, year_budget=year_budget, sums=sums)
    if request.method == "POST":
        budget_ids = request.form.getlist("budget_id")
        amounts = request.form.getlist("amount")
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if budgets.budget_update(budget_ids,amounts):
            year = int(year)
            return redirect("/budgets/"+str(year))
        else:
            return render_template("error.html",\
                error="Budjetin päivittäminen ei onnistunut")

@app.route("/summary")
def summary_result():
    try:
        month_from = request.args["month_from"]
        year_from =request.args["year_from"]
        month_to = request.args["month_to"]
        year_to =request.args["year_to"]
        time_from = summary.set_days(month_from,year_from,month_to,year_to)[0]
        time_to = summary.set_days(month_from,year_from,month_to,year_to)[1]
        monthly_result = summary.monthly(time_from,time_to)
        total = summary.total_sum(time_from,time_to)
        by_categories = summary.by_categories(time_from,time_to)
        years = transactions.all_years()
        months = []
        for i in range(1,13):
            months.append(i)
        return render_template("summary.html",\
            monthly_result=monthly_result, total=total, by_categories=by_categories, time_from=time_from, time_to=time_to, years=years, months=months)
    except:
        years = transactions.all_years()
        months = []
        for i in range(1,13):
            months.append(i)
        return render_template("summary.html",\
            monthly_result=[], total=[], time_from="", time_to="", years=years, months=months)

@app.route("/transactions/pictures/<int:id>/show")
def show(id): 
    picture = transactions.show_picture(id)
    return picture

@app.route("/transactions/<int:id>/picture/remove",methods=["POST"])
def remove_picture(id):
    if transactions.picture_remove(id):
        return redirect("/transactions/"+str(id))
    else:
        return render_template("error.html", error="Kuitin poistaminen ei onnistunut")

@app.route("/search")
def view_search():
    try:
        time_from = request.args["time_from"]
        time_to = request.args["time_to"]
        if time_from == "":
            time_from = search.first_and_last()[0]
        else:
            time_from = time_from+" "+"00:00:00"
            time_from = datetime.strptime(time_from, "%Y-%m-%d %H:%M:%S")
        if time_to == "":
            time_to = search.first_and_last()[1]
        else:
            time_to = request.args["time_to"]+" "+"23:59:59"
            time_to = datetime.strptime(time_to, "%Y-%m-%d %H:%M:%S")
        if time_from > time_to:
            time_to = time_from + timedelta(days=30)
        query = request.args["query"]
        transaction_list = search.find(time_from, time_to,query)
        if query == "":
            query = "ei hakusanaa"
        return render_template("search.html", \
            transaction_list=transaction_list, time_from=time_from, time_to=time_to, query=query)
    except:
        return render_template("search.html",\
            transaction_list=[], time_from="", time_to="", query="")
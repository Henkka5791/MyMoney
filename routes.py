from app import app
from flask import redirect, render_template, request, session
import accounts
import category

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
        incomes = category.income_categories()
        outcomes = category.outcome_categories()
        return render_template("categories.html",incomes = incomes, outcomes = outcomes)
    if request.method == "POST":
        name = request.form["name"]
        outcome = request.form["outcome"]
        if category.add_category(name,outcome):
            return redirect("/categories")
        else:
            return render_template("categories.html",error_message="Kategorian lisääminen ei onnistunut")

@app.route("/categories/<int:id>",methods=["GET","POST"])
def subcategory_view(id):
    if request.method == "GET":
        subcategory_list = category.subcategory_list(id)
        name = category.category_name(id)
        return render_template("subcategory.html", subcategory_list=subcategory_list, name=name, id=id)
    if request.method == "POST":
        name = request.form["name"]
        category_id = id
        if category.add_subcategory(name,category_id):
            return redirect("/categories/"+str(id))
        else:
            return render_template("error.html", error="Alakategorian lisäy ei onnistunut")

@app.route("/categories/<int:id>/remove",methods=["POST"])
def category_remove(id):
    if category.category_remove(id):
        return redirect("/categories")
    return render_template("error.html", error="Kategorian poisto ei onnistunut")

@app.route("/categories/<int:id>/<int:sub_id>",methods=["POST"])
def subcategory_remove(id,sub_id):
    if category.subcategory_remove(sub_id):
        return redirect("/categories/"+str(id))
    else:
        return render_template("error.html", error="Alakategorian poisto ei onnistunut")

@app.route("/transactions", methods=["GET","POST"])
def transaction_view():
    if request.method == "GET":
        categories_subcategories = category.category_subcategory_list_all()
        return render_template("transactions.html",categories_subcategories = categories_subcategories)
    if request.method == "POST":
        name = request.form["category_subcategory"]
        amount = request.form["amount"]
        description = request.form["description"]
        print(amount,name,description)
        return redirect("/transactions")
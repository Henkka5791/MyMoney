from app import app
from flask import redirect, render_template, request, session
import accounts

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
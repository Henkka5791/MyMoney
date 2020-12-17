from flask import Flask
from flask import redirect, render_template, request

app = Flask(__name__)

import routes

@app.route("/")
def index():
    return render_template("index.html")
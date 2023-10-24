from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/notes")
@login_required
def notes():
    return render_template("notes.html", user=current_user)

@views.route("/calc", methods=['POST', 'GET'])
def calc():
    return render_template("calc.html", user=current_user)

@views.route("/orders")
@login_required
def orders():
    return render_template("orders.html", user=current_user)
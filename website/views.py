from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/signup")
def signup():
    return render_template("signup.html")
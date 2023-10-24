from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This user already exists', category='error')
        elif len(email) < 4:
            flash('Email must be greater that 3 charachters', category='error')
        elif len(firstname) < 2:
            flash('First name must be greater that 1 charachters', category='error')
        elif len(lastname) < 2:
            flash('Last name must be greater that 1 charachters', category='error')
        elif password != password2:
            flash('password must match', category='error')
        elif len(password) < 3:
            flash('Password must be greater that 2 charachters', category='error')
        else:
            new_user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            
            flash('Account created', category="success")
            return redirect(url_for('views.home'))
               
    return render_template("signup.html", user=current_user)

@auth.route("/login", methods=["GET", "POST"])
def log_in():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in succesfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.notes'))
            else:
                flash('Incorrect password, try again', category='error')
        else:
            flash('User does not exist', category='error')
                

    return render_template("login.html", user=current_user)

@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.log_in"))
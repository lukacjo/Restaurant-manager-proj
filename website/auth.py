from flask import Blueprint, render_template, request, flash, redirect


auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        
        
        if len(email) < 4:
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
            flash('Account created!', category='success')
        
    return render_template("signup.html")


@auth.route("/login", methods=['POST', 'GET'])
def login():
    return render_template("login.html")
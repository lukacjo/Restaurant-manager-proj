from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint("views", __name__)

@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/notes", methods=['POST', 'GET']) 
@login_required
def notes():
    if request.method == 'POST': 
        title = request.form.get('title') 
        note = request.form.get('note') # Bierze note i title z htmla

        title = title.capitalize()
        if len(note) < 1:
            flash('Note is too short!', category='error') 
        if len(title) < 1:
            flash('Title is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id, title=title)  
            db.session.add(new_note) # dodawanie notatki do bazydanych
            db.session.commit()
            flash('Note added!', category='success')
            
    return render_template("notes.html", user=current_user)

@views.route("/calc", methods=['POST', 'GET'])
def calc():
    return render_template("calc.html", user=current_user)

@views.route("/orders")
@login_required
def orders():
    return render_template("orders.html", user=current_user)
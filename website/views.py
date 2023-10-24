from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

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
            db.session.add(new_note) # Dodawanie notatki do bazy danych
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

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})
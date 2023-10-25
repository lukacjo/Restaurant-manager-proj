from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, SearchForm
from . import db
import json
from datetime import datetime

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

@views.route('/edit_note/<int:id>', methods=['POST', 'GET'])
@login_required
def get_note(id):
    old_note = Note.query.get_or_404(id)
    if old_note:
        if old_note.user_id == current_user.id:
            old_title = old_note.title
            old_data=old_note.data
            old_date=old_note.date_now
            if request.method == 'POST': 
                title = request.form.get('title') 
                note_text = request.form.get('note') 
                title = title.capitalize()
                if len(note_text) < 1:
                    flash('Note is too short!', category='error') 
                if len(title) < 1:
                    flash('Title is too short!', category='error') 
                else:
                    db.session.delete(old_note) # usuwam starą notatkę
                    new_note = Note(data=note_text, user_id=current_user.id, title=title, id=old_note.id, date_now=old_date)  # ustalam jakie dane ma mieć nowa notatka, zostawiając stare id
                    db.session.add(new_note)  # dodaję nową notatkę
                    db.session.commit()
                    flash('Note edited!', category='success')
                    return redirect(url_for('views.get_note', id=new_note.id))
            
            return render_template("edit_note.html", note=old_note, user=current_user, title=old_title, data=old_data)
    
    

@views.context_processor
def base():
    form = SearchForm()
    return dict(form=form)

@views.route('/search', methods=['POST', 'GET'])
def search():
    form = SearchForm()
    notes=Note.query
    user=current_user
    
    if form.validate_on_submit():
        searched = form.searched.data
        notes = notes.filter(Note.data.like('%' + searched + '%'))
        notes = notes.filter(Note.user_id==user.id)
        notes = notes.order_by(Note.id).all()
        
        if len(searched) < 1:
            flash('Search cant be empty', category='error')
        else:
            return render_template("search.html", form=form, searched=searched,user=user, notes=notes)
        
@views.route("/menu")
def menu():
    return render_template("menu.html", user=current_user)
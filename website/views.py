from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, SearchForm, Prod
from . import db
import json
from datetime import datetime
import mysql.connector

# connecuje się do bazy danych zeby usunąc wszystkie pojawienia się jednego produktu
mydb = mysql.connector.connect(
    host = "localhost",
    user="root",
    passwd = "restaurantmanager"
    #,auth_plugin='mysql_native_password'
)

views = Blueprint("views", __name__) # uycie wcześniejszego blueprinta

@views.route("/")
def home():
    return render_template("menu.html", user=current_user)

# notatki
@views.route("/notes", methods=['POST', 'GET']) 
@login_required # wymaga bycia zalogowanym
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
            new_note = Note(data=note, user_id=current_user.id, title=title)  # wsadzam dane do wczesniej przygotowanego modelu eby potem poszło do bazy naych
            db.session.add(new_note) # Dodawanie notatki do bazy danych
            db.session.commit()
            flash('Note added!', category='success')
            
    return render_template("notes.html", user=current_user)

# miejsce na kalulator
@views.route("/calc", methods=['POST', 'GET'])
def calc():
    return render_template("calc.html", user=current_user)

# zamówienia
@views.route("/orders", methods=['POST', 'GET'])
@login_required
def orders():
    if request.method == 'POST': 
        prod = request.form.get('prod_name')  # Bierze  produkt z htmla
        mycursor = mydb.cursor() # ustawiam kursor
        mycursor.execute("USE `managerdatabase`;") # w ten sposob zaczynam działac na konkretnej bazie danych
            
        sql = "DELETE FROM prod WHERE food = '%s';"  %prod # usuwam wszystkie pokazania sie danego rpoduktu przy uyciu skłądni sqla
        mycursor.execute(sql) # executuje
        mydb.commit()   

        flash('Product deleted!', category='success')
        return redirect("/orders")
    else:
        prod = Prod.query

        sum_of_prod = {} # dict w którym bede trzymać wszystkie produkty ale tylko raz i sumując ile ich łącznie jest
    
        for product in prod: # tą petla wsadzam rzeczy do dicta sum_of_prod
            if product.food in sum_of_prod:
                sum_of_prod[product.food] += product.qty
            else:
                sum_of_prod[product.food] = product.qty
        return render_template("orders.html", user=current_user, prod=prod, sum_of_prod=sum_of_prod)

@views.route('/delete-note', methods=['POST']) # do usuwania notatek
def delete_note():
    note = json.loads(request.data) # ładuje dane wysłane wczesniej przez JS z notes.html
    noteId = note['noteId'] # pobieram id z htmla
    note = Note.query.get(noteId) # a teraz wyszukuje na podstawie tego id w modelu
    if note:
        if note.user_id == current_user.id: # usuwam tylko jeeli id usera i current usera sie zgadza
            db.session.delete(note) # usuwam
            db.session.commit()
    return jsonify({}) # musze tak zwrócić chyba dlatego ę to potem znowu do JSa idzie

@views.route('/delete-order', methods=['POST']) # tak samo jak z notatkami tylko na produkcie dla jednego zamówienia a nie eby usunąć wszystkie
def delete_order():
    prod = json.loads(request.data)
    prodId = prod['prodId']
    prod = Prod.query.get(prodId)
    if prod:
        db.session.delete(prod)
        db.session.commit()
    return jsonify({})

@views.route('/edit_note/<int:id>', methods=['POST', 'GET']) # tu edituje notatki i uywam do tego id w linku
@login_required
def get_note(id):
    old_note = Note.query.get_or_404(id) # biore notatke na podstawie id
    if old_note:
        if old_note.user_id == current_user.id:
            old_title = old_note.title # rozdzielam sobie
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
        notes = notes.filter(Note.data.like('%' + searched + '%')) # wyszukuje notatke taka która jest podobna
        notes = notes.filter(Note.user_id==user.id) # eby sie zgadzało id
        notes = notes.order_by(Note.id).all() # ustalam jaki order
        
        if len(searched) < 1:
            flash('Search cant be empty', category='error')
        else:
            return render_template("search.html", form=form, searched=searched,user=user, notes=notes)
        
@views.route("/menu",methods=['POST', 'GET'])
def menu():
    if request.method == 'POST': 
        qty = request.form.get('qty') 
        prod = request.form.get('prod_name')  # Bierze qty i produkt z htmla
        if qty == None:
            flash('Quantity cant be empty', category='error')
        else:
            new_ord = Prod(qty=qty, food=prod)  
            db.session.add(new_ord) # Dodawanie notatki do bazy danych
            db.session.commit()
            flash('Product added!', category='success')
    return render_template("menu.html", user=current_user)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db" # ustawienei nazwy bazy danych

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'eh2WGSwY@HwO$!S!j32EM*9$36zKJCyvrvu#fRVV3rgs$3@H&whPGXwknMyW#qypW%E#D8yhTPDq$m##Ho6wUkNdIeuWozI8dZM' # secret key jest tu widoczny bo jest to tylko do portfolio inaczej byłby ukryty ze względów bezpieczeństwa, moze jeszcze tym sie zajmę ale zobaczę 
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 
    db.init_app(app)
   
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    from .models import User, Note 
    
    with app.app_context():
        db.create_all()
    

    return app


from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'eh2WGSwY@HwO$!S!j32EM*9$36zKJCyvrvu#fRVV3rgs$3@H&whPGXwknMyW#qypW%E#D8yhTPDq$m##Ho6wUkNdIeuWozI8dZM' # secret key jest tu widoczny bo jest to tylko do portfolio inaczej byłby ukryty ze względów bezpieczeństwa, moze jeszcze tym sie zajmę ale zobaczę 
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
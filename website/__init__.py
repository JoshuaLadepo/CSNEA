from flask import Flask
from .auth import auth
from .user_dashboard import home
from .admin_dashboard import admin

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"]= "CS_NEA"

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    app.register_blueprint(admin,url_prefix='/')
    return app

    

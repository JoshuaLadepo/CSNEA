from flask import Blueprint , render_template , request , redirect, url_for , flash , session

login = Blueprint("Login",__name__)
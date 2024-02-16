
from flask import Blueprint, render_template


main = Blueprint('main', __name__)

@main.route("/")
@main.route("/login")
def home():
    return render_template("login/login.html")

@main.route("/register")
def register():
    return render_template("login/register.html")

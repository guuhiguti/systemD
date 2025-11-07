from flask import Blueprint, render_template, session, redirect, url_for

home_route = Blueprint('home', __name__)

@home_route.route('/')
def home():
    usuario = session.get("usuario")
    if not usuario:
        return redirect(url_for("auth.login"))
    return render_template("home.html", usuario=usuario)

@home_route.route('/about')
def about():
    return render_template('landing_page.html')


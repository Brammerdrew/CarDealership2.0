from flask import render_template
from app import app
from flask_login import current_user
from models import User 

@app.route("/")
def home_page():
    return render_template('home.html', current_user=current_user)

@app.route('/inventory')
def inventory_page():
    return render_template('inventory.html', current_user=current_user)

@app.route('/profile')
def profile():
    return render_template('profile.html', current_user=current_user)
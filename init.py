from flask import Flask, render_template, url_for, flash, redirect
from forms import SignIn, SignUp
from models import User, Car

app = Flask(__name__)


app.app_context().push()
import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    '''
        set Config variables for the flask app
        useing Enviroment variables where available.
        Otherwise, create the config variable if not done already
    '''
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Insert text here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_NOTIFICATIONS = False

app.config.from_object(Config)

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route('/inventory')
def inventory_page():
    return render_template('inventory.html')

@app.route("/signup", methods=['GET', 'POST'])
def signup_page():
    form = SignUp()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', "success")
        return redirect(url_for('home_page'))
    return render_template('signup.html', form=form)

@app.route("/signin", methods=['GET', 'POST'])
def signin_page():
    form = SignIn()
    return render_template('signin.html', form=form)
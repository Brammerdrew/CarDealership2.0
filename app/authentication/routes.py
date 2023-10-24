from forms import SignIn, SignUp
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, User
from flask_login import login_user, current_user, logout_user, login_required
from app import bcrypt


auth = Blueprint('auth', __name__, template_folder='auth_templates')



@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SignUp()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('auth.signin'))
    return render_template('signup.html', current_user=current_user, form=form)

@auth.route("/signin", methods=['GET', 'POST'])
def signin():
    form = SignIn()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(user.password , form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home_page'))
        else:
            flash(f'Login Unsuccessful. Please check email and password', "danger")
    return render_template('signin.html', current_user=current_user, form=form)

@auth.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for('home_page'))
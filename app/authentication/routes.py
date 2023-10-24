from forms import SignIn, SignUp
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, User, check_password_hash
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
  


auth = Blueprint('auth', __name__, template_folder='auth_templates')



@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    form = SignUp()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            
            user = User(first_name, last_name, email, password, g_auth_verify=False)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.first_name.data}!', 'success')
            return redirect(url_for('auth.signin'))
    except:
        raise Exception("Invalid Form Data: Please Check Your Form")
    return render_template('signup.html', form=form)

@auth.route("/signin", methods=['GET', 'POST'])
def signin():
    form = SignIn()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)
            
            user = User.query.filter(User.email==email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('You have successfully logged in.', 'success')
                return redirect(url_for('site.home_page'))
    except:
        raise Exception("Invalid Form Data: Please Check Your Form")
    return render_template('signin.html', form=form)

@auth.route("/signout")
def signout():
    logout_user()
    return redirect(url_for('site.home_page'))
from flask import render_template, Blueprint, url_for, flash, redirect, request
from forms import UpdateProfile
from flask_login import current_user
from flask_login import login_required
from models import db, User




site = Blueprint('site', __name__, template_folder='site_templates')


@site.route("/")
def home_page():
    return render_template('home.html')

@site.route('/inventory')
def inventory_page():
    return render_template('inventory.html')



@site.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfile()
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('site.profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.email.data = current_user.email
    return render_template('profile.html',  form=form, name=current_user.first_name, user=current_user)
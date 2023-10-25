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
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
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
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', image_file=image_file, form=form, name=current_user.first_name, user=current_user)
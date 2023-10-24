from flask import render_template, Blueprint, url_for


site = Blueprint('site', __name__, template_folder='site_templates')


@site.route("/")
def home_page():
    return render_template('home.html')

@site.route('/inventory')
def inventory_page():
    return render_template('inventory.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')
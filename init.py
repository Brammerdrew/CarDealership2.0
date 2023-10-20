from flask import Flask, render_template
from config import Config

app = Flask(__name__)

app.config.from_object(Config)

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route('/inventory')
def inventory_page():
    return render_template('inventory.html')
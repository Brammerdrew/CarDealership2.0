from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

ma = Marshmallow()
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=True, nullable = False)
    last_name = db.Column(db.String(20), unique=True, nullable = False)
    email = db.Column(db.String(120), unique=True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    cars = db.relationship("Car", backref='seller', lazy=True)

    def __repr__(self):
        return f"User('{self.first_name}''{self.last_name}' ,'{self.email}', '{self.image_file}')"
    
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20))
    date_listed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    seller_id = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=False)

    def __repr__(self):
        return f"Car('{self.make}','{self.model}', '{self.year}','{self.color}','{self.image_file}','{self.date_listed}')"
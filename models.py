from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import uuid
from flask_marshmallow import Marshmallow



db = SQLAlchemy()
loginManager = LoginManager()
ma = Marshmallow()

@loginManager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(20), nullable = False)
    last_name = db.Column(db.String(50), nullable = False)  
    email = db.Column(db.String(120), unique=True, nullable = False)
    password = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    token = db.Column(db.String, default = '', unique = True)
    cars = db.relationship("Car", backref='seller', lazy=True)
    g_auth_verify = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, g_auth_verify=False):
        self.first_name = first_name.title()
        self.last_name = last_name.title()
        self.id = self.set_id()
        self.email = email.lower()
        self.password = self.set_password(password)
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify
    
    def set_token(self, length):
       return secrets.token_hex(length)
        
    def set_id(self):
        return str(uuid.uuid4())
        
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f"User('{self.first_name}' '{self.last_name}', '{self.email}')"
    
class Car(db.Model):
    id = db.Column(db.String, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    date_listed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    seller_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, make, model, year, color, price, mileage,  seller_id):
        self.make = make
        self.id = self.get_id()
        self.model = model
        self.year = year
        self.price = price
        self.mileage = mileage
        self.color = color
        self.seller_id = seller_id
        self.date_listed = datetime.utcnow()
    
    def get_id(self):
        return (secrets.token_urlsafe())
    

    def __repr__(self):
        return f"Car('{self.make}','{self.model}', '{self.year}','{self.color}','{self.date_listed}', '{self.price}', '{self.mileage}')"
    
class CarSchema(ma.Schema):
    class Meta:
        fields = ('id', 'make', 'model', 'year', 'color', 'mileage', 'price' 'date_listed', 'seller_id')


car_schema = CarSchema()
cars_schema = CarSchema(many=True)

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from models import db, User, Car, car_schema, cars_schema, loginManager
from helpers import token_required
from forms import PostCar
from flask_login import current_user, login_required


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/inventory', methods=['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    color = request.json['color']
    price = request.json['price']
    mileage = request.json['mileage']
    image_file = request.json['image_file']
    seller_id = current_user_token.id

    car = Car(make, model, year, color, image_file,price,mileage, seller_id=seller_id)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename) 
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) 
#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)
#     return picture_fn

# @api.route('/inventory', methods=['POST'])
# @token_required
# def post_car(current_user_token):
#     form = PostCar()
#     if form.validate_on_submit():
#         if form.image_file.data:
#             picture_file = save_picture(form.image_file.data)
#             current_user.image_file = picture_file
#         make = form.make.data
#         model = form.model.data
#         year = form.year.data
#         color = form.color.data
#         image_file = form.image_file.data
#         seller_id = current_user_token.id
#         car = Car(make, model, year, color, image_file, seller_id=seller_id)

#         db.session.add(car)
#         db.session.commit()

#         response = car_schema.dump(car)
#         return jsonify(response)
    

@api.route('/inventory', methods=['GET'])
@token_required
def get_car(current_user_token, id):
    current_user_token = current_user_token.token
    id = Car.query.get(id)
    response = car_schema.dump(id)
    return jsonify(response)

@api.route('/inventory', methods=['GET'])
#@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(seller_id=owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/inventory/<id>', methods=['PUT', 'POST'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)

    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.color = request.json['color']
    car.image_file = request.json['image_file']
    car.seller_id = current_user_token.id

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/inventory/<id>', methods=['DELETE'])
@token_required
def delete_car(current_user_token, id):
    id = request.json['id']
    current_user_token = current_user_token.token
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class StaffProfile(db.Model):
    """
    """
    __tablename__ = 'staff_profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(500), nullable=True)
    about = db.Column(db.String(1000), nullable=True)
    gender = db.Column(db.String(500), nullable=True)
    birth_date = db.Column(db.DateTime, nullable=True)
    avatar = db.Column(db.String(500), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)

    def __init__(self):
        self.updated_at = datetime.datetime.now()
        self.created_at = datetime.datetime.now()

class StaffAddress(db.Model):
    """
    """
    __tablename__ = 'staff_address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(500), nullable=True)
    district = db.Column(db.String(500), nullable=True)
    postal_code = db.Column(db.Integer, nullable=True)
    llong = db.Column(db.Integer, nullable=True)
    llat = db.Column(db.Integer, nullable=True)
    localized_city = db.Column(db.String(500), nullable=True)

    def __init__(self, city, district, postal_code, llong, llat, localized_city):
        self.city = city
        self.district = district
        self.postal_code = postal_code
        self.llong = llong
        self.llat = llat
        self.localized_city = localized_city

class StaffOrganizer(db.Model):
    """
    """
    __tablename__ = 'staff_organizer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    provider_id = db.Column(db.Integer, nullable=False)
    staff_id = db.Column(db.Integer, nullable=False)
    position = db.Column(db.String(50), nullable=True)
    email_account = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=True)  # joined/inactive/waiting
    updated_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)

    def __init__(self):
        self.updated_at = datetime.datetime.now()
        self.created_at = datetime.datetime.now()
        self.status = 'waiting'
        self.position = 'staff'

class StaffSkill(db.Model):
    """
    """
    __tablename__ = 'staff_skill'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer, nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)

    updated_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)

    def __init__(self):
        self.updated_at = datetime.datetime.now()
        self.created_at = datetime.datetime.now()

class StaffService(db.Model):
    __tablename__ = 'staff_service'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    staff_id = db.relationship('StaffProfile', lazy=True)
    price = db.Column(db.BigInteger, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    
    def __init__(self):
        self.updated_at = datetime.datetime.now()
        self.created_at = datetime.datetime.now()
    
class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    staff_id = db.relationship('StaffProfile', lazy=True)
    user_id = db.relationship('UserProfile', lazy=True)
    service_id = db.relationship('StaffService', lazy=True)
    status = db.Column(db.String(100), nullable=False)
    totalPrice = db.Column(db.BigInteger, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    
    def __init__(self):
        self.updated_at = datetime.datetime.now()
        self.created_at = datetime.datetime.now()
        
class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # account_id = db.Column(db.Integer, nullable=False)
    # email_account = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    gender = db.Column(db.String(500), nullable=True)
    birth_date = db.Column(db.DateTime, nullable=True)
    photo = db.Column(db.String(500), nullable=True)
    phone = db.Column(db.String(500), nullable=True)
    zip_code = db.Column(db.String(500), nullable=True)
    city = db.Column(db.String(500), nullable=True)
    district = db.Column(db.String(500), nullable=True)
    identity_id = db.Column(db.String(50), nullable=True, default=None)
    description = db.Column(db.String(500), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    addresses = db.relationship('UserAddress', backref='user_profile', lazy=True)

    def __init__(self, account_id, full_name, gender, birth_date, photo, phone, zip_code, city, district,
                 description, last_update, identity_id=None):
        self.account_id = account_id
        self.full_name = full_name
        self.gender = gender
        self.birth_date = birth_date
        self.photo = photo
        self.phone = phone
        self.zip_code = zip_code
        self.district = district
        self.city = city
        self.description = description
        if identity_id:
            self.identity_id = identity_id
        self.updated_at = datetime.datetime.now()
        self.created_at = datetime.datetime.now()

class UserAddress(db.Model):
    __tablename__ = 'user_address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('user_profile.id'), nullable=False)
    city = db.Column(db.String(500), nullable=True)
    district = db.Column(db.String(500), nullable=True)
    apartment_number = db.Column(db.String(500), nullable=True)
    postal_code = db.Column(db.Integer, nullable=True)
    llong = db.Column(db.Float, nullable=True)
    llat = db.Column(db.Float, nullable=True)
    localized_city = db.Column(db.String(500), nullable=True)
    note = db.Column(db.String(500), nullable=True)

    def __init__(self, profile_id, city, district, apartment_number, postal_code, llong, llat, localized_city, note):
        self.profile_id = profile_id
        self.city = city
        self.district = district
        self.apartment_number = apartment_number
        self.postal_code = postal_code
        self.llong = llong
        self.llat = llat
        self.localized_city = localized_city
        self.note = note

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id,'username': self.username, 'email': self.email}
    
    
db.create_all()

#create a test route
@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)


# create a user
@app.route('/users', methods=['POST'])
def create_user():
  try:
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return make_response(jsonify({'message': 'user created'}), 201)
  except e:
    return make_response(jsonify({'message': 'error creating user'}), 500)

# get all users
@app.route('/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    return make_response(jsonify([user.json() for user in users]), 200)
  except e:
    return make_response(jsonify({'message': 'error getting users'}), 500)

# get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      return make_response(jsonify({'user': user.json()}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error getting user'}), 500)

# update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.username = data['username']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error updating user'}), 500)

# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error deleting user'}), 500)
from flask import Blueprint, request, abort
from init import db, bcrypt
from models.user import User, UserSchema
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

# This route is used to check if the user is logged in or not by checking if the JWT token is valid or not and returns the user's details if the token is valid or returns an error if the token is invalid
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        stmt = db.select(User).filter_by(email=request.json['email'])
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            return {'token': token, 'user': UserSchema(only=['email','name']).dump(user)}, 200
        else:
            return {'error': 'Invalid email or password'}, 401 # Unauthorized
    except KeyError:
        return {'error': 'Invalid email or password'}, 401 # Unauthorized

# This route is used to register a new user and returns the user's details if the registration is successful or returns an error if the registration is unsuccessful
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        user_details = UserSchema().load(request.json)
    except ValidationError as valdiation_error:
        return {'error': 'Validation Error', 'errors': valdiation_error.messages}, 400
    
    user = User.query.filter_by(email=user_details['email']).first()
    if user:
        return {'error': 'Email is already in use by another user.'}, 400
    
    hashed_password = bcrypt.generate_password_hash(user_details['password']).decode('utf-8')

    new_user = User(
        name = user_details['name'],
        email = user_details['email'],
        password = hashed_password,
        role = user_details['role'],
    )

    db.session.add(new_user)
    db.session.commit()

    return UserSchema(exclude=['password']).dump(new_user), 201

# This route is used to get all the users in the database and returns all the users if the user is an admin or returns an error if the user is not an admin
@auth_bp.route('/users', methods=['GET'])
def all_users():
    admin_required()
    stmt = db.select(User)
    users = db.session.scalars(stmt).all()
    if users:
        return UserSchema(many=True, exclude=['password']).dump(users)
    else: 
        return {'error': 'No users found.'}, 404 # Not found

# This route is used to get a specific user in the database and returns the user if the user is an admin or returns an error if the user is not an admin
@jwt_required()
def admin_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user:
        abort(400, 'User not found.')
    if not user.is_admin:
        abort(400, 'Admin required.')

# This route is used to get a specific user in the database and returns the user if the user is an admin or has the role "team" - returns an error if the user is not an admin
@jwt_required()
def admin_or_team_role_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user =db.session.scalar(stmt)
    if not user:
        abort(400, 'User not found.')
    if not (user.is_admin or user.role == 'team'):
        abort(400, 'Admin or Team can only perform this function.')
    return user

# This route is used to get a specific user in the database and returns the user if the user is an admin or has the role "driver" - returns an error if the user is not an admin
@jwt_required()
def admin_or_driver_role_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user =db.session.scalar(stmt)
    if not user:
        abort(400, 'User not found.')
    if not (user.is_admin or user.role == 'driver'):
        abort(400, 'Admin or Driver can only perform this function.')
    return user

# This route is used to get a specific user in the database and returns the user if the user is an admin or has the role "organizer" - returns an error if the user is not an admin

@jwt_required()
def admin_or_organizer_role_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user =db.session.scalar(stmt)
    if not user:
        abort(400, 'User not found.')
    if not (user.is_admin or user.role == 'organizer'):
        abort(400, 'Admin or Organizer can only perform this function.')
    return user
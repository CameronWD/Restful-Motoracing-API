from flask import Blueprint, request, abort
from init import db, bcrypt
from models.user import User, UserSchema
from marshmallow.exceptions import ValidationError
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        stmt = db.select(User).filter_by(email=request.json['email'])
        user = db.session.scalar(stmt)
        if user and bcrypt.check_password_hash(user.password, request.json['password']):
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            return {'token': token, 'user': UserSchema(only=['email','name']).dump(user)}, 200
        else:
            return {'error': 'Invalid email or password'}, 401
    except KeyError:
        return {'error': 'Invalid email or password'}, 401

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


@auth_bp.route('/users', methods=['GET'])
def all_users():
    stmt = db.select(User)
    users = db.session.scalars(stmt).all()
    return UserSchema(many=True, exclude=['password']).dump(users)

@jwt_required()
def admin_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if not user:
        abort(400, 'User not found.')
    if not user.is_admin:
        abort(400, 'Admin required.')

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
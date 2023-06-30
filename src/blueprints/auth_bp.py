from flask import Blueprint
from init import db, bcrypt
from models.user import User, UserSchema

auth_bp = Blueprint('auth', __name__)

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

    return UserSchema().dump(new_user), 201
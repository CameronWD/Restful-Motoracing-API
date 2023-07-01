from flask import Blueprint, request
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from models.user import User, UserSchema
from models.driver import Driver, DriverSchema
from blueprints.auth_bp import admin_or_driver_role_required
from flask_jwt_extended import get_jwt_identity, jwt_required

drivers_bp = Blueprint('driver', __name__, url_prefix='/drivers')

@drivers_bp.route('/')
def all_drivers():
    stmt = db.select(Driver)
    drivers = db.session.scalars(stmt).all()
    return DriverSchema(many=True).dump(drivers)

@drivers_bp.route('/<int:driver_id>')
def one_driver(driver_id):
    stmt = db.select(Driver).filter_by(id=driver_id)
    driver = db.session.scalar(stmt)
    if driver:
        return DriverSchema().dump(driver)
    else:
        return{'error': 'Driver not found.'}, 400

@drivers_bp.route('/', methods=['POST'])
def create_driver():
    current_user = admin_or_driver_role_required()

    exising_driver = Driver.query.filter_by(user_id=current_user.id).first()
    
    if exising_driver:
        return{'error': f'Driver already exists for this user. Please delete or update your current driver profile, {exising_driver.first_name} {exising_driver.last_name}'}, 400

    try:
        driver_details = DriverSchema().load(request.json)
    except ValidationError as valdiation_error:
        return {'error': 'Validation Error', 'errors': valdiation_error.messages}, 400

    driver = Driver(
        first_name = driver_details['first_name'],
        last_name = driver_details['last_name'],
        date_of_birth = driver_details['date_of_birth'],
        nationality = driver_details['nationality'],
        user_id = current_user.id
    )

    db.session.add(driver)
    db.session.commit()
    return DriverSchema().dump(driver), 201

@drivers_bp.route('/<int:driver_id>', methods=['PUT', 'PATCH'])
def update_driver(driver_id):
    current_user = admin_or_driver_role_required()

    stmt = db.select(Driver).filter_by(id=driver_id)
    driver = db.session.scalar(stmt)

    if not driver:
        return{'error': 'Driver not found.'}, 404
    
    if not (current_user.is_admin or current_user.id == driver.user_id):
        return{'error': 'Permission denied.'}, 403

    try:
        driver_details = DriverSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400
    
    if driver:
        driver.first_name = driver_details.get('first_name', driver.first_name)
        driver.last_name = driver_details.get('last_name', driver.last_name)
        driver.nationality = driver_details.get('nationality', driver.nationality)
        driver.date_of_birth = driver_details.get('date_of_birth', driver.date_of_birth)
        db.session.commit()
        return DriverSchema().dump(driver)


@drivers_bp.route('/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    current_user = admin_or_driver_role_required()

    stmt = db.select(Driver).filter_by(id=driver_id)
    driver = db.session.scalar(stmt)

    if not driver:
        return{'error': 'Driver not found.'}, 404
    
    if not (current_user.is_admin or current_user.id == driver.user_id):
        return{'error': 'Permission denied.'}, 403
    
    if driver:
        db.session.delete(driver)
        db.session.commit()
        return{'message': f'Driver {driver.first_name} {driver.last_name} successfully deleted.'}, 200
    else:
        return{'error': 'Driver not found.'}, 404
        

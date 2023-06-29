from flask import Blueprint, request
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from models.user import User, UserSchema
from models.team import Team, TeamSchema
from models.driver import Driver, DriverSchema
from models.driver import Driver, DriverSchema
from datetime import date

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
    try:
        driver_details = DriverSchema().load(request.json)
    except ValidationError as valdiation_error:
        return {'error': 'Validation Error', 'errors': valdiation_error.messages}, 400

    driver = Driver(
        first_name = driver_details['first_name'],
        last_name = driver_details['last_name'],
        date_of_birth = driver_details['date_of_birth'],
        nationality = driver_details['nationality']
    )

    db.session.add(driver)
    db.session.commit()
    return DriverSchema().dump(driver), 201

@drivers_bp.route('/<int:driver_id>', methods=['PUT', 'PATCH'])
def update_driver(driver_id):
    try:
        driver_details = DriverSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400

    stmt = db.select(Driver).filter_by(id=driver_id)
    driver = db.session.scalar(stmt)
    
    if driver:
        driver.first_name = driver_details.get('first_name', driver.first_name)
        driver.last_name = driver_details.get('last_name', driver.last_name)
        driver.nationality = driver_details.get('nationality', driver.nationality)
        driver.date_of_birth = driver_details.get('date_of_birth', driver.date_of_birth)
        db.session.commit()
        return DriverSchema().dump(driver)
    else:
        return{'error': 'Driver not found.'}, 404

@drivers_bp.route('/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    stmt = db.select(Driver).filter_by(id=driver_id)
    driver = db.session.scalar(stmt)
    if driver:
        db.session.delete(driver)
        db.session.commit()
        return{'message': f'Driver {driver_id} successfully deleted.'}, 200
    else:
        return{'error': 'Driver not found.'}, 404
        

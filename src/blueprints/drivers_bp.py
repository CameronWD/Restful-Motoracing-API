from flask import Blueprint, request
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from models.driver import Driver, DriverSchema
from blueprints.auth_bp import admin_or_driver_role_required
from utils import validate_schema, get_resource_or_404

drivers_bp = Blueprint('driver', __name__, url_prefix='/drivers')

@drivers_bp.route('/')
def all_drivers():
    stmt = db.select(Driver)
    drivers = db.session.scalars(stmt).all()
    if drivers:
        return DriverSchema(many=True).dump(drivers) 
    else:
        return{'error': 'No drivers found.'}, 404 # Not Found: The requested drivers resource does not exist.

@drivers_bp.route('/<int:driver_id>')
def one_driver(driver_id):
    driver = get_resource_or_404(db.select(Driver).filter_by(id=driver_id), 'Driver')
    return DriverSchema().dump(driver)

@drivers_bp.route('/', methods=['POST'])
def create_driver():
    current_user = admin_or_driver_role_required()
    driver_details = validate_schema(DriverSchema(), request.json)

    exising_driver = db.session.query(Driver).filter_by(user_id=current_user.id).first()
    if exising_driver:
        return{'error': f'Driver already exists for this user. Please delete or update your current driver profile for {exising_driver.first_name} {exising_driver.last_name}'}, 409

    driver = Driver(
        first_name = driver_details['first_name'],
        last_name = driver_details['last_name'],
        date_of_birth = driver_details['date_of_birth'],
        nationality = driver_details['nationality'],
        user_id = current_user.id
    )

    db.session.add(driver)
    db.session.commit()
    return DriverSchema().dump(driver), 201 # Created: The driver resource has been successfully created.

@drivers_bp.route('/<int:driver_id>', methods=['PUT', 'PATCH'])
def update_driver(driver_id):
    current_user = admin_or_driver_role_required()
    driver = get_resource_or_404(db.select(Driver).filter_by(id=driver_id), 'Driver')
    
    if not (current_user.is_admin or current_user.id == driver.user_id):
        return{'error': 'Permission denied.'}, 403 # Forbidden: The server understood the request, but is refusing to fulfill it.

    driver_details = validate_schema(DriverSchema(), request.json, partial=True)
    
   
    driver.first_name = driver_details.get('first_name', driver.first_name)
    driver.last_name = driver_details.get('last_name', driver.last_name)
    driver.nationality = driver_details.get('nationality', driver.nationality)
    driver.date_of_birth = driver_details.get('date_of_birth', driver.date_of_birth)
    db.session.commit()
    return DriverSchema().dump(driver)


@drivers_bp.route('/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    current_user = admin_or_driver_role_required()
    driver = get_resource_or_404(db.select(Driver).filter_by(id=driver_id), 'Driver')

    if not (current_user.is_admin or current_user.id == driver.user_id):
        return{'error': 'Permission denied.'}, 403 # Forbidden: The server understood the request, but is refusing to fulfill it.
    
    db.session.delete(driver)
    db.session.commit()
    return {}, 204 # No Content: The server successfully processed the request, but is not returning any content.
    
        

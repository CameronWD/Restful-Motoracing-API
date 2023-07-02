from flask import Blueprint, request
from init import db
from models.race import Race, RaceSchema
from datetime import date
from blueprints.auth_bp import admin_or_organizer_role_required
from utils import validate_schema, get_resource_or_404
from models.category import Category
from models.circuit import Circuit  

races_bp = Blueprint('race', __name__, url_prefix='/races')

# This route is used to get all the races in the database and returns all the races

@races_bp.route('/')
def all_races():
    stmt = db.select(Race)
    races = db.session.scalars(stmt).all()
    if races:
        return RaceSchema(many=True).dump(races)
    else:
        return{'error': 'No races found.'}, 404 # Not found

# GET /races/<race_id> - Returns a specific race from the database

@races_bp.route('/<int:race_id>')
def one_race(race_id):
    race = get_resource_or_404(db.select(Race).filter_by(id=race_id), 'Race')
    return RaceSchema().dump(race)

# POST /races - Creates a new race in the database and returns the new race. The user must be an admin or organizer to create a race.
@races_bp.route('/', methods=['POST'])
def create_race():
    current_user = admin_or_organizer_role_required()
    race_details = validate_schema(RaceSchema(), request.json)

    existing_race = db.session.query(Race).filter_by(date=race_details['date'], name=race_details['name']).first()
    if existing_race:
        return {'error': 'Race already exists.'}, 409  # Conflict: The race already exists and creates a conflict with the unique constraint.
    
    category = db.session.query(Category).filter_by(id=race_details['category_id']).first()
    if not category:
        return {'error': 'Category does not exist.'}, 400
    
    circuit = db.session.query(Circuit).filter_by(id=race_details['circuit_id']).first()
    if not circuit:
        return {'error': 'Circuit does not exist.'}, 400
    

    race = Race(
        name = race_details['name'],
        date = race_details['date'],
        circuit_id = race_details['circuit_id'],
        category_id = race_details['category_id'],
        user_id = current_user.id
    )

    db.session.add(race)
    db.session.commit()
    return RaceSchema().dump(race), 201
    
# PUT /races/<races_id> - Updates a specific race in the database and returns the updated race. The user must be an admin or organizer to update a race.  Organizer must own the race. 
@races_bp.route('/<int:race_id>', methods=['PUT', 'PATCH'])
def update_race(race_id):
    current_user = admin_or_organizer_role_required()
    race = get_resource_or_404(db.select(Race).filter_by(id=race_id), 'Race')

    if not (current_user.id == race.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this race.'}, 403 # Forbidden: The user is not authorized to update the race resource.
    
    race_details = validate_schema(RaceSchema(), request.json, partial=True)
        
    race.date = race_details.get('date', race.date)
    race.name = race_details.get('name', race.name)
    race.circuit_id = race_details.get('circuit_id', race.circuit_id)
    race.category_id = race_details.get('category_id', race.category_id)

    db.session.commit()
    return RaceSchema().dump(race)

# DELETE /races/<races_id> - Delete a specific race in the database and returns a 204. The user must be an admin or organizer who owns the race result. 
@races_bp.route('/<int:race_id>', methods=['DELETE'])
def delete_race(race_id):
    current_user = admin_or_organizer_role_required()
    race = get_resource_or_404(db.select(Race).filter_by(id=race_id), 'Race')

    if not (current_user.id == race.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this race.'}, 403

    db.session.delete(race)
    db.session.commit()
    return{}, 204
   

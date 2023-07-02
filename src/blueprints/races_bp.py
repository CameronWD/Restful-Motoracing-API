from flask import Blueprint, request
from init import db
from models.race import Race, RaceSchema
from datetime import date
from blueprints.auth_bp import admin_or_organizer_role_required
from utils import validate_schema, get_resource_or_404

races_bp = Blueprint('race', __name__, url_prefix='/races')

@races_bp.route('/')
def all_races():
    stmt = db.select(Race)
    races = db.session.scalars(stmt).all()
    if races:
        return RaceSchema(many=True).dump(races)
    else:
        return{'error': 'No races found.'}, 404 # Not found

@races_bp.route('/<int:race_id>')
def one_race(race_id):
    race = get_resource_or_404(db.select(Race).filter_by(id=race_id), 'Race')
    return RaceSchema().dump(race)

@races_bp.route('/', methods=['POST'])
def create_race():
    current_user = admin_or_organizer_role_required()
    race_details = validate_schema(RaceSchema(), request.json)

    existing_race = db.session.query(Race).filter_by(date=race_details['date'], name=race_details['name']).first()
    if existing_race:
        return {'error': 'Race already exists.'}, 409 # Conflict: The race already exists and creates a conflict with the unique constraint.

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

@races_bp.route('/<int:race_id>', methods=['DELETE'])
def delete_race(race_id):
    current_user = admin_or_organizer_role_required()
    race = get_resource_or_404(db.select(Race).filter_by(id=race_id), 'Race')

    if not (current_user.id == race.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this race.'}, 403

    db.session.delete(race)
    db.session.commit()
    return{}, 204
   

from flask import Blueprint, request
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from models.user import User, UserSchema
from models.race import Race, RaceSchema
from datetime import date
from blueprints.auth_bp import admin_or_organizer_role_required

races_bp = Blueprint('race', __name__, url_prefix='/races')

@races_bp.route('/')
def all_races():
    stmt = db.select(Race)
    races = db.session.scalars(stmt).all()
    return RaceSchema(many=True).dump(races)

@races_bp.route('/<int:race_id>')
def one_race(race_id):
    stmt = db.select(Race).filter_by(id=race_id)
    race = db.session.scalar(stmt)
    if race:
        return RaceSchema().dump(race), 200
    else:
        return{'error': 'Race not found.'}, 400

@races_bp.route('/', methods=['POST'])
def create_race():
    current_user = admin_or_organizer_role_required()
    existing_race = Race.query.filter_by(user_id=current_user.id).first()

    try:
        race_details = RaceSchema().load(request.json)
    except ValidationError as valdiation_error:
        return {'error': 'Validation Error', 'errors': valdiation_error.messages}, 400
    
    # A race can have the same name as another race, like "Tour de France", but can not have the same date. 
    # Therefore a race that is held every year for example, can still have the same name as the date will change 
    # every year. 

    existing_race = db.session.query(Race).filter_by(date=race_details['date'], name=race_details['name']).first()
    if existing_race:
        return {'error': 'Race already exists.'}, 400

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

    stmt = db.select(Race).filter_by(id=race_id)
    race = db.session.scalar(stmt)

    if not race:
        return{'error': 'Race not found.'}, 404
    if not (current_user.id == race.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this race.'}, 403
    try:
        race_details = RaceSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400
    
    existing_race = db.session.query(Race).filter_by(date=race_details['date']).first()
    if existing_race:
        return {'error': 'Race already exists.'}, 400
    
    if race:
        race.date = race_details.get('date', race.date)
        race.name = race_details.get('name', race.name)
        race.circuit_id = race_details.get('circuit_id', race.circuit_id)
        race.category_id = race_details.get('category_id', race.category_id)
        db.session.commit()
        return RaceSchema().dump(race)

@races_bp.route('/<int:race_id>', methods=['DELETE'])
def delete_race(race_id):
    current_user = admin_or_organizer_role_required()
    stmt = db.select(Race).filter_by(id=race_id)
    race = db.session.scalar(stmt)
    if not (current_user.id == race.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this race.'}, 403
    if race:
        db.session.delete(race)
        db.session.commit()
        return{}, 200
    else:
        return{'error': 'Race not found.'}, 404

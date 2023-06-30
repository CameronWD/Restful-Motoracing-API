from flask import Blueprint, request
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from models.user import User, UserSchema
from models.race import Race, RaceSchema
from datetime import date

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
    try:
        race_details = RaceSchema().load(request.json)
    except ValidationError as valdiation_error:
        return {'error': 'Validation Error', 'errors': valdiation_error.messages}, 400

    race = Race(
        name = race_details['name'],
        date = race_details['date'],
        circuit_id = race_details['circuit_id'],
        category_id = race_details['category_id']
    )

    db.session.add(race)
    db.session.commit()
    return RaceSchema().dump(race), 201
    

@races_bp.route('/<int:race_id>', methods=['PUT', 'PATCH'])
def update_race(race_id):
    try:
        race_details = RaceSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400
    
    stmt = db.select(Race).filter_by(id=race_id)
    race = db.session.scalar(stmt)

    if race:
        race.date = race_details.get('date', race.date)
        race.name = race_details.get('name', race.name)
        race.circuit_id = race_details.get('circuit_id', race.circuit_id)
        race.category_id = race_details.get('category_id', race.category_id)
        db.session.commit()
        return RaceSchema().dump(race)
    else:
        return{'error': 'Race not found.'}, 404

@races_bp.route('/<int:race_id>', methods=['DELETE'])
def delete_race(race_id):
    stmt = db.select(Race).filter_by(id=race_id)
    race = db.session.scalar(stmt)
    if race:
        db.session.delete(race)
        db.session.commit()
        return{'message': ' wow'}, 200
    else:
        return{'error': 'Race not found.'}, 404

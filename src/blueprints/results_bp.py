from flask import Blueprint, request
from init import db
from marshmallow.exceptions import ValidationError
from models.driver import Driver
from models.race import Race
from models.result import Result, ResultSchema
from blueprints.auth_bp import admin_or_organizer_role_required


results_bp = Blueprint('result', __name__, url_prefix='/results')

@results_bp.route('/')
def all_results():
    stmt=db.select(Result)
    results=db.session.scalars(stmt).all()
    if results:
        schema = ResultSchema(many=True, exclude=('driver','race',))
        return schema.dump(results)
    else:
        return{'error': 'No results found.'}, 404

@results_bp.route('/<int:result_id>')
def one_result(result_id):
    stmt=db.select(Result).filter_by(id=result_id)
    result=db.session.scalar(stmt)
    if result:
        schema = ResultSchema(exclude=('driver_id','race_id'))
        return schema.dump(result)
    else:
        return{'error': 'Result not found.'}, 400

@results_bp.route('/', methods=['POST'])
def create_result():
    current_user = admin_or_organizer_role_required()

    try:
        result_details = ResultSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400
    
    existing_result = db.session.query(Result).filter_by(race_id=result_details['race_id'], driver_id=result_details['driver_id']).first()
    if existing_result:
        return {'error': 'Result already exists.'}, 400
    
    race = Race.query.get(result_details['race_id'])
    if not race:
        return {'error': f'Race ID {result_details["race_id"]} not found.'}, 404
    
    driver = Driver.query.get(result_details['driver_id'])
    if not driver:
        return {'error': f'Driver ID {result_details["driver_id"]} not found.'}, 404

    result = Result(
        start_position = result_details['start_position'],
        end_position = result_details['end_position'],
        points = result_details['points'],
        race_id=result_details['race_id'],
        driver_id=result_details['driver_id'],
        user_id=current_user.id
    )

    db.session.add(result)
    db.session.commit()
    return ResultSchema().dump(result), 201

@results_bp.route('/<int:result_id>', methods=['PUT', 'PATCH'])
def update_result(result_id):
    current_user = admin_or_organizer_role_required()

    stmt = db.select(Result).filter_by(id=result_id)
    result = db.session.scalar(stmt)

    if not result:
        return {'error': f'Result ID {result_id} not found.'}, 404
    if not (current_user.is_admin or current_user.id == result.user_id):
        return {'error': 'You do not have permission to edit this result.'}, 403
    
    try:
        result_details = ResultSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400
    
    if 'race_id' in result_details:
        race = Race.query.get(result_details['race_id'])
        if not race:
            return{'error': f'Race ID {result_details["race_id"]} not found.'}, 404
    
    if 'driver_id' in result_details:
        driver = Driver.query.get(result_details['driver_id'])
        if not driver:
            return{'error': f'Driver ID {result_details["driver_id"]} not found.'}, 404

    result.start_position = result_details.get('start_position', result.start_position)
    result.end_position = result_details.get('end_position', result.end_position)
    result.points = result_details.get('points', result.points)
    result.race_id = result_details.get('race_id', result.race_id)
    result.driver_id = result_details.get('driver_id', result.driver_id)

    db.session.commit()
    return ResultSchema().dump(result)


@results_bp.route('/<int:result_id>', methods=['DELETE'])
def delete_result(result_id):
    current_user = admin_or_organizer_role_required()

    stmt = db.select(Result).filter_by(id=result_id)
    result = db.session.scalar(stmt)

    if not result:
        return {'error': f'Result ID {result_id} not found.'}, 404
    if not (current_user.is_admin or current_user.id == result.user_id):
        return {'error': 'You do not have permission to edit this result.'}, 403
    
    if result:
        db.session.delete(result)
        db.session.commit()
        return{}, 200
   
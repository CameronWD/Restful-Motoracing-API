from flask import Blueprint, request
from init import db
from marshmallow.exceptions import ValidationError
from models.driver import Driver
from models.race import Race
from models.result import Result, ResultSchema


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
    try:
        result_details = ResultSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400
    
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
        race=race,
        driver=driver
    )

    db.session.add(result)
    db.session.commit()
    return ResultSchema().dump(result), 201

@results_bp.route('/<int:result_id>', methods=['PUT', 'PATCH'])
def update_result(result_id):
    try:
        result_details = ResultSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400
    
    stmt = db.select(Result).filter_by(id=result_id)
    result = db.session.scalar(stmt)

    if not result:
        return {'error': f'Result ID {result_id} not found.'}, 404
    
    if 'race_id' in result_details:
        race = Race.query.get(result_details['race_id'])
        if not race:
            return{'error': f'Race ID {result_details["race_id"]} not found.'}, 404
    
    if 'driver_id' in result_details:
        driver = Driver.query.get(result_details['driver_id'])
        if not driver:
            return{'error': f'Driver ID {result_details["driver_id"]} not found.'}, 404

    if result:
        result.start_position = result_details.get('start_position', result.start_position)
        result.end_position = result_details.get('end_position', result.end_position)
        result.points = result_details.get('points', result.points)
        result.race_id = result_details.get('race_id', result.race_id)
        result.driver_id = result_details.get('driver_id', result.driver_id)
        db.session.commit()
        return ResultSchema().dump(result)

    else:
        return{'error': 'Result not found.'}, 404

@results_bp.route('/<int:result_id>', methods=['DELETE'])
def delete_result(result_id):
    stmt = db.select(Result).filter_by(id=result_id)
    result = db.session.scalar(stmt)
    if result:
        db.session.delete(result)
        db.session.commit()
        return{'details': f'Result {result.id} successfully deleted'}, 200
    else:
        return{'error': 'Result not found.'}, 404
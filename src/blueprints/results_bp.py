from flask import Blueprint, request
from init import db
from models.driver import Driver
from models.race import Race
from models.result import Result, ResultSchema
from blueprints.auth_bp import admin_or_organizer_role_required
from utils import validate_schema, get_resource_or_404


results_bp = Blueprint('result', __name__, url_prefix='/results')

# GET /results - Returns a list of all results.

@results_bp.route('/')
def all_results():
    stmt=db.select(Result)
    results=db.session.scalars(stmt).all()
    if results:
        schema = ResultSchema(many=True, exclude=('driver','race',))
        return schema.dump(results)
    else:
        return{'error': 'No results found.'}, 404 # Not Found: The requested results resource does not exist.
    
# GET /results/<result_id> - Returns a specific result from the database
@results_bp.route('/<int:result_id>')
def one_result(result_id):
    result = get_resource_or_404(db.select(Result).filter_by(id=result_id), 'Result')
    return ResultSchema().dump(result)

# POST /results - Creates a new result in the database and returns the new result. The user must be an admin or organizer to create a result.
@results_bp.route('/', methods=['POST'])
def create_result():
    current_user = admin_or_organizer_role_required()
    result_details = validate_schema(ResultSchema(), request.json)
    
    existing_result = db.session.query(Result).filter_by(race_id=result_details['race_id'], driver_id=result_details['driver_id']).first()
    if existing_result:
        return {'error': 'Result already exists.'}, 409 # Conflict: The result already exists and creates a conflict with the unique constraint.
    
    race = Race.query.get(result_details['race_id'])
    if not race:
        return {'error': f'Race ID {result_details["race_id"]} not found.'}, 404 # Not Found: The requested race resource does not exist.
    
    driver = Driver.query.get(result_details['driver_id'])
    if not driver:
        return {'error': f'Driver ID {result_details["driver_id"]} not found.'}, 404 # Not Found: The requested race resource does not exist.

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
    return ResultSchema().dump(result), 201 # Created: The result resource has been successfully created.

# PUT /results/<result_id> - Updates a specific result in the database and returns the updated result. The user must be an admin or organizer to update a result. Organizers can only update results they created.
@results_bp.route('/<int:result_id>', methods=['PUT', 'PATCH'])
def update_result(result_id):
    current_user = admin_or_organizer_role_required()
    result = get_resource_or_404(db.select(Result).filter_by(id=result_id), 'Result')

    if not (current_user.is_admin or current_user.id == result.user_id):
        return {'error': 'You do not have permission to edit this result.'}, 403 # Forbidden: The user is not authorized to update the result resource.

    result_details = validate_schema(ResultSchema(), request.json)
    
    if 'race_id' in result_details:
        race = Race.query.get(result_details['race_id'])
        if not race:
            return{'error': f'Race ID {result_details["race_id"]} not found.'}, 404  # Not Found: The requested race resource does not exist.
    
    if 'driver_id' in result_details:
        driver = Driver.query.get(result_details['driver_id'])
        if not driver:
            return{'error': f'Driver ID {result_details["driver_id"]} not found.'}, 404 # Not Found: The requested driver resource does not exist.

    result.start_position = result_details.get('start_position', result.start_position)
    result.end_position = result_details.get('end_position', result.end_position)
    result.points = result_details.get('points', result.points)
    result.race_id = result_details.get('race_id', result.race_id)
    result.driver_id = result_details.get('driver_id', result.driver_id)

    db.session.commit()
    return ResultSchema().dump(result)

# DELETE /results/<result_id> - Deletes a specific result from the database. The user must be an admin or organizer to delete a result. Organizers can only delete results they created.
@results_bp.route('/<int:result_id>', methods=['DELETE'])
def delete_result(result_id):
    current_user = admin_or_organizer_role_required()
    result = get_resource_or_404(db.select(Result).filter_by(id=result_id), 'Result')

    if not (current_user.is_admin or current_user.id == result.user_id): 
        return {'error': 'You do not have permission to edit this result.'}, 403 # Forbidden: The user is not authorized to update the result resource.

    db.session.delete(result)
    db.session.commit()
    return{}, 204  # No Content: The result has been successfully deleted.
   
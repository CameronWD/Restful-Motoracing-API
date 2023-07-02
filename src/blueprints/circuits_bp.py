from flask import Blueprint, request
from init import db
from marshmallow.exceptions import ValidationError
from models.user import User, UserSchema
from models.circuit import Circuit, CircuitSchema
from blueprints.auth_bp import admin_or_organizer_role_required

circuits_bp = Blueprint('circuit', __name__, url_prefix='/circuits')

@circuits_bp.route('/')
def all_circuits():
    stmt=db.select(Circuit)
    circuits=db.session.scalars(stmt).all()
    if circuits:
        return CircuitSchema(many=True).dump(circuits)
    else:
        return{'error': 'No circuits found.'}, 404 # Not Found: The requested circuits resource does not exist.

@circuits_bp.route('/<int:circuit_id>')
def one_circuit(circuit_id):
    stmt=db.select(Circuit).filter_by(id=circuit_id)
    circuit=db.session.scalar(stmt)
    if circuit:
        return CircuitSchema().dump(circuit)
    else:
        return{'error': 'Circuit not found.'}, 404 # Not Found: The requested circuit resource does not exist.

@circuits_bp.route('/', methods=['POST'])
def create_circuit():
    current_user = admin_or_organizer_role_required()

    try:
        circuit_details=CircuitSchema().load(request.json)
    except ValidationError as err:
        return{'error': 'Validation Error', 'errors': err.messages}, 400
    existing_circuit = db.session.query(Circuit).filter_by(track_name=circuit_details['track_name']).first()

    if existing_circuit:
        return {'error': 'Circuit already exists.'}, 400
    
    circuit=Circuit(
        track_name=circuit_details['track_name'],
        location=circuit_details['location'],
        lap_record=circuit_details['lap_record'],
        user_id=current_user.id
    )

    db.session.add(circuit)
    db.session.commit()
    return CircuitSchema().dump(circuit), 201

@circuits_bp.route('/<int:circuit_id>', methods=['PUT', 'PATCH'])
def update_circuit(circuit_id):
    current_user = admin_or_organizer_role_required()

    stmt = db.select(Circuit).filter_by(id=circuit_id)
    circuit = db.session.scalar(stmt)

    if not circuit:
        return{'error': 'Circuit not found.'}, 404 # Not Found: The requested circuit resource does not exist.
    if not (current_user.is_admin or current_user.id == circuit.user_id):
        return {'error': 'You are not authorized to update this circuit.'}, 403 # Forbidden: The server understood the request, but is refusing to fulfill it.
    
    try:
        circuit_details=CircuitSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400 # Bad Request: The request could not be understood by the server due to malformed syntax. The client SHOULD NOT repeat the request without modifications.
    
    if circuit:
        circuit.track_name = circuit_details.get('track_name', circuit.track_name)
        circuit.location = circuit_details.get('location', circuit.location)
        circuit.lap_record = circuit_details.get('lap_record', circuit.lap_record)
        db.session.commit()
        return CircuitSchema().dump(circuit)
    else:
        return{'error': 'Circuit not found.'}, 404 # Not Found: The requested circuit resource does not exist.

@circuits_bp.route('/<int:circuit_id>', methods=['DELETE'])
def delete_circuit(circuit_id):
    current_user = admin_or_organizer_role_required()

    stmt = db.select(Circuit).filter_by(id=circuit_id)
    circuit = db.session.scalar(stmt)

    if not circuit:
        return{'error': 'Circuit not found.'}, 404 # Not Found: The requested circuit resource does not exist.
    if not (current_user.is_admin or current_user.id == circuit.user_id):
        return {'error': 'You are not authorized to delete this circuit.'}, 403 # Forbidden: The server understood the request, but is refusing to fulfill it.
    
    if circuit:
        db.session.delete(circuit)
        db.session.commit()
        return{}, 204 # No Content: The server successfully processed the request and is not returning any content.
   
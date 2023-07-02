from flask import Blueprint, request
from init import db
from models.circuit import Circuit, CircuitSchema
from blueprints.auth_bp import admin_or_organizer_role_required
from utils import validate_schema, get_resource_or_404

circuits_bp = Blueprint('circuit', __name__, url_prefix='/circuits')

# This route is used to get all the circuits in the database and returns all the circuits - Is open to all users and public to view
@circuits_bp.route('/')
def all_circuits():
    stmt=db.select(Circuit)
    circuits=db.session.scalars(stmt).all()
    if circuits:
        return CircuitSchema(many=True).dump(circuits)
    else:
        return{'error': 'No circuits found.'}, 404 # Not Found: The requested circuits resource does not exist.

# This route is used to get a specific circuit in the database and returns the circuit if the circuit exists or returns an error if the circuit does not exist - Is open to all users and public to view
@circuits_bp.route('/<int:circuit_id>')
def one_circuit(circuit_id):
    circuit = get_resource_or_404(db.select(Circuit).filter_by(id=circuit_id), 'Circuit')
    return CircuitSchema().dump(circuit)

# This route is used to create a new circuit in the database and returns the new circuit if the user is an admin or organizer or returns an error if the user is not an admin or organizer - Is only open to admin and organizer users
@circuits_bp.route('/', methods=['POST'])
def create_circuit():
    current_user = admin_or_organizer_role_required()
    circuit_details = validate_schema(CircuitSchema(), request.json)
    
    existing_circuit = db.session.query(Circuit).filter_by(track_name=circuit_details['track_name']).first()
    if existing_circuit:
        return {'error': 'Circuit already exists.'}, 409 # Conflict: The request could not be completed due to circuit already existing.
    
    circuit=Circuit(
        track_name=circuit_details['track_name'],
        location=circuit_details['location'],
        lap_record_seconds=circuit_details['lap_record_seconds'],
        user_id=current_user.id
    )

    db.session.add(circuit)
    db.session.commit()
    return CircuitSchema().dump(circuit), 201

# This route is used to update a specific circuit in the database and returns the updated circuit if the user is an admin or organizer or returns an error if the user is not an admin or organizer - Only the user who created the circuit or an admin can update the circuit
@circuits_bp.route('/<int:circuit_id>', methods=['PUT', 'PATCH'])
def update_circuit(circuit_id):
    current_user = admin_or_organizer_role_required()
    circuit = get_resource_or_404(db.select(Circuit).filter_by(id=circuit_id), 'Circuit')

    if not (current_user.is_admin or current_user.id == circuit.user_id):
        return {'error': 'You are not authorized to update this circuit.'}, 403 # Forbidden: The server understood the request, but is refusing to fulfill it.
    
    circuit_details = validate_schema(CircuitSchema(), request.json)

    circuit.track_name = circuit_details.get('track_name', circuit.track_name)
    circuit.location = circuit_details.get('location', circuit.location)
    circuit.lap_record_seconds = circuit_details.get('lap_record_seconds', circuit.lap_record_seconds)
    db.session.commit()
    return CircuitSchema().dump(circuit)

# This route is used to delete a specific circuit in the database and returns a 204 status code if the user is an admin or organizer or returns an error if the user is not an admin or organizer - Only the user who created the circuit or an admin can delete the circuit
@circuits_bp.route('/<int:circuit_id>', methods=['DELETE'])
def delete_circuit(circuit_id):
    current_user = admin_or_organizer_role_required()
    circuit = get_resource_or_404(db.select(Circuit).filter_by(id=circuit_id), 'Circuit')

    if not (current_user.is_admin or current_user.id == circuit.user_id):
        return {'error': 'You are not authorized to delete this circuit.'}, 403 # Forbidden: The server understood the request, but is refusing to fulfill it.
    

    db.session.delete(circuit)
    db.session.commit()
    return{}, 204 # No Content: The server successfully processed the request and is not returning any content.
   
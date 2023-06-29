from flask import Blueprint, request
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from models.user import User, UserSchema
from models.team import Team, TeamSchema
from models.category import Category, CategorySchema
from models.circuit import Circuit, CircuitSchema
from datetime import date

circuits_bp = Blueprint('circuit', __name__, url_prefix='/circuits')

@circuits_bp.route('/')
def all_circuits():
    stmt=db.select(Circuit)
    circuits=db.session.scalars(stmt).all()
    return CircuitSchema(many=True).dump(circuits)

@circuits_bp.route('/<int:circuit_id>')
def one_circuit(circuit_id):
    stmt=db.select(Circuit).filter_by(id=circuit_id)
    circuit=db.session.scalar(stmt)
    if circuit:
        return CircuitSchema().dump(circuit)
    else:
        return{'error': 'Circuit not found.'}, 400

@circuits_bp.route('/', methods=['POST'])
def create_circuit():
    try:
        circuit_details=CircuitSchema().load(request.json)
    except ValidationError as err:
        return{'error': 'Validation Error', 'errors': err.messages}, 400

    circuit=Circuit(
        track_name=circuit_details['track_name'],
        location=circuit_details['location'],
        lap_record=circuit_details['lap_record']
    )

    db.session.add(circuit)
    db.session.commit()
    return CircuitSchema().dump(circuit), 201

@circuits_bp.route('/<int:circuit_id>', methods=['PUT', 'PATCH'])
def update_circuit(circuit_id):
    try:
        circuit_details=CircuitSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400
    
    stmt = db.select(Circuit).filter_by(id=circuit_id)
    circuit = db.session.scalar(stmt)

    if circuit:
        circuit.track_name = circuit_details.get('track_name', circuit.track_name)
        circuit.location = circuit_details.get('location', circuit.location)
        circuit.lap_record = circuit_details.get('lap_record', circuit.lap_record)
        circuit.id = circuit_details.get('id', circuit.id)
        db.session.commit()
        return CircuitSchema().dump(circuit)
    else:
        return{'error': 'Circuit not found.'}, 404

@circuits_bp.route('/<int:circuit_id>', methods=['DELETE'])
def delete_circuit(circuit_id):
    stmt = db.select(Circuit).filter_by(id=circuit_id)
    circuit = db.session.scalar(stmt)
    if circuit:
        db.session.delete(circuit)
        db.session.commit()
        return{}, 200
    else:
        return{'error': 'Circuit not found.'}, 404
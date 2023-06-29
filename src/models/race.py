from init import db, ma
from marshmallow import fields
from models.circuit import CircuitSchema
from models.category import CategorySchema
from datetime import date

class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)

    circuit_id = db.Column(db.Integer, db.ForeignKey('circuits.id'))
    circuit = db.relationship('Circuit', back_populates='races')

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='races')

    results = db.relationship('Result', back_populates='race')

class RaceSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    date = fields.Date(required=True)
    circuit_id = fields.Int(required=True, load_only=True)
    category_id = fields.Int(required=True, load_only=True)
    circuit = ma.Nested('CircuitSchema', dump_only=('id', 'track_name', 'location'))
    category = ma.Nested('CategorySchema', dump_only=('id', 'name'))
#  this took so long to get to work. Now when dumping from the API create, the return JSON will include the circuit and category objects WITHOUT 
# repeating the category_id/circuit_id
    class Meta:
        fields = ('id', 'date', 'name', 'circuit', 'category', 'circuit_id', 'category_id')
        load_instance = True  # Optional: deserialize to model instances



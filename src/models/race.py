from init import db, ma
from marshmallow import fields
from models.circuit import CircuitSchema
from models.category import CategorySchema
from datetime import date

class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String, nullable=False)

    circuit_id = db.Column(db.Integer, db.ForeignKey('circuits.id'),nullable=False)
    circuit = db.relationship('Circuit', back_populates='races')

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='races')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='races')

    results = db.relationship('Result', back_populates='race')


class RaceSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True)
    date = fields.Date(required=True)
    circuit_id = fields.Int(required=True, load_only=True)
    category_id = fields.Int(required=True, load_only=True)
    circuit = ma.Nested('CircuitSchema', dump_only=('id', 'track_name', 'location'))
    category = ma.Nested('CategorySchema', dump_only=('id', 'name'))
    results = ma.Nested('ResultSchema', many=True)
    user = ma.Nested('UserSchema', only=('id',))
    
    class Meta:
        fields = ('id', 'date', 'name', 'circuit', 'category', 'circuit_id', 'category_id', 'user')


 
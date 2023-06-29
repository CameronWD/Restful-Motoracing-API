from init import db, ma
from marshmallow import fields
from datetime import datetime

class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.String)

    circuit_id = db.Column(db.Integer, db.ForeignKey('circuits.id'))
    circuit = db.relationship('Circuit', back_populates='races')

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='races')

    results = db.relationship('Result', back_populates='race')

class RaceSchema(ma.Schema):
    circuit = ma.Nested('CircuitSchema')
    category = ma.Nested('CategorySchema')
    results = fields.Nested('ResultSchema', many=True)

    class Meta:
        fields = ('id', 'date', 'circuit', 'category', 'results')
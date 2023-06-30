from init import db, ma
from marshmallow import fields
from models.race import Race, RaceSchema
from models.driver import Driver, DriverSchema

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)

    start_position = db.Column(db.Integer, nullable=False)
    end_position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer)

    race_id = db.Column(db.Integer, db.ForeignKey('races.id'))
    race = db.relationship('Race', backrefs='results')

    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    driver = db.relationship('Driver', back_populates='results')

class ResultSchema(ma.Schema):
    race = ma.Nested('RaceSchema')
    driver = ma.Nested('DriverSchema')
    race_id = fields.Int(required=True)
    driver_id = fields.Int(required=True)

    class Meta:
        fields = ('id','start_position', 'end_position', 'points', 'driver', 'race', 'race_id', 'driver_id')
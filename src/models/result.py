from init import db, ma
from marshmallow import fields, validate
from models.race import Race, RaceSchema
from models.driver import Driver, DriverSchema

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)

    start_position = db.Column(db.Integer, nullable=False)
    end_position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer)

    race_id = db.Column(db.Integer, db.ForeignKey('races.id'))
    race = db.relationship('Race', back_populates='results')

    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id', ondelete='CASCADE'), nullable=False)
    driver = db.relationship('Driver', back_populates='results')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='results')

class ResultSchema(ma.Schema):
    race = ma.Nested('RaceSchema')
    driver = ma.Nested('DriverSchema')
    user = ma.Nested('UserSchema', only=('id',))
    # introduced range validation for start_position, end_position, points, driver_id and race_id as these are all inputs from the user and can't be negative
    race_id = fields.Int(required=True, validate=validate.Range(min=1))
    driver_id = fields.Int(required=True, validate=validate.Range(min=1))
    start_position = fields.Int(required=True, validate=validate.Range(min=1)) 
    end_position = fields.Int(required=True, validate=validate.Range(min=1)) 
    points = fields.Int(required=True, validate=validate.Range(min=0))

    class Meta:
        fields = ('id','start_position', 'end_position', 'points', 'driver', 'race', 'race_id', 'driver_id', 'user_id')
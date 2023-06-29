from init import db, ma
from marshmallow import fields

class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)

    start_position = db.Column(db.Integer, nullable=False)
    end_position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer)

    race_id = db.Column(db.Integer, db.ForeignKey('races.id'), nullable=False)
    race = db.relationship('Race', back_populates='results')

    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    driver = db.relationship('Driver', back_populates='results')

class ResultSchema(ma.Schema):
    race = ma.Nested('RaceSchema')
    driver = ma.Nested('DriverSchema')

    class Meta:
        fields = ('start_position', 'end_position', 'points', 'driver', 'race')
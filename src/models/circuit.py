from init import db, ma
from marshmallow import fields

class Circuit(db.Model):
    __tablename__ = 'circuits'

    id = db.Column(db.Integer, primary_key=True)

    track_name = db.Column(db.String, nullable=False, unique=True)
    location = db.Column(db.String)
    lap_record = db.Column(db.Integer)

class CircuitSchema(ma.Schema):
    class Meta:
        fields = ('track_name', 'location', 'lap_record')
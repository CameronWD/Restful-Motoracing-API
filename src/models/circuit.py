from init import db, ma
from marshmallow import fields, validate

class Circuit(db.Model):
    __tablename__ = 'circuits'

    id = db.Column(db.Integer, primary_key=True)

    track_name = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(100))
    lap_record = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='circuits')

    races = db.relationship('Race', back_populates='circuit')

class CircuitSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=('id',))
    races =fields.Nested('RaceSchema', many=True, only=('id', 'name', 'date'))
    track_name = fields.Str(required=True, validate=validate.Length(min=4, max=100))
    location = fields.Str(validate=validate.Length(min=4, max=100))
    lap_record = fields.Int(validate=validate.Range(min=5, max=9000000)) # in thousands of a second can handle over 24 hours which is probably the longest a race can go that is 'common' 
    class Meta:
        fields = ('id','track_name', 'location', 'lap_record', 'user_id', 'user', 'races')
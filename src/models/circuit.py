from init import db, ma
from marshmallow import fields, validate

# Creation of the Circuit model with the following attributes: id, track_name, location, lap_record_seconds and user_id
class Circuit(db.Model):
    __tablename__ = 'circuits'

    id = db.Column(db.Integer, primary_key=True)

    track_name = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(100))
    lap_record_seconds = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='circuits')

    races = db.relationship('Race', back_populates='circuit')

# Creation of the CircuitSchema with the following attributes: id, track_name, location, lap_record_seconds and user and is used to serialize the data
class CircuitSchema(ma.Schema):
    user = fields.Nested('UserSchema', exclude=('password','is_admin'))
    races =fields.Nested('RaceSchema', many=True, only=('id', 'name', 'date'))
    track_name = fields.Str(required=True, validate=validate.Length(min=4, max=100))
    location = fields.Str(validate=validate.Length(min=4, max=100))
    lap_record_seconds = fields.Int(validate=validate.Range(min=5, max=9000000)) # in thousands of a second can handle over 24 hours which is probably the longest a race can go that is 'common' 
    class Meta:
        fields = ('id','track_name', 'location', 'lap_record_seconds', 'user', 'races')
        
from init import db, ma
from marshmallow import fields, validate
from datetime import datetime

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False, unique=True)
    year_founded = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='team')

    drivers = db.relationship('Driver', back_populates='team')

class TeamSchema(ma.Schema):
    drivers = ma.Nested('DriverSchema', many=True, only=('id', 'first_name', 'last_name'))
    user= ma.Nested('UserSchema', only=('id',))
    name = fields.Str(required=True, validate=validate.Length(min=5, max=100))
    # year founded can be as early as the year 1000 but can not be any earlier than the current date
    year_founded = fields.Int(required=True, validate=validate.Range(min=1000, max=datetime.now().year))
    class Meta:
        fields = ('id','name', 'year_founded', 'drivers', 'user', 'user_id')
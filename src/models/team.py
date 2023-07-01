from init import db, ma
from marshmallow import fields

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False, unique=True)
    year_founded = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='team')

    drivers = db.relationship('Driver', back_populates='team')

class TeamSchema(ma.Schema):
    drivers = ma.Nested('DriverSchema', many=True, only=('id', 'first_name', 'last_name'))
    user= ma.Nested('UserSchema', only=('id',))
    class Meta:
        fields = ('id','name', 'year_founded', 'drivers', 'user', 'user_id')
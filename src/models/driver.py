from init import db, ma
from marshmallow import fields, validate, validates, ValidationError
from marshmallow.validate import Range
from datetime import datetime, date

# Creation of the Driver model with the attributes: id, date of birth, first_name, last_name, nationality, team_id, team, user_id, user and results
class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)

    date_of_birth = db.Column(db.Date())
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    nationality = db.Column(db.String(60)) #longest nationality is 58 charcters long 

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=True)
    team = db.relationship('Team', back_populates='drivers')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='driver')

    results = db.relationship('Result', back_populates='driver', cascade='all, delete-orphan')

# Creation of the DriverSchema that will be used to serialize the data from the database
class DriverSchema(ma.Schema):
    team = ma.Nested('TeamSchema', only=('id','name'))
    user = ma.Nested('UserSchema', exclude=('password','is_admin'))
    
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    nationality = fields.Str(validate=validate.Length(min=4, max=60))
    date_of_birth = fields.Date(required=True)


    @validates('date_of_birth')
    def validate_date_of_birth(self, value):
        print("Value: ", value)
        if value is None:
            raise ValidationError('DOB is required.')
        elif value < date(1900, 1, 1) or value > date.today():
            raise ValidationError('Date of birth must be between 1900-01-01 and today.')
    class Meta:
        fields = ('id','date_of_birth', 'first_name', 'last_name', 'nationality', 'team', 'user') 
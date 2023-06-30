from init import db, ma
from marshmallow import fields
from datetime import datetime

class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)

    date_of_birth = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    nationality = db.Column(db.String)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='drivers')

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'))
    team = db.relationship('Team', back_populates='drivers')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='drivers')

    results = db.relationship('Result', back_populates='driver')

class DriverSchema(ma.Schema):
    category = ma.Nested('CategorySchema')
    team = ma.Nested('TeamSchema')
    user = ma.Nested('UserSchema')

    class Meta:
        fields = ('id','date_of_birth', 'first_name', 'last_name', 'nationality', 'category', 'team', 'user') 
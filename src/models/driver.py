from init import db, ma
from marshmallow import fields
from datetime import datetime

class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)

    date_of_birth = db.Column(db.Date())
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    nationality = db.Column(db.String)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', back_populates='drivers')

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'))
    team = db.relationship('Team', back_populates='drivers')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='driver')

    results = db.relationship('Result', back_populates='driver', cascade='all, delete-orphan')

class DriverSchema(ma.Schema):
    category = ma.Nested('CategorySchema', only=('id',))
    team = ma.Nested('TeamSchema', only=('id',))
    user = ma.Nested('UserSchema', only=('id',))

    
    class Meta:
        fields = ('id','date_of_birth', 'first_name', 'last_name', 'nationality', 'category', 'team', 'user') 
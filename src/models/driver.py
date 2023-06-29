from init import db, ma
from marshmallow import fields

class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)

    date_of_birth = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    nationality = db.Column(db.String)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='drivers')

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    team = db.relationship('Team', back_populates='drivers')

    results = db.relationship('Result', back_populates='driver')

class DriverSchema(ma.Schema):
    category = ma.Nested('CategorySchema')
    team = ma.Nested('TeamSchema')

    class Meta:
        fields = ('id','date_of_birth', 'first_name', 'last_name', 'nationality', 'category', 'team')
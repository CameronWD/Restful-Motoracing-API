from init import db, ma
from marshmallow import fields

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False, unique=True)
    year_founded = db.Column(db.Integer)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    category = db.relationship('Category', back_populates='teams')

    drivers = db.relationship('Driver', back_populates='team')

class TeamSchema(ma.Schema):
    category = ma.Nested('CategorySchema')
    class Meta:
        fields = ('id','name', 'year_founded', 'category_id')
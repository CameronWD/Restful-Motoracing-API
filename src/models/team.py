from init import db, ma
from marshmallow import fields

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False, unique=True)
    year_founded = db.Column(db.String)

    category_id = db.relationship(db.Integer, db.ForeignKey('categories.id', nullable=False))
    category = db.relationship('Category', back_populates='teams')

class TeamSchema(ma.Schema):
    category = ma.Nested('CategorySchema')
    class Meta:
        fields = ('name', 'year_founded', 'category')
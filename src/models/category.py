from init import db, ma
from marshmallow import fields

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)

    drivers = db.relationship('Driver', back_populates='category', cascade='all,delete')

    races = db.relationship('Race', back_populates='category')

class CategorySchema(ma.Schema):
    class Meta:
        fields = ('name', 'description')
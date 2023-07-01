from init import db, ma
from marshmallow import fields

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String)

    races = db.relationship('Race', back_populates='category')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='category')


class CategorySchema(ma.Schema):
    user= ma.Nested('UserSchema', only=('id',))
    class Meta:
        fields = ('id','name', 'description', 'user')
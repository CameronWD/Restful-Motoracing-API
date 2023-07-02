from init import db, ma
from marshmallow import validate, fields

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text())

    races = db.relationship('Race', back_populates='category')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='category')


class CategorySchema(ma.Schema):
    user= ma.Nested('UserSchema', exclude=('password','is_admin'))
    name = fields.Str(required=True, validate=validate.Length(min=4, max=100))
    description = fields.Str(validate=validate.Length(min=5, max=500))
    class Meta:
        fields = ('id','name', 'description', 'user')
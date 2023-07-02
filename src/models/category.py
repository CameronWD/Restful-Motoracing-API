from init import db, ma
from marshmallow import validate, fields

# Creation of the Category model with the following attributes: id, name, description and user_id
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text(), nullable=True)

    races = db.relationship('Race', back_populates='category')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='category')

# Creation of the CategorySchema with the following attributes: id, name, description and user and is used to serialize the data
class CategorySchema(ma.Schema):
    user= ma.Nested('UserSchema', exclude=('password','is_admin'))
    name = fields.Str(required=True, validate=validate.Length(min=4, max=100))
    description = fields.Str(required=False, validate=validate.Length(max=500))
    class Meta:
        fields = ('id','name', 'description', 'user')
        
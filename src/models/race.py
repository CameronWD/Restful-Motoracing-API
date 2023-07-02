from init import db, ma
from marshmallow import fields, validate


class Race(db.Model):
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String(100), nullable=False)

    circuit_id = db.Column(db.Integer, db.ForeignKey('circuits.id'),nullable=False)
    circuit = db.relationship('Circuit', back_populates='races')

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='races')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='races')

    results = db.relationship('Result', back_populates='race')


class RaceSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=5, max=100))
    date = fields.Date(required=True)
    circuit_id = fields.Int(required=True, load_only=True)
    category_id = fields.Int(required=True, load_only=True)
    circuit = ma.Nested('CircuitSchema', exclude=('races',))
    category = ma.Nested('CategorySchema', dump_only=('id', 'name'))
    results = ma.Nested('ResultSchema', many=True)
    user = ma.Nested('UserSchema', exclude=('password','is_admin'))
    
    class Meta:
        fields = ('id', 'date', 'name', 'circuit', 'category', 'circuit_id', 'category_id', 'user')


 
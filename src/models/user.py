from init import db, ma
from marshmallow import validates, ValidationError, validates_schema

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default=False)

    is_admin = db.Column(db.Boolean, default=False)

    driver = db.relationship('Driver', back_populates='user')
class UserSchema(ma.Schema):
    class Meta:
       fields = ('id', 'name', 'email', 'password', 'role', 'is_admin')

    @validates('role')
    def validate_role(self, role):
        if role not in ['user', 'team', 'driver', 'organizer']:
            raise ValidationError('Role must be either user, team, driver or organizer.')

    @validates_schema
    def validate_role_and_admin(self, both, **kwargs):
        if not both.get('is_admin', False) and 'role' not in both:
            raise ValidationError('Non-admin users must have a role.')

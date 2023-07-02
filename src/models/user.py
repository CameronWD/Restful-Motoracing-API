from init import db, ma
from marshmallow import validates, ValidationError, validates_schema, validate, fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)

    is_admin = db.Column(db.Boolean, default=False)

    driver = db.relationship('Driver', back_populates='user')
    team = db.relationship('Team', back_populates='user')
    category = db.relationship('Category', back_populates='user')
    circuits = db.relationship('Circuit', back_populates='user')
    races = db.relationship('Race', back_populates='user')
    results = db.relationship('Result', back_populates='user')

class UserSchema(ma.Schema):
    name = fields.Str(validate=validate.Length(min=2, max=100))
    email = fields.Email(required=True)
    # Minimum eight characters, at least one uppercase letter, one lowercase letter and one number
    password = fields.Str(required=True, validate=validate.Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')) 
    role = fields.Str(validate=validate.OneOf(["team", "driver", "organizer"]))
    is_admin = fields.Boolean()
    class Meta:
       fields = ('id', 'name', 'email', 'password', 'role', 'is_admin')

    @validates('role')
    def validate_role(self, role):
        if role not in ['team', 'driver', 'organizer']:
            raise ValidationError('Role must be either team, driver or organizer.')

    @validates_schema
    def validate_role_and_admin(self, both, **kwargs):
        if not both.get('is_admin', False) and 'role' not in both:
            raise ValidationError('Non-admin users must have a role.')

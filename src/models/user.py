from init import db, ma, bcrypt

class UserType(db.Model):
    __tablename__ = 'user_types'
    user_type_id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(50), unique = True, nullable = False)
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    user_type_id = db.Column(db.Integer,db.ForeignKey('user_types.user_type'), nullable = False)

    user_type = db.relationship('UserType', backref = 'users', lazy = True')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
        
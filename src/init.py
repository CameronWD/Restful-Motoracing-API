from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

ma = Marshmallow()
db = SQLAlchemy()
jwt = JWTManager()
bcrypt = Bcrypt()
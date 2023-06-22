from flask import Flask
from init import db, ma, bcrypt, jwt
from os import environ


def setup():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': str(err)}, 401
    
    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404
    

    return app
from flask import Flask
from os import environ
from init import db, ma, bcrypt, jwt
from blueprints.cli_bp import cli_bp
from blueprints.auth_bp import auth_bp
from blueprints.teams_bp import teams_bp
from blueprints.categories_bp import categories_bp
from blueprints.circuits_bp import circuits_bp
from blueprints.drivers_bp import drivers_bp
from blueprints.races_bp import races_bp
from blueprints.results_bp import results_bp

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URI')
    app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(400)
    def bad_request(error):
        return {'error': str(error)}, 400

    @app.errorhandler(401)
    def unauthorized(error):
        return {'error': str(error)}, 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return {'error': str(error)}, 403
    
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': str(error)}, 404
    

    app.register_blueprint(cli_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(circuits_bp)
    app.register_blueprint(drivers_bp)
    app.register_blueprint(races_bp)
    app.register_blueprint(results_bp)
  
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        app.run()
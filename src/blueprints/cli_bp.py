from flask import Blueprint
from init import db, bcrypt
from models.user import User

cli_bp = Blueprint('db', __name__)

@cli_bp.cli.command('create')
def create_db():
    db.drop_all()
    db.create_all()
    print('Tables Created')

@cli_bp.cli.command('seed')
def seed_db():
    users = [
        User(
            email='admin@racingapi.com',
            password=bcrypt.generate_password_hash('spafrancorchamps'),
            is_admin=True
        ),
        User(
            email='organizer@racingapi.com',
            password=bcrypt.generate_password_hash('silverstone'),
            is_organizer=True
        ),
        User(
            name='Charles Leclerc',
            email='driver@racingapi.com',
            password=bcrypt.generate_password_hash('suzuka')
        )
    ]

    db.session.query(User).delete()
    db.session.add_all(users)
    db.session.commit()

    print('Models seeded')


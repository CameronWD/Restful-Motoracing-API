from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.circuit import Circuit
from models.category import Category
from models.team import Team
from models.driver import Driver
from models.race import Race
from models.result import Result

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
            name='Admin',
            email='admin@racingapi.com',
            password=bcrypt.generate_password_hash('spafrancorchamps').decode('utf-8'),
            is_admin=True
        ),
        User(
            name = 'Organizer McOrganizerface',
            email='organizer@racingapi.com',
            password=bcrypt.generate_password_hash('silverstone').decode('utf-8'),
            role='organizer'
            ),
        User(
            name='Team Manager',
            email='team@racingapi.com',
            password=bcrypt.generate_password_hash('margin').decode('utf-8'),
            role='team'
        ),
        User(
            name='Joshua',
            email='driver@racingapi.com',
            password=bcrypt.generate_password_hash('suzuka').decode('utf-8'),
            role='driver'
        ),
        User(
            name='Charles Leclerc',
            email='CLeclerc@racingapi.com',
            password=bcrypt.generate_password_hash('baku').decode('utf-8'),
            role='driver'
        ),
        User(
            name='Team McManager',
            email='Mcteam@racingapi.com',
            password=bcrypt.generate_password_hash('Maccas').decode('utf-8'),
            role='team'
        ),
    ]

    db.session.query(User).delete()
    db.session.add_all(users)
    db.session.commit()
    print('Users successfully seeded')

    categories = [
        Category(
            name='Kart Racing',
            description='Road racing motorsport on small, four-wheeled vehicles called go-karts. Generally raced on smaller circuits.',
            user = users[1]
            
        ),
        Category(
            name='Hillclimbing',
            description='Racing against the clock to complete an uphill track.',
            user = users[1]
        ),
        Category(
            name='Endurance Racing',
            description='Form of motorsport that aims to test the durability and endurance of participants and machines. Often can use multiple drivers over a race that ends after a certain period of time has passed.',
            user = users[0]
        )

    ]

    db.session.query(Category).delete()
    db.session.add_all(categories)
    db.session.commit()
    print('Categories successfully seeded')

    circuits = [
        Circuit(
            track_name='Nordschleife',
            location='Germany',
            lap_record_seconds=401,
            user = users[0]
        ), 
        Circuit(
            track_name='Mount Panorama',
            location='Victoria',
            lap_record_seconds=120,
            user = users[1]
        ), 
        Circuit(
            track_name='Laguna Seca',
            location='Brazil',
            lap_record_seconds=53,
            user = users[1]
        )
    ]

    db.session.query(Circuit).delete()
    db.session.add_all(circuits)
    db.session.commit()
    print('Circuits successfully seeded')

    teams = [
        Team(
            name='Ferrari',
            year_founded=1929,
            user_id=3
        ),
        Team(
            name='Burnouts Club',
            year_founded=2004,
            user_id=6
        )
    ]

    db.session.query(Team).delete()
    db.session.add_all(teams)
    db.session.commit()
    print('Teams successfully seeded')

    drivers = [
        Driver(
            date_of_birth='2000-04-11',
            first_name='Fernando',
            last_name='Alonso',
            nationality='Spanish',
            team=teams[1],
            user=users[3]
        ),
        Driver(
            date_of_birth='2000-04-11',
            first_name='Michael',
            last_name='Phelps',
            nationality='American',
            team=teams[0],
            user=users[4]
        ),
        Driver(
            date_of_birth='1995-04-11',
            first_name='Cookie',
            last_name='Monster',
            nationality='American',
            team=teams[0],
            user=users[0]
        )
    ]

    db.session.query(Driver).delete()
    db.session.add_all(drivers)
    db.session.commit()
    print('Drivers successfully seeded')

    races = [
        Race(
            name = 'German GP',
            date='1994-03-25',
            circuit_id=1,
            category_id=1,
            user_id=2
        ),
        Race(
            name = 'Fun Day at the Nurbergring GP', 
            date='2005-03-25',
            circuit_id=1,
            category_id=2,
            user_id=1
        ),
        Race(
            name = 'Victoria GP',
            date='2000-03-25',
            circuit_id=2,
            category_id=1,
            user_id=6
        ),
        Race(
            name = 'Mountain GP',
            date='2000-01-25',
            circuit_id=2,
            category_id=3,
            user_id=6
        )
    ]

    db.session.query(Race).delete()
    db.session.add_all(races)
    db.session.commit()
    print('Races successfully seeded')

    results = [
        Result(
            start_position=10,
            end_position=1,
            points=25,
            race_id=1,
            driver_id=1,
            user_id=4
        ),
         Result(
            start_position=10,
            end_position=15,
            points=0,
            race_id=2,
            driver_id=1,
            user_id=4
        ),
         Result(
            start_position=5,
            end_position=5,
            points=7,
            race_id=2,
            driver_id=2,
            user_id=4
        )
    ]
    
    db.session.query(Result).delete()
    db.session.add_all(results)
    db.session.commit()
    print('Results successfully seeded')
    print('Seeding Completed.')




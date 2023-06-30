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
            password=bcrypt.generate_password_hash('suzuka').decode('utf-8'),
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
            password=bcrypt.generate_password_hash('suzuka').decode('utf-8'),
            role='driver'
        )
    ]

    db.session.query(User).delete()
    db.session.add_all(users)
    db.session.commit()
    print('Users successfully seeded')

    categories = [
        Category(
            name='Kart Racing',
            description='Road racing motorsport on small, four-wheeled vehicles called go-karts. Generally raced on smaller circuits.'
        ),
        Category(
            name='Hillclimbing',
            description='Racing against the clock to complete an uphill track.'
        ),
        Category(
            name='Endurance Racing',
            description='Form of motorsport that aims to test the durability and endurance of participants and machines. Often can use multiple drivers over a race that ends after a certain period of time has passed.'
        )

    ]

    db.session.query(Category).delete()
    db.session.add_all(categories)
    db.session.commit()
    print('Categories successfully seeded')

    circuits = [
        Circuit(
            track_name='Nordschleife',
            location='test',
            lap_record=10

        ), 
        Circuit(
            track_name='Mount Panorama',
            location='test',
            lap_record=10
        ), 
        Circuit(
            track_name='Laguna Seca',
            location='test',
            lap_record=10
        )
    ]

    db.session.query(Circuit).delete()
    db.session.add_all(circuits)
    db.session.commit()
    print('Circuits successfully seeded')

    teams = [
        Team(
            name='Ferrari',
            year_founded=1929
        ),
        Team(
            name='Burnouts',
            year_founded=2004
        ), 
        Team(
            name='Darryl Dodgers',
            year_founded=2020
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
            category=categories[1],
            team=teams[1],
            user_id=4
        ),
        Driver(
            date_of_birth='2000-04-11',
            first_name='Michael',
            last_name='Phelps',
            nationality='American',
            category=categories[1],
            team=teams[1],
            user_id=4
        ),
        Driver(
            date_of_birth='2000-04-11',
            first_name='Yuki',
            last_name='Tsunoda',
            nationality='Japanese',
            category=categories[1],
            team=teams[1],
            user_id=1
        )
    ]

    db.session.query(Driver).delete()
    db.session.add_all(drivers)
    db.session.commit()
    print('Drivers successfully seeded')

    races = [
        Race(
            name = 'Mexico GP',
            date='1994-03-25',
            circuit_id=1,
            category_id=1
        ),
        Race(
            name = 'Monaco GP',
            date='2005-03-25',
            circuit_id=1,
            category_id=2
        ),
        Race(
            name = 'Brisbane GP',
            date='2000-03-25',
            circuit_id=2,
            category_id=1
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
            driver_id=2
        ),
         Result(
            start_position=10,
            end_position=15,
            points=0,
            race_id=2,
            driver_id=1
        ),
         Result(
            start_position=5,
            end_position=5,
            points=7,
            race_id=2,
            driver_id=2
        )
    ]
    
    db.session.query(Result).delete()
    db.session.add_all(results)
    db.session.commit()
    print('Results successfully seeded')
    print('Seeding Completed.')




from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


# Drivers: driver_id(PK), profile_id(FK), category_id(FK), team_id(FK)
class Driver(db.Model):
    driver_id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey('profile.profile_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullabe=False)

# Profiles: profile_id(PK), date_of_birth, first_name, last_name, nationality
class Profiles(db.Model):
    profile_id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column()
    first_name = db.Column(db.string)
    last_name = db.Column(db.string)
    nationality = db.Column(db.string)

# Teams: team_id(PK), name, year_founded, category_id(FK)
class Teams(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.string, db.ForeignKey('category.category_id'), nullable=False)
    name = db.Column(db.string, nullable=False)
    year_founded = db.Column(db.Integer)
    
# Circuits: circuit_id(PK), track_name, location
class Circuits(db.Circuits):
    circuit_id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.string, nullable=False)
    location = db.Column(db.string, nullable=False)

# Results: results_id(PK), race_id(FK), driver_id(FK), start_position, end_position, points
class Results(db.Results):
    result_id = db.Column(db.Integer, primary_key=True)
    race_id = 
    driver_id = 
    start_position = db.Column(db.string, nullable=False)
    end_position = db.Column(db.string, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    
# Categories: category_id(PK), name, description

class Categories(db.Categories):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, nullabe=False)
    description = db.Column(db.string, nullable=False)

# Race: race_id(PK), date, circuit_id(FK), category_id(FK)

class Races(db.Races):
    race_id = db.Column(db.Integer, primary_key=True)
    circuit_id = 
    category_id = 
    date = db.Column(db.Integer, nullabe=False)


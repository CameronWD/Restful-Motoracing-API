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

# Categories: category_id(PK), name, description

# Race: race_id(PK), date, circuit_id(FK), category_id(FK)


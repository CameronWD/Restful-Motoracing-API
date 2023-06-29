from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from models.team import Team, TeamSchema
from datetime import date

teams_bp = Blueprint('team', __name__, url_prefix='/teams')

@teams_bp.route('/')
def all_teams():
    stmt = db.select(Team)
    teams = db.session.scalars(stmt).all()
    return TeamSchema(many=True).dump(teams)

@teams_bp.route('/<int:team_id>')
def one_team(team_id):
    stmt = db.select(Team).filter_by(id=team_id)
    team = db.session.scalar(stmt)
    if team:
        return TeamSchema().dump(team)
    else:
        return{'error': 'Team not found.'}, 404

@teams_bp.route('/', methods=['POST'])
def create_team():
    team_details = TeamSchema().load(request.json)
    team = Team(
        name = team_details['name'],
        year_founded = team_details['year_founded'],
        category_id = team_details['category_id']
    )
    db.session.add(team)
    db.session.commit()
    return TeamSchema().dump(team), 201

# @teams_bp.route('/<int:team_id>', methods=['PUT', 'PATCH'])

# @teams_bp.route('/<int:team_id', methods=['DELETE'])
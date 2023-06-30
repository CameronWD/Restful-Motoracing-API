from flask import Blueprint, request
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from models.team import Team, TeamSchema
from models.category import Category

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
        return{'error': 'Team not found.'}, 400

@teams_bp.route('/', methods=['POST'])
def create_team():
    try:
        team_details = TeamSchema().load(request.json)
    except ValidationError as err:
        return {'error': 'Validation Error', 'errors': err.messages}, 400
    
    category = Category.query.get(team_details['category_id'])
    if not category:
        return {'error':'Category not found.'}, 400

    team = Team(
        name = team_details['name'],
        year_founded = team_details['year_founded'],
        category_id = team_details['category_id']
    )

    db.session.add(team)
    db.session.commit()
    return TeamSchema().dump(team), 201

@teams_bp.route('/<int:team_id>', methods=['PUT', 'PATCH'])
def update_team(team_id):
    try:
        team_details = TeamSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400

    stmt = db.select(Team).filter_by(id=team_id)
    team = db.session.scalar(stmt)
    
    if team:
        team.name = team_details.get('name', team.name)
        team.year_founded = team_details.get('year_founded', team.year_founded)
        team.category_id = team_details.get('category_id', team.category_id)
        db.session.commit()
        return TeamSchema().dump(team)
    else:
        return{'error': 'Team not found.'}, 404


@teams_bp.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    stmt = db.select(Team).filter_by(id=team_id)
    team = db.session.scalar(stmt)
    if team:
        db.session.delete(team)
        db.session.commit()
        return {}, 200
    else:
        return{'error': 'Team not found.'}, 404
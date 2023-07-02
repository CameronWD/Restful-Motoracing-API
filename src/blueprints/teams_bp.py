from flask import Blueprint, request
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from models.team import Team, TeamSchema
from blueprints.auth_bp import admin_or_team_role_required
from flask_jwt_extended import get_jwt_identity, jwt_required

teams_bp = Blueprint('team', __name__, url_prefix='/teams')

@teams_bp.route('/')
def all_teams():
    stmt = db.select(Team)
    teams = db.session.scalars(stmt).all()
    if teams:
        return TeamSchema(many=True).dump(teams)
    else:
        return{'error': 'No teams found.'}, 404 # Not Found: The requested teams resource does not exist.

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
    current_user = admin_or_team_role_required()

    exising_team = Team.query.filter_by(user_id=current_user.id).first()

    if exising_team:
        return{'error': 'Team already exists for this user. Please delete or update your current team profile.'}, 409 # Conflict: The team already exists and creates a conflict with the unique constraint.
    
    try:
        team_details = TeamSchema().load(request.json)
    except ValidationError as err:
        return {'error': 'Validation Error', 'errors': err.messages}, 400 # Bad Request: The request data is invalid.

    team = Team(
        name = team_details['name'],
        year_founded = team_details['year_founded'],
        user_id = current_user.id
    )

    db.session.add(team)
    db.session.commit()
    return TeamSchema().dump(team), 201 # Created: The team resource has been successfully created.

@teams_bp.route('/<int:team_id>', methods=['PUT', 'PATCH'])
def update_team(team_id):
    current_user = admin_or_team_role_required()

    stmt = db.select(Team).filter_by(id=team_id)
    team = db.session.scalar(stmt)

    if not team:
        return{'error': 'Team not found.'}, 404 # Not Found: The requested team resource does not exist.
    if not (current_user.id == team.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this team.'}, 403 # Forbidden: The user is not authorized to update the team resource.

    try:
        team_details = TeamSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400 # Bad Request: The request data is invalid.

    if team:
        team.name = team_details.get('name', team.name)
        team.year_founded = team_details.get('year_founded', team.year_founded)
        db.session.commit()
        return TeamSchema().dump(team)
    


@teams_bp.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    current_user = admin_or_team_role_required()

    stmt = db.select(Team).filter_by(id=team_id)
    team = db.session.scalar(stmt)

    if not team:
        return{'error': 'Team not found.'}, 404 # Not Found: The requested team resource does not exist.
    if not (current_user.id == team.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to delete this team.'}, 403 # Forbidden: The user is not authorized to delete the team resource.
    
    if team:
        db.session.delete(team)
        db.session.commit()
        return {}, 204 # No Content: The team resource has been successfully deleted.
    else:
        return{'error': 'Team not found.'}, 404 # Not Found: The requested team resource does not exist.
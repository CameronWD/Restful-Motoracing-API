from flask import Blueprint, request
from init import db
from models.team import Team, TeamSchema
from blueprints.auth_bp import admin_or_team_role_required
from utils import validate_schema, get_resource_or_404

teams_bp = Blueprint('team', __name__, url_prefix='/teams')

# This route is used to get all the teams in the database and returns all the teams

@teams_bp.route('/')
def all_teams():
    stmt = db.select(Team)
    teams = db.session.scalars(stmt).all()
    if teams:
        return TeamSchema(many=True).dump(teams)
    else:
        return{'error': 'No teams found.'}, 404 # Not Found: The requested teams resource does not exist.

# This route is used to get a specific team in the database and returns the team if the team exists or returns an error if the team does not exist
@teams_bp.route('/<int:team_id>')
def one_team(team_id):
    team = get_resource_or_404(db.select(Team).filter_by(id=team_id), 'Team')
    return TeamSchema().dump(team)

# This route is used to create a new team in the database and returns the new team if the user is an admin or has the role team or returns an error if the user is not an admin or does not have the role team
@teams_bp.route('/', methods=['POST'])
def create_team():
    current_user = admin_or_team_role_required()
    team_details = validate_schema(TeamSchema(), request.json)

    existing_team = Team.query.filter_by(user_id=current_user.id).first()
    if existing_team:
        return{'error': 'Team already exists for this user. Please delete or update your current team profile.'}, 409 # Conflict: The team already exists and creates a conflict with the unique constraint.

    team = Team(
        name = team_details['name'],
        year_founded = team_details['year_founded'],
        user_id = current_user.id
    )

    db.session.add(team)
    db.session.commit()
    return TeamSchema().dump(team), 201 # Created: The team resource has been successfully created.

# This route is used to update a specific team in the database and returns the updated team if the user is an admin or has the role team or returns an error if the user is not an admin or does not have the role team
@teams_bp.route('/<int:team_id>', methods=['PUT', 'PATCH'])
def update_team(team_id):
    current_user = admin_or_team_role_required()
    team = get_resource_or_404(db.select(Team).filter_by(id=team_id), 'Team')

    if not (current_user.id == team.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this team.'}, 403 # Forbidden: The user is not authorized to update the team resource.

    team_details = validate_schema(TeamSchema(), request.json, partial=True)

    team.name = team_details.get('name', team.name)
    team.year_founded = team_details.get('year_founded', team.year_founded)
    
    db.session.commit()
    return TeamSchema().dump(team)
    

# This route is used to delete a specific team in the database and returns an error if the user is not an admin or does not have the role team or returns an error if the user is not an admin or does not have the role team
@teams_bp.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    current_user = admin_or_team_role_required()
    team = get_resource_or_404(db.select(Team).filter_by(id=team_id), 'Team')

    if not (current_user.id == team.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to delete this team.'}, 403 # Forbidden: The user is not authorized to delete the team resource.
    
    db.session.delete(team)
    db.session.commit()
    return {}, 204 # No Content: The team resource has been successfully deleted.
    
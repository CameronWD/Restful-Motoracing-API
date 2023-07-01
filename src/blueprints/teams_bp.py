from flask import Blueprint, request
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from models.team import Team, TeamSchema
from models.category import Category
from models.user import User, UserSchema
from blueprints.auth_bp import admin_or_team_role_required

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
    current_user = admin_or_team_role_required()

    exising_team = Team.query.filter_by(user_id=current_user.id).first()
    if exising_team:
        return{'error': 'Team already exists for this user. Please delete or update your current team profile.'}, 400
    
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
    current_user = admin_or_team_role_required()

    stmt = db.select(Team).filter_by(id=team_id)
    team = db.session.scalar(stmt)

    if not team:
        return{'error': 'Team not found.'}, 404
    if not (current_user.id == team.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this team.'}, 403

    try:
        team_details = TeamSchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400

    if team:
        team.name = team_details.get('name', team.name)
        team.year_founded = team_details.get('year_founded', team.year_founded)
        team.category_id = team_details.get('category_id', team.category_id)
        db.session.commit()
        return TeamSchema().dump(team)
    


@teams_bp.route('/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    current_user = admin_or_team_role_required()

    stmt = db.select(Team).filter_by(id=team_id)
    team = db.session.scalar(stmt)

    if not team:
        return{'error': 'Team not found.'}, 404
    if not (current_user.id == team.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to delete this team.'}, 403
    
    if team:
        db.session.delete(team)
        db.session.commit()
        return {}, 200
    else:
        return{'error': 'Team not found.'}, 404
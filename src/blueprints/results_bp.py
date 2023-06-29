from flask import Blueprint, request
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from models.user import User, UserSchema
from models.team import Team, TeamSchema
from models.category import Category, CategorySchema
from datetime import date

results_bp = Blueprint('result', __name__, url_prefix='/results')

@results_bp.route('/')
def
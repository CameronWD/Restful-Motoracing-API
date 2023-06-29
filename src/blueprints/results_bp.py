from flask import Blueprint
from init import db
from models.result import Result, ResultSchema


results_bp = Blueprint('result', __name__, url_prefix='/results')

@results_bp.route('/')
def all_results():
    stmt=db.select(Result)
    results=db.session.scalars(stmt).all()
    return ResultSchema(many=True).dump(results)
from flask import Blueprint, request
from init import db, bcrypt
from marshmallow.exceptions import ValidationError
from models.user import User, UserSchema
from models.category import Category, CategorySchema
from blueprints.auth_bp import admin_or_organizer_role_required

categories_bp = Blueprint('category', __name__, url_prefix='/categories')

@categories_bp.route('/')
def all_categories():
    stmt = db.select(Category)
    categories = db.session.scalars(stmt).all()
    return CategorySchema(many=True).dump(categories)

@categories_bp.route('/<int:category_id>')
def one_category(category_id):
    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)
    if category:
        return CategorySchema().dump(category)
    else:
        return{'error': 'Category not found.'}, 404

@categories_bp.route('/', methods=['POST'])
def create_category():
    current_user = admin_or_organizer_role_required()

    existing_category = Category.query.filter_by(user_id=current_user.id).first()
    
    try:
        category_details = CategorySchema().load(request.json)
    except ValidationError as validation_error:
        return {'error': 'Validation Error', 'errors': validation_error.messages}, 400

    existing_category = db.session.query(Category).filter_by(name=category_details['name']).first()
    if existing_category:
        return {'error': 'Category already exists.'}, 400

    category = Category(
        name = category_details['name'],
        description = category_details['description'],
        user_id = current_user.id
    )

    db.session.add(category)
    db.session.commit()
    return CategorySchema().dump(category), 201

@categories_bp.route('/<int:category_id>', methods=['PUT', 'PATCH'])
def update_category(category_id):
    current_user = admin_or_organizer_role_required()

    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)

    if not category:
        return{'error': 'Category not found.'}, 404
    if not (current_user.id == category.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this category.'}, 403
    
    try:
        category_details = CategorySchema().load(request.json)
    except ValidationError as valdiation_error:
        return{'error': 'Validation Error', 'errors': valdiation_error.messages}, 400

    if category:
        category.name = category_details.get('name', category.name)
        category.description = category_details.get('description', category.description)
        db.session.commit()
        return CategorySchema().dump(category)


@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    current_user = admin_or_organizer_role_required()

    stmt = db.select(Category).filter_by(id=category_id)
    category = db.session.scalar(stmt)

    if not category:
        return{'error': 'Category not found.'}, 404
    if not (current_user.id == category.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this category.'}, 403
    
    if category:
        db.session.delete(category)
        db.session.commit()
        return {}, 200
    else:
        return{'error': 'Category not found.'}, 404
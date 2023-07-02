from flask import Blueprint, request
from init import db
from models.category import Category, CategorySchema
from blueprints.auth_bp import admin_or_organizer_role_required
from utils import validate_schema, get_resource_or_404

categories_bp = Blueprint('category', __name__, url_prefix='/categories')

# This route is used to get all the categories in the database and returns all the categories
@categories_bp.route('/')
def all_categories():
    stmt = db.select(Category)
    categories = db.session.scalars(stmt).all()
    if categories:
        return CategorySchema(many=True).dump(categories)
    else:
        return{'error': 'No categories found.'}, 404 # Not Found: The requested categories resource does not exist.

# This route is used to get a specific category in the database and returns the category if the category exists or returns an error if the category does not exist
@categories_bp.route('/<int:category_id>')
def one_category(category_id):
    category = get_resource_or_404(db.select(Category).filter_by(id=category_id), 'Category')
    return CategorySchema().dump(category)

# This route is used to create a new category in the database and returns the new category if the user is an admin or organizer or returns an error if the user is not an admin or organizer
@categories_bp.route('/', methods=['POST'])
def create_category():
    current_user = admin_or_organizer_role_required()
    category_details = validate_schema(CategorySchema(), request.json)

    name = category_details['name']
    description = category_details.get('description', '')

    category = Category(
        name = name,
        description = description,
        user_id = current_user.id
    )

    db.session.add(category)
    db.session.commit()
    return CategorySchema().dump(category), 201

# This route is used to update a specific category in the database and returns the updated category if the user is an admin or organizer or returns an error if the user is not an admin or organizer. Organizer can only update the category that they created.
@categories_bp.route('/<int:category_id>', methods=['PUT', 'PATCH'])
def update_category(category_id):
    current_user = admin_or_organizer_role_required()
    category = get_resource_or_404(db.select(Category).filter_by(id=category_id), 'Category')

    if not (current_user.id == category.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this category.'}, 403
    
    category_details = validate_schema(CategorySchema(), request.json)

    category.name = category_details.get('name', category.name)
    category.description = category_details.get('description', category.description)
    db.session.commit()
    return CategorySchema().dump(category)

# This route is used to delete a specific category in the database and returns an error if the user is not an admin or organizer. Organizer can only delete the category that they created.

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    current_user = admin_or_organizer_role_required()
    category = get_resource_or_404(db.select(Category).filter_by(id=category_id), 'Category')

    if not (current_user.id == category.user_id or current_user.is_admin):
        return{'error': 'You are not authorized to update this category.'}, 403
    
    db.session.delete(category)
    db.session.commit()
    return {}, 204
    
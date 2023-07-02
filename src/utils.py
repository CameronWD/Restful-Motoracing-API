from marshmallow.exceptions import ValidationError
from flask import abort
from init import db

def validate_schema(schema, data):
    print(data)
    try:
        validated_data = schema.load(data)
    except KeyError as key_error:
        missing_key = str(key_error).strip("'")
        abort(400, {'error': f'Request is missing {missing_key}.'})
    except ValidationError as validation_error:
        abort(400, {'error': 'Validation Error', 'errors': validation_error.messages})
    return validated_data
    
def get_resource_or_404(query, resource_name):
    resource = db.session.scalar(query)
    if not resource:
        abort(404,{'error': f'{resource_name} not found.'})
    return resource
    
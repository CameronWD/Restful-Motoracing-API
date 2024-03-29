from marshmallow.exceptions import ValidationError
from flask import abort
from init import db

# aims to catch all validation errors to make blueprint code much dryer 

def validate_schema(schema, data, partial=False):
    print(data)
    try:
        validated_data = schema.load(data, partial=partial)
    except KeyError as key_error:
        missing_key = str(key_error).strip("'")
        abort(400, {'error': f'Request is missing {missing_key}.'})
    except ValidationError as validation_error:
        abort(400, {'error': 'Validation Error', 'errors': validation_error.messages})
    return validated_data
    
# aims to catch all 404 errors to make blueprint code much dryer
def get_resource_or_404(query, resource_name):
    resource = db.session.scalar(query)
    if not resource:
        abort(404,{'error': f'{resource_name} not found.'})
    return resource
    
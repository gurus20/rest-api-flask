from functools import wraps
from flask import request, jsonify

def check_required_params():
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            errors = []
            request_data = {}
            
            if isinstance(request.json, dict):
                request_data = request.json
            else:
                errors.append("data is required in body as json")

            # Retrieve required params from the view class
            required_params = self.get_required_params()
            
            # Check if all required parameters are present in the request
            for param in required_params:
                if not request_data.get(param):
                    errors.append(f'{param} is required')
                    
            if errors:
                return jsonify({'message': 'bad request', 'errors': errors}), 400
            
            return func(self, request_data, *args, **kwargs)
        return wrapper
    return decorator

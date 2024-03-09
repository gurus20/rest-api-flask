import jwt
from functools import wraps
from flask import request, jsonify, current_app
from models.user_models import User

def check_required_params():
    def decorator(func):
        @wraps(func)
        def wrapper(self, current_user, *args, **kwargs):
            errors = []
            request_data = {}

            if isinstance(request.json, dict):
                request_data = request.json
            else:
                errors.append({"data": "data is required in body as json"})

            # Retrieve required params from the view class
            required_params = self.get_required_params()

            # Check if all required parameters are present in the request
            for param in required_params:
                if not request_data.get(param):
                    errors.append({param: f'{param} is required'})

            if errors:
                return jsonify({'message': 'bad request', 'errors': errors}), 400

            if current_user:
                return func(self, request_data, current_user, *args, **kwargs)
            else:
                return func(self, request_data, *args, **kwargs)
                
        return wrapper
    return decorator

def token_required(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        token = None

        # Check if Authorization header is present
        if 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            # Extract the token from the header
            token = auth_header.split()[1] if len(auth_header.split()) > 1 else None

        if not token:
            return jsonify({'error': 'access token is missing'}), 401

        try:
            # Verify the token
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(username=payload['user_id']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'access token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'invalid access token'}), 401

        return f(self, current_user, *args, **kwargs)

    return decorated

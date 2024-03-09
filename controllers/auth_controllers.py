from flask import jsonify, request
from flask.views import MethodView
from db.init_db import db
from models.user_models import User
from helpers.decorators import check_required_params

# Define your class-based view
class LoginView(MethodView):
    def post(self):
        return jsonify({"status": "ok"})


class SignupView(MethodView):
    @check_required_params()  
    def post(self, request_data):
        # Create a new user instance
        new_user = User(
            username=request_data.get('username'),
            email=request_data.get('email'),
            first_name=request_data.get('first_name'),
            middle_name=request_data.get('middle_name'),
            last_name=request_data.get('last_name')
        )
        
        # Set password (hash it)
        new_user.set_password(request_data.get('password'))

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    
    def get_required_params(self):
        return [
            "username",
            "email",
            "password",
            "first_name",
        ]


class RefreshTokenView(MethodView):
    def post(self):
        return jsonify({"status": "ok"})


class ChangePasswordView(MethodView):
    def post(self):
        return jsonify({"status": "ok"})


class ForgotPasswordView(MethodView):
    def post(self):
        return jsonify({"status": "ok"})


class SendOTPView(MethodView):
    def post(self):
        return jsonify({"status": "ok"})


class VerifyOTPView(MethodView):
    def post(self):
        return jsonify({"status": "ok"})

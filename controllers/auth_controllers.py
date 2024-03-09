import jwt
import secrets
from flask import jsonify, request, current_app
from flask.views import MethodView
from models.user_models import User
from helpers.decorators import check_required_params, token_required
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from db.init_db import db
from helpers.utils import send_mail
from helpers.common import cache

# Define your class-based view
class LoginView(MethodView):
    def post(self):
        errors = []
        data = {}

        if not isinstance(request.json, dict):
            errors.append({"data": "data is required in body as json"})
        else:
            data = request.json

        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        if not email and not username:
            errors.append({"email": "email or username is required"})
        
        if not password:
            errors.append({"password": "password is required"})

        if errors:
            response = {
                "message": "bad request",
                "errors": errors
            }
            return jsonify(response), 400
        
        # Check if the user exists by email or username
        user = User.query.filter((User.email == email) | (
            User.username == username)).first()
        
        if user and check_password_hash(user.password, password):
            # Generate JWT token
            exp = datetime.utcnow() + timedelta(hours=1)
            token = jwt.encode({
                'user_id': user.username,
                'exp': exp},
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            response = {
                "access_token": token,
                "expiry": exp
            }
            return jsonify(response)
        else:
            # Invalid credentials
            
            response = {
                "message": "Invalid credentials",
                "errors": "Invalid username/email and password"
            }
            return jsonify(response), 401


class SignupView(MethodView):
    @check_required_params()
    def post(self, request_data):
        # Create a new user instance
        errors = []

        # Check if username or email already exists
        if User.query.filter_by(username=request_data['username']).first():
            errors.append(
                {"username": "username already exist, use different username"})

        if User.query.filter_by(email=request_data['email']).first():
            errors.append(
                {"email": "Email already exist, use different email"})

        if errors:
            response = {
                "message": "bad request",
                "errors": errors
            }
            return jsonify(response), 400

        new_user = User(
            username=request_data.get('username'),
            email=request_data.get('email'),
            first_name=request_data.get('first_name'),
            middle_name=request_data.get('middle_name'),
            last_name=request_data.get('last_name')
        )

        # Set password (hash it)
        new_user.set_password(request_data.get('password'))

        try:
            # Add user to the database
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'message': 'User created successfully'}), 201
        except Exception as e:
            # Handle database error
            db.session.rollback()
            return jsonify({'error': 'Failed to create user'}), 500

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
    @token_required
    @check_required_params()
    def post(self, request_data, user):
        if not user:
            return jsonify({'error': 'User not found or token invalid'}), 404
        
        current_password = request_data.get("current_password")
        new_password = request_data.get("new_password")

        # # Check if the current password matches
        if not check_password_hash(user.password, current_password):
            return jsonify({'error': 'Incorrect current password'}), 401

        try:
            # Update the password
            user.set_password(new_password)
            db.session.commit()
        except Exception as e:
            # Handle database error
            db.session.rollback()
            return jsonify({'error': 'Failed to change password'}), 500
        return jsonify({"status": "ok"})
    
    def get_required_params(self):
        return [
            "current_password",
            "new_password"
        ]
 

class ForgotPasswordView(MethodView):
    def post(self):
        return jsonify({"status": "ok"})

class VerifyEmailView(MethodView):
    def get(self):
        token = request.args.get('token')

        if not token:
            return "Unauthorized, Token is missing", 401

        # here email verify logic
        username = cache.get(token)
        user = User.query.filter_by(username=username).first()

        if not user:
            return "Unauthorized, Token is missing", 404

        try:
            # Update the password
            user.email_verified = True
            db.session.commit()
            return jsonify({'message': 'Email verified succesfully'})
        except Exception as e:
            # Handle database error
            db.session.rollback()
            return jsonify({'error': 'Failed to verify email'}), 500
        return jsonify({'error': 'Failed to verify email'}), 500


    @token_required
    def post(self, user):
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # generate token and save
        token = secrets.token_urlsafe(16)
        cache.set(token, user.username)

        send_mail(
            recipients=[user.email],
            subject="Verify your email",
            template="email/verify_email.html",
            username=user.username,
            verification_link=f"{request.base_url}?token={token}",
        )

        return jsonify({"message": "verification link sent to your email"}) 


class SendOTPView(MethodView):
    def post(self):
        return jsonify({"status": "ok"})


class VerifyOTPView(MethodView):
    def post(self):
        return jsonify({"status": "ok"})

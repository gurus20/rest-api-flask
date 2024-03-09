from flask import Blueprint
from controllers.auth_controllers import (
    LoginView,
    SignupView,
    RefreshTokenView,
    ChangePasswordView,
    ForgotPasswordView,
    VerifyOTPView,
    SendOTPView
)

# Create a Blueprint object
# Add the class-based view to the Blueprint with a route
bp = Blueprint("routes", __name__)


# Define your routes
BASE_ENDPOINT = "/api/v1/auth"


bp.add_url_rule(
    f"{BASE_ENDPOINT}/login",
    view_func=LoginView.as_view("login"))

bp.add_url_rule(
    f"{BASE_ENDPOINT}/signup",
    view_func=SignupView.as_view("signup"))

bp.add_url_rule(
    f"{BASE_ENDPOINT}/refresh",
    view_func=RefreshTokenView.as_view("refresh"))

bp.add_url_rule(
    f"{BASE_ENDPOINT}/change-password",
    view_func=ChangePasswordView.as_view("change_password"))

bp.add_url_rule(
    f"{BASE_ENDPOINT}/forgot-password",
    view_func=ForgotPasswordView.as_view("forgot_password"))

bp.add_url_rule(
    f"{BASE_ENDPOINT}/send-otp",
    view_func=VerifyOTPView.as_view("send_otp"))

bp.add_url_rule(
    f"{BASE_ENDPOINT}/verify-otp",
    view_func=SendOTPView.as_view("verify_otp"))

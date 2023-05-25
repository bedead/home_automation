from flask import Blueprint, render_template

# Create a blueprint for the home routes
auth_page_bp = Blueprint("auth_page", __name__)

# Define the route for the home page
@auth_page_bp.route("/auth/signup")
def signup():
    return render_template("/auth/signup_page.html")

@auth_page_bp.route("/auth/signin")
def signin():
    return render_template("/auth/signin_page.html")

@auth_page_bp.route("/auth/email_verify")
def email_verificatation():
    pass


@auth_page_bp.route("/auth/password_recovery")
def password_recovery():
    pass

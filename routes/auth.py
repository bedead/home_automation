from flask import Blueprint, render_template

# Create a blueprint for the home routes
auth_page_bp = Blueprint("auth_page", __name__)

# Define the route for the home page
@auth_page_bp.route("/auth/")
def home():
    pass

@auth_page_bp.route("/auth/signup")
def about():
    return render_template("/auth/signup_page.html")

@auth_page_bp.route("/auth/signin")
def about():
    return render_template("/auth/signin_page.html")

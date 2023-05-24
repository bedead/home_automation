from flask import Blueprint, render_template

# Create a blueprint for the home routes
home_bp = Blueprint("home", __name__)

# Define the route for the home page
@home_bp.route("/")
def home():
    return render_template('home.html')

# You can define additional routes within the same blueprint if needed
@home_bp.route("/about")
def about():
    return "This is the about page."

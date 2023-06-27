from flask import Blueprint, render_template

# Create a blueprint for the home routes
base_page_bp = Blueprint("landing_page", __name__)

# Define the route for the home page
@base_page_bp.route("/")
def home():
    return render_template('/base/landing_page.html')




@base_page_bp.route("/services")
def services():
    return render_template("/base/services_page.html")



@base_page_bp.route("/become_a_aggregator")
def become_aggregator():
    return render_template("/base/become_aggregator_page.html")



@base_page_bp.route("/products")
def products():
    return render_template("/base/download_page.html")



@base_page_bp.route("/about")
def about():
    return render_template("/base/about_page.html")

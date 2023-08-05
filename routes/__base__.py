"""
The base_page_bp blueprint is responsible for rendering HTML templates and sending files 
for download. Here's a breakdown of the code:
"""

from flask import Blueprint, render_template, send_file

# Create a blueprint for the home routes
base_page_bp = Blueprint("landing_page", __name__)


"""
The home() function handles the route for the home page ("/"). 
It renders the "landing_page.html" template.
The services() function handles the route for the services page ("/services"). 
It renders the "services_page.html" template.
The products() function handles the route for the products page ("/products"). 
It renders the "download_page.html" template.
The routes for downloading specific files for different categories are defined 
using routes like market_player_raspbian_64_bit, aggregator_raspbian_64_bit, 
and utility_raspbian_64_bit. These routes use the send_file() function to send 
files for download. The path variable specifies the location of the files on the server.
The about() function handles the route for the about page ("/about"). 
It renders the "about_page.html" template.
"""


# Define the route for the home page
@base_page_bp.route("/")
def home():
    return render_template("/base/landing_page.html")


@base_page_bp.route("/services")
def services():
    return render_template("/base/services_page.html")


@base_page_bp.route("/products")
def products():
    return render_template("/base/download_page.html")


@base_page_bp.route("/products/market_player/raspbian_64_bit")
def market_player_raspbian_64_bit():
    path = "E:/Projects/Python/home_automation/static/files/Market Player"
    return send_file(path, as_attachment=True)


@base_page_bp.route("/products/aggregator/raspbian_64_bit")
def aggregator_raspbian_64_bit():
    path = "E:/Projects/Python/home_automation/static/files/Aggregator"
    return send_file(path, as_attachment=True)


@base_page_bp.route("/products/utility/raspbian_64_bit")
def utility_raspbian_64_bit():
    path = "E:/Projects/Python/home_automation/static/files/Utility"
    return send_file(path, as_attachment=True)


@base_page_bp.route("/about")
def about():
    return render_template("/base/about_page.html")

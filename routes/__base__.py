from flask import Blueprint, render_template, send_file

# Create a blueprint for the home routes
base_page_bp = Blueprint("landing_page", __name__)


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

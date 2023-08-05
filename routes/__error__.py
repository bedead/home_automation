"""
The error_page_bp blueprint is created using Blueprint from the Flask framework. 
It's designed to manage routes 
related to different error scenarios within the application.
"""

from flask import Blueprint, redirect, render_template, request, url_for, session

# Create a blueprint for the home routes
error_page_bp = Blueprint("error_page", __name__)

"""
error_404(): This route handles the scenario where a user encounters a "404 - 
Page Not Found" error. It renders the 404_page.html template, which likely 
contains information to inform the user about the error.

error_403(): This route is responsible for displaying a "403 - Forbidden" error 
page. It renders the 403_page.html template, which informs users that 
they do not have the necessary permissions to access a particular resource.

under_construction(): This route represents a page for indicating that a particular 
section of the website is still under construction. It renders the 
under_construction_page.html template, which informs users about the ongoing development process.

unknown_error(): This route is used to display a generic "Unknown Error" 
page. It renders the unknown_error_page.html template, which can provide users 
with a message stating that an unexpected error has occurred.

base_error(status, message): This route is a catch-all for rendering a 
more general error page. It takes in the status and message as 
route parameters. This could be utilized for displaying custom error messages, potentially with 
specific status codes, and renders the base_error_page.html template.
"""


@error_page_bp.route("/error/404")
def error_404():
    return render_template("/error/404_page.html")


@error_page_bp.route("/error/403")
def error_403():
    return render_template("/error/403_page.html")


@error_page_bp.route("/error/underconstruction")
def under_construction():
    return render_template("/error/under_construction_page.html")


@error_page_bp.route("/error/unknown")
def unknown_error():
    return render_template("/error/unknown_error_page.html")


@error_page_bp.route("/error/<status>/<message>")
def base_error(status, message):
    return render_template(
        "/error/base_error_page.html", status=status, message=message
    )

from flask import Blueprint, redirect, render_template, request, url_for, session
# Create a blueprint for the home routes
error_page_bp = Blueprint("error_page", __name__)

@error_page_bp.route("/error/404")
def error_404():
    return render_template('/error/404_page.html')

@error_page_bp.route("/error/403")
def error_403():
    return render_template('/error/403_page.html')

@error_page_bp.route("/error/underconstruction")
def under_construction():
    return render_template('/error/under_construction_page.html')


@error_page_bp.route("/error/<status>/<message>")
def base_error(status, message):
    return render_template('/error/base_error_page.html',
                            status=status,
                            message=message
                            )
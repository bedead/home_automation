from flask import Blueprint, redirect, render_template, request, url_for, session
# Create a blueprint for the home routes
error_page_bp = Blueprint("error_page", __name__)

@error_page_bp.route("/error//")
def error_404():
    return "Error 404 | Page not found"
from flask import Blueprint, redirect, render_template, request, url_for,session

# Create a blueprint for the home routes
dashboard_page_bp = Blueprint("dashboard_page", __name__)

@dashboard_page_bp.route("/user/consumer")
def consumer_dashboard():
    if session:
        return render_template('/dashboard/consumer_page.html')
    else:
        return redirect(url_for('auth_page.signin'))
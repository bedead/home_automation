from flask import Blueprint, redirect, render_template, request, url_for,session

# Create a blueprint for the home routes
aggregator_page_bp = Blueprint("aggregator_page", __name__)


@aggregator_page_bp.route("/user/aggregator/dashboard")
def aggregator_dashboard():
    if session['user-type'] == "Aggregator":
        return render_template('/aggregator/aggregator_dashboard_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
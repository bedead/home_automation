from flask import Blueprint, redirect, render_template, request, url_for,session

# Create a blueprint for the home routes
producer_page_bp = Blueprint("producer_page", __name__)



@producer_page_bp.route("/user/producer/dashboard")
def producer_dashboard():
    if session['user-type'] =="Producer":
        return render_template('/producer/producer_dashboard_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
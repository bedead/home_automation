from flask import Blueprint, redirect, render_template, request, url_for,session

# Create a blueprint for the home routes
prosumer_page_bp = Blueprint("prosumer_page", __name__)



@prosumer_page_bp.route("/user/prosumer/dashboard")
def prosumer_dashboard():
    if session['user-type'] =="Prosumer":
        return render_template('/prosumer/prosumer_dashboard_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
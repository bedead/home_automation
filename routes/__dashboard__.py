from flask import Blueprint, redirect, render_template, request, url_for,session

# Create a blueprint for the home routes
dashboard_page_bp = Blueprint("dashboard_page", __name__)

@dashboard_page_bp.route("/user/consumer")
def consumer_dashboard():
    if session['user-type'] =="Consumer":
        return render_template('/dashboard/consumer_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    




@dashboard_page_bp.route("/user/producer")
def producer_dashboard():
    if session['user-type'] =="Producer":
        return render_template('/dashboard/producer_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    



@dashboard_page_bp.route("/user/prosumer")
def prosumer_dashboard():
    if session['user-type'] =="Prosumer":
        return render_template('/dashboard/prosumer_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    


@dashboard_page_bp.route("/user/aggregator")
def aggregator_dashboard():
    if session['user-type'] == "Aggregator":
        return render_template('/dashboard/aggregator_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
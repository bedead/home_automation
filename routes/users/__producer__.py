from flask import Blueprint, redirect, render_template, request, url_for,session

# Create a blueprint for the home routes
producer_page_bp = Blueprint("producer_page", __name__)



@producer_page_bp.route("/user/producer/dashboard")
def producer_dashboard():
    access = session['user-type'] =="Producer"
    if access:
        return render_template('/producer/producer_dashboard_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    elif not access:
        return redirect(url_for('error_page.error_403'))
    else:
        return "Some error occured."
    


@producer_page_bp.route("/user/producer/history")
def producer_history():
    access = session['user-type'] =="Producer"

    if access:
        return render_template('/producer/producer_history_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    elif not access:
        return redirect(url_for('error_page.error_403'))
    else:
        return "Some error occured."





@producer_page_bp.route("/user/producer/monitor")
def producer_monitor():
    access = session['user-type'] =="Producer"
    if access:
        return render_template('/producer/producer_monitor_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    elif not access:
        return redirect(url_for('error_page.error_403'))
    else:
        return "Some error occured."





@producer_page_bp.route("/user/producer/settings")
def producer_settings():
    access = session['user-type'] =="Producer"
    if access:
        return render_template('/producer/producer_settings_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    elif not access:
        return redirect(url_for('error_page.error_403'))
    else:
        return "Some error occured."

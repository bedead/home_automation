from flask import Blueprint, redirect, render_template, request, url_for,session

from routes.utility.fetch_Data import fetch_From_Producer_Monitor

# Create a blueprint for the home routes
producer_page_bp = Blueprint("producer_page", __name__)



@producer_page_bp.route("/user/producer/dashboard")
def producer_dashboard():
    if session:
        if not (session['user-type'] =="Producer"):
            print("Uer id: ", session['user_id'])
            return redirect(url_for('error_page.error_403'))

        return render_template('/producer/producer_dashboard_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."
    


@producer_page_bp.route("/user/producer/history")
def producer_history():
    if session:
        if not (session['user-type'] =="Producer"):
            print("Uer id: ", session['user_id'])
            return redirect(url_for('error_page.error_403'))

        return render_template('/producer/producer_history_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."





@producer_page_bp.route("/user/producer/monitor")
def producer_monitor():
    if session:
        if not (session['user-type'] =="Producer"):
            print("Uer id: ", session['user_id'])
            return redirect(url_for('error_page.error_403'))
        
        data = fetch_From_Producer_Monitor(session['user_id'])

        return render_template('/producer/producer_monitor_page.html', data=data)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."





@producer_page_bp.route("/user/producer/settings")
def producer_settings():
    if session:
        if not (session['user-type'] =="Producer"):
            print("Uer id: ", session['user_id'])
            return redirect(url_for('error_page.error_403'))

        return render_template('/producer/producer_settings_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."

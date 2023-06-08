from flask import Blueprint, redirect, render_template, request, url_for,session

from routes.utility.fetch_Data import fetch_From_Aggregator_Dashboard

# Create a blueprint for the home routes
aggregator_page_bp = Blueprint("aggregator_page", __name__)


@aggregator_page_bp.route("/user/aggregator/dashboard")
def aggregator_dashboard():
    if session:
        if not (session['user-type'] == "Aggregator"):
            return redirect(url_for('error_page.error_403'))
        
        print("Uer id: ", session['user_id'])
        data = fetch_From_Aggregator_Dashboard()
        
        return render_template('/aggregator/aggregator_dashboard_page.html', data=data)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."
    
@aggregator_page_bp.route("/user/aggregator/history")
def aggregator_history():
    if session:
        if not (session['user-type'] == "Aggregator"):
            return redirect(url_for('error_page.error_403'))
        print("Uer id: ", session['user_id'])

        return render_template('/aggregator/aggregator_history_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."
    
@aggregator_page_bp.route("/user/aggregator/settings")
def aggregator_settings():
    if session:
        if not (session['user-type'] == "Aggregator"):
            return redirect(url_for('error_page.error_403'))
        print("Uer id: ", session['user_id'])

        return render_template('/aggregator/aggregator_settings_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."
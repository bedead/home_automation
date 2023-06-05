from flask import Blueprint, redirect, render_template, request, url_for,session
from routes.utility.fetch_Data import fetch_From_Consumer_Dashboard, fetch_From_Consumer_History, fetch_From_Consumer_Monitor

# Create a blueprint for the home routes
consumer_page_bp = Blueprint("consumer_page", __name__)


@consumer_page_bp.route("/user/consumer/dashboard")
def consumer_dashboard():
    if session:
        print("Uer id: ", session['user_id'])

        if not (session['user-type'] =="Consumer"): 
            return redirect(url_for('error_page.error_403'))

        total_trades, average_wh_hour, average_cost_hour, access_grants, access_rejected, some_other = fetch_From_Consumer_Dashboard(session['user_id'])
        
        return render_template('/consumer/consumer_dashboard_page.html', 
                               total_trades=total_trades,
                               average_wh_hour=average_wh_hour,
                               average_cost_hour=average_cost_hour,
                               access_grants=access_grants,
                               access_rejected=access_rejected,
                               some_other=some_other)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."





@consumer_page_bp.route("/user/consumer/history")
def consumer_history():
    if session:
        print("Uer id: ", session['user_id'])

        if not (session['user-type'] =="Consumer"):
            return redirect(url_for('error_page.error_403'))
        
        data = fetch_From_Consumer_History(session['user_id'])

        return render_template('/consumer/consumer_history_page.html', data=data)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."





@consumer_page_bp.route("/user/consumer/monitor")
def consumer_monitor():
    if session['user-type'] =="Consumer":
        print("Uer id: ", session['user_id'])

        if not (session['user-type'] =="Consumer"):
            return redirect(url_for('error_page.error_403'))

        data = fetch_From_Consumer_Monitor(session['user_id'])

        return render_template('/consumer/consumer_monitor_page.html', data=data)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."





@consumer_page_bp.route("/user/consumer/settings")
def consumer_settings():
    if session['user-type'] =="Consumer":

        if not (session['user-type'] =="Consumer"):
            return redirect(url_for('error_page.error_403'))
        
        return render_template('/consumer/consumer_settings_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."




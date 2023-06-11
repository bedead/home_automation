from flask import Blueprint, redirect, render_template, request, url_for,session

from routes.utility.fetch_Data import fetch_From_Producer_Monitor

# Create a blueprint for the home routes
prosumer_page_bp = Blueprint("prosumer_page", __name__)



@prosumer_page_bp.route("/user/prosumer/dashboard")
def prosumer_dashboard():
    if session:
        if not (session['user-type'] =="Prosumer"):
            print("Uer id: ", session['user_id'])
            return redirect(url_for('error_page.error_403'))

        return render_template('/producer/producer_dashboard_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."
    


@prosumer_page_bp.route("/user/procumer/history")
def prosumer_history():
    if session:
        if not (session['user-type'] =="Prosumer"):
            print("Uer id: ", session['user_id'])
            return redirect(url_for('error_page.error_403'))

        return render_template('/producer/producer_history_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."


@prosumer_page_bp.route("/user/prosumer/monitor/sell", methods=['POST'])
def sell_energy():
    print('sell endpoint trigger')

    return redirect(url_for('procumer_page.procumer_monitor'))

@prosumer_page_bp.route("/user/prosumer/monitor")
def prosumer_monitor():
    if session:
        if not (session['user-type'] =="Prosumer"):
            print("Uer id: ", session['user_id'])
            return redirect(url_for('error_page.error_403'))
        
        # data = fetch_From_Producer_Monitor(session['user_id'])

        return render_template('/producer/producer_monitor_page.html', data=None)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."





@prosumer_page_bp.route("/user/procumer/settings")
def procumer_settings():
    if session:
        if not (session['user-type'] =="Procumer"):
            print("Uer id: ", session['user_id'])
            return redirect(url_for('error_page.error_403'))

        return render_template('/producer/producer_settings_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."

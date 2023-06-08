from flask import Blueprint, redirect, render_template, request, url_for,session
from routes.utility.fetch_Data import fetch_From_Consumer_Dashboard, fetch_From_Consumer_History, fetch_From_Consumer_Monitor
from routes.__config__ import Config
from routes.utility.general_methods import get_User_Session_Details

# Create a blueprint for the home routes
consumer_page_bp = Blueprint("consumer_page", __name__)
supabase_ = Config.supabase_


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
        data = fetch_From_Consumer_History(session['user_id'])

        if not (session['user-type'] =="Consumer"):
            return redirect(url_for('error_page.error_403'))
        
        return render_template('/consumer/consumer_history_page.html', data=data)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."



def insert_One_Into_Aggregator_Dashboard(wh_hour):
    user_email, user_type, user_id = get_User_Session_Details()
    data = {
        "user_id": user_id,
        "user_email":user_email,
        "wh_hours":wh_hour,
        "user_type":user_type,
        "status": 'PENDING',
    }
    table_name = 'aggregator_dasboard'
    try:
        response = supabase_.table(table_name=table_name).insert(data).execute()
        print(response)
    except Exception as e:
        return redirect(url_for('error_page.unknown_error'))

@consumer_page_bp.route("/user/consumer/monitor/buy_energy", methods=['POST'])
def buy_energy():
    if (request.method == 'POST'):
        wh_hour = request.form['wh_hour']
        insert_One_Into_Aggregator_Dashboard(wh_hour)
        return redirect(url_for('consumer_page.consumer_monitor', status=True))

@consumer_page_bp.route("/user/consumer/monitor")
@consumer_page_bp.route("/user/consumer/monitor/<status>")
def consumer_monitor(status=None):
    if session:
        print("Uer id: ", session['user_id'])
        data = fetch_From_Consumer_Monitor(session['user_id'])
        total_current = data[-1]['current_total']
        total_w = data[-1]['power_total']

        if not (session['user-type'] =="Consumer"):
            return redirect(url_for('error_page.error_403'))
        
        return render_template('/consumer/consumer_monitor_page.html', data=data, total_current=total_current, total_w=total_w, status=status)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."





@consumer_page_bp.route("/user/consumer/settings")
def consumer_settings():
    if session:

        if not (session['user-type'] =="Consumer"):
            return redirect(url_for('error_page.error_403'))
        
        return render_template('/consumer/consumer_settings_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."



from flask import Blueprint, redirect, render_template, request, url_for,session
from routes.data_generator.triple_des import encrypt_Text
from routes.utility.fetch_Data import fetch_From_Consumer_Dashboard, fetch_From_Consumer_History, fetch_From_Consumer_Monitor
from routes.__config__ import Config
from routes.utility.gen_secret_key_helper import get_Shared_Key
from routes.utility.general_methods import get_User_Session_Details, get_User_Session_Other_Public_Key, get_User_Session_Private_Key
from datetime import datetime

# Create a blueprint for the home routes
consumer_page_bp = Blueprint("consumer_page", __name__)
supabase_ = Config.supabase_


@consumer_page_bp.route("/user/consumer/dashboard")
def consumer_dashboard():
    if session:
        print("Uer id: ", session['user_id'])

        if not (session['user-type'] =="Consumer"): 
            return redirect(url_for('error_page.error_403'))

        try:
            total_trades, average_wh_hour, average_cost_hour, access_grants, access_rejected, some_other = fetch_From_Consumer_Dashboard(session['user_id'])
        except UnboundLocalError as e:
            # no internet (create new error page for this type)
            return redirect(url_for('error_page.unknown_error'))
        except TypeError as e:
            return redirect(url_for('error_page.unknown_error'))
            
        
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



def insert_One_Into_Aggregator_Dashboard(data: dict):
    user_email, user_type, user_id = get_User_Session_Details()
    table_name = 'aggregator_dasboard'
    created_at = datetime.now()
    row = {
        'created_at': str(created_at),
        "user_id": user_id,
        "user_email":user_email,
        "user_type":user_type,
        "status": 'PENDING',
        'type': 'BUY'
    }    
    
    for key, value in data.items():
        row[key] = value
    try:
        response = supabase_.table(table_name=table_name).insert(row).execute()
    except Exception as e:
        return redirect(url_for('error_page.unknown_error'))

@consumer_page_bp.route("/user/consumer/monitor/buy_energy", methods=['POST'])
def buy_energy():
    if (request.method == 'POST'):
        first = request.form['12-1am'];second = request.form['1-2am'];third = request.form['2-3am']
        four = request.form['3-4am'];five = request.form['4-5am'];six = request.form['5-6am']
        seven = request.form['6-7am'];eight = request.form['7-8am'];nine = request.form['8-9am']
        ten = request.form['9-10am'];eleven = request.form['10-11am'];twelve = request.form['11-12am']
        
        first_pm = request.form['12-1pm'];second_pm = request.form['1-2pm'];third_pm = request.form['2-3pm']
        four_pm = request.form['3-4pm'];five_pm = request.form['4-5pm'];six_pm = request.form['5-6pm']
        seven_pm = request.form['6-7pm'];eight_pm = request.form['7-8pm'];nine_pm = request.form['8-9pm']
        ten_pm = request.form['9-10pm'];eleven_pm = request.form['10-11pm'];twelve_pm = request.form['11-12pm']

        data = {
            '12-1am': first,'1-2am': second,'2-3am': third,
            '3-4am': four,'4-5am': five,'5-6am': six,
            '6-7am': seven,'7-8am': eight,'8-9am': nine,
            '9-10am': ten,'10-11am': eleven,'11-12am': twelve,
            '12-1pm': first_pm,'1-2pm': second_pm,'2-3pm': third_pm,
            '3-4pm': four_pm,'4-5pm': five_pm,'5-6pm': six_pm,
            '6-7pm': seven_pm,'7-8pm': eight_pm,'8-9pm': nine_pm,
            '9-10pm': ten_pm,'10-11pm': eleven_pm,'11-12pm': twelve_pm,
        }
    
        aggregator_public_key = get_User_Session_Other_Public_Key()
        user_private_key = get_User_Session_Private_Key()
        shared_key_hex = get_Shared_Key(private_key_hex=user_private_key, public_key_hex=aggregator_public_key)

        shared_key_hex = shared_key_hex[:24]
        print("Shared key :",shared_key_hex)

        for key,each_d in data.items():
            hex_ciphertext_each_d = encrypt_Text(plaintext=each_d, secret_key=shared_key_hex)
            data[key] = hex_ciphertext_each_d

        insert_One_Into_Aggregator_Dashboard(data)
        return redirect(url_for('consumer_page.consumer_monitor', status=True))

@consumer_page_bp.route("/user/consumer/monitor")
@consumer_page_bp.route("/user/consumer/monitor/<status>")
def consumer_monitor(status=None):
    if session:
        if not (session['user-type'] =="Consumer"):
            return redirect(url_for('error_page.error_403'))

        print("Uer id: ", session['user_id'])
        total_current = 0
        total_w = 0
        data = []
        try:
            data = fetch_From_Consumer_Monitor(session['user_id'])
            total_current = data[-1]['current_total']
            total_w = data[-1]['power_total']
        except TypeError as e:
            return redirect(url_for('error_page.unknown_error'))
        except IndexError as e:
            # (no enough entries in consumer_monitor table in database)
            return redirect(url_for('error_page.unknown_error'))
        
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



from datetime import datetime
from flask import Blueprint, redirect, render_template, request, url_for,session
from routes.__config__ import Config
from routes.data_generator.triple_des import encrypt_Text
from routes.utility.fetch_Data import fetch_From_Producer_Monitor, fetch_From_Producer_Dashboard, fetch_From_Producer_History
from routes.utility.gen_secret_key_helper import get_Shared_Key
from routes.utility.general_methods import get_User_Session_Details, get_User_Session_Other_Public_Key, get_User_Session_Private_Key, get_User_Aggregator_Id

# Create a blueprint for the home routes
producer_page_bp = Blueprint("producer_page", __name__)
supabase_ = Config.supabase_


@producer_page_bp.route("/user/producer/dashboard")
def producer_dashboard():
    if session:
        if not (session['user-type'] =="Producer"):
            return redirect(url_for('error_page.error_403'))

        print("User id: ", session['user_id'])

        total_trades, average_wh_hour, average_cost_hour, access_grants, access_rejected, some_other = 0, 0, 0, 0, 0, 0
        try:
            total_trades, average_wh_hour, average_cost_hour, access_grants, access_rejected, some_other = fetch_From_Producer_Dashboard(session['user_id'])
        except UnboundLocalError as e:
            # no internet (create new error page for this type)
            return redirect(url_for('error_page.unknown_error'))
        except TypeError as e:
            return redirect(url_for('error_page.unknown_error'))

        return render_template('/producer/producer_dashboard_page.html',total_trades=total_trades,
                               average_wh_hour=average_wh_hour,
                               average_cost_hour=average_cost_hour,
                               access_grants=access_grants,
                               access_rejected=access_rejected,
                               some_other=some_other)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."

@producer_page_bp.route("/user/producer/history")
def producer_history():
    if session:
        if not (session['user-type'] =="Producer"):
            return redirect(url_for('error_page.error_403'))

        print("User id: ", session['user_id'])

        data = fetch_From_Producer_History(session['user_id'])

        return render_template('/producer/producer_history_page.html', data=data)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."

def insert_One_Into_Aggregator_Dashboard(data: dict):
    user_email, user_type, user_id = get_User_Session_Details()
    aggregator_id = get_User_Aggregator_Id()
    table_name = 'aggregator_dashboard'
    created_at = datetime.now()
    row = {
        'created_at': str(created_at),
        "user_id": user_id,
        "user_email":user_email,
        "user_type":user_type,
        "status": 'PENDING',
        'type': 'SELL',
        'aggregator_id': aggregator_id
    }    
    
    for key, value in data.items():
        row[key] = value
    # print(row)
    try:
        response = supabase_.table(table_name=table_name).insert(row).execute()
        # print(response.data)
    except Exception as e:
        return redirect(url_for('error_page.unknown_error'))

@producer_page_bp.route("/user/producer/monitor/sell_energy", methods=['POST'])
def sell_energy():
    # print('sell endpoint trigger')
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

        print("Sell request made.")
        return redirect(url_for('producer_page.producer_monitor', status=True))

def get_Total_Current_And_Power(data):
    total_current = 0
    total_w = 0

    for each_row in data:
        for key, values in each_row.items():
            if (key == 'current'):
                total_current += values
            elif (key == 'power'):
                total_w += values

    return round(total_current, 1), round(total_w, 2)

@producer_page_bp.route("/user/producer/monitor")
@producer_page_bp.route("/user/producer/monitor/<status>")
def producer_monitor(status=None):
    if session:
        if not (session['user-type'] =="Producer"):
            return redirect(url_for('error_page.error_403'))
        
        print("User id: ", session['user_id'])

        data = []
        # try:
        data = fetch_From_Producer_Monitor(session['user_id'])
        print(data)
        total_current, total_w = get_Total_Current_And_Power(data)

        return render_template('/producer/producer_monitor_page.html', data=data, total_current=total_current, total_w=total_w, status=status)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."

@producer_page_bp.route("/user/producer/settings")
def producer_settings():
    if session:
        if not (session['user-type'] =="Producer"):
            return redirect(url_for('error_page.error_403'))

        print("User id: ", session['user_id'])

        return render_template('/producer/producer_settings_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."

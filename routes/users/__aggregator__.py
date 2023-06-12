from flask import Blueprint, redirect, render_template, request, url_for,session
from routes.__config__ import Config
from routes.data_generator.triple_des import decrypt_Text

from routes.utility.fetch_Data import fetch_All_From_Aggregator_Dashboard, fetch_One_From_Aggregator_Dashboard
from routes.utility.gen_secret_key_helper import get_Shared_Key
from routes.utility.general_methods import get_User_Session_Private_Key, get_User_User_Id

supabase = Config.supabase_

# Create a blueprint for the home routes
aggregator_page_bp = Blueprint("aggregator_page", __name__)

def decode_All_Data():
    aggregator_id = get_User_User_Id()
    data = fetch_All_From_Aggregator_Dashboard(aggregator_id=aggregator_id)
    user_private_key = get_User_Session_Private_Key()
    # print("Aggregator private key :",user_private_key)
    # print(data)
    dashboard_data = []
    for each_row in data:
        row_user_id = each_row['user_id']
        user_row_public_key = get_Public_Key_For_ID(row_user_id)
        
        shared_key_hex = get_Shared_Key(private_key_hex=user_private_key, public_key_hex=user_row_public_key)
        shared_key_hex = shared_key_hex[:24]
        print("Shared key :", shared_key_hex)

        dashboard_row = {}
        for key,each_d in each_row.items():
            if (('am' in key) or ('pm' in key)):
                plain_text_each_d = decrypt_Text(cipher_text=each_d, secret_key=shared_key_hex)
                dashboard_row[key] = plain_text_each_d
            else:
                dashboard_row[key] = each_d
        dashboard_data.append(dashboard_row)

    return dashboard_data

def decode_One_Data(request_user_id: str, created_at: str):
    dashboard_row = {}
    detail_data = fetch_One_From_Aggregator_Dashboard(user_id=request_user_id, created_at=created_at)
    detail_data = detail_data[0]

    row_user_id = detail_data['user_id']
    user_private_key = get_User_Session_Private_Key()
    user_row_public_key = get_Public_Key_For_ID(row_user_id)
    
    shared_key_hex = get_Shared_Key(private_key_hex=user_private_key, public_key_hex=user_row_public_key)
    shared_key_hex = shared_key_hex[:24]
    print("Shared key :", shared_key_hex)

    for key,each_d in detail_data.items():
        if (('am' in key) or ('pm' in key)):
            plain_text_each_d = decrypt_Text(cipher_text=each_d, secret_key=shared_key_hex)
            dashboard_row[key] = plain_text_each_d
        else:
            dashboard_row[key] = each_d

    return dashboard_row

def get_Public_Key_For_ID(user_id):
    table_name = 'private_data'
    response1= supabase.table(table_name=table_name).select('public_key').eq('user_id',user_id).execute()
    user_public_key = response1.data[0]['public_key']

    return user_public_key

@aggregator_page_bp.route("/user/aggregator/dashboard")
def aggregator_dashboard():
    if session:
        if not (session['user-type'] == "Aggregator"):
            return redirect(url_for('error_page.error_403'))
        
        print("User id: ", session['user_id'])

        data = decode_All_Data()
        print(data)
        return render_template('/aggregator/aggregator_dashboard_page.html', data=data)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."

@aggregator_page_bp.route("/user/aggregator/dashboard/request_details/")
def aggregator_user_details():
    if session:
        if not (session['user-type'] == "Aggregator"):
            return redirect(url_for('error_page.error_403'))
        
        print("User id: ", session['user_id'])
        
        request_user_id = request.args.get('user_id', None)
        created_at = request.args.get('created_at', None)
        data = decode_One_Data(request_user_id=request_user_id, created_at=created_at)

        return render_template('/aggregator/aggregator_dashboard_request_details_page.html', data=data)
    
    
    
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
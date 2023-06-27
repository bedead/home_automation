from flask import Blueprint, redirect, render_template, request, url_for,session

from routes.__config__ import Config
from routes.utility.fetch_Data import fetch_All_Aggregator_From_Private_Data, fetch_All_Buy_Request_From_Aggregator_Dashboard, fetch_All_Market_Players_From_Private_Data, fetch_All_Sell_Request_From_Aggregator_Dashboard

# Create a blueprint for the home routes
utility_page_bp = Blueprint("utility_page", __name__)
supabase_ = Config.supabase_


@utility_page_bp.route("/admin/utility/dashboard")
def utility_dashboard():
    if session:
        if not (session['user-type'] =="Utility"): 
            return redirect(url_for('error_page.error_403'))

        print("User id: ", session['user_id'])

        return render_template('/utililty/utility_main_dashboard_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."

@utility_page_bp.route("/admin/utility/private_data")
def utility_private_data():
    if session:
        if not (session['user-type'] =="Utility"): 
            return redirect(url_for('error_page.error_403'))

        print("User id: ", session['user_id'])

        aggregator_data = fetch_All_Aggregator_From_Private_Data()
        market_player_data = fetch_All_Market_Players_From_Private_Data()
        # print(aggregator_data)

        return render_template('/utililty/utility_private_data_page.html', 
                               aggregator_data=aggregator_data,
                               market_player_data=market_player_data)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."

@utility_page_bp.route("/admin/utility/buy_sell_request")
def utility_buy_sell_request():
    if session:
        if not (session['user-type'] =="Utility"): 
            return redirect(url_for('error_page.error_403'))

        print("User id: ", session['user_id'])

        buy_request = fetch_All_Buy_Request_From_Aggregator_Dashboard()
        sell_request = fetch_All_Sell_Request_From_Aggregator_Dashboard()
        return render_template('/utililty/utility_aggregator_request_page.html', 
                               buy_request=buy_request,
                               sell_request=sell_request)
    elif not session:
        return redirect(url_for('auth_page.signin'))
    else:
        return "Some error occured."


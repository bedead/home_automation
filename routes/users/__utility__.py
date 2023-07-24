from ast import literal_eval
from flask import Blueprint, redirect, render_template, request, url_for, session

from routes.__config__ import Config
from routes.data_generator.tp_chaos_generator.tp_chaos_generator.triple_pendulum import (
    decrypt_Text_New,
)
from routes.utility.diffi_hellman_EC import get_Shared_Key
from routes.utility.fetch_Data import (
    fetch_All_Aggregator_From_Private_Data,
    fetch_All_Buy_Request_From_Aggregator_Dashboard,
    fetch_All_Market_Players_From_Private_Data,
    fetch_All_Sell_Request_From_Aggregator_Dashboard,
    fetch_All_User_Complaints_From_Utility,
    fetch_Public_Key_From_Email,
)
from routes.utility.general_methods import (
    get_User_Session_Private_Key,
    get_User_User_Id,
    get_User_Username,
)

# Create a blueprint for the home routes
utility_page_bp = Blueprint("utility_page", __name__)
supabase_ = Config.supabase_


@utility_page_bp.route("/admin/utility/dashboard")
def utility_dashboard():
    if session:
        if not (session["user-type"] == "Utility"):
            return redirect(url_for("error_page.error_403"))

        print("User id: ", session["user_id"])

        return render_template("/utililty/utility_main_dashboard_page.html")
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


@utility_page_bp.route("/admin/utility/private_data")
def utility_private_data():
    if session:
        if not (session["user-type"] == "Utility"):
            return redirect(url_for("error_page.error_403"))

        print("User id: ", session["user_id"])

        aggregator_data = fetch_All_Aggregator_From_Private_Data()
        market_player_data = fetch_All_Market_Players_From_Private_Data()
        # print(aggregator_data)

        return render_template(
            "/utililty/utility_private_data_page.html",
            aggregator_data=aggregator_data,
            market_player_data=market_player_data,
        )
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


@utility_page_bp.route("/admin/utility/buy_sell_request")
def utility_buy_sell_request():
    if session:
        if not (session["user-type"] == "Utility"):
            return redirect(url_for("error_page.error_403"))

        print("User id: ", session["user_id"])

        buy_request = fetch_All_Buy_Request_From_Aggregator_Dashboard()
        # print(buy_request)
        sell_request = fetch_All_Sell_Request_From_Aggregator_Dashboard()
        return render_template(
            "/utililty/utility_buy_sell_page.html",
            buy_request=buy_request,
            sell_request=sell_request,
        )
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


@utility_page_bp.route("/admin/utility/aggregator_applications")
def utility_aggregator_applications():
    if session:
        if not (session["user-type"] == "Utility"):
            return redirect(url_for("error_page.error_403"))

        name = get_User_Username()
        print("User id: ", session["user_id"])

        return render_template(
            "/utililty/utility_aggregator_application_page.html", name=name
        )
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


def decode_Utiltiy_Complaints(data):
    complaints = []
    utility_private_key = get_User_Session_Private_Key()

    for each_complaints in data:
        email = each_complaints["email"]
        user_public_key = fetch_Public_Key_From_Email(email)

        # print(user_public_key)
        # print(type(user_public_key))

        shared_key_hex = get_Shared_Key(utility_private_key, user_public_key)
        d = {}
        for key, values in each_complaints.items():
            if key == "message":
                values_encrpyted = literal_eval(values)
                plain_text_each_d = decrypt_Text_New(values_encrpyted, shared_key_hex)
                d[key] = plain_text_each_d
            else:
                d[key] = values

        complaints.append(d)

    return complaints


@utility_page_bp.route("/admin/utility/market_player/issues")
def utility_marketplayer_issues():
    if session:
        if not (session["user-type"] == "Utility"):
            return redirect(url_for("error_page.error_403"))

        name = get_User_Username()
        print("User id: ", session["user_id"])

        data = []
        encrpyted_data = fetch_All_User_Complaints_From_Utility()
        print(encrpyted_data)
        data = decode_Utiltiy_Complaints(encrpyted_data)
        print(data)
        return render_template(
            "/utililty/utility_marketplayer_issues_page.html", name=name, data=data
        )
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."

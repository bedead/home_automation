from ast import literal_eval
import csv
import time
from flask import Blueprint, redirect, render_template, request, url_for, session

from routes.__config__ import Config
from routes.data_generator.tp_chaos_generator.tp_chaos_generator.triple_pendulum import (
    decode_key,
    decrypt_Text_New,
    get_encoded_key,
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
    """
    This route handles the utility's main dashboard page.
    It checks if the user is logged in as a utility. If
    not, it redirects to the appropriate error page. If the user is a utility,
    it renders the utility's main dashboard page.
    """
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
    """
    This route displays the utility's private data page.
    It checks if the user is logged in as a utility
    and then retrieves data related to aggregators
    and market players using the fetch_All_Aggregator_From_Private_Data()
    and fetch_All_Market_Players_From_Private_Data() functions. The retrieved
    data is then passed to the template for rendering.
    """
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
    """
    This route displays the utility's page for viewing buy
    and sell requests from aggregators. Similar to previous
    routes, it checks if the user is logged in as a utility
    and then fetches buy and sell request data using
    the appropriate functions. The retrieved data
    is then passed to the template for rendering.
    """
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
    """
    This route handles the utility's aggregator applications
    page. It checks if the user is logged in as a
    utility and retrieves the user's name. The
    name is then passed to the template for rendering.
    """
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
    """
    This function decodes complaints data received by the
    utility. It takes a list of complaint data as input
    and processes each complaint. It uses the utility's
    private key to derive shared keys with the users
    who submitted the complaints. It then decodes the
    encrypted complaint messages using the shared
    keys and returns a list of decoded complaints.
    """
    complaints = []
    utility_private_key = get_User_Session_Private_Key()

    for each_complaints in data:
        email = each_complaints["email"]
        user_public_key = fetch_Public_Key_From_Email(email)

        # print(user_public_key)
        # print(type(user_public_key))

        shared_key_hex = get_Shared_Key(utility_private_key, user_public_key)
        encoded_key = get_encoded_key(shared_key_hex)
        generate_list_key = decode_key(encoded_key[0])
        d = {}
        for key, values in each_complaints.items():
            if key == "message":
                values_encrpyted = literal_eval(values)
                plain_text_each_d = decrypt_Text_New(
                    values_encrpyted, generate_list_key
                )
                d[key] = plain_text_each_d
            else:
                d[key] = values

        complaints.append(d)

    return complaints


@utility_page_bp.route("/admin/utility/market_player/issues")
def utility_marketplayer_issues():
    """
    This route handles the utility's page for viewing issues
    submitted by market players. It first checks if the user
    is logged in as a utility. If the user is not logged in,
    it redirects to the signin page. If the user is a utility,
    it retrieves the utility's username and user ID. Then, it
    fetches encrypted complaint data from market players using the
    fetch_All_User_Complaints_From_Utility() function. After retrieving
    the data, it decodes the complaints using the decode_Utiltiy_Complaints()
    function, which decrypts the complaint messages using shared
    keys. The decoded complaints are then passed to the template along with
    the username for rendering the market player issues page.
    """
    if session:
        if not (session["user-type"] == "Utility"):
            return redirect(url_for("error_page.error_403"))

        name = get_User_Username()
        print("User id: ", session["user_id"])

        data = []
        encrpyted_data = fetch_All_User_Complaints_From_Utility()

        data = decode_Utiltiy_Complaints(encrpyted_data)

        return render_template(
            "/utililty/utility_marketplayer_issues_page.html", name=name, data=data
        )
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."

import csv
import time
from flask import Blueprint, redirect, render_template, request, url_for, session
from routes.__config__ import Config
from routes.data_generator.tp_chaos_generator.tp_chaos_generator.triple_pendulum import (
    decode_key,
    decrypt_Text_New,
    get_encoded_key,
)
from ast import literal_eval
from routes.utility.fetch_Data import (
    fetch_All_From_Aggregator_Dashboard,
    fetch_All_User_Complaints_From_Aggregator,
    fetch_One_From_Aggregator_Dashboard,
    fetch_Public_Key_From_Email,
)
from routes.utility.diffi_hellman_EC import get_Shared_Key
from routes.utility.general_methods import (
    get_User_Session_Private_Key,
    get_User_User_Id,
)

supabase = Config.supabase_

# Create a blueprint for the home routes
aggregator_page_bp = Blueprint("aggregator_page", __name__)


def decode_All_Data(data: list) -> list:
    """
    This function takes a list of encrypted data rows as
    input and returns a list of decoded dashboard rows. It
    iterates through each row, excluding the time-specific
    keys ('am' and 'pm'). For each row, it creates a new
    dashboard row with decrypted values using a shared key
    generated from the user's private key and their
    public key. The decoded dashboard data is then returned.
    """
    user_private_key = get_User_Session_Private_Key()
    # print("Aggregator private key :",user_private_key)
    # print(data)
    dashboard_data = []
    for each_row in data:
        row_user_id = each_row["user_id"]

        dashboard_row = {}
        for key, each_d in each_row.items():
            if ("am" in key) or ("pm" in key):
                pass
            else:
                dashboard_row[key] = each_d
        dashboard_data.append(dashboard_row)

    return dashboard_data


def decode_One_Data(detail_data: dict) -> dict:
    """
    This function takes a dictionary of encrypted detailed
    data as input and returns a decoded dashboard row.
    It focuses on a single row of detailed data.
    It first extracts the detail data from the dictionary
    and identifies the corresponding user's public key.
    Using the user's private key and the public key, it
    generates a shared key and decodes the encrypted values.
    The decoded details are returned in a dictionary format.
    """
    dashboard_row = {}
    print(detail_data)
    detail_data = detail_data[0]

    row_user_id = detail_data["user_id"]
    user_private_key = get_User_Session_Private_Key()
    user_row_public_key = get_Public_Key_For_ID(row_user_id)

    shared_key_hex = get_Shared_Key(user_private_key, user_row_public_key)
    print("Shared key :", shared_key_hex)
    encoded_key = get_encoded_key(shared_key_hex)
    generate_list_key = decode_key(encoded_key[0])

    for key, each_d in detail_data.items():
        if ("am" in key) or ("pm" in key):
            each_d = literal_eval(each_d)
            plain_text_each_d = decrypt_Text_New(each_d, generate_list_key)
            dashboard_row[key] = plain_text_each_d
        else:
            dashboard_row[key] = each_d

    return dashboard_row


def get_Public_Key_For_ID(user_id):
    """
    This function retrieves the public key associated with a
    given user ID. It queries the "private_data" table using
    the user ID and extracts the public key from the
    response data. The retrieved public key is then returned.
    """
    table_name = "private_data"
    response1 = (
        supabase.table(table_name=table_name)
        .select("public_key")
        .eq("user_id", user_id)
        .execute()
    )
    user_public_key = response1.data[0]["public_key"]

    return user_public_key


@aggregator_page_bp.route("/user/aggregator/dashboard")
def aggregator_dashboard():
    """
    This route is accessed by aggregators to view their
    dashboard. It first checks if a user session exists.
    If the user is not logged in or not an aggregator,
    it redirects to appropriate pages. If the user is an
    aggregator, it retrieves the aggregator's ID and
    fetches encrypted data related to their dashboard.
    It then decodes this data using the decode_All_Data
    function to obtain the decrypted dashboard information. The decoded
    data is passed to the HTML template for rendering.
    """
    if session:
        if not (session["user-type"] == "Aggregator"):
            return redirect(url_for("error_page.error_403"))

        print("User id: ", session["user_id"])

        aggregator_id = get_User_User_Id()
        encrypted_data = fetch_All_From_Aggregator_Dashboard(aggregator_id)
        # print(encrypted_data)
        data = decode_All_Data(encrypted_data)
        print(data)

        return render_template("/aggregator/aggregator_dashboard_page.html", data=data)
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


@aggregator_page_bp.route("/user/aggregator/dashboard/request_details/")
def aggregator_user_details():
    """
    This route is accessed to view detailed information
    about a specific user's request. It checks if a user
    session exists and if the user is an aggregator. If
    so, it retrieves query parameters like user_id and
    created_at. It fetches encrypted detailed data related to
    the specified user and timestamp, then decodes this data
    using the decode_One_Data method to obtain the decrypted
    information. It also measures the time taken for fetching
    and decryption, records it in a CSV file,
    and renders a template to display the decrypted data.
    """
    if session:
        if not (session["user-type"] == "Aggregator"):
            return redirect(url_for("error_page.error_403"))

        print("User id: ", session["user_id"])

        request_user_id = request.args.get("user_id", None)
        created_at = request.args.get("created_at", None)
        starttime = time.time()
        encrypted_detail_data = fetch_One_From_Aggregator_Dashboard(
            user_id=request_user_id, created_at=created_at
        )
        endtime = time.time()
        fetchtime = endtime - starttime

        starttime = time.time()
        data = decode_One_Data(encrypted_detail_data)
        endtime = time.time()
        decryption_time = endtime - starttime

        with open("aggre_request_show.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([fetchtime, decryption_time])
        file.close()

        return render_template(
            "/aggregator/aggregator_dashboard_request_details_page.html", data=data
        )

    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


@aggregator_page_bp.route("/user/aggregator/history")
def aggregator_history():
    """
    This route is used to display the history of an
    aggregator's actions. It checks the user's session
    and whether they are an aggregator. If valid,
    it retrieves the user's ID and renders a
    template to display the aggregator's history page.
    """
    if session:
        if not (session["user-type"] == "Aggregator"):
            return redirect(url_for("error_page.error_403"))
        print("Uer id: ", session["user_id"])

        return render_template("/aggregator/aggregator_history_page.html")

    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


def decode_Complaints_Data(data):
    """
    This function takes a list of encrypted complaint
    data as input and returns a list of decoded complaint
    entries. It iterates through each encrypted complaint,
    decrypts the "message" value using the shared key
    derived from the aggregator's private key and the
    user's public key. It constructs a new complaint entry with decrypted
    values and returns the list of decoded complaints.
    """
    aggre_private_key = get_User_Session_Private_Key()
    complaint_data = []
    # print(data)
    for each_complaints in data:
        email = each_complaints["email"]
        user_public_key = fetch_Public_Key_From_Email(email)

        # print(user_public_key)
        # print(type(user_public_key))

        shared_key_hex = get_Shared_Key(aggre_private_key, user_public_key)
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

        complaint_data.append(d)

    return complaint_data


@aggregator_page_bp.route("/user/aggregator/complaints")
def aggregator_complaints():
    """
    This route is accessed to view complaints submitted
    by users to the aggregator. It checks the user's
    session and whether they are an aggregator. If valid,
    it fetches encrypted complaint data related to the aggregator,
    then decodes this data using the decode_Complaints_Data method
    to obtain decrypted complaint entries.
    It renders a template to display the decoded complaints.
    """
    if session:
        if not (session["user-type"] == "Aggregator"):
            return redirect(url_for("error_page.error_403"))
        print("Uer id: ", session["user_id"])
        data = []
        aggregator_id = get_User_User_Id()

        encrpyted_data = fetch_All_User_Complaints_From_Aggregator(aggregator_id)

        data = decode_Complaints_Data(encrpyted_data)
        # print(data)

        return render_template("/aggregator/aggregator_complaints_page.html", data=data)

    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


@aggregator_page_bp.route("/user/aggregator/settings")
def aggregator_settings():
    """
    This route provides access to the aggregator's settings
    page. It checks the user's session and whether they
    are an aggregator. If valid, it retrieves the user's
    ID and renders a template to display the settings page.
    """
    if session:
        if not (session["user-type"] == "Aggregator"):
            return redirect(url_for("error_page.error_403"))
        print("Uer id: ", session["user_id"])

        return render_template("/aggregator/aggregator_settings_page.html")
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."

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
    if session:
        if not (session["user-type"] == "Aggregator"):
            return redirect(url_for("error_page.error_403"))
        print("Uer id: ", session["user_id"])
        data = []
        aggregator_id = get_User_User_Id()

        startime = time.time()
        encrpyted_data = fetch_All_User_Complaints_From_Aggregator(aggregator_id)
        endtime = time.time()
        complaint_fetch_time = endtime - startime

        startime = time.time()
        data = decode_Complaints_Data(encrpyted_data)
        endtime = time.time()
        decryption_time = endtime - startime

        with open("complaint_show.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([complaint_fetch_time, decryption_time])
        file.close()
        # print(data)

        return render_template("/aggregator/aggregator_complaints_page.html", data=data)

    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


@aggregator_page_bp.route("/user/aggregator/settings")
def aggregator_settings():
    if session:
        if not (session["user-type"] == "Aggregator"):
            return redirect(url_for("error_page.error_403"))
        print("Uer id: ", session["user_id"])

        return render_template("/aggregator/aggregator_settings_page.html")
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."

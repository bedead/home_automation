import csv
from ast import literal_eval
from flask import Blueprint, redirect, render_template, request, url_for, session
from routes.data_generator.tp_chaos_generator.tp_chaos_generator.triple_pendulum import (
    decode_key,
    encrypt_Text_New,
    get_encoded_key,
)
from routes.utility.diffi_hellman_EC import get_Shared_Key
from routes.utility.fetch_Data import (
    fetch_From_Consumer_Dashboard,
    fetch_From_Consumer_History,
    fetch_From_Consumer_Monitor,
)
from routes.__config__ import Config
from routes.utility.general_methods import (
    get_Chaos_Key_List_Aggregator,
    get_User_Session_Details,
    get_User_Session_Other_Public_Key,
    get_User_Session_Private_Key,
    get_User_Aggregator_Id,
    get_User_Username,
    get_Utility_Public_Key,
    set_Utility_Chaos_Key,
)
from datetime import datetime
import time

from routes.utility.insert_Data import (
    send_Issue_Message_To_Aggregator,
    send_Issue_Message_To_Utility,
)

# Create a blueprint for the home routes
consumer_page_bp = Blueprint("consumer_page", __name__)
supabase_ = Config.supabase_


@consumer_page_bp.route("/user/consumer/dashboard")
def consumer_dashboard():
    """
    This route displays the consumer's dashboard. It first
    checks if a user session exists. If the user is a consumer,
    it fetches various statistics and data related to the consumer's
    dashboard, such as total trades, average watt-hour consumption,
    average cost per hour, access grants, access rejections, and other
    data. If any exceptions occur during data retrieval, such as
    UnboundLocalError or TypeError, it redirects to an
    "unknown error" page. Otherwise, it renders the
    consumer's dashboard template with the fetched data.
    """
    if session:
        print("User id: ", session["user_id"])

        if not (session["user-type"] == "Consumer"):
            return redirect(url_for("error_page.error_403"))
        (
            total_trades,
            average_wh_hour,
            average_cost_hour,
            access_grants,
            access_rejected,
            some_other,
        ) = (0, 0, 0, 0, 0, 0)
        try:
            (
                total_trades,
                average_wh_hour,
                average_cost_hour,
                access_grants,
                access_rejected,
                some_other,
            ) = fetch_From_Consumer_Dashboard(session["user_id"])
        except UnboundLocalError as e:
            # no internet (create new error page for this type)
            return redirect(url_for("error_page.unknown_error"))
        except TypeError as e:
            return redirect(url_for("error_page.unknown_error"))

        return render_template(
            "/consumer/consumer_dashboard_page.html",
            total_trades=total_trades,
            average_wh_hour=average_wh_hour,
            average_cost_hour=average_cost_hour,
            access_grants=access_grants,
            access_rejected=access_rejected,
            some_other=some_other,
        )
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


@consumer_page_bp.route("/user/consumer/history")
def consumer_history():
    """
    This route displays the consumer's trading history.
    It checks if a user session exists and if the user is
    a consumer. If so, it retrieves trading history
    data related to the consumer's user ID and renders the
    consumer's history template with the fetched data.
    """
    if session:
        if not (session["user-type"] == "Consumer"):
            return redirect(url_for("error_page.error_403"))

        print("User id: ", session["user_id"])
        data = fetch_From_Consumer_History(session["user_id"])

        return render_template("/consumer/consumer_history_page.html", data=data)
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


def insert_One_Into_Aggregator_Dashboard(data: dict):
    """
    This function inserts a single trade record into the aggregator's
    dashboard. It takes a dictionary of trade-related data as
    input. The function fetches the user's email, user type,
    and user ID from the session. It constructs a new row with
    information about the trade, including the creation timestamp, user
    details, trade status, trade type, and aggregator ID. The provided
    trade data is also incorporated into the row. The function then
    attempts to insert the row into the "aggregator_dashboard" table.
    If an exception occurs during the insertion
    process, it redirects to the "unknown error" page.
    """
    user_email, user_type, user_id = get_User_Session_Details()
    table_name = "aggregator_dashboard"
    created_at = datetime.now()
    row = {
        "created_at": str(created_at),
        "user_id": user_id,
        "user_email": user_email,
        "user_type": user_type,
        "status": "PENDING",
        "type": "BUY",
        "aggregator_id": get_User_Aggregator_Id(),
    }

    for key, value in data.items():
        row[key] = value
    try:
        supabase_.table(table_name=table_name).insert(row).execute()

    except Exception as e:
        return redirect(url_for("error_page.unknown_error"))


@consumer_page_bp.route("/user/consumer/monitor/buy_energy", methods=["POST"])
def buy_energy():
    """
    This route handles the consumer's request to buy energy. It
    captures the data from a POST request representing the energy
    consumption for different time slots. The data is collected
    from the form fields for each hour in both AM and PM periods.
    It then constructs a dictionary named data containing the
    encrypted energy consumption values for each hour. The data
    is encrypted using the shared key list obtained from the
    get_Chaos_Key_List_Aggregator() function. The encrypted data
    is then inserted into the aggregator's dashboard using
    the insert_One_Into_Aggregator_Dashboard() function. The
    execution time of encryption and data insertion is
    recorded and stored in a CSV file. Finally, it redirects to the
    consumer monitor page with a status parameter.
    """
    if request.method == "POST":
        first = request.form["12-1am"]
        second = request.form["1-2am"]
        third = request.form["2-3am"]
        four = request.form["3-4am"]
        five = request.form["4-5am"]
        six = request.form["5-6am"]
        seven = request.form["6-7am"]
        eight = request.form["7-8am"]
        nine = request.form["8-9am"]
        ten = request.form["9-10am"]
        eleven = request.form["10-11am"]
        twelve = request.form["11-12am"]

        first_pm = request.form["12-1pm"]
        second_pm = request.form["1-2pm"]
        third_pm = request.form["2-3pm"]
        four_pm = request.form["3-4pm"]
        five_pm = request.form["4-5pm"]
        six_pm = request.form["5-6pm"]
        seven_pm = request.form["6-7pm"]
        eight_pm = request.form["7-8pm"]
        nine_pm = request.form["8-9pm"]
        ten_pm = request.form["9-10pm"]
        eleven_pm = request.form["10-11pm"]
        twelve_pm = request.form["11-12pm"]

        data = {
            "12-1am": first,
            "1-2am": second,
            "2-3am": third,
            "3-4am": four,
            "4-5am": five,
            "5-6am": six,
            "6-7am": seven,
            "7-8am": eight,
            "8-9am": nine,
            "9-10am": ten,
            "10-11am": eleven,
            "11-12am": twelve,
            "12-1pm": first_pm,
            "1-2pm": second_pm,
            "2-3pm": third_pm,
            "3-4pm": four_pm,
            "4-5pm": five_pm,
            "5-6pm": six_pm,
            "6-7pm": seven_pm,
            "7-8pm": eight_pm,
            "8-9pm": nine_pm,
            "9-10pm": ten_pm,
            "10-11pm": eleven_pm,
            "11-12pm": twelve_pm,
        }

        # aggregator_public_key = get_User_Session_Other_Public_Key()
        # user_private_key = get_User_Session_Private_Key()
        shared_key_list = get_Chaos_Key_List_Aggregator()

        print("Shared key :", shared_key_list)

        start_time = time.time()
        for key, each_d in data.items():
            hex_ciphertext_each_d = encrypt_Text_New(each_d, shared_key_list)
            data[key] = str(hex_ciphertext_each_d)
        end_time = time.time()
        encryption_time_taken = end_time - start_time

        start_time = time.time()
        insert_One_Into_Aggregator_Dashboard(data)
        end_time = time.time()
        datasending_to_database_time_taken = end_time - start_time

        with open("buy_request.csv", "a", newline="") as file:
            writer = csv.writer(file)
            # writer.writerow(['Data Encrytion time','Data sending time'])
            writer.writerow([encryption_time_taken, datasending_to_database_time_taken])
        file.close()

        print("Buy request made.")
        return redirect(url_for("consumer_page.consumer_monitor", status=True))


def get_Total_Current_And_Power(data):
    """
    This function calculates the total current and total power
    consumption from the provided data. It iterates
    through each row in the data and accumulates
    the current and power values. The
    rounded total current and total power are returned.
    """
    total_current = 0
    total_w = 0

    for each_row in data:
        for key, values in each_row.items():
            if key == "current":
                total_current += values
            elif key == "power":
                total_w += values

    return round(total_current, 1), round(total_w, 1)


@consumer_page_bp.route("/user/consumer/monitor")
@consumer_page_bp.route("/user/consumer/monitor/<status>")
def consumer_monitor(status=None):
    """
    This route displays the consumer's energy consumption
    monitoring page. It first checks if a user session exists
    and if the user is a consumer. If so, it retrieves the
    user's username and energy consumption data from the database
    using the fetch_From_Consumer_Monitor() function. The function
    get_Total_Current_And_Power() is then used to calculate the
    total current and total power from the fetched data.
    The consumer's monitor page is rendered with the username,
    energy consumption data, total current, total power, and
    an optional status parameter (if provided). If there's no data available, the
    total current and total power are set to 0.
    """
    if session:
        if not (session["user-type"] == "Consumer"):
            return redirect(url_for("error_page.error_403"))

        print(f'User id {session["user_id"]} in Consumer Monitor Page')

        username = get_User_Username()
        data = []

        data = fetch_From_Consumer_Monitor(session["user_id"])
        print(data)
        if data == []:
            total_current, total_w = 0, 0
        else:
            total_current, total_w = get_Total_Current_And_Power(data)

        return render_template(
            "/consumer/consumer_monitor_page.html",
            username=username,
            data=data,
            total_current=total_current,
            total_w=total_w,
            status=status,
        )

    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


@consumer_page_bp.route("/user/consumer/issue/aggregator")
def consumer_issue_to_aggregator():
    """
    This route handles consumer grievances directed towards the
    aggregator. It first checks if the user is logged in as a
    consumer and then retrieves the message_status query parameter
    from the URL, indicating whether a message was successfully
    sent or not. It fetches the username using the get_User_Username()
    function. Depending on the message_status, it renders a template for the consumer's
    grievance page with appropriate status messages.
    """
    if session:
        if not (session["user-type"] == "Consumer"):
            return redirect(url_for("error_page.error_403"))

        print(f'User id {session["user_id"]} in Consumer grievance Page')
        message_status = request.args.get("message", None)
        username = get_User_Username()

        if message_status == "send":
            return render_template(
                "/consumer/consumer_issue_aggregator_page.html",
                username=username,
                status=True,
            )
        elif message_status == "not send":
            return render_template(
                "/consumer/consumer_issue_aggregator_page.html",
                username=username,
                status=False,
            )
        else:
            return render_template(
                "/consumer/consumer_issue_aggregator_page.html", username=username
            )

    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


@consumer_page_bp.route("/user/consumer/issue/aggregator/post", methods=["POST"])
def send_message_to_aggregator():
    """
    This route is triggered by a POST request when a consumer
    submits a grievance message to the aggregator. It captures the
    username, email, and message from the form data. It then
    encrypts the message using the chaos key obtained from the
    get_Chaos_Key_List_Aggregator() function. The encrypted message
    is sent to the aggregator using the send_Issue_Message_To_Aggregator()
    function. The time taken for encryption and sending is
    recorded and stored in a CSV file. Upon successful
    completion, the route redirects back to the
    consumer's grievance page with a success status.
    """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        message = request.form["message"]

        print(username, email, message)

        try:
            starttime = time.time()
            choas_secret_key = get_Chaos_Key_List_Aggregator()
            cipher_text = encrypt_Text_New(message, choas_secret_key)
            endtime = time.time()
            encryption_time = endtime - starttime

            starttime = time.time()
            send_Issue_Message_To_Aggregator(username, email, cipher_text)
            endtime = time.time()
            sending_time = endtime - starttime

            with open("grievance.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([encryption_time, sending_time])
            file.close()

            return redirect(
                url_for("consumer_page.consumer_issue_to_aggregator", message="send")
            )
        except Exception as e:
            print(e.args)
            return redirect(
                url_for(
                    "consumer_page.consumer_issue_to_aggregator", message="not send"
                )
            )


@consumer_page_bp.route("/user/consumer/issue/utility")
def consumer_issue_to_utility():
    """
    Similar to the aggregator grievance page, this route handles
    consumer grievances directed towards the utility company. It
    retrieves the message_status query parameter
    and renders the grievance page accordingly.
    """
    if session:
        if not (session["user-type"] == "Consumer"):
            return redirect(url_for("error_page.error_403"))

        print(f'User id {session["user_id"]} in Consumer Ascalate Page')

        username = get_User_Username()
        message_status = request.args.get("message", None)
        if message_status == "send":
            return render_template(
                "/consumer/consumer_issue_utility_page.html",
                username=username,
                status=True,
            )
        elif message_status == "not send":
            return render_template(
                "/consumer/consumer_issue_utility_page.html",
                username=username,
                status=False,
            )
        else:
            return render_template(
                "/consumer/consumer_issue_utility_page.html", username=username
            )

    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."


@consumer_page_bp.route("/user/consumer/issue/utility/post", methods=["POST"])
def send_message_to_utility():
    """
    This route is triggered when a consumer submits a grievance
    message to the utility company. It captures the username,
    email, and message from the form data. It calculates the
    shared key between the user's private key and the utility
    company's public key using the get_Shared_Key() function.
    The shared key is used to generate a chaos key for encrypting
    the message. The chaos key is set for the utility using the
    set_Utility_Chaos_Key() function. The message is then encrypted
    and sent to the utility. Time taken for key generation,
    encryption, and sending is recorded and stored
    in a CSV file. Upon completion, the route
    redirects back to the consumer's utility grievance page.
    """
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        message = request.form["message"]

        print(username, email, message)

        try:
            starttime = time.time()
            user_private_key = get_User_Session_Private_Key()
            utility_public_key = get_Utility_Public_Key()

            print(user_private_key)
            print(utility_public_key)

            shared_hex_key = get_Shared_Key(user_private_key, utility_public_key)
            encoded_key = get_encoded_key(shared_hex_key)
            utility_chaos_key = decode_key(encoded_key[0])
            endtime = time.time()
            utility_key_gen = endtime - starttime

            starttime = time.time()
            set_Utility_Chaos_Key(utility_chaos_key)
            cipher_text = encrypt_Text_New(message, utility_chaos_key)
            endtime = time.time()
            encryption_time = endtime - starttime

            starttime = time.time()
            send_Issue_Message_To_Utility(username, email, cipher_text)
            endtime = time.time()
            sending_time = endtime - starttime

            with open("ascaliate.csv", "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([utility_key_gen, encryption_time, sending_time])
            file.close()

            return redirect(
                url_for("consumer_page.consumer_issue_to_utility", message="send")
            )
        except Exception as e:
            print(e.args)
            return redirect(
                url_for("consumer_page.consumer_issue_to_utility", message="not send")
            )


@consumer_page_bp.route("/user/consumer/settings")
def consumer_settings():
    """
    This route displays the consumer's settings page. Similar
    to other routes, it checks if the user is a consumer, fetches the
    username, and renders the consumer settings page.
    """
    if session:
        if not (session["user-type"] == "Consumer"):
            return redirect(url_for("error_page.error_403"))

        print(f'User id {session["user_id"]} in Consumer Settings Page')

        return render_template("/consumer/consumer_settings_page.html")
    elif not session:
        return redirect(url_for("auth_page.signin"))
    else:
        return "Some error occured."

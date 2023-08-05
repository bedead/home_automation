import csv
from flask import redirect, url_for
from routes.data_generator.tp_chaos_generator.tp_chaos_generator.triple_pendulum import (
    decrypt_Text_New,
)
from routes.utility.general_methods import get_Fetch_Exception_Details
from ..__config__ import Config
import time
from ast import literal_eval

# from gotrue.errors import Au
# httpx.ConnectTimeout:
supabase_ = Config.supabase_


def compute_Avg(info, column_name):
    """
    This function calculates the average value of a
    specific column in the given dataset. It iterates
    through the dataset, decrypts the values
    in the specified column, computes
    the average, and returns the rounded result.
    """
    val = 0
    for each in info:
        plainInt = int(decrypt_Text_New(each[column_name]))
        val += plainInt
    val = val / len(info)
    return round(val, 2)


def fetch_From_Consumer_Dashboard(user_id):
    """
    This function fetches various statistics and metrics from
    the consumer dashboard for a specific user. It
    constructs multiple queries to retrieve data related to
    total trades, average watt-hour per hour, average cost
    per hour, access grants, access rejections, and other
    stats. The retrieved data is decrypted and processed.
    The function calculates averages for the top 10 values of
    the average_wh_hour and average_cost_hour columns. Finally, it
    returns a list containing the fetched and calculated values.
    """
    table_name = "consumer_dashboard"
    col1 = "total_trades"
    col2 = "average_wh_hour"
    col3 = "average_cost_hour"
    col4 = "access_grants"
    col5 = "access_rejected"
    col6 = "some_other_stats"
    # defining all queries
    q1 = (
        supabase_.table(table_name=table_name)
        .select(col1)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
    )
    q2 = (
        supabase_.table(table_name=table_name)
        .select(col2)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(7)
    )
    q3 = (
        supabase_.table(table_name=table_name)
        .select(col3)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(7)
    )
    q4 = (
        supabase_.table(table_name=table_name)
        .select(col4)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
    )
    q5 = (
        supabase_.table(table_name=table_name)
        .select(col5)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
    )
    q6 = (
        supabase_.table(table_name=table_name)
        .select(col6)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
    )

    # executing all queries to fetch data
    try:
        total_trades = q1.execute()
        average_wh_hour = q2.execute()
        average_cost_hour = q3.execute()
        access_grants = q4.execute()
        access_rejected = q5.execute()
        some_other = q6.execute()

        total_trades_0 = int(decrypt_Text_New(literal_eval(total_trades.data[0][col1])))
        access_grants_0 = int(
            decrypt_Text_New(literal_eval(access_grants.data[0][col4]))
        )
        access_rejected_0 = int(
            decrypt_Text_New(literal_eval(access_rejected.data[0][col5]))
        )
        some_other_0 = int(decrypt_Text_New(literal_eval(some_other.data[0][col6])))

        # finding average of top 10 values of average_wh_hour and average_cost_hour
        average_wh_hour_0 = compute_Avg(average_wh_hour.data, col2)
        average_cost_hour_0 = compute_Avg(average_cost_hour.data, col3)

        # print(average_wh_hour)
        # print(average_cost_hour)

        # returning all values (including average value)
        return [
            total_trades_0,
            average_wh_hour_0,
            average_cost_hour_0,
            access_grants_0,
            access_rejected_0,
            some_other_0,
        ]

    except Exception as e:
        print(e.__dict__)
        return [0, 0, 0, 0, 0, 0]

    # decryption


def fetch_From_Consumer_History(user_id):
    """
    This function retrieves data from the consumer history
    table for a specific user. It constructs a query to
    fetch the data and then iterates through the response
    to decrypt and process specific columns like
    full_name, wh_hour_price, and email. The decrypted data is then returned.
    """
    table_name = "consumer_history"
    query = (
        supabase_.table(table_name=table_name)
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(7)
    )
    try:
        response = query.execute()
    except Exception as e:
        get_Fetch_Exception_Details(e)
        return redirect(url_for("error_page.base_error"))

    data = response.data
    for each_index in range(len(data)):
        data[each_index]["full_name"] = decrypt_Text_New(
            literal_eval(data[each_index]["full_name"])
        )
        data[each_index]["wh_hour_price"] = int(
            decrypt_Text_New(literal_eval(data[each_index]["wh_hour_price"]))
        )
        data[each_index]["email"] = decrypt_Text_New(
            literal_eval(data[each_index]["email"])
        )

    return data


def fetch_From_Consumer_Monitor(user_id):
    """
    This function fetches data from the consumer monitor
    table for a specific user. It retrieves the total_appliances
    for the user and constructs a query to fetch data related
    to various load types. The fetched data is decrypted
    and processed to create a new data structure. The function
    also measures the time taken for fetching and decrypting data and records
    it in a CSV file named "dashboard_data.csv."
    """

    total_appliances = fetch_User_Total_Appliances(user_id)
    # print(total_appliances)

    starttime = time.time()
    table_name = "consumer_monitor"
    query = (
        supabase_.table(table_name=table_name)
        .select("*")
        .eq("user_id", user_id)
        .order("id", desc=True)
        .limit(total_appliances)
    )
    try:
        response = query.execute()
    except Exception as e:
        get_Fetch_Exception_Details(e)
        return redirect(url_for("error_page.unknown_error"))

    if response.data == []:
        return response.data
    else:
        all_loads = []
        end_time = time.time()
        fetch_time = end_time - starttime

        # decrypting each column value
        start_time = time.time()
        data = []
        for each_index in range(len(response.data)):
            data_load = response.data[each_index]["load_type"]

            if data_load not in all_loads:
                all_loads.append(data_load)
                # print(response.data[each_index]['id'])
                volt = decrypt_Text_New(literal_eval(response.data[each_index]["volt"]))
                pf = decrypt_Text_New(
                    literal_eval(response.data[each_index]["power_factor"])
                )
                current = decrypt_Text_New(
                    literal_eval(response.data[each_index]["current"])
                )
                f = decrypt_Text_New(
                    literal_eval(response.data[each_index]["frequency"])
                )
                p = decrypt_Text_New(literal_eval(response.data[each_index]["power"]))
                e = (
                    decrypt_Text_New(literal_eval(response.data[each_index]["energy"]))
                    if response.data[each_index]["energy"] != None
                    else 0
                )
                ne = {
                    "load_type": data_load,
                    "volt": (0 if volt == "nan" else float(volt)),
                    "power_factor": (0 if pf == "nan" else float(pf)),
                    "current": (0 if current == "nan" else float(current)),
                    "frequency": (0 if f == "nan" else float(f)),
                    "power": (0 if p == "nan" else float(p)),
                    "energy": (0 if e == "nan" else float(e)),
                    "user_id": response.data[each_index]["user_id"],
                    "created_at": response.data[each_index]["created_at"],
                }
                data.append(ne)

        end_time = time.time()
        decryption_time_taken = end_time - start_time

        with open("dashboard_data.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([fetch_time, decryption_time_taken])
        file.close()

        return data


def fetch_From_Producer_Dashboard(user_id):
    """
    Similar to the previous description, this function fetches
    various statistics and metrics from the producer dashboard
    for a specific user. It constructs queries to retrieve
    data related to total trades, average watt-hour per hour,
    average cost per hour, access grants, access rejections,
    and other stats. The retrieved data is decrypted and
    processed. The function calculates averages
    for specific columns and returns the results.
    """
    table_name = "producer_dashboard"
    col1 = "total_trades"
    col2 = "average_wh_hour"
    col3 = "average_cost_hour"
    col4 = "access_grants"
    col5 = "access_rejected"
    col6 = "some_other_stats"
    # defining all queries
    q1 = (
        supabase_.table(table_name=table_name)
        .select(col1)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
    )
    q2 = (
        supabase_.table(table_name=table_name)
        .select(col2)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(7)
    )
    q3 = (
        supabase_.table(table_name=table_name)
        .select(col3)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(7)
    )
    q4 = (
        supabase_.table(table_name=table_name)
        .select(col4)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
    )
    q5 = (
        supabase_.table(table_name=table_name)
        .select(col5)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
    )
    q6 = (
        supabase_.table(table_name=table_name)
        .select(col6)
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(1)
    )

    # executing all queries to fetch data
    try:
        total_trades = q1.execute()
        average_wh_hour = q2.execute()
        average_cost_hour = q3.execute()
        access_grants = q4.execute()
        access_rejected = q5.execute()
        some_other = q6.execute()

        total_trades_0 = int(decrypt_Text_New(literal_eval(total_trades.data[0][col1])))
        access_grants_0 = int(
            decrypt_Text_New(literal_eval(access_grants.data[0][col4]))
        )
        access_rejected_0 = int(
            decrypt_Text_New(literal_eval(access_rejected.data[0][col5]))
        )
        some_other_0 = int(decrypt_Text_New(literal_eval(some_other.data[0][col6])))

        # finding average of top 10 values of average_wh_hour and average_cost_hour
        average_wh_hour_0 = compute_Avg(average_wh_hour.data, col2)
        average_cost_hour_0 = compute_Avg(average_cost_hour.data, col3)

        # print(average_wh_hour)
        # print(average_cost_hour)

        # returning all values (including average value)
        return [
            total_trades_0,
            average_wh_hour_0,
            average_cost_hour_0,
            access_grants_0,
            access_rejected_0,
            some_other_0,
        ]

    except Exception as e:
        return [0, 0, 0, 0, 0, 0]
    # decryption


def fetch_From_Producer_History(user_id):
    """
    This function retrieves data from the producer history
    table for a specific user. It constructs a query to fetch
    the data and then iterates through the response to
    decrypt and process specific columns like
    full_name, wh_hour_price, and email. The decrypted data is then returned.
    """
    table_name = "producer_history"
    query = (
        supabase_.table(table_name=table_name)
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .limit(7)
    )
    try:
        response = query.execute()
    except Exception as e:
        get_Fetch_Exception_Details(e)
        return redirect(url_for("error_page.base_error"))

    data = response.data
    for each_index in range(len(data)):
        data[each_index]["full_name"] = decrypt_Text_New(
            literal_eval(data[each_index]["full_name"])
        )
        data[each_index]["wh_hour_price"] = int(
            decrypt_Text_New(literal_eval(data[each_index]["wh_hour_price"]))
        )
        data[each_index]["email"] = decrypt_Text_New(
            literal_eval(data[each_index]["email"])
        )

    return data


def fetch_From_Producer_Monitor(user_id):
    """
    This function fetches data from the producer monitor table
    for a specific user. It retrieves the total_appliances
    for the user and constructs a query to fetch data related
    to various load types. The fetched data is decrypted
    and processed to create a new data structure.
    The function returns the processed data.
    """
    total_appliances = fetch_User_Total_Appliances(user_id)

    table_name = "producer_monitor"
    query = (
        supabase_.table(table_name=table_name)
        .select("*")
        .eq("user_id", user_id)
        .order("id", desc=True)
        .limit(total_appliances)
    )
    try:
        response = query.execute()
    except Exception as e:
        get_Fetch_Exception_Details(e)
        return redirect(url_for("error_page.unknown_error"))

    if response.data == []:
        return response.data
    else:
        all_loads = []

        # decrypting each column value
        data = []
        for each_index in range(len(response.data)):
            data_load = response.data[each_index]["load_type"]

            if data_load not in all_loads:
                all_loads.append(data_load)
                volt = decrypt_Text_New(literal_eval(response.data[each_index]["volt"]))
                pf = decrypt_Text_New(
                    literal_eval(response.data[each_index]["power_factor"])
                )
                current = decrypt_Text_New(
                    literal_eval(response.data[each_index]["current"])
                )
                f = decrypt_Text_New(
                    literal_eval(response.data[each_index]["frequency"])
                )
                p = decrypt_Text_New(literal_eval(response.data[each_index]["power"]))
                e = (
                    decrypt_Text_New(literal_eval(response.data[each_index]["energy"]))
                    if response.data[each_index]["energy"] != None
                    else 0
                )
                ne = {
                    "load_type": data_load,
                    "volt": (0 if volt == "nan" else float(volt)),
                    "power_factor": (0 if pf == "nan" else float(pf)),
                    "current": (0 if current == "nan" else float(current)),
                    "frequency": (0 if f == "nan" else float(f)),
                    "power": (0 if p == "nan" else float(p)),
                    "energy": (0 if e == "nan" else float(e)),
                    "user_id": response.data[each_index]["user_id"],
                    "created_at": response.data[each_index]["created_at"],
                }
                data.append(ne)

        return data


def fetch_All_From_Aggregator_Dashboard(aggregator_id):
    """
    This function retrieves all data from the aggregator
    dashboard table for a specific aggregator. It
    constructs a query to retrieve all entries related to
    the given aggregator_id and returns the response data.
    """
    table_name = "aggregator_dashboard"
    response = (
        supabase_.table(table_name=table_name)
        .select("*")
        .eq("aggregator_id", aggregator_id)
        .order("created_at", desc=True)
        .execute()
    )
    return response.data


def fetch_One_From_Aggregator_Dashboard(user_id: str, created_at: str) -> list:
    """
    This function fetches a single entry from the aggregator dashboard
    table based on the user_id and created_at
    timestamp. It constructs a query to retrieve
    the specific entry and returns the response data.
    """
    table_name = "aggregator_dashboard"

    response = (
        supabase_.table(table_name=table_name)
        .select("*")
        .eq("user_id", user_id)
        .eq("created_at", created_at)
        .execute()
    )

    return response.data


# fetch_From_Consumer_History('19353ea3-5608-4971-b168-cccf5a9324a7')
def fetch_All_Aggregator_From_Private_Data():
    """
    This function retrieves data from the private_data table for
    all users with the user type "Aggregator." It orders the data by creation time in
    descending order and limits the result to 6 entries.
    """
    table = "private_data"
    query = (
        supabase_.table(table_name=table)
        .select("*")
        .eq("user_type", "Aggregator")
        .order("created_at", desc=True)
        .limit(6)
        .execute()
    )
    # return redirect(url_for('error_page.unknown_error'))
    return query.data


def fetch_All_Market_Players_From_Private_Data():
    """
    This function retrieves data from the private_data table for
    all users with user types "Consumer" or "Producer."
    Similar to the previous function, it orders
    the data by creation time in descending
    order and limits the result to 6 entries.
    """
    table = "private_data"
    query = (
        supabase_.table(table_name=table)
        .select("*")
        .in_("user_type", ["Consumer", "Producer"])
        .order("created_at", desc=True)
        .limit(6)
        .execute()
    )

    return query.data


def fetch_All_Buy_Request_From_Aggregator_Dashboard():
    """
    This function fetches buy request data from the
    aggregator_dashboard table. It selects specific columns
    related to buy requests, orders the data by creation time in
    descending order, and limits the result to 6 entries.
    """
    table = "aggregator_dashboard"
    query = (
        supabase_.table(table_name=table)
        .select(
            "user_id",
            "user_email",
            "aggregator_id",
            "type",
            "status",
            "user_type",
            "created_at",
        )
        .eq("type", "BUY")
        .order("created_at", desc=True)
        .limit(6)
        .execute()
    )
    # print(query)

    return query.data


def fetch_All_Sell_Request_From_Aggregator_Dashboard():
    """
    This function fetches sell request data from the aggregator_dashboard
    table. It selects specific columns related to
    sell requests, orders the data by creation time in
    descending order, and limits the result to 6 entries.
    """
    table = "aggregator_dashboard"
    query = (
        supabase_.table(table_name=table)
        .select(
            "user_id",
            "user_email",
            "aggregator_id",
            "type",
            "status",
            "user_type",
            "created_at",
        )
        .eq("type", "SELL")
        .order("created_at", desc=True)
        .limit(6)
        .execute()
    )
    # print(query)

    return query.data


def fetch_User_Total_Appliances(user_id: str):
    """
    This function retrieves the total number of appliances
    associated with a specific user. It fetches the total_appliances value from
    the private_data table for the given user_id.
    """
    table_name = "private_data"
    query = (
        supabase_.table(table_name=table_name)
        .select("total_appliances")
        .eq("user_id", user_id)
        .execute()
    )

    return query.data[0]["total_appliances"]


def get_Aggregator_Id_From_Username(user_name: str) -> str:
    """
    This function retrieves the aggregator ID based on the
    provided username. It fetches the
    user_id from the private_data table where
    the username matches the given user_name.
    """
    table_name = "private_data"
    query = (
        supabase_.table(table_name=table_name)
        .select("user_id")
        .eq("username", user_name)
        .execute()
    )

    return query.data[0]["user_id"]


def fetch_All_User_Complaints_From_Aggregator(user_id):
    """
    This function retrieves all user complaints
    related to a specific aggregator. It fetches data
    from the aggregator_issues table where the
    aggregator_id matches the given user_id. The
    function returns a list of complaint data.
    """
    table_name = "aggregator_issues"
    query = (
        supabase_.table(table_name=table_name)
        .select("*")
        .eq("aggregator_id", user_id)
        .execute()
    )

    return query.data


def fetch_All_User_Complaints_From_Utility():
    """
    This function retrieves all user complaints related to the
    utility. It fetches data from the utility_issues
    table and returns a list of complaint data.
    """
    table_name = "utility_issues"
    query = supabase_.table(table_name=table_name).select("*").execute()

    return query.data


def fetch_Public_Key_From_Email(email):
    """
    This function retrieves the public key associated with a
    given email address. It fetches the public_key
    value from the private_data table where the
    email_id matches the provided email. The function
    returns the public key value as a string.
    """
    table_name = "private_data"
    query = (
        supabase_.table(table_name=table_name)
        .select("public_key")
        .eq("email_id", email)
        .execute()
    )

    return query.data[0]["public_key"]


# print(fetch_User_Total_Appliances("48a6cc6b-93c7-4a31-b0c9-bef7b27675bb"))

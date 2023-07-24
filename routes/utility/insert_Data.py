import os
import httpx
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = True
SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")

supabase_: Client = create_client(supabase_url=SUPABASE_URL, supabase_key=SUPABASE_KEY)


# def insert_One_Into_Consumer_Dashboard(user_id, total_trades, access_grants, access_rejected, average_wh_hour, average_cost_hour, some_other_stats):
#     table_name = 'consumer_dashboard'
#     row = {
#         'user_id': user_id,
#         'total_trades': total_trades,
#         'access_grants' : access_grants,
#         'access_rejected' : access_rejected,
#         'average_wh/hour' : average_wh_hour,
#         'average_cost/hour' : average_cost_hour,
#         'some_other_stats': some_other_stats,
#         'user_id': ''
#     }
#     response = supabase_.table(table_name).insert(row).execute()
#     return response


def insert_Many_Into_Consumer_Dashboard(data, type):
    table_name = None
    if type == "producer":
        table_name = "producer_dashboard"
    elif type == "consumer":
        table_name = "consumer_dashboard"
    supabase_.table(table_name=table_name).insert(data).execute()


def insert_Many_Into_Consumer_History(data, type):
    table_name = None
    if type == "producer":
        table_name = "producer_history"
    elif type == "consumer":
        table_name = "consumer_history"
    supabase_.table(table_name=table_name).insert(data).execute()


def insert_Many_into_Consumer_Monitor(data, type):
    table_name = None
    if type == "producer":
        table_name = "producer_monitor"
    elif type == "consumer":
        table_name = "consumer_monitor"
    try:
        supabase_.table(table_name=table_name).insert(data).execute()
    except httpx.ConnectTimeout as e:
        print(e.args)
    except httpx.WriteTimeout as e:
        print(e.args)


def insert_Into_Private_Data_From_Aggregator(row: dict):
    table_name = "private_data"
    supabase_.table(table_name=table_name).insert(row).execute()


def insert_Into_Aggregator_Data_From_Aggregator(user_id: str, username: str):
    table_name = "aggregator_data"
    row = {"aggregator_id": user_id, "username": username}
    supabase_.table(table_name=table_name).insert(row).execute()


def send_Issue_Message_To_Aggregator(username, email, message):
    table_name = "aggregator_issues"
    row = {"username": username, "message": message, "email": email}

    supabase_.table(table_name=table_name).insert(row).execute()


def send_Issue_Message_To_Utility(username, email, message):
    table_name = "utility_issues"
    row = {"username": username, "message": message, "email": email}

    supabase_.table(table_name=table_name).insert(row).execute()

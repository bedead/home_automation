from __config__ import Config
supabase_ = Config.supabase_

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

def insert_Many_Into_Consumer_Dashboard(data):
    table_name = 'consumer_dashboard'
    response = supabase_.table(table_name=table_name).insert(data).execute()

def insert_Many_Into_Consumer_History(data):
    table_name = 'consumer_history'
    response = supabase_.table(table_name=table_name).insert(data).execute()

def insert_Many_into_Consumer_Monitor(data, type):
    table_name = None
    if (type == 'producer'):
        table_name = 'producer_monitor'
    elif (type == 'consumer'):
        table_name = 'consumer_monitor'
    response = supabase_.table(table_name=table_name).insert(data).execute()
    
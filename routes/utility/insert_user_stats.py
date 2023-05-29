from __config__ import Config
supabase_ = Config.supabase_

table_name = 'user_stats'

# def insert_Empty_Into_User_Stats(user_uuid):
#     row = {
#         'user_uuid': user_uuid,
#         'total_trades': 0,
#         'access_grants' : 0,
#         'access_rejected' : 0,
#         'average_wh/hour' : 0,
#         'average_cost/hour' : 0,
#     }

#     response = supabase_.table(table_name).insert(row).execute()

#     return response

def update_Into_User_Stats(user_uuid):
    row = {
        'user_uuid': '',
        'total_trades': 0,
        'access_grants' : 0,
        'access_rejected' : 0,
        'average_wh/hour' : 0,
        'average_cost/hour' : 0,
    }
    pass
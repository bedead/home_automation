from ..__config__ import Config
supabase_ = Config.supabase_

def compute_Avg(info,column_name):
    val = 0
    for each in info:
        val += each[column_name]
    
    val = val / len(info)

    return round(val, 2)

def fetch_From_Consumer_Dashboard(user_id):
    table_name = "consumer_dashboard"
    col1 = 'total_trades'; col2='average_wh_hour';col3='average_cost_hour';col4="access_grants"
    col5 = 'access_rejected';col6 = 'some_other_stats'
    # defining all queries
    q1 = supabase_.table(table_name=table_name).select(col1).eq('user_id', user_id).order('created_at', desc=True).limit(1)
    q2 = supabase_.table(table_name=table_name).select(col2).eq('user_id', user_id).order('created_at', desc=True).limit(10)
    q3 = supabase_.table(table_name=table_name).select(col3).eq('user_id', user_id).order('created_at', desc=True).limit(10)
    q4 = supabase_.table(table_name=table_name).select(col4).eq('user_id', user_id).order('created_at', desc=True).limit(1)
    q5 = supabase_.table(table_name=table_name).select(col5).eq('user_id', user_id).order('created_at', desc=True).limit(1)
    q6 = supabase_.table(table_name=table_name).select(col6).eq('user_id', user_id).order('created_at', desc=True).limit(1)
 
    # executing all queries to fetch data
    total_trades = q1.execute();average_wh_hour = q2.execute();average_cost_hour = q3.execute()
    access_grants = q4.execute();access_rejected = q5.execute();some_other = q6.execute()

    # finding average of top 10 values of average_wh_hour and average_cost_hour 
    average_wh_hour = compute_Avg(average_wh_hour.data,col2)    
    average_cost_hour = compute_Avg(average_cost_hour.data,col3) 

    # print(average_wh_hour)
    # print(average_cost_hour)   
    

    # returning all values (including average value)
    return total_trades.data[0][col1], average_wh_hour, average_cost_hour, access_grants.data[0][col4], access_rejected.data[0][col5], some_other.data[0][col6]

def fetch_From_Consumer_History(user_id):
    table_name = "consumer_history"
    query = supabase_.table(table_name=table_name).select('*').eq('user_id', user_id).order('created_at', desc=True).limit(7)
    response = query.execute()
    
    return response.data

def fetch_From_Consumer_Monitor(user_id):
    table_name = "consumer_monitor"
    query = supabase_.table(table_name=table_name).select('*').eq('user_id', user_id).order('created_at', desc=True).limit(5)
    response = query.execute()
    
    return response.data

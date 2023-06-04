from flask import redirect, url_for
from routes.data_generator.encrypt import decrypt_Text

from routes.utility.general_methods import get_Fetch_Exception_Details
from ..__config__ import Config
supabase_ = Config.supabase_

def compute_Avg(info,column_name):
    val = 0
    for each in info:
        plainInt = int(decrypt_Text(each[column_name]))
        val += plainInt
    val = val / len(info)
    return round(val, 2)


def fetch_From_Consumer_Dashboard(user_id):
    table_name = "consumer_dashboard"
    col1 = 'total_trades'; col2='average_wh_hour';col3='average_cost_hour';col4="access_grants"
    col5 = 'access_rejected';col6 = 'some_other_stats'
    # defining all queries
    q1 = supabase_.table(table_name=table_name).select(col1).eq('user_id', user_id).order('created_at', desc=True).limit(1)
    q2 = supabase_.table(table_name=table_name).select(col2).eq('user_id', user_id).order('created_at', desc=True).limit(7)
    q3 = supabase_.table(table_name=table_name).select(col3).eq('user_id', user_id).order('created_at', desc=True).limit(7)
    q4 = supabase_.table(table_name=table_name).select(col4).eq('user_id', user_id).order('created_at', desc=True).limit(1)
    q5 = supabase_.table(table_name=table_name).select(col5).eq('user_id', user_id).order('created_at', desc=True).limit(1)
    q6 = supabase_.table(table_name=table_name).select(col6).eq('user_id', user_id).order('created_at', desc=True).limit(1)
 
    # executing all queries to fetch data
    try:
        total_trades = q1.execute();average_wh_hour = q2.execute();average_cost_hour = q3.execute()
        access_grants = q4.execute();access_rejected = q5.execute();some_other = q6.execute()
    except Exception as e:
        get_Fetch_Exception_Details(e)
        # return redirect(url_for('error_page.base_error'))
    
    # decryption
    total_trades = int(decrypt_Text(total_trades.data[0][col1]))
    access_grants = int(decrypt_Text(access_grants.data[0][col4]))
    access_rejected = int(decrypt_Text(access_rejected.data[0][col5]))
    some_other = int(decrypt_Text(some_other.data[0][col6]))

    # finding average of top 10 values of average_wh_hour and average_cost_hour 
    average_wh_hour = compute_Avg(average_wh_hour.data,col2)    
    average_cost_hour = compute_Avg(average_cost_hour.data,col3) 

    # print(average_wh_hour)
    # print(average_cost_hour)   
    

    # returning all values (including average value)
    return total_trades, average_wh_hour, average_cost_hour, access_grants, access_rejected, some_other


def fetch_From_Consumer_History(user_id):
    table_name = "consumer_history"
    query = supabase_.table(table_name=table_name).select('*').eq('user_id', user_id).order('created_at', desc=True).limit(7)
    try:
        response = query.execute()
    except Exception as e:
        get_Fetch_Exception_Details(e)
        return redirect(url_for('error_page.base_error'))
    
    data = response.data
    for each_index in range(len(data)):
        data[each_index]['full_name'] = decrypt_Text(data[each_index]['full_name'])
        data[each_index]['wh_hour_price'] = int(decrypt_Text(data[each_index]['wh_hour_price']))
        data[each_index]['email'] = decrypt_Text(data[each_index]['email'])
        

    return data


def fetch_From_Consumer_Monitor(user_id):
    table_name = "consumer_monitor"
    query = supabase_.table(table_name=table_name).select('*').eq('user_id', user_id).order('created_at', desc=True).limit(5)
    try:
        response = query.execute()
    except Exception as e:
        get_Fetch_Exception_Details(e)
        return redirect(url_for('error_page.base_error'))
    
    # decrypting each column value 
    data = response.data
    for each_index in range(len(data)):
        data[each_index]['room'] = decrypt_Text(data[each_index]['room'])
        data[each_index]['wh_hour'] = int(decrypt_Text(data[each_index]['wh_hour']))
        data[each_index]['temp'] = int(decrypt_Text(data[each_index]['temp']))

    return response.data


# fetch_From_Consumer_History('19353ea3-5608-4971-b168-cccf5a9324a7')

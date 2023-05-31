from __config__ import Config
supabase_ = Config.supabase_

def fetch_From_Consumer_Dashboard(user_id):
    table_name = "consumer_dashboard"
    query = supabase_.table(table_name=table_name).select('*').eq('user_id', user_id).order('created_at', ascending=False).limit(10)
    response = query.execute()
    
    return response

def fetch_From_Consumer_History(user_id):
    table_name = "consumer_history"
    query = supabase_.table(table_name=table_name).select('*').eq('user_id', user_id).order('created_at', ascending=False).limit(10)
    response = query.execute()
    
    return response

def fetch_From_Consumer_Monitor(user_id):
    table_name = "consumer_monitor"
    query = supabase_.table(table_name=table_name).select('*').eq('user_id', user_id).order('created_at', ascending=False).limit(10)
    response = query.execute()
    
    return response
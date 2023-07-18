from flask import session

def get_User_Type_Route():
    consumer = "consumer_page.consumer_monitor"
    producer = "producer_page.producer_monitor"
    procumer = "producer_page.prosumer_monitor"
    Aggregator = "aggregator_page.aggregator_dashboard"
    Utility = "utility_page.utility_dashboard"

    if session['user-type'] == "Consumer":
        return consumer
    elif session['user-type'] == "Producer":
        return producer
    elif session['user-type'] == "Prosumer":
        return procumer
    elif session['user-type'] == "Aggregator":
        return Aggregator
    elif session['user-type'] == "Utility":
        return Utility
    

def set_User_Session(email, user_type, user_id, access_token,shared_key_list = None, other_public_key=None, user_private_key=None,aggregator_id=None):
    session['email'] = email
    session['access_token'] = access_token
    session['user-type'] = user_type
    session['user_id'] = user_id
    session['shared_key_list'] = shared_key_list
    session['aggregator_id'] = aggregator_id
    session['other_public_key'] = other_public_key
    session['user_private_key'] = user_private_key

def get_User_Session_Details():
    return session['email'], session['user-type'], session['user_id']

def get_Shared_Key_List():
    return session['shared_key_list']

def get_User_Session_Other_Public_Key():
    return session['other_public_key']

def get_User_Session_Private_Key():
    return session['user_private_key']

def get_User_Aggregator_Id():
    return session['aggregator_id']

def get_User_User_Id():
    return session['user_id']

def clear_User_Session():
    session.clear()

def get_User_Exception_Details(e):
    exception_dict = e.__dict__
    message = exception_dict['message']
    # name = exception_dict['name']
    # status = exception_dict['status']
            
    return message

def get_Fetch_Exception_Details(e):
    
    pass
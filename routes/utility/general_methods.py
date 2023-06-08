from flask import session

def get_User_Type_Route():
    consumer = "consumer_page.consumer_monitor"
    producer = "producer_page.producer_monitor"
    Aggregator = "aggregator_page.aggregator_dashboard"

    if session['user-type'] == "Consumer":
        return consumer
    elif session['user-type'] == "Producer":
        return producer
    elif session['user-type'] == "Aggregator":
        return Aggregator
    

def set_User_Session(email, user_type, user_id, session_token=None):
    session['email'] = email
    session['user-type'] = user_type
    session['session_token'] = session_token
    session['user_id'] = user_id

def get_User_Session_Details():
    return session['email'], session['user-type'], session['user_id']

def clear_User_Session():
    session.clear()

def get_User_Exception_Details(e):
    exception_dict = e.__dict__
    message = exception_dict['message']
    name = exception_dict['name']
    status = exception_dict['status']
            
    return message, name, status

def get_Fetch_Exception_Details(e):
    
    pass
from flask import session

def get_User_Type_Route():
    consumer = "consumer_page.consumer_dashboard"
    producer = "producer_page.producer_dashboard"
    prosumer = "prosumer_page.prosumer_dashboard"
    Aggregator = "aggregator_page.aggregator_dashboard"

    if session['user-type'] == "Consumer":
        return consumer
    elif session['user-type'] == "Producer":
        return producer
    elif session['user-type'] == "Prosumer":
        return prosumer
    elif session['user-type'] == "Aggregator":
        return Aggregator
    

def set_User_Session(email, user_type, session_token=None):
    session['email'] = email
    session['user-type'] = user_type
    session['session_token'] = session_token

def clear_User_Session():
    session.clear()

def get_Exception_Details(e):
    exception_dict = e.__dict__
    message = exception_dict['message']
    name = exception_dict['name']
    status = exception_dict['status']
            
    return message, name, status

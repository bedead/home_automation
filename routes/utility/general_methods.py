from flask import session

def get_User_Type_Route():
    consumer = "dashboard_page.consumer_dashboard"
    producer = "dashboard_page.producer_dashboard"
    prosumer = "dashboard_page.prosumer_dashboard"
    Aggregator = "dashboard_page.aggregator_dashboard"

    if session['user-type'] == "Consumer":
        return consumer
    elif session['user-type'] == "Producer":
        return producer
    elif session['user-type'] == "Prosumer":
        return prosumer
    elif session['user-type'] == "Aggregator":
        return Aggregator
    

def set_User_Session(email, user_type):
    session['email'] = email
    session['user-type'] = user_type

def clear_User_Session():
    session.clear()

def get_Exception_Details(e):
    exception_dict = e.__dict__
    message = exception_dict['message']
    name = exception_dict['name']
    status = exception_dict['status']
            
    return message, name, status
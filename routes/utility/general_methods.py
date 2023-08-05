from flask import session

"""
get_User_Type_Route(): Determines the appropriate route based on the user's 
type (Consumer, Producer, Prosumer, 
Aggregator, or Utility) for redirection after logging in.

set_User_Session(...): Sets various user-related information in the 
session, including email, user type, user ID, access token, 
username, public and private keys, aggregator ID, and more.

set_Utility_Chaos_Key(key): Sets the chaos key associated with a utility user in the session.

get_Utility_Public_Key(): Retrieves the utility user's public key from the session.

get_User_Session_Details(): Retrieves user details from the session, 
including email, user type, and user ID.

get_User_Username(): Retrieves the username from the session.

get_Chaos_Key_List_Aggregator(): Retrieves the chaos key 
associated with an aggregator user from the session.

get_User_Session_Other_Public_Key(): Retrieves another user's public key from the session.

get_User_Session_Private_Key(): Retrieves the user's private key from the session.

get_User_Aggregator_Id(): Retrieves the aggregator ID from the session.

get_User_User_Id(): Retrieves the user ID from the session.

clear_User_Session(): Clears the user session, effectively logging the user out.

get_User_Exception_Details(e): Extracts and returns exception details 
such as the error message from an exception object.

get_Fetch_Exception_Details(e): Prints the exception details for debugging purposes.
"""


def get_User_Type_Route():
    consumer = "consumer_page.consumer_monitor"
    producer = "producer_page.producer_monitor"
    procumer = "producer_page.prosumer_monitor"
    Aggregator = "aggregator_page.aggregator_dashboard"
    Utility = "utility_page.utility_dashboard"

    if session["user-type"] == "Consumer":
        return consumer
    elif session["user-type"] == "Producer":
        return producer
    elif session["user-type"] == "Prosumer":
        return procumer
    elif session["user-type"] == "Aggregator":
        return Aggregator
    elif session["user-type"] == "Utility":
        return Utility


def set_User_Session(
    email,
    user_type,
    user_id,
    access_token,
    username=None,
    other_public_key=None,
    user_private_key=None,
    aggregator_id=None,
    chaos_key_aggregator=None,
    utility_public_key=None,
):
    session["email"] = email
    session["username"] = username
    session["access_token"] = access_token
    session["user-type"] = user_type
    session["user_id"] = user_id
    session["aggregator_id"] = aggregator_id
    session["other_public_key"] = other_public_key
    session["user_private_key"] = user_private_key
    session["chaos_key_aggregator"] = chaos_key_aggregator
    session["utility_public_key"] = utility_public_key


def set_Utility_Chaos_Key(key):
    session["chaos_key_utility"] = key


def get_Utility_Public_Key():
    return session["utility_public_key"]


def get_User_Session_Details():
    return session["email"], session["user-type"], session["user_id"]


def get_User_Username():
    return session["username"]


def get_Chaos_Key_List_Aggregator():
    return session["chaos_key_aggregator"]


def get_User_Session_Other_Public_Key():
    return session["other_public_key"]


def get_User_Session_Private_Key():
    return session["user_private_key"]


def get_User_Aggregator_Id():
    return session["aggregator_id"]


def get_User_User_Id():
    return session["user_id"]


def clear_User_Session():
    session.clear()


def get_User_Exception_Details(e):
    exception_dict = e.__dict__
    message = exception_dict["message"]
    # name = exception_dict['name']
    # status = exception_dict['status']

    return message


def get_Fetch_Exception_Details(e):
    print(e)

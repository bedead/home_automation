"""
This code snippet defines a Flask blueprint named api_insert_bp, which 
handles API routes responsible for inserting data into a database, 
particularly Supabase. These routes facilitate the insertion of replies to market player 
complaints and sending messages to utility sources.
"""
# Create a blueprint for the home routes
from flask import Blueprint, request
from routes.__config__ import Config


api_insert_bp = Blueprint("api_insert_page", __name__)

supabase_ = Config.supabase_


@api_insert_bp.route(
    "/api/insert/reply_to_market_players_complaints/", methods=["POST"]
)
def send_reply_to_market_player_complaints():
    """
    function handles the route /api/insert/reply_to_market_players_complaints/.
    It receives a JSON payload containing the cipher_reply (encrypted reply)
    and complaint_id. The function updates the aggregator_issues table in
    Supabase, setting the reply field with the provided encrypted reply. The update is
    targeted at the record with the specified complaint_id.
    """

    data = request.get_json()

    try:
        cipher_reply = data["cipher_reply"]
        complaint_id = data["complaint_id"]

        table_name = "aggregator_issues"
        row = {
            "reply": cipher_reply,
        }
        resp = (
            supabase_.table(table_name=table_name)
            .update(row)
            .eq("id", complaint_id)
            .execute()
        )

        return "success", 200
    except Exception as e:
        print(e.args)

        return "error", 500


@api_insert_bp.route("/api/insert/send_message_to_utility/", methods=["POST"])
def send_message_to_utility():
    """
    function is associated with the route /api/insert/send_message_to_utility/.
    This route expects JSON data containing username, cipher_text (encrypted message),
    email, and aggregator_id. The function inserts a new row into the
    aggregator_to_utility_issues table in Supabase, storing the
    encrypted message along with other provided details.
    """
    data = request.get_json()

    try:
        username = data["username"]
        cipher_text = data["cipher_text"]
        email = data["email"]
        aggregator_id = data["aggregator_id"]

        table_name = "aggregator_to_utility_issues"
        row = {
            "username": username,
            "message": cipher_text,
            "email": email,
            "aggregator_id": aggregator_id,
        }

        response = supabase_.table(table_name=table_name).insert(row).execute()

        return "success", 200
    except Exception as e:
        print(e.args)

        return "error", 500

"""
Flask blueprint named api_fetch_bp, dedicated to handling various API fetch 
routes for retrieving data from a database, specifically Supabase. These 
routes enable fetching details related to aggregator 
dashboards, complaints, and messages from utility sources.
"""

# Create a blueprint for the home routes
from flask import Blueprint, request
from routes.__config__ import Config


api_fetch_bp = Blueprint("api_fetch_page", __name__)

supabase_ = Config.supabase_


@api_fetch_bp.route("/api/fetch/all_aggregator_dashboard_details/", methods=["POST"])
def fetch_all_aggregator_dashboard_details():
    """
    function handles the route /api/fetch/all_aggregator_dashboard_details/.
    This route receives a JSON payload, extracts the aggregator_id, and
    queries the Supabase table aggregator_dashboard to fetch
    all records associated with the provided aggregator_id.
    """
    data = request.get_json()

    try:
        aggregator_id = data["aggregator_id"]

        table_name = "aggregator_dashboard"
        query = (
            supabase_.table(table_name=table_name)
            .select("*")
            .eq("aggregator_id", aggregator_id)
            .order("created_at", desc=True)
            .execute()
        )

        return query.data, 200
    except Exception as e:
        print(e.args)

        return "error", 500


@api_fetch_bp.route("/api/fetch/one_aggregator_dashboard_details/", methods=["POST"])
def fetch_one_aggregator_dashboard_details():
    """
    function manages the route /api/fetch/one_aggregator_dashboard_details/.
    This route receives JSON data containing aggregator_id, created_at,
    and user_id. It queries the aggregator_dashboard table
    to fetch a specific record matching the given parameters.
    """
    data = request.get_json()

    try:
        aggregator_id = data["aggregator_id"]
        created_at = data["created_at"]
        user_id = data["user_id"]

        table_name = "aggregator_dashboard"
        query = (
            supabase_.table(table_name=table_name)
            .select("*")
            .eq("user_id", user_id)
            .eq("aggregator_id", aggregator_id)
            .eq("created_at", created_at)
        ).execute()

        return query.data, 200
    except Exception as e:
        print(e.args)

        return "error", 500


@api_fetch_bp.route("/api/fetch/all_aggregator_complaints/", methods=["POST"])
def fetch_all_aggregator_complaints():
    """
    function is associated with the route /api/fetch/all_aggregator_complaints/.
    It receives JSON data with an aggregator_id, queries the aggregator_issues
    table in Supabase, and retrieves
    all complaints associated with the given aggregator_id.
    """
    data = request.get_json()

    try:
        aggregator_id = data["aggregator_id"]

        table_name = "aggregator_issues"
        query = (
            supabase_.table(table_name=table_name)
            .select("*")
            .eq("aggregator_id", aggregator_id)
            .execute()
        )

        return query.data, 200
    except Exception as e:
        print(e.args)

        return "error", 500


@api_fetch_bp.route("/api/fetch/one_latest_message_from_utility/", methods=["POST"])
def fetch_latest_message_details_from_utility():
    """
    function handles the route /api/fetch/one_latest_message_from_utility/. This
    route expects JSON data containing the email of a user. It queries
    the aggregator_to_utility_issues table in Supabase, sorts the results
    in descending order of created_at, limits the result to one entry, and
    retrieves the latest message from the utility source.
    """
    data = request.get_json()

    try:
        email = data["email"]

        table_name = "aggregator_to_utility_issues"
        query = (
            supabase_.table(table_name=table_name)
            .select("*")
            .eq("email", email)
            .order("created_at", desc=True)
            .limit(1)
            .execute()
        )

        return query.data, 200
    except Exception as e:
        print(e.args)

        return "error", 500

# Create a blueprint for the home routes
from flask import Blueprint, request
from routes.__config__ import Config


api_fetch_bp = Blueprint("api_fetch_page", __name__)

supabase_ = Config.supabase_


@api_fetch_bp.route("/api/fetch/all_aggregator_dashboard_details/", methods=["POST"])
def fetch_all_aggregator_dashboard_details():
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

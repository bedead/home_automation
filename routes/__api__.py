import json
from flask import Blueprint, render_template, request, send_file

from routes.__config__ import Config
from routes.data_generator.tp_chaos_generator.tp_chaos_generator.triple_pendulum import (
    decode_key,
    encrypt_Text_New,
    get_encoded_key,
)
from routes.utility.diffi_hellman_EC import get_Shared_Key
from routes.utility.fetch_Data import (
    fetch_From_Consumer_Dashboard,
    fetch_From_Consumer_History,
    fetch_From_Consumer_Monitor,
    fetch_From_Producer_Dashboard,
    fetch_From_Producer_History,
    fetch_From_Producer_Monitor,
    get_Aggregator_Id_From_Username,
)
from routes.utility.insert_Data import (
    send_Issue_Message_To_Aggregator,
    send_Issue_Message_To_Utility,
)

# Create a blueprint for the home routes
api_page_bp = Blueprint("api_page", __name__)

supabase_ = Config.supabase_


@api_page_bp.route("/api/test/", methods=["GET"])
def test():
    return "success", 200


@api_page_bp.route("/api/user/create_account/", methods=["POST"])
def market_player_create_account():
    data = request.get_json()
    return_data = {}
    try:
        user = supabase_.auth.sign_up(
            {
                "email": data["email"],
                "password": data["password"],
                "options": {
                    "data": {
                        "user-type": data["user_type"],
                        "private-key": data["private_key"],
                        "username": data["username"],
                        "user_address": data["user_address"],
                    }
                },
            }
        )
        if user:
            table_name = "private_data"
            aggregator_id = get_Aggregator_Id_From_Username(data["aggre_type"])
            # print("Selected Aggregator_id : ", aggregator_id)
            row = {
                "user_id": user.user.id,
                "public_key": data["public_key"],
                "user_type": data["user_type"],
                "email_id": data["email"],
                "username": data["username"],
                "utility_public_key": "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d485977454159484b6f5a497a6a3043415159464b34454541434944596741456d466d7641695041526b554c6b63494e4b6e476369704f57586b7275744539630a772f656f6b7870386a41686d4b79716757646536553372306331417038473058366158536876724755456166313276785076427575356973337868767663515a0a6d576a4753707164716634387362317338384853314364766e663469412b51350a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a",
                "mac_address": data["mac_address"],
                "aggregator_id": aggregator_id,
            }

            response1 = (
                supabase_.table(table_name=table_name)
                .select("public_key")
                .eq("user_id", aggregator_id)
                .execute()
            )
            aggregator_public_key = response1.data[0]["public_key"]

            shared_key_hex = get_Shared_Key(data["private_key"], aggregator_public_key)
            encoded_key = get_encoded_key(shared_key_hex)
            generate_keys_list = decode_key(encoded_key[0])
            # print("Chaos key :", generate_keys_list)

            encrypted_generate_key_list = encrypt_Text_New(str(generate_keys_list))
            # print("Encrypted Chaos key :", encrypted_generate_key_list)
            try:
                response = supabase_.table(table_name=table_name).insert(row).execute()
            except Exception as e:
                print(e.args)
                print("private data insert error")
                return "Data not stored", 507

    except Exception as e:
        print(e.args)
        print("Sign in Error")

        return "Sign in error", 500
    return_data["user_id"] = user.user.id
    return_data["aggregator_id"] = aggregator_id
    return_data["aggregator_public_key"] = aggregator_public_key
    return_data["encrypted_chaos"] = encrypted_generate_key_list

    return return_data, 200


user = {}


@api_page_bp.route("/api/user/signin/", methods=["POST"])
def api_sign_in():
    data = request.get_json()
    return_data = {}
    user1 = supabase_.auth.sign_in_with_password(
        {"email": data["email"], "password": data["password"]}
    )
    print(user1.session.access_token)
    if user1:
        global user
        user = user1
        return_data["access_token"] = user1.session.access_token
        return_data["refresh_token"] = user1.session.refresh_token
        return_data["user_id"] = user1.user.id

        return return_data, 200
    else:
        return "error", 500


@api_page_bp.route("/api/user/signout/", methods=["GET"])
def api_sign_out():
    global user
    if user:
        print(user.user.email)
        out = supabase_.auth.sign_out()

        return "success", 200
    else:
        return "Unauthorized", 401


@api_page_bp.route("/api/aggregator/create_account", methods=["POST"])
def aggregator_create_account():
    data = request.get_json()
    return_data = {}
    try:
        user = supabase_.auth.sign_up(
            {
                "email": data["email"],
                "password": data["password"],
                "options": {
                    "data": {
                        "user-type": data["user_type"],
                        "private-key": data["private_key"],
                        "username": data["username"],
                        "user_address": data["user_address"],
                    }
                },
            }
        )
        if user:
            utility_public_key = "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d485977454159484b6f5a497a6a3043415159464b34454541434944596741456d466d7641695041526b554c6b63494e4b6e476369704f57586b7275744539630a772f656f6b7870386a41686d4b79716757646536553372306331417038473058366158536876724755456166313276785076427575356973337868767663515a0a6d576a4753707164716634387362317338384853314364766e663469412b51350a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a"
            row = {
                "user_id": user.user.id,
                "public_key": data["private_key"],
                "user_type": data["user_type"],
                "email_id": data["email"],
                "username": data["username"],
                "utility_public_key": utility_public_key,
            }

            table_name = "private_data"
            res = supabase_.table(table_name=table_name).insert(row).execute()

            table_name = "aggregator_data"
            row1 = {"aggregator_id": user.user.id, "username": data["username"]}
            res1 = supabase_.table(table_name=table_name).insert(row1).execute()

            shared_key_hex = get_Shared_Key(data["private_key"], utility_public_key)
            encoded_key = get_encoded_key(shared_key_hex)
            generate_keys_list = decode_key(encoded_key[0])
            # print("Chaos key :", generate_keys_list)

            encrypted_generate_key_list = encrypt_Text_New(str(generate_keys_list))

    except Exception as e:
        print(e.args)
        print("Sign in Error")

        return "Sign in error", 500

    return_data["user_id"] = user.user.id
    return_data["utility_public_key"] = utility_public_key
    return_data["encrypted_chaos"] = encrypted_generate_key_list

    return return_data, 200


@api_page_bp.route("/api/market_player/consumer/monitor", methods=["POST"])
def consumer_fetch_Monitor_data():
    global user
    if user:
        data = request.get_json()
        return_data = fetch_From_Consumer_Monitor(data["user_id"])

        return return_data, 200
    else:
        return "Unauthorized", 401


@api_page_bp.route("/api/market_player/consumer/dashboard", methods=["POST"])
def consumer_fetch_Dashboard_data():
    global user
    if user:
        data = request.get_json()
        return_data = fetch_From_Consumer_Dashboard(data["user_id"])

        return return_data, 200
    else:
        return "Unauthorized", 401


@api_page_bp.route("/api/market_player/consumer/history", methods=["POST"])
def consumer_fetch_History_data():
    global user
    if user:
        data = request.get_json()
        return_data = fetch_From_Consumer_History(data["user_id"])

        return return_data, 200
    else:
        return "Unauthorized", 401


@api_page_bp.route("/api/market_player/producer/monitor", methods=["POST"])
def producer_fetch_Monitor_data():
    global user
    if user:
        data = request.get_json()
        return_data = fetch_From_Producer_Monitor(data["user_id"])

        return return_data, 200
    else:
        return "Unauthorized", 401


@api_page_bp.route("/api/market_player/producer/dashboard", methods=["POST"])
def producer_fetch_Dashboard_data():
    global user
    if user:
        data = request.get_json()
        return_data = fetch_From_Producer_Dashboard(data["user_id"])

        return return_data, 200
    else:
        return "Unauthorized", 401


@api_page_bp.route("/api/market_player/producer/history", methods=["POST"])
def producer_fetch_History_data():
    global user
    if user:
        data = request.get_json()
        return_data = fetch_From_Producer_History(data["user_id"])

        return return_data, 200
    else:
        return "Unauthorized", 401


@api_page_bp.route("/api/utility/get_utility_chaos", methods=["POST"])
def send_utility_public():
    utility_public_key = "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d485977454159484b6f5a497a6a3043415159464b34454541434944596741454247394c6a7a794a2b652b61706e7139622b416571552f535259707472334e700a4673723852696933663270664b4a717676416a7758533550756e346972374965424a7a2b4e6568704266645062735562465139366258776e674d362b455342570a723974792b50772b367936485176426c4654754f2b4778736c7750553863322b0a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a"
    data = request.get_json()

    shared_hex_key = get_Shared_Key(data["user_private_key"], utility_public_key)
    encoded_key = get_encoded_key(shared_hex_key)
    utility_chaos_key = decode_key(encoded_key[0])

    encrypted_utility_chaos_list = encrypt_Text_New(str(utility_chaos_key))
    return encrypted_utility_chaos_list, 200

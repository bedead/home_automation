from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    session,
)
from routes.__config__ import Config
from routes.data_generator.tp_chaos_generator.tp_chaos_generator.triple_pendulum import (
    decode_key,
    get_encoded_key,
)

# from routes.utility.fetch_Data import fetch_Private_Key_From_Private_Data
from routes.utility.diffi_hellman_EC import (
    generate_Hex_Private_Public_Key,
    get_Shared_Key,
)
from routes.utility.fetch_Data import get_Aggregator_Id_From_Username
from routes.utility.insert_Data import (
    insert_Into_Aggregator_Data_From_Aggregator,
    insert_Into_Private_Data_From_Aggregator,
)
from .utility.general_methods import (
    get_User_Exception_Details,
    get_User_Type_Route,
    set_User_Session,
)
from gotrue.errors import AuthApiError
import csv, time

# Create a blueprint for the auth routes
auth_page_bp = Blueprint("auth_page", __name__)
supabase_ = Config.supabase_


@auth_page_bp.route("/auth/signup/", methods=["GET", "POST"])
def signup(pass_same=False):
    """
    Route for user signup.

    Args:
        pass_same (bool): Flag to indicate if password confirmation is the same.

    Returns:
        str: Redirects to various routes based on signup status.
    """
    if not session:
        # fetching all aggregators name
        table_name = "private_data"
        try:
            response = (
                supabase_.table(table_name=table_name)
                .select("username")
                .eq("user_type", "Aggregator")
                .execute()
            )

            aggregator_list = response.data

        except Exception as e:
            return redirect(url_for("error_page.unknown_error"))
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            user_type = request.form["user-type"]
            aggre_type = request.form["aggre-type"]
            user_address = request.form["address"]
            ip_address = request.form["ip_address"]
            # encrypt password here using 3DES
            password = request.form["password"]
            confirm_password = request.form["reenter_password"]

            # print(ip_address)
            if password == confirm_password:
                (
                    user_private_key_hex,
                    user_public_key_hex,
                ) = generate_Hex_Private_Public_Key()
                try:
                    user = supabase_.auth.sign_up(
                        {
                            "email": email,
                            "password": password,
                            "options": {
                                "data": {
                                    "user-type": user_type,
                                    "private-key": user_private_key_hex,
                                    "username": username,
                                    "user_address": user_address,
                                }
                            },
                        }
                    )

                    table_name = "private_data"
                    aggregator_id = get_Aggregator_Id_From_Username(aggre_type)
                    print("Selected Aggregator_id : ", aggregator_id)
                    row = {
                        "user_id": user.user.id,
                        "public_key": user_public_key_hex,
                        "user_type": user_type,
                        "email_id": email,
                        "username": username,
                        "utility_public_key": "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d485977454159484b6f5a497a6a3043415159464b34454541434944596741456d466d7641695041526b554c6b63494e4b6e476369704f57586b7275744539630a772f656f6b7870386a41686d4b79716757646536553372306331417038473058366158536876724755456166313276785076427575356973337868767663515a0a6d576a4753707164716634387362317338384853314364766e663469412b51350a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a",
                        # 'mac_address': 'sd',
                        "ip_address": ip_address,
                        "aggregator_id": aggregator_id,
                    }

                    try:
                        response = (
                            supabase_.table(table_name=table_name).insert(row).execute()
                        )
                    except Exception as e:
                        return redirect(url_for("error_page.unknown_error"))

                except ConnectionError as e:
                    message = get_User_Exception_Details(e)
                    print(message)
                    return redirect(url_for("error_page.unknown_error"))
                except Exception as e:
                    message = get_User_Exception_Details(e)
                    print(message)
                    return redirect(url_for("error_page.unknown_error"))

                if user.user.id != None:
                    return redirect(
                        url_for("auth_page.email_verificatation", email=email)
                    )

            else:
                pass_same = True
                # flag error saying both password are not same
                return redirect(url_for("auth_page.signup", pass_same=pass_same))

        # if pass_same is True render pop up in html saying passwords are same
        return render_template(
            "/auth/signup_page.html",
            pass_same=pass_same,
            aggregator_list=aggregator_list,
        )
    elif session:
        dashboard_type = get_User_Type_Route()

        return redirect(url_for(dashboard_type))


@auth_page_bp.route("/auth/signin/", methods=["GET", "POST"])
def signin():
    if not session:
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]
            # encrpt passeord here and send it to supabase server to auth
            user = None
            try:
                start_time = time.time()
                user = supabase_.auth.sign_in_with_password(
                    {"email": email, "password": password}
                )

                # print(user)
                if user.user.id != None:
                    # getting user details in python format
                    user_metadata = user.user.user_metadata
                    user_id = user.user.id
                    user_access_token = user.session.access_token

                    supabase_.postgrest.auth(user_access_token)

                    table_name = "private_data"
                    response = (
                        supabase_.table(table_name=table_name)
                        .select("aggregator_id", "utility_public_key", "username")
                        .eq("user_id", user_id)
                        .execute()
                    )
                    if user_metadata["user-type"] not in ["Aggregator", "Utility"]:
                        user_private_key = user_metadata["private-key"]
                        end_time = time.time()
                        time_taken_private_key_exchange = end_time - start_time
                        # for consumer, producer and prosumer

                        # print(response.data)
                        start_time = time.time()
                        aggregator_id = response.data[0]["aggregator_id"]
                        utility_public_key = response.data[0]["utility_public_key"]
                        username = response.data[0]["username"]

                        response1 = (
                            supabase_.table(table_name=table_name)
                            .select("public_key")
                            .eq("user_id", aggregator_id)
                            .execute()
                        )
                        aggregator_public_key = response1.data[0]["public_key"]
                        end_time = time.time()
                        time_taken_pubic_key_exchange = end_time - start_time

                        shared_key_hex = get_Shared_Key(
                            user_private_key, aggregator_public_key
                        )
                        encoded_key = get_encoded_key(shared_key_hex)
                        generate_keys_list = decode_key(encoded_key[0])

                        # print(user_private_key)
                        # print(aggregator_public_key)

                        # setting user login session
                        set_User_Session(
                            email=email,
                            username=username,
                            user_type=user_metadata["user-type"],
                            access_token=user_access_token,
                            user_private_key=user_private_key,
                            user_id=user_id,
                            utility_public_key=utility_public_key,
                            aggregator_id=aggregator_id,
                            chaos_key_aggregator=generate_keys_list,
                        )
                    else:
                        aggregator_private_key = user_metadata["private-key"]
                        aggregator_id = response.data[0]["aggregator_id"]
                        utility_public_key = response.data[0]["utility_public_key"]
                        username = response.data[0]["username"]
                        set_User_Session(
                            email=email,
                            username=username,
                            user_type=user_metadata["user-type"],
                            access_token=user_access_token,
                            user_id=user_id,
                            utility_public_key=utility_public_key,
                            user_private_key=aggregator_private_key,
                        )

                    # getting return dashboard type depending on user-type
                    dashboard_type = get_User_Type_Route()
                    print("New user joined-id:", user_id)
                    return redirect(url_for(dashboard_type))

            except ConnectionError as e:
                print(e.strerror)
            except AuthApiError as e:
                # status code == 400 for invalid credientials
                print(e.message)

        return render_template("/auth/signin_page.html")
    elif session:
        dashboard_type = get_User_Type_Route()

        return redirect(url_for(dashboard_type))
    else:
        # cases where internal error has occured
        message = "Same Internal Error has occured"
        pass


@auth_page_bp.route("/auth/become_aggregator/signup/", methods=["GET", "POST"])
def aggregator_signup(pass_same=False):
    """
    The aggregator_signup route, located within the authentication blueprint,
    facilitates the signup process for users aiming to become aggregators.
    It handles both GET and POST requests. For POST requests, the route
    validates user-provided data, generates encryption keys, and
    registers the user through Supabase. If successful, the user's data
    is added to relevant tables. If passwords don't match, a flag is
    set for error notification. For GET requests, the route either
    renders the signup form or redirects logged-in users
    based on their role to their respective dashboard.
    """
    if not session:
        if request.method == "POST":
            username = request.form["username"]
            email = request.form["email"]
            address = request.form["address"]
            password = request.form["password"]
            confirm_password = request.form["reenter_password"]
            user_type = "Aggregator"

            if password == confirm_password:
                (
                    user_private_key_hex,
                    user_public_key_hex,
                ) = generate_Hex_Private_Public_Key()
                try:
                    user = supabase_.auth.sign_up(
                        {
                            "email": email,
                            "password": password,
                            "options": {
                                "data": {
                                    "user-type": user_type,
                                    "private-key": user_private_key_hex,
                                    "username": username,
                                    "user_address": address,
                                }
                            },
                        }
                    )

                    row = {
                        "user_id": user.user.id,
                        "public_key": user_public_key_hex,
                        "user_type": user_type,
                        "email_id": email,
                        "username": username,
                        "utility_public_key": "2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d485977454159484b6f5a497a6a3043415159464b34454541434944596741456d466d7641695041526b554c6b63494e4b6e476369704f57586b7275744539630a772f656f6b7870386a41686d4b79716757646536553372306331417038473058366158536876724755456166313276785076427575356973337868767663515a0a6d576a4753707164716634387362317338384853314364766e663469412b51350a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a",
                    }

                    insert_Into_Private_Data_From_Aggregator(row)
                    insert_Into_Aggregator_Data_From_Aggregator(user.user.id, username)

                except ConnectionError as e:
                    message = get_User_Exception_Details(e)
                    print(message)
                    return redirect(url_for("error_page.unknown_error"))
                except Exception as e:
                    message = get_User_Exception_Details(e)
                    print(message)
                    return redirect(url_for("error_page.unknown_error"))

                if user.user.id != None:
                    return redirect(
                        url_for("auth_page.email_verificatation", email=email)
                    )

            else:
                pass_same = True
                # flag error saying both password are not same
                return redirect(
                    url_for("auth_page.aggregator_signup", pass_same=pass_same)
                )

        # if pass_same is True render pop up in html saying passwords are same
        return render_template("/auth/aggregator_signup_page.html", pass_same=pass_same)
    elif session:
        dashboard_type = get_User_Type_Route()

        return redirect(url_for(dashboard_type))


@auth_page_bp.route("/auth/email_verify/")
def email_verificatation():
    """
    This route handles email verification. It retrieves the email
    from the query parameters using request.args.get("email", None)
    and returns a message indicating that an email
    verification has been sent to the provided email address.
    """
    email = request.args.get("email", None)
    return f"Email verification has been sent to {email} mail."


@auth_page_bp.route("/auth/password_recovery/")
def password_recovery():
    """
    This route is related to password recovery. It checks if the
    password_recovery_ready flag is set to True. If not, it redirects
    to an "under construction" page using redirect(url_for("error_page.under_construction")).
    If the flag is
    set to True, it renders the password recovery page using
    """
    password_recovery_ready = False
    if not password_recovery_ready:
        return redirect(url_for("error_page.under_construction"))
    else:
        return render_template("/auth/password_recovery_page.html")


@auth_page_bp.route("/auth/logout/", methods=["GET", "POST"])
def logout():
    """
    This route handles user logout. It first prints the email of the
    current session user. Then, it signs the user out using supabase_.auth.sign_out(),
    clears the session using session.clear(), and finally redirects the user to
    the signin page using redirect(url_for("auth_page.signin")).
    """
    print(session["email"])
    out = supabase_.auth.sign_out()
    session.clear()
    print(out)
    return redirect(url_for("auth_page.signin"))

from flask import Blueprint, redirect, render_template, request, url_for, session, make_response
from routes.__config__ import Config
# from routes.utility.fetch_Data import fetch_Private_Key_From_Private_Data
from routes.utility.diffi_hellman_EC import generate_Hex_Private_Public_Key
from .utility.general_methods import get_User_Exception_Details, get_User_Type_Route, set_User_Session
from gotrue.errors import AuthApiError

# Create a blueprint for the auth routes
auth_page_bp = Blueprint("auth_page", __name__)
supabase_ = Config.supabase_


@auth_page_bp.route("/auth/signup/", methods=['GET','POST'])
def signup(pass_same=False):
    if not session:
        if request.method == 'POST':
            email = request.form['email']
            user_type = request.form['user-type']
            aggre_type = request.form['aggre-type']
            # encrypt password here using 3DES
            password = request.form['password']
            confirm_password = request.form['reenter_password']
            
            if (password==confirm_password):
                user_private_key_hex, user_public_key_hex = generate_Hex_Private_Public_Key()
                try:
                    user = supabase_.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {
                        "data":{
                            "user-type": user_type,
                            "private-key": user_private_key_hex,
                        }
                    }})
                    
                    table_name = 'private_data'
                    row = {
                            'user_id': user.user.id,
                            'public_key': user_public_key_hex,
                            'user_type': user_type,
                            'email_id': email,
                        }

                    if (user_type not in ['Utility', 'Aggregator'] ):
                        if (aggre_type == 'Aggregator-1'):
                            row['aggregator_id'] = '79867cfd-e0d5-4d5c-999e-492e02207cd5'
                        elif (aggre_type == 'Aggregator-2'):
                            row['aggregator_id'] = 'b9f77962-6db7-468a-9178-1f19d342bf4f'
                    else:
                        aggre_type = None

                    try:
                        response = supabase_.table(table_name=table_name).insert(row).execute()
                    except Exception as e:
                        return redirect(url_for('error_page.unknown_error'))

                except ConnectionError as e:
                    message = get_User_Exception_Details(e)
                    print(message)
                    return redirect(url_for('error_page.unknown_error'))
                except Exception as e:
                    message = get_User_Exception_Details(e)
                    print(message)
                    return redirect(url_for('error_page.unknown_error'))
                
                if user.user.id != None:
                    return redirect(url_for('auth_page.email_verificatation', email=email))
                
            else:
                pass_same = True
                # flag error saying both password are not same
                return redirect(url_for('auth_page.signup', pass_same=pass_same))
        
        
        # if pass_same is True render pop up in html saying passwords are same
        return render_template("/auth/signup_page.html", pass_same=pass_same)
    elif session:
        dashboard_type = get_User_Type_Route()

        return redirect(url_for(dashboard_type))


@auth_page_bp.route("/auth/signin/", methods=['GET', 'POST'])
def signin():
    if not session:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            # encrpt passeord here and send it to supabase server to auth
            user = None
            try:
                user = supabase_.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                print(user)
                if user.user.id != None:
                    # getting user details in python format
                    user_metadata = user.user.user_metadata
                    user_id = user.user.id
                    user_access_token = user.session.access_token

                    supabase_.postgrest.auth(user_access_token)
                    
                    if (user_metadata['user-type'] not in ['Aggregator','Utility']):
                        user_private_key = user_metadata['private-key']
                        # for consumer, producer and prosumer
                        
                        table_name = 'private_data'
                        response = supabase_.table(table_name=table_name).select('aggregator_id').eq('user_id',user_id).execute()

                        # print(response.data)
                        aggregator_id = response.data[0]['aggregator_id']

                        response1= supabase_.table(table_name=table_name).select('public_key').eq('user_id',aggregator_id).execute()
                        aggregator_public_key = response1.data[0]['public_key']
                        # print(user_private_key)
                        # print(aggregator_public_key)

                        # setting user login session
                        set_User_Session(email=email,
                                        user_type=user_metadata['user-type'],
                                        access_token=user_access_token,
                                        user_id=user_id,
                                        other_public_key=aggregator_public_key,
                                        user_private_key = user_private_key,
                                        aggregator_id=aggregator_id
                                        )
                    else:
                        aggregator_private_key = user_metadata['private-key']
                        set_User_Session(email=email,
                                        user_type=user_metadata['user-type'],
                                        access_token=user_access_token,
                                        user_id=user_id,
                                        user_private_key=aggregator_private_key)
                    
                    # getting return dashboard type depending on user-type
                    dashboard_type = get_User_Type_Route()
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


@auth_page_bp.route("/auth/email_verify/")
def email_verificatation():
    email = request.args.get('email', None)
    return f"Email verification has been sent to {email} mail."


@auth_page_bp.route("/auth/password_recovery/")
def password_recovery():
    password_recovery_ready = False
    if not password_recovery_ready:
        return redirect(url_for('error_page.under_construction'))
    else:
        return render_template('/auth/password_recovery_page.html')


@auth_page_bp.route("/auth/logout/", methods=['GET','POST'])
def logout():
    print(session['email'])
    out = supabase_.auth.sign_out()
    session.clear()
    print(out)
    return redirect(url_for('auth_page.signin'))
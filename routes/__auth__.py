from flask import Blueprint, redirect, render_template, request, url_for, session
from __config__ import Config
from .utility.general_methods import get_User_Type_Route, set_User_Session, get_Exception_Details

# Create a blueprint for the auth routes
auth_page_bp = Blueprint("auth_page", __name__)
supabase = Config.supabase_

@auth_page_bp.route("/auth/signup/", methods=['GET','POST'])
def signup(pass_same=False):
    if not session:
        if request.method == 'POST':
            email = request.form['email']
            user_type = request.form['user-type']
            password = request.form['password']
            confirm_password = request.form['reenter_password']

            if (password==confirm_password):
                try:
                    user = supabase.auth.sign_up({
                    "email": email,
                    "password": password,
                    "options": {
                        "data":{
                            "user-type": user_type,
                        }
                    }})
                except ConnectionError as e:
                    message, name, status = get_Exception_Details(e)
                    return redirect(url_for('error_page.base_error',
                                        status=status,
                                        message=message,
                                        ))
                except Exception as e:
                    message, name, status = get_Exception_Details(e)
                    return redirect(url_for('error_page.base_error',
                                        status=status,
                                        message=message,
                                        ))
                
                if user.user.id != None:
                    set_User_Session(email=email, user_type=user_type)

                    return redirect(url_for('auth_page.email_verificatation'))

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

            try:
                user = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                    })
            except ConnectionError as e:
                message, name, status = get_Exception_Details(e)
                return redirect(url_for('error_page.base_error',
                                        status=status,
                                        message=message,
                                        ))
            except Exception as e:
                message, name, status = get_Exception_Details(e)
                return redirect(url_for('error_page.base_error',
                                        status=status,
                                        message=message,
                                        ))

            if user.user.id != None:
                # getting user details in python format
                user = user.user
                user_type = user.user_metadata['user-type']
                set_User_Session(email=email, user_type=user_type)
                dashboard_type = get_User_Type_Route()
                
                return redirect(url_for(dashboard_type))
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
    if session:
        return "Email verification has been sent to you."
    else:
        return redirect(url_for('error_page.error_404'))



@auth_page_bp.route("/auth/email_verify/ok")
def email_verified(access_token):
    if session:
        return "Your email has been verified"
    else:
        return redirect(url_for('error_page.error_404'))



@auth_page_bp.route("/auth/password_recovery/")
def password_recovery():
    password_recovery_ready = False
    if not password_recovery_ready:
        return redirect(url_for('error_page.under_construction'))
    else:
        return render_template('/auth/password_recovery_page.html')







@auth_page_bp.route("/auth/logout/", methods=['GET','POST'])
def logout():
    if session:
        out = supabase.auth.sign_out()
        session.clear()
        return redirect(url_for('auth_page.signin'))
    else:
        return redirect(url_for('auth_page.signin'))
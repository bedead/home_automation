from flask import Blueprint, redirect, render_template, request, url_for, session
from __config__ import Config
# Create a blueprint for the home routes
auth_page_bp = Blueprint("auth_page", __name__)
supabase = Config.supabase_

@auth_page_bp.route("/auth/signup/", methods=['GET','POST'])
def signup():
    if session:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['reenter_password']

            if (password==confirm_password):
                user = supabase.auth.sign_up({"email": email,"password": password})
                if user:
                    return redirect(url_for('auth_page.email_verificatation'))
                # add logic for condition if user is not created

            else:
                # flag error saying both password are not same
                pass
        
        return redirect(url_for('dashboard_page.consumer_dashboard'))
    else:
        return render_template("/auth/signup_page.html")


@auth_page_bp.route("/auth/signin/", methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = supabase.auth.sign_in_with_password({"email": email,"password": password})
        if user:
            session['email'] = email

            return redirect(url_for('dashboard_page.consumer_dashboard'))
            
    return render_template("/auth/signin_page.html")

@auth_page_bp.route("/auth/email_verify/")
def email_verificatation():
    if session:
        return "Email verification has been sent to you."
    else:
        return redirect(url_for('error_page.error_404'))

@auth_page_bp.route("/auth/password_recovery/")
def password_recovery():
    pass

@auth_page_bp.route("/auth/logout/")
def logout():
    if session:
        session.clear()
    else:
        return redirect(url_for('auth_page.signin'))
    return "Session logout"
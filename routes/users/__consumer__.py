from flask import Blueprint, redirect, render_template, request, url_for,session
from __config__ import Config


# Create a blueprint for the home routes
consumer_page_bp = Blueprint("consumer_page", __name__)
supabase = Config.supabase_


@consumer_page_bp.route("/user/consumer/dashboard")
def consumer_dashboard():
    access = session['user-type'] =="Consumer"
    if access:
        return render_template('/consumer/consumer_dashboard_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    elif not access:
        return redirect(url_for('error_page.error_403'))
    else:
        return "Some error occured."





@consumer_page_bp.route("/user/consumer/history")
def consumer_history():
    access = session['user-type'] =="Consumer"

    if access:
        return render_template('/consumer/consumer_history_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    elif not access:
        return redirect(url_for('error_page.error_403'))
    else:
        return "Some error occured."





@consumer_page_bp.route("/user/consumer/monitor")
def consumer_monitor():
    access = session['user-type'] =="Consumer"
    if access:
        return render_template('/consumer/consumer_monitor_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    elif not access:
        return redirect(url_for('error_page.error_403'))
    else:
        return "Some error occured."





@consumer_page_bp.route("/user/consumer/settings")
def consumer_settings():
    access = session['user-type'] =="Consumer"
    if access:
        return render_template('/consumer/consumer_settings_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))
    elif not access:
        return redirect(url_for('error_page.error_403'))
    else:
        return "Some error occured."




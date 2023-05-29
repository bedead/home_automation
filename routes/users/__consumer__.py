from flask import Blueprint, redirect, render_template, request, url_for,session
from __config__ import Config


# Create a blueprint for the home routes
consumer_page_bp = Blueprint("consumer_page", __name__)
supabase = Config.supabase_


@consumer_page_bp.route("/user/consumer/dashboard")
def consumer_dashboard():
    if session['user-type'] =="Consumer":
        

        return render_template('/consumer/consumer_dashboard_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))





@consumer_page_bp.route("/user/consumer/history")
def consumer_history():
    if session['user-type'] =="Consumer":

        return render_template('/consumer/consumer_history_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))





@consumer_page_bp.route("/user/consumer/monitor")
def consumer_monitor():
    if session['user-type'] =="Consumer":

        return render_template('/consumer/consumer_monitor_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))





@consumer_page_bp.route("/user/consumer/settings")
def consumer_settings():
    if session['user-type'] =="Consumer":
        return render_template('/consumer/consumer_settings_page.html')
    elif not session:
        return redirect(url_for('auth_page.signin'))




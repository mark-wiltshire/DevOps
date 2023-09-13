"""
wep_app.py

DEPRECATED - was used for original Local Jenkins run NOT in Docker Version

Provides Web access to the project

uses the db_connector.py module for the database access
registers an atexit method to ensure database connections are closed when program closes

required arguments
db_host
db_port
db_user
db_password
"""
import atexit
import os
import signal
import argparse

from flask import Flask, render_template

import globals
import db_connector

# parse arguments
parser = argparse.ArgumentParser(description="Run our Web App")
parser.add_argument("db_host", type=str, help="the DB host")
parser.add_argument("db_port", type=int, help="the DB port")
parser.add_argument("db_user", type=str, help="the DB username")
parser.add_argument("db_password", type=str, help="the DB password")
args = parser.parse_args()

# Open and initialise DB Connection
db_connector.get_connection(args.db_host, args.db_port, args.db_user, args.db_password)
db_connector.init()

# initialise globals
globals.init()

# setup app
app = Flask(__name__)


def close_up():
    """
    Will perform clean up and close database connections when the program exits.

    :return: none
    """
    db_connector.close_connection()
    print("DB Connection Closed")


# Register the function to be called on exit
atexit.register(close_up)


# accessed via <HOST>:<PORT>/users/get_user_data/
@app.route('/users/get_user_data/<user_id>')
def hello_user(user_id):
    """
    hello_user - will read the user_id from the URL and read the user_name from the database

    :param user_id:
    :return: HTML to display on the web page
    """
    user_name = db_connector.read_user(user_id)
    if user_name == "":
        return f'<h1 id="error">no such user: {user_id}</h1>', 500  # status code
    else:
        return f'<h1 id="user">{user_name}</h1>', 200  # status code


@app.route('/stop_server')
def stop_server():
    """
    Stop the server

    :return: String
    """
    print(f"Stopping the server")
    try:
        # os.kill(os.getpid(), signal.CTRL_C_EVENT)
        os.kill(os.getpid(), signal.SIGKILL)
        return 'Server stopped'
    except Exception as e:
        print(f"Exception when stopping server [{e}]")
        return 'Server NOT stopped'


@app.errorhandler(404)
def page_not_found(e):
    print(f"Page not found [{e}]")
    return render_template('404.html'), 404


# host is pointing at local machine address
# debug is used for more detailed logs + hot swaping
# the desired port - feel free to change
app.run(host='127.0.0.1', debug=True, port=5001)

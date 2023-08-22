"""
wep_app.py

Provides Web access to the project

uses the db_connector.py module for the database access
registers an atexit method to ensure database connections are closed when program closes

"""
import atexit
import os
import signal

from flask import Flask

import db_connector

# import os

# looking for environment variable - TODO remove
# print(os.environ)

app = Flask(__name__)

# initialise DB Connection
db_connector.get_connection()
print("DB Connection Opened")

db_connector.init()
print("DB initialised")


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


# host is pointing at local machine address
# debug is used for more detailed logs + hot swaping
# the desired port - feel free to change
app.run(host='127.0.0.1', debug=True, port=5001)

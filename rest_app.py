"""
rest_app.py

Provides REST API for the project

uses the db_connector.py module for the database access
registers an atexit method to ensure database connections are closed when program closes

Will ask user for user_id and user_name for testing
if user_id is already in use in the DB - it will try with random ID till it works.

when adding user - if user_id is already used will keep trying with new random ID until user is added
will return new user_id

optional arguments
db_host
db_port
db_user
db_pass - could be secret path or password

Gets
api_host
api_port
api_path - from globals - which are read from DB config table
"""

import atexit
import os
import signal
import argparse
from random import randint

from flask import Flask, request

import globals
import db_connector

# parse arguments
parser = argparse.ArgumentParser(description="Run our Rest API")
parser.add_argument("--db_host", type=str, help="the DB host")
parser.add_argument("--db_port", type=int, help="the DB port")
parser.add_argument("--db_user", type=str, help="the DB username")
parser.add_argument("--db_pass", type=str, help="the DB password")
args = parser.parse_args()

# check if db_pass is passed as secret file
db_pass = args.db_pass
isFile = os.path.exists(db_pass)
print(f"password isFile [{isFile}]")
# as this is where it will be stored in a container docker secret - overwrite it with password in the file
if isFile:
    try:
        with open(db_pass, 'r') as file:
            db_pass = file.read().strip()
    except Exception as e:
        print(e)
        raise Exception("No Password Secret File Found")

# Open and initialise DB Connection
print(f"db_host [{args.db_host}]")
print(f"db_port [{args.db_port}]")
print(f"db_user [{args.db_user}]")
print(f"db_pass [{db_pass}]")
db_connector.get_connection(args.db_host, args.db_port, args.db_user, db_pass)
db_connector.init()

# initialise globals
globals.init()

# setup app
app = Flask(__name__)

# api gateway is host, port and path - need to split up
api_gateway = str(globals.global_dict[globals.KEY_API_GATEWAY])
# strip off quotes and brackets
api_gateway = api_gateway[2:-2]
print(f"API Gateway [{api_gateway}]")
# split string
api_host = api_gateway.split(':', 1)[0]
print(f"API URL [{api_host}]")
api_port = int(api_gateway.split(':', 1)[1].split("/", 1)[0])
print(f"API Port [{api_port}]")
api_path = api_gateway.split(':', 1)[1].split("/", 1)[1]
print(f"API Path [{api_path}]")


def get_random_user_id():
    """
    Looksup random integer
    :return: int
    """
    return randint(1, 10000)


def close_up():
    """
    Will perform clean up and close database connections when the program exits.

    :return: none
    """
    db_connector.close_connection()
    print("DB Connection Closed")


# Register the function to be called on exit
atexit.register(close_up)


# supported methods
@app.route('/' + api_path + '/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user(user_id):
    """
    Defines the methods for the REST API
    - GET - read user_name from database for the passed user_id
    - POST - will save user_name for user_id
            if user_id already used it will find a new random one to use and pass this new user_id back
    - DELETE - will delete from database this user_id
    - PUT - will update user_name for this user_id in the database
    :param user_id:
    :return: JSON and status
    """
    if request.method == 'GET':
        """
        GET data from user_id
        
        :return: 200 with user_name if found - 500 with status error if not found
        """
        user_name = db_connector.read_user(user_id)
        if user_name == "":
            return {'status': 'error', 'reason': 'no such id'}, 500  # status code
        else:
            return {'status': 'ok', 'user_name': user_name}, 200  # status code

    elif request.method == 'POST':
        """
        POST - save new user_id and user_name
        
        will try to add user - if user_id already exists will generate a new random id and pass this back
        :return: 200 - user_added - 200 user_added_with_new_id - 500 error
        """
        # getting the json data payload from request
        request_data = request.json
        # treating request_data as a dictionary to get a specific value from key
        user_name = request_data.get('user_name')
        if db_connector.add_user(user_id, user_name):
            return {'status': 'ok', 'user_added': user_name, }, 200  # status code
        else:
            orig_user_id = user_id
            # Try and Keep Trying with Random user_id - till it gets added.
            user_added = False
            while not user_added:
                try:
                    user_id = get_random_user_id()
                    print(f"WARNING User id [{orig_user_id} Already exists trying new [{user_id}]")
                    if db_connector.add_user(user_id, user_name):
                        user_added = True
                    else:
                        continue
                except Exception as e:
                    print(f'Exception {e}')
                    # if for whatever reason we do get an exception - return 500 status
                    return {'status': 'error', 'reason': 'id already exists'}, 500  # status code
            return {'status': 'ok', 'user_added_with_new_id': user_id}, 200  # status code
    elif request.method == 'PUT':
        """
        PUT - update data
        
        will update user_name for a user_id
        :return: 200 - user_updated - 500 no such id
        """
        # getting the json data payload from request
        request_data = request.json
        # treating request_data as a dictionary to get a specific value from key
        user_name = request_data.get('user_name')
        if db_connector.update_user(user_id, user_name):
            return {'status': 'ok', 'user_updated': user_name, }, 200  # status code
        else:
            return {'status': 'error', 'reason': 'no such id'}, 500  # status code
    elif request.method == 'DELETE':
        """
        DELETE - delete data

        will delete data for a user_id
        :return: 200 - user_deleted - 500 no such id
        """
        if db_connector.delete_user(user_id):
            return {'status': 'ok', 'user_deleted': user_id, }, 200  # status code
        else:
            return {'status': 'error', 'reason': 'no such id'}, 500  # status code


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
    return {'status': 'error', 'reason': 'route not found'}, 404  # status code


app.run(host=api_host, debug=True, port=api_port)

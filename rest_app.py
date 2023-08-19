"""
rest_app.py

Provides REST API for the project

uses the db_connector.py module for the database access
registers an atexit method to ensure database connections are closed when program closes

Gets
api_host
api_port
api_path - from globals - which are read from DB config table
"""

import atexit

from flask import Flask, request

import db_connector
import globals

app = Flask(__name__)

# initialise DB Connection
db_connector.get_connection()
print("DB Connection Opened")

db_connector.init()
print("DB initialised")

# initialise globals
globals.init()
# api gateway is host, port and path - need to split up
api_gateway = str(globals.global_dict[globals.KEY_API_GATEWAY])
#strip off quotes and brackets
api_gateway = api_gateway[2:-2]
print(f"API Gateway [{api_gateway}]")
#split string
api_host = api_gateway.split(':', 1)[0]
print(f"API URL [{api_host}]")
api_port = api_gateway.split(':', 1)[1].split("/",1)[0]
print(f"API Port [{api_port}]")
api_path = api_gateway.split(':', 1)[1].split("/",1)[1]
print(f"API Path [{api_path}]")

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
@app.route('/'+api_path+'/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user(user_id):
    """
    Defines the methods for the REST API
    - GET - read user_name from database for the passed user_id
    - POST - will save user_name for user_id
    - DELETE - will delete from database this user_id
    - PUT - will update user_name for this user_id in the database
    :param user_id:
    :return: JSON and status
    """
    if request.method == 'GET':
        user_name = db_connector.read_user(user_id)
        if user_name == "":
            return {'status': 'error', 'reason': 'no such id'}, 500  # status code
        else:
            return {'status': 'ok', 'user_name': user_name}, 200  # status code

    elif request.method == 'POST':
        # getting the json data payload from request
        request_data = request.json
        # treating request_data as a dictionary to get a specific value from key
        user_name = request_data.get('user_name')
        if db_connector.add_user(user_id, user_name):
            return {'status': 'ok', 'user_added': user_name, }, 200  # status code
        else:
            return {'status': 'error', 'reason': 'id already exists'}, 500  # status code
    elif request.method == 'PUT':
        # getting the json data payload from request
        request_data = request.json
        # treating request_data as a dictionary to get a specific value from key
        user_name = request_data.get('user_name')
        if db_connector.update_user(user_id, user_name):
            return {'status': 'ok', 'user_updated': user_name, }, 200  # status code
        else:
            return {'status': 'error', 'reason': 'no such id'}, 500  # status code
    elif request.method == 'DELETE':
        if db_connector.delete_user(user_id):
            return {'status': 'ok', 'user_deleted': user_id, }, 200  # status code
        else:
            return {'status': 'error', 'reason': 'no such id'}, 500  # status code


app.run(host=api_host, debug=True, port=api_port)

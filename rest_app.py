# rest_app.py
# Provides REST API for the project

from flask import Flask, request
import atexit
import db_connector

app = Flask(__name__)

#initialise DB Connection
db_connector.get_connection()
print("DB Connection Opened")

def close_up():
    db_connector.close_connection()
    print("DB Connection Closed")
#Register the function to be called on exit
atexit.register(close_up)

# supported methods
@app.route('/users/<user_id>', methods=['GET', 'POST', 'DELETE', 'PUT'])
def user(user_id):
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
        if (db_connector.add_user(user_id,user_name)):
            return {'status': 'ok', 'user_added': user_name,}, 200  # status code
        else:
            return {'status': 'error', 'reason': 'id already exists'}, 500  # status code
  # todo elif for put and delete


app.run(host='127.0.0.1', debug=True, port=5000)
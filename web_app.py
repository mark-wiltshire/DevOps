import atexit

from flask import Flask

import db_connector

app = Flask(__name__)

# initialise DB Connection
db_connector.get_connection()
print("DB Connection Opened")

db_connector.init()
print("DB initialised")


def close_up():
    db_connector.close_connection()
    print("DB Connection Closed")


# Register the function to be called on exit
atexit.register(close_up)


# accessed via <HOST>:<PORT>/users/get_user_data/
@app.route('/users/get_user_data/<user_id>')
def hello_user(user_id):
    user_name = db_connector.read_user(user_id)
    if user_name == "":
        return f'<h1 id="error">no such user: {user_id}</h1>', 500  # status code
    else:
        return f'<h1 id="user">{user_name}</h1>', 200  # status code


# host is pointing at local machine address
# debug is used for more detailed logs + hot swaping
# the desired port - feel free to change
app.run(host='127.0.0.1', debug=True, port=5001)

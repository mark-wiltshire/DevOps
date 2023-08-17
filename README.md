# Global Dev Experts - DevOps - Project First part
### First Part Project for DevOps Course

Mark Wiltshire

Contains all code for PyCharm Project

PyCharm project requirements
* pip install flask
* pip install requests
* pip install pymysql
* pip install cryptography
* pip install selenium

Uses freesqldatabase.com for the MySQL Server

Run res_app.py to test REST API
Utilises the db_connectory.py
On Mac used https://apps.apple.com/gb/app/postcat-rest-api-testing/id1662268013?mt=12 to test
Using MySQL to check data stored in DB
* GET - http://127.0.0.1:5000/users/<user_id> will return user_name
* POST - http://127.0.0.1:5000/users/<user_id> with user_name payload - will set user_name
* PUT - http://127.0.0.1:5000/users/<user_id> with user_name payload - will update user_name
* DELETE - http://127.0.0.1:5000/users/<user_id>  - will delete entry

Run web_app.py to test Web Interface
Utilises the db_connectory.py
* point browser to http://127.0.0.1:5001/users/get_user_data/1 

Running frontend_testing.py
This will test web interface 
* you must edit file for location of: 
* A - chrome executable 
* B - chromedriver 
* web_app.py must be running

Running backend_testing.py
This will test REST API and Database Testing
* rest_app.py must be running

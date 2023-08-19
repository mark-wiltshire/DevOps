# Global Dev Experts - DevOps - Project First part
### First Part Project for DevOps Course

Mark Wiltshire

Contains all code for PyCharm Project

PyCharm project requirements
* pip install flask
* pip install requests
* pip install pymysql (want to replace with mysql to support prepared statements)
* pip install cryptography
* pip install selenium

Uses freesqldatabase.com for the MySQL Server connected to in the db_connector.py

Run res_app.py to test REST API
* Utilises the db_connector.py and globals.py
* NOW gets data from Config DB for host, port and path (Stored in globals.py)
* On Mac used App tool - PostCat to test https://apps.apple.com/gb/app/postcat-rest-api-testing/id1662268013?mt=12
* Using MySQL direct to database to check data stored in DB:
* GET - http://127.0.0.1:5000/users/<user_id> will return user_name
* POST - http://127.0.0.1:5000/users/<user_id> with user_name payload - will set user_name
* PUT - http://127.0.0.1:5000/users/<user_id> with user_name payload - will update user_name
* DELETE - http://127.0.0.1:5000/users/<user_id>  - will delete entry

Run web_app.py to test Web Interface
Utilises the db_connector.py and globals.py
* point browser to http://127.0.0.1:5001/users/get_user_data/1 

Running frontend_testing.py - This will test Web interface 
* web_app.py must be running
* you must edit location of: 
* A - chrome executable 
* B - chromedriver 
* Clean's test data when completed

Running backend_testing.py - This will test REST API and Database Testing
* rest_app.py must be running
Clean's test data when completed

Running combined_testing.py - This will test BOTH Web and Rest API
* BOTH web_app.py AND rest_app.py must be running
* Asks user for number (which it will validate) and name (can be any string)
* Will then used this for test data 
* Clean's test data when completed


Extras
- PyDoc - DONE
- Prepared Statements MySQL - pymysql doesn't support - had issues installing mysql
- DATETIME - DONE - changed DB table
- config table in DB - DONE - Reads into dictionary in new globals.py file

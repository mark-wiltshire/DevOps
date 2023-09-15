# Global Dev Experts - DevOps - Project First part

### First Part Project for DevOps Course

Mark Wiltshire
Contains all code for PyCharm Project for the Global Dev Experts - DevOps course

## Part 3 - Docker

1. NEW Jenkins build file  - will checkout, test, build & Push Docker Image and Test on Docker

Notes
- added curl to docker alpine image so docker-compose healthcheck will work
- You can see healthcheck results using command - docker inspect --format "{{json .State.Health }}" <container name>
- added Jenkins variable base_version - to tag hub.docker.com images with versioning
- COULD expand this to use git tags
- 


New Files
- Jenkins_Docker.Jenkinsfile -
- Dockerfile - to run the docker container running the rest_app.py
- requirements.txt - contains python requirements for rest_app.py
- docker-compose.yaml - docker compose to run the rest_app.py - see https://docs.docker.com/compose/reference/

Extras - 

a. Run MYSQL as another container - using compose - and change your rest_app code to use it - instead of remote DB

No Longer used files (left here for learning / running previous options)
- web_app.py
- frontend_testing.py
- combined_testing.py

## Part 2

### Creating CI Pipeline for a Python Project

Completed Part 2 of project with all Extras

Now have 2 build files
1. Jenkinsfile.Jenkinsfile - which will checkout, runs apps and tests build in Part 1
2. Jenkinsfile_wp.Jenkinsfile - which will checkout, ask for parameter and test based on parameter

Additional files this project:
clean_environment.py - will stop web_app.py and rest_app.py servers in testing
/templates/404.html - 404 error page

Extras
1. Send email on failure - DONE
2. Parameterized Build - DONE
3. sys.argvs - DONE
4. Route Error Handling - DONE


## Part 1

### Building Python Frontend and Backend Stack

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

globals.py

* contains global STATICS and variables - read from config DB in a dictionary

Extras

1. PyDoc - DONE
2. Prepared Statements MySQL - pymysql doesn't support - had issues installing mysql
   I have added prepared statements - but this states pymysql doesn't fully support it.
   https://stackoverflow.com/questions/65638489/prepared-statement-pymysql-who-is-correct
3. DATETIME - DONE - changed DB table
4. config table in DB - DONE - Reads into dictionary in new globals.py file
5. ID already taken - use new ID - DONE
6. PyPika - Not Done Yet

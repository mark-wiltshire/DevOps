"""
Will stop both the REST API and the WEB APP

"""
import requests

try:
    print(f"Stopping REST API")
    res = requests.get('http://127.0.0.1:5000/stop_server')
except requests.exceptions.RequestException as e:
    print(f"RequestException {e}")
    test = e.args[0].args[0]
    if "Connection aborted" in e.args[0].args[0]:
        print(f"STOP SERVER WORKED")
    else:
        print(f"STOP SERVER Server wasn't running")

try:
    print(f"Stopping WEB API")
    res = requests.get('http://127.0.0.1:5001/stop_server')
except requests.exceptions.RequestException as e:
    print(f"RequestException {e}")
    test = e.args[0].args[0]
    if "Connection aborted" in e.args[0].args[0]:
        print(f"STOP SERVER WORKED")
    else:
        print(f"STOP SERVER Server wasn't running")

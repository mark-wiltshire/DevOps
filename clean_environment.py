"""
Will stop both the REST API and the WEB APP

"""
from http.client import RemoteDisconnected

import requests

try:
    print(f"Stopping REST API")
    res = requests.get('http://127.0.0.1:5000/stop_server')
    if res.ok:
        print(f"RESPONSE {res.text}")
# except (ConnectionRefusedError, NewConnectionError, MaxRetryError, ConnectionError) as e:
except OSError as e:
    print(f"STOP SERVER Server wasn't running")
    # This means server wasn't running - i.e. I we should do nothing
except RemoteDisconnected as e:
    # As server would stop exactly before response returned we would expect this on success
    print(f"STOP SERVER WORKED")

try:
    print(f"Stopping WEB API")
    res = requests.get('http://127.0.0.1:5001/stop_server')
    if res.ok:
        print(f"RESPONSE {res.text}")
# except (ConnectionRefusedError, NewConnectionError, MaxRetryError, ConnectionError) as e:
except OSError as e:
    print(f"STOP SERVER Server wasn't running")
    # This means server wasn't running - i.e. I we should do nothing
except RemoteDisconnected as e:
    # As server would stop exactly before response returned we would expect this on success
    print(f"STOP SERVER WORKED")

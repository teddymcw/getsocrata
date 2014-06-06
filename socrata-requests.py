import json
import requests

"""
Follow the pattern in 'auth' below when building the get request.  
That means a dict with 2 key-value pairs, one each for username and password.
"""

empty_credentials = { "username" : "", "password" : "" }

with open('oauth.auth', 'r') as f:
    credentials = json.load(f)

#credentials = empty_credentials

print credentials
r = requests.get('https://data.sfgov.org/resource/g8m3-pdis.json', X-App-Token=(credentials['username']) )

print r.status_code
print r.headers['content-type']
print r.encoding
print r.text
print r.json()

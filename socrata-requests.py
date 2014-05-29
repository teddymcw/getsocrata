import json
import requests

"""
Follow the pattern in 'auth' below when building the get request.  
That means a dict with 2 key-value pairs, one each for username and password.
"""
with open('oauth.auth', 'r') as f:
    credentials = json.load(f)

print credentials
r = requests.get('https://api.github.com/user', auth=(credentials['username'], credentials['password']))

print r.status_code
print r.headers['content-type']
print r.encoding
print r.text
print r.json()

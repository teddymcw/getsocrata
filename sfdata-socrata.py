"""

Retrieve data from sfgov's API with requests.

"""

import json
import requests

oauth_filename = 'oauth.auth'

target_url = 'https://data.sfgov.org/resource/g8m3-pdis.json'

def generate_output_file(filename="unspecified_project"):
    """
    Generate a file using provided arguments and a time
    """
    return "out.dat"

output_filename = generate_output_file()

empty_credentials = { "username" : "", "password" : "" }

with open(oauth_filename, 'r') as f:
    credentials = json.load(f)

#credentials = empty_credentials

socrata_headers = { 'X-App-Token' : credentials['username'] }
r = requests.get(url=target_url, headers=socrata_headers)

print r.status_code
print r.headers['content-type']
print r.encoding
#print r.text

with open(output_filename, 'w') as f:
    for chunk in r.iter_content(1024):
        f.write( chunk )

#print r.json()

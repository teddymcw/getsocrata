"""

Retrieve data from sfgov's API with requests.

Run with the -h argument for help. All arguments must be included.

"""

import json
import requests
import argparse

parser = argparse.ArgumentParser(description='Assign a target URL and an output project or filename.')
parser.add_argument('--url', type=str, help='source URL')
parser.add_argument('--outfile', type=str, help='name of output file')
parser.add_argument('--auth', type=str, help='auth string')

# use args.url, args.auth, and args.outfile
args = parser.parse_args()

socrata_headers = { 'X-App-Token' : args.auth }
r = requests.get(url=args.url, headers=socrata_headers)

print r.status_code
print r.headers['content-type']
print r.encoding
#print r.text

with open(args.outfile, 'w') as f:
    for chunk in r.iter_content(1024):
        f.write( chunk )

#print r.json()

"""

Run with the -h argument for help. All arguments must be included.

This module may be run from the command line or may be imported into a larger project.

If used in a larger project, use the format:

    import getsocrata
    getsocrata.get_socrata_data(user_app_key, source_url, target_output_filename)

Retrieve and record a file from a socrata API.

This specific setup has been tested on SFgov's Socrata API.

This uses the deprecated authentication format with no callback URL. Socrata may 
discontinue this request type in the future in favor of a callback URL method.

"""

import json
import requests
import argparse


def get_socrata_data(user_auth, source_url, target_file):
    """
    If used in a larger project, use the format:

        import getsocrata
        getsocrata.get_socrata_data(user_app_key, source_url, target_output_filename)

    Retrieve and record a file from a socrata API.

    This specific setup has been tested on SFgov's Socrata API.

    This uses the deprecated authentication format with no callback URL. Socrata may 
    discontinue this request type in the future in favor of a callback URL method.
    """

    socrata_headers = { 'X-App-Token' : user_auth }
    
    r = requests.get(url=source_url, headers=socrata_headers)
   
    # Keep this here for the time being.
    if str(r.status_code) != '200':
        print "HTTP Request Failed!"
        exit()

    # This will raise an exception if the response is not 200/ok or the json decoding otherwise fails.
    # r.json() will return a list of dictionaries. So, in order to join them, we just join the lists.
    # example: full_document.extend(r.json()) where full_document is initiated from the first list retrieved.
    # print r.json()

    with open(target_file, 'r+') as f:
        for chunk in r.iter_content(1024):
            f.write( chunk )

    # return r.json()

if __name__ == '__main__':
    """
    Provide command line options for running this function outside of python.
    """

    parser = argparse.ArgumentParser(description='Assign a target URL and an output project or filename.')
    parser.add_argument('--url', type=str, help='source URL')
    parser.add_argument('--outfile', type=str, help='name of output file')
    parser.add_argument('--auth', type=str, help='auth string')
    
    # use args.url, args.auth, and args.outfile
    args = parser.parse_args()
    
    get_socrata_data(args.auth, args.url, args.outfile) 


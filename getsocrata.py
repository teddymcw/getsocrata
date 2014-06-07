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
    
    with open(target_file, 'w') as f:
        for chunk in r.iter_content(1024):
            f.write( chunk )


if __name__ == __main__:

    parser = argparse.ArgumentParser(description='Assign a target URL and an output project or filename.')
    parser.add_argument('--url', type=str, help='source URL')
    parser.add_argument('--outfile', type=str, help='name of output file')
    parser.add_argument('--auth', type=str, help='auth string')
    
    # use args.url, args.auth, and args.outfile
    args = parser.parse_args()
    
    get_socrata_data(args.auth, args.url, args.outfile) 


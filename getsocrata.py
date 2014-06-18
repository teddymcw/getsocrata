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

    # r.json() will return a list of dictionaries. So, in order to join them, we just join the lists.
    # example: full_document.extend(r.json()) where full_document is initiated from the first list retrieved.
    # print r.json()
"""

import json
import requests
import argparse
from ConfigParser import SafeConfigParser
import sys


def get_socrata_data(user_auth, source_url):
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
   
    # Keep this here for now.
    if str(r.status_code) != '200':
        print "HTTP Request Failed!"
        exit()

    return r.json()


def write_to_file(json_ready_data, target_file, mode="a+"):


    with open(target_file, mode) as f:
        json.dump(json_ready_data, f)

def retrieve_config(config_filename="getsocrata.config"):
    """Read and return url, output file, and pagesize from a configuration file.
    
    """

    config = SafeConfigParser()
    config.read(config_filename)

    try:
        url = config.get('getsocrata', 'url')
    except NoSectionError:
        return "no url specified in config file"
    except:
        print( "Unexpected Error:", sys.exc_info()[0])

    try:
        config.get('getsocrata', 'outfile')


    
    print(config.get('getsocrata', 'pagesize'))

    


    url = "hello"
    outfile = "hello"
    pagesize = "hello"

    return (url, outfile, pagesize)



if __name__ == '__main__':
    """Provide command line options for running this function outside of python.
    
    """

    parser = argparse.ArgumentParser(description='Assign a target URL and an output project or filename.')
    parser.add_argument('--url', type=str, help='source URL')
    parser.add_argument('--outfile', type=str, help='name of output file')
    parser.add_argument('--auth', type=str, help='auth string')
    parser.add_argument('--pagesize', type=int, help='# of records per request')
    
    # use args.url, args.auth, args.pagesize, and args.outfile
    args = parser.parse_args()
    
    complete_data_list = []
    page_offset = 0
    next_page = True # This will be used as a list in the while loop.

    while next_page != []:

        # build the next URL of pagesize records
        next_url = args.url + "?$limit=" + str(args.pagesize) + "&$offset=" + str(page_offset)
        print next_url
        next_page = get_socrata_data(args.auth, next_url)
        complete_data_list.extend(next_page)
        page_offset += args.pagesize
    
    write_to_file(complete_data_list, args.outfile)

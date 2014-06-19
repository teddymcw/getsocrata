"""

Run with the -h argument for help. All arguments must be included.

This module may be run from the command line or may be imported into a larger project.

Retrieve and record a file from a socrata API.

This specific setup has been tested on SFgov's Socrata API.

This uses the deprecated authentication format with no callback URL. Socrata may 
discontinue this request type in the future in favor of a callback URL method.

"""

import json
import requests
import argparse
import ConfigParser  # Exceptions are used, import the whole thing!
import sys
import os
import traceback


def get_socrata_data(user_auth, source_url):
    """
    If used in a larger project, use the format:

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


def retrieve_config(config_filename="simple.config", section="getsocrata"):
    """Read and return configuration values from a configuration file.
    
    """

    config = ConfigParser.SafeConfigParser()
    config.read(config_filename)

    config_dict = {}

    # Iterate over a list of all the options provided in a section.
    for arg_key in config.options(section):
        try:
            config_dict[arg_key] = config.get(section, arg_key)
        except:
            print( "Unexpected Error:", sys.exc_info())
            raise

    return config_dict


class MissingArgumentException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


if __name__ == '__main__':
    """Provide command line options for running this function outside of python.
    
    """

    parser = argparse.ArgumentParser(description='Assign a target URL and an output project or filename.')
    parser.add_argument('--url', type=str, help='source URL')
    parser.add_argument('--outfile', type=str, help='name of output file')
    parser.add_argument('--auth', type=str, help='auth string')
    parser.add_argument('--pagesize', type=int, help='# of records per request')
    parser.add_argument('--config', type=str, help='specify a configuration file')
    
    # use args.url, args.auth, args.pagesize, and args.outfile
    args = parser.parse_args()

    # Set runtime options here:
    # retrieve dict of runtime options from a configuration file if one is specified.
    if args.config != None:
        getsocrata_options = retrieve_config(args.config)
    else:
        getsocrata_options = {}

    # Explicitly define argparse options and override configuration file settings.
    if args.url != None:
        getsocrata_options['url'] = args.url
    if args.outfile != None:
        getsocrata_options['output_file'] = args.outfile
    if args.auth != None:
        getsocrata_options['auth'] = args.auth
    if args.pagesize != None:
        getsocrata_options['pagesize'] = args.pagesize

    # Rudimentary error checking:
    if 'url' not in getsocrata_options:
        raise MissingArgumentException("No URL specified!")
    if 'output_file' not in getsocrata_options:
        raise MissingArgumentException("No output_file specified!")
    if 'auth' not in getsocrata_options:
        raise MissingArgumentException("No auth key specified!")
    if 'pagesize' not in getsocrata_options:
        raise MissingArgumentException("No pagesize specified!")

    complete_data_list = []
    page_offset = 0  # Start at the beginning, this could be an option.
    next_page = None   # Utilized in the while loop below

    while next_page != []:

        # consider replacing this with urlparse
        # build the next URL of pagesize records
        next_url = getsocrata_options['url'] + "?$limit=" + str(getsocrata_options['pagesize']) + "&$offset=" + str(page_offset)
        print next_url
        next_page = get_socrata_data(getsocrata_options['auth'], next_url)
        
        with open(getsocrata_options['output_file'], "a+") as f:
            for each in next_page:
                f.write(json.dumps(each) + os.linesep)
        
        page_offset += int(getsocrata_options['pagesize'])
    


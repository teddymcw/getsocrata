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

    arg_keys = config.options(section)
    arg_values = []

    config_dict = {}

    for arg_key in arg_keys:
        try:
            config_dict[arg_key] = config.get(section, arg_key)
        except ConfigParser.NoOptionError as err:
            config_dict[arg_key] = None
            print(err, "not specified in config file")
        except:
            print( "Unexpected Error:", sys.exc_info()[0])

    return config_dict


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
    if getsocrata_options['url'] == None:
        raise error("No URL specified!")
    if getsocrata_options['output_file'] == None:
        raise error("No output_file specified!")
    if getsocrata_options['auth'] == None:
        raise error("No auth key specified!")
    if getsocrata_options['pagesize'] == None:
        raise error("No pagesize specified!")

    complete_data_list = []
    page_offset = 0
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
    


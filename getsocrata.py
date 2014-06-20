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
import datetime
import traceback


http_request_history = {}

def get_socrata_data(user_auth, source_url):
    """
    Retrieve and turn a list of json objects (records) from a socrata API endpoint.

    This specific setup has been tested on SFgov's Socrata API.

    This uses the deprecated authentication format with no callback URL. Socrata may 
    discontinue this request type in the future in favor of a callback URL method.
    """

    socrata_headers = { 'X-App-Token' : user_auth }
    
    tries = 3 # try at least 3 times 
    while tries > 0:
        try:
            r = requests.get(url=source_url, headers=socrata_headers)
        except Exception as e:
            print "Request error:", sys.exc_info()[0]
            trues -= 1
            print "HTTP Request Failed! Retrying", tries, "more times..."
            continue

        http_request_history[source_url] = r.status_code
        if str(r.status_code) == '200':
            return r.json()
        else:
            tries -= 1
            print "HTTP Request Failed! Retrying", tries, "more times..."
            continue

    else:
        return None


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
        except: # This shouldn't happen, if it does refer to ConfigParser docs.
            print( "Unexpected Error:", sys.exc_info())
            raise

    return config_dict


def generate_filename(filename_base='output'):
    """ Use a timestamp and an optional project name to make a unique filename.

    """
    time_string = datetime.datetime.now().strftime("%m%d%Y.%H%M%S")
    return filename_base + "." + time_string + ".json"


class MissingArgumentException(Exception):
    """ Exception class for when a critical argument is not passed before it is needed. 

    """
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
    parser.add_argument('--project', type=str, help='specify a project name for output')
    
    # use args.url, args.auth, args.pagesize, and args.outfile
    args = parser.parse_args()

    # Set runtime options here:
    # retrieve dict of runtime options from a configuration file if one is specified.
    if args.config != None:
        getsocrata_options = retrieve_config(args.config)
    else:
        getsocrata_options = {}

    # Explicitly define argparse options and override configuration file settings.
    # Don't change these if statements, the user should be able to pass an empty string.
    if args.url != None:
        getsocrata_options['url'] = args.url
    if args.auth != None:
        getsocrata_options['auth'] = args.auth
    if args.pagesize != None:
        getsocrata_options['pagesize'] = args.pagesize
    if args.project != None:
        getsocrata_options['project'] = args.project
    if args.outfile != None:
        getsocrata_options['output_file'] = args.outfile
    
    # Rudimentary error checking:
    if 'url' not in getsocrata_options:
        raise MissingArgumentException("No URL specified!")
    if 'auth' not in getsocrata_options:
        raise MissingArgumentException("No auth key specified!")
    if 'pagesize' not in getsocrata_options:
        raise MissingArgumentException("No pagesize specified!")
    if 'output_file' not in getsocrata_options:
        if 'project' in getsocrata_options: # use project to generate filename if it exists
            getsocrata_options['output_file'] = generate_filename(getsocrata_options['project'])
        else:
            getsocrata_options['output_file'] = generate_filename()

    complete_data_list = []
    page_offset = 0  # Start at the beginning, this could be an option.
    next_page = None   # Utilized in the while loop below

    while next_page != []:

        # consider replacing this with urlparse
        # build the next URL of pagesize records
        next_url = getsocrata_options['url'] + "?$limit=" + str(getsocrata_options['pagesize']) + "&$offset=" + str(page_offset)
        print next_url
        next_page = get_socrata_data(getsocrata_options['auth'], next_url)
        page_offset += int(getsocrata_options['pagesize']) # do this after building the URL
        if next_page == None:
            continue # skip if the request fails, use the http_request_history to repeat later
        with open(getsocrata_options['output_file'], "a+") as f:
            for each in next_page:
                f.write(json.dumps(each) + os.linesep)
    
    # Indication of failure to the user:
    for k,v in http_request_history.iteritems():
        if str(v) != "200":
            print "Failed:", k, "Response:", v
    # Log all requests for the user:
    with open(getsocrata_options['output_file']+".log", "w+") as f:
        json.dump(http_request_history, f)
    


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
import ConfigParser  # Exceptions are used, import the whole thing! Open question, will the SafeConfigParser function have access to the ConfigParser exceptions if we use the import format 'from ConfigParser import SafeConfigParser' ????
import sys
import os
import datetime
import urllib
import traceback


http_request_history = {}
getsocrata_options = {}


def get_socrata_data(user_auth, source_url, output_file):
    """
    Retrieve and turn a list of json objects (records) from a socrata API endpoint.

    This specific setup has been tested on SFgov's Socrata API.

    This uses the deprecated authentication format with no callback URL. Socrata may 
    discontinue this request type in the future in favor of a callback URL method.
    """

    socrata_headers = { 'X-App-Token' : user_auth }
    
    tries = 3 # try at least 3 times 
    r = None  # Need r in this scope for while/else statement
    while tries > 0:
        try:
            r = requests.get(url=source_url, headers=socrata_headers)
        except Exception as e:
            tries -= 1
            print "Request error:", sys.exc_info()[0], "trying", tries, "more times."
            continue

        http_request_history[source_url] = r.status_code
        if str(r.status_code) == '200':
            # Write successful attempt to log.
            with open(output_file+".log", "a+") as f:
                f.write(json.dumps({'time of request': datetime.datetime.now().strftime("%m.%d.%Y,%H:%M:%S"), str(source_url) : str(r.status_code)}) + os.linesep)
            return r.json()
        else:
            tries -= 1
            print "HTTP Request Failed! Retrying", tries, "more times..."
            continue
    # In the event that we have a failure, record it into a log file so it can be tracked and continue on.
    else:
        # Some errors do not ever assign a status code, so we'll assign one if r remains 'None'
        if r == None:
            status_code = 0
        else:
            status_code = r.status_code

        print "Failed:", str(source_url), "Response:", str(status_code)
        with open(output_file+".log", "a+") as f:
            f.write(json.dumps({'time of request': datetime.datetime.now().strftime("%m.%d.%Y,%H:%M:%S"), str(source_url) : str(status_code)}) + os.linesep)

        # if we returned [] then we couldn't tell the difference between a failed response and the end of the data stream.
        return None 


def parse_config_file(config_filename):
    """ Load a configuration file into the configuration dict and return it.

    This is really just a controller function for using the generic retrieve_config() function.
    """

    # placeholder - we need to check to make sure the file actually exists before trying to use it!

    getsocrata_options = {}

    getsocrata_options = retrieve_config(config_filename, 'getsocrata')
    getsocrata_options['filters'] = retrieve_config(config_filename, 'getsocrata filters')

    return getsocrata_options


def retrieve_config(config_filename="simple.config", section="getsocrata"):
    """Read and return configuration values from a configuration file.
    
    This is a generic function for moving key-value pairs from a ConfigParser config file into a dictionary.
    """
    config = ConfigParser.SafeConfigParser()
    try:
        config.read(config_filename)
    except: # Catch any unexpected configuration file issues and raise.
        print "Unexpected Error: Configuration file error. Check name and format.", sys.exc_info()
        raise

    config_dict = {}

    # Iterate over a list of all the options provided in a section.
    try:
        for arg_key in config.options(section):
            config_dict[arg_key] = config.get(section, arg_key)
    except ConfigParser.NoSectionError:
        print "Warning: No config section '" + str(section) + "' Returning an empty dictionary for this section."
        return {}

    return config_dict


def generate_filename(filename_base='myproject'):
    """ Use a timestamp and an optional project name to make a unique filename.

    """

    return filename_base + "." + datetime.datetime.now().strftime("%m%d%Y.%H%M%S") + ".json"


class MissingArgumentException(Exception):
    """ Exception class for when a critical argument is not passed before it is needed. 

    """
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def build_url_and_query_string(getsocrata_options):
    """Builds url string from user provided socrata SODA api parameters.

    Question: Can URL QueryStrings be ordered? Does the order matter? Does socrata need the order or respect the order?
    """

    generated_url = ""
    accepted_querystrings = ["$select", "$where", "$order", "$group", "$limit", "$offset"]
    
    #append base URL and begin querystring
    generated_url += getsocrata_options['url'] + "?"

    #socrata filters - use urllib's urlencode to ensure spaces and other special characters are encoded.
    generated_url += urllib.urlencode(getsocrata_options['filters'])#.replace('+','%20')

    #socrata SoQL queries
    for key, value in getsocrata_options.iteritems():
        if key in accepted_querystrings:
            #generated_url += "&"+str(key)+"="+str(value)
            generated_url += "&"+urllib.urlencode([(key, value)]).replace('+','%20')

    return generated_url


def increment_offset_and_record_data_until_empty():
    """ This control loop iteratively pulls data until it runs out
    
    """

    next_page = None   # Utilized in the while loop below
    while next_page != []:

        next_url = build_url_and_query_string(getsocrata_options)
        print next_url

        next_page = get_socrata_data(getsocrata_options['auth'], next_url, getsocrata_options['output_file'])

        # increment the offset regardless of success. "move on"
        getsocrata_options['$offset'] = int(getsocrata_options['$offset']) + int(getsocrata_options['$limit'])

        # skip the write if the request fails, the http_request_history json log file can be used to retry.
        if next_page == None:
            continue
        
        # write one json object per line (contains <$limit> records)
        with open(getsocrata_options['output_file'], "a+") as f:
            for each in next_page:
                f.write(json.dumps(each) + os.linesep)




if __name__ == '__main__':
    """Provide command line options for running this function outside of python.
    
    """

    # The config file can specify any variable used in argparse, but argparse will override SafeConfigParser.
    # However, the config file MUST be passed as an argument in __main__ or it will not be used.
    parser = argparse.ArgumentParser(description='Assign a target URL and an output project or filename.')
    parser.add_argument('--url', type=str, help='source URL')
    parser.add_argument('--outfile', type=str, help='name of output file') # generated from project+timestamp unless specified.
    parser.add_argument('--auth', type=str, help='auth string')
    parser.add_argument('--config', type=str, help='specify a configuration file')
    parser.add_argument('--project', type=str, help='specify a project name for output')
    
    args = parser.parse_args()

    # Warning: you really should specify an args.config if you are using the "if name == '__main__'" code block.
    if args.config != None:
        getsocrata_options = parse_config_file(args.config)
    else:
        print "Warning: Running this module as __main__ generally requires a configuration file."
        pass

    # TAR 062214 - This area should be generalized using args.__dict__ and a loop.
    # (This is the same effect as vars(args)). This will ensure that all argument 
    # objects that are not None override all config options. (With the added effect 
    # of removing the explicit arguments, generalizing the code)
    #
    # Explicitly define argparse options and override configuration file settings.
    # Don't change these if statements, the user should be able to pass an empty string.
    if args.url != None:
        getsocrata_options['url'] = args.url
    if args.auth != None:
        getsocrata_options['auth'] = args.auth
    if args.project != None:
        getsocrata_options['project'] = args.project
    if args.outfile != None:
        getsocrata_options['output_file'] = args.outfile
    

    # Rudimentary error checking:
    # Consider putting this in a function:

    # We can also set defaults here. SoQL has some defaults which should be respected if unspecified by the user.
    if 'url' not in getsocrata_options:
        raise MissingArgumentException("No URL specified!")
    if 'auth' not in getsocrata_options:
        raise MissingArgumentException("No auth key specified!")
    
    # Two defaults in socrata, we must define them to allow __main__ to auto-increment by default.
    if '$offset' not in getsocrata_options:
        getsocrata_options['$offset'] = 0
    if '$limit' not in getsocrata_options:
        getsocrata_options['$limit'] = 1000

    # use project to generate json output filename if one is not specified. Else use a default.
    if 'output_file' not in getsocrata_options:
        if 'project' in getsocrata_options:
            getsocrata_options['output_file'] = generate_filename(getsocrata_options['project'])
        else:
            getsocrata_options['output_file'] = generate_filename() # use default value


    # Control logic for __main__:
    increment_offset_and_record_data_until_empty()
    


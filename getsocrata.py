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
import ConfigParser  # Exceptions are used, import the whole thing!
import sys
import os


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


# Potentially deprecated, was used in main()
def write_to_file(json_ready_data, target_file, mode="a+"):

    with open(target_file, mode) as f:
        json.dump(json_ready_data, f)


def retrieve_config(config_filename="simple.config", section="getsocrata"):
    """Read and return configuration values from a configuration file.
    
    Call in code like this:
    url, outfile, pagesize, auth = retrieve_config(<"optional_configname">)
    """

    config = ConfigParser.SafeConfigParser()
    config.read(config_filename)

    arg_keys = config.options(section)
    arg_values = []

    def retrieve_config_args(section, arg_key):

        arg_value = None
        try:
            arg_value = config.get(section, arg_key)
        except ConfigParser.NoOptionError as err:
            arg_value = None
            print(err, "not specified in config file")
        except:
            print( "Unexpected Error:", sys.exc_info()[0])

        return arg_value


    for arg_key in arg_keys:
        arg_values.append(retrieve_config_args(section, arg_key))

    return dict(zip(arg_keys, arg_values))


if __name__ == '__main__':
    """Provide command line options for running this function outside of python.
    
    """

    parser = argparse.ArgumentParser(description='Assign a target URL and an output project or filename.')
    parser.add_argument('--url', type=str, help='source URL')
    parser.add_argument('--outfile', type=str, help='name of output file')
    parser.add_argument('--auth', type=str, help='auth string')
    parser.add_argument('--pagesize', type=int, help='# of records per request')
    parser.add_argument('--config', type=str, help='specify a configuration file')
    
    getsocrata_options = {} # our runtime options reside here

    # use args.url, args.auth, args.pagesize, and args.outfile
    args = parser.parse_args()

    # retrieve a configuration file if one is specified.
    if args.config != None:
        config_dict = retrieve_config(args.config)
        
    expected_config_options = ['url', 'output_file', 'auth', 'pagesize' ]
    
    for expected_key in expected_config_options:
        if expected_key in config_dict:
            getsocrata_options[expected_key] = config_dict[expected_key]

    # Explicitly define argparse options and override configuration file settings.
    if args.url != None:
        getsocrata_options['url'] = args.url
    if args.outfile != None:
        getsocrata_options['output_file'] = args.outfile
    if args.auth != None:
        getsocrata_options['auth'] = args.auth
    if args.pagesize != None:
        getsocrata_options['pagesize'] = args.pagesize

    complete_data_list = []
    page_offset = 0
    next_page = True # This will be used as a list in the while loop.

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
    
    # superceded by the new approach of appending line separated json serializable objects
    # write_to_file(complete_data_list, outfile)

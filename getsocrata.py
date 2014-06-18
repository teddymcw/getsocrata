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


def retrieve_config(config_filename="simple.config"):
    """Read and return configuration values from a configuration file.
    
    Call in code like this:
    url, outfile, pagesize, auth = retrieve_config(<"optional_configname">)
    """
    section = "getsocrata"
    arg_keys = ["url", "outfile", "pagesize", "auth"]
    arg_values = []

    config = ConfigParser.SafeConfigParser()
    config.read(config_filename)

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

    return tuple(arg_values)



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

    # retrieve a configuration file if one is specified.
    if args.config != None:
        url, outfile, pagesize, auth = retrieve_config(args.config)

    if args.url != None:
        url = args.url
    if args.outfile != None:
        outfile = args.outfile
    if args.auth != None:
        auth = args.auth
    if args.pagesize != None:
        pagesize = args.pagesize

    pagesize = int(pagesize) #explicitly defines integer value

    complete_data_list = []
    page_offset = 0
    next_page = True # This will be used as a list in the while loop.

    while next_page != []:

        # consider replacing this with urlparse
        # build the next URL of pagesize records
        next_url = url + "?$limit=" + str(pagesize) + "&$offset=" + str(page_offset)
        print next_url
        next_page = get_socrata_data(auth, next_url)
        
        with open(outfile, "a+") as f:
            for each in next_page:
                f.write(json.dumps(each) + os.linesep)
        
        page_offset += pagesize
    
    # superceded by the new approach of appending line separated json serializable objects
    # write_to_file(complete_data_list, outfile)

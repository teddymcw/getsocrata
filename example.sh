#!/bin/bash

config="sample.config"

# store app token as a string in a .auth file
# token.sh.auth should include the following:
: '
#!/bin/bash
token="<app token>"
'

source token.sh.auth
python getsocrata.py --token $token --config $config

# unset env variables
unset auth
unset config

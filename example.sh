#!/bin/bash

config="simple.config"

# store authentication as a string in a .auth file
# key.sh.auth should include the following:
: '
#!/bin/bash
auth="<public key>"
'

source key.sh.auth

python getsocrata.py --auth $auth --config $config

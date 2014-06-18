#!/bin/bash

config="simple.config"

# store authentication as a string in a .auth file
source ./sh_auth.auth

python getsocrata.py --auth $auth --config $config

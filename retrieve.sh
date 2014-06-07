#!/bin/bash

url="https://data.sfgov.org/resource/g8m3-pdis.json"
outfile="out.dat"

# store authentication as a string in a .auth file
source ./sh_auth.auth

python sfdata-socrata.py --url $url --outfile $outfile --auth $auth

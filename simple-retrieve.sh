#!/bin/bash

#url="http://data.sfgov.org/resource/7h4w-reyq.json" # SF Job titles by job code
#url="http://data.sfgov.org/resource/7h4w-reyq.json"  # SF Salaries
#url="https://data.sfgov.org/resource/h4ui-ubbu.json" # SF Restaurant Scores
url="https://data.sfgov.org/resource/g8m3-pdis.json" # SF business registrations
outfile="allsfcompanies.json"
pagesize="1000"

# store authentication as a string in a .auth file
source ./sh_auth.auth

python getsocrata.py --url $url --outfile $outfile --auth $auth --pagesize $pagesize

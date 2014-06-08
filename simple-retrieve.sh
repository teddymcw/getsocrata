#!/bin/bash


url="https://data.sfgov.org/resource/h4ui-ubbu.json" # SF Restaurant Scores
#url="https://data.sfgov.org/resource/g8m3-pdis.json" # SF business registrations
outfile="out.dat"
pagesize="1000"

# store authentication as a string in a .auth file
source ./sh_auth.auth

python getsocrata.py --url $url --outfile $outfile --auth $auth --pagesize $pagesize

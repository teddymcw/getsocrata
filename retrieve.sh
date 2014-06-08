#!/bin/bash

# record limit on sfgov.org (socrata) is 1000 records
#url="https://data.sfgov.org/resource/g8m3-pdis.json"

offset=0
limit=1000

# do this wherever the script is run
directory='dat'
mkdir -p $directory

# authentication stored as $auth="<token>" in this source file (*.auth files are in .gitignore)
source ./sh_auth.auth

while true # until we get the right response
do

    url="https://data.sfgov.org/resource/g8m3-pdis.json?\$limit="$limit"&\$offset="$offset
    outfile=$directory"/out"$offset"."`expr $offset + $limit`".dat"
    
    python getsocrata.py --url $url --outfile $outfile --auth $auth
    
    offset=`expr $offset + $limit`
    echo $offset

    sleep 2

done # stop snagging data

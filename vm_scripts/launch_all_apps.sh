#!/bin/bash

set -e
source /usr/local/bin/tc_variables.sh


cat "$gitListFile" | while read line
do
    appName=$(cut -d, -f1)
    gitAdress=$(cur -d, -f1)
done
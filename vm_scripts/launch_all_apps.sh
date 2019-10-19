#!/bin/bash

set -e
source ./tc_variables.sh
source ./tc_functions.sh

cat "$gitListFile" | while read line
do
    appName=$(cut -d, -f1)

done
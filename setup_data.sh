#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: $0 <small|large>"
    exit 1
fi

if [ $1 == "large" ]; then
    # format all data points
    echo "Formatting all data points"
elif [ $1 == "small" ]; then
    # format 100 patients, with all long-covid patients included
    echo "Formatting 100 patients, with all long-covid patients included"
else
    echo "Invalid argument: $1. Use either 'small' or 'large'"
    exit 1
fi

#!/usr/bin/env sh

# ROUTE must be declared as an env variable
if [ -z $ROUTE ]; then
    echo "ROUTE must be declared first as an environment variable."
    exit 1
fi

# WORKING_DIR must be declared as an env variable
if [ -z $WORKING_DIR ]; then
    echo "ROUTE must be declared first as an environment variable."
    exit 1
fi

# Get json
hist_date=$( date +%Y%m%d_%H%M%S )
output_dir="$WORKING_DIR/stop/$ROUTE"
mkdir -p $output_dir
wget -O "$output_dir/${hist_date}.json" "http://www3.septa.org/hackathon/Stops/$ROUTE"


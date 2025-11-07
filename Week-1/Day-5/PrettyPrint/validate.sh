#!/bin/bash

LOG_FILE="./.husky/Logs/validation.log"



log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

if [ -d "src" ]; then
    log_message "Directory 'src/' exists."
else
    log_message "Error: Directory 'src/' does not exist!"
    echo "Directory 'src/' does not exist! Exiting."
    exit 1
fi


if [ -f "config.json" ]; then
    if jq empty config.json > /dev/null 2>&1; then
        log_message "config.json is valid."
    else
        log_message "Error: config.json is invalid JSON!"
        echo "config.json is invalid JSON! Exiting."
        exit 1
    fi
else
    log_message "Error: config.json does not exist!"
    echo "config.json does not exist! Exiting."
    exit 1
fi

log_message "Validation completed successfully."
echo "Validation completed successfully."




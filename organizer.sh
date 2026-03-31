#!/bin/bash

# Create archive folder if not exists
if [ ! -d "archive" ]; then
    mkdir archive
fi

# Check if grades.csv exists
if [ ! -f "grades.csv" ]; then
    echo "grades.csv not found!"
    exit 1
fi

# Create timestamp
timestamp=$(date +"%Y%m%d-%H%M%S")

# Rename file
new_filename="grades_$timestamp.csv"

# Move file
mv grades.csv archive/$new_filename

# Create new empty file
touch grades.csv

# Log action
echo "$timestamp - archived as $new_filename" >> organizer.log

echo "Done!"

#!/bin/bash

# Define base directory
DIR_LOGS="test_logs"

echo "Creating base directory..."
mkdir -p "$DIR_LOGS"

echo "Populating '$DIR_LOGS' with folders in a single specific format (YYYY-MM-DD)..."

# Create a sequence of dated folders
mkdir -p "$DIR_LOGS/2023-10-01"
mkdir -p "$DIR_LOGS/2023-10-02"
mkdir -p "$DIR_LOGS/2023-10-03"
mkdir -p "$DIR_LOGS/2023-10-04"
mkdir -p "$DIR_LOGS/2023-10-05"
mkdir -p "$DIR_LOGS/2023-10-06"
mkdir -p "$DIR_LOGS/2023-10-07"
mkdir -p "$DIR_LOGS/2023-10-08"

echo "Test environment created successfully!"
ls -l "$DIR_LOGS"

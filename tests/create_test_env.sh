#!/bin/bash

# Define base directories
DIR_LOGS="test_logs"
DIR_DATA="test_data"

echo "Creating base directories..."
mkdir -p "$DIR_LOGS"
mkdir -p "$DIR_DATA"

echo "Populating '$DIR_LOGS' with standard date formats (YYYY-MM-DD)..."
# Creating 6 folders so a retention limit of 3 or 5 will trigger deletions
mkdir -p "$DIR_LOGS/2023-01-01"
mkdir -p "$DIR_LOGS/2023-02-15"
mkdir -p "$DIR_LOGS/2023-03-10"
mkdir -p "$DIR_LOGS/2023-04-05"
mkdir -p "$DIR_LOGS/2023-05-20"
mkdir -p "$DIR_LOGS/2023-06-25"

echo "Populating '$DIR_DATA' with mixed formats and non-date folders..."
# YYYY_MM_DD
mkdir -p "$DIR_DATA/2023_10_01"
# DD.MM.YYYY
mkdir -p "$DIR_DATA/15.10.2023"
# YYYYMMDD
mkdir -p "$DIR_DATA/20231030"
# Text-heavy date (if dateparser handles it)
mkdir -p "$DIR_DATA/October_5_2023"

# Non-date folders to ensure the Python script safely ignores them
mkdir -p "$DIR_DATA/random_backup_files"
mkdir -p "$DIR_DATA/system_configs"

echo "Test environment created successfully!"
ls -l "$DIR_LOGS"
ls -l "$DIR_DATA"

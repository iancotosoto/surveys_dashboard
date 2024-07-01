#!/bin/bash

# Wait for the databases to be ready (for 30 seconds)
wait-for-it.sh -t 30 db:5432 -- echo "PostgreSQL is up"
wait-for-it.sh -t 30 mongodb:27017 -- echo "MongoDB is up"

# Run main process
python3 main.py
echo "Data insertion completed"
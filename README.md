# Surveys Dashboard

## Description
Using Docker and Streamlit, a web dashboard displays survey data and their results. The data is stored in PostgreSQL and MongoDB. Spark is used for data processing (ETL and OLAP).

## Objective
The Objective of this project is to demonstrate abilities used in data analysis.

## Installation
1. Resave any shell file (run.sh and start.sh)

2. Create external network
```console
docker network create dashboard_network
```

3. Build database docker
```console
docker compose -f ./apps/databases/docker-compose.yml up -d
```

4. Build spark docker
```console
docker compose -f ./apps/spark/docker-compose.yml up -d
```

5. Build dashboard docker
```console
docker compose -f ./apps/dashboard/docker-compose.yml up -d
```

6. Go to a browser and open http://localhost:8501

> **Note**: Be sure that you are in surveys_dashboard before executing all the commands. Also, to create the external network.

## Possible errors
- exec /usr/local/bin/start.sh: no such file or directory

Resave the shell file because when making the start.sh file in Windows it creates a CRLF line ending file. Linux uses LF.
Resource: https://stackoverflow.com/questions/72735140/azure-agents-with-docker-start-sh-no-such-file-or-directory 

- port is already allocated

To fix it, it is necessary to change the port in the docker to another unoccupied or eliminate the container utilizing that port.
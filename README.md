# Surveys Dashboard

## Description
Using Docker and Streamlit, a web dashboard displays survey data and their results. The data is stored in PostgreSQL and MongoDB. Spark is used for data processing (ETL and OLAP).

## Objective
The objective of this project is to demonstrate abilities used in data analysis.

## Installation
1. Build database docker
```console
docker compose -f ./apps/databases/docker-compose.yml up -d
```

2. Build spark docker
```console
docker compose -f ./apps/spark/docker-compose.yml up -d
```

3. Build dashboard docker
```console
docker compose -f ./apps/dashboard/docker-compose.yml up -d
```

4. Go to a browser and open http://localhost:8501

> **Note**: Be sure that you are in surveys_dashboard before executing all the commands

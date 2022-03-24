# JIRA K183 Backend

## Environment

To run the API, create an `.env` file using local or remote database.

    MONGODB_HOSTNAME=localhost
    MONGODB_PORT=27017
    MONGODB_USERNAME=username
    MONGODB_PASSWORD=password
    MONGODB_DATABASE=database_name
    
    API_PORT=5002

## Setup

1. Install `Docker` and `docker-compose`
2. Copy `.env.docker` to `.env`
3. Launch dockerized API, Mongo and Redis instances:
> docker-compose up -d

## Docs
Access OpenAPI documentation at `localhost:5001`

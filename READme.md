# Shopping API

## Setup

1. Install `Docker` and `docker-compose`
2. Copy `.env.docker` to `.env`
3. Launch dockerized API, Mongo and Redis instances:
> docker-compose up -d

## Integration Tests
1. Install Python 3.9.
2. Install dependencies from `requirements.txt`
3. Copy `.env.tests` to `.env`
4. Run integration tests from root directory:
> python -m unittest

**Docker Mongo and Redis instance is required.**

## Docs
Access OpenAPI documentation at `localhost:5001`
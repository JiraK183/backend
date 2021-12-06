# Shopping API

## Setup

1. Install `Docker` and `docker-compose`.
2. Launch dockerized API, Mongo and Redis instances:
> docker-compose up -d

## Integration Tests
Run integration tests in tests folder. **Python 3.9 required.**
> python -m unittest
> 
*Make sure database environment variables are set!*

## Docs
Access OpenAPI documentation at `localhost:5001`